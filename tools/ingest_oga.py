#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""D3 · OpenGameArt MIDI 接入器（源 id = oga）

输入：sources/oga/<asset-slug>/<file>.mid（由 fetch_oga.py 抓取）
      许可信息在 tools/state/oga-progress.json 的 files 映射中（逐 asset）
输出：data/midi/oga/b*/ + midi_db/tracks/oga.jsonl

许可靠谱性：CC0 / CC-BY* / CC-BY-SA* / OGA-BY / GPL 均可商用再分发（逐曲标注）。
UNKNOWN 许可的条目 zone=pending（不发布）。

用法：python tools/ingest_oga.py
"""
from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "sources" / "oga"
STATE = ROOT / "tools" / "state" / "oga-progress.json"
OUT_JSONL = ROOT / "midi_db" / "tracks" / "oga.jsonl"

SOURCE_ID = "oga"
BUCKET = 1000
OK_LIC = re.compile(r"CC0|CC-BY|OGA-BY|GPL", re.I)


def main() -> int:
    st = json.loads(STATE.read_text(encoding="utf-8"))
    files = st.get("files", {})
    items = []
    for key, meta in sorted(files.items()):
        asset = meta.get("asset", "")
        url = meta.get("url", "")
        lic = (meta.get("license") or "UNKNOWN").strip()
        # fetch_oga.py 落盘目录名把 asset 路径的 "/" 替换为 "_"
        adir = SRC / asset.strip("/").replace("/", "_")
        fname = url.rsplit("/", 1)[-1]
        f = adir / fname
        if not f.exists():
            cands = list(adir.rglob("*.mid")) + list(adir.rglob("*.midi")) if adir.exists() else []
            f = next((c for c in cands if c.name == fname), None)
        if f is None or not f.exists():
            continue
        items.append({"src": f, "asset": asset, "license": lic,
                      "title": re.sub(r"[-_]+", " ", f.stem).strip(),
                      "author": asset.strip("/").split("/")[-1]})
    print(f"[collect] oga {len(items)} files", flush=True)

    n = 0
    with OUT_JSONL.open("w", encoding="utf-8", newline="\n") as fj:
        for seq, it in enumerate(items):
            bucket = seq // BUCKET
            rel = (f"data/midi/{SOURCE_ID}/b{bucket:03d}/"
                   f"{SOURCE_ID}-b{bucket:03d}-{seq % BUCKET:05d}.mid")
            target = ROOT / rel
            if not target.exists() or target.stat().st_size != it["src"].stat().st_size:
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(it["src"], target)
            lic_ok = bool(OK_LIC.search(it["license"]))
            row = {
                "id": f"{SOURCE_ID}-{seq:06d}", "source": SOURCE_ID,
                "src_path": f"sources/oga/{it['src'].relative_to(SRC).as_posix()}",
                "title": it["title"], "composer_slug": it["author"],
                "composer_name": it["author"], "opus": None, "no": None,
                "genre": "game", "form": None, "key": None, "period": "contemporary",
                "region": None, "instrument": "ensemble",
                "license": it["license"] if lic_ok else "UNSPECIFIED",
                "zone": "main" if lic_ok else "pending",
                "midi": {"file": rel, "duration_sec": None, "note_count": None,
                         "tracks_count": None, "bpm": None},
                "fingerprint": None,
                "extra": {"source": "OpenGameArt.org", "asset": it["asset"],
                          "raw_license": it["license"]},
            }
            fj.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")
            n += 1
    print(f"[jsonl] {n} rows -> {OUT_JSONL}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
