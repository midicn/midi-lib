#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A2 · period 现代源统一 + 作曲家频次统计（A3 准备）

- groove/emopia/oga/maestro/atepp/pdmx 等现代源 → period=contemporary（仅空白者）
- 输出 composer 频次 top（供中文名映射）
用法：python tools/enrich_period_modern.py [--dry-run]
"""
from __future__ import annotations
import argparse, json, shutil
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACKS = ROOT / 'midi_db' / 'tracks'
BAK = ROOT / 'midi_db' / 'tracks_backup'

MODERN_SOURCES = {'groove', 'emopia', 'oga', 'maestro', 'atepp'}


def main(dry: bool):
    stats = Counter()
    comp_freq = Counter()
    for f in sorted(TRACKS.glob('*.jsonl')):
        sid = f.stem
        lines = f.read_text(encoding='utf-8').splitlines()
        new = []
        changed = 0
        for line in lines:
            r = json.loads(line)
            comp_freq[(sid, r.get('composer_slug') or '', r.get('composer_name') or '')] += 1
            if not r.get('period') and sid in MODERN_SOURCES:
                r['period'] = 'contemporary'
                changed += 1
                new.append(json.dumps(r, ensure_ascii=False, separators=(',', ':')))
            else:
                new.append(line)
        if changed:
            stats[sid] = changed
            if not dry:
                BAK.mkdir(exist_ok=True)
                shutil.copy2(f, BAK / f'pre-period-{sid}-20260923.jsonl')
                f.write_text('\n'.join(new) + '\n', encoding='utf-8')
    print('period 现代源统一:', dict(stats), '· 合计', sum(stats.values()))

    # composer 频次（跨源合并）
    agg = Counter()
    names = {}
    for (sid, slug, name), n in comp_freq.items():
        agg[slug] += n
        if slug not in names or len(name) > len(names[slug]):
            names[slug] = name
    print()
    print('作曲家 top60（slug · 频次 · 显示名）:')
    for slug, n in agg.most_common(60):
        print(f'  {slug:26s} {n:>7,}  {names[slug][:34]}')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    main(ap.parse_args().dry_run)
