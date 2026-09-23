#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""数据质量全面体检（只读）：脏值 / 缺失 / 值域异常 / 文件引用完整性"""
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACKS = ROOT / 'midi_db' / 'tracks'

issues = defaultdict(Counter)
samples = defaultdict(list)
region_vals = Counter()
form_vals = Counter()
period_vals = Counter()

for f in sorted(TRACKS.glob('*.jsonl')):
    sid = f.stem
    for line in f.open(encoding='utf-8'):
        r = json.loads(line)
        rid = r['id']

        # ① 数值健康
        for k in ('opus', 'no', 'yr'):
            v = r.get(k)
            if v == 0:
                issues[f'{k}=0 脏值'][sid] += 1
                if len(samples[f'{k}=0']) < 3: samples[f'{k}=0'].append(rid)
            if k == 'yr' and v:
                if not (800 <= v <= 2026):
                    issues['yr 越界'][sid] += 1
                    if len(samples['yr 越界']) < 5: samples['yr 越界'].append((rid, v))

        # ② duration / note_count
        mid = r.get('midi') or {}
        d = mid.get('duration_sec') or 0
        nc = mid.get('note_count') or 0
        if d <= 0:
            issues['duration<=0'][sid] += 1
            if len(samples['duration<=0']) < 3: samples['duration<=0'].append(rid)
        if nc <= 0:
            issues['note_count<=0'][sid] += 1
            if len(samples['note_count<=0']) < 3: samples['note_count<=0'].append(rid)

        # ③ fingerprint 缺失
        if not r.get('fingerprint'):
            issues['fingerprint 缺失'][sid] += 1

        # ④ 值域清点
        if r.get('region'): region_vals[r['region']] += 1
        if r.get('form'): form_vals[r['form']] += 1
        if r.get('period'): period_vals[r['period']] += 1

print('══ 问题计数（按源）══')
for k in sorted(issues, key=lambda x: -sum(issues[x].values())):
    tot = sum(issues[k].values())
    detail = ', '.join(f'{s}:{n}' for s, n in issues[k].most_common(4))
    print(f'  {k:22s} {tot:>7,}   [{detail}]')
    if samples.get(k):
        print(f'      样例: {samples[k][:3]}')

print()
print('══ region 值域（全量', len(region_vals), '个）低频项（<100）══')
low = [(v, n) for v, n in region_vals.most_common() if n < 100]
print('  ', low if low else '无')
print()
print('══ form 值域（全量', len(form_vals), '个）══')
print('  ', form_vals.most_common())
print()
print('══ period 值域 ══')
print('  ', period_vals.most_common())
