#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cyber Hymnal 接入器（源 id = cyberhymnal）

输入：
  sources/cyberhymnal/mid/**/*.mid          12,885 首赞美诗曲调（Tune）
  sources/cyberhymnal/idx/tch-idx.txt       官方索引：赞美诗标题 → 主 MIDI 曲调名

许可依据（站点 copyrite.htm 原文）：
  "Material on our site which does not have a copyright notice is ... in the public domain.
   You may post our public domain MIDI files, scores, pictures, etc. on another Web site,
   provided you attribute them to the Cyber Hymnal™ & include a link ..."
  → **署名即可再分发**；有版权的曲目在文件 meta 里会标注版权方。
  本接入器**只保留 meta 中标注 "Public Domain" 的曲调**，其余一律排除。

输出：data/midi/cyberhymnal/b*/cyberhymnal-bXXX-NNNNN.mid + midi_db/tracks/cyberhymnal.jsonl
用法：
  python tools/ingest_cyberhymnal.py [--jsonl-only]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "sources" / "cyberhymnal" / "mid"
IDX = ROOT / "sources" / "cyberhymnal" / "idx" / "tch-idx.txt"
OUT_JSONL = ROOT / "midi_db" / "tracks" / "cyberhymnal.jsonl"
DST = ROOT / "data" / "midi" / "cyberhymnal"

SOURCE_ID = "cyberhymnal"
LICENSE = "PD"
ZONE = "main"
BUCKET = 1000


