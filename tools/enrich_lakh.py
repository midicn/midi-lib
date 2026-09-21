#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""lakh 补全：乐器（MIDI program change 挖掘）+ 作曲家人声/风格/编号（文件名解析）

lakh 的 9,640 首来自各种 MIDI 合集，元数据薄。但：
  ① MIDI 文件自身的 program change 事件 = 真实乐器（挖出来即有据可依）
  ② 文件名常含作曲家与目录编号（"Giuliani Op74 No1 Sostenuto" / "K309 Piano Sonata" / "mozk310a"）
用法：python tools/enrich_lakh.py [--dry-run]
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LAKH = ROOT / "midi_db/tracks/lakh.jsonl"
BACKUP = ROOT / "midi_db/tracks_backup"
HEAD = 65536

# GM 音色族（0-127）
GM_FAMILY = [
    (0, 7, "piano"), (8, 15, "chromatic percussion"), (16, 23, "organ"), (24, 31, "guitar"),
    (32, 39, "bass"), (40, 47, "strings"), (48, 55, "ensemble"), (56, 63, "brass"),
    (64, 71, "reed"), (72, 79, "pipe"), (80, 87, "synth lead"), (88, 95, "synth pad"),
    (96, 103, "fx"), (104, 111, "ethnic"), (112, 119, "percussive"), (120, 127, "sfx"),
]
# 归一到本站 instrument 词表
FAMILY_TO_OURS = {
    "piano": "piano", "guitar": "guitar", "organ": "organ", "strings": "ensemble",
    "ensemble": "ensemble", "brass": "ensemble", "reed": "ensemble", "pipe": "ensemble",
    "bass": "ensemble", "synth lead": "melody", "synth pad": "melody", "ethnic": "melody",
    "percussive": "drums", "sfx": "drums", "chromatic percussion": "drums",
}

# 文件名里的作曲家线索（词首姓氏）
NAME_HINT = {
    "bach": ("Johann Sebastian Bach", "bach"), "mozart": ("Wolfgang Amadeus Mozart", "mozart"),
    "beethoven": ("Ludwig van Beethoven", "beethoven"), "chopin": ("Frederic Chopin", "chopin"),
    "schubert": ("Franz Schubert", "schubert"), "haydn": ("Joseph Haydn", "haydn"),
    "handel": ("George Frideric Handel", "handel"), "brahms": ("Johannes Brahms", "brahms"),
    "liszt": ("Franz Liszt", "liszt"), "schumann": ("Robert Schumann", "schumann"),
    "giuliani": ("Mauro Giuliani", "giuliani"), "sor": ("Fernando Sor", "sor"),
    "tarrega": ("Francisco Tarrega", "tarrega"), "carulli": ("Ferdinando Carulli", "carulli"),
    "carcassi": ("Matteo Carcassi", "carcassi"), "aguado": ("Dionisio Aguado", "aguado"),
    "coste": ("Napoleon Coste", "coste"), "mertz": ("Johann Kaspar Mertz", "mertz"),
    "paganini": ("Niccolo Paganini", "paganini"), "villa": ("Heitor Villa-Lobos", "villa-lobos"),
    "telemann": ("Georg Philipp Telemann", "telemann"), "vivaldi": ("Antonio Vivaldi", "vivaldi"),
    "scarlatti": ("Domenico Scarlatti", "scarlatti"), "mendelssohn": ("Felix Mendelssohn", "mendelssohn"),
    "grieg": ("Edvard Grieg", "grieg"), "tchaikovsky": ("Pyotr Tchaikovsky", "tchaikovsky"),
    "debussy": ("Claude Debussy", "debussy"), "satis": ("Erik Satie", "satie"),
}
CAT_RE = re.compile(r"\b(bwv|kv|k|op|d|hob)\s*[.\s]?\s*(\d{1,4})", re.I)
ID_RE = re.compile(r"^(bwv|mozk|k)(\d{1,4})", re.I)


def gm_family(prog: int) -> str:
    for lo, hi, name in GM_FAMILY:
        if lo <= prog <= hi:
            return name
    return "unknown"


