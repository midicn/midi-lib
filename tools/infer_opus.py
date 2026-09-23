#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""opus/no 提取：从标题的 Op./No. 模式提取作品号与编号（纯本地 · dry-run 先行）

只提取明确模式：
  - Opus 号：`Op. 10` / `Op.10` / `op. 10` / `Opus 10`（\b 边界，最多 3 位数字）
  - 编号：  `No. 1` / `No.1` / `nr. 2` / `Nr. 2`（同上）
  - `Op.2 No.1` 两者都提；只提各自第一个。
不提取 WoO/BWV/D/Hob 等其他编号体系（opus 字段是数字型，语义不符——宁缺不混）。
不覆盖已有 opus/no 值。
"""
from __future__ import annotations
import argparse, json, re, sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACKS = ROOT / 'midi_db' / 'tracks'

RE_OP = re.compile(r'\bop(?:us)?\.?\s?(\d{1,3})\b', re.I)
RE_NO = re.compile(r'\bno\.?\s?(\d{1,3})\b', re.I)


def run(dry_run: bool):
    files = sorted(TRACKS.glob('*.jsonl'))
    stats = Counter()
    per_src = Counter()
    samples = []

    for f in files:
        lines = f.read_text(encoding='utf-8').splitlines()
        modified = False
        for i, line in enumerate(lines):
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            title = r.get('title') or ''
            if not title:
                continue
            changed = False

            if not r.get('opus'):
                m = RE_OP.search(title)
                if m:
                    r['opus'] = int(m.group(1))
                    stats['opus'] += 1
                    per_src[r.get('source', '?')] += 1
                    changed = True

            if not r.get('no'):
                m = RE_NO.search(title)
                if m:
                    r['no'] = int(m.group(1))
                    stats['no'] += 1
                    changed = True

            if changed:
                lines[i] = json.dumps(r, ensure_ascii=False, separators=(',', ':'))
                modified = True
                if len(samples) < 8:
                    samples.append((r['id'], title[:48], r.get('opus'), r.get('no')))

        if modified and not dry_run:
            f.write_text('\n'.join(lines) + '\n', encoding='utf-8')

    print('=' * 72)
    print(f'opus/no 提取 · {"DRY-RUN" if dry_run else "已写入"}')
    print('=' * 72)
    print(f"opus 新增: {stats['opus']:,d} · no 新增: {stats['no']:,d}")
    print()
    print('opus 按来源:')
    for sid, n in per_src.most_common():
        print(f'   {sid:16s} {n:>7,d}')
    print()
    print('样例:')
    for sid, t, op, no in samples:
        print(f'   {sid}  "{t}"  → opus={op} no={no}')
    if dry_run:
        print('\n※ dry-run 确认后加 --apply 执行写回')
    return stats


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    args = ap.parse_args()
    run(dry_run=not args.apply)
    return 0


if __name__ == '__main__':
    sys.exit(main())
