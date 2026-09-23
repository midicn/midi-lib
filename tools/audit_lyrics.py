# -*- coding: utf-8 -*-
"""审计 MIDI 内嵌歌词（lyrics_inline）的来源/档位/许可分布，为歌词版权定性。"""
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACKS = ROOT / "midi_db" / "tracks"

by_src = Counter()          # 有内嵌歌词的曲目数（按来源）
zone_of = defaultdict(Counter)
lic_of = defaultdict(Counter)
title_src = defaultdict(list)
field_names = Counter()
total = 0
sample = defaultdict(list)

for f in sorted(TRACKS.glob("*.jsonl")):
    for line in f.open(encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        try:
            r = json.loads(line)
        except Exception:
            continue
        total += 1
        midi = r.get("midi") or {}
        for k in midi.keys():
            if "lyric" in k.lower():
                field_names[f"midi.{k}"] += 1
        ex = r.get("extra") or {}
        for k in ex.keys():
            if "lyric" in k.lower():
                field_names[f"extra.{k}"] += 1
        if "lyrics_incomplete" in r:
            field_names["top.lyrics_incomplete"] += 1

        li = midi.get("lyrics_inline")
        if not li:
            continue
        src = r.get("source")
        by_src[src] += 1
        zone_of[src][r.get("zone")] += 1
        lic_of[src][r.get("license")] += 1
        title_src[src].append((r.get("id"), r.get("title"), r.get("composer_name"), len(li) if isinstance(li, str) else len(str(li))))
        if len(sample[src]) < 3 and isinstance(li, str):
            sample[src].append(li[:180].replace("\n", " / "))

print(f"总记录 {total:,}")
print(f"\n=== 含内嵌歌词的字段统计 ===")
for k, v in field_names.most_common():
    print(f"  {k:32} {v:>8,}")

tot = sum(by_src.values())
print(f"\n=== 含内嵌歌词曲目：{tot:,} 首 ===")
print(f"{'来源':14} {'曲目':>6}  {'档位':22} 许可")
for src, n in by_src.most_common():
    z = ", ".join(f"{k}={v}" for k, v in zone_of[src].most_common())
    l = ", ".join(f"{k}={v}" for k, v in lic_of[src].most_common())
    print(f"{src:14} {n:>6}  {z:22} {l}")

print("\n=== 歌词样例 ===")
for src in sorted(sample):
    print(f"\n--- {src} ---")
    for s in sample[src]:
        print(f"    {s!r}")
