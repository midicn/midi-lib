#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""补漏 1 · essen 的 .sm 字段（CUT 原文曲名 + REG 结构化地域）
用法：python tools/enrich_essen_sm_fields.py [--dry-run]
"""
from __future__ import annotations
import argparse, json, re, shutil
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ABC = ROOT / 'sources' / 'essen' / 'esac'
JSONL = ROOT / 'midi_db' / 'tracks' / 'essen.jsonl'
BAK = ROOT / 'midi_db' / 'tracks_backup'

# REG 末段 → 中文国家/地区
COUNTRY = {
    'deutschland': '德国', 'oesterreich': '奥地利', 'osterreich': '奥地利', 'schweiz': '瑞士',
    'luxemburg': '卢森堡', 'lothringen': '法国', 'elsass': '法国', 'frankreich': '法国',
    'polen': '波兰', 'galizien': '乌克兰', 'posen': '波兰', 'schlesien': '波兰',
    'ostpreussen': '俄罗斯', 'ungarn': '匈牙利', 'tschechien': '捷克', 'boehmen': '捷克',
    'maehren': '捷克', 'slowakei': '斯洛伐克', 'italien': '意大利', 'spanien': '西班牙',
    'england': '英国', 'schottland': '英国', 'irland': '爱尔兰', 'niederlande': '荷兰',
    'holland': '荷兰', 'belgien': '比利时', 'daenemark': '丹麦', 'schweden': '瑞典',
    'norwegen': '挪威', 'finnland': '芬兰', 'russland': '俄罗斯', 'japan': '日本',
    'china': '中国', 'korea': '韩国', 'portugal': '葡萄牙', 'griechenland': '希腊',
    'tuerkei': '土耳其', 'kroatien': '克罗地亚', 'serbien': '塞尔维亚', 'bulgarien': '保加利亚',
    'rumaenien': '罗马尼亚', 'slovenien': '斯洛文尼亚', 'usa': '美国', 'kanada': '加拿大',
    'australien': '澳大利亚', 'brasilien': '巴西', 'mexiko': '墨西哥', 'suedamerika': '南美洲',
}


def main(dry: bool):
    index = {}
    for f in sorted(ABC.glob('*.sm')):
        t = f.read_text(encoding='utf-8', errors='replace')
        for block in [b for b in t.split('\n\n') if b.strip()]:
            mkey = re.search(r'KEY\[(\S+)', block)
            cut = re.search(r'CUT\[([^\]]*)\]', block)
            reg = re.search(r'REG\[([^\]]*)\]', block)
            if mkey:
                index.setdefault(f.stem.upper(), {})[mkey.group(1)] = {
                    'cut': cut.group(1).strip() if cut else None,
                    'reg': reg.group(1).strip() if reg else None}
    print(f'.sm 索引: {len(index)} 文件 · 条目 {sum(len(v) for v in index.values()):,}')

    rows = [json.loads(l) for l in JSONL.open(encoding='utf-8')]
    stats = Counter()
    for r in rows:
        kid = str((r.get('extra') or {}).get('key_in_dataset') or '')
        m = re.match(r'^([A-Za-z0-9]+)#x(\d+)$', kid)
        if not m:
            stats['无 key'] += 1; continue
        code, x = m.group(1).upper(), int(m.group(2))
        # .sm 的 KEY 是 A0001/ C0002 形式的 ESAC 编号——用 native_id 匹配更稳
        nat = str((r.get('extra') or {}).get('native_id') or '')
        ent = None
        smap = index.get(code) or {}
        if nat:
            for k, v in smap.items():
                if k.startswith(nat):
                    ent = v; break
        if not ent:
            # 回退：按 X 序号在 .sm 条目中定位（同序）
            vals = list(smap.values())
            if 1 <= x <= len(vals):
                ent = vals[x - 1]
        if not ent:
            stats['未匹配'] += 1; continue
        if ent.get('cut'):
            r.setdefault('extra', {})['cut_title'] = ent['cut']
            stats['CUT 补'] += 1
        if ent.get('reg') and not r.get('region'):
            parts = [p.strip().lower() for p in ent['reg'].split(',')]
            cn = None
            for p in reversed(parts):
                if p in COUNTRY:
                    cn = COUNTRY[p]; break
                if p in ('europa', 'mitteleuropa', 'nordeuropa', 'suedeuropa', 'westeuropa', 'osteuropa'):
                    continue
                if p.startswith('china') or p in ('asien',):
                    cn = '中国' if 'china' in p else None
                    if cn:
                        break
            if cn:
                r['region'] = cn
                r['region_src'] = 'essen-sm-reg'
                stats['region 补'] += 1
    print('统计:', dict(stats))
    if dry:
        print('[dry-run] 未写回')
        return
    BAK.mkdir(exist_ok=True)
    shutil.copy2(JSONL, BAK / 'pre-essen-sm-20260923.jsonl')
    with JSONL.open('w', encoding='utf-8', newline='\n') as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False, separators=(',', ':')) + '\n')
    print('✓ essen.jsonl 已写入')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    main(ap.parse_args().dry_run)