def slugify(s: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return s or "unknown"


def period_from_year(y):
    if not y:
        return None
    if y < 1600:
        return "renaissance"
    if y < 1750:
        return "baroque"
    if y < 1820:
        return "classical"
    if y < 1900:
        return "romantic"
    if y < 1945:
        return "modern"
    return "contemporary"


def meta_texts(data: bytes):
    """极简 MIDI 解析：抓 0x01 文本 / 0x02 版权事件。"""
    out = []
    if data[:4] != b"MThd":
        return out
    i = 8 + int.from_bytes(data[4:8], "big")
    while i < len(data) - 8:
        if data[i:i+4] != b"MTrk":
            break
        ln = int.from_bytes(data[i+4:i+8], "big")
        j = i + 8
        end = j + ln
        running = None
        while j < end:
            while j < end:
                b0 = data[j]; j += 1
                if not (b0 & 0x80):
                    break
            if j >= end:
                break
            st = data[j]
            if st & 0x80:
                j += 1
                running = st
            else:
                st = running
            if st == 0xFF:
                mt = data[j]; j += 1
                ln2 = 0
                while True:
                    b0 = data[j]; j += 1
                    ln2 = (ln2 << 7) | (b0 & 0x7F)
                    if not (b0 & 0x80):
                        break
                payload = data[j:j+ln2]
                j += ln2
                if mt in (0x01, 0x02, 0x03):
                    out.append(payload.decode("utf-8", "replace").strip())
            elif st in (0xF0, 0xF7):
                ln2 = 0
                while True:
                    b0 = data[j]; j += 1
                    ln2 = (ln2 << 7) | (b0 & 0x7F)
                    if not (b0 & 0x80):
                        break
                j += ln2
            elif st is None:
                j += 1
            elif 0x80 <= st < 0xF0:
                j += 2 if not (0xD0 <= st < 0xE0) else 1
            else:
                j += 1
        i = end
    return out


def parse_composer(texts):
    """meta 文本 -> (composer, year)。格式如 'By Ira David Sankey, 1902'。"""
    year = None
    name = None
    for t in texts:
        if t.lower().startswith("by ") or "arranged" in t.lower() or "harmonized" in t.lower():
            name = t
            m = re.search(r"(\d{4})", t)
            if m:
                year = int(m.group(1))
            break
    return name, year


def clean_composer(name):
    """'By Ira David  Sankey, 1902' -> 'Ira David Sankey'"""
    if not name:
        return None
    n = re.sub(r"^By\s+", "", name.strip(), flags=re.I)
    n = re.sub(r"[,\s]*\d{4}\s*$", "", n)
    n = re.sub(r"\s+", " ", n).strip(" ,")
    return n or None


def load_index():
    """tune_name(lower) -> [title, ...]（保持索引顺序）"""
    tunes = defaultdict(list)
    for line in IDX.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^(.{1,70}?)\s{2,}(\S+)$", line.strip())
        if not m:
            continue
        title, tune = m.group(1).strip(), m.group(2).strip()
        if title.upper() in ("TITLE", "PRIMARY MIDI FILE") or title.startswith("©"):
            continue
        if "Cyber Hymnal" in title and "Index" in title:
            continue
        tunes[tune.lower()].append(title)
    return tunes


def midi_stats(path: Path):
    try:
        import mido
        mid = mido.MidiFile(path)
        notes = sum(1 for tr in mid.tracks for msg in tr
                    if msg.type == "note_on" and msg.velocity > 0)
        return round(mid.length, 1), notes
    except Exception:  # noqa: BLE001
        return None, None


def collect():
    files = sorted(SRC.rglob("*.mid"))
    tunes = load_index()
    print(f"[collect] midi = {len(files):,} · 索引曲调 = {len(tunes):,}")
    rows = []
    n_pd = n_copy = n_nometa = 0
    for f in files:
        stem = f.stem
        if stem.endswith("-o"):            # 管风琴变奏版：跳过，只留主版本
            continue
        texts = meta_texts(f.read_bytes())
        is_pd = any(t.lower() == "public domain" for t in texts)
        if not texts:
            n_nometa += 1
        if not is_pd:
            n_copy += 1
            continue
        n_pd += 1
        composer, year = parse_composer(texts)
        titles = tunes.get(stem.lower(), [])
        rows.append({
            "src": f, "tune": stem, "title": titles[0] if titles else stem.replace("_", " ").title(),
            "alt_titles": len(titles) - 1, "composer": composer, "year": year,
        })
    print(f"  公有领域(PD): {n_pd:,} · 有版权(排除): {n_copy:,} · 无 meta: {n_nometa:,}")
    rows.sort(key=lambda x: (x["tune"], x["title"]))
    for seq, r in enumerate(rows):
        bucket = seq // BUCKET
        r["seq"] = seq
        r["midi_rel"] = f"data/midi/{SOURCE_ID}/b{bucket:03d}/{SOURCE_ID}-b{bucket:03d}-{seq % BUCKET:05d}.mid"
    return rows


def copy_files(rows):
    n = 0
    for r in rows:
        target = ROOT / r["midi_rel"]
        if target.exists() and target.stat().st_size == r["src"].stat().st_size:
            n += 1
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(r["src"], target)
        n += 1
    print(f"[copy] {n:,}/{len(rows):,} files -> {DST}")


def write_jsonl(rows):
    final = []
    dup = 0
    seen = set()
    for r in rows:
        md5 = hashlib.md5(r["src"].read_bytes()).hexdigest()
        if md5 in seen:
            dup += 1
            continue
        seen.add(md5)
        dur, notes = midi_stats(r["src"])
        final.append({
            "id": f"{SOURCE_ID}-{r['seq']:06d}",
            "source": SOURCE_ID,
            "src_path": f"sources/cyberhymnal/mid/{r['tune'][0]}/{r['src'].relative_to(SRC).as_posix()}",
            "title": r["title"],
            "composer_slug": slugify(clean_composer(r["composer"]) or "traditional"),
            "composer_name": clean_composer(r["composer"]) or "Traditional",
            "opus": None,
            "no": None,
            "genre": "hymn",
            "form": None,
            "key": None,
            "period": period_from_year(r["year"]),
            "region": None,
            "instrument": "organ",
            "license": LICENSE,
            "zone": ZONE,
            "midi": {"file": r["midi_rel"], "duration_sec": dur, "note_count": notes,
                     "tracks_count": None, "bpm": None},
            "fingerprint": md5,
            "extra": {"source": "The Cyber Hymnal™ (hymntime.com/tch)",
                      "tune": r["tune"], "tune_year": r["year"],
                      "alt_titles": r["alt_titles"],
                      "attribution": "The Cyber Hymnal™ — hymntime.com/tch"},
        })
    OUT_JSONL.parent.mkdir(parents=True, exist_ok=True)
    with OUT_JSONL.open("w", encoding="utf-8", newline="\n") as f:
        for r in final:
            f.write(json.dumps(r, ensure_ascii=False, separators=(",", ":")) + "\n")
    print(f"[jsonl] {len(final):,} rows -> {OUT_JSONL}")
    print(f"  内容重复剔除: {dup} · 时长缺失: {sum(1 for x in final if not x['midi']['duration_sec'])}")
    print("  period 分布:", dict(Counter(x["period"] for x in final)))
    print("  作曲家数:", len({x["composer_slug"] for x in final}))
    print("  样例:", [(x["title"][:28], x["composer_name"][:22]) for x in final[:3]])
    return len(final)


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--jsonl-only", action="store_true")
    args = ap.parse_args(argv[1:])
    if not SRC.exists():
        print(f"[err] 未找到 {SRC}")
        return 1
    rows = collect()
    if not args.jsonl_only:
        copy_files(rows)
    write_jsonl(rows)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
