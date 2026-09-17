#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""D8 去重 v1（两阶段）→ midi_db/stats/dedup-report.md

阶段 1：MD5 完全相同文件（秒级）
阶段 2：音高序列指纹（同曲不同转录/格式，mido 解析）

输出报告含重复组明细与建议（不自动删除，供人工决策）。

用法（须用带 mido 的托管 venv python）：
  python tools/dedup.py [--phase1-only] [--limit N]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACKS = ROOT / "midi_db" / "tracks"
REPORT = ROOT / "midi_db" / "stats" / "dedup-report.md"
STATE = ROOT / "tools" / "state" / "dedup-fingerprints.json"

QUANT = 0.125    # 起始时间量化（1/8 拍）


def iter_tracks():
    for f in sorted(TRACKS.glob("*.jsonl")):
        for line in f.open(encoding="utf-8"):
            r = json.loads(line)
            p = ROOT / r["midi"]["file"]
            if p.exists():
                yield r, p


def md5_phase() -> tuple[dict, int]:
    md5_map = defaultdict(list)
    n = 0
    for r, p in iter_tracks():
        h = hashlib.md5(p.read_bytes()).hexdigest()
        md5_map[h].append({"id": r["id"], "source": r["source"],
                           "title": r.get("title") or "", "file": r["midi"]["file"]})
        n += 1
    return {h: v for h, v in md5_map.items() if len(v) > 1}, n


def pitch_fingerprint(path: Path) -> str | None:
    """音高+节奏序列指纹（跨格式/转录的近似同曲检测）。"""
    try:
        import mido
        mid = mido.MidiFile(str(path))
        notes = []
        t = 0.0
        for msg in mid:
            t += msg.time
            if msg.type == "note_on" and msg.velocity > 0:
                notes.append((round(t / QUANT), msg.note))
        if len(notes) < 8:
            return None
        # 归一化：相对首音音高 + 相对起始
        base = notes[0][1]
        t0 = notes[0][0]
        sig = ";".join(f"{q - t0}:{p - base}" for q, p in notes[:400])
        return hashlib.md5(sig.encode()).hexdigest()
    except Exception:
        return None


def load_fp_state() -> dict:
    if STATE.exists():
        return json.loads(STATE.read_text(encoding="utf-8"))
    return {}


def save_fp_state(d: dict) -> None:
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase1-only", action="store_true")
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--workers", type=int, default=8)
    args = ap.parse_args(argv[1:])

    t0 = time.time()
    md5_dups, n = md5_phase()
    print(f"[md5] {n:,} 首 · 重复组 {len(md5_dups):,}（{time.time()-t0:.0f}s）", flush=True)

    fp_dups = {}
    fp_meta = {}
    if not args.phase1_only:
        from concurrent.futures import ThreadPoolExecutor, as_completed
        cache = load_fp_state()
        fp_map = defaultdict(list)
        todo = []
        for r, p in iter_tracks():
            key = r["midi"]["file"]
            fp = cache.get(key)
            if fp is None:
                todo.append((r, p, key))
            elif fp:
                fp_map[fp].append({"id": r["id"], "source": r["source"],
                                   "title": r.get("title") or "", "file": key})
        print(f"[fp] 缓存命中 {len(cache):,} · 待计算 {len(todo):,}", flush=True)
        done = 0
        with ThreadPoolExecutor(max_workers=args.workers) as ex:
            futs = {ex.submit(pitch_fingerprint, p): (r, key) for r, p, key in todo}
            for fut in as_completed(futs):
                r, key = futs[fut]
                fp = fut.result()
                cache[key] = fp
                done += 1
                if fp:
                    fp_map[fp].append({"id": r["id"], "source": r["source"],
                                       "title": r.get("title") or "", "file": key})
                if done % 2000 == 0:
                    save_fp_state(cache)
                    print(f"  ... 指纹 {done:,}/{len(todo):,} ({time.time()-t0:.0f}s)", flush=True)
        save_fp_state(cache)
        fp_dups = {h: v for h, v in fp_map.items() if len(v) > 1}
        print(f"[fp] 指纹完成 +{done:,} · 重复组 {len(fp_dups):,}（{time.time()-t0:.0f}s）", flush=True)

    # 报告
    md5_extra = sum(len(v) - 1 for v in md5_dups.values())
    fp_extra = sum(len(v) - 1 for v in fp_dups.values())
    lines = [
        "# D8 去重报告 v1",
        "",
        f"> 生成：{datetime.now().isoformat(timespec='seconds')} · 扫描 {n:,} 首",
        "",
        "## 一、MD5 完全相同（文件级重复）",
        "",
        f"- 唯一文件 {n - md5_extra:,} · **重复组 {len(md5_dups):,}** · 冗余 {md5_extra:,} 首",
        "",
    ]
    cross = Counter()
    for v in md5_dups.values():
        cross[tuple(sorted({x["source"] for x in v}))] += 1
    if cross:
        lines += ["| 跨源组合 | 组数 |", "|---|---:|"]
        for k, c in cross.most_common(10):
            lines.append(f"| {' + '.join(k)} | {c:,} |")
        lines.append("")
        lines += ["### 样例（前 20 组）", ""]
        for h, v in list(md5_dups.items())[:20]:
            desc = " | ".join(f"{x['id']}·{x['source']}·{(x['title'] or '')[:24]}" for x in v[:3])
            lines.append(f"- {desc}")
        lines.append("")

    if fp_dups:
        lines += [
            "## 二、音高指纹重复（同曲不同版本）",
            "",
            f"- **重复组 {len(fp_dups):,}** · 冗余 {fp_extra:,} 首",
            "",
            "### 样例（前 20 组）",
            "",
        ]
        for h, v in list(fp_dups.items())[:20]:
            desc = " | ".join(f"{x['id']}·{x['source']}·{(x['title'] or '')[:22]}" for x in v[:3])
            lines.append(f"- {desc}")
        lines.append("")

    lines += [
        "## 三、处置建议",
        "",
        "1. 保留**元数据最完整**的版本（title/license/zone 齐全者优先）",
        "2. 跨源重复优先保留 `main` 分区版本（可商用），而非 research/pending",
        "3. 同源内重复（如 ariamidi 内部）保留 id 最小者",
        "4. 去重执行前自动备份至 `midi_trash/`",
    ]
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"[report] {REPORT.relative_to(ROOT)}", flush=True)
    print(f"[summary] MD5 冗余 {md5_extra:,} · 指纹冗余 {fp_extra:,}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