def mine_instrument(path: Path):
    """读 MIDI：统计各通道 program 与音符数 → 主乐器族。"""
    try:
        with path.open("rb") as f:
            data = f.read(HEAD)
    except Exception:
        return None
    if data[:4] != b"MThd":
        return None
    prog = defaultdict(lambda: 0)      # channel → program
    notes = Counter()                  # channel → note count
    fam_note = Counter()               # family → weighted notes
    i = 8 + int.from_bytes(data[4:8], "big")
    while i < len(data) - 8 and data[i:i+4] == b"MTrk":
        ln = int.from_bytes(data[i+4:i+8], "big")
        j, end = i + 8, min(i + 8 + ln, len(data))
        running = None
        while j < end:
            b0 = data[j]; j += 1
            if b0 & 0x80:
                st = b0
                if st == 0xFF:
                    if j >= end: break
                    j += 1
                    ln2 = 0
                    while j < end:
                        c = data[j]; j += 1
                        ln2 = (ln2 << 7) | (c & 0x7F)
                        if not (c & 0x80): break
                    j += ln2
                    continue
                if st in (0xF0, 0xF7):
                    ln2 = 0
                    while j < end:
                        c = data[j]; j += 1
                        ln2 = (ln2 << 7) | (c & 0x7F)
                        if not (c & 0x80): break
                    j += ln2
                    continue
                running = st
            else:
                st = running
            if st is None:
                continue
            hi, ch = st & 0xF0, st & 0x0F
            if hi == 0xC0:                      # program change
                if j < end:
                    prog[ch] = data[j]; j += 1
            elif hi == 0x90:                    # note on
                if j + 1 < end:
                    if data[j+1] > 0:
                        notes[ch] += 1
                    j += 2
            elif hi in (0x80, 0xA0, 0xB0, 0xE0):
                j += 2
            elif hi == 0xD0:
                j += 1
        i = (j + 7) & ~7
    if not notes:
        return None
    for ch, n in notes.items():
        fam = gm_family(prog.get(ch, 0)) if ch != 9 else "percussive"
        fam_note[fam] += n
    top = fam_note.most_common(1)[0][0]
    return FAMILY_TO_OURS.get(top, "melody")


def parse_name(r):
    """文件名/标题 → composer / opus / genre 线索。"""
    ch = {}
    t = (r.get("title") or "").strip()
    low = t.lower()
    # 编号体系
    m = ID_RE.match(low) or CAT_RE.search(low)
    comp_now = r.get("composer_name")
    if m:
        pre, num = m.group(1).lower(), m.group(2)
        scheme = {"bwv": ("bach", "BWV"), "kv": ("mozart", "K."), "k": ("mozart", "K."),
                  "op": (None, "Op."), "d": ("schubert", "D."), "hob": ("haydn", "Hob.")}.get(pre)
        if pre == "mozk":
            scheme = ("mozart", "K.")
        if scheme:
            slug, label = scheme
            if not r.get("opus"):
                ch["opus"] = int(num) if num.isdigit() else num
            if slug:
                # 编号体系是比文件夹更硬的证据：BWV→Bach / K.→Mozart / D.→Schubert / Hob.→Haydn
                # （例如放在 Bach 目录里的 K518 其实是莫扎特作品——以编号为准）
                full = {"bach": ("Johann Sebastian Bach", "bach"), "mozart": ("Wolfgang Amadeus Mozart", "mozart"),
                        "schubert": ("Franz Schubert", "schubert"), "haydn": ("Joseph Haydn", "haydn")}[slug]
                if (r.get("composer_slug") or "") != full[1]:
                    ch["composer_name"] = full[0]
                    ch["composer_slug"] = full[1]
    # 文件名里的作曲家姓氏
    if not ch.get("composer_name") and (not comp_now or comp_now == "Traditional"):
        for key, (full, slug) in NAME_HINT.items():
            if re.search(rf"\b{key}\b", low):
                ch["composer_name"] = full
                ch["composer_slug"] = slug
                break
    return ch


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args(argv[1:])

    rows = [json.loads(l) for l in LAKH.open(encoding="utf-8")]
    changed = 0
    kinds = Counter()
    inst_dist = Counter()
    samples = []
    out = []
    n = 0
    for r in rows:
        ch = parse_name(r)
        inst = None
        rel = (r.get("midi") or {}).get("file")
        p = ROOT / rel if rel else None
        if p and p.exists() and not r.get("instrument") and (not args.limit or n < args.limit):
            n += 1
            inst = mine_instrument(p)
            if inst:
                ch["instrument"] = inst
                inst_dist[inst] += 1
        if ch:
            changed += 1
            for k in ch:
                kinds[k] += 1
            if len(samples) < 8:
                samples.append((r["id"], r.get("title"), dict(ch)))
            r2 = dict(r); r2.update(ch); out.append(r2)
        else:
            out.append(r)
    print()
    print("=== lakh 收尾报告 ===")
    print(f"  条数 {len(rows):,} · 改动 {changed:,} · 字段 {dict(kinds)}")
    print(f"  乐器分布: {dict(inst_dist.most_common(10))}")
    for s in samples:
        print(f"    {s[0]}  {str(s[1])[:36]:38s} → {s[2]}")
    if args.dry_run:
        print("\n[dry-run] 未写回")
        return 0
    ts = time.strftime("%Y%m%d-%H%M%S")
    bdir = BACKUP / f"pre-lakh-{ts}"
    bdir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(LAKH, bdir / LAKH.name)
    print(f"\n[backup] {bdir}")
    with LAKH.open("w", encoding="utf-8", newline="\n") as fh:
        for r in out:
            fh.write(json.dumps(r, ensure_ascii=False, separators=(",", ":")) + "\n")
    print("[write] lakh.jsonl 已更新")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
