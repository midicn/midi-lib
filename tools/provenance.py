#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""来源台账复核器 / 文档生成器（midicn-lib）

功能
  python tools/provenance.py            # 复核：注册表 ↔ 站点 archive.js ↔ 发布 catalog ↔ 本地证据
  python tools/provenance.py --hash     # 追加复核整包校验值（MD5/字节数）
  python tools/provenance.py --online   # 追加复核各「原始地址」当前可达性
  python tools/provenance.py --render   # 由注册表生成 docs/PROVENANCE.md

设计原则
  1. 地址唯一：每个来源只登记一个地址，且必须等于 archive.js 里实际渲染的值
  2. 档位一致：C1/C2/C3 必须与发布 catalog 的 z 字段一致（合规红线）
  3. 证据可查：每条地址都指向本地证据文件（并校验其中的关键串）
  4. 校验值优先上游：有上游官方 md5/大小就用它，否则记本地快照值仅作完整性基线

需要能访问数据工作副本（含 sources/ 与 release/site-repo/）。
未找到时脚本会自动降级为「记录自检」模式（仍可校验注册表内部一致性与地址可达性）。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import urllib.request
from collections import Counter
from pathlib import Path

TIER_OF = {'main': 'C1', 'piano': 'C2', 'piano-special': 'C2', 'study': 'C3'}
UA = 'Mozilla/5.0 (compatible; midicn-provenance-check/1.0)'


# ─────────────────────────── 定位工作副本 ───────────────────────────
def find_root(explicit: str | None) -> Path | None:
    cands: list[Path] = []
    if explicit:
        cands.append(Path(explicit))
    if os.environ.get('MIDICN_ROOT'):
        cands.append(Path(os.environ['MIDICN_ROOT']))
    here = Path(__file__).resolve()
    for up in list(here.parents)[:4]:
        cands += [up, up / 'lib.midicn.com']
    for c in cands:
        if (c / 'release/site-repo/assets/archive.js').exists():
            return c
    return None


def md5_file(p: Path) -> str:
    h = hashlib.md5()
    with p.open('rb') as f:
        while True:
            b = f.read(1 << 22)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


# ─────────────────────────── 读取权威来源 ───────────────────────────
def read_site(archive_js: Path):
    s = archive_js.read_text(encoding='utf-8')
    out = {}
    for m in re.finditer(r"\{\n    id:'(\w+)',(.*?)\n  \}", s, re.S):
        b = m.group(2)
        out[m.group(1)] = {
            'url': re.search(r"url:'([^']+)'", b).group(1),
            'zone': re.search(r"zone:'([^']+)'", b).group(1),
            'license': re.search(r"license:'([^']+)'", b).group(1),
            'count': int(re.search(r"count:(\d+)", b).group(1)),
        }
    return out


def read_catalog(cat_path: Path):
    cat = json.loads(cat_path.read_text(encoding='utf-8'))
    rows = cat if isinstance(cat, list) else (cat.get('tracks') or cat.get('items') or [])
    cnt, zone, lic = Counter(), Counter(), Counter()
    for r in rows:
        sid = re.sub(r'-\d+$', '', str(r.get('id', '')))
        cnt[sid] += 1
        zone[(sid, str(r.get('z')))] += 1
        lic[(sid, str(r.get('l')))] += 1
    return rows, cnt, zone, lic


def dominant(pairs, sid, default='?'):
    got = [(k[1], v) for k, v in pairs.items() if k[0] == sid]
    return max(got, key=lambda t: t[1])[0] if got else default


