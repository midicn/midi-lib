#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""essen 体裁（R:/FCT）补采（A0）· form 缺口 10,373 的官方答案

- 数据源：sources/essen/esac/*.abc 的 R: 字段（首段 = 体裁，后续 = 题材）
- 匹配：essen.jsonl 的 extra.key_in_dataset（'HAN1#x1' → 文件 HAN1 · X=1）
- form：首段体裁 → 英文小写标准值（与全库 213 个 form 值同风格）；未命中留空（不猜）
- topic：后续题材原文存入 extra.topics（不作中译，避免猜译）
用法：python tools/enrich_essen_form.py [--dry-run]
"""
from __future__ import annotations
import argparse, json, re, shutil
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ABC = ROOT / 'sources' / 'essen' / 'esac'
JSONL = ROOT / 'midi_db' / 'tracks' / 'essen.jsonl'
BAK = ROOT / 'midi_db' / 'tracks_backup'

# 体裁关键词 → 标准 form 值（英文小写，与全库风格一致）
FORM_MAP = [
    ('wiegen', 'lullaby'),
    ('kinder - spiel', "children's game"), ('kinderspiel', "children's game"),
    ('kinder', "children's song"),
    ('liebes - lied', 'love song'), ('liebeslied', 'love song'),
    ('hochzeits', 'wedding song'), ('ehestands', 'wedding song'),
    ('abschieds', 'farewell song'),
    ('wander', 'wandering song'),
    ('studenten', 'student song'),
    ('trink', 'drinking song'), ('zech', 'drinking song'),
    ('soldaten', "soldiers' song"), ('kriegs', "soldiers' song"),
    ('jaeger', 'hunting song'),
    ('helden', 'commemorative song'), ('ehren', 'commemorative song'), ('gedaechtnis', 'commemorative song'),
    ('berufslied', 'work song'), ('handwerker', 'work song'), ('bauern', 'work song'),
    ('politisch', 'patriotic song'), ('vaterlands', 'patriotic song'), ('national', 'patriotic song'),
    ('historische', 'historical song'),
    ('geistlich', 'hymn'), ('religioes', 'hymn'), ('religiöses', 'hymn'), ('wallfahrts', 'hymn'),
    ('sagen', 'narrative song'), ('erzaehlendes', 'narrative song'), ('erzählendes', 'narrative song'),
    ('scherz', 'comic song'), ('schalks', 'comic song'), ('schelmen', 'comic song'),
    ('lyrisches', 'lyric song'),
    ('reigen', 'round dance'),
    ('tanz', 'dance'), ('taneczna', 'dance'),
    ('ballade', 'ballade'),
    ('romanze', 'romance'),
    ('lied', 'song'),
    ('xiaodiao', 'xiaodiao'),
    ('shange', 'shange'),
    ('haozi', 'haozi'),
    ('dumy', 'dumy'),
    ('variation', 'variations'),
    ('sonate', 'sonata'),
]


def clean_first(r: str):
    """取 R: 首段（按 , ; 分割），去尾巴符号"""
    first = re.split(r'[;,]', r)[0]
    return first.replace(']', '').replace('"', '').strip().lower()


def main(dry: bool):
    # ① 解析 ABC：文件代号 → {X 序号: (R 原文)}
    index = {}
    for f in sorted(ABC.glob('*.abc')):
        code = f.stem.upper()
        t = f.read_text(encoding='utf-8', errors='replace')
        tunes = re.split(r'(?=^X:\s*\d+)', t, flags=re.M)[1:]
        per = {}
        for tn in tunes:
            mx = re.search(r'^X:\s*(\d+)', tn, re.M)
            mr = re.search(r'^R:\s*(.+)', tn, re.M)
            if mx:
                per[int(mx.group(1))] = (mr.group(1).strip() if mr else '')
        index[code] = per
    print(f'ABC 文件 {len(index)} · 曲目 {sum(len(v) for v in index.values()):,}')

    # ② 逐曲匹配
    rows = [json.loads(l) for l in JSONL.open(encoding='utf-8')]
    stats = Counter()
    topic_cnt = 0
    for r in rows:
        ex = r.get('extra') or {}
        kid = str(ex.get('key_in_dataset') or '')
        m = re.match(r'^([A-Za-z0-9]+)#x(\d+)$', kid)
        if not m:
            stats['无key_in_dataset'] += 1
            continue
        code, x = m.group(1).upper(), int(m.group(2))
        raw = (index.get(code) or {}).get(x)
        if raw is None:
            stats['ABC未命中'] += 1
            continue
        first = clean_first(raw)
        form = None
        for kw, val in FORM_MAP:
            if kw in first:
                form = val
                break
        if form and not r.get('form'):
            r['form'] = form
            stats['form 已补'] += 1
        elif not form:
            stats['体裁未识别'] += 1
        # 题材（首段之后的原文）
        rest = [p.strip() for p in re.split(r'[;,]', raw)[1:] if p.strip()]
        if rest:
            r.setdefault('extra', {})['topics'] = rest[:4]
            topic_cnt += 1
        elif form is None:
            stats['R 为空'] += 1
    print('统计:', dict(stats))
    print(f'form 覆盖: {sum(1 for r in rows if r.get("form")):,} / {len(rows):,}')
    print(f'含题材: {topic_cnt:,}')
    # 值域预览
    print('新 form 值:', Counter(r['form'] for r in rows if r.get('form')).most_common(12))
    print('样例题材:', [r['extra'].get('topics') for r in rows if (r.get('extra') or {}).get('topics')][:3])
    if dry:
        print('[dry-run] 未写回')
        return
    BAK.mkdir(exist_ok=True)
    shutil.copy2(JSONL, BAK / 'pre-essen-form-20260923.jsonl')
    with JSONL.open('w', encoding='utf-8', newline='\n') as f2:
        for r in rows:
            f2.write(json.dumps(r, ensure_ascii=False, separators=(',', ':')) + '\n')
    print('✓ 已写入 essen.jsonl（备份 pre-essen-form-20260923.jsonl）')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    main(ap.parse_args().dry_run)
