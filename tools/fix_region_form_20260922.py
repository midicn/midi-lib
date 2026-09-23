#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""region 归一化第二轮 + essen form 清洗 + no=0 脏值修复

① region：英文/德文/拼音形容词与国名 → 中文国名；Taiwan→中国台湾（红线）；问号标注（Bolivia?）去问号归一
② essen form 全清：德文题材描述词（liebes-lied 等 720 个杂值）不是曲式——宁缺毋滥
③ aria 的 no=0 脏值 → 清空
"""
from __future__ import annotations
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACKS = ROOT / 'midi_db' / 'tracks'

NORM2 = {
    # 英文形容词 → 中文国名
    'Danish': '丹麦', 'Australian': '澳大利亚', 'Finnish': '芬兰', 'Swedish': '瑞典',
    'Ukrainian': '乌克兰', 'Dutch': '荷兰', 'Swiss': '瑞士', 'Bohemian': '捷克',
    'Mexican': '墨西哥', 'Cuban': '古巴', 'Portuguese': '葡萄牙', 'Romanian': '罗马尼亚',
    'Canadian': '加拿大', 'Argentine': '阿根廷', 'Armenian': '亚美尼亚', 'Japanese': '日本',
    'Scottish': '英国', 'Irish': '爱尔兰', 'Filipino': '菲律宾', 'Colombian': '哥伦比亚',
    'Uruguayan': '乌拉圭', 'Chilean': '智利', 'Bulgarian': '保加利亚', 'Croatian': '克罗地亚',
    'Icelandic': '冰岛', 'Lithuanian': '立陶宛', 'Paraguayan': '巴拉圭', 'Venezuelan': '委内瑞拉',
    'Iranian': '伊朗', 'Indian': '印度', 'Latvian': '拉脱维亚', 'Nigerian': '尼日利亚',
    'Egyptian': '埃及', 'Peruvian': '秘鲁', 'Turkish': '土耳其', 'English': '英国',
    'Hungarian': '匈牙利', 'Chinese': '中国', 'Flemish': '比利时',
    # 英文国名
    'Greece': '希腊', 'Hungary': '匈牙利', 'Russia': '俄罗斯', 'Turkey': '土耳其',
    'France': '法国', 'Italy': '意大利', 'Sweden': '瑞典', 'Norway': '挪威',
    'Finland': '芬兰', 'Canada': '加拿大', 'England': '英国', 'Scotland': '英国',
    'Mexico': '墨西哥', 'Argentina': '阿根廷', 'Bolivia': '玻利维亚', 'Peru': '秘鲁',
    'Ukraine': '乌克兰', 'Albania': '阿尔巴尼亚', 'Armenia': '亚美尼亚', 'Croatia': '克罗地亚',
    'China': '中国', 'USA': '美国', 'Taiwan': '中国台湾', 'Japan': '日本',
    # 德文国名
    'Frankreich': '法国', 'Russland': '俄罗斯', 'Ungarn': '匈牙利', 'Schweden': '瑞典',
    'Daenemark': '丹麦', 'Mexiko': '墨西哥', 'Polen': '波兰', 'Norge': '挪威',
    'Boehmen': '捷克', 'Maehren': '捷克', 'Kroatien': '克罗地亚', 'Slowakei': '斯洛伐克',
    'Rumaenien': '罗马尼亚', 'Litauen': '立陶宛', 'Irland': '爱尔兰', 'Ungarn(?)': '匈牙利',
    # 中国省市拼音 → 中文（chinafolk 转写残留）
    'Yunnan': '云南', 'Shanxi': '山西', 'Shaanxi': '陕西', 'Liaoning': '辽宁',
    'Anhui': '安徽', 'Hubei': '湖北', 'Heilongjiang': '黑龙江', 'Hebei': '河北',
    'Sichuan': '四川', 'Jiangsu': '江苏', 'Qinghai': '青海', 'Xinjiang': '新疆',
    'Hunan': '湖南', 'Shanbei': '陕西',
    # 问号标注 → 去问号归一
    'Bolivia?': '玻利维亚', 'Smaaland?': 'Smaaland', 'Peru?': '秘鲁', 'Peru/Bolivia': '秘鲁',
}

# essen 的 form 是德文题材描述（liebes-lied 等），不是曲式——全清（宁缺毋滥）
CLEAR_FORM_SRC = {'essen'}


def run():
    stats = Counter()
    for f in sorted(TRACKS.glob('*.jsonl')):
        sid = f.stem
        lines = f.read_text(encoding='utf-8').splitlines()
        modified = False
        for i, line in enumerate(lines):
            r = json.loads(line)

            # ① region 归一化
            rg = r.get('region')
            if rg in NORM2 and NORM2[rg] != rg:
                r['region'] = NORM2[rg]
                stats[f'region:{rg}→{NORM2[rg]}'] += 1
                lines[i] = json.dumps(r, ensure_ascii=False, separators=(',', ':'))
                modified = True

            # ② essen form 清空
            if sid in CLEAR_FORM_SRC and r.get('form'):
                r['form'] = None
                stats['form_clear'] += 1
                lines[i] = json.dumps(r, ensure_ascii=False, separators=(',', ':'))
                modified = True

            # ③ no=0 脏值
            if r.get('no') == 0:
                r['no'] = None
                stats['no_zero_fix'] += 1
                lines[i] = json.dumps(r, ensure_ascii=False, separators=(',', ':'))
                modified = True

        if modified:
            f.write_text('\n'.join(lines) + '\n', encoding='utf-8')
            print(f'  [saved] {f.name}', flush=True)

    print('=' * 72)
    for k, n in sorted(stats.items()):
        print(f'  {k:34s} {n:>7,d}')


if __name__ == '__main__':
    run()
