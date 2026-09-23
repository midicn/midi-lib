#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F1 · lakh 现代版权作品剔除器（含人工复核台账产出）。

用法：
  # 干跑：只出报告，不改数据
  python tools/exclude_lakh_modern.py

  # 执行：标 verify_flag=broken + 移走实体 MIDI（先自动备份）
  python tools/exclude_lakh_modern.py --apply

产出：
  docs/internal/lakh-review-420.md   全量候选台账（逐条分类 + 理由），供人工复核
  midi_db/backup-docs-<date>/lakh.jsonl.bak   数据备份
  <root>/_lakh_quarantine/<id>.mid     被剔除的 MIDI 实体（可人工检查后删）

设计要点：
  · 三分类词表见 tools/lakh_denylist.py —— 不用单一正则，避免误删公有领域内容
  · 只剔除 modern / artist 两类；traditional / false-positive 一律保留
  · 阈值可调：--min-conf 控制从严（默认把 'other' 视为保留）
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lakh_denylist import (  # noqa: E402
    ARTIST_NAMES,
    FALSE_POSITIVE,
    MODERN_COPYRIGHT,
    MODERN_DIRS,
    TRADITIONAL_PD,
    classify,
    classify_record,
    composer_is_copyrighted,
    top_dir,
)

ROOT = Path(__file__).resolve().parents[1]
TRACKS = ROOT / "midi_db" / "tracks" / "lakh.jsonl"
TODAY = date.today().isoformat()
REPORT = ROOT / "docs" / "internal" / f"lakh-review-{TODAY}.md"
BACKUP_DIR = ROOT / "midi_db" / f"backup-docs-{TODAY.replace('-', '')}"
QUARANTINE = ROOT / "_lakh_quarantine"

# 候选筛选：这些词才会进入人工复核视野（避免把 9,630 首全列出来）
CANDIDATE_RE = re.compile(r"christmas|carol|xmas|noel|santa|rudolph|jingle|frosty", re.I)


def resolve_midi(r: dict) -> Path | None:
    """midi.file 优先，回退 src_path（新源写法）。"""
    mf = (r.get("midi") or {}).get("file")
    if mf and (ROOT / mf).exists():
        return ROOT / mf
    sp = (r.get("src_path") or "").replace("\\", "/")
    if sp and (ROOT / sp).exists():
        return ROOT / sp
    return None


# 与 tools/build_release.py 保持一致的发布口径（勿各自为政）
SKIP_ZONES = {"pending"}
SKIP_SOURCES = {"musedata"}
SOURCE_ZONE = {"chinafolk": "study", "atepp": "main"}


