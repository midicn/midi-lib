#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ATEPP 接入器（源 id = atepp）· 演奏版维度（version_type=performance）

输入：
  sources/atepp/data/<Composer>/<Work>/<Movement>/<NNNNN>.mid   （HF 镜像 anusfoil/atepp-midi）
  sources/atepp/ATEPP-metadata-1.2.csv   作品/质量/专辑/录音年（官方）
  sources/atepp/splits.csv               演奏者（label）+ split（镜像）

许可：CC BY 4.0（据 PianoCoRe/TISMIR 论文对照表）+ 官方 disclaimer 无使用限制 → 归 C1
执行日期核验：2026-09-22

输出：midi_db/tracks/atepp.jsonl
用法：python tools/ingest_atepp.py [--dry-run]
"""
from __future__ import annotations
import argparse, csv, hashlib, json, re, sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'sources' / 'atepp'
DATA = SRC / 'data'
META = SRC / 'ATEPP-metadata-1.2.csv'
SPLITS = SRC / 'splits.csv'
OUT = ROOT / 'midi_db' / 'tracks' / 'atepp.jsonl'

SOURCE_ID = 'atepp'
LICENSE = 'CC-BY-4.0'
ZONE = 'piano-special'          # 与 aria 同为钢琴演奏区

# 质量过滤：官方建议排除低质/噪声/损坏/掌声
BAD_QUALITY = {'low quality', 'background noise', 'corrupted', 'applause'}

PERIOD_MAP = {
    'johann sebastian bach': 'baroque', 'george frideric handel': 'baroque',
    'domenico scarlatti': 'baroque', 'franz joseph haydn': 'classical',
    'wolfgang amadeus mozart': 'classical', 'ludwig van beethoven': 'classical',
    'franz schubert': 'romantic', 'robert schumann': 'romantic', 'frederic chopin': 'romantic',
    'franz liszt': 'romantic', 'johannes brahms': 'romantic', 'felix mendelssohn': 'romantic',
    'pyotr ilyich tchaikovsky': 'romantic', 'cesar franck': 'romantic',
    'edvard grieg': 'romantic', 'modest mussorgsky': 'romantic',
    'sergei rachmaninoff': 'romantic', 'alexander scriabin': 'romantic',
    'claude debussy': 'impressionist', 'maurice ravel': 'impressionist',
    'sergei prokofiev': 'modern', 'dmitri shostakovich': 'modern', 'bela bartok': 'modern',
    'anton webern': 'modern', 'paul hindemith': 'modern',
}


def sanitize(rel: str) -> str:
    """Windows 非法字符消毒（与下载脚本一致）"""
    parts = [re.sub(r'[:*?"<>|]', '_', seg) for seg in rel.split('/')]
    return '/'.join(parts)


def slugify(s: str) -> str:
    s = re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')
    return s or 'unknown'


def midi_stats(p: Path):
    """极简 MIDI 解析：时长（秒）+ 音符数 + 首 tempo + 拍号"""
    data = p.read_bytes()
    if data[:4] != b'MThd':
        return None
    div = int.from_bytes(data[12:14], 'big') or 480   # MThd: format(8-9) ntrks(10-11) division(12-13)
    i = 8 + int.from_bytes(data[4:8], 'big')
    total_ticks = 0
    notes = 0
    tempo = None
    timesig = None
    while i < len(data) - 8:
        if data[i:i+4] != b'MTrk':
            break
        ln = int.from_bytes(data[i+4:i+8], 'big')
        j = i + 8
        end = j + ln
        running = None
        cur = 0
        while j < end:
            # delta
            d = 0
            for _ in range(4):
                b0 = data[j]; j += 1
                d = (d << 7) | (b0 & 0x7F)
                if not (b0 & 0x80):
                    break
            cur += d
            if j >= end:
                break
            st = data[j]
            if st & 0x80:
                j += 1
                running = st
            else:
                st = running
            if st == 0xFF:
                mt = data[j]; j += 1
                l2 = 0
                while True:
                    b0 = data[j]; j += 1
                    l2 = (l2 << 7) | (b0 & 0x7F)
                    if not (b0 & 0x80):
                        break
                if mt == 0x51 and l2 >= 3:
                    us = int.from_bytes(data[j:j+3], 'big')
                    if us:
                        tempo = round(60_000_000 / us)
                elif mt == 0x58 and l2 >= 2:
                    timesig = f'{data[j]}/{2 ** data[j+1]}'
                j += l2
            elif st in (0xF0, 0xF7):
                l2 = 0
                while True:
                    b0 = data[j]; j += 1
                    l2 = (l2 << 7) | (b0 & 0x7F)
                    if not (b0 & 0x80):
                        break
                j += l2
            else:
                hi = st & 0xF0
                if hi in (0x80, 0x90, 0xA0, 0xB0, 0xE0):
                    if hi == 0x90 and data[j+1] > 0:
                        notes += 1
                    j += 2
                elif hi in (0xC0, 0xD0):
                    j += 1
                else:
                    break
        total_ticks = max(total_ticks, cur)
        i = end
    sec = total_ticks / div * (60 / (tempo or 120)) if div else 0
    return {'duration_sec': round(sec, 1), 'note_count': notes, 'bpm': tempo, 'timesig': timesig}


def main(dry: bool):
    # metadata：midi_path(相对 data 的路径) → 元数据
    meta = {}
    if META.exists():
        for r in csv.DictReader(META.open(encoding='utf-8')):
            meta[sanitize(r['midi_path'].strip())] = r
    splits = {}
    if SPLITS.exists():
        for r in csv.DictReader(SPLITS.open(encoding='utf-8')):
            p = r['midi_path'].strip().strip('"')
            splits[sanitize(p)] = r['label'].strip()

    rows = []
    skipped_q = 0
    n = 0
    for f in sorted(DATA.rglob('*.mid')):
        rel = f.relative_to(DATA).as_posix()
        m = meta.get(rel)
        if not m:
            continue
        q = (m.get('quality') or '').strip()
        if q in BAD_QUALITY:
            skipped_q += 1
            continue
        composer = (m.get('composer') or '').strip() or 'Unknown'
        track = (m.get('track') or '').strip()
        artist = splits.get(rel) or (m.get('artist') or '').strip()
        album = (m.get('album') or '').strip()
        try:
            yr = int(re.match(r'(\d{4})', m.get('album_date') or '').group(1))
        except Exception:
            yr = None
        st = midi_stats(f)
        if not st or st['note_count'] <= 0:
            continue
        fp = hashlib.md5(f.read_bytes()).hexdigest()
        n += 1
        rows.append({
            'id': f'{SOURCE_ID}-{n:06d}',
            'source': SOURCE_ID,
            'src_path': f'sources/atepp/data/{rel}',
            'title': track or None,
            'composer_slug': slugify(composer),
            'composer_name': composer,
            'genre': 'classical',
            'instrument': 'piano',
            'period': PERIOD_MAP.get(composer.lower()),
            'region': None,
            'opus': None,
            'no': None,
            'form': None,
            'key': None,
            'yr': yr,
            'license': LICENSE,
            'zone': ZONE,
            'midi': {'file': None, 'duration_sec': st['duration_sec'], 'note_count': st['note_count'],
                     'tracks_count': None, 'bpm': st['bpm']},
            'fingerprint': fp,
            'version_type': 'performance',        # 多版本架构：演奏版
            'performer': artist or None,
            'album': album or None,
            'extra': {'source': 'ATEPP (ISMIR 2022)', 'quality': q or None,
                      'timesig': st['timesig'], 'license_basis': 'CC BY 4.0（TISMIR 论文对照表）',
                      'mirror': 'huggingface.co/datasets/anusfoil/atepp-midi'},
        })

    print(f'ATEPP 元数据 {len(meta):,} · splits {len(splits):,}')
    print(f'data 下 MIDI {len(rows) + skipped_q:,}（质量过滤排除 {skipped_q}）→ 入库 {len(rows):,}')
    print('演奏者 top5:', Counter(r['performer'] for r in rows).most_common(5))
    print('作曲家 top5:', Counter(r['composer_name'] for r in rows).most_common(5))
    if dry:
        print('[dry-run] 未写回')
        return
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open('w', encoding='utf-8', newline='\n') as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False, separators=(',', ':')) + '\n')
    print(f'✓ 已写入 {OUT.relative_to(ROOT)}')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    main(ap.parse_args().dry_run)
