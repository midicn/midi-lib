#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""china-folk 歌词提取（A0）· MusicXML <lyric> → 独立歌词库

- 输入：sources/china-folk/lyrics-included/**/*.musicxml（10,481）
- 匹配：chinafolk.jsonl 的 src_path（.mid → .musicxml）
- 输出：midi_db/lyrics/chinafolk.jsonl（{id, lyrics}）+ chinafolk.jsonl 加 has_lyrics 标记
- 已知：shaanxi2 目录名自述「some lyric characters are missing」→ 标注 lyrics_incomplete
用法：python tools/extract_chinafolk_lyrics.py [--dry-run]
"""
from __future__ import annotations
import argparse, json, re, shutil
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACKS = ROOT / 'midi_db' / 'tracks' / 'chinafolk.jsonl'
LYRICS_DIR = ROOT / 'midi_db' / 'lyrics'
OUT = LYRICS_DIR / 'chinafolk.jsonl'
BAK = ROOT / 'midi_db' / 'tracks_backup'
RE_TEXT = re.compile(r'<lyric[^>]*>\s*<text>([^<]*)</text>', re.S)
RE_SYL = re.compile(r'<syllabic>([^<]*)</syllabic>')


def extract(xml: Path):
    try:
        t = xml.read_text(encoding='utf-8', errors='strict')
    except UnicodeDecodeError:
        t = xml.read_text(encoding='utf-8', errors='replace')
    parts = [m.group(1).strip() for m in RE_TEXT.finditer(t)]
    parts = [p for p in parts if p]
    if not parts:
        return None
    # 拼接：中文音节直接连；遇到以连字符结尾的西文音节也不加空格
    line = ''.join(parts)
    line = re.sub(r'\s+', ' ', line).strip()
    return line or None


def main(dry: bool):
    rows = [json.loads(l) for l in TRACKS.open(encoding='utf-8')]
    print(f'chinafolk {len(rows):,}')
    stats = Counter()
    out_rows = []
    for r in rows:
        sp = r.get('src_path') or ''
        xml = ROOT / sp.replace('.mid', '.musicxml')
        incomplete = 'some lyric characters are missing' in sp or 'shaanxi2' in sp
        if not xml.exists():
            stats['无文件'] += 1
            continue
        ly = extract(xml)
        if not ly:
            stats['无歌词'] += 1
            continue
        r['has_lyrics'] = True
        if incomplete:
            r['lyrics_incomplete'] = True
        out_rows.append({'id': r['id'], 'lyrics': ly, 'chars': len(ly),
                         'incomplete': incomplete})
        stats['有歌词'] += 1
    print('统计:', dict(stats))
    if out_rows:
        import statistics
        lens = [x['chars'] for x in out_rows]
        print(f'歌词长度: 中位 {statistics.median(lens):.0f} · 最大 {max(lens)}')
        print('样例:')
        for x in out_rows[:3]:
            print(f'   {x["id"]}: {x["lyrics"][:60]}')
    if dry:
        print('[dry-run] 未写回')
        return
    LYRICS_DIR.mkdir(parents=True, exist_ok=True)
    with OUT.open('w', encoding='utf-8', newline='\n') as f:
        for x in out_rows:
            f.write(json.dumps(x, ensure_ascii=False, separators=(',', ':')) + '\n')
    BAK.mkdir(exist_ok=True)
    shutil.copy2(TRACKS, BAK / 'pre-chinafolk-lyrics-20260923.jsonl')
    with TRACKS.open('w', encoding='utf-8', newline='\n') as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False, separators=(',', ':')) + '\n')
    print(f'✓ 歌词库 {OUT.relative_to(ROOT)}（{len(out_rows):,} 首）· chinafolk.jsonl 已加 has_lyrics')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    main(ap.parse_args().dry_run)
