#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""key 调性提取：从 MIDI 文件的 key_signature meta 事件读取（纯本地 · 确定性元数据）

- 只处理 key 为空的行；文件里没有 key_signature 事件则保持留空（不猜）
- 输出格式对齐现有值域：大调小写音名（'c' / 'eb' / 'f#'），小调加 m（'am' / 'ebm'）
- 多个 key_signature 事件取第一个；读取失败/文件缺失跳过
- mido 运行于隔离 venv：C:/Users/chenhua/.workbuddy/binaries/python/envs/default
"""
from __future__ import annotations
import argparse, json, sys
from collections import Counter
from pathlib import Path

import mido

ROOT = Path(__file__).resolve().parents[1]
TRACKS = ROOT / 'midi_db' / 'tracks'

MAJOR = {0: 'c', 1: 'g', 2: 'd', 3: 'a', 4: 'e', 5: 'b', 6: 'f#', 7: 'c#',
         -1: 'f', -2: 'bb', -3: 'eb', -4: 'ab', -5: 'db', -6: 'gb', -7: 'cb'}
MINOR = {0: 'am', 1: 'em', 2: 'bm', 3: 'f#m', 4: 'c#m', 5: 'g#m', 6: 'd#m', 7: 'a#m',
         -1: 'dm', -2: 'gm', -3: 'cm', -4: 'fm', -5: 'bbm', -6: 'ebm', -7: 'abm'}


def key_from_midi(path: Path) -> str | None:
    """读 MIDI 文件的第一个 key_signature → 值域格式；无则 None"""
    try:
        mf = mido.MidiFile(str(path))
        for track in mf.tracks:
            for msg in track:
                if msg.type == 'key_signature':
                    sf = msg.key[0]      # sharps/flaps: -7..7（signed char）
                    mi = msg.key[1]      # 0 major / 1 minor
                    if sf > 7:
                        sf -= 256        # unsigned char 修正
                    return MINOR[sf] if mi else MAJOR[sf]
    except Exception:
        return None
    return None


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
            if r.get('key'):
                continue
            # 定位 midi 文件（优先规范化路径 data/midi/...，fallback src_path）
            mid = r.get('midi')
            rel = mid.get('file') if isinstance(mid, dict) else mid
            cand = rel or r.get('src_path')
            if not cand:
                continue
            p = ROOT / cand
            if not p.exists():
                p = ROOT / r.get('src_path', '')
                if not p.exists():
                    stats['file_missing'] += 1
                    continue
            k = key_from_midi(p)
            if k:
                r['key'] = k
                stats['key'] += 1
                per_src[r.get('source', '?')] += 1
                lines[i] = json.dumps(r, ensure_ascii=False, separators=(',', ':'))
                modified = True
                if len(samples) < 8:
                    samples.append((r['id'], str(cand)[-32:], k))
            else:
                stats['no_sig'] += 1

        if modified and not dry_run:
            f.write_text('\n'.join(lines) + '\n', encoding='utf-8')
            print(f'  [saved] {f.name}', flush=True)

    print('=' * 72)
    print(f'key 提取 · {"DRY-RUN" if dry_run else "已写入"}')
    print('=' * 72)
    print(f"key 新增: {stats['key']:,d} · 文件无 key_signature: {stats['no_sig']:,d} · 文件缺失: {stats['file_missing']:,d}")
    print()
    print('按来源:')
    for sid, n in per_src.most_common():
        print(f'   {sid:16s} {n:>7,d}')
    print()
    print('样例:')
    for sid, p, k in samples:
        print(f'   {sid}  …{p}  → {k}')
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
