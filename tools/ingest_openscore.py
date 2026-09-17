#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""D3 · OpenScore Lieder Corpus 接入器（源 id = openscore）

输入：sources/openscore-lieder/scores/<Composer,_Name>/<Collection>/<N_Title>/lcXXXXXXX.mxl
处理：music21 解析 MusicXML(.mxl) → 导出 MIDI → data/midi/openscore/b*/openscore-bXXX-NNNNN.mid
输出：midi_db/tracks/openscore.jsonl（含真实曲名 title）+ 断点 tools/state/openscore-progress.json

用法（须用托管 venv 的 python，已装 music21）：
  python tools/ingest_openscore.py             # 全量（增量续跑）
  python tools/ingest_openscore.py --limit 100 # 本次最多转换 100 首（开机跑批配额）
  python tools/ingest_openscore.py --jsonl-only  # 只重建 JSONL（不转换）
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "sources" / "openscore-lieder" / "scores"
STATE = ROOT / "tools" / "state" / "openscore-progress.json"
OUT_JSONL = ROOT / "midi_db" / "tracks" / "openscore.jsonl"

SOURCE_ID = "openscore"
LICENSE = "CC0-1.0"
ZONE = "main"
BUCKET = 1000
LEAD_NUM = re.compile(r"^\d+[\s_.-]*")


def load_state() -> dict:
    if STATE.exists():
        return json.loads(STATE.read_text(encoding="utf-8"))
    return {"converted": {}, "failed": []}


def save_state(st: dict) -> None:
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(st, ensure_ascii=False, indent=1), encoding="utf-8")


def human(slug: str) -> str:
    return slug.replace("_", " ").strip()


def composer_from_dir(dirname: str) -> tuple[str, str]:
    """'Burleigh,_Harry_Thacker' -> ('burleigh', 'Harry Thacker Burleigh')"""
    if "," in dirname:
        last, rest = dirname.split(",", 1)
        name = f"{human(rest)} {human(last)}".strip()
        slug = human(last).lower().replace(" ", "")
    else:
        name = human(dirname)
        slug = name.lower().replace(" ", "")
    slug = re.sub(r"[^a-z0-9\-]", "", slug)
    return slug, name


def title_from_dir(dirname: str) -> str:
    return human(LEAD_NUM.sub("", dirname))


def collect() -> list[dict]:
    items = []
    for mxl in SRC.rglob("*.mxl"):
        rel = mxl.relative_to(SRC)
        parts = rel.parts
        if len(parts) >= 4:
            comp_dir, coll, song = parts[0], parts[1], parts[2]
        else:
            comp_dir, coll, song = parts[0], "", parts[1]
        slug, name = composer_from_dir(comp_dir)
        items.append({
            "src": mxl,
            "lc_id": mxl.stem,
            "composer_slug": slug,
            "composer_name": name,
            "collection": human(LEAD_NUM.sub("", coll)),
            "title": title_from_dir(song),
            "rel": rel.as_posix(),
        })
    items.sort(key=lambda x: x["lc_id"])
    for seq, it in enumerate(items):
        bucket = seq // BUCKET
        it["seq"] = seq
        it["midi_rel"] = f"data/midi/{SOURCE_ID}/b{bucket:03d}/{SOURCE_ID}-b{bucket:03d}-{seq % BUCKET:05d}.mid"
    return items


def convert(items: list[dict], st: dict, limit: int | None) -> None:
    from music21 import converter, environment   # 延迟导入
    environment.Environment()  # 触发 music21 环境初始化，静默首次噪声
    todo = [it for it in items if it["lc_id"] not in st["converted"]]
    if limit:
        todo = todo[:limit]
    print(f"[convert] total={len(items)} done={len(st['converted'])} todo={len(todo)}")
    for i, it in enumerate(todo, 1):
        try:
            score = converter.parse(str(it["src"]))
            # 修复：畸形 Repeat 标记会让写 MIDI 时的 expandRepeats 崩溃 → 先移除
            from music21 import repeat as _rp
            for m in list(score.recurse().getElementsByClass(_rp.RepeatMark)):
                try:
                    m.activeSite.remove(m)
                except Exception:
                    pass
            target = ROOT / it["midi_rel"]
            target.parent.mkdir(parents=True, exist_ok=True)
            score.write("midi", fp=str(target))
            st["converted"][it["lc_id"]] = {"bytes": target.stat().st_size}
        except Exception as e:
            st["failed"].append({"lc_id": it["lc_id"], "err": str(e)[:200]})
            print(f"[convert][err] {it['lc_id']}: {str(e)[:120]}")
        if i % 25 == 0:
            save_state(st)
            print(f"  ... {i}/{len(todo)}")
    save_state(st)
    print(f"[convert] done this run: +{len(todo)}")


def write_jsonl(items: list[dict], st: dict) -> int:
    rows = []
    for it in items:
        if it["lc_id"] not in st["converted"]:
            continue
        rows.append({
            "id": f"{SOURCE_ID}-{it['seq']:06d}",
            "source": SOURCE_ID,
            "src_path": f"sources/openscore-lieder/scores/{it['rel']}",
            "title": it["title"],
            "composer_slug": it["composer_slug"],
            "composer_name": it["composer_name"],
            "opus": None,
            "no": None,
            "genre": "classical",
            "form": "song",
            "key": None,
            "period": None,
            "region": None,
            "instrument": "voice_piano",
            "license": LICENSE,
            "zone": ZONE,
            "midi": {"file": it["midi_rel"], "duration_sec": None, "note_count": None,
                     "tracks_count": None, "bpm": None},
            "fingerprint": None,
            "extra": {"collection": it["collection"], "lc_id": it["lc_id"],
                      "name_source": "path"},
        })
    OUT_JSONL.parent.mkdir(parents=True, exist_ok=True)
    with OUT_JSONL.open("w", encoding="utf-8", newline="\n") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False, separators=(",", ":")) + "\n")
    print(f"[jsonl] {len(rows)} rows -> {OUT_JSONL}")
    return len(rows)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--jsonl-only", action="store_true")
    args = ap.parse_args(argv[1:])

    items = collect()
    print(f"[collect] mxl files = {len(items)} · composers = {len({i['composer_slug'] for i in items})}")
    st = load_state()
    if not args.jsonl_only:
        convert(items, st, args.limit)
    write_jsonl(items, st)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