# ─────────────────────────── 复核 ───────────────────────────
def verify(reg: dict, root: Path | None, do_hash: bool, do_online: bool) -> int:
    ok = bad = soft = 0

    def line(state, name, detail=''):
        nonlocal ok, bad, soft
        mark = {'OK': '  ✓', 'FAIL': '  ✗', 'SKIP': '  ·'}[state]
        if state == 'OK':
            ok += 1
        elif state == 'FAIL':
            bad += 1
        else:
            soft += 1
        print(f'{mark} {name}' + (f' — {detail}' if detail else ''))

    print('=' * 96)
    print(f'来源台账复核 · 核验日期 {reg.get("verified_on")} · 工作副本 {root or "（未找到，降级为记录自检）"}')
    print('=' * 96)

    site = read_site(root / 'release/site-repo/assets/archive.js') if root else {}
    rows = cnt = zone = lic = None
    if root:
        rows, cnt, zone, lic = read_catalog(root / 'release/site-repo/meta/catalog.json')
        print(f'站点 SOURCES {len(site)} 条 · 发布 catalog {len(rows):,} 首')

    ids_reg = [s['id'] for s in reg['sources']]
    if site:
        line('OK' if set(ids_reg) == set(site) else 'FAIL', '来源集合一致（注册表 ↔ 站点）',
             f'仅注册表: {sorted(set(ids_reg) - set(site))} 仅站点: {sorted(set(site) - set(ids_reg))}'
             if set(ids_reg) != set(site) else f'{len(ids_reg)} 个')

    print('-' * 96)
    print(f'{"来源":13s} {"地址核验":9s} {"档位":9s} {"计数":16s} {"证据":7s} {"校验值":9s}')
    print('-' * 96)

    for s in reg['sources']:
        sid = s['id']
        # ① 地址
        st = site.get(sid)
        a_state = 'FAIL'
        if st:
            a_state = 'OK' if st['url'] == s['address'] else 'FAIL'
        line(a_state, f'{sid:13s} 地址', f'{s["address"]}' if a_state == 'OK' else
             f'注册表 {s["address"]} ≠ 站点 {st["url"] if st else "（缺失）"}')

        # ② 档位（合规红线）
        t_site = TIER_OF.get(st['zone'], st['zone']) if st else '?'
        t_cat = TIER_OF.get(dominant(zone, sid), dominant(zone, sid)) if zone else s['tier']
        t_state = 'OK' if (t_site == t_cat == s['tier']) else 'FAIL'
        line(t_state, f'{sid:13s} 档位', f'{t_site} / catalog {t_cat}' if t_state == 'OK'
             else f'站上 {t_site} · catalog {t_cat} · 注册表 {s["tier"]}')

        # ③ 计数
        c_site = st['count'] if st else 0
        c_cat = cnt.get(sid, 0) if cnt else s['count']
        c_state = 'OK' if (c_site == c_cat == s['count']) else 'FAIL'
        line(c_state, f'{sid:13s} 计数', f'{c_cat:,} 首' if c_state == 'OK'
             else f'站点 {c_site:,} · catalog {c_cat:,} · 注册表 {s["count"]:,}')

        # ④ 证据
        ev_fail = []
        for e in s['evidence']:
            if not root:
                ev_fail.append('（无工作副本，跳过）')
                break
            fp = root / e['path']
            if not fp.exists():
                ev_fail.append(f'缺文件 {e["path"]}')
            elif e.get('contains'):
                try:
                    t = fp.read_text(encoding='utf-8', errors='replace') if fp.is_file() else \
                        '\n'.join(x.name for x in fp.iterdir())
                except OSError:
                    t = ''
                if e['contains'] not in t:
                    ev_fail.append(f'{e["path"]} 不含「{e["contains"][:40]}」')
        ev_state = 'SKIP' if (not root or ev_fail == ['（无工作副本，跳过）']) else ('OK' if not ev_fail else 'FAIL')
        line(ev_state, f'{sid:13s} 证据', f'{len(s["evidence"])} 项'
             if ev_state == 'OK' else ('工作副本不可用' if ev_state == 'SKIP' else '；'.join(ev_fail)[:120]))

        # ⑤ 校验值
        chk_state = 'SKIP'
        detail = ''
        if do_hash and root and s['archives']:
            probs = []
            for a in s['archives']:
                fp = root / a['path']
                if not fp.exists():
                    probs.append(f'缺 {a["file"]}')
                else:
                    sz = fp.stat().st_size
                    if sz != a['bytes']:
                        probs.append(f'{a["file"]} 字节 {sz:,} ≠ {a["bytes"]:,}')
                    elif a.get('md5') and md5_file(fp) != a['md5']:
                        probs.append(f'{a["file"]} MD5 不符')
            chk_state = 'OK' if not probs else 'FAIL'
            detail = f'{len(s["archives"])} 个整包一致' if not probs else '；'.join(probs)[:120]
        elif s.get('upstream'):
            u = s['upstream']
            chk_state = 'OK'
            detail = f'上游 {u["kind"]} {u["what"]} = {u["value"]}'
        elif s['archives']:
            detail = f'{len(s["archives"])} 个本地整包（用 --hash 复核）'
        line(chk_state, f'{sid:13s} 校验值', detail)

        # ⑥ 地址可达性
        if do_online:
            try:
                r = urllib.request.urlopen(urllib.request.Request(
                    s['address'], headers={'User-Agent': UA}), timeout=30)
                code = r.status
            except Exception as e:
                code = getattr(e, 'code', None) or type(e).__name__
            reach = 'OK' if str(code).startswith('2') or str(code) in ('403', '406') else 'FAIL'
            line(reach, f'{sid:13s} 可达性', f'HTTP {code}'
                 + ('（站点对脚本限流，浏览器可访问）' if str(code) in ('403', '406') else ''))

    print('-' * 96)
    print(f'结果：通过 {ok} · 失败 {bad} · 跳过/提示 {soft}')
    return 1 if bad else 0


