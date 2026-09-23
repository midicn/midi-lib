#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PDMX 接入器（源 id = pdmx）· 乐谱型维度（version_type=score）

筛选链（法律安全优先）：
  ① subset:rated_deduplicated（官方最优子集）
  ② subset:no_license_conflict（排除 12.29% 许可冲突）
  ③ composer_name 有效（非 NA/anon/trad）
  ④ genres 有值
  ⑤ 非草稿
  ⑥ **genre 白名单**：只收传统/古典类（classical/folk/worldmusic/religiousmusic）
     —— 现代类（soundtrack/rock/pop/jazz/electronic）一律排除（自标 CC0 但为现代版权作品的不可信样本）

输入：sources/pdmx/PDMX-v2.csv · sources/pdmx/selected/*.mid（已按 hash 解压）
输出：midi_db/tracks/pdmx.jsonl
用法：python tools/ingest_pdmx.py [--dry-run]
"""
from __future__ import annotations
import argparse, csv, hashlib, io, json, re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'sources' / 'pdmx'
CSV = SRC / 'PDMX-v2.csv'
SELECTED = SRC / 'selected'
OUT = ROOT / 'midi_db' / 'tracks' / 'pdmx.jsonl'

SOURCE_ID = 'pdmx'
LICENSE_DEFAULT = 'CC0-1.0'
ZONE = 'main'

GENRE_WHITELIST = {'classical', 'folk', 'worldmusic', 'religiousmusic'}

# 知名作品 → 正确作曲家（上游把编配者填进了 composer 字段时的修正，只处理可 100% 确定的）
TITLE_COMPOSER_FIX = {
    'nutcracker': 'Pyotr Ilyich Tchaikovsky',
    'swan lake': 'Pyotr Ilyich Tchaikovsky',
    'sleeping beauty': 'Pyotr Ilyich Tchaikovsky',
    'eugene onegin': 'Pyotr Ilyich Tchaikovsky',
    'the seasons': 'Pyotr Ilyich Tchaikovsky',
}
NA = {'', 'na', 'n/a', 'none', 'null', 'anon.', 'trad.', 'trad', 'traditional', 'tradicional', 'unknown'}

PERIOD_MAP = {
    'bach': 'baroque', 'handel': 'baroque', 'scarlatti': 'baroque', 'vivaldi': 'baroque', 'purcell': 'baroque',
    'mozart': 'classical', 'haydn': 'classical', 'beethoven': 'classical',
    'schubert': 'romantic', 'schumann': 'romantic', 'chopin': 'romantic', 'liszt': 'romantic',
    'brahms': 'romantic', 'mendelssohn': 'romantic', 'tchaikovsky': 'romantic', 'wagner': 'romantic',
    'debussy': 'impressionist', 'ravel': 'impressionist', 'satie': 'impressionist',
    'bartok': 'modern', 'prokofiev': 'modern', 'shostakovich': 'modern',
}


def sanitize(rel: str) -> str:
    return '/'.join(re.sub(r'[:*?"<>|]', '_', seg) for seg in rel.split('/'))


def clean_composer(name: str) -> str | None:
    """作曲家名清洗：截断明显脏值（如 'Béla BartókRevised and Arrangedby...'）"""
    n = name.strip()
    if n.lower() in NA:
        return None
    # 去掉 'Revised...'/'Arranged...'/'Composed...' 之后的尾巴
    n = re.split(r'(?<=[a-zà-ÿ])(?=[A-Z][a-z]+ed\b)|(?=[A-Z][a-z]+by\b)|Revised|Arranged|Arrangedby|Composed by', n)[0].strip()
    n = re.sub(r'\s+', ' ', n).strip(' .,;:')
    if len(n) < 3 or len(n) > 60:
        return None
    return n


def slugify(s: str) -> str:
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-') or 'unknown'


def midi_meta(p: Path):
    """提取：时长（秒）+ 音符数 + 调号 + 拍号 + 速度（MIDI 内自带，PDMX 渲染保留）"""
    data = p.read_bytes()
    if data[:4] != b'MThd':
        return None
    div = int.from_bytes(data[12:14], 'big') or 480
    i = 8 + int.from_bytes(data[4:8], 'big')
    total_ticks = 0
    notes = 0
    tempo = None
    timesig = None
    key = None
    while i < len(data) - 8:
        if data[i:i+4] != b'MTrk':
            break
        ln = int.from_bytes(data[i+4:i+8], 'big')
        j = i + 8
        end = j + ln
        running = None
        cur = 0
        while j < end:
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
                    if us and tempo is None:
                        tempo = round(60_000_000 / us)
                elif mt == 0x58 and l2 >= 2 and timesig is None:
                    timesig = f'{data[j]}/{2 ** data[j+1]}'
                elif mt == 0x59 and l2 >= 2 and key is None:
                    sf, mi = data[j], data[j+1]
                    names = ['C', 'G', 'D', 'A', 'E', 'B', 'F#', 'C#', 'F', 'Bb', 'Eb', 'Ab', 'Db', 'Gb', 'Cb']
                    if -7 <= sf <= 7:
                        n = names[sf + 7]
                        key = (n + 'm') if mi == 1 else n
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
    sec = total_ticks * 60 / (div * (tempo or 120))
    return {'duration_sec': round(sec, 1), 'note_count': notes, 'bpm': tempo,
            'timesig': timesig, 'key': key}


def main(dry: bool):
    rows_csv = {}
    f = CSV.open(encoding='utf-8', errors='replace')
    cols = next(csv.reader(io.StringIO(f.readline())))
    idx = {c: i for i, c in enumerate(cols)}
    for line in f:
        row = next(csv.reader(io.StringIO(line)))
        if len(row) < len(cols):
            continue
        h = Path(row[idx['path']].strip()).stem
        rows_csv[h] = row
    print(f'CSV {len(rows_csv):,} 行')

    rows = []
    skipped = Counter()
    for fp in sorted(SELECTED.glob('*.mid')):
        h = fp.stem
        row = rows_csv.get(h)
        if not row:
            skipped['无CSV行'] += 1
            continue
        def g(k):
            return row[idx[k]].strip()
        # 筛选链
        if g('subset:rated_deduplicated').lower() != 'true':
            skipped['非最优子集'] += 1; continue
        if g('subset:no_license_conflict').lower() != 'true' or g('license_conflict').lower() == 'true':
            skipped['许可冲突'] += 1; continue
        if g('is_draft').lower() == 'true':
            skipped['草稿'] += 1; continue
        gl = {x.strip().lower() for x in g('genres').split('|') if x.strip()}
        if not (gl & GENRE_WHITELIST):
            skipped['现代类genre'] += 1; continue
        composer = clean_composer(g('composer_name'))
        if not composer:
            skipped['无作曲家'] += 1; continue
        title = g('song_name') or g('title') or g('subtitle') or None
        # 上游把编配者填进作曲家字段时的修正（知名作品可 100% 确定）
        combo = ((title or '') + ' ' + g('title')).lower()
        fixed = next((v for k, v in TITLE_COMPOSER_FIX.items() if k in combo and g('composer_name').strip() not in combo), None)
        suspect = False
        if fixed and fixed.lower().split()[-1] not in composer.lower():
            composer = fixed
            suspect = True
        st = midi_meta(fp)
        if not st or st['note_count'] <= 0:
            skipped['无效MIDI'] += 1; continue
        low = composer.lower()
        period = next((v for k, v in PERIOD_MAP.items() if k in low), None)
        rows.append({
            'id': f'{SOURCE_ID}-{len(rows)+1:06d}',
            'source': SOURCE_ID,
            'src_path': f'sources/pdmx/selected/{fp.name}',
            'title': title,
            'composer_slug': slugify(composer),
            'composer_name': composer,
            'genre': 'classical' if 'classical' in gl else sorted(gl)[0],
            'instrument': 'piano' if g('tracks').lower().startswith('piano') or g('n_tracks') == '1' else None,
            'period': period,
            'region': None,
            'opus': None, 'no': None, 'form': None,
            'key': st['key'],
            'yr': None,
            'license': 'CC0-1.0' if g('license') == 'cc-zero' else 'PD',
            'zone': ZONE,
            'midi': {'file': None, 'duration_sec': st['duration_sec'], 'note_count': st['note_count'],
                     'tracks_count': int(g('n_tracks') or 0) or None, 'bpm': st['bpm']},
            'fingerprint': hashlib.md5(fp.read_bytes()).hexdigest(),
            'version_type': 'score',
            'extra': {'source': 'PDMX (ICASSP 2025)', 'timesig': st['timesig'],
                      'complexity': g('complexity') or None, 'rating': g('rating') or None,
                      'genres': g('genres'), 'tracks_desc': g('tracks') or None,
                      'has_lyrics': g('has_lyrics') == 'True',
                      'musescore_id': h, 'license_src': g('license'), 'composer_suspect': suspect},
        })

    print(f'可入库 {len(rows):,} · 跳过 {dict(skipped)}')
    print('作曲家 top10:', Counter(r['composer_name'] for r in rows).most_common(10))
    print('genre:', Counter(r['genre'] for r in rows).most_common())
    print('有 key:', sum(1 for r in rows if r['key']), '· 有拍号:', sum(1 for r in rows if r['extra']['timesig']))
    if dry:
        print('[dry-run] 未写回')
        return
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open('w', encoding='utf-8', newline='\n') as f2:
        for r in rows:
            f2.write(json.dumps(r, ensure_ascii=False, separators=(',', ':')) + '\n')
    print(f'✓ 已写入 {OUT.relative_to(ROOT)}')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    main(ap.parse_args().dry_run)
