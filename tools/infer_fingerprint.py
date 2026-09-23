#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fingerprint 统一重算：对**发布文件（midi.file）**内容算 MD5（v1.22 语义定稿）

v1.21 及之前的 fingerprint 混用两种语义（cyberhymnal/giantmidi=源文件、其余=src_path 指向的数据包如
tunes.csv 导致 thesession 全库同指纹）——本脚本统一为 midi.file（用户实际下载的文件）MD5。
全库覆盖重算（不跳过已有值）。用法：python tools/infer_fingerprint.py --apply --force
"""
from __future__ import annotations
import argparse, hashlib, json, sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACKS = ROOT / 'midi_db' / 'tracks'


def md5_of(p: Path) -> str | None:
    try:
        h = hashlib.md5()
        with p.open('rb') as f:
            for chunk in iter(lambda: f.read(1 << 20), b''):
                h.update(chunk)
        return h.hexdigest()
    except Exception:
        return None


def run(dry_run: bool, force: bool):
    stats = Counter()
    per_src = Counter()
    for f in sorted(TRACKS.glob('*.jsonl')):
        lines = f.read_text(encoding='utf-8').splitlines()
        modified = False
        for i, line in enumerate(lines):
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            if not force and r.get('fingerprint'):
                continue
            # 语义定稿：发布文件 midi.file（去重的真正对象）
            mid = r.get('midi') or {}
            cand = mid.get('file') or r.get('src_path')
            if not cand:
                stats['no_path'] += 1
                continue
            p = ROOT / cand
            if not p.exists():
                stats['file_missing'] += 1
                continue
            md5 = md5_of(p)
            if md5:
                if r.get('fingerprint') != md5:
                    stats['ok'] += 1
                    per_src[r.get('source', '?')] += 1
                r['fingerprint'] = md5
                lines[i] = json.dumps(r, ensure_ascii=False, separators=(',', ':'))
                modified = True
            else:
                stats['read_fail'] += 1
        if modified and not dry_run:
            f.write_text('\n'.join(lines) + '\n', encoding='utf-8')
            print(f'  [saved] {f.name}', flush=True)

    print('=' * 72)
    print(f'fingerprint 重算（语义=发布文件 MD5）· {"DRY-RUN" if dry_run else "已写入"}')
    print('=' * 72)
    print(f"更新 {stats['ok']:,} · 文件缺失 {stats['file_missing']:,} · 无路径 {stats['no_path']:,} · 读取失败 {stats['read_fail']:,}")
    for sid, n in per_src.most_common():
        print(f'   {sid:16s} {n:>7,d}')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    ap.add_argument('--force', action='store_true', help='覆盖已有值（语义统一重算）')
    a = ap.parse_args()
    run(dry_run=not a.apply, force=a.force)