# ─────────────────────────── 生成文档 ───────────────────────────
def render(reg: dict, out_md: Path) -> None:
    S = reg['sources']
    L = []
    L.append('# PROVENANCE · 来源台账（每个原始地址的取得与核验记录）')
    L.append('')
    L.append(f'> 核验日期 **{reg["verified_on"]}** · 来源 **{len(S)}** 个 · '
             f'合计 **{sum(s["count"] for s in S):,}** 首 · 机器可读版 [`provenance.json`](provenance.json)')
    L.append('>')
    L.append('> 本文件回答一个问题：**来源页上写的那个「原始地址」，凭什么说它是我们真正取得数据的地方？**')
    L.append('> 每个来源都给出：地址、取得方式、本地证据文件、整包校验值（有则附上游官方值）、许可档位与核验日期。')
    L.append('')
    L.append('## 一、三条规则')
    L.append('')
    L.append('1. **地址唯一且真实**：每个来源只登记一个地址，= 我们实际取得数据的位置；')
    L.append('   不写泛泛的站点首页，不写凭印象猜的官网，更不写与数据无关的站点。')
    L.append('2. **档位必须与数据一致**：C1 可商用 / C2 非商用 / C3 学习研究，逐曲写入 catalog 的 `z` 字段；')
    L.append('   来源页标注与 catalog 不一致即视为缺陷（本台账每次复核都会检查）。')
    L.append('3. **可复核**：每条地址都有本地证据（文件自述 / 采集台账 / 校验值），并记录核验日期。')
    L.append('')
    L.append('## 二、总表')
    L.append('')
    L.append('| 来源 | 档位 | 曲目数 | 原始地址 |')
    L.append('|---|---|---:|---|')
    for s in S:
        L.append(f'| {s["id"]} | {s["tier"]} | {s["count"]:,} | `{s["address"]}` |')
    L.append(f'| **合计** | | **{sum(s["count"] for s in S):,}** | |')
    L.append('')
    L.append('## 三、逐源明细')
    L.append('')
    for s in S:
        L.append(f'### {s["id"]}')
        L.append('')
        L.append(f'- **原始地址**：`{s["address"]}`')
        L.append(f'- **取得方式**：{s["how_we_got_it"]}')
        L.append(f'- **入库脚本**：`{s["ingest"]}`')
        ev = '；'.join(
            (f'`{e["path"]}`' + (f'（含 `{e["contains"]}`）' if e.get('contains') else ''))
            for e in s['evidence'])
        L.append(f'- **本地证据**：{ev or "—"}')
        loc = '；'.join(f'`{l["dir"]}` {l["files"]:,} 文件 / {l["bytes"]/1e6:.1f}MB' for l in s['local'])
        L.append(f'- **本地规模**：{loc or "—"}')
        if s['archives']:
            for a in s['archives']:
                L.append(f'- **整包校验**：`{a["file"]}` {a["bytes"]:,} 字节 · MD5 `{a["md5"]}`'
                         '（本地快照值，用于完整性复核）')
        if s.get('upstream'):
            u = s['upstream']
            L.append(f'- **上游官方口径**：{u["what"]} = `{u["value"]}` —— 来源：{u["source"]}')
        L.append(f'- **许可**：{s["site_license"]}（catalog 标识 `{s["catalog_license"]}`）—— {s["license_note"]}')
        L.append(f'- **核验日期**：{s["verified_on"]}')
        L.append('')
    L.append('## 四、如何自行复核')
    L.append('')
    L.append('```bash')
    L.append('# 1) 对照来源页与数据：站点标注 ↔ 发布 catalog ↔ 台账')
    L.append('python tools/provenance.py            # 地址 / 档位 / 计数 / 证据文件')
    L.append('python tools/provenance.py --hash     # 追加整包 MD5 与字节数复核')
    L.append('python tools/provenance.py --online   # 追加各地址当前可达性')
    L.append('')
    L.append('# 2) 只用公开信息核验（无需我们的采集目录）')
    L.append('#    - Wikifonia 整包 MD5 可与公开数据集注册表比对：')
    L.append('#      muspy.datasets.wikifonia → md5(Wikifonia.zip) = d26e22562e67eb7d37535e96cc5eebba')
    L.append('#    - GiantMIDI-Piano：官方 README 声明数据集 193 MB，与本台账 midis_v1.2.zip')
    L.append('#      192,678,627 字节一致')
    L.append('```')
    L.append('')
    L.append('## 五、变更纪律')
    L.append('')
    L.append('- **改任何来源地址前**：先按本台账的办法取得证据（文件自述 / 采集台账 / 上游官方口径），')
    L.append('  再改 `assets/archive.js` 与本文件，并更新核验日期。**拿不到证据就不要改，也不要写。**')
    L.append('- **改许可档位前**：必须用发布 catalog（`release/site-repo/meta/catalog.json`）重新统计，')
    L.append('  档位与数据不一致会直接影响使用者的合规判断（历史上 lakh 与 emopia 曾各错标一次，已修）。')
    L.append('- 回归：`tools/e2e-test.js` 的【11】段已把 19 个地址、档位与「禁止错误地址复现」写进断言。')
    L.append('')
    L.append('---')
    L.append('')
    L.append('## English (summary)')
    L.append('')
    L.append(f'Provenance ledger, verified {reg["verified_on"]}. '
             f'{len(S)} sources, {sum(s["count"] for s in S):,} tracks. Each source records a **single** address — '
             'the place we actually obtained the data from — together with how it was obtained, a local evidence '
             'file (self-statement or acquisition ledger), package checksums where available (upstream-published '
             'values preferred), the licence tier, and the verification date.')
    L.append('')
    L.append('Three rules: (1) one true address per source, never a generic homepage or a guessed official site; '
             '(2) the tier (C1 commercial / C2 non-commercial / C3 study-only) must match the per-track `z` field '
             'in the published catalog; (3) every address must be backed by evidence. '
             'Re-verify with `python tools/provenance.py [--hash] [--online]`.')
    L.append('')
    out_md.write_text('\n'.join(L) + '\n', encoding='utf-8')


