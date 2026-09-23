#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""补漏 3 · essen 题材（extra.topics 德/波原文）→ 中文标签 extra.topics_zh
用法：python tools/translate_essen_topics.py [--dry-run]
"""
from __future__ import annotations
import argparse, json, re, shutil
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JSONL = ROOT / 'midi_db' / 'tracks' / 'essen.jsonl'
BAK = ROOT / 'midi_db' / 'tracks_backup'

# 题材关键词 → 中文标签（按顺序匹配，长词优先）
TOPIC_MAP = [
    ('wiegen', '摇篮'), ('kinder', '童趣'), ('reigen', '轮舞'), ('tanz', '舞会'), ('taenze', '舞会'),
    ('hochzeit', '婚礼'), ('ehestand', '婚姻'), ('brautwerbung', '求亲'), ('liebes', '爱情'), ('liebe', '爱情'),
    ('leid', '悲怨'), ('klage', '哀叹'), ('sehnsucht', '思念'), ('abschied', '离别'), ('trennung', '分离'),
    ('heimkehr', '归乡'), ('wander', '漫游'), ('reise', '旅途'), ('fremde', '异乡'),
    ('tod', '死亡'), ('mord', '凶杀'), ('selbstmord', '自尽'), ('strafe', '报应'), ('reue', '悔恨'),
    ('hinrichtung', '刑罚'), ('krieg', '战争'), ('soldat', '从军'), ('helden', '英雄'), ('ehren', '荣光'),
    ('vaterland', '家国'), ('heimat', '乡土'), ('politisch', '时政'), ('national', '家国'),
    ('jaeger', '狩猎'), ('beruf', '劳作'), ('handwerker', '工匠'), ('bauern', '农事'), ('hirt', '牧歌'),
    ('trink', '饮酒'), ('zech', '饮酒'), ('studenten', '学子'), ('scherz', '诙谐'), ('schalk', '戏谑'),
    ('schelmen', '戏谑'), ('spott', '讽刺'), ('satyre', '讽刺'),
    ('geistlich', '宗教'), ('religioes', '宗教'), ('religiöses', '宗教'), ('wallfahrt', '朝圣'),
    ('heiligen', '圣徒'), ('legende', '传说'), ('sage', '传说'), ('maerchen', '童话'), ('zauber', '奇幻'),
    ('natur', '自然'), ('jahreszeiten', '时令'), ('fruehling', '春'), ('sommer', '夏'), ('herbst', '秋'), ('winter', '冬'),
    ('staende', '身份'), ('adelige', '贵族'), ('dienstmagd', '主仆'), ('standesunterschied', '门第'),
    ('habgier', '贪婪'), ('betrug', '欺骗'), ('verfuehrung', '引诱'), ('verbotene liebe', '禁忌之恋'),
    ('flucht', '逃亡'), ('entfuehrung', '掳掠'), ('menschenhandel', '买卖人口'), ('rettung', '拯救'),
    ('mordversuch', '谋害'), ('rache', '复仇'), ('schwangerschaft', '身孕'), ('familien', '家族'),
    ('geschichte', '史事'), ('historische', '史事'), ('gedaechtnis', '追忆'), ('todesahnung', '预兆'),
    ('blut', '血案'), ('marien', '圣母'), ('fest', '节庆'), ('glaube', '信仰'), ('hosianna', '赞颂'),
]


def to_zh(topics):
    out = []
    for t in topics:
        low = t.lower()
        zh = None
        for kw, z in TOPIC_MAP:
            if kw in low:
                zh = z
                break
        if zh and zh not in out:
            out.append(zh)
    return out[:3]


def main(dry: bool):
    rows = [json.loads(l) for l in JSONL.open(encoding='utf-8')]
    stats = Counter()
    dist = Counter()
    for r in rows:
        ex = r.get('extra') or {}
        ts = ex.get('topics') or []
        if not ts:
            continue
        zh = to_zh(ts)
        if zh:
            ex['topics_zh'] = zh
            r['extra'] = ex
            stats['topics_zh'] += 1
            for z in zh:
                dist[z] += 1
        else:
            stats['未映射'] += 1
    print('统计:', dict(stats))
    print('中文题材 top14:', dist.most_common(14))
    if dry:
        print('[dry-run] 未写回')
        return
    BAK.mkdir(exist_ok=True)
    shutil.copy2(JSONL, BAK / 'pre-essen-topics-zh-20260923.jsonl')
    with JSONL.open('w', encoding='utf-8', newline='\n') as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False, separators=(',', ':')) + '\n')
    print('✓ essen.jsonl 已写入')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    main(ap.parse_args().dry_run)
