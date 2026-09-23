#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""版权合规审计器 · preflight 第 4 关。

背景：2026-09-23 发现 lakh 混入 356 首在保护期内的现代商业作品（根因：`ingest_lakh.py`
把 `christmas|carol` 当成公有领域代理）。本审计器把该结论固化为**可重复执行的断言**，
防止后续任何改动把受保护内容重新带进发布包。

三项断言
--------
1. **发布侧 lakh 无现代版权作品**（硬失败）
   对 lakh 所有可发布曲目，用与 ingest 同源的词表 `tools/lakh_denylist.py` 扫描
   标题 + 源路径（含分隔符归一化），命中 `MODERN_RE` / `ARTIST_RE` 即失败。
   范围限定 lakh：oga / emopia / groove 等来源的现代曲目是**上游逐曲明确授权**的
   （CC0 / CC BY / CC BY-NC-SA），不属于本项风险。
2. **内嵌歌词分布可解释**（信息 + 越界告警）
   输出 `midi.lyrics_inline` 的来源分布。若出现词表外的新来源，提示人工确认其授权基础。
3. **歌词独立权利层条款在位**（硬失败）
   `docs/LICENSE.md` 必须含 §2.3 内嵌歌词条款，`docs/NOTICE.md` 必须含歌词节。

用法
----
  python tools/audit_license.py           # 完整输出
  python tools/audit_license.py --quiet   # 仅输出结论（给 preflight 用）

退出码：0 全部通过 / 1 有硬失败
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from lakh_denylist import MODERN_RE, ARTIST_RE, classify_record  # noqa: E402

DROP_KINDS = {"modern", "artist", "modern-dir", "modern-composer"}

TRACKS = ROOT / "midi_db" / "tracks"
LICENSE_MD = ROOT / "docs" / "LICENSE.md"
NOTICE_MD = ROOT / "docs" / "NOTICE.md"

# 与 build_release.py 同源的发布口径
SKIP_ZONES = {"pending"}
SKIP_SOURCES = {"musedata"}
SOURCE_ZONE = {"chinafolk": "study", "atepp": "main"}

# 允许承载现代作品的来源：上游逐曲明确授权（非本项风险范围）

# 硬失败的来源范围：词表是针对 lakh（文件名/标题混杂流行乐）标定并逐条人工复核的，
# 套到 cyberhymnal/aria/abcmisc 这类**策展型 PD 语料**会产生大量误报
# （如 cyberhymnal「Abba Padre Te Adoramos」的 Abba 是阿拉米语"父"，非乐团 ABBA）。
# 故硬断言只覆盖 lakh；其它来源的命中作为**人工复核提示**输出。
SCOPE = {"lakh"}


def probes(*values: str) -> tuple[str, ...]:
    """路径/标题的分隔符归一化变体（路径写 White-Christmas，词表按空格写）。"""
    out = []
    for v in values:
        if not v:
            continue
        out += [v, re.sub(r"[-_]+", " ", v), re.sub(r"[-_\s]+", "", v)]
    return tuple(out)