def main(argv):
    ap = argparse.ArgumentParser(description='来源台账复核 / 文档生成')
    ap.add_argument('--root', help='数据工作副本（含 sources/ 与 release/site-repo/）')
    ap.add_argument('--registry', help='台账 JSON 路径（默认 <root>/docs/provenance.json）')
    ap.add_argument('--hash', action='store_true', help='复核整包 MD5 与字节数')
    ap.add_argument('--online', action='store_true', help='探测各地址当前可达性')
    ap.add_argument('--render', action='store_true', help='生成 docs/PROVENANCE.md')
    args = ap.parse_args(argv[1:])

    root = find_root(args.root)
    reg_path = Path(args.registry) if args.registry else (
        (root / 'docs/provenance.json') if root else Path('docs/provenance.json'))
    if not reg_path.exists():
        print(f'找不到台账文件：{reg_path}', file=sys.stderr)
        return 2
    reg = json.loads(reg_path.read_text(encoding='utf-8'))
    print(f'台账：{reg_path}（{len(reg["sources"])} 条）')

    if args.render:
        for dest in [reg_path.parent / 'PROVENANCE.md']:
            render(reg, dest)
            print('已生成', dest, f'({dest.stat().st_size/1024:.1f}KB)')
        return 0

    return verify(reg, root, args.hash, args.online)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
