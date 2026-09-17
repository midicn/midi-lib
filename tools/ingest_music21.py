#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""D3 · music21 CoreCorpus 接入器（源 id = m21）

music21 自带语料库（Bach 众赞歌/贝多芬/莫扎特/海顿/蒙特威尔第/帕莱斯特里那等，
含 kern 与 MusicXML 格式），本地已随 music21 安装 → 直接导出 MIDI。

输出：data/midi/m21/b*/ + midi_db/tracks/m21.jsonl
许可：曲目本身公有领域（PD）→ zone=main

用法（托管 venv python）：
  python tools/ingest_music21.py [--limit N] [--jsonl-only]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_JSONL = ROOT / "midi_db" / "tracks" / "m21.jsonl"
STATE = ROOT / "tools" / "state" / "m21-progress.json"

SOURCE_ID = "m21"
LICENSE = "PD"
ZONE = "main"
BUCKET = 1000


def load_state() -> dict:
    if STATE.exists():
        return json.loads(STATE.read_text(encoding="utf-8"))
    return {"done": {}, "failed": []}


def save_state(st: dict) -> None:
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(st, ensure_ascii=False), encoding="utf-8")


def composer_of(path_str: str) -> tuple[str, str]:
    """从（可能是绝对路径的）语料路径中提取作曲家。
    'C:/.../music21/corpus/bach/bwv66.6.mxl' -> ('bach', 'Bach')
    """
    parts = [p for p in path_str.replace("\\", "/").split("/") if p]
    if "corpus" in parts:
        i = parts.index("corpus")
        name = parts[i + 1] if i + 1 < len(parts) - 1 else "unknown"
    elif len(parts) > 1:
        name = parts[-2] if parts[-1].count(".") else parts[-1]
    else:
        name = "unknown"
    name = name.strip() or "unknown"
    slug = re.sub(r"[^a-z0-9\-]", "-", name.lower()).strip("-") or "unknown"
    return slug, name.replace("_", " ").title()


def collect() -> list[dict]:
    from music21 import corpus
    c = corpus.corpora.CoreCorpus()
    paths = c.getPaths()
    items = []
    for p in paths:
        rel = str(p).replace("\\", "/")
        slug, name = composer_of(rel)
        fname = rel.rsplit("/", 1)[-1]
        title = fname.rsplit(".", 1)[0].replace("_", " ")
        items.append({"path": rel, "composer": slug, "composer_name": name,
                      "title": title})
    items.sort(key=lambda x: x["path"])
    return items


def convert_one(it: dict, seq: int, tmpdir: Path) -> tuple[str, dict | None, str | None]:
    try:
        from music21 import corpus
        sc = corpus.parse(it["path"])
        out = tmpdir / f"m{seq}.mid"
        sc.write("midi", fp=str(out))
        bucket = seq // BUCKET
        rel = f"data/midi/{SOURCE_ID}/b{bucket:03d}/{SOURCE_ID}-b{bucket:03d}-{seq % BUCKET:05d}.mid"
        target = ROOT / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(out.read_bytes())
        return it["path"], {"seq": seq, "midi": rel, "path": it["path"],
                            "composer": it["composer"], "title": it["title"],
                            "subdir": it["subdir"]}, None
    except Exception as e:
        return it["path"], None, str(e)[:150]


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--jsonl-only", action="store_true")
    args = ap.parse_args(argv[1:])

    items = collect()
    st = load_state()
    done = set(st["done"].keys())
    todo = [it for it in items if it["path"] not in done]
    if args.limit:
        todo = todo[:args.limit]
    print(f"[collect] music21 corpus 文件 {len(items)} · 已完成 {len(done)} · todo {len(todo)}",
          flush=True)
    if not args.jsonl_only and todo:
        with tempfile.TemporaryDirectory() as td, ThreadPoolExecutor(max_workers=args.workers) as ex:
            tmp = Path(td)
            seq_map = {it["path"]: i for i, it in enumerate(items)}
            futs = {ex.submit(convert_one, it, seq_map[it["path"]], tmp): it for it in todo}
            n_ok = n_err = 0
            for fut in as_completed(futs):
                key, row, err = fut.result()
                if row:
                    st["done"][key] = row
                    n_ok += 1
                else:
                    st["failed"].append({"key": key, "err": err})
                    n_err += 1
            st["failed"] = st["failed"][-300:]
        save_state(st)
        print(f"[convert] +{n_ok} ok · {n_err} failed", flush=True)

    keys = sorted(st["done"].keys())
    with OUT_JSONL.open("w", encoding="utf-8", newline="\n") as f:
        for seq, k in enumerate(keys):
            r = st["done"][k]
            row = {
                "id": f"{SOURCE_ID}-{seq:06d}", "source": SOURCE_ID,
                "src_path": f"music21-corpus/{r['path']}",
                "title": r["title"],
                "composer_slug": r["composer"].lower(),
                "composer_name": r["composer"].replace("_", " ").title(),
                "opus": None, "no": None, "genre": "classical", "form": None,
                "key": None, "period": None, "region": None, "instrument": "ensemble",
                "license": LICENSE, "zone": ZONE,
                "midi": {"file": r["midi"], "duration_sec": None, "note_count": None,
                         "tracks_count": None, "bpm": None},
                "fingerprint": None,
                "extra": {"source": "music21 CoreCorpus", "subdir": r["subdir"]},
            }
            f.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")
    print(f"[jsonl] {len(keys)} rows -> {OUT_JSONL}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
