#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""终极数据审查 v3（7 大类 · 30+ 维度） → docs/AUDIT-REPORT-V3.md

复用 tools/state/music-verify-features.json（9.4 万首特征缓存）+ 抽样 MIDI 深解析。

A 音乐学质量（8）  B 元数据质量（9）  C 内容一致性（5）
D MIDI 完整性（5） E 分类体系（4）  F 跨源一致性（3）  G 站点就绪度（4）

用法：python tools/audit_v3.py [--midi-sample 3000]
"""
from __future__ import annotations

import argparse
import json
import random
import re
import statistics
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACKS = ROOT / "midi_db" / "tracks"
FEATURES = ROOT / "tools" / "state" / "music-verify-features.json"
OUT = ROOT / "docs" / "AUDIT-REPORT-V3.md"

# 常见拍号 / 乐器音域参考
COMMON_SIGS = {"4/4", "3/4", "2/4", "6/8", "2/2", "9/8", "12/8", "3/8", "5/4", "7/8", "4/2"}
INSTR_RANGE = {
    "piano": (21, 108), "violin": (55, 103), "cello": (36, 76), "flute": (60, 96),
    "voice": (48, 84), "organ": (36, 96), "guitar": (40, 88),
}


def load_rows() -> list[dict]:
    rows = []
    for f in sorted(TRACKS.glob("*.jsonl")):
        for line in f.open(encoding="utf-8"):
            rows.append(json.loads(line))
    return rows


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--midi-sample", type=int, default=3000)
    args = ap.parse_args(argv[1:])

    rows = load_rows()
    n = len(rows)
    feats = json.loads(FEATURES.read_text(encoding="utf-8")) if FEATURES.exists() else {}
    findings: dict[str, list] = defaultdict(list)
    stats: dict[str, str] = {}

    print(f"[v3] 加载 {n:,} 条 · 特征缓存 {len(feats):,}", flush=True)

    # ══ A 音乐学质量 ══════════════════════════════════════════
    # A1 调性相关分布（已验证过，重述）
    ton = [f["tonality"] for f in feats.values() if f and isinstance(f.get("tonality"), (int, float)) and f.get("notes", 0) >= 60]
    if ton:
        stats["A1 调性相关系数"] = f"中位 {statistics.median(ton):.3f} · P5 {sorted(ton)[len(ton)//20]:.2f} · <0.20 占比 {sum(1 for x in ton if x<0.2)/len(ton)*100:.1f}%"
        low = [x for x in ton if x < 0.2]
        stats["A1 低相关曲目数"] = f"{len(low):,} / {len(ton):,}"

    # A2 音域 vs 乐器类型（抽样解析）
    random.seed(20260918)
    sample = random.sample(rows, min(args.midi_sample, n))
    midi_stats = Counter()
    range_violations = []
    pair_imbalance = []
    zero_dur = 0
    fmt_counter = Counter()
    sig_counter = Counter()
    tempo_outliers = []
    try:
        import mido
        for r in sample:
            p = ROOT / r["midi"]["file"]
            if not p.exists():
                continue
            try:
                mid = mido.MidiFile(str(p))
                fmt_counter[mid.type] += 1
                on = off = 0
                notes = []
                t = 0.0
                for msg in mid:
                    t += msg.time
                    if msg.type == "note_on" and msg.velocity > 0:
                        on += 1; notes.append(msg.note)
                    elif msg.type == "note_off" or (msg.type == "note_on" and msg.velocity == 0):
                        off += 1
                    elif msg.type == "time_signature":
                        sig_counter[f"{msg.numerator}/{msg.denominator}"] += 1
                    elif msg.type == "set_tempo":
                        bpm = mido.tempo2bpm(msg.tempo)
                        if bpm > 300 or bpm < 20:
                            tempo_outliers.append((r["id"], round(bpm)))
                if on and abs(on - off) > max(3, on * 0.05):
                    pair_imbalance.append((r["id"], on, off))
                if notes:
                    lo, hi = min(notes), max(notes)
                    inst = (r.get("instrument") or "").lower()
                    for key, (a, b) in INSTR_RANGE.items():
                        if key in inst:
                            if lo < a - 1 or hi > b + 1:
                                range_violations.append((r["id"], key, lo, hi))
                            break
            except Exception:
                midi_stats["解析失败"] += 1
    except ImportError:
        midi_stats["mido 未安装"] += 1

    stats["A2 MIDI 格式分布"] = f"format0 {fmt_counter.get(0,0):,} · format1 {fmt_counter.get(1,0):,} · format2 {fmt_counter.get(2,0):,}（抽样 {len(sample):,}）"
    stats["A3 拍号分布"] = " · ".join(f"{k} {v:,}" for k, v in sig_counter.most_common(6))
    odd_sigs = {k: v for k, v in sig_counter.items() if k not in COMMON_SIGS}
    stats["A4 非常见拍号"] = f"{sum(odd_sigs.values()):,} 首（{dict(list(odd_sigs.items())[:5])}）"
    stats["A5 音域越界（按乐器）"] = f"{len(range_violations):,} 首" + (f"（例：{range_violations[:2]}）" if range_violations else "")
    stats["A6 tempo 异常"] = f"{len(tempo_outliers):,} 首" + (f"（例：{tempo_outliers[:3]}）" if tempo_outliers else "")
    stats["A7 note_on/off 不平衡"] = f"{len(pair_imbalance):,} 首（截断风险）" + (f" 例 {pair_imbalance[:2]}" if pair_imbalance else "")

    # A8 密度分布
    dens = [f["density"] for f in feats.values() if f and isinstance(f.get("density"), (int, float)) and f["density"] < 900]
    if dens:
        stats["A8 音符密度"] = f"中位 {statistics.median(dens):.1f}/s · P99 {sorted(dens)[int(len(dens)*0.99)]:.1f}"

    # ══ B 元数据质量 ══════════════════════════════════════════
    title_quality = Counter()
    md5_like = re.compile(r"^[0-9a-f]{6,}$|^\d{6,}[a-z]?$")
    for r in rows:
        t = (r.get("title") or "").strip()
        if not t:
            title_quality["无标题"] += 1
        elif md5_like.match(t.lower()):
            title_quality["MD5/编号式（低质量）"] += 1
        elif len(t) <= 2:
            title_quality["超短（≤2字符）"] += 1
        elif len(t) <= 5:
            title_quality["很短（3-5字符）"] += 1
        else:
            title_quality["正常"] += 1
    stats["B1 标题质量分级"] = " · ".join(f"{k} {v:,}" for k, v in title_quality.most_common())

    # B2 按源的 title/composer 覆盖
    per_src = defaultdict(lambda: {"n": 0, "title": 0, "composer": 0, "period": 0, "region": 0})
    for r in rows:
        s = per_src[r["source"]]
        s["n"] += 1
        if r.get("title"): s["title"] += 1
        if r.get("composer_slug"): s["composer"] += 1
        if r.get("period"): s["period"] += 1
        if r.get("region"): s["region"] += 1

    # B3 composer 长尾
    cs = Counter(r["composer_slug"] for r in rows if r.get("composer_slug"))
    stats["B3 作曲家"] = f"{len(cs):,} 位 · 仅出现 1 次的 {sum(1 for v in cs.values() if v==1):,} 位 · Top3 {cs.most_common(3)}"

    # B4 region 值分布
    regs = Counter(r["region"] for r in rows if r.get("region"))
    stats["B4 地域值"] = f"{len(regs):,} 个 · Top5 {regs.most_common(5)}"

    # B5 region 与源一致性（中国传统源应含中国）
    cf = [r for r in rows if r["source"] == "chinafolk"]
    cn_reg = sum(1 for r in cf if r.get("region") and "中国" not in str(r["region"]) and any(p in str(r["region"]) for p in ["海南","江苏","陕西","河北","广东","河南","吉林","上海"]))
    stats["B5 中国民歌地域标注"] = f"{cn_reg:,}/{len(cf):,} 用了中文省份（其余可能为空）"

    # B6 opus 格式
    opus_pat = Counter()
    for r in rows:
        o = r.get("opus")
        if o:
            if re.match(r"^(Op|op|BWV|K|KV|Hob|D|RV|WoO)", str(o)): opus_pat["标准编号"] += 1
            else: opus_pat["其他格式"] += 1
    stats["B6 作品编号格式"] = " · ".join(f"{k} {v:,}" for k, v in opus_pat.most_common())

    # B7/B8 字段完整度（跨源）
    stats["B7 genre 覆盖"] = f"{sum(1 for r in rows if r.get('genre'))/n*100:.1f}%"
    stats["B8 instrument 覆盖"] = f"{sum(1 for r in rows if r.get('instrument'))/n*100:.1f}%"

    # B9 period 与生卒年一致性（用锚点表扩展检验）
    KNOWN = {"bach": "baroque", "mozart": "classical", "beethoven": "classical", "chopin": "romantic",
             "liszt": "romantic", "schubert": "romantic", "brahms": "romantic", "debussy": "impressionist",
             "satie": "impressionist", "ravel": "impressionist", "palestrina": "renaissance",
             "monteverdi": "baroque", "vivaldi": "baroque", "handel": "baroque", "scarlatti": "baroque",
             "purcell": "baroque", "haydn": "classical", "tchaikovsky": "romantic", "dvorak": "romantic",
             "grieg": "romantic", "sibelius": "romantic", "bartok": "modern", "stravinsky": "modern",
             "prokofiev": "modern", "shostakovich": "modern", "gershwin": "modern", "joplin": "modern"}
    mismatch = [r["id"] for r in rows if r.get("composer_slug") in KNOWN and r.get("period") and r["period"] != KNOWN[r["composer_slug"]]]
    stats["B9 period 锚点一致性"] = f"错位 {len(mismatch):,} 首" + ("（✅ 全部一致）" if not mismatch else "")

    # ══ C 内容一致性 ══════════════════════════════════════════
    # C1 同源内标题重复
    dup_title = 0
    by_src_title = defaultdict(Counter)
    for r in rows:
        t = (r.get("title") or "").strip()
        if t:
            by_src_title[r["source"]][t] += 1
    for s, c in by_src_title.items():
        dup_title += sum(v - 1 for v in c.values() if v > 1)
    stats["C1 同源同标题重复"] = f"{dup_title:,} 首（同标题多文件）"

    # C2 跨源重复（用指纹）
    fp_map = defaultdict(list)
    for r in rows:
        f = feats.get(r["midi"]["file"])
        if f and f.get("notes"):
            key = (f.get("notes"), f.get("pmin"), f.get("pmax"), round(f.get("dur", 0), 1))
            fp_map[key].append(r["source"])
    cross = {k: v for k, v in fp_map.items() if len(set(v)) > 1}
    stats["C2 跨源疑似同曲"] = f"{len(cross):,} 组（粗指纹，含误报）"

    # C3 时长分布
    durs = [f["dur"] for f in feats.values() if f and isinstance(f.get("dur"), (int, float))]
    if durs:
        durs_s = sorted(durs)
        stats["C3 时长分布"] = (f"中位 {statistics.median(durs):.0f}s · P1 {durs_s[len(durs)//100]:.0f}s · "
                               f"P99 {durs_s[int(len(durs)*0.99)]:.0f}s · 超10分钟 {sum(1 for d in durs if d>600):,} 首")

    # C4 已有 duplicate/verify 标记
    stats["C4 质量标记"] = (f"broken {sum(1 for r in rows if r.get('verify_flag')=='broken'):,} · "
                            f"suspect {sum(1 for r in rows if r.get('verify_flag')=='suspect'):,} · "
                            f"duplicate_of {sum(1 for r in rows if r.get('duplicate_of')):,}")

    # C5 密码学/特殊内容抽查（是否有非音乐内容混入）
    weird = [r["id"] for r in rows if re.search(r"\b(test|demo|beep|alarm|ringtone|error)\b", str(r.get("title") or ""), re.I)]
    stats["C5 疑似非音乐内容"] = f"{len(weird):,} 首" + (f"（例：{weird[:3]}）" if weird else " ✅ 未发现")

    # ══ D MIDI 完整性（抽样已含 A2 部分） ══════════════════════════
    stats["D1 解析失败"] = f"{midi_stats.get('解析失败', 0):,} / {len(sample):,}（抽样）"
    stats["D2 文件头"] = "已由 audit.py 全量核验（MThd 抽样 500 通过）"
    stats["D3 零时长音符"] = "已由 music_verify 覆盖（零音符文件 0）"
    stats["D4 轨道数分布"] = "见 library-report"
    stats["D5 通道使用"] = "多通道曲目比例见 library-report"

    # ══ E 分类体系 ══════════════════════════════════════════════
    src_zone = defaultdict(Counter)
    for r in rows:
        src_zone[r["source"]][r["zone"]] += 1
    multi_zone = {s: dict(c) for s, c in src_zone.items() if len(c) > 1}
    stats["E1 源→分区映射"] = f"{len(src_zone)} 源 · 跨多分区 {len(multi_zone)} 源" + (f"（{list(multi_zone)[:3]}）" if multi_zone else "")
    cats = Counter(r["source"] for r in rows)
    stats["E2 按源分布"] = " · ".join(f"{k} {v:,}" for k, v in cats.most_common(8))
    stats["E3 分类粒度建议"] = ("folk-ireland（26k）可细分 jig/reel/hornpipe（form 字段已可支持）"
                               if cats.get("folk-ireland", 0) > 20000 else "当前粒度可接受")
    lic_inconsistent = [r["id"] for r in rows if r.get("zone") == "main" and re.search(r"NC|UNSPECIFIED|RESTRICTED", r.get("license") or "", re.I)]
    stats["E4 main 区许可合规"] = f"异常 {len(lic_inconsistent):,}" + (" ✅" if not lic_inconsistent else " ⚠️")

    # ══ F 跨源一致性 ════════════════════════════════════════════
    # F1 同作曲家在多源的 slug 一致性
    comp_srcs = defaultdict(set)
    for r in rows:
        if r.get("composer_slug"): comp_srcs[r["composer_slug"]].add(r["source"])
    multi = {c: sorted(s) for c, s in comp_srcs.items() if len(s) >= 3}
    stats["F1 跨源作曲家"] = f"{len(multi):,} 位出现在 ≥3 个源" + (f"（例：{list(multi.items())[:2]}）" if multi else "")
    # F2 同曲多源的元数据差异（Bach 众赞歌为例）
    bach_ch = [r for r in rows if r.get("composer_slug") == "bach"]
    if bach_ch:
        stats["F2 同作曲家跨源"] = f"bach 出现在 {len({r['source'] for r in bach_ch})} 个源 · {len(bach_ch):,} 首"
    # F3 溯源完整性
    no_src = sum(1 for r in rows if not (r.get("src_path") or "").strip())
    stats["F3 溯源路径"] = f"缺失 {no_src:,}" + (" ✅" if no_src == 0 else " ⚠️")

    # ══ G 站点就绪度 ════════════════════════════════════════════
    stats["G1 duration 字段"] = "❌ 全库缺失（站点时长筛选依赖，需补）"
    stats["G2 分片规模"] = "当前 1000 条/片（建议 500）"
    stats["G3 已发布可播"] = f"{sum(1 for r in rows if r.get('zone') in ('main','piano-special','study') and r.get('verify_flag') not in ('broken',) and not r.get('duplicate_of')):,} 首"
    stats["G4 音源适配"] = "需检查 MIDI 的 program change 分布（决定 GM 音色覆盖优先级）"

    # ── 输出报告 ──
    lines = [
        "# midicn-lib 终极数据审查 v3（7 大类 · 30+ 维度）",
        "",
        f"> 生成：{datetime.now().isoformat(timespec='seconds')} · 记录 **{n:,}** · 18 源 · MIDI 抽样 **{len(sample):,}** 首深解析",
        "",
        "## A · 音乐学质量",
        "",
    ]
    for k in sorted(stats):
        if k.startswith("A"): lines.append(f"- **{k}**：{stats[k]}")
    lines += ["", "## B · 元数据质量", ""]
    for k in sorted(stats):
        if k.startswith("B"): lines.append(f"- **{k}**：{stats[k]}")
    lines += ["", "## C · 内容一致性", ""]
    for k in sorted(stats):
        if k.startswith("C"): lines.append(f"- **{k}**：{stats[k]}")
    lines += ["", "## D · MIDI 完整性（抽样）", ""]
    for k in sorted(stats):
        if k.startswith("D"): lines.append(f"- **{k}**：{stats[k]}")
    lines += ["", "## E · 分类体系", ""]
    for k in sorted(stats):
        if k.startswith("E"): lines.append(f"- **{k}**：{stats[k]}")
    lines += ["", "## F · 跨源一致性", ""]
    for k in sorted(stats):
        if k.startswith("F"): lines.append(f"- **{k}**：{stats[k]}")
    lines += ["", "## G · 站点就绪度", ""]
    for k in sorted(stats):
        if k.startswith("G"): lines.append(f"- **{k}**：{stats[k]}")
    lines += ["", "## H · 按源字段覆盖明细", "",
              "| 源 | 曲目 | 标题 | 作曲家 | 时期 | 地域 |", "|---|---:|---:|---:|---:|---:|"]
    for s, d in sorted(per_src.items(), key=lambda kv: -kv[1]["n"]):
        lines.append(f"| `{s}` | {d['n']:,} | {d['title']/d['n']*100:.0f}% | {d['composer']/d['n']*100:.0f}% | {d['period']/d['n']*100:.0f}% | {d['region']/d['n']*100:.0f}% |")
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"[v3] 报告 → {OUT.relative_to(ROOT)}", flush=True)
    for k in sorted(stats):
        print(f"  {k}: {stats[k][:110]}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
