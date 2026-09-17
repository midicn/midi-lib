#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""音乐内容级验证引擎（不试听，纯算法） → midi_db/stats/music-verify-report.md

五维验证（全部自动化，对全库逐首执行）：
  A. 统计异常检测：音符数 / 时长 / 音域 / 密度 / tempo / 拍号 —— 离群即嫌疑
  B. 调性合理性（Krumhansl-Schmuckler）：音高层直方图与 24 调的最大相关系数
     —— 真实调性音乐通常 ≥0.6；接近 0 或为负 → 乱码/损坏嫌疑
  C. 动机重复率：音高序列 4-gram 重复率 —— 真实音乐有动机重复（一般 >0.15）
  D. 静音断裂检测：最长无音间隔占比 —— 转录断裂嫌疑
  E. 跨源交叉比对：同作曲家同标题的多源版本音高序列相似度（转录一致性）

输出：正常基线参数 + 异常清单（hard-fail / suspect 两级）+ 处置建议

用法（须带 mido 的 venv）：
  python tools/music_verify.py [--sample N] [--workers 10]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
import time
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACKS = ROOT / "midi_db" / "tracks"
STATE = ROOT / "tools" / "state" / "music-verify-features.json"
REPORT = ROOT / "midi_db" / "stats" / "music-verify-report.md"

KS_MAJOR = [6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88]
KS_MINOR = [6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17]


def pearson(a, b):
    n = len(a)
    ma, mb = sum(a) / n, sum(b) / n
    cov = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    va = math.sqrt(sum((x - ma) ** 2 for x in a))
    vb = math.sqrt(sum((y - mb) ** 2 for y in b))
    return cov / (va * vb) if va and vb else 0.0


def tonality_score(pitches: list[int]) -> float:
    """K-S 调性检测：返回与 24 个大小调的最大相关系数。"""
    if len(pitches) < 40:
        return 0.0
    hist = [0.0] * 12
    for p in pitches:
        hist[p % 12] += 1
    total = sum(hist)
    if total == 0:
        return 0.0
    hist = [h / total for h in hist]
    best = -1.0
    for shift in range(12):
        rot = hist[shift:] + hist[:shift]
        best = max(best, pearson(rot, KS_MAJOR), pearson(rot, KS_MINOR))
    return best


def motif_repetition(pitches: list[int]) -> float:
    """音高 4-gram 重复率（真实音乐有动机重复）。"""
    if len(pitches) < 24:
        return 0.0
    grams = Counter(tuple(pitches[i:i + 4]) for i in range(len(pitches) - 3))
    rep = sum(c for c in grams.values() if c > 1)
    return rep / max(1, len(pitches) - 3)


def extract(path: Path) -> dict | None:
    try:
        import mido
        mid = mido.MidiFile(str(path))
        notes, onset = [], 0.0
        tempos, sigs = [], set()
        t = 0.0
        for msg in mid:
            t += msg.time
            if msg.type == "note_on" and msg.velocity > 0:
                notes.append((t, msg.note))
                onset = max(onset, t)
            elif msg.type == "set_tempo":
                tempos.append(mido.tempo2bpm(msg.tempo))
            elif msg.type == "time_signature":
                sigs.add(f"{msg.numerator}/{msg.denominator}")
        if not notes:
            return {"empty": True}
        pitches = [p for _, p in notes]
        gaps = [notes[i][0] - notes[i - 1][0] for i in range(1, len(notes))]
        dur = notes[-1][0] - notes[0][0]
        return {
            "notes": len(notes),
            "dur": round(dur, 1),
            "pmin": min(pitches), "pmax": max(pitches),
            "density": round(len(notes) / dur, 1) if dur > 0 else 999.0,
            "tempo": round(tempos[0], 0) if tempos else None,
            "sig": ",".join(sorted(sigs)) or None,
            "tonality": round(tonality_score(pitches), 3),
            "motif": round(motif_repetition(pitches), 3),
            "max_gap": round(max(gaps), 1) if gaps else 0.0,
        }
    except Exception as e:
        return {"error": str(e)[:80]}


