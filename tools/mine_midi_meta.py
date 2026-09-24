#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MIDI 文件内嵌 meta 文本挖掘（全库 12.4 万文件）

很多 MIDI 文件在自身 meta 事件里写着作曲家 / 版权 / 标题 / 年份——
Cyber Hymnal 的经验证明这是高价值免费数据源。本工具通读全库，
提取文本并对齐现有字段，找出可补的缺口。

用法：
  python tools/mine_midi_meta.py --dry-run   # 只出候选报告
  python tools/mine_midi_meta.py             # 写入（备份后）
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
TRACKS = ROOT / "midi_db" / "tracks"
BACKUP = ROOT / "midi_db" / "tracks_backup"
DATA = ROOT.parent / "data" / "midi"
HEAD = 65536          # 只读前 64KB（meta 通常在最前面的轨道）

COPY_RE = re.compile(r"(©|\(c\)|copyright|all rights|public domain|pd\b)", re.I)
BY_RE = re.compile(r"^\s*(?:by|music by|composed by|composer:?)\s+(.{2,60})$", re.I)
ARR_RE = re.compile(r"\b(arr(?:anged)?|harmoniz|transcri|sequenc|typeset|editor)\b", re.I)
YEAR_RE = re.compile(r"\b(1[5-9]\d{2}|20[0-2]\d)\b")


def meta_texts(path: Path):
    """读前 HEAD 字节，解析 meta 事件文本（0x01/0x02/0x03）。"""
    try:
        with path.open("rb") as f:
            data = f.read(HEAD)
    except Exception:
        return []
    if data[:4] != b"MThd":
        return []
    out = []
    i = 8 + int.from_bytes(data[4:8], "big")
    while i < len(data) - 8:
        if data[i:i+4] != b"MTrk":
            break
        ln = int.from_bytes(data[i+4:i+8], "big")
        j = i + 8
        end = min(j + ln, len(data))
        running = None
        while j < end:
            b0 = data[j]; j += 1
            if b0 & 0x80:
                st = b0
                if st == 0xFF:
                    if j >= end: break
                    mt = data[j]; j += 1
                    ln2 = 0
                    while j < end:
                        c = data[j]; j += 1
                        ln2 = (ln2 << 7) | (c & 0x7F)
                        if not (c & 0x80): break
                    payload = data[j:j+ln2]; j += ln2
                    if mt in (0x01, 0x02, 0x03, 0x09):
                        t = payload.decode("utf-8", "replace").strip()
                        if t:
                            out.append(t[:200])
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
            if 0x80 <= st < 0xF0:
                j += 2 if not (0xD0 <= st < 0xE0) else 1
        i = j if j > i else i + 8
        if i + 8 > len(data):
            break
        i = end if end > i else i + 8
        i = (j + 7) & ~7
    return out


def guess_composer(texts, cur_name):
    """从 meta 文本猜作曲家（保守：只认 'By X' 形式且 X 像人名）。"""
    for t in texts:
        m = BY_RE.match(t)
        if not m:
            continue
        cand = m.group(1).strip().strip(".,;:")
        cand = re.sub(r"[,;]?\s*\d{4}.*$", "", cand).strip()
        if len(cand) < 3 or ARR_RE.search(cand):
            continue
        if not re.search(r"[A-Za-zÀ-ž]{3}", cand):
            continue
        if cur_name and cand.lower() in str(cur_name).lower():
            return None
        return cand
    return None


def guess_year(texts, cur_yr):
    if cur_yr:
        return None
    for t in texts:
        if COPY_RE.search(t) or BY_RE.match(t):
            m = YEAR_RE.search(t)
            if m:
                y = int(m.group(1))
                if 1400 <= y <= 2026:
                    return y
    return None


def guess_title_hint(texts):
    """文件名式标题的源（如 lakh 的 030900b）→ 从 meta 找更像标题的文本。"""
    for t in texts:
        if BY_RE.match(t) or COPY_RE.search(t):
            continue
        if 3 <= len(t) <= 80 and re.search(r"[A-Za-zÀ-ž]{3}", t) and not re.match(r"^[\d\s\-_.]+$", t):
            return t
    return None


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--limit", type=int, default=0, help="每源最多处理条数（调试）")
    args = ap.parse_args(argv[1:])

    report = {}
    out_lines = {}
    stats = Counter()
    samples = defaultdict(list)

    for fp in sorted(TRACKS.glob("*.jsonl")):
        rows = [json.loads(l) for l in fp.open(encoding="utf-8")]
        src = rows[0]["source"]
        changed = 0
        kinds = Counter()
        new_rows = []
        n = 0
        for r in rows:
            rel = r.get("midi", {}).get("file") or ""
            p = ROOT / rel if rel else None
            ch = None
            if p and p.exists() and (not args.limit or n < args.limit):
                n += 1
                texts = meta_texts(p)
                if texts:
                    ch = {}
                    c = guess_composer(texts, r.get("composer_name"))
                    if c and (not r.get("composer_name") or r.get("composer_name") == "Traditional"):
                        ch["composer_name"] = c
                        ch["composer_slug"] = re.sub(r"[^a-z0-9]+", "-", c.lower()).strip("-")
                    y = guess_year(texts, (r.get("extra") or {}).get("tune_year") or r.get("yr"))
                    if y:
                        ch["yr"] = y
                    if not r.get("title") or re.match(r"^[0-9a-z]{4,12}$", str(r.get("title") or "").strip().lower()):
                        th = guess_title_hint(texts)
                        if th and th.lower() != str(r.get("title") or "").lower():
                            ch["title_hint"] = th
                    if not ch:
                        ch = None
            if ch:
                changed += 1
                for k in ch:
                    kinds[k] += 1
                if len(samples[src]) < 4:
                    samples[src].append((r["id"], dict(ch)))
                r2 = dict(r)
                r2.update(ch)
                new_rows.append(r2)
            else:
                new_rows.append(r)
        if changed:
            report[src] = (len(rows), changed, dict(kinds))
        out_lines[src] = new_rows

    print()
    print("=== MIDI meta 挖掘报告 ===")
    tot = 0
    for src in sorted(report):
        n, c, kinds = report[src]
        tot += c
        print(f"  {src:14s} {n:>7,} 条 · 候选 {c:>7,} · {kinds}")
        for s in samples[src][:3]:
            print(f"      {s[0]} → {s[1]}")
    print(f"  合计候选 {tot:,}")

    if args.dry_run:
        print("\n[dry-run] 未写回")
        return 0

    ts = time.strftime("%Y%m%d-%H%M%S")
    bdir = BACKUP / f"pre-minemeta-{ts}"
    bdir.mkdir(parents=True, exist_ok=True)
    for fp in TRACKS.glob("*.jsonl"):
        shutil.copy2(fp, bdir / fp.name)
    print(f"\n[backup] {bdir}")
    for name, rows in out_lines.items():
        with (TRACKS / f"{name}.jsonl").open("w", encoding="utf-8", newline="\n") as fh:
            for r in rows:
                fh.write(json.dumps(r, ensure_ascii=False, separators=(",", ":")) + "\n")
    print("[write] 已写回（title_hint 需人工确认后再采用，暂只作候选字段保留）")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
