#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Lakh MIDI 接入器（过滤 + 入库 C3=study）

合规依据：Lakh MIDI Dataset 声明 CC-BY 4.0（允许再分发）；
但作者明言「未转录任何 MIDI、均从公开来源抓取」→ 内容层需严格过滤：
  1. 剔除所有**含版权声明**的曲目（读 MIDI 的 Copyright meta-event）
  2. 剔除**路径含流行/摇滚/游戏/影视关键词**的曲目（内容性质风险）
  3. 仅保留**明确提出为古典/传统/宗教/学术**的曲目 → 定级 C3（仅供研究/学习）

用法（须带 mido + 托管 venv）：
  python tools/ingest_lakh.py [--limit N] [--dry-run]
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import tarfile
import tempfile
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARBALL = ROOT / "sources" / "lakh" / "lmd_full.tar.gz"
OUT_JSONL = ROOT / "midi_db" / "tracks" / "lakh.jsonl"
STATE = ROOT / "tools" / "state" / "lakh-progress.json"

SOURCE_ID = "lakh"
LICENSE = "CC-BY-4.0"
ZONE = "study"          # C3 · 仅供研究/学习
BUCKET = 1000

# 保留：明确的古典/传统/宗教/学术类路径
KEEP_PAT = re.compile(
    r"classical|klassik|baroque|renaissance|medieval|"
    r"bach|mozart|beethoven|chopin|liszt|schubert|brahms|handel|vivaldi|haydn|"
    r"hymn|church|choral|organ|sacred|gospel|christmas|carol|"
    r"traditional|trad[_ ]|folk|celtic|irish|scottish|"
    r"etude|sonata|symphony|concerto|nocturne|prelude|fugue|waltz|mazurka",
    re.I)

# 剔除：流行/摇滚/影视/游戏/现代商业音乐
DROP_PAT = re.compile(
    r"\bpop\b|top.?40|hits|charts?|"
    r"rock|metal|punk|grunge|hard.?rock|"
    r"tv.?theme|movie|soundtrack|film|"
    r"nintendo|sega|playstation|final fantasy|zelda|mario|game|"
    r"samba|pagode|forro|mpb|axé|"
    r"rap|hip.?hop|techno|trance|house|dance|"
    r"disco|reggae|kpop|jpop|anime",
    re.I)

COPYRIGHT_PAT = re.compile(r"©|\(c\)|copyright|all rights reserved|www\.|http", re.I)


def has_copyright_event(path: Path) -> bool:
    """读 MIDI 的 Copyright meta-event（速度优先，只扫前若干事件）。"""
    try:
        import mido
        mid = mido.MidiFile(str(path))
        for track in mid.tracks:
            for msg in track[:60]:
                if msg.type == "copyright" and msg.text and COPYRIGHT_PAT.search(msg.text):
                    return True
        return False
    except Exception:
        return True          # 解析失败的保守剔除


# tar 内文件以 MD5 命名 → 需用原始路径映射做内容判断
PATHS_MAP: dict = {}


def load_paths_map() -> dict:
    global PATHS_MAP
    if PATHS_MAP:
        return PATHS_MAP
    p = ROOT / "sources" / "lakh" / "md5_to_paths.json"
    if p.exists():
        import json as _json
        PATHS_MAP = _json.loads(p.read_text(encoding="utf-8"))
    print(f"[lakh] md5→路径映射: {len(PATHS_MAP):,} 条", flush=True)
    return PATHS_MAP


def orig_paths_of(md5: str) -> list[str]:
    return PATHS_MAP.get(md5, [])


def extract_and_filter(tar_path: Path, tmpdir: Path, limit: int | None) -> list[Path]:
    """解压 + 初筛（用 md5 反查原始路径），返回保留的文件路径列表。"""
    load_paths_map()
    kept = []
    stats = Counter()
    with tarfile.open(tar_path, "r:gz") as tf:
        for i, m in enumerate(tf):
            if not m.isfile() or not m.name.lower().endswith(".mid"):
                continue
            md5 = Path(m.name).stem.lower()
            origs = orig_paths_of(md5)
            if not origs:
                stats["drop_无路径记录"] += 1
                continue
            joined = " | ".join(origs)
            if DROP_PAT.search(joined):
                stats["drop_流行/影视/游戏"] += 1
                continue
            if not KEEP_PAT.search(joined):
                stats["drop_无古典传统标记"] += 1
                continue
            stats["路径级保留"] += 1
            f = tf.extractfile(m)
            if f is None:
                continue
            dest = tmpdir / Path(m.name).name
            dest.write_bytes(f.read())
            kept.append(dest)
            if limit and len(kept) >= limit:
                break
            if len(kept) % 1000 == 0:
                print(f"  ... 已提取 {len(kept):,} 首", flush=True)
    print(f"[extract] {dict(stats)}", flush=True)
    return kept


