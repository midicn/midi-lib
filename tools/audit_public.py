#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""公开内容卫生审计器 —— **发布强制门之一**。

为什么需要它
------------
2026-09-23 用户指出：**内部的推理、讨论、过程记录不该出现在网站上，也不该出现在公开仓/发布包里**。
当时的实例：
  · 「（与法律口径一致，不另设固定时限）」—— 把我们的法律推理写进了公开条款
  · 页面注释里写「用户明确反馈不要这个行为」
  · 12 个页面的 SEO 注释里带着内部脚本名 `_apply_site_shell.py`
  · `provenance.json` 的「本地证据」路径指向 `docs/internal/…`
  · 规划文档 `EXPANSION-PLAN-BATCH34.md`（批次计划·待确认）随包分发
  · 公开文档里的 2 处「待补」TODO
这类泄漏**极易复发**，故做成可自动执行的检查，纳入 preflight。

检查对象
--------
① 三站页面与脚本：`*/site-repo/**` 的 html / js / css / txt / xml / json（排除数据分片与 `_` 前缀件）
② 公开文档：`tools/docs_manifest.json` 里 `public` 与 `public_docs` 两组指向的文件
   （这两组正是会被同步到公开仓、并装配进 Release 的那批）

规则
----
- **BLOCK**：必须为 0，否则发布中止
- **WARN**：只提示（例如同义词也许正当）

用法
  python tools/audit_public.py              # 审计（BLOCK > 0 时退出码 1）
  python tools/audit_public.py --warn-only  # 只看报告
  python tools/audit_public.py --list       # 列出被检查的文件
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MIDI = ROOT.parent

# ── BLOCK 规则：这些出现在公开内容里就是缺陷 ──────────────────────────────
BLOCK = [
    # 内部路径与内部件（`_` 前缀 = 内部，永不同步到公开仓）
    (r"docs/internal/|internal/[a-z\-]+\.md",                  "内部文档路径"),
    (r"tools/_[a-z_]+\.py|_[a-z_]+\.py 的",                     "内部脚本名"),
    # 把我们的推理过程写进公开条款
    (r"口径一致|时限口径|不另设固定|不自行承诺|我们内部|内部讨论|内部台账",
     "内部推理/内部口径"),
    # 把用户意见/决策过程写进公开内容
    (r"用户(明确)?(反馈|要求|拍板|决策|确认)",                   "用户意见写进公开内容"),
    # 过程与项目管理痕迹
    (r"（三犯）|踩坑记录|踩过|现场发现|E[1-9][0-9]?\s*[:：]",     "过程记录/发现编号"),
    (r"阶段\s*[0-9]|批次\s*[0-9]|验收清单|回滚方案|发布计划",      "项目管理术语"),
    (r"\bTODO\b|\bFIXME\b|待补|待办|待修",                       "TODO 残留"),
    (r"WorkBuddy|\.workbuddy|MEMORY\.md|你的助手|内部工具",       "内部工具/环境"),
]

# ── WARN 规则：可疑但可能正当 ─────────────────────────────────────────────
WARN = [
    (r"设计系统 v[0-9]|做减法定案|硬门槛判定",   "内部规范命名"),
    (r"本次整改|本轮|这次改",                    "修订过程口吻"),
    (r"临时|暂定|待定|先这样",                    "未定稿口吻"),
]

# 合法白名单：命中这些不算（公开工具名、正常用语）
ALLOW = re.compile(
    r"tools/ingest_[a-z_]+\.py|tools/build_release\.py|tools/pack_release\.py"
    r"|tools/build_dim_packs\.py|tools/provenance\.py|tools/preflight\.py"
    r"|tools/sync_docs\.py|tools/music_verify\.py|tools/dedup[a-z_]*\.py"
    r"|tools/quality_pipeline\.py|tools/infer_[a-z_]+\.py|tools/fetch_[a-z_]+\.py"
    r"|tools/dl_[a-z_]+\.py|tools/normalize_[a-z_]+\.py|tools/enrich_[a-z_]+\.py"
    r"|tools/gen_[a-z_]+\.py|tools/analyze_[a-z_]+\.py|tools/fix_[a-z_]+\.py"
    r"|tools/audit[a-z0-9_]*\.py|tools/lakh_denylist\.py|tools/exclude_[a-z_]+\.py"
    r"|tools/extract_[a-z_]+\.py|tools/ingest_lakh\.py|tools/music21[a-z_]*\.py",
    re.I)


def public_files() -> list[Path]:
    out: list[Path] = []
    for site in ("lib.midicn.com/release/site-repo", "mid.midicn.com/site-repo",
                 "zip.midicn.com/site-repo"):
        base = MIDI / site
        if not base.exists():
            continue
        for f in base.rglob("*"):
            if not f.is_file() or f.name.startswith("_") or f.name.startswith("."):
                continue
            if "__pycache__" in f.parts or "node_modules" in f.parts:
                continue
            if f.suffix in (".html", ".js", ".css", ".txt", ".xml"):
                out.append(f)
    man_p = ROOT / "tools" / "docs_manifest.json"
    if man_p.exists():
        man = json.loads(man_p.read_text(encoding="utf-8"))
        for g in ("public", "public_docs"):
            for _name, rel in man.get("groups", {}).get(g, {}).get("files", {}).items():
                p = ROOT / rel
                if p.exists():
                    out.append(p)
    return sorted(set(out))


def scan(files: list[Path]) -> tuple[list, list]:
    blocks, warns = [], []
    for f in files:
        try:
            s = f.read_text(encoding="utf-8")
        except Exception:
            continue
        try:
            rel = f.relative_to(MIDI).as_posix()
        except ValueError:
            rel = f.as_posix()
        for i, line in enumerate(s.splitlines(), 1):
            # 先剥掉 JS 正则字面量（如 /口径一致|不另设固定/）与合法工具名，
            # 否则审计器与 e2e 里的「规则定义」会被自己判为违规（自指假阳性）
            clean = re.sub(r"/[^/\n]{0,120}/[gimsuy]*", "", line)
            clean = ALLOW.sub("", clean)
            for pat, why in BLOCK:
                if re.search(pat, clean):
                    blocks.append((rel, i, why, line.strip()[:150]))
                    break
            else:
                if not re.search(r"历史快照|本文件为过程文档", line):
                    for pat, why in WARN:
                        if re.search(pat, clean):
                            warns.append((rel, i, why, line.strip()[:150]))
                            break
    return blocks, warns


def main(argv) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--warn-only", action="store_true")
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args(argv[1:])

    files = public_files()
    if args.list:
        for f in files:
            print("  " + f.relative_to(MIDI).as_posix())
        print(f"  共 {len(files)} 个公开文件")
        return 0

    blocks, warns = scan(files)
    print(f"公开内容卫生审计 · 检查 {len(files)} 个文件")
    if blocks:
        print(f"\n✗ BLOCK {len(blocks)} 处（**必须清掉才能发布**）：")
        for rel, i, why, txt in blocks[:40]:
            print(f"    {rel}:{i}  [{why}]  {txt}")
        if len(blocks) > 40:
            print(f"    … 另有 {len(blocks)-40} 处")
    if warns:
        print(f"\n· WARN {len(warns)} 处（提示，可接受）：")
        for rel, i, why, txt in warns[:10]:
            print(f"    {rel}:{i}  [{why}]  {txt}")
        if len(warns) > 10:
            print(f"    … 另有 {len(warns)-10} 处")

    if not blocks:
        print("\n✓ 通过：公开内容无内部讨论 / 内部路径 / 内部脚本名 / TODO 残留")
    return 0 if (args.warn_only or not blocks) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
