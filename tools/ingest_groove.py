#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""D3 · Groove MIDI Dataset 接入器（源 id = groove）

输入：sources/groove/<drummerN>/<sessionN>/<seq>_<style>_<bpm>_<beat|fill>_<meter>.mid
输出：data/midi/groove/b*/groove-bXXX-NNNNN.mid + midi_db/tracks/groove.jsonl
许可：CC BY 4.0（Google Magenta Groove，署名）

用法：
  python tools/ingest_groove.py [--jsonl-only]
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "sources" / "groove"
OUT_JSONL = ROOT / "midi_db" / "tracks" / "groove.jsonl"

SOURCE_ID = "groove"
LICENSE = "CC-BY-4.0"
ZONE = "main"
BUCKET = 1000
NAME = re.compile(r"^(\d+)_(.+?)_(\d+)_(beat|fill)_(\d)-(\d)$")


def collect() -> list[dict]:
    items = []
    for mid in sorted(SRC.rglob("*.mid")):
        rel = mid.relative_to(SRC)
        parts = rel.parts
        # 结构：<...>/<drummerN>/<sessionN>/<file>.mid —— 从文件名向上两层取
        drummer = parts[-3] if len(parts) >= 3 else "unknown"
        session = parts[-2] if len(parts) >= 2 else "s0"
        m = NAME.match(mid.stem)
        if m:
            seq, style, bpm, kind, num, den = m.groups()
            title = f"{style} · {bpm} BPM · {kind} {num}/{den}"
        else:
            seq = style = bpm = kind = num = den = None
            title = mid.stem.replace("_", " ")
        items.append({
            "src": mid, "rel": rel.as_posix(), "drummer": drummer, "session": session,
            "seq": seq, "style": style, "bpm": int(bpm) if bpm else None,
            "kind": kind, "meter": f"{num}/{den}" if num else None, "title": title,
        })
    items.sort(key=lambda x: (x["drummer"], x["session"], int(x["seq"]) if x["seq"] else 0))
    for i, it in enumerate(items):
        bucket = i // BUCKET
        it["n"] = i
        it["midi_rel"] = f"data/midi/{SOURCE_ID}/b{bucket:03d}/{SOURCE_ID}-b{bucket:03d}-{i % BUCKET:05d}.mid"
    return items


def copy_files(items: list[dict]) -> None:
    n = 0
    for it in items:
        t = ROOT / it["midi_rel"]
        if t.exists() and t.stat().st_size == it["src"].stat().st_size:
            n += 1
            continue
        t.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(it["src"], t)
        n += 1
    print(f"[copy] {n}/{len(items)}")


def write_jsonl(items: list[dict]) -> None:
    with OUT_JSONL.open("w", encoding="utf-8", newline="\n") as f:
        for it in items:
            r = {
                "id": f"{SOURCE_ID}-{it['n']:06d}",
                "source": SOURCE_ID,
                "src_path": f"sources/groove/{it['rel']}",
                "title": it["title"],
                "composer_slug": it["drummer"],
                "composer_name": it["drummer"].replace("drummer", "Drummer "),
                "opus": None,
                "no": int(it["seq"]) if it["seq"] else None,
                "genre": "drum",
                "form": it["style"],
                "key": None,
                "period": None,
                "region": None,
                "instrument": "drums",
                "license": LICENSE,
                "zone": ZONE,
                "midi": {"file": it["midi_rel"], "duration_sec": None, "note_count": None,
                         "tracks_count": None, "bpm": it["bpm"]},
                "fingerprint": None,
                "extra": {"session": it["session"], "kind": it["kind"], "meter": it["meter"],
                          "source": "Groove MIDI Dataset (Magenta)"},
            }
            f.write(json.dumps(r, ensure_ascii=False, separators=(",", ":")) + "\n")
    print(f"[jsonl] {len(items)} rows -> {OUT_JSONL}")


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--jsonl-only", action="store_true")
    args = ap.parse_args(argv[1:])
    items = collect()
    print(f"[collect] midi={len(items)} · drummers={len({i['drummer'] for i in items})}")
    print("  风格:", dict(Counter(i["style"] for i in items).most_common()))
    if not args.jsonl_only:
        copy_files(items)
    write_jsonl(items)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