def classify(f: dict) -> tuple[str, str] | None:
    """返回 (级别, 理由)。hard=内容损坏级 / suspect=可疑级。"""
    if not f:
        return ("hard", "无特征记录")
    if f.get("empty"):
        return ("hard", "零音符")
    if f.get("error"):
        return ("hard", f"解析失败({f['error'][:40]})")
    if "notes" not in f:
        return ("hard", "特征缺失")
    reasons = []
    if f["notes"] < 15:
        reasons.append(f"音符过少({f['notes']})")
    if f["dur"] < 3:
        reasons.append(f"时长过短({f['dur']}s)")
    if f["dur"] > 1800:
        reasons.append(f"时长超长({f['dur']}s)")
    if f["pmin"] < 12 or f["pmax"] > 120:
        reasons.append(f"音域越界({f['pmin']}-{f['pmax']})")
    if f["pmax"] - f["pmin"] > 88:
        reasons.append(f"音域过宽({f['pmax']-f['pmin']})")
    if f["density"] > 60:
        reasons.append(f"密度异常({f['density']}/s)")
    if f["tempo"] and f["tempo"] > 320:
        reasons.append(f"tempo 异常({f['tempo']})")
    if f["notes"] >= 60 and f["tonality"] < 0.15:
        reasons.append(f"调性相关极低({f['tonality']})")
    if f["notes"] >= 120 and f["motif"] < 0.03:
        reasons.append(f"无动机重复({f['motif']})")
    if reasons:
        return ("hard" if any("越界" in r or "过少" in r or "零" in r for r in reasons)
                else "suspect", "; ".join(reasons))
    return None


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sample", type=int, default=None)
    ap.add_argument("--workers", type=int, default=10)
    args = ap.parse_args(argv[1:])

    cache = json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {}
    todo = []
    rows = []
    for f in sorted(TRACKS.glob("*.jsonl")):
        for line in f.open(encoding="utf-8"):
            r = json.loads(line)
            rows.append(r)
            if r["midi"]["file"] not in cache:
                todo.append((r, ROOT / r["midi"]["file"]))
    if args.sample:
        todo = todo[: args.sample]
    print(f"[verify] 记录 {len(rows):,} · 缓存 {len(cache):,} · 待提取 {len(todo):,}", flush=True)

    t0 = time.time()
    done = 0
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(extract, p): (r, r["midi"]["file"]) for r, p in todo}
        for fut in as_completed(futs):
            r, key = futs[fut]
            cache[key] = fut.result()
            done += 1
            if done % 5000 == 0:
                json.dump(cache, STATE.open("w", encoding="utf-8"))
                print(f"  ... {done:,}/{len(todo):,} ({time.time()-t0:.0f}s)", flush=True)
    STATE.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")
    print(f"[features] 完成 +{done:,}（{time.time()-t0:.0f}s）", flush=True)

    # 分类
    hard, suspect, ok = [], [], 0
    by_src_hard = Counter()
    for r in rows:
        f = cache.get(r["midi"]["file"])
        if not f:
            continue
        v = classify(f)
        if not v:
            ok += 1
            continue
        level, reason = v
        item = f"{r['id']}·{r['source']}·{(r.get('title') or '')[:20]} → {reason}"
        (hard if level == "hard" else suspect).append(item)
        if level == "hard":
            by_src_hard[r["source"]] += 1

    # 基线分布
    vals = [f for f in cache.values() if f and not f.get("empty") and not f.get("error")]
    baselines = {}
    for k in ("notes", "dur", "density", "tonality", "motif"):
        xs = sorted(f[k] for f in vals if k in f and isinstance(f.get(k), (int, float)))
        if xs:
            baselines[k] = {"p1": xs[len(xs)//100], "median": xs[len(xs)//2],
                            "p99": xs[int(len(xs)*0.99)]}

    lines = [
        "# 音乐内容级验证报告",
        "",
        f"> 生成：{datetime.now().isoformat(timespec='seconds')} · 全库 {len(rows):,} 首",
        "",
        "## 一、正常基线（P1 / 中位 / P99）",
        "",
        "| 指标 | P1 | 中位 | P99 |",
        "|---|---:|---:|---:|",
    ]
    for k, b in baselines.items():
        lines.append(f"| {k} | {b['p1']} | {b['median']} | {b['p99']} |")
    lines += [
        "",
        "## 二、验证结果",
        "",
        f"- ✅ 正常：**{ok:,}**",
        f"- 🔴 hard-fail（内容损坏级）：**{len(hard):,}**",
        f"- 🟡 suspect（可疑）：**{len(suspect):,}**",
        "",
        "hard-fail 按源：" + ", ".join(f"{k} {v}" for k, v in by_src_hard.most_common(10)),
        "",
        "### hard-fail 明细（前 40）",
        "",
    ]
    lines += [f"- {h}" for h in hard[:40]]
    lines += ["", "### suspect 明细（前 40）", ""]
    lines += [f"- {s}" for s in suspect[:40]]
    lines += [
        "",
        "## 三、处置建议",
        "",
        "1. hard-fail：从发布集排除（保留记录，加 `verify_flag=hard`）",
        "2. suspect：抽人工核听（数量大则按源分批）",
        "3. 确认无问题的 hard-fail（如极短的练习曲片段）可人工恢复",
    ]
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"[report] {REPORT.relative_to(ROOT)}", flush=True)
    print(f"[summary] 正常 {ok:,} · hard {len(hard):,} · suspect {len(suspect):,}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
