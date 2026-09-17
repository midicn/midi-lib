#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""D3 · Wikifonia 接入器（源 id = wikifonia）—— 带 PD 过滤

输入：sources/wikifonia/Wikifonia.zip（6,434 个 .mxl lead sheets）
处理：**只保留传统/民歌类**（署名含 traditional / folk / hungarian song / anon 等），
      其余为 20 世纪流行曲/爵士标准曲（版权内）→ 不收录。
转换：music21 解析 .mxl → 导出 MIDI → data/midi/wikifonia/b*/

许可：传统/民歌部分为公有领域（PD）→ zone=main；其余不收录。

用法（托管 venv python）：
  python tools/ingest_wikifonia.py [--dry-run]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import tempfile
import zipfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ZIP = ROOT / "sources" / "wikifonia" / "Wikifonia.zip"
OUT_JSONL = ROOT / "midi_db" / "tracks" / "wikifonia.jsonl"
STATE = ROOT / "tools" / "state" / "wikifonia-progress.json"

SOURCE_ID = "wikifonia"
LICENSE = "PD"
ZONE = "main"
BUCKET = 1000

# PD 白名单（署名关键词）
PD_PAT = re.compile(r"traditional|folk|hungarian song|anon|trad\.|volkslied|"
                    r"public domain|unknown author|folk song", re.I)
# 明确排除（版权内的 20 世纪流行署名常见词，兜底）
RISK_PAT = re.compile(r"lennon|mccartney|gershwin|porter|berlin|bacharach|"
                      r"rodgers|hammerstein|ellington|monk|denver|sty|"
                      r"cahn|loesser|williams|marley|dy­lan", re.I)


def load_state() -> dict:
    if STATE.exists():
        return json.loads(STATE.read_text(encoding="utf-8"))
    return {"done": {}, "failed": [], "skipped": 0}


def save_state(st: dict) -> None:
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(st, ensure_ascii=False), encoding="utf-8")


def collect() -> list[dict]:
    z = zipfile.ZipFile(ZIP)
    items = []
    skipped = 0
    for n in z.namelist():
        if not n.lower().endswith(".mxl"):
            continue
        base = Path(n).stem
        if " - " in base:
            composer, title = base.split(" - ", 1)
        else:
            composer, title = "", base
        composer, title = composer.strip(), title.strip()
        if not PD_PAT.search(composer) or RISK_PAT.search(composer):
            skipped += 1
            continue
        items.append({"zip_name": n, "composer": composer, "title": title})
    items.sort(key=lambda x: x["zip_name"])
    print(f"[collect] 总 {len(z.namelist())} 条目 · PD 白名单命中 {len(items)} · 过滤掉 {skipped}",
          flush=True)
    return items


def convert_one(it: dict, seq: int, zip_path: Path, tmpdir: Path) -> tuple[str, dict | None, str | None]:
    try:
        from music21 import converter, repeat
        import zipfile as zf
        with zf.ZipFile(zip_path) as z:
            data = z.read(it["zip_name"])
        src = tmpdir / f"w{seq}.mxl"
        src.write_bytes(data)
        sc = converter.parse(str(src))
        for m in list(sc.recurse().getElementsByClass(repeat.RepeatMark)):
            try:
                m.activeSite.remove(m)
            except Exception:
                pass
        bucket = seq // BUCKET
        rel = (f"data/midi/{SOURCE_ID}/b{bucket:03d}/"
               f"{SOURCE_ID}-b{bucket:03d}-{seq % BUCKET:05d}.mid")
        target = ROOT / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        out = tmpdir / f"w{seq}.mid"
        sc.write("midi", fp=str(out))
        target.write_bytes(out.read_bytes())
        return it["zip_name"], {"seq": seq, "midi": rel, **it}, None
    except Exception as e:
        return it["zip_name"], None, str(e)[:150]


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--workers", type=int, default=6)
    args = ap.parse_args(argv[1:])

    items = collect()
    if args.dry_run:
        from collections import Counter
        print("署名 Top15:", Counter(i["composer"] for i in items).most_common(15))
        return 0

    st = load_state()
    done = set(st["done"].keys())
    todo = [it for it in items if it["zip_name"] not in done]
    print(f"[convert] todo {len(todo)} / {len(items)}", flush=True)
    if todo:
        seq_map = {it["zip_name"]: i for i, it in enumerate(items)}
        with tempfile.TemporaryDirectory() as td, ThreadPoolExecutor(max_workers=args.workers) as ex:
            tmp = Path(td)
            futs = {ex.submit(convert_one, it, seq_map[it["zip_name"]], ZIP, tmp): it for it in todo}
            n_ok = n_err = 0
            for fut in as_completed(futs):
                key, row, err = fut.result()
                if row:
                    st["done"][key] = row
                    n_ok += 1
                else:
                    st["failed"].append({"key": key, "err": err})
                    n_err += 1
            st["failed"] = st["failed"][-200:]
        save_state(st)
        print(f"[convert] +{n_ok} ok · {n_err} failed", flush=True)

    keys = sorted(st["done"].keys())
    with OUT_JSONL.open("w", encoding="utf-8", newline="\n") as fj:
        for seq, k in enumerate(keys):
            r = st["done"][k]
            fj.write(json.dumps({
                "id": f"{SOURCE_ID}-{seq:06d}", "source": SOURCE_ID,
                "src_path": f"sources/wikifonia/Wikifonia.zip!/{r['zip_name']}",
                "title": r["title"], "composer_slug": None,
                "composer_name": r["composer"], "opus": None, "no": None,
                "genre": "folk", "form": None, "key": None, "period": None,
                "region": None, "instrument": "melody",
                "license": LICENSE, "zone": ZONE,
                "midi": {"file": r["midi"], "duration_sec": None, "note_count": None,
                         "tracks_count": None, "bpm": None},
                "fingerprint": None,
                "extra": {"source": "Wikifonia (PD subset only)",
                          "origin": "Wikifonia project archive"},
            }, ensure_ascii=False, separators=(",", ":")) + "\n")
    print(f"[jsonl] {len(keys)} rows -> {OUT_JSONL}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
