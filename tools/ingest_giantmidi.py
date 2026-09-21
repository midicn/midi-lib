#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GiantMIDI-Piano 接入器（源 id = giantmidi）

输入：sources/giantmidi/extracted/GiantMIDI-PIano/midis/*.mid
      文件名格式：Surname, Firstname, Piece, youtubeID.mid
元数据：sources/giantmidi/extracted/GiantMIDI-PIano/metadata/
        full_music_pieces_youtube_similarity_pianosoloprob_split.csv（TSV）

许可：CC BY 4.0（仓库 README 明示；disclaimer 仅为标准免责）→ zone=main（C1 可商用，须署名）
输出：data/midi/giantmidi/b*/giantmidi-bXXX-NNNNN.mid + midi_db/tracks/giantmidi.jsonl

用法：
  python tools/ingest_giantmidi.py
  python tools/ingest_giantmidi.py --jsonl-only
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import shutil
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "sources" / "giantmidi" / "extracted" / "GiantMIDI-PIano" / "midis"
META = ROOT / "sources" / "giantmidi" / "extracted" / "GiantMIDI-PIano" / "metadata" / \
    "full_music_pieces_youtube_similarity_pianosoloprob_split.csv"
OUT_JSONL = ROOT / "midi_db" / "tracks" / "giantmidi.jsonl"
DST = ROOT / "data" / "midi" / "giantmidi"

SOURCE_ID = "giantmidi"
LICENSE = "CC-BY-4.0"
ZONE = "main"
BUCKET = 1000
YT = re.compile(r"[A-Za-z0-9_-]{11}$")


def slugify(s: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return s or "unknown"


def period_from_years(birth, death):
    """以逝世年为主判据（无则用生年），按音乐史常用断代。"""
    def to_int(x):
        x = str(x).strip()
        return int(x) if x.isdigit() and 1000 <= int(x) <= 2100 else None
    y = to_int(death) or to_int(birth)
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


def load_meta():
    """youtube_id -> {nationality, birth, death}"""
    out = {}
    if not META.exists():
        print(f"[meta] 未找到 {META}，跳过元数据匹配")
        return out
    with META.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            yt = (row.get("youtube_id") or "").strip()
            if yt:
                out[yt] = {
                    "nationality": (row.get("nationality") or "").strip(),
                    "birth": (row.get("birth") or "").strip(),
                    "death": (row.get("death") or "").strip(),
                }
    print(f"[meta] 载入 {len(out):,} 条（按 youtube_id 索引）")
    return out


def parse_name(stem: str):
    """'Friedman, Ignaz, Estampes, Op.22a, 7MiyKnYouDU' -> (composer, piece, youtube_id)"""
    parts = [p.strip() for p in stem.split(",")]
    if len(parts) >= 3 and YT.match(parts[-1]):
        yt = parts[-1]
        surname = parts[0]
        firstname = parts[1] if len(parts) >= 4 else ""
        piece = ", ".join(parts[2:-1]).strip()
    else:
        yt, surname, firstname, piece = "", stem, "", stem
    composer = f"{firstname} {surname}".strip() if firstname else surname
    return composer, piece or stem, yt


def midi_stats(path: Path):
    """返回 (duration_sec, note_count)。与 music_verify.py 同口径（mido）。"""
    try:
        import mido
        mid = mido.MidiFile(path)
        dur = mid.length
        notes = sum(1 for tr in mid.tracks for msg in tr
                    if msg.type == "note_on" and msg.velocity > 0)
        return round(dur, 1), notes
    except Exception:  # noqa: BLE001
        return None, None


def collect():
    items = []
    for mid in sorted(SRC.rglob("*.mid")):
        composer, piece, yt = parse_name(mid.stem)
        items.append({"src": mid, "rel": mid.name, "composer": composer,
                      "title": piece, "yt": yt})
    items.sort(key=lambda x: (x["composer"], x["title"], x["yt"]))
    for seq, it in enumerate(items):
        bucket = seq // BUCKET
        it["seq"] = seq
        it["midi_rel"] = f"data/midi/{SOURCE_ID}/b{bucket:03d}/{SOURCE_ID}-b{bucket:03d}-{seq % BUCKET:05d}.mid"
    return items


def copy_files(items):
    n = 0
    for it in items:
        target = ROOT / it["midi_rel"]
        if target.exists() and target.stat().st_size == it["src"].stat().st_size:
            n += 1
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(it["src"], target)
        n += 1
    print(f"[copy] {n:,}/{len(items):,} files -> {DST}")
    return n


def write_jsonl(items, meta):
    final = []
    dup = dur_missing = 0
    seen_md5 = set()
    for it in items:
        md5 = hashlib.md5(it["src"].read_bytes()).hexdigest()
        if md5 in seen_md5:
            dup += 1
            continue
        seen_md5.add(md5)
        info = meta.get(it["yt"], {})
        dur, notes = midi_stats(it["src"])
        if dur is None:
            dur_missing += 1
        birth, death = info.get("birth", ""), info.get("death", "")
        nat = info.get("nationality", "")
        to_i = lambda x: int(x) if x.isdigit() else None  # noqa: E731
        final.append({
            "id": f"{SOURCE_ID}-{it['seq']:06d}",
            "source": SOURCE_ID,
            "src_path": f"sources/giantmidi/extracted/GiantMIDI-PIano/midis/{it['rel']}",
            "title": it["title"],
            "composer_slug": slugify(it["composer"]),
            "composer_name": it["composer"],
            "opus": None,
            "no": None,
            "genre": "classical",
            "form": None,
            "key": None,
            "period": period_from_years(birth, death),
            "region": None if (not nat or nat.lower() == "unknown") else nat,
            "instrument": "piano",
            "license": LICENSE,
            "zone": ZONE,
            "midi": {"file": it["midi_rel"], "duration_sec": dur, "note_count": notes,
                     "tracks_count": None, "bpm": None},
            "fingerprint": md5,
            "extra": {"source": "GiantMIDI-Piano v1.2 (ByteDance, CC BY 4.0)",
                      "youtube_id": it["yt"],
                      "nationality": None if (not nat or nat.lower() == "unknown") else nat,
                      "birth": to_i(birth), "death": to_i(death)},
        })
    OUT_JSONL.parent.mkdir(parents=True, exist_ok=True)
    with OUT_JSONL.open("w", encoding="utf-8", newline="\n") as f:
        for r in final:
            f.write(json.dumps(r, ensure_ascii=False, separators=(",", ":")) + "\n")
    print(f"[jsonl] {len(final):,} rows -> {OUT_JSONL}")
    print(f"  内容重复剔除: {dup} · 时长缺失: {dur_missing}")
    print("  period 分布:", dict(Counter(x["period"] for x in final)))
    print("  作曲家数:", len({x["composer_slug"] for x in final}))
    return len(final)


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--jsonl-only", action="store_true")
    args = ap.parse_args(argv[1:])
    if not SRC.exists():
        print(f"[err] 未找到 {SRC}")
        return 1
    items = collect()
    meta = load_meta()
    print(f"[collect] midi = {len(items):,}")
    if not args.jsonl_only:
        copy_files(items)
    write_jsonl(items, meta)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