def convert_one(idx: int, src: Path) -> tuple[str, dict | None, str | None]:
    """内容级过滤（版权声明）→ 入库。"""
    try:
        if has_copyright_event(src):
            return src.name, None, "含版权声明"
        bucket = idx // BUCKET
        rel = f"data/midi/{SOURCE_ID}/b{bucket:03d}/{SOURCE_ID}-b{bucket:03d}-{idx % BUCKET:05d}.mid"
        target = ROOT / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, target)
        return src.name, {"seq": idx, "midi": rel, "orig": src.name,
                          "orig_path": (orig_paths_of(Path(src.name).stem.lower()) or [""])[0]}, None
    except Exception as e:
        return src.name, None, str(e)[:100]


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--workers", type=int, default=8)
    args = ap.parse_args(argv[1:])

    if not TARBALL.exists():
        print(f"[error] 未找到 {TARBALL}", flush=True)
        return 1
    print(f"[lakh] tarball {TARBALL.stat().st_size/1024**3:.2f}GB", flush=True)

    st = json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {"done": {}, "failed": []}
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        kept = extract_and_filter(TARBALL, tmp, args.limit)
        if args.dry_run:
            print(f"[dry-run] 路径级保留 {len(kept):,} 首（未做版权过滤）", flush=True)
            return 0
        print(f"[lakh] 路径级保留 {len(kept):,} 首 → 内容级过滤…", flush=True)
        n_ok = n_bad = 0
        base = len(st["done"])
        with ThreadPoolExecutor(max_workers=args.workers) as ex:
            futs = {ex.submit(convert_one, base + i, p): p for i, p in enumerate(kept)}
            for fut in as_completed(futs):
                name, row, err = fut.result()
                if row:
                    st["done"][name] = row
                    n_ok += 1
                else:
                    st["failed"].append({"f": name, "err": err})
                    n_bad += 1
                if (n_ok + n_bad) % 1000 == 0:
                    STATE.write_text(json.dumps(st, ensure_ascii=False), encoding="utf-8")
                    print(f"  ... {n_ok + n_bad:,}/{len(kept):,}（保留 {n_ok:,}）", flush=True)
    st["failed"] = st["failed"][-300:]
    STATE.write_text(json.dumps(st, ensure_ascii=False), encoding="utf-8")
    print(f"[lakh] 内容过滤：保留 {n_ok:,} · 剔除 {n_bad:,}", flush=True)

    keys = sorted(st["done"].keys())
    with OUT_JSONL.open("w", encoding="utf-8", newline="\n") as fj:
        for seq, k in enumerate(keys):
            r = st["done"][k]
            fj.write(json.dumps({
                "id": f"{SOURCE_ID}-{seq:06d}", "source": SOURCE_ID,
                "src_path": f"sources/lakh/{r.get('orig_path') or r['orig']}",
                "title": Path(r.get("orig_path") or r["orig"]).stem.replace("_", " ")[:80],
                "composer_slug": None, "composer_name": None,
                "opus": None, "no": None, "genre": None, "form": None,
                "key": None, "period": None, "region": None, "instrument": None,
                "license": LICENSE, "zone": ZONE,
                "midi": {"file": r["midi"], "duration_sec": None, "note_count": None,
                         "tracks_count": None, "bpm": None},
                "fingerprint": None,
                "extra": {"source": "Lakh MIDI Dataset",
                          "note": "内容层已过滤版权声明；原数据集许可 CC-BY 4.0"},
            }, ensure_ascii=False, separators=(",", ":")) + "\n")
    print(f"[jsonl] {len(keys):,} rows -> {OUT_JSONL}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
