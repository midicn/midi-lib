#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""歌词库分片生成器（F2 · 歌词仅站内检索）。

把 `midi_db/lyrics/chinafolk.jsonl`（10,035 首中国民歌歌词）切成
`release/site-repo/data/lyrics/` 下的分片，**仅供站内检索**。

⚠️ 版权红线（2026-09-23 拍板，见 docs/LICENSE.md §2.3）
  · 歌词库**不进任何发布包** —— `build_release.py` 不复制、`pack_release.py` 不打包
  · 仅站内展示，**不提供下载**；页面必须显著声明「仅限研究/学习」
  · 歌词是**独立权利层**：不随曲目档位授予商用许可，本库不主张歌词著作权
  · 上游：中国民间歌曲集成（OMR 数据集，TRADITIONAL-STUDY）→ 须署名

输出
  data/lyrics/index.json   [[id, title, region, chars, shard, incomplete], …]（紧凑数组）
  data/lyrics/sNN.json     {id: lyrics}（每片 500 首）

用法
  python tools/gen_lyrics_shards.py            # 生成
  python tools/gen_lyrics_shards.py --verify   # 生成并校验条数/分片自洽
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LYRICS = ROOT / "midi_db" / "lyrics" / "chinafolk.jsonl"
TRACKS = ROOT / "midi_db" / "tracks" / "chinafolk.jsonl"
OUT = ROOT.parent / "site" / "data" / "lyrics"
SHARD_SIZE = 500


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--verify", action="store_true")
    args = ap.parse_args(argv[1:])

    if not LYRICS.exists():
        print(f"[err] 未找到 {LYRICS}", file=sys.stderr)
        return 1

    # ── 曲目元数据（标题 / 地区）按 id 索引 ───────────────────────────────
    meta: dict[str, tuple[str, str]] = {}
    if TRACKS.exists():
        for line in TRACKS.open(encoding="utf-8"):
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            meta[r["id"]] = (r.get("title") or "", r.get("region") or "")

    rows = []
    for line in LYRICS.open(encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        r = json.loads(line)
        t, reg = meta.get(r["id"], ("", ""))
        rows.append((r["id"], t, reg, int(r.get("chars") or len(r.get("lyrics") or "")),
                     bool(r.get("incomplete")), r.get("lyrics") or ""))
    rows.sort(key=lambda x: x[0])
    print(f"[lyrics] 读入 {len(rows):,} 首（曲目元数据命中 {sum(1 for r in rows if r[1]):,}）")

    OUT.mkdir(parents=True, exist_ok=True)
    for old in OUT.glob("*.json"):
        old.unlink()

    # ── 分片 ──────────────────────────────────────────────────────────────
    n_shard = (len(rows) + SHARD_SIZE - 1) // SHARD_SIZE
    index = []
    for si in range(n_shard):
        chunk = rows[si * SHARD_SIZE:(si + 1) * SHARD_SIZE]
        bundle = {r[0]: r[5] for r in chunk}
        (OUT / f"s{si:02d}.json").write_text(
            json.dumps(bundle, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        for rid, t, reg, ch, inc, _l in chunk:
            index.append([rid, t, reg, ch, si, 1 if inc else 0])

    (OUT / "index.json").write_text(
        json.dumps(index, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")

    total_bytes = sum(f.stat().st_size for f in OUT.glob("*.json"))
    print(f"[out] {OUT.relative_to(ROOT)}")
    print(f"       index.json {len(index):,} 条 · 分片 {n_shard} 个 · 合计 {total_bytes/1e6:.1f} MB")

    # ── 校验 ──────────────────────────────────────────────────────────────
    if args.verify:
        idx = json.loads((OUT / "index.json").read_text(encoding="utf-8"))
        shard_of = {x[0]: x[4] for x in idx}
        seen = 0
        bad = 0
        for si in range(n_shard):
            bundle = json.loads((OUT / f"s{si:02d}.json").read_text(encoding="utf-8"))
            seen += len(bundle)
            for rid in bundle:                     # 每条 id 的 index 分片号必须自洽
                if shard_of.get(rid) != si:
                    bad += 1
        c1 = len(idx) == len(rows)
        c2 = seen == len(rows)
        c3 = bad == 0
        print(f"[verify] index {len(idx):,}/{len(rows):,} {'✓' if c1 else '✗'}"
              f" · 分片合计 {seen:,} {'✓' if c2 else '✗'}"
              f" · 分片号错位 {bad} {'✓' if c3 else '✗'}")
        return 0 if (c1 and c2 and c3) else 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
