#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""D3 · MuseData/CCARH 接入器（源 id = musedata）

输入：sources/musedata-*/ 下的 .mid（直接用）与 .krn（music21 转换）
输出：data/midi/musedata/b*/ + midi_db/tracks/musedata.jsonl

⚠️ 许可：CCARH MuseData 许可禁止任何形式分发（含非商业）→ **zone=research**，
   本地研究收录，永不进 dist 发布包，门户仅链接。.krn 来自 CCARH 仓库同样受限。

用法（须用带 music21 的 venv python）：
  python tools/ingest_musedata.py [--jsonl-only]
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_JSONL = ROOT / "midi_db" / "tracks" / "musedata.jsonl"
STATE = ROOT / "tools" / "state" / "musedata-progress.json"

SOURCE_ID = "musedata"
LICENSE = "CCARH-RESTRICTED"
ZONE = "research"
BUCKET = 1000

REPO_COMPOSER = {
    "beethoven": ("beethoven", "Ludwig van Beethoven"),
    "corelli": ("corelli", "Arcangelo Corelli"),
    "vivaldi": ("vivaldi", "Antonio Vivaldi"),
    "haydn": ("haydn", "Joseph Haydn"),
    "mozart": ("mozart", "Wolfgang Amadeus Mozart"),
    "bach": ("bach", "Johann Sebastian Bach"),
}


def load_state() -> dict:
    if STATE.exists():
        return json.loads(STATE.read_text(encoding="utf-8"))
    return {"done": {}, "failed": []}


def save_state(st: dict) -> None:
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(st, ensure_ascii=False), encoding="utf-8")


def composer_of(path: Path) -> tuple[str, str]:
    low = path.as_posix().lower()
    for k, v in REPO_COMPOSER.items():
        if k in low:
            return v
    return "unknown", "Unknown"


def collect() -> list[dict]:
    items = []
    for repo in sorted((ROOT / "sources").glob("musedata-*")):
        for f in sorted(repo.rglob("*")):
            if f.suffix.lower() not in (".mid", ".krn"):
                continue
            slug, name = composer_of(f)
            items.append({"src": f, "rel": f.relative_to(ROOT).as_posix(),
                          "kind": f.suffix.lower().lstrip("."), "slug": slug, "name": name,
                          "title": f.stem.replace("-", " ").replace("_", " ")})
    items.sort(key=lambda x: (x["rel"]))
    return items


def convert_one(it: dict, seq: int, tmpdir: Path) -> tuple[str, dict | None, str | None]:
    try:
        bucket = seq // BUCKET
        rel = f"data/midi/{SOURCE_ID}/b{bucket:03d}/{SOURCE_ID}-b{bucket:03d}-{seq % BUCKET:05d}.mid"
        target = ROOT / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        if it["kind"] == "mid":
            data = it["src"].read_bytes()
            target.write_bytes(data)
        else:  # kern → music21
            from music21 import converter, repeat
            sc = converter.parse(str(it["src"]))
            # 修复：畸形 Repeat 标记会让写 MIDI 时的 expandRepeats 崩溃 → 先移除
            for m in list(sc.recurse().getElementsByClass(repeat.RepeatMark)):
                try:
                    m.activeSite.remove(m)
                except Exception:
                    pass
            tmp_mid = tmpdir / f"k{seq}.mid"
            sc.write("midi", fp=str(tmp_mid))
            shutil.copy2(tmp_mid, target)
        return it["rel"], {"seq": seq, "midi": rel, "src_path": it["rel"],
                           "title": it["title"], "slug": it["slug"], "name": it["name"],
                           "kind": it["kind"]}, None
    except Exception as e:
        return it["rel"], None, str(e)[:150]


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--jsonl-only", action="store_true")
    ap.add_argument("--workers", type=int, default=6)
    args = ap.parse_args(argv[1:])

    items = collect()
    seq_map = {it["rel"]: i for i, it in enumerate(items)}
    st = load_state()
    done = set(st["done"].keys())
    todo = [it for it in items if it["rel"] not in done]
    print(f"[collect] musedata 文件 {len(items)} · 已完成 {len(done)} · todo {len(todo)}")
    if not args.jsonl_only and todo:
        t0 = time.time()
        with tempfile.TemporaryDirectory() as td, ThreadPoolExecutor(max_workers=args.workers) as ex:
            tmp = Path(td)
            futs = {ex.submit(convert_one, it, seq_map[it["rel"]], tmp): it for it in todo}
            n_ok = n_err = 0
            for fut in as_completed(futs):
                key, row, err = fut.result()
                if row:
                    st["done"][key] = row
                    n_ok += 1
                else:
                    st["failed"].append({"key": key, "err": err})
                    n_err += 1
            st["failed"] = st["failed"][-400:]
        save_state(st)
        print(f"[convert] +{n_ok} ok · {n_err} failed in {time.time()-t0:.0f}s")

    keys = sorted(st["done"].keys())
    with OUT_JSONL.open("w", encoding="utf-8", newline="\n") as f:
        for seq, k in enumerate(keys):
            r = st["done"][k]
            row = {
                "id": f"{SOURCE_ID}-{seq:06d}", "source": SOURCE_ID, "src_path": r["src_path"],
                "title": r["title"], "composer_slug": r["slug"], "composer_name": r["name"],
                "opus": None, "no": None, "genre": "classical",
                "form": None, "key": None, "period": None, "region": None,
                "instrument": "ensemble",
                "license": LICENSE, "zone": ZONE,
                "midi": {"file": r["midi"], "duration_sec": None, "note_count": None,
                         "tracks_count": None, "bpm": None},
                "fingerprint": None,
                "extra": {"source": "MuseData/CCARH", "kind": r["kind"],
                          "license_note": "CCARH 许可禁止分发；本地研究专用"},
            }
            f.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")
    print(f"[jsonl] {len(keys)} rows -> {OUT_JSONL}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
