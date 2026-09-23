#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A0 收尾：maestro 录音年 + abcmisc 的 O: 字段

maestro：官方 CSV（canonical_composer/title/year/duration）→ yr（录音年，语义标注）
abcmisc：ABC 头部 O:（演奏者/来源）→ extra.performer_or_source
用法：python tools/enrich_maestro_abcmisc.py [--dry-run]
"""
from __future__ import annotations
import argparse, csv, io, json, re, shutil
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACKS = ROOT / 'midi_db' / 'tracks'
BAK = ROOT / 'midi_db' / 'tracks_backup'


def do_maestro(dry: bool):
    csvp = ROOT / 'sources' / 'maestro' / 'maestro-v3.0.0' / 'maestro-v3.0.0.csv'
    if not csvp.exists():
        print('maestro CSV 缺失'); return
    idx = {}
    f = csvp.open(encoding='utf-8', errors='replace')
    for row in csv.DictReader(f):
        idx[row['midi_filename'].strip()] = row
    print(f'maestro CSV {len(idx):,}')
    p = TRACKS / 'maestro.jsonl'
    rows = [json.loads(l) for l in p.open(encoding='utf-8')]
    stats = Counter()
    for r in rows:
        sp = (r.get('src_path') or '').replace('\\', '/')
        base = sp.split('/')[-1]
        # CSV 的 midi_filename 形如 2018/MIDI-Unprocessed_...midi
        hit = None
        for k, v in idx.items():
            if k.split('/')[-1] == base:
                hit = v; break
        if not hit:
            stats['未匹配'] += 1; continue
        if hit.get('year') and not r.get('yr'):
            try:
                r['yr'] = int(hit['year']); stats['yr 补'] += 1
            except Exception:
                stats['year 异常'] += 1
        r.setdefault('extra', {})['canonical_composer'] = hit.get('canonical_composer')
        r['extra']['canonical_title'] = hit.get('canonical_title')
        r['extra']['yr_semantics'] = 'recording-year'
    print('maestro 统计:', dict(stats), '· yr 覆盖', sum(1 for r in rows if r.get('yr')), '/', len(rows))
    if not dry:
        BAK.mkdir(exist_ok=True)
        shutil.copy2(p, BAK / 'pre-maestro-year-20260923.jsonl')
        with p.open('w', encoding='utf-8', newline='\n') as f2:
            for r in rows:
                f2.write(json.dumps(r, ensure_ascii=False, separators=(',', ':')) + '\n')
        print('✓ maestro.jsonl 已写入')


def do_abcmisc(dry: bool):
    src = ROOT / 'sources' / 'abc-misc'
    # ABC 文件 → {标题: {O, Z}}（按标题匹配）
    index = {}
    for f in sorted(src.glob('*.abc')):
        t = f.read_text(encoding='utf-8', errors='replace')
        tunes = re.split(r'(?=^X:\s*\d+)', t, flags=re.M)[1:]
        per = {}
        for tn in tunes:
            mt = re.search(r'^T:\s*(.+)', tn, re.M)
            mo = re.search(r'^O:\s*(.+)', tn, re.M)
            mz = re.search(r'^Z:\s*(.+)', tn, re.M)
            if mt:
                per[mt.group(1).strip().lower()] = {
                    'O': mo.group(1).strip() if mo else None,
                    'Z': mz.group(1).strip() if mz else None}
        index[f.stem.upper()] = per
    print(f'abcmisc ABC {len(index)} 文件 · {sum(len(v) for v in index.values()):,} 曲')
    p = TRACKS / 'abcmisc.jsonl'
    rows = [json.loads(l) for l in p.open(encoding='utf-8')]
    stats = Counter()
    for r in rows:
        title = (r.get('title') or '').strip().lower()
        if not title:
            stats['无标题'] += 1; continue
        hit = None
        for code, per in index.items():
            if title in per:
                hit = per[title]; break
        if not hit:
            stats['未匹配'] += 1; continue
        stats['匹配'] += 1
        if hit.get('O'):
            r.setdefault('extra', {})['performer_or_source'] = hit['O']
            stats['O 补'] += 1
        if hit.get('Z'):
            r['extra']['transcriber'] = hit['Z']
    print('abcmisc 统计:', dict(stats))
    print('样例 extra:', [r.get('extra') for r in rows[:2] if (r.get('extra') or {}).get('performer_or_source')][:2])
    if not dry:
        BAK.mkdir(exist_ok=True)
        shutil.copy2(p, BAK / 'pre-abcmisc-o-20260923.jsonl')
        with p.open('w', encoding='utf-8', newline='\n') as f2:
            for r in rows:
                f2.write(json.dumps(r, ensure_ascii=False, separators=(',', ':')) + '\n')
        print('✓ abcmisc.jsonl 已写入')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()
    do_maestro(a.dry_run)
    print()
    do_abcmisc(a.dry_run)
