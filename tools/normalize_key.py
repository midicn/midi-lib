#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""key 值域全库归一：统一为 aria 格式（小写音名 + 可选 #/b + 小调 m）

规则（音乐学标准：非大小调调式归入最近的大小调）：
  major/maj/ionian/lydian/mixolydian → 大调（纯音名）
  minor/min/dorian/aeolian/phrygian → 小调（m 后缀）
  纯大写音名（'D'/'F'）→ 大调；'Dm' → 小调
  ABC 装饰（'Dm =b'/'Am ^f'/'clef=treble'/'octave=1'）剥除；'none'/'Hp'/'b#' 等无法解析 → 清空
"""
from __future__ import annotations
import json, re, sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACKS = ROOT / 'midi_db' / 'tracks'

SPECIAL = {'Es': 'eb', 'es': 'eb', 'As': 'ab', 'as': 'ab'}
RE_KEY = re.compile(r'^([A-Ga-g])([#b]{0,2})\s*(m|maj|min|major|minor|mix|mixolydian|dor|dorian|phr|phrygian|lyd|lydian|ion|ionian|aeo|aeolian)?\b(.*)$', re.I)
MINOR_MODES = ('m', 'min', 'minor', 'dor', 'dorian', 'aeo', 'aeolian', 'phr', 'phrygian')
MAJOR_MODES = ('maj', 'major', 'mix', 'mixolydian', 'lyd', 'lydian', 'ion', 'ionian')


def norm_key(k: str) -> str | None:
    k = k.strip()
    if not k or k.lower() in ('none', 'unknown'):
        return None
    if k in SPECIAL:
        return SPECIAL[k]
    m = RE_KEY.match(k)
    if not m:
        return None
    letter = m.group(1).lower()
    acc = m.group(2) or ''
    mode = (m.group(3) or '').lower()
    tail = (m.group(4) or '').strip()
    # 尾部必须像装饰（=/^/%/空格/字母数字混合的 ABC 标记），若是明显其他内容则拒
    if tail and not re.match(r'^[\s=%^_+#a-zA-Z0-9.\-]*$', tail):
        return None
    if mode in MINOR_MODES:
        return letter + acc + 'm'
    if mode in MAJOR_MODES or mode == '':
        return letter + acc
    return None


def run(dry_run: bool):
    stats = Counter()
    mapping = {}
    for f in sorted(TRACKS.glob('*.jsonl')):
        lines = f.read_text(encoding='utf-8').splitlines()
        modified = False
        for i, line in enumerate(lines):
            r = json.loads(line)
            k = r.get('key')
            if not k:
                continue
            nk = norm_key(k)
            mapping[k] = nk
            if nk != k:
                r['key'] = nk
                lines[i] = json.dumps(r, ensure_ascii=False, separators=(',', ':'))
                modified = True
                stats['norm'] += 1
                if nk is None:
                    stats['cleared'] += 1
        if modified and not dry_run:
            f.write_text('\n'.join(lines) + '\n', encoding='utf-8')
            print(f'  [saved] {f.name}', flush=True)

    print('=' * 72)
    print(f'key 归一 · {"DRY-RUN" if dry_run else "已写入"}')
    print('=' * 72)
    print(f"变换 {stats['norm']:,} 行（其中清空无法解析 {stats['cleared']:,}）")
    print()
    print('映射表（原值 → 新值 · 次数）——只列有变化的:')
    vc = Counter()
    for f in sorted(TRACKS.glob('*.jsonl')):
        for line in f.open(encoding='utf-8'):
            k = json.loads(line).get('key')
            if k: vc[k] += 1
    changes = [(k, mapping.get(k), n) for k, n in vc.most_common() if mapping.get(k) != k]
    for k, nk, n in changes[:60]:
        print(f'   {k!r:30s} → {nk!r:10s} {n:>6,d}')
    if len(changes) > 60:
        print(f'   …共 {len(changes)} 项变化')
    print()
    # 归一后值域预览
    after = Counter()
    for k, n in vc.items():
        nk = mapping.get(k, k)
        if nk: after[nk] += n
    print(f'归一后值域（{len(after)} 个）: {after.most_common()}')


if __name__ == '__main__':
    run(dry_run='--apply' not in sys.argv)
