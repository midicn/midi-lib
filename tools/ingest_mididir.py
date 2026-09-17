#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""通用「已有 MIDI 目录」接入器（源 id 由 --source 指定）

支持：
  musicnet   <Composer>/<id>_<title>.mid          CC BY 4.0    main
  emopia     EMOPIA_2.2/midis/<Qn>_<ytid>_<n>.mid CC BY-NC-SA research（过滤 __MACOSX/._ 噪声）
  maestro    <year>/<name>.midi + CSV 元数据      CC BY-NC-SA research

用法：
  python tools/ingest_mididir.py --source musicnet
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUCKET = 1000

SOURCES = {
    "musicnet": {
        "dir": "sources/musicnet", "ext": ".mid",
        "license": "CC-BY-4.0", "zone": "main", "genre": "classical",
        "instrument": "ensemble", "composer_from_dir": True, "composer_index": 1,
        "source_name": "MusicNet",
    },
    "emopia": {
        "dir": "sources/emopia", "ext": ".mid",
        "license": "CC-BY-NC-SA-4.0", "zone": "research", "genre": "pop",
        "instrument": "piano", "skip_prefix": "._", "skip_dirs": ["__MACOSX"],
        "quadrant": True, "source_name": "EMOPIA (Pop Piano)",
    },
    "maestro": {
        "dir": "sources/maestro", "ext": ".midi",
        "license": "CC-BY-NC-SA-4.0", "zone": "research", "genre": "classical",
        "instrument": "piano", "csv_meta": True, "source_name": "MAESTRO v3.0.0",
    },
}

QUAD = {"Q1": "Q1 高唤醒-高愉悦", "Q2": "Q2 高唤醒-低愉悦",
        "Q3": "Q3 低唤醒-低愉悦", "Q4": "Q4 低唤醒-高愉悦"}


def load_csv_meta(p: Path) -> dict:
    out = {}
    for c in p.rglob("*.csv"):
        try:
            with c.open(encoding="utf-8") as f:
                for r in csv.DictReader(f):
                    key = (r.get("midi_filename") or "").replace("\\", "/")
                    if key:
                        out[key] = r
        except Exception:
            continue
    return out


def collect(src_id: str, cfg: dict) -> list[dict]:
    base = ROOT / cfg["dir"]
    meta = load_csv_meta(base) if cfg.get("csv_meta") else {}
    items = []
    for f in sorted(base.rglob(f"*{cfg['ext']}")):
        rel = f.relative_to(base)
        if cfg.get("skip_prefix") and f.name.startswith(cfg["skip_prefix"]):
            continue
        if cfg.get("skip_dirs") and any(s in rel.parts for s in cfg["skip_dirs"]):
            continue
        composer, name, title, extra = None, "Unknown", f.stem, {}
        if cfg.get("composer_from_dir"):
            # musicnet 结构：musicnet_midis/<Composer>/<file>.mid（跳过包装目录）
            idx = cfg.get("composer_index", 0)
            if len(rel.parts) > idx:
                composer = rel.parts[idx]
            else:
                composer = "Unknown"
            m = re.match(r"^\d+_(.+)$", f.stem)
            title = m.group(1).replace("_", " ") if m else f.stem
        elif cfg.get("quadrant"):
            m = re.match(r"^(Q\d)_([A-Za-z0-9\-]+)_(\d+)$", f.stem)
            if m:
                extra["quadrant"] = QUAD.get(m.group(1), m.group(1))
                extra["ytid"] = m.group(2)
                title = f"{m.group(1)} #{m.group(3)}"
        elif meta:
            key = rel.as_posix()
            r = (meta.get(key) or meta.get(f.name)
                 or meta.get("/".join(rel.parts[1:]))      # 去掉顶层目录
                 or meta.get(rel.parts[-1]))
            if r:
                composer = r.get("canonical_composer")
                title = r.get("canonical_title") or f.stem
                extra["year"] = r.get("year")
                extra["duration"] = r.get("duration")
                extra["split"] = r.get("split")
            extra["performer"] = "MAESTRO pianists (Yamaha Disklavier)"
        items.append({"src": f, "rel": rel.as_posix(), "composer": composer,
                      "title": title, "extra": extra})
    items.sort(key=lambda x: x["rel"])
    return items


def slugify(s: str) -> str:
    return re.sub(r"[^a-z0-9\-]", "", s.lower().replace(" ", "-")) or "unknown"


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True, choices=list(SOURCES))
    args = ap.parse_args(argv[1:])
    src_id, cfg = args.source, SOURCES[args.source]

    items = collect(src_id, cfg)
    print(f"[collect] {src_id}: {len(items)} MIDI", flush=True)
    if not items:
        return 1

    out_jsonl = ROOT / "midi_db" / "tracks" / f"{src_id}.jsonl"
    n = 0
    with out_jsonl.open("w", encoding="utf-8", newline="\n") as fj:
        for seq, it in enumerate(items):
            bucket = seq // BUCKET
            rel_midi = (f"data/midi/{src_id}/b{bucket:03d}/"
                        f"{src_id}-b{bucket:03d}-{seq % BUCKET:05d}.mid")
            target = ROOT / rel_midi
            if not target.exists() or target.stat().st_size != it["src"].stat().st_size:
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(it["src"], target)
            composer = it["composer"] or "Unknown"
            row = {
                "id": f"{src_id}-{seq:06d}", "source": src_id,
                "src_path": f"{cfg['dir']}/{it['rel']}",
                "title": it["title"],
                "composer_slug": slugify(composer),
                "composer_name": composer,
                "opus": None, "no": None,
                "genre": cfg["genre"], "form": None, "key": None, "period": None,
                "region": None, "instrument": cfg["instrument"],
                "license": cfg["license"], "zone": cfg["zone"],
                "midi": {"file": rel_midi, "duration_sec": None, "note_count": None,
                         "tracks_count": None, "bpm": None},
                "fingerprint": None,
                "extra": {"source": cfg["source_name"], **it["extra"]},
            }
            fj.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")
            n += 1
            if n % 500 == 0:
                print(f"  ... {n}/{len(items)}", flush=True)
    print(f"[jsonl] {n} rows -> {out_jsonl}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
