#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""路径单一真源 —— 数据侧（Library 线）所有工具都应从这里取路径。

> **公开件**：用公开文件名（无 `_` 前缀），因为公开工具（`build_release.py` 等）
> 会 `import paths`；若叫 `_paths` 则不会同步到公开仓，公开用户拿到的工具会 import 失败。

为什么需要它
------------
2026-09-24 工作区做了一次目录规范化（见 `plans/HANDOFF-目录重构说明.md` §三）：

    lib.midicn.com/sources/          →  lib/sources/
    lib.midicn.com/data/             →  lib/data/
    lib.midicn.com/midi_db/          →  lib/work/midi_db/
    lib.midicn.com/tools/            →  lib/work/tools/      ← 本文件所在
    lib.midicn.com/docs/             →  lib/work/docs/
    lib.midicn.com/release/          →  lib/output/
    lib.midicn.com/release/site-repo/→  lib/site/
    midi-lib-repo/                   →  lib/library/
    mid.midicn.com/site-repo/        →  mid/site/
    zip.midicn.com/site-repo/        →  zip/site/

**要留意的点**：工具里普遍写 `ROOT = parents[1]`，
搬迁后 `parents[1]` 从「lib 根」变成了「lib/work」——
对 `midi_db` / `tools` / `docs` 恰好仍然正确（它们一起搬进了 `lib/work/`），
但对 `data/` 与 `release/` **静默失效**（指向不存在的位置）。
所以路径**不要各自推算**，一律 import 本模块。

仓名（2026-09-24 改名，旧名 301 重定向）：
    midicn/midi-lib-site → midicn/lib      midicn/mid-site → midicn/mid
    midicn/zip-site      → midicn/zip      midicn/midi-lib → midicn/midi-library
"""
from __future__ import annotations

from pathlib import Path

# ── 三个根 ────────────────────────────────────────────────────────────────
WORK = Path(__file__).resolve().parents[1]      # lib/work/     （工具、文档、曲目真源）
LIB = WORK.parent                               # lib/          （数据侧本仓工作副本）
MIDI = LIB.parent                               # 工作区根

# ── 数据侧目录 ────────────────────────────────────────────────────────────
TOOLS = WORK / "tools"
DOCS = WORK / "docs"
TRACKS = WORK / "midi_db" / "tracks"
MIDI_DB = WORK / "midi_db"

SOURCES = LIB / "sources"                       # 上游原始素材（永不删）
DATA = LIB / "data"                             # 构建输入（注意：不是 staging！）
OUTPUT = LIB / "output"                         # 发布产物（旧 release/）
LIBRARY = LIB / "library"                       # 数据仓克隆 = midicn/midi-library
LAKH_QUARANTINE = LIB / "_lakh_quarantine"
DESIGN = LIB / "design"

# ── 站点仓（新布局都在工作区根下）────────────────────────────────────────
SITES = {
    "lib": MIDI / "lib" / "site",
    "mid": MIDI / "mid" / "site",
    "zip": MIDI / "zip" / "site",
}

# ── 仓全名（改名后）──────────────────────────────────────────────────────
REPOS = {
    "lib": "midicn/lib",
    "mid": "midicn/mid",
    "zip": "midicn/zip",
    "library": "midicn/midi-library",
}

# ── 域名 / 品牌（不变）───────────────────────────────────────────────────
HOSTS = {"lib": "lib.midicn.com", "mid": "mid.midicn.com", "zip": "zip.midicn.com"}


def lib_site() -> Path:
    """lib 站产物仓（旧 `release/site-repo`）。"""
    return SITES["lib"]


def output_dir(version: str | None = None) -> Path:
    """发布产物目录：`lib/output/`（全量）或 `lib/output/midicn-lib-<version>/`（单版本树）。"""
    return OUTPUT / f"midicn-lib-{version}" if version else OUTPUT


def version() -> str:
    """从 `build_release.py` 读版本号（**单源**）。返回形如 `v1.23`。"""
    import re
    src = (TOOLS / "build_release.py").read_text(encoding="utf-8")
    m = re.search(r'^VERSION\s*=\s*"([^"]+)"', src, re.M)
    if not m:
        raise SystemExit("[err] 在 tools/build_release.py 里找不到 VERSION")
    return "v" + m.group(1).lstrip("v")


def missing() -> list[tuple[str, Path]]:
    """自检：返回不存在的关键目录（空列表 = 布局正常）。"""
    must = [("工具", TOOLS), ("文档", DOCS), ("曲目真源", TRACKS),
            ("上游素材", SOURCES), ("构建输入", DATA), ("发布产物", OUTPUT),
            ("数据仓克隆", LIBRARY), ("lib 站", SITES["lib"]),
            ("mid 站", SITES["mid"]), ("zip 站", SITES["zip"])]
    return [(why, p) for why, p in must if not p.exists()]


if __name__ == "__main__":
    print(f"WORK   = {WORK}")
    print(f"LIB    = {LIB}")
    print(f"MIDI   = {MIDI}")
    print(f"VERSION= {version()}")
    bad = missing()
    if bad:
        print("\n✗ 缺失：")
        for why, p in bad:
            print(f"    {why:12} {p}")
    else:
        print("\n✓ 布局正常（10 个关键目录全部就位）")
