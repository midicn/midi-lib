#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""D8 去重执行（保守版）· 标记不删

策略（质量优先）：
  1. MD5 完全相同组 → 高置信，标记
  2. 指纹重复且**标题相同**组 → 高置信，标记
  3. 指纹重复但仅同作曲家 → **不动**（可能为不同作品），输出待核清单
  处理方式：给被判定重复的记录加 `duplicate_of` 字段（**保留文件与记录**，发布时按此过滤）

保留优先序：zone(main > research > pending > piano-special) > 元数据完整度 > id 小者

用法：
  python tools/dedup_apply.py [--dry-run]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from dedup import QUANT, iter_tracks, pitch_fingerprint  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
TRACKS = ROOT / "midi_db" / "tracks"
REPORT = ROOT / "midi_db" / "stats" / "dedup-applied.md"
PENDING = ROOT / "midi_db" / "stats" / "dedup-pending-review.md"
ZONE_RANK = {"main": 0, "research": 1, "pending": 2, "piano-special": 3}


def completeness(r: dict) -> int:
    return sum(1 for k in ("title", "opus", "form", "key", "period", "region")
               if r.get(k))


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv[1:])

    # 载入全部记录
    files = sorted(TRACKS.glob("*.jsonl"))
    data = {f: [json.loads(l) for l in f.open(encoding="utf-8")] for f in files}
    by_id = {}
    for f, rows in data.items():
        for r in rows:
            by_id[r["id"]] = r

    # 阶段 1：MD5 组
    md5_map = defaultdict(list)
    for r, p in iter_tracks():
        md5_map[hashlib.md5(p.read_bytes()).hexdigest()].append(r["id"])
    md5_dups = [v for v in md5_map.values() if len(v) > 1]

    # 阶段 2：指纹组（标题相同才处理）
    cache = json.loads((ROOT / "tools" / "state" / "dedup-fingerprints.json")
                       .read_text(encoding="utf-8")) if (ROOT / "tools" / "state" / "dedup-fingerprints.json").exists() else {}
    fp_map = defaultdict(list)
    for r, p in iter_tracks():
        fp = cache.get(r["midi"]["file"])
        if fp:
            fp_map[fp].append(r["id"])
    fp_title_dups, fp_comp_only = [], []
    for v in fp_map.values():
        if len(v) < 2:
            continue
        titles = {(by_id[i].get("title") or "") for i in v}
        if len(titles) == 1 and next(iter(titles)):
            fp_title_dups.append(v)
        else:
            fp_comp_only.append(v)

    def pick_keeper(ids: list[str]) -> tuple[str, list[str]]:
        ids = sorted(ids)
        best = min(ids, key=lambda i: (ZONE_RANK.get(by_id[i].get("zone"), 9),
                                       -completeness(by_id[i]), i))
        return best, [i for i in ids if i != best]

    marked = 0
    groups = 0
    for group in md5_dups + fp_title_dups:
        keep, drop = pick_keeper(group)
        groups += 1
        for i in drop:
            by_id[i]["duplicate_of"] = keep
            marked += 1

    print(f"[dedup] MD5 组 {len(md5_dups)} · 同标题指纹组 {len(fp_title_dups)} "
          f"→ 共 {groups} 组，标记重复 {marked} 条", flush=True)
    print(f"[dedup] 仅同作曲家（保守不动）：{len(fp_comp_only)} 组待人工复核", flush=True)

    if not args.dry_run:
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        bdir = ROOT / "midi_trash" / f"pre-dedup-{ts}"
        bdir.mkdir(parents=True, exist_ok=True)
        for f, rows in data.items():
            shutil.copy2(f, bdir / f.name)
            with f.open("w", encoding="utf-8", newline="\n") as fh:
                for r in rows:
                    fh.write(json.dumps(r, ensure_ascii=False, separators=(",", ":")) + "\n")
        print(f"[write] 已写回（备份 {bdir.relative_to(ROOT)}）", flush=True)

    # 报告
    lines = [
        "# 去重执行报告（保守版 · 标记不删）",
        "",
        f"> 生成：{datetime.now().isoformat(timespec='seconds')} · {'（试运行）' if args.dry_run else '（已写回）'}",
        "",
        f"- MD5 完全相同组：**{len(md5_dups)}**",
        f"- 指纹重复且标题相同组：**{len(fp_title_dups)}**",
        f"- 标记为重复的记录（`duplicate_of`）：**{marked}** 条",
        f"- 仅同作曲家、保守未动：**{len(fp_comp_only)}** 组（待人工复核）",
        "",
        "## 处置说明",
        "",
        "1. 被标记的记录**保留在库中**（文件与元数据完整），发布时按 `duplicate_of` 字段过滤",
        "2. 保留优先序：分区（main > research > pending > piano-special）→ 元数据完整度 → id 序",
        "3. 复核清单见 `dedup-pending-review.md`",
    ]
    REPORT.write_text("\n".join(lines), encoding="utf-8")

    pend = ["# 待人工复核的疑似重复（仅同作曲家，未处理）", "",
            f"> {len(fp_comp_only)} 组", ""]
    for v in fp_comp_only[:200]:
        desc = " | ".join(f"{i}·{by_id[i].get('composer_slug')}·{(by_id[i].get('title') or '(无题)')[:24]}"
                          for i in sorted(v)[:3])
        pend.append(f"- {desc}")
    PENDING.write_text("\n".join(pend), encoding="utf-8")
    print(f"[report] {REPORT.relative_to(ROOT)} · {PENDING.relative_to(ROOT)}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
