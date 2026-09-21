#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""D3 · 中国民间歌曲集成接入器（源 id = chinafolk）

输入：sources/china-folk/lyrics-included/<province>/<n>_<中文曲名>.mid
输出：data/midi/chinafolk/b*/chinafolk-bXXX-NNNNN.mid + midi_db/tracks/chinafolk.jsonl
      （region=省份中文名；title=中文曲名；composer=traditional）

⚠️ 许可状态：源仓库无 LICENSE 声明 → zone=pending（本地收录，暂不进发布包；门户仅链接）

用法：
  python tools/ingest_chinafolk.py
  python tools/ingest_chinafolk.py --jsonl-only
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "sources" / "china-folk" / "lyrics-included"
OUT_JSONL = ROOT / "midi_db" / "tracks" / "chinafolk.jsonl"
DST = ROOT / "data" / "midi" / "chinafolk"

SOURCE_ID = "chinafolk"
LICENSE = "UNSPECIFIED"          # 源未声明，待作者确认
ZONE = "pending"                 # 待定分区：本地收录，不进发布包
BUCKET = 1000
LEAD = re.compile(r"^(\d+)[_\-\.\s]*")

PROVINCE = {
    "beijing": "北京", "tianjin": "天津", "shanghai": "上海",
    "guangdong": "广东", "hainan": "海南", "hebei1": "河北", "hebei2": "河北",
    "henan": "河南", "jiangsu1": "江苏", "jiangsu2": "江苏", "jilin": "吉林",
    "shaanxi1": "陕西", "shaanxi2": "陕西", "sichuan1": "四川",
}


def prov_of(dirname: str) -> str:
    """'shaanxi2 (some lyric characters are missing)' -> '陕西'"""
    base = re.split(r"[ (]", dirname, maxsplit=1)[0].strip()
    return PROVINCE.get(base, base)


def collect() -> list[dict]:
    items = []
    for mid in sorted(SRC.rglob("*.mid")):
        rel = mid.relative_to(SRC)
        prov_dir = rel.parts[0]
        stem = mid.stem
        m = LEAD.match(stem)
        num = m.group(1) if m else None
        title = LEAD.sub("", stem).strip() or stem
        items.append({
            "src": mid,
            "rel": rel.as_posix(),
            "prov_dir": prov_dir,
            "region": prov_of(prov_dir),
            "num": num,
            "title": title,
            "note": "lyrics partially missing (upstream warning)" if "lyric" in prov_dir else None,
        })
    items.sort(key=lambda x: (x["prov_dir"], int(x["num"]) if x["num"] else 0, x["title"]))
    for seq, it in enumerate(items):
        bucket = seq // BUCKET
        it["seq"] = seq
        it["midi_rel"] = f"data/midi/{SOURCE_ID}/b{bucket:03d}/{SOURCE_ID}-b{bucket:03d}-{seq % BUCKET:05d}.mid"
    return items


def copy_files(items: list[dict]) -> int:
    n = 0
    for it in items:
        target = ROOT / it["midi_rel"]
        if target.exists() and target.stat().st_size == it["src"].stat().st_size:
            n += 1
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(it["src"], target)
        n += 1
    print(f"[copy] {n}/{len(items)} files -> {DST}")
    return n


def write_jsonl(items: list[dict]) -> int:
    rows = []
    for it in items:
        rows.append({
            "id": f"{SOURCE_ID}-{it['seq']:06d}",
            "source": SOURCE_ID,
            "src_path": f"sources/china-folk/lyrics-included/{it['rel']}",
            "title": it["title"],
            "composer_slug": "traditional",
            "composer_name": "民歌 Traditional",
            "opus": None,
            "no": int(it["num"]) if it["num"] else None,
            "genre": "folk",
            "form": None,
            "key": None,
            "period": None,
            "region": it["region"],
            "instrument": "voice",
            "license": LICENSE,
            "zone": ZONE,
            "midi": {"file": it["midi_rel"], "duration_sec": None, "note_count": None,
                     "tracks_count": None, "bpm": None},
            "fingerprint": None,
            "extra": {"province_dir": it["prov_dir"], "seq_in_volume": it["num"],
                      "source": "Anthology of Chinese Folk Songs (OMR)",
                      "note": it["note"]},
        })
    OUT_JSONL.parent.mkdir(parents=True, exist_ok=True)
    with OUT_JSONL.open("w", encoding="utf-8", newline="\n") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False, separators=(",", ":")) + "\n")
    print(f"[jsonl] {len(rows)} rows -> {OUT_JSONL}")
    return len(rows)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--jsonl-only", action="store_true")
    args = ap.parse_args(argv[1:])
    items = collect()
    from collections import Counter
    print(f"[collect] midi = {len(items)} · provinces = {len({i['region'] for i in items})}")
    print("  分布:", dict(Counter(i["region"] for i in items).most_common()))
    if not args.jsonl_only:
        copy_files(items)
    write_jsonl(items)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
