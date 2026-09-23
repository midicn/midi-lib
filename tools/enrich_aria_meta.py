#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""aria 上游元数据补采（A0）· 从 sources/ariamidi/metadata.json 补 4 个字段

- difficulty（新字段）：beginner/intermediate/advanced/virtuoso
- form（补空）：etude/sonata/prelude/... （官方曲式词）
- key（补空）：key_signature 标准化（'c'→'C'，'dm'→'Dm'，'c#m'→'C#m'）
- no（补空）：piece_number
用法：python tools/enrich_aria_meta.py [--dry-run]
"""
from __future__ import annotations
import argparse, json, re, shutil
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
META = ROOT / 'sources' / 'ariamidi' / 'metadata.json'
OUT = ROOT / 'midi_db' / 'tracks' / 'aria.jsonl'
BAK = ROOT / 'midi_db' / 'tracks_backup'

KEY_RE = re.compile(r'^([a-g])([#b]?)(m?)$')


def norm_key(k: str):
    """'c'→'C' 'dm'→'Dm' 'c#m'→'C#m' 'eb'→'Eb' 'bb'→'Bb'"""
    m = KEY_RE.match((k or '').strip().lower())
    if not m:
        return None
    letter, acc, mi = m.groups()
    return letter.upper() + acc + mi


def main(dry: bool):
    meta = json.loads(META.read_text(encoding='utf-8'))
    lines = OUT.read_text(encoding='utf-8').splitlines()
    stats = Counter()
    new_lines = []
    for line in lines:
        r = json.loads(line)
        num = r['id'].split('-')[1].lstrip('0')
        key = str(int(num)) if num else '0'
        md = (meta.get(key) or {}).get('metadata') or {}
        changed = False
        if md.get('difficulty') and not r.get('difficulty'):
            r['difficulty'] = md['difficulty']
            stats['difficulty'] += 1
            changed = True
        if md.get('form') and not r.get('form'):
            r['form'] = md['form']
            stats['form'] += 1
            changed = True
        if md.get('key_signature') and not r.get('key'):
            k = norm_key(md['key_signature'])
            if k:
                r['key'] = k
                stats['key'] += 1
                changed = True
        if md.get('piece_number') and not r.get('no'):
            r['no'] = str(md['piece_number'])
            stats['no'] += 1
            changed = True
        new_lines.append(json.dumps(r, ensure_ascii=False, separators=(',', ':')) if changed else line)

    print('补采统计:', dict(stats))
    # 新覆盖预览
    rows = [json.loads(l) for l in new_lines]
    n = len(rows)
    for f in ['difficulty', 'form', 'key', 'no']:
        have = sum(1 for r in rows if r.get(f))
        print(f'  {f:12s} {have:>7,}  {have/n*100:5.1f}%')
    if dry:
        print('[dry-run] 未写回')
        return
    BAK.mkdir(exist_ok=True)
    shutil.copy2(OUT, BAK / 'pre-aria-meta-20260923.jsonl')
    OUT.write_text('\n'.join(new_lines) + '\n', encoding='utf-8')
    print(f'✓ 已写入 {OUT.relative_to(ROOT)}（备份 pre-aria-meta-20260923.jsonl）')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    main(ap.parse_args().dry_run)
