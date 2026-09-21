#!/usr/bin/env python3
"""抓取 Mutopia .ly 头文件（1,861 首）→ sources/mutopia/_headers/{Init}/{Work}.ly"""
import json, re, sys, time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
paths = json.loads((ROOT / 'sources/mutopia/_repo_tree.json').read_text(encoding='utf-8'))
lys = set(p for p in paths if p.startswith('ftp/') and p.endswith('.ly'))
rows = [json.loads(l) for l in (ROOT / 'midi_db/tracks/mutopia.jsonl').open(encoding='utf-8')]
OUT = ROOT / 'sources/mutopia/_headers'
OUT.mkdir(parents=True, exist_ok=True)

jobs = []
for r in rows:
    sp = r.get('src_path') or ''
    m = re.match(r'sources/mutopia/([^/]+)/([^/]+)/', sp)
    if not m:
        continue
    init, work = m.group(1), m.group(2)
    rel = f'ftp/{init}/{work}/{work}.ly'
    dest = OUT / init / f'{work}.ly'
    if dest.exists() and dest.stat().st_size > 50:
        continue
    rp = rel if rel in lys else None
    if rp is None:
        cand = [p for p in lys if p.lower().startswith(f'ftp/{init}/{work}/'.lower())]
        rp = cand[0] if cand else None
    if rp:
        jobs.append((r['id'], rp, dest))

print(f'待抓取: {len(jobs):,}（已缓存 {len(rows)-len(jobs)}）', flush=True)
BASE = 'https://raw.githubusercontent.com/MutopiaProject/MutopiaProject/master/'

def fetch(job):
    tid, rp, dest = job
    for a in range(3):
        try:
            req = urllib.request.Request(BASE + rp, headers={'User-Agent': 'midicn'})
            txt = urllib.request.urlopen(req, timeout=45).read().decode('utf-8', 'replace')
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(txt, encoding='utf-8')
            return tid, True, None
        except Exception as e:
            if a == 2:
                return tid, False, f'{type(e).__name__} {str(e)[:60]}'
            time.sleep(1.5 * (a + 1))

ok = fail = 0
fails = []
with ThreadPoolExecutor(max_workers=8) as ex:
    futs = [ex.submit(fetch, j) for j in jobs]
    for fut in as_completed(futs):
        tid, success, err = fut.result()
        if success:
            ok += 1
        else:
            fail += 1
            fails.append((tid, err))
        if (ok + fail) % 200 == 0:
            print(f'  进度 {ok + fail:,}/{len(jobs):,} · 失败 {fail}', flush=True)
print(f'完成: 成功 {ok:,} · 失败 {fail:,}')
for tid, err in fails[:10]:
    print('  失败:', tid, err)