def published_total() -> int:
    """复现 build_release.py 的发布口径，为"剔除前后总数"提供准确基线。

    之前这里硬编码 134191，一旦数据变动就会报告错误总数——改为实时计算。
    """
    n = 0
    for f in sorted((ROOT / "midi_db" / "tracks").glob("*.jsonl")):
        for line in f.open(encoding="utf-8"):
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except Exception:
                continue
            src = r.get("source")
            zone = SOURCE_ZONE.get(src, r.get("zone"))
            if src in SKIP_SOURCES or zone in SKIP_ZONES:
                continue
            if r.get("verify_flag") == "broken" or r.get("duplicate_of"):
                continue
            if resolve_midi(r) is None:
                continue
            n += 1
    return n


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="实际写入（默认干跑）")
    ap.add_argument("--limit", type=int, default=0, help="仅处理前 N 条（调试用）")
    args = ap.parse_args(argv[1:])

    if not TRACKS.exists():
        print(f"[err] 未找到 {TRACKS}")
        return 1

    rows = []
    for line in TRACKS.open(encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        rows.append(json.loads(line))
    print(f"[lakh] 读入 {len(rows):,} 条")

    # ── 分类 ──────────────────────────────────────────────────────────
    # 用 classify_record：在标题之外叠加「一级目录是否现代艺人/游戏/商业包」与
    # 「作曲家卒年是否晚于 PD 截止线」两个信号（第二轮排查新增）。
    buckets: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        t = r.get("title") or ""
        cls = classify_record(r)
        if cls == "other":
            # 非候选词命中，且不含泛圣诞词 → 不进复核
            if not CANDIDATE_RE.search(t):
                continue
            cls = "other"
        buckets[cls].append(r)

    dup_ids = {r["id"] for r in rows if r.get("duplicate_of")}
    bro_ids = {r["id"] for r in rows if r.get("verify_flag") == "broken"}

    def already_out(r: dict) -> bool:
        return r["id"] in dup_ids or r["id"] in bro_ids

    counts = Counter()
    for k, v in buckets.items():
        live = [r for r in v if not already_out(r)]
        counts[k] = len(live)

    print("\n── 候选分类 ──────────────────────────")
    for k in ("modern", "artist", "modern-dir", "modern-composer",
              "traditional", "false-positive", "other"):
        tot = len(buckets.get(k, []))
        print(f"  {k:16s} 命中 {tot:4d}  （其中可发布 {counts[k]:4d}）")
    to_remove = (counts["modern"] + counts["artist"]
                 + counts["modern-dir"] + counts["modern-composer"])
    # 基线总数：从 build_release 的实际发布口径读取（跳 musedata/pending/broken/dup）
    pub_total = published_total()
    print(f"\n  建议剔除（modern + artist + 现代目录 + 晚卒作曲家）: {to_remove}")
    print(f"  剔除后总数: {pub_total - to_remove:,}")

    # ── 人工复核台账 ──────────────────────────────────────────────────
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        f"# lakh 版权复核台账（{TODAY}）",
        "",
        "> 由 `tools/exclude_lakh_modern.py` 生成。**这是一份需要人工逐条确认的清单。**",
        "> 判定依据：词曲作者卒年是否在保护期内（中国：作者生前 + 50 年）。",
        "",
        f"## 汇总（lakh 共 {len(rows):,} 首）",
        "",
        "| 分类 | 命中 | 未剔除 | 处置 |",
        "| --- | ---: | ---: | --- |",
        f"| modern（现代版权作品） | {len(buckets.get('modern', []))} | {counts['modern']} | **剔除** |",
        f"| artist（演唱/演奏者名） | {len(buckets.get('artist', []))} | {counts['artist']} | **剔除** |",
        f"| modern-dir（现代艺人/游戏/商业包目录） | {len(buckets.get('modern-dir', []))} | {counts['modern-dir']} | **剔除** |",
        f"| modern-composer（卒年晚于 PD 线的作曲家） | {len(buckets.get('modern-composer', []))} | {counts['modern-composer']} | **剔除** |",
        f"| traditional（传统 PD） | {len(buckets.get('traditional', []))} | {counts['traditional']} | 保留 |",
        f"| false-positive（正则误命中） | {len(buckets.get('false-positive', []))} | {counts['false-positive']} | 保留 |",
        f"| other（待人工判定） | {len(buckets.get('other', []))} | {counts['other']} | **需人工判断** |",
        "",
        f"**建议剔除合计 {to_remove} 首 → 总数 {pub_total - to_remove:,}**",
        "",
    ]

    for key, title, action in [
        ("modern", "① modern · 现代版权作品（剔除）", "剔除"),
        ("artist", "② artist · 现代艺人/团体（剔除）", "剔除"),
        ("modern-dir", "②b modern-dir · 现代艺人/游戏/商业包目录（剔除）", "剔除"),
        ("modern-composer", "②c modern-composer · 卒年晚于 PD 线的作曲家（剔除）", "剔除"),
        ("other", "③ other · 待人工判定", "待判"),
        ("traditional", "④ traditional · 传统公有领域（保留）", "保留"),
        ("false-positive", "⑤ false-positive · 正则误命中（保留）", "保留"),
    ]:
        items = buckets.get(key, [])
        lines += [f"## {title}", "", f"共 {len(items)} 条", ""]
        if not items:
            lines += ["（无）", ""]
            continue
        lines += ["| id | 标题 | 状态 |", "| --- | --- | --- |"]
        for r in sorted(items, key=lambda x: x["id"]):
            st = "已剔" if already_out(r) else action
            t = (r.get("title") or "").replace("|", "\\|")
            lines.append(f"| `{r['id']}` | {t} | {st} |")
        lines.append("")

    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"\n[report] {REPORT.relative_to(ROOT)}  （{len(lines)} 行）")

    if not args.apply:
        print("\n[干跑] 未改动数据。确认台账后加 --apply 执行。")
        return 0

    # ── 执行剔除 ──────────────────────────────────────────────────────
    targets = [r for k in ("modern", "artist", "modern-dir", "modern-composer")
               for r in buckets.get(k, []) if not already_out(r)]
    print(f"\n[apply] 待剔除 {len(targets)} 首")

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    # 不覆盖既有备份：第二轮曾把第一轮的原始备份冲掉（原始未改状态只能从隔离区反推）。
    # 改为自动编号 lakh.jsonl.bak / .bak2 / .bak3 …
    bak = BACKUP_DIR / "lakh.jsonl.bak"
    i = 1
    while bak.exists():
        i += 1
        bak = BACKUP_DIR / f"lakh.jsonl.bak{i}"
    shutil.copy2(TRACKS, bak)
    print(f"[backup] {bak}")

    QUARANTINE.mkdir(exist_ok=True)
    kill_ids = {r["id"] for r in targets}
    moved = 0
    for r in targets:
        p = resolve_midi(r)
        if p and p.exists():
            shutil.move(str(p), str(QUARANTINE / f"{r['id']}.mid"))
            moved += 1

    out_lines = []
    for line in TRACKS.open(encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        r = json.loads(line)
        if r["id"] in kill_ids:
            r["verify_flag"] = "broken"
            r["extra"] = dict(r.get("extra") or {})
            r["extra"]["excluded_reason"] = "现代版权作品（作者卒年在保护期内）"
            r["extra"]["excluded_on"] = TODAY
        out_lines.append(json.dumps(r, ensure_ascii=False, separators=(",", ":")))

    TRACKS.write_text("\n".join(out_lines) + "\n", encoding="utf-8")
    print(f"[done] 标记 broken {len(kill_ids)} 条 · 移走实体 {moved} 个")
    print(f"       实体隔离区：{QUARANTINE}")
    print(f"       复核后可删除隔离区，或移回以撤销。")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
