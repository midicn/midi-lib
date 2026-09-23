#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A3 补 · 显示名统一：每 slug 取其最高频显示名为规范名（数据驱动，不做人工猜测）

- 排除 traditional / unknown（各源语境不同，且已有 cn_zh）
用法：python tools/unify_composer_display.py [--dry-run]
"""
from __future__ import annotations
import argparse, json, shutil
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACKS = ROOT / 'midi_db' / 'tracks'
BAK = ROOT / 'midi_db' / 'tracks_backup'
SKIP = {'traditional', 'unknown', ''}


def main(dry: bool):
    # ① 统计每 slug 的显示名频次
    cnt = defaultdict(Counter)
    for f in TRACKS.glob('*.jsonl'):
        for line in f.open(encoding='utf-8'):
            r = json.loads(line)
            s = r.get('composer_slug') or ''
            n = r.get('composer_name') or ''
            if s and n:
                cnt[s][n] += 1
    canon = {}
    for s, c in cnt.items():
        if s in SKIP:
            continue
        canon[s] = c.most_common(1)[0][0]
    print(f'规范显示名 {len(canon):,} 个')

    # ② 应用
    changed_total = 0
    for f in sorted(TRACKS.glob('*.jsonl')):
        lines = f.read_text(encoding='utf-8').splitlines()
        new = []
        changed = 0
        for line in lines:
            r = json.loads(line)
            s = r.get('composer_slug') or ''
            want = canon.get(s)
            if want and r.get('composer_name') != want:
                r['composer_name'] = want
                changed += 1
                new.append(json.dumps(r, ensure_ascii=False, separators=(',', ':')))
            else:
                new.append(line)
        if changed and not dry:
            BAK.mkdir(exist_ok=True)
            shutil.copy2(f, BAK / f'pre-display-unify-{f.stem}-20260923.jsonl')
            f.write_text('\n'.join(new) + '\n', encoding='utf-8')
        changed_total += changed
        if changed:
            print(f'  {f.stem}: {changed:,}')
    print(f'显示名统一 {changed_total:,} 处')
    # 样例
    print('样例（slug → 规范显示名）:')
    for s in ['johann-sebastian-bach', 'carl-czerny', 'franz-liszt', 'ludwig-van-beethoven', 'frederic-chopin']:
        if s in canon:
            print(f'  {s:28s} → {canon[s]}')
    if dry:
        print('[dry-run] 未写回')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    main(ap.parse_args().dry_run)
