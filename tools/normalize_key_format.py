#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""key 格式规范化：全库统一为 'C' / 'Dm' / 'C#m' / 'Eb' 形式

（aria 等源存的是原始小写格式 'a'/'dm'/'c#m'，语义：末位 m 为小调）
用法：python tools/normalize_key_format.py [--dry-run]
"""
from __future__ import annotations
import argparse, json, re, shutil
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACKS = ROOT / 'midi_db' / 'tracks'
BAK = ROOT / 'midi_db' / 'tracks_backup'
RE = re.compile(r'^([a-gA-G])([#b♯♭]?)(m|min|minor|maj|major)?$')
ACC = {'♯': '#', '♭': 'b'}


def norm(k: str):
    if not k:
        return None
    m = RE.match(k.strip())
    if not m:
        return None
    letter, acc, mode = m.groups()
    letter = letter.upper()
    acc = ACC.get(acc, acc)
    out = letter + acc
    if mode and mode.lower() in ('m', 'min', 'minor'):
        out += 'm'
    return out


def main(dry: bool):
    stats = Counter()
    bad = Counter()
    for f in sorted(TRACKS.glob('*.jsonl')):
        lines = f.read_text(encoding='utf-8').splitlines()
        new = []
        changed = 0
        for line in lines:
            r = json.loads(line)
            k = r.get('key')
            if not k:
                new.append(line); continue
            n = norm(k)
            if n is None:
                bad[str(k)[:20]] += 1
                new.append(line); continue
            if n != k:
                r['key'] = n
                changed += 1
                stats[f.stem] += 1
                new.append(json.dumps(r, ensure_ascii=False, separators=(',', ':')))
            else:
                new.append(line)
        if changed and not dry:
            BAK.mkdir(exist_ok=True)
            shutil.copy2(f, BAK / f'pre-keyfmt-{f.stem}-20260923.jsonl')
            f.write_text('\n'.join(new) + '\n', encoding='utf-8')
    print('规范化:', dict(stats), '· 合计', sum(stats.values()))
    if bad:
        print('无法解析的值:', bad.most_common(10))
    # 值域确认
    vals = Counter()
    for f in TRACKS.glob('*.jsonl'):
        for line in f.open(encoding='utf-8'):
            r = json.loads(line)
            if r.get('key'):
                vals[r['key']] += 1
    print(f'规范化后值域 {len(vals)} 个:', vals.most_common(12))
    if dry:
        print('[dry-run] 未写回')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    main(ap.parse_args().dry_run)
