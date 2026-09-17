#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""D3 · Mutopia Project 接入器（源 id = mutopia）

输入：sources/mutopia/<ComposerAbbr>/<WorkNo>/<PieceName>/*.mid
      （由 tools/fetch_mutopia.py 抓取）
输出：data/midi/mutopia/b*/ + midi_db/tracks/mutopia.jsonl

许可：Mutopia 全站 PD 或 CC（均可商用/再分发）→ zone=main；
      逐曲精确许可（CC BY / CC BY-SA / PD）可在原站查询，本数据集标 MUTOPIA-MIXED。

用法：
  python tools/ingest_mutopia.py [--jsonl-only] [--workers 8]
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "sources" / "mutopia"
OUT_JSONL = ROOT / "midi_db" / "tracks" / "mutopia.jsonl"
STATE = ROOT / "tools" / "state" / "mutopia-ingest.json"

SOURCE_ID = "mutopia"
LICENSE = "MUTOPIA-MIXED"      # PD / CC BY / CC BY-SA 混合，均可商用
ZONE = "main"
BUCKET = 1000

# 常见作曲家目录缩写 -> (slug, 显示名)
COMPOSER_MAP = {
    "BachJS": ("bach", "Johann Sebastian Bach"),
    "BachCPE": ("bach-cpe", "Carl Philipp Emanuel Bach"),
    "BachWF": ("bach-wf", "Wilhelm Friedemann Bach"),
    "BachJC": ("bach-jc", "Johann Christian Bach"),
    "MozartWA": ("mozart", "Wolfgang Amadeus Mozart"),
    "BeethovenL": ("beethoven", "Ludwig van Beethoven"),
    "HandelGF": ("handel", "George Frideric Handel"),
    "ChopinF": ("chopin", "Frédéric Chopin"),
    "SchubertF": ("schubert", "Franz Schubert"),
    "SchumannR": ("schumann", "Robert Schumann"),
    "BrahmsJ": ("brahms", "Johannes Brahms"),
    "LisztF": ("liszt", "Franz Liszt"),
    "DebussyC": ("debussy", "Claude Debussy"),
    "TchaikovskyPI": ("tchaikovsky", "Pyotr Ilyich Tchaikovsky"),
    "HaydnJF": ("haydn", "Joseph Haydn"),
    "VivaldiA": ("vivaldi", "Antonio Vivaldi"),
    "PurcellH": ("purcell", "Henry Purcell"),
    "SatieE": ("satie", "Erik Satie"),
    "GriegE": ("grieg", "Edvard Grieg"),
    "MendelssohnF": ("mendelssohn", "Felix Mendelssohn"),
}


def composer_of(dirname: str) -> tuple[str, str]:
    if dirname in COMPOSER_MAP:
        return COMPOSER_MAP[dirname]
    # 通用规则：'BachJS' -> ('bach', 'Bach JS')；'(Traditional' 等原样
    m = re.match(r"^([A-Z][a-zà-ÿA-Z'\-]+)([A-Z]{1,3})?$", dirname)
    if m:
        slug = m.group(1).lower().replace("'", "")
        return slug, dirname
    return re.sub(r"[^a-z0-9\-]", "", dirname.lower()), dirname


def human(name: str) -> str:
    return name.replace("_", " ").strip()


def collect() -> list[dict]:
    items = []
    for mid in sorted(SRC.rglob("*.mid")):
        rel = mid.relative_to(SRC)
        parts = rel.parts
        composer_dir = parts[0] if len(parts) > 1 else "Unknown"
        work = parts[1] if len(parts) > 2 else None
        slug, name = composer_of(composer_dir)
        items.append({
            "src": mid, "rel": rel.as_posix(), "slug": slug, "name": name,
            "work": human(work) if work else None,
            "title": human(mid.stem),
        })
    items.sort(key=lambda x: x["rel"])
    return items


def load_state() -> dict:
    if STATE.exists():
        return json.loads(STATE.read_text(encoding="utf-8"))
    return {"rows": {}}


def save_state(st: dict) -> None:
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(st, ensure_ascii=False), encoding="utf-8")


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--jsonl-only", action="store_true")
    args = ap.parse_args(argv[1:])

    items = collect()
    print(f"[collect] mutopia MIDI = {len(items)} · 作曲家目录 = "
          f"{len({i['slug'] for i in items})}")
    if not items:
        print("[warn] 尚无文件（抓取进行中？）")
        return 1

    st = load_state()
    rows = st["rows"]
    t0 = time.time()
    n = 0
    for seq, it in enumerate(items):
        key = it["rel"]
        bucket = seq // BUCKET
        rel_midi = (f"data/midi/{SOURCE_ID}/b{bucket:03d}/"
                    f"{SOURCE_ID}-b{bucket:03d}-{seq % BUCKET:05d}.mid")
        target = ROOT / rel_midi
        if not target.exists() or target.stat().st_size != it["src"].stat().st_size:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(it["src"], target)
        rows[key] = {k: (str(v) if isinstance(v, Path) else v) for k, v in it.items()}
        rows[key].update({"seq": seq, "midi": rel_midi})
        n += 1
        if n % 500 == 0:
            save_state(st)
            print(f"  ... {n}/{len(items)}")
    save_state(st)
    print(f"[copy] {n} files in {time.time()-t0:.0f}s")

    keys = sorted(rows.keys())
    with OUT_JSONL.open("w", encoding="utf-8", newline="\n") as f:
        for seq, k in enumerate(keys):
            r = rows[k]
            row = {
                "id": f"{SOURCE_ID}-{seq:06d}", "source": SOURCE_ID,
                "src_path": f"sources/mutopia/{r['rel']}",
                "title": r["title"], "composer_slug": r["slug"], "composer_name": r["name"],
                "opus": None, "no": None,
                "genre": "classical", "form": None, "key": None, "period": None,
                "region": None, "instrument": "ensemble",
                "license": LICENSE, "zone": ZONE,
                "midi": {"file": r["midi"], "duration_sec": None, "note_count": None,
                         "tracks_count": None, "bpm": None},
                "fingerprint": None,
                "extra": {"work": r["work"], "source": "Mutopia Project",
                          "license_note": "逐曲 PD/CC 见原站 piece 页"},
            }
            f.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")
    print(f"[jsonl] {len(keys)} rows -> {OUT_JSONL}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
