#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""文档单一真源同步器（midicn-lib）

真源：本工作副本的 `docs/`（以及生成的 `midi_db/stats/music-verify-report.md`）。
清单：`tools/docs_manifest.json`（分 public / internal 两组 + mirrors 映射）。

用法
  python tools/sync_docs.py --check          # 检查漂移（差异/缺失/残留已退休文件），有漂移则退出码 1
  python tools/sync_docs.py --apply          # 把真源同步到各 mirror（数据仓根 + 数据仓 docs/ + tools/）
  python tools/sync_docs.py --adopt          # 真源缺失时从 mirror 反向收养（一次性修复）
  python tools/sync_docs.py --release V1.20  # 把文档装配进 release/midicn-lib-V1.20/（根 + docs/）

设计
  · 一个文件只有一个真源，其余都是副本；副本永不手工编辑
  · --check 可接入发布前置检查（见 tools/preflight.py），防止「改了一处忘另一处」
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'tools' / 'docs_manifest.json'


def md5(p: Path) -> str:
    h = hashlib.md5()
    with p.open('rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


PUBLIC_FALLBACK = {
  'note': '内置最小清单（仅公开组）。完整清单 tools/docs_manifest.json 属内部配置，不随公开仓分发。',
  'groups': {
    'public': {'desc': '对外公开文档', 'files': {
      'README.md': 'docs/README.md', 'README.en.md': 'docs/README.en.md',
      'LICENSE.md': 'docs/LICENSE.md', 'NOTICE.md': 'docs/NOTICE.md',
      'DATASET-CARD.md': 'docs/DATASET-CARD.md', 'DATASET-CARD.en.md': 'docs/DATASET-CARD.en.md',
      'DATA-QUALITY-STATEMENT.md': 'docs/DATA-QUALITY-STATEMENT.md',
      'DATA-QUALITY-STATEMENT.en.md': 'docs/DATA-QUALITY-STATEMENT.en.md',
      'DATA-STRUCTURE.md': 'docs/DATA-STRUCTURE.md', 'SOURCE-CATALOG.md': 'docs/SOURCE-CATALOG.md',
      'schema.md': 'docs/schema.md', 'EXPANSION-PLAN-BATCH34.md': 'docs/EXPANSION-PLAN-BATCH34.md',
      'CITATION.bib': 'docs/CITATION.bib'}},
    'public_docs': {'desc': '审计与质量档案', 'files': {
      'LICENSE-AUDIT.md': 'docs/LICENSE-AUDIT.md',
      'AUDIT-REPORT.md': 'docs/AUDIT-REPORT.md', 'AUDIT-REPORT-V2.md': 'docs/AUDIT-REPORT-V2.md',
      'AUDIT-REPORT-V3.md': 'docs/AUDIT-REPORT-V3.md', 'QUALITY-GATES.md': 'docs/QUALITY-GATES.md',
      'music-verify-report.md': 'docs/music-verify-report.md'}},
  },
  'mirrors': {}, 'tools_exclude': [],
}


def load() -> dict:
    if MANIFEST.exists():
        return json.loads(MANIFEST.read_text(encoding='utf-8'))
    return PUBLIC_FALLBACK      # 公开仓副本：无内部清单也能独立运行（仅公开组）


def pairs(cfg: dict):
    """(名称, 真源路径, 目标文件名) —— 目标名以 manifest 键为准"""
    for gname, g in cfg['groups'].items():
        for fname, src in g['files'].items():
            yield gname, fname, ROOT / src


def mirrors_for(cfg: dict, gname: str):
    return [ROOT / m for m in cfg['mirrors'].get(gname, [])]


def cmd_check(cfg: dict) -> int:
    print('=' * 84)
    print('文档同步检查（真源 → 副本）')
    print('=' * 84)
    drift = missing = 0
    for gname, fname, src in pairs(cfg):
        if not src.exists():
            print(f'  ✗ 真源缺失  {fname:34s} ← {src.relative_to(ROOT)}')
            missing += 1
            continue
        for m in mirrors_for(cfg, gname):
            dst = m / fname
            if not dst.exists():
                print(f'  ✗ 副本缺失  {fname:34s} → {dst.relative_to(ROOT.parent)}')
                drift += 1
            elif md5(dst) != md5(src):
                print(f'  ✗ 内容漂移  {fname:34s} → {dst.relative_to(ROOT.parent)}')
                drift += 1
    # 已退休文件不得复活
    for r in cfg.get('retired', []):
        if (ROOT / r).exists():
            print(f'  ✗ 已退休文件仍在  {r}')
            drift += 1
    # 副本目录里的重复旧副本（真源已上移）
    for r in cfg.get('retired_mirror', []):
        if (ROOT / r).exists():
            print(f'  ✗ 副本重复仍在  {r}')
            drift += 1
    # tools 同步
    t = cfg.get('tools')
    if t:
        src_dir, dst_dir = ROOT / t['src'], ROOT / t['dest']
        if src_dir.exists() and dst_dir.exists():
            excl = set(cfg.get('tools_exclude', []))
            for f in sorted(src_dir.iterdir()):
                if not f.is_file() or f.name.startswith('__') or f.name in excl:
                    continue
                d = dst_dir / f.name
                if not d.exists():
                    print(f'  ✗ 工具缺失  tools/{f.name}')
                    drift += 1
                elif md5(d) != md5(f):
                    print(f'  ✗ 工具漂移  tools/{f.name}')
                    drift += 1
            extra = [f.name for f in sorted(dst_dir.iterdir())
                     if f.is_file() and not (src_dir / f.name).exists() and not f.name.startswith('.')]
            if extra:
                print(f'  · 副本独有工具（真源没有）: {extra}')
    total = sum(1 for _ in pairs(cfg))
    print('-' * 84)
    print(f'清单 {total} 个文档 · 漂移 {drift} · 真源缺失 {missing}')
    return 1 if (drift or missing) else 0


def cmd_apply(cfg: dict) -> int:
    n = 0
    # 清理副本目录里的重复旧副本
    for r in cfg.get('retired_mirror', []):
        p = ROOT / r
        if p.exists():
            p.unlink()
            n += 1
            print(f'  × 清理重复副本 {r}')
    for gname, fname, src in pairs(cfg):
        if not src.exists():
            print(f'  · 跳过（真源缺失）{fname}')
            continue
        for m in mirrors_for(cfg, gname):
            m.mkdir(parents=True, exist_ok=True)
            dst = m / fname
            if dst.exists() and md5(dst) == md5(src):
                continue
            shutil.copy2(src, dst)
            n += 1
            print(f'  → {dst.relative_to(ROOT.parent)}')
    t = cfg.get('tools')
    if t:
        src_dir, dst_dir = ROOT / t['src'], ROOT / t['dest']
        dst_dir.mkdir(parents=True, exist_ok=True)
        excl = set(cfg.get('tools_exclude', []))
        for f in sorted(src_dir.iterdir()):
            if not f.is_file() or f.name.startswith('__') or f.name in excl:
                continue
            d = dst_dir / f.name
            if not (d.exists() and md5(d) == md5(f)):
                shutil.copy2(f, d)
                n += 1
                print(f'  → {d.relative_to(ROOT.parent)}')
    print(f'\n已同步 {n} 个文件')
    return 0


def cmd_adopt(cfg: dict) -> int:
    """真源缺失 → 从任一 mirror 反向收养（一次性修复用）"""
    n = 0
    for gname, fname, src in pairs(cfg):
        if src.exists():
            continue
        for m in mirrors_for(cfg, gname):
            cand = m / fname
            if cand.exists():
                src.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(cand, src)
                print(f'  ← 收养 {src.relative_to(ROOT)}  （来自 {cand.relative_to(ROOT.parent)}）')
                n += 1
                break
        else:
            print(f'  ✗ 无法收养（各处都缺）{fname}')
    print(f'\n已收养 {n} 个文件')
    return 0


def cmd_release(cfg: dict, ver: str) -> int:
    dest = ROOT / 'release' / f'midicn-lib-{ver}'
    if not dest.exists():
        print(f'发布目录不存在：{dest}', file=sys.stderr)
        return 2
    n = 0
    for gname, fname, src in pairs(cfg):
        if not src.exists():
            continue
        sub = dest if gname == 'public' else dest / 'docs'
        sub.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, sub / fname)
        n += 1
    print(f'已把 {n} 个文档装配到 {dest}（根 {len(cfg["groups"]["public"]["files"])} · docs/ '
          f'{len(cfg["groups"]["internal"]["files"])}）')
    return 0


def main(argv) -> int:
    ap = argparse.ArgumentParser(description='文档单一真源同步器')
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--apply', action='store_true')
    ap.add_argument('--adopt', action='store_true')
    ap.add_argument('--release', metavar='VER', help='装配进 release/midicn-lib-<VER>/')
    args = ap.parse_args(argv[1:])
    cfg = load()
    if args.adopt:
        return cmd_adopt(cfg)
    if args.apply:
        return cmd_apply(cfg)
    if args.release:
        return cmd_release(cfg, args.release)
    return cmd_check(cfg)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
