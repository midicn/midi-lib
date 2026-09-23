#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A3 · 作曲家规范化（slug 归并 + 显示名清洗 + 中文名 cn_zh）

原则（SOUL.md）：不做相似度自动合并 —— 归并表为**人工确认的同人**；显示名清洗只用确定性规则；中文名只给有标准译名者。

用法：python tools/normalize_composer.py [--dry-run]
"""
from __future__ import annotations
import argparse, json, re, shutil
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACKS = ROOT / 'midi_db' / 'tracks'
BAK = ROOT / 'midi_db' / 'tracks_backup'

# ── ① slug 归并（人工确认的同人；值为规范 slug）─────────────
SLUG_MERGE = {
    'bach': 'johann-sebastian-bach',
    'js-bach': 'johann-sebastian-bach',
    'j-s-bach': 'johann-sebastian-bach',
    'beethoven': 'ludwig-van-beethoven',
    'mozart': 'wolfgang-amadeus-mozart',
    'schubert': 'franz-schubert',
    'schumann': 'robert-schumann',
    'chopin': 'frederic-chopin', 'fr-d-ric-chopin': 'frederic-chopin',
    'scarlatti': 'domenico-scarlatti',
    'rachmaninoff': 'sergei-rachmaninoff',
    'mendelssohn': 'felix-mendelssohn', 'mendelssohn-bartholdy': 'felix-mendelssohn',
    'haydn': 'franz-joseph-haydn',
    'liszt': 'franz-liszt',
    'brahms': 'johannes-brahms',
    'tchaikovsky': 'pyotr-ilyich-tchaikovsky',
    'debussy': 'claude-debussy',
    'bartok': 'bela-bartok',
    'prokofiev': 'sergei-prokofiev',
    'grieg': 'edvard-grieg',
    'handel': 'george-frideric-handel',
    'satie': 'erik-satie',
    'ravel': 'maurice-ravel',
    'dvorak': 'antonin-dvorak',
    'mussorgsky': 'modest-mussorgsky',
    'shostakovich': 'dmitri-shostakovich',
    'scriabin': 'alexander-scriabin',
    'czerny': 'carl-czerny',
    'clementi': 'muzio-clementi',
    'corelli': 'arcangelo-corelli',
    'vivaldi': 'antonio-vivaldi',
    'weber': 'carl-maria-von-weber',
    'giuliani': 'mauro-giuliani',
    'moszkowski': 'moritz-moszkowski',
}

# 特殊分流：slug=bach 下混有其他 Bach
CPE_BACH = 'carl-philipp-emanuel-bach'
# groove 鼓手（非作曲家）→ traditional
DRUMMER_RE = re.compile(r'^drummer\d+$')

# ── ② 显示名清洗规则（确定性）────────────────────────────
PREFIX_RE = re.compile(r'^(?:arranged\s+from|arrangement\s+of|from|attributed\s+to|composed\s+by|by|after)\s+', re.I)
TRIM_RE = re.compile(r'\s*(?:,?\s*(?:based\s+o\w*|adapted\s+by|arranged\s+(?:by|fm)|ca\.\s*\d|18\d\d|19\d\d|\d{4}).*)$', re.I)

# groove 以外：显示名尾部噪音
def clean_name(n: str, slug: str):
    if not n:
        return n
    x = n.strip()
    x = PREFIX_RE.sub('', x).strip()
    x = TRIM_RE.sub('', x).strip(' .,;:')
    x = re.sub(r'\s+', ' ', x)
    return x or n

# ── ③ 中文名（只给有确定标准译名者）──────────────────────
CN = {
    'johann-sebastian-bach': '巴赫', 'carl-philipp-emanuel-bach': 'C.P.E. 巴赫',
    'ludwig-van-beethoven': '贝多芬', 'wolfgang-amadeus-mozart': '莫扎特',
    'franz-schubert': '舒伯特', 'frederic-chopin': '肖邦', 'franz-liszt': '李斯特',
    'robert-schumann': '舒曼', 'johannes-brahms': '勃拉姆斯', 'pyotr-ilyich-tchaikovsky': '柴可夫斯基',
    'claude-debussy': '德彪西', 'maurice-ravel': '拉威尔', 'erik-satie': '萨蒂',
    'domenico-scarlatti': '斯卡拉蒂', 'franz-joseph-haydn': '海顿', 'george-frideric-handel': '亨德尔',
    'carl-czerny': '车尔尼', 'alexander-scriabin': '斯克里亚宾', 'sergei-rachmaninoff': '拉赫玛尼诺夫',
    'felix-mendelssohn': '门德尔松', 'edvard-grieg': '格里格', 'sergei-prokofiev': '普罗科菲耶夫',
    'bela-bartok': '巴托克', 'muzio-clementi': '克莱门蒂', 'moritz-moszkowski': '莫什科夫斯基',
    'charles-valentin-alkan': '阿尔康', 'cecile-chaminade': '夏米娜德', 'cornelius-gurlitt': '古利特',
    'mauro-giuliani': '朱利亚尼', 'arcangelo-corelli': '科雷利', 'carl-maria-von-weber': '韦伯',
    'giovanni-pierluigi-da-palestrina': '帕莱斯特里那', 'antonio-vivaldi': '维瓦尔第',
    'henry-purcell': '普赛尔', 'georg-philipp-telemann': '泰勒曼', 'tomaso-albinoni': '阿尔比诺尼',
    'luigi-boccherini': '博凯里尼', 'niccolo-paganini': '帕格尼尼', 'gioachino-rossini': '罗西尼',
    'giuseppe-verdi': '威尔第', 'giacomo-puccini': '普契尼', 'vincenzo-bellini': '贝利尼',
    'gaetano-donizetti': '多尼采蒂', 'hector-berlioz': '柏辽兹', 'cesar-franck': '弗兰克',
    'camille-saint-saens': '圣桑', 'georges-bizet': '比才', 'charles-gounod': '古诺',
    'jules-massenet': '马斯内', 'gabriel-faure': '福雷', 'modest-mussorgsky': '穆索尔斯基',
    'alexander-borodin': '鲍罗丁', 'nikolai-rimsky-korsakov': '里姆斯基-科萨科夫',
    'mikhail-glinka': '格林卡', 'milij-balakirev': '巴拉基列夫', 'alexander-glazunov': '格拉祖诺夫',
    'dmitri-shostakovich': '肖斯塔科维奇', 'dmitry-kabalevsky': '卡巴列夫斯基',
    'aram-khachaturian': '哈恰图良', 'gustav-mahler': '马勒', 'anton-bruckner': '布鲁克纳',
    'richard-wagner': '瓦格纳', 'richard-strauss': '理查·施特劳斯', 'jean-sibelius': '西贝柳斯',
    'carl-nielsen': '尼尔森', 'niels-gade': '加德', 'johan-svendsen': '斯文森',
    'franz-berwald': '贝瓦尔德', 'edward-elgar': '埃尔加', 'ralph-vaughan-williams': '沃恩·威廉斯',
    'gustav-holst': '霍尔斯特', 'frederick-delius': '戴留斯', 'benjamin-britten': '布里顿',
    'enrique-granados': '格拉纳多斯', 'isaac-albeniz': '阿尔贝尼斯', 'manuel-de-falla': '法雅',
    'joaquin-turina': '图里纳', 'joaquin-rodrigo': '罗德里戈', 'fernando-sor': '索尔',
    'francisco-tarrega': '塔雷加', 'heitor-villa-lobos': '维拉-洛博斯',
    'alberto-ginastera': '希纳斯特拉', 'astor-piazzolla': '皮亚佐拉', 'louis-moreau-gottschalk': '戈特沙尔克',
    'edward-macdowell': '麦克道尔', 'aaron-copland': '科普兰', 'samuel-barber': '巴伯',
    'george-gershwin': '格什温', 'charles-ives': '艾夫斯', 'john-cage': '凯奇',
    'philip-glass': '格拉斯', 'steve-reich': '赖希', 'john-adams': '约翰·亚当斯',
    'olivier-messiaen': '梅西安', 'pierre-boulez': '布列兹', 'karlheinz-stockhausen': '施托克豪森',
    'gyorgy-ligeti': '利盖蒂', 'krzysztof-penderecki': '彭德雷茨基', 'henryk-gorecki': '戈雷茨基',
    'arvo-part': '帕特', 'john-tavener': '塔文纳', 'hans-werner-henze': '亨策',
    'kurt-weill': '魏尔', 'paul-hindemith': '欣德米特', 'carl-orff': '奥尔夫',
    'leos-janacek': '亚纳切克', 'antonin-dvorak': '德沃夏克', 'bedrich-smetana': '斯美塔那',
    'lili-boulanger': '莉莉·布朗热', 'germaine-tailleferre': '塔耶费尔',
    'rebecca-clarke': '丽贝卡·克拉克', 'amy-beach': '比奇', 'florence-price': '普莱斯',
    'william-grant-still': '斯蒂尔', 'scott-joplin': '乔普林',
    'zhao-yuanren': '赵元任', 'huang-zi': '黄自', 'he-luting': '贺绿汀', 'nie-er': '聂耳',
    'xian-xinghai': '冼星海', 'ding-shande': '丁善德', 'wang-jianzhong': '王建中',
    'chu-wanghua': '储望华', 'wang-lisan': '汪立三', 'li-yinghai': '黎英海', 'chen-peixun': '陈培勋',
    'tan-dun': '谭盾', 'chen-qigang': '陈其钢', 'ye-xiaogang': '叶小钢', 'guo-wenjing': '郭文景',
    'zhou-long': '周龙', 'sheng-zong': '盛宗亮',
    'toru-takemitsu': '武满彻', 'joe-hisaishi': '久石让', 'ryuichi-sakamoto': '坂本龙一',
    'isang-yun': '尹伊桑',
    'traditional': '传统曲调', 'unknown': '佚名',
}


def main(dry: bool):
    stats = Counter()
    slug_change = Counter()
    for f in sorted(TRACKS.glob('*.jsonl')):
        sid = f.stem
        lines = f.read_text(encoding='utf-8').splitlines()
        new = []
        changed = 0
        for line in lines:
            r = json.loads(line)
            slug = r.get('composer_slug') or ''
            name = r.get('composer_name') or ''
            orig = (slug, name)
            # groove 鼓手 → traditional + performer
            if DRUMMER_RE.match(slug):
                r['composer_slug'] = 'traditional'
                r['composer_name'] = '传统曲调 Traditional'
                r.setdefault('extra', {})['performer'] = name
                stats['鼓手→传统'] += 1
            else:
                # CPE Bach 分流（slug=bach 且显示名含 Carl Philipp）
                if slug == 'bach' and 'carl philipp' in name.lower():
                    r['composer_slug'] = CPE_BACH
                    stats['CPE 分流'] += 1
                elif slug in SLUG_MERGE:
                    r['composer_slug'] = SLUG_MERGE[slug]
                # 显示名清洗
                cn = clean_name(name, r.get('composer_slug') or '')
                if cn != name:
                    r['composer_name'] = cn
                    stats['显示名清洗'] += 1
            # 中文名
            s2 = r.get('composer_slug') or ''
            if s2 in CN and not r.get('cn_zh'):
                r['cn_zh'] = CN[s2]
                stats['cn_zh'] += 1
            if (r.get('composer_slug'), r.get('composer_name')) != orig:
                changed += 1
                slug_change[(orig[0], r.get('composer_slug'))] += 1
            new.append(json.dumps(r, ensure_ascii=False, separators=(',', ':')) if changed else line)
        if changed and not dry:
            BAK.mkdir(exist_ok=True)
            shutil.copy2(f, BAK / f'pre-composer-norm-{sid}-20260923.jsonl')
            f.write_text('\n'.join(new) + '\n', encoding='utf-8')
    print('统计:', dict(stats))
    print()
    print('slug 归并明细（前 25）:')
    for (a, b), n in slug_change.most_common(25):
        if a != b:
            print(f'  {a:32s} → {b:32s} {n:>7,}')
    if dry:
        print('[dry-run] 未写回')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    main(ap.parse_args().dry_run)
