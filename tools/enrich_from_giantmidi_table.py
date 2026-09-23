#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""B 阶段（本地优先）· giantmidi 官方表补作曲家国籍 + 生卒年

- 数据源：sources/giantmidi/**.csv（143,572 行 · 6,176 位作曲家 · nationality/birth/death）
- 补：region（若空，按作曲家国籍→中文国名）+ 新字段 birth / death
- 清洗：'unknown' 跳过；1500/1600 类占位值过滤
用法：python tools/enrich_from_giantmidi_table.py [--dry-run]
"""
from __future__ import annotations
import argparse, csv, json, re, shutil
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACKS = ROOT / 'midi_db' / 'tracks'
BAK = ROOT / 'midi_db' / 'tracks_backup'

NAT_CN = {
    'german': '德国', 'french': '法国', 'italian': '意大利', 'american': '美国', 'british': '英国',
    'english': '英国', 'scottish': '英国', 'irish': '爱尔兰', 'welsh': '英国',
    'austrian': '奥地利', 'russian': '俄罗斯', 'belgian': '比利时', 'spanish': '西班牙',
    'danish': '丹麦', 'polish': '波兰', 'hungarian': '匈牙利', 'norwegian': '挪威',
    'swedish': '瑞典', 'czech': '捷克', 'bohemian': '捷克', 'australian': '澳大利亚',
    'canadian': '加拿大', 'brazilian': '巴西', 'swiss': '瑞士', 'dutch': '荷兰',
    'finnish': '芬兰', 'japanese': '日本', 'chinese': '中国', 'korean': '韩国',
    'portuguese': '葡萄牙', 'greek': '希腊', 'turkish': '土耳其', 'ukrainian': '乌克兰',
    'croatian': '克罗地亚', 'serbian': '塞尔维亚', 'bulgarian': '保加利亚', 'romanian': '罗马尼亚',
    'slovak': '斯洛伐克', 'slovenian': '斯洛文尼亚', 'mexican': '墨西哥', 'argentine': '阿根廷',
    'argentinian': '阿根廷', 'chilean': '智利', 'cuban': '古巴', 'israeli': '以色列',
    'egyptian': '埃及', 'indian': '印度', 'persian': '伊朗', 'iranian': '伊朗',
    'armenian': '亚美尼亚', 'georgian': '格鲁吉亚', 'estonian': '爱沙尼亚', 'latvian': '拉脱维亚',
    'lithuanian': '立陶宛', 'icelandic': '冰岛', 'maltese': '马耳他', 'luxembourgish': '卢森堡',
    'moldovan': '摩尔多瓦', 'belarusian': '白俄罗斯', 'uzbek': '乌兹别克斯坦', 'kazakh': '哈萨克斯坦',
    'thai': '泰国', 'vietnamese': '越南', 'indonesian': '印度尼西亚', 'philippine': '菲律宾',
    'filipino': '菲律宾', 'malaysian': '马来西亚', 'singaporean': '新加坡', 'mongolian': '蒙古',
    'salvadoran': '萨尔瓦多', 'colombian': '哥伦比亚', 'peruvian': '秘鲁', 'venezuelan': '委内瑞拉',
    'uruguayan': '乌拉圭', 'bolivian': '玻利维亚', 'ecuadorian': '厄瓜多尔', 'guatemalan': '危地马拉',
    'puerto rican': '波多黎各', 'dominican': '多米尼加', 'jamaican': '牙买加', 'haitian': '海地',
    'albanian': '阿尔巴尼亚', 'macedonian': '北马其顿', 'bosnian': '波黑', 'montenegrin': '黑山',
    'cypriot': '塞浦路斯', 'syrian': '叙利亚', 'lebanese': '黎巴嫩', 'iraqi': '伊拉克',
    'moroccan': '摩洛哥', 'tunisian': '突尼斯', 'algerian': '阿尔及利亚', 'nigerian': '尼日利亚',
    'south african': '南非', 'ethiopian': '埃塞俄比亚', 'kenyan': '肯尼亚', 'senegalese': '塞内加尔',
    'pakistani': '巴基斯坦', 'bangladeshi': '孟加拉国', 'sri lankan': '斯里兰卡', 'burmese': '缅甸',
    'cambodian': '柬埔寨', 'laotian': '老挝', 'nepalese': '尼泊尔', 'tibetan': '中国',
}


def load_table():
    p = list((ROOT / 'sources' / 'giantmidi').rglob('*similarity*.csv'))
    if not p:
        return {}
    by_sur = defaultdict(list)
    with p[0].open(encoding='utf-8', errors='replace') as f:
        for r in csv.DictReader(f, delimiter='\t'):
            s = (r.get('surname') or '').strip()
            fn = (r.get('firstname') or '').strip()
            nat = (r.get('nationality') or '').strip()
            b = (r.get('birth') or '').strip()
            d = (r.get('death') or '').strip()
            if not s:
                continue
            if b == '1500' and d == '1600':
                b = d = 'unknown'
            by_sur[s.lower()].append((fn, nat, b, d))
    # 去重：同 surname+firstname 取非 unknown 值
    table = {}
    for sur, lst in by_sur.items():
        merged = {}
        for fn, nat, b, d in lst:
            k = fn.lower()
            cur = merged.setdefault(k, {'nat': '', 'b': '', 'd': ''})
            if nat and nat.lower() != 'unknown':
                cur['nat'] = nat
            if b and b.lower() != 'unknown':
                cur['b'] = b
            if d and d.lower() != 'unknown':
                cur['d'] = d
        table[sur] = merged
    return table


def main(dry: bool):
    table = load_table()
    print(f'giantmidi 表：{len(table):,} 个姓氏')

    stats = Counter()
    for f in sorted(TRACKS.glob('*.jsonl')):
        sid = f.stem
        lines = f.read_text(encoding='utf-8').splitlines()
        new = []
        changed = 0
        for line in lines:
            r = json.loads(line)
            name = (r.get('composer_name') or '').strip()
            if not name or name.lower().startswith(('传统', 'traditional', 'unknown', '佚名')):
                new.append(line)
                continue
            parts = name.split()
            sur = parts[-1].lower().strip('.,')
            first = parts[0].lower() if len(parts) > 1 else ''
            cands = table.get(sur)
            if not cands:
                new.append(line)
                continue
            hit = cands.get(first) if first else None
            if hit is None and len(cands) == 1:
                hit = next(iter(cands.values()))
            if not hit:
                stats['姓氏有但名字不匹配'] += 1
                new.append(line)
                continue
            upd = False
            if hit['nat'] and not r.get('region'):
                cn = NAT_CN.get(hit['nat'].lower())
                if cn:
                    r['region'] = cn
                    r['region_src'] = 'giantmidi-nationality'
                    stats['region 补'] += 1
                    upd = True
            if hit['b'] and not r.get('birth'):
                r['birth'] = int(hit['b']) if hit['b'].isdigit() else hit['b']
                stats['birth 补'] += 1
                upd = True
            if hit['d'] and not r.get('death'):
                r['death'] = int(hit['d']) if hit['d'].isdigit() else hit['d']
                stats['death 补'] += 1
                upd = True
            if upd:
                changed += 1
                new.append(json.dumps(r, ensure_ascii=False, separators=(',', ':')))
            else:
                new.append(line)
        if changed and not dry:
            BAK.mkdir(exist_ok=True)
            shutil.copy2(f, BAK / f'pre-gmtable-{sid}-20260923.jsonl')
            f.write_text('\n'.join(new) + '\n', encoding='utf-8')
    print('统计:', dict(stats))
    if dry:
        print('[dry-run] 未写回')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    main(ap.parse_args().dry_run)