def published(r: dict) -> bool:
    src = r.get("source")
    zone = SOURCE_ZONE.get(src, r.get("zone"))
    if src in SKIP_SOURCES or zone in SKIP_ZONES:
        return False
    if r.get("verify_flag") == "broken" or r.get("duplicate_of"):
        return False
    return True


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args(argv[1:])

    def say(*a):
        if not args.quiet:
            print(*a)

    def verdict(*a):
        """结论行永远输出（供 preflight 抓取），不受 --quiet 影响。"""
        print(*a)

    fails: list[str] = []
    pub = Counter()
    scope_hits: list[tuple[str, str, str]] = []
    other_hits = Counter()
    lyrics = Counter()
    total_pub = 0

    for f in sorted(TRACKS.glob("*.jsonl")):
        for line in f.open(encoding="utf-8"):
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except Exception:
                continue
            if not published(r):
                continue
            src = r.get("source")
            total_pub += 1
            pub[src] += 1

            if (r.get("midi") or {}).get("lyrics_inline"):
                lyrics[src] += 1

            # 复用单一真源 lakh_denylist.classify_record（标题 + 目录 + 卒年），
            # 与清理器、ingest 三处同源，避免"审计与清理口径不一致"。
            if classify_record(r) not in DROP_KINDS:
                continue
            rec = (r.get("id", "?"), src, r.get("title") or "")
            if src in SCOPE:
                scope_hits.append(rec)
            else:
                other_hits[src] += 1

    # ── 断言 1 ──────────────────────────────────────────────────────────
    say("=" * 84)
    say("版权合规审计 · audit_license")
    say("=" * 84)
    say(f"发布侧曲目 {total_pub:,} 首 · 来源 {len(pub)} 个")
    say(f"硬断言范围：{sorted(SCOPE)}（词表标定与人工复核均针对该来源）")

    say(f"\n[1] lakh 现代版权作品   发布 {pub.get('lakh', 0):,} 首 · 命中 {len(scope_hits)}")
    if scope_hits:
        fails.append(f"lakh 仍有 {len(scope_hits)} 首现代版权作品在发布侧")
        for rid, src, t in scope_hits[:25]:
            say(f"    ✗ {rid}  [{src}]  {t}")
        if len(scope_hits) > 25:
            say(f"    … 另有 {len(scope_hits) - 25} 首")
    else:
        say("    ✓ 无（MODERN_RE / ARTIST_RE 全量扫描 0 命中）")

    say("\n[1b] 其它来源的命中（**仅提示，不判失败，勿据此处置**）")
    if other_hits:
        top = other_hits.most_common(5)
        say("    词表是为 lakh（文件名/标题混杂流行乐）标定并逐条人工复核的，套到"
            "策展型 PD 语料上\n    会产生大量误报（短模式如 `\\bsia\\b`/`\\babba\\b` 会命中人名与外语词），"
            "故此处不设阈值。")
        for src, n in top:
            say(f"      · {src:12} {n:>5}")
        say(f"      … 共 {len(other_hits)} 个来源有命中，合计 {sum(other_hits.values()):,} 条（含大量误报，未逐条核）")
    else:
        say("    （无）")

    # ── 断言 2 ──────────────────────────────────────────────────────────
    say("\n[2] 内嵌歌词来源分布（信息项）")
    n_ly = sum(lyrics.values())
    for src, n in lyrics.most_common():
        say(f"    {src:14} {n:>6}")
    say(f"    合计 {n_ly:,} 首")
    unknown = set(lyrics) - {"openscore", "m21", "wikifonia", "mutopia", "lakh", "cyberhymnal"}
    if unknown:
        say(f"    ⚠ 出现词表外的新带词来源：{sorted(unknown)} —— 请确认其歌词授权基础")

    # ── 断言 3 ──────────────────────────────────────────────────────────
    say("\n[3] 歌词独立权利层条款在位")
    lic = LICENSE_MD.read_text(encoding="utf-8") if LICENSE_MD.exists() else ""
    not_ = NOTICE_MD.read_text(encoding="utf-8") if NOTICE_MD.exists() else ""
    checks = [
        ("LICENSE.md §2.3 内嵌歌词条款", "2.3 内嵌歌词" in lic),
        ("NOTICE.md 内嵌歌词节", "内嵌歌词" in not_),
    ]
    for label, ok in checks:
        say(f"    {'✓' if ok else '✗'} {label}")
        if not ok:
            fails.append(f"{label} 缺失")

    say("\n" + "-" * 84)
    if fails:
        verdict(f"audit_license：✗ 失败 {len(fails)} 项")
        for x in fails:
            verdict(f"   · {x}")
        return 1
    verdict("audit_license：✓ 通过（发布侧无现代版权作品 · 歌词权利层条款在位）")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
