#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""B 阶段 · hymntime 作曲家页 → cyberhymnal 的 region（国籍）+ 生卒年

- URL 规则：bio/<surname 前 4 字母逐字母>/<surname>_<缩写>.htm（缩写多变体尝试）
- 解析：生卒年 + 出生地（'Born: ... , Medfield, Massachusetts.' → 美国）
- 断点缓存 _hymntime_bio.json；限速 1s；仅抓 cyberhymnal 曲目数 top N 的作曲家
用法：python tools/fetch_hymntime_bio.py --top 200 [--apply]
"""
from __future__ import annotations
import argparse, json, re, shutil, time, urllib.request
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACKS = ROOT / 'midi_db' / 'tracks'
BAK = ROOT / 'midi_db' / 'tracks_backup'
CACHE = ROOT.parent / '_hymntime_bio.json'
BASE = 'http://www.hymntime.com/tch/bio/'
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) midicn/1.0'}
OP = urllib.request.build_opener(urllib.request.ProxyHandler({}))

US_STATES = {'alabama', 'alaska', 'arizona', 'arkansas', 'california', 'colorado', 'connecticut', 'delaware',
             'florida', 'georgia', 'hawaii', 'idaho', 'illinois', 'indiana', 'iowa', 'kansas', 'kentucky',
             'louisiana', 'maine', 'maryland', 'massachusetts', 'michigan', 'minnesota', 'mississippi',
             'missouri', 'montana', 'nebraska', 'nevada', 'new hampshire', 'new jersey', 'new mexico',
             'new york', 'north carolina', 'north dakota', 'ohio', 'oklahoma', 'oregon', 'pennsylvania',
             'rhode island', 'south carolina', 'south dakota', 'tennessee', 'texas', 'utah', 'vermont',
             'virginia', 'washington', 'west virginia', 'wisconsin', 'wyoming', 'district of columbia'}
UK_TERMS = {'england', 'scotland', 'wales', 'ireland', 'northern ireland', 'yorkshire', 'lancashire',
            'devon', 'cornwall', 'kent', 'essex', 'sussex', 'surrey', 'norfolk', 'suffolk', 'somerset',
            'gloucestershire', 'cheshire', 'derbyshire', 'staffordshire', 'warwickshire', 'worcestershire',
            'london', 'manchester', 'birmingham', 'liverpool', 'bristol', 'edinburgh', 'glasgow', 'dublin',
            'belfast', 'cardiff', 'oxford', 'cambridge', 'nottingham', 'leeds', 'sheffield', 'bath'}
CA_PROV = {'ontario', 'quebec', 'nova scotia', 'new brunswick', 'manitoba', 'british columbia',
           'prince edward island', 'saskatchewan', 'alberta', 'newfoundland'}
COUNTRY = {'germany': '德国', 'france': '法国', 'italy': '意大利', 'sweden': '瑞典', 'norway': '挪威',
           'denmark': '丹麦', 'netherlands': '荷兰', 'holland': '荷兰', 'belgium': '比利时',
           'switzerland': '瑞士', 'austria': '奥地利', 'russia': '俄罗斯', 'poland': '波兰',
           'spain': '西班牙', 'portugal': '葡萄牙', 'hungary': '匈牙利', 'czechoslovakia': '捷克',
           'australia': '澳大利亚', 'new zealand': '新西兰', 'south africa': '南非', 'india': '印度',
           'japan': '日本', 'china': '中国', 'korea': '韩国', 'mexico': '墨西哥', 'brazil': '巴西',
           'canada': '加拿大', 'usa': '美国', 'united states': '美国', 'america': '美国',
           'scotland': '英国', 'england': '英国', 'wales': '英国', 'ireland': '爱尔兰'}


def guess_country(place: str):
    low = place.lower()
    for term in UK_TERMS:
        if term in low:
            return '英国' if term not in ('ireland', 'northern ireland', 'dublin', 'belfast') else '爱尔兰'
    for st in US_STATES:
        if st in low:
            return '美国'
    for pv in CA_PROV:
        if pv in low:
            return '加拿大'
    for k, v in COUNTRY.items():
        if k in low:
            return v
    return None


def variants(name: str):
    """'Charles Hutchinson Gabriel' → ['gabriel_ch','gabriel_c','gabriel']"""
    parts = [p for p in re.split(r'[\s.]+', name) if p]
    if len(parts) < 2:
        return []
    sur = parts[-1].lower()
    firsts = [p[0].lower() for p in parts[:-1] if p]
    out = []
    if len(firsts) >= 2:
        out.append(f'{sur}_{firsts[0]}{firsts[1]}')
    out.append(f'{sur}_{firsts[0]}')
    out.append(sur)
    return out


def url_for(sur: str, abbr: str):
    letters = (sur + 'xxxx')[:4]
    return BASE + '/'.join(letters) + f'/{sur}_{abbr}.htm' if abbr else BASE + '/'.join(letters) + f'/{sur}.htm'


def fetch(name: str):
    m = re.split(r'[\s.]+', name)
    if len(m) < 2:
        return None
    sur = m[-1].lower()
    for ab in [f'{m[0][0].lower()}{m[1][0].lower()}' if len(m) > 2 else m[0][0].lower(),
               m[0][0].lower(), '']:
        u = url_for(sur, ab)
        try:
            r = OP.open(urllib.request.Request(u, headers=UA), timeout=25)
            return r.read().decode('utf-8', 'replace'), u
        except urllib.error.HTTPError:
            continue
        except Exception:
            time.sleep(2)
            continue
    return None


def parse(t: str):
    plain = re.sub(r'<script.*?</script>', ' ', t, flags=re.S)
    plain = re.sub(r'<[^>]+>', ' ', plain)
    plain = plain.replace('\u00ad', '').replace('\u2011', '-')
    plain = re.sub(r'\s+', ' ', plain)
    b = re.search(r'Born:\s*(?:\w+\s+\d{1,2},\s*)?(\d{4})[^.]*?\.([^.]{0,120})', plain)
    d = re.search(r'Died:\s*(?:\w+\s+\d{1,2},\s*)?(\d{4})', plain)
    yrs = re.search(r'(\d{4})\s*[-–]\s*(\d{4})', plain)
    birth = b.group(1) if b else (yrs.group(1) if yrs else None)
    death = d.group(1) if d else (yrs.group(2) if yrs else None)
    place = b.group(2) if b else ''
    return birth, death, guess_country(place), place.strip()[:80]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--top', type=int, default=200)
    ap.add_argument('--apply', action='store_true')
    a = ap.parse_args()

    rows = [json.loads(l) for l in (TRACKS / 'cyberhymnal.jsonl').open(encoding='utf-8')]
    freq = Counter(r.get('composer_name') for r in rows if r.get('composer_name'))
    targets = [n for n, _ in freq.most_common(a.top)
               if not n.lower().startswith(('anonymous', 'traditional', 'unknown')) and ' ' in n]
    print(f'目标作曲家 {len(targets)}（覆盖 {sum(freq[n] for n in targets):,} 首）')

    cache = json.loads(CACHE.read_text(encoding='utf-8')) if CACHE.exists() else {}
    ok = fail = 0
    t0 = time.time()
    for i, name in enumerate(targets):
        if name in cache:
            continue
        r = fetch(name)
        if r:
            birth, death, country, place = parse(r[0])
            cache[name] = {'birth': birth, 'death': death, 'country': country, 'place': place, 'url': r[1]}
            ok += 1
        else:
            cache[name] = {'birth': None, 'death': None, 'country': None, 'place': None, 'url': None}
            fail += 1
        if i % 20 == 0:
            CACHE.write_text(json.dumps(cache, ensure_ascii=False), encoding='utf-8')
            print(f'  [{i}/{len(targets)}] ok={ok} fail={fail} · {time.time()-t0:.0f}s', flush=True)
        time.sleep(1)
    CACHE.write_text(json.dumps(cache, ensure_ascii=False), encoding='utf-8')
    got_c = sum(1 for v in cache.values() if v.get('country'))
    got_y = sum(1 for v in cache.values() if v.get('birth'))
    print(f'✓ 完成：{len(cache)} 位 · 有国籍 {got_c} · 有生年 {got_y}')

    if a.apply:
        stats = Counter()
        new = []
        for r in rows:
            nm = r.get('composer_name') or ''
            v = cache.get(nm) or {}
            upd = False
            if v.get('country') and not r.get('region'):
                r['region'] = v['country']
                r['region_src'] = 'hymntime-bio'
                stats['region 补'] += 1
                upd = True
            if v.get('birth') and not r.get('birth'):
                r['birth'] = int(v['birth'])
                stats['birth 补'] += 1
                upd = True
            if v.get('death') and not r.get('death'):
                r['death'] = int(v['death'])
                stats['death 补'] += 1
                upd = True
            new.append(json.dumps(r, ensure_ascii=False, separators=(',', ':')) if upd else json.dumps(r, ensure_ascii=False, separators=(',', ':')))
        BAK.mkdir(exist_ok=True)
        shutil.copy2(TRACKS / 'cyberhymnal.jsonl', BAK / 'pre-hymntime-bio-20260923.jsonl')
        (TRACKS / 'cyberhymnal.jsonl').write_text('\n'.join(new) + '\n', encoding='utf-8')
        print('统计:', dict(stats))


if __name__ == '__main__':
    main()
