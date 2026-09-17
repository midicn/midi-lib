#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""D9 发布构建器：生成发布目录树 + 索引 + 校验

规则（已拍板）：
  - piano-special 公开；research 不发布（仅本地）；pending 不发布
  - broken / duplicate_of 排除
  - 文件统一 {id}.mid 命名
  - 大分类：源 → main/<category>/ 或 piano-special/

产出：
  release/midicn-lib-v1.0/
    ├── meta/catalog.json + index-*.json × 4 + MD5SUMS.txt
    ├── main/<category>/*.mid
    └── piano-special/*.mid
  （文档由 docs/ 提供，另行放入）

用法：python tools/build_release.py [--dry-run]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACKS = ROOT / "midi_db" / "tracks"
REL = ROOT / "release" / "midicn-lib-v1.0"
VERSION = "1.0"

CATEGORY = {
    "thesession": ("main", "folk-ireland"),
    "norbeck": ("main", "folk-ireland"),
    "essen": ("main", "folk-world"),
    "nottingham": ("main", "folk-british"),
    "abcmisc": ("main", "klezmer-balkan"),
    "mutopia": ("main", "classical-open"),
    "openscore": ("main", "classical-open"),
    "m21": ("main", "classical-open"),
    "musicnet": ("main", "classical-open"),
    "oga": ("main", "game"),
    "groove": ("main", "drum"),
    "aria": ("piano-special", "piano"),
    "wikifonia": ("main", "folk-world"),
}
SKIP_ZONES = {"pending"}
SKIP_SOURCES = {"maestro", "emopia", "musedata", "chinafolk"}   # research / pending 不发布


def build(args) -> int:
    t0 = time.time()
    catalog = []
    by_comp = defaultdict(list)
    by_region = defaultdict(list)
    by_period = defaultdict(list)
    by_source = defaultdict(list)
    md5_lines = []
    copied = skipped = 0
    stats = Counter()

    for f in sorted(TRACKS.glob("*.jsonl")):
        for line in f.open(encoding="utf-8"):
            r = json.loads(line)
            src = r["source"]
            if src in SKIP_SOURCES or r.get("zone") in SKIP_ZONES:
                skipped += 1
                continue
            if r.get("verify_flag") == "broken" or r.get("duplicate_of"):
                skipped += 1
                continue
            pack, cat = CATEGORY.get(src, ("main", "misc"))
            rel = f"{pack}/{cat}/{r['id']}.mid"
            srcf = ROOT / r["midi"]["file"]
            if not srcf.exists():
                skipped += 1
                continue
            catalog.append({
                "id": r["id"], "t": r.get("title"), "c": r.get("composer_slug"),
                "cn": r.get("composer_name"), "g": r.get("genre"), "p": r.get("period"),
                "r": r.get("region"), "i": r.get("instrument"), "z": r.get("zone"),
                "l": r.get("license"), "v": r.get("verify_flag"), "f": rel,
            })
            by_comp[r.get("composer_slug") or "unknown"].append(r["id"])
            if r.get("region"):
                by_region[r["region"]].append(r["id"])
            if r.get("period"):
                by_period[r["period"]].append(r["id"])
            by_source[src].append(r["id"])

            if not args.dry_run:
                dest = REL / rel
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(srcf, dest)
                md5 = hashlib.md5(dest.read_bytes()).hexdigest()
                md5_lines.append(f"{md5}  {rel}")
            copied += 1
            stats[f"{pack}/{cat}"] += 1

    REL.mkdir(parents=True, exist_ok=True)
    meta = REL / "meta"
    meta.mkdir(parents=True, exist_ok=True)

    if not args.dry_run:
        (meta / "catalog.json").write_text(
            json.dumps({"version": VERSION, "count": len(catalog), "tracks": catalog},
                       ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        for name, idx in (("by-composer", by_comp), ("by-region", by_region),
                          ("by-period", by_period), ("by-source", by_source)):
            (meta / f"index-{name}.json").write_text(
                json.dumps({k: sorted(v) for k, v in sorted(idx.items())},
                           ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        (meta / "MD5SUMS.txt").write_text("\n".join(md5_lines), encoding="utf-8")

    print(f"[build] 复制 {copied:,} · 跳过 {skipped:,} · 分类 {dict(stats.most_common())}")
    print(f"[build] 耗时 {time.time()-t0:.0f}s · 输出 {REL}")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    sys.exit(build(ap.parse_args(sys.argv[1:])))
