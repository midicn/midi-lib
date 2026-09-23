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
import datetime
import hashlib
import json
import os
import re
import sys
import urllib.request
from collections import Counter
from pathlib import Path

# 本脚本所在仓库根（lib.midicn.com）——供自动补跑外壳注入器使用
ROOT_DIR = Path(__file__).resolve().parents[1]

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
def verify(reg: dict, root: Path | None, do_hash: bool, do_online: bool, reg_path: Path | None = None) -> int:
    ok = bad = soft = 0

    warns: list[str] = []

    def line(state, name, detail=''):
        nonlocal ok, bad, soft
        mark = {'OK': '  ✓', 'FAIL': '  ✗', 'SKIP': '  ·', 'WARN': '  !'}[state]
        if state == 'OK':
            ok += 1
        elif state == 'FAIL':
            bad += 1
        elif state == 'WARN':
            warns.append(f'{name} — {detail}')
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
            if 'path' not in e:
                # 证据为「另有留存」的非文件型说明（如内部处置台账，不随包分发）：
                # 记入证据数但不做文件存在性检查 —— 公开台账里不应出现内部路径。
                continue
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

    # ⑦ 复核到期提醒（时间维度：180 天为一个复核周期）
    today = datetime.date.today()
    due = [s['id'] for s in reg['sources']
           if s.get('next_review_due') and s['next_review_due'] < today.isoformat()]
    if due:
        line('WARN', '复核到期', f'{len(due)} 个来源已过复核期（{today}）：{" ".join(due[:8])}'
                               f'{" …" if len(due) > 8 else ""} → 重新核验后更新 reverified / next_review_due')
    else:
        nxt = min((s['next_review_due'] for s in reg['sources'] if s.get('next_review_due')), default='—')
        line('OK', '复核周期', f'均在有效期内（最近到期 {nxt}）')

    print('-' * 96)
    # ⑧ 台账文档新鲜度（防止注册表改了、文档没重生成）
    if reg_path:
        doc = reg_path.parent / 'PROVENANCE.md'
        if doc.exists():
            same = doc.read_text(encoding='utf-8') == render_text(reg)
            line('OK' if same else 'FAIL', '台账文档与注册表同步',
                 'PROVENANCE.md 与注册表一致' if same else '内容不一致 → 运行 tools/provenance.py --render')
        else:
            line('SKIP', '台账文档与注册表同步', f'未找到 {doc}')

    print('-' * 96)
    print(f'结果：通过 {ok} · 失败 {bad} · 提醒 {len(warns)} · 跳过/提示 {soft}')
    for w in warns:
        print(f'  ! 提醒：{w}')
    return 1 if bad else 0


# ─────────────────────────── 生成站内页 ───────────────────────────
PAGE_TPL = """<!DOCTYPE html>
<html lang="zh" data-lang="zh" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>来源台账 · midicn-lib</title>
<meta name="description" content="midicn-lib 来源台账：每个来源的实际采集地址、取得方式、证据文件、整包校验值与核验日期。">
<link rel="canonical" href="https://lib.midicn.com/provenance.html">
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<header><div class="hbar">
  <a class="brand" href="./">midicn<span>-lib</span></a>
  <nav class="nav">
    <a href="./" data-zh="音乐库" data-en="Library">音乐库</a>
    <a href="download.html" data-zh="数据下载" data-en="Download">数据下载</a>
    <a href="sources.html" data-zh="数据来源" data-en="Sources">数据来源</a>
    <a href="lyrics.html" data-zh="歌词检索" data-en="Lyrics">歌词检索</a>
    <a href="licenses.html" data-zh="许可与法律" data-en="Licence">许可与法律</a>
  </nav>
  <span class="spacer"></span>
  <button class="iconbtn langbtn" id="lang">EN</button>
</div></header>

<main class="doc wide">
  <p class="meta" data-zh="档案 · 来源台账" data-en="ARCHIVE · PROVENANCE">档案 · 来源台账</p>
  <h1 data-zh="来源台账" data-en="Provenance ledger">来源台账</h1>
  <p class="lede" data-zh="本页回答一个问题：来源页上写的那个「原始地址」，凭什么说它是我们真正取得数据的地方？每个来源都给出地址、取得方式、本地证据文件、整包校验值与核验日期。"
     data-en="This page answers one question: what makes the address shown on the Sources page the place we actually obtained the data from? For every source: the address, how it was obtained, the local evidence file, package checksums and the verification date.">本页回答一个问题：来源页上写的那个「原始地址」，凭什么说它是我们真正取得数据的地方？每个来源都给出地址、取得方式、本地证据文件、整包校验值与核验日期。</p>
  <p class="meta"><span data-zh="机器可读版 provenance.json · 复核脚本 tools/provenance.py · " data-en="Machine-readable provenance.json · verifier tools/provenance.py · ">机器可读版 provenance.json · 复核脚本 tools/provenance.py · </span><a href="https://github.com/midicn/midi-lib/blob/main/docs/PROVENANCE.md" target="_blank" rel="noopener">GitHub · PROVENANCE.md</a></p>

  __RULES__

  <div class="stitle"><h2 data-zh="总表" data-en="Summary">总表</h2>
    <span class="spacer"></span><span class="meta">__COUNT__</span></div>
  <div class="panel"><div class="panel-bd"><dl class="dl">__TABLE__</dl></div></div>

  <div class="stitle"><h2 data-zh="逐源明细" data-en="Per source">逐源明细</h2></div>
  <div id="list">__CARDS__</div>

  <div class="stitle"><h2 data-zh="复核周期与变更纪律" data-en="Review cycle">复核周期与变更纪律</h2></div>
  <div class="panel"><div class="panel-bd" data-zh="__DISC_ZH__" data-en="__DISC_EN__">__DISC_ZH__</div></div>
</main>

<footer><div class="wrap">
  <div class="fbar">
    <b>midicn-lib</b>
    <nav class="fnav">
      <a href="./" data-zh="音乐库" data-en="Library">音乐库</a>
      <a href="download.html" data-zh="数据下载" data-en="Download">数据下载</a>
      <a href="sources.html" data-zh="数据来源" data-en="Sources">数据来源</a>
      <a href="provenance.html" data-zh="来源台账" data-en="Provenance">来源台账</a>
      <a href="lyrics.html" data-zh="歌词检索" data-en="Lyrics">歌词检索</a>
      <a href="licenses.html" data-zh="许可与法律" data-en="Licence">许可与法律</a>
      <a href="https://github.com/midicn/midi-lib" target="_blank" rel="noopener">GitHub</a>
    </nav>
    <span class="flic">__FNAME__</span>
  </div>
  <div class="fnote"><span id="footNote">__FOOTNOTE__</span><span id="footLegal">__FOOTLEGAL__</span></div>
</div></footer>

<style>
.pc{margin-bottom:var(--s4)}
.pc .panel-hd{gap:var(--s3)}
.pc .addr{word-break:break-all;font-family:var(--mono);font-size:var(--fs-12)}
.pc .dl dt{min-width:74px}
</style>
<script>
(function(){
  var KEY='midicn-lang';
  function store(k,v){try{ if(v===undefined) return localStorage.getItem(k); localStorage.setItem(k,v);}catch(e){return null}}
  var LANG = store(KEY) || 'zh';
  function apply(){
    document.documentElement.lang = LANG==='zh'?'zh':'en';
    document.querySelectorAll('[data-zh]').forEach(function(el){
      var v = el.getAttribute('data-'+LANG); if (v!=null) el.innerHTML = v;
    });
    document.querySelectorAll('[data-ph-zh]').forEach(function(el){
      var v = el.getAttribute('data-ph-'+LANG); if (v!=null) el.setAttribute('placeholder', v);
    });
    var b=document.getElementById('lang'); if(b) b.textContent = LANG==='zh'?'EN':'中文';
  }
  var btn=document.getElementById('lang');
  if(btn) btn.onclick=function(){ LANG = LANG==='zh'?'en':'zh'; store(KEY,LANG); apply(); };
  apply();
})();
</script>
</body>
</html>
"""


def render_page(reg: dict, dest: Path, foot_lic: str = '', foot_note: str = '', foot_legal: str = '') -> None:
    S = sorted(reg['sources'], key=lambda x: -x['count'])
    esc = lambda t: (str(t).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))
    rows = []
    for s in S:
        rows.append(f'<dt>{esc(s["id"])} · {s["tier"]} · {s["count"]:,}</dt>'
                    f'<dd class="addr"><a href="{esc(s["address"])}" target="_blank" rel="noopener">{esc(s["address"])}</a></dd>')
    cards = []
    for s in S:
        ev = '；'.join(((e.get('path') or e.get('note', '另有留存'))
                        + (f'（含 `{e["contains"]}`）' if e.get('contains') else ''))
                       for e in s['evidence'])
        loc = '；'.join(f'{l["dir"]} · {l["files"]:,} 文件 / {l["bytes"]/1e6:.1f}MB' for l in s['local'])
        arch = ''.join(
            f'<dt>整包校验</dt><dd>{esc(a["file"])} · {a["bytes"]:,} 字节 · MD5 <span class="addr">{a["md5"]}</span></dd>'
            for a in s['archives'])
        up = ''
        if s.get('upstream'):
            u = s['upstream']
            up = f'<dt>上游口径</dt><dd>{esc(u["what"])} = <span class="addr">{esc(u["value"])}</span> —— {esc(u["source"])}</dd>'
        acq = s.get('acquired') or {}
        acq_txt = ''
        if acq.get('date'):
            acq_txt = (f'<dt>取得时点</dt><dd>{esc(acq["date"])}（依据：{esc(acq.get("basis","?"))}'
                       + (f' · {esc(acq.get("evidence"))}' if acq.get('evidence') else '') + '）</dd>')
        cards.append(
            '<div class="panel pc">'
            '<div class="panel-hd"><b style="font-size:var(--fs-16)">' + esc(s['id']) + '</b>'
            '<span class="lic ' + ('c1' if s['tier'] == 'C1' else 'c2' if s['tier'] == 'C2' else 'c3') + '">'
            + s['tier'] + '</span>'
            '<span style="margin-left:auto"></span>'
            '<span class="meta">' + f'{s["count"]:,}' + ' 首</span></div>'
            '<div class="panel-bd"><dl class="dl">'
            f'<dt>原始地址</dt><dd class="addr"><a href="{esc(s["address"])}" target="_blank" rel="noopener">{esc(s["address"])}</a></dd>'
            f'<dt>取得方式</dt><dd>{esc(s["how_we_got_it"])}</dd>'
            f'<dt>入库脚本</dt><dd class="addr">{esc(s["ingest"])}</dd>'
            f'<dt>本地证据</dt><dd class="addr">{esc(ev) or "—"}</dd>'
            f'<dt>本地规模</dt><dd class="addr">{esc(loc) or "—"}</dd>'
            f'{arch}{up}{acq_txt}'
            f'<dt>许可</dt><dd>{esc(s["site_license"])}（{s["tier"]}）—— {esc(s["license_note"])}</dd>'
            f'<dt>核验</dt><dd>{esc(s["verified_on"])}'
            + (f' · 下次复核不晚于 {esc(s["next_review_due"])}' if s.get('next_review_due') else '') + '</dd>'
            '</dl></div></div>')
    rules = ('<div class="panel"><div class="panel-bd">'
             '<p><b>三条规则</b></p>'
             '<p>① <b>地址唯一且真实</b>——每个来源只登记一个地址，等于我们实际取得数据的位置；'
             '不写泛泛的站点首页，不写凭印象猜的官网，更不写与数据无关的站点。</p>'
             '<p>② <b>档位必须与数据一致</b>——C1 可商用 / C2 非商用 / C3 学习研究，逐曲写入目录的 <code>z</code> 字段；'
             '来源页标注与数据不一致即视为缺陷。</p>'
             '<p>③ <b>可复核</b>——每条地址都有本地证据（数据自述 / 采集台账 / 校验值）与核验日期，'
             '并附可执行的复核脚本；校验值分三级，本地快照绝不冒充上游官方值。</p>'
             '</div></div>')
    disc_zh = ('台账设 180 天复核周期：到期时复核脚本会给出提醒，届时重新核验各地址（含整包哈希与可达性），'
               '并把新日期追加进时间线。「永久可复核」的含义是：不是核验一次就永远成立，'
               '而是永远有一条可复跑的核验路径加一个到期提醒。<br>'
               '改任何来源地址前，必须先取得证据再改；拿不到证据就不要改，也不要写。')
    disc_en = ('The ledger runs on a 180-day review cycle: when due, the verifier raises a reminder and every '
               'address is re-checked (package hashes and reachability), with the new date appended to the timeline. '
               '"Permanently verifiable" means there is always a re-runnable verification path plus a due reminder, '
               'not that a single check holds forever.<br>'
               'Never change a source address without evidence first — if there is no evidence, do not change it.')
    html = (PAGE_TPL
            .replace('__RULES__', rules)
            .replace('__COUNT__', f'{len(S)} 个来源 · 合计 {sum(x["count"] for x in S):,} 首 · 核验 {reg["verified_on"]}')
            .replace('__TABLE__', ''.join(rows))
            .replace('__CARDS__', ''.join(cards))
            .replace('__DISC_ZH__', disc_zh).replace('__DISC_EN__', disc_en)
            .replace('__FNAME__', esc(foot_lic or f'ver {reg["verified_on"]}'))
            .replace('__FOOTNOTE__', esc(foot_note or '台正本为中文，English summary 见数据仓 docs/PROVENANCE.md'))
            .replace('__FOOTLEGAL__', esc(foot_legal or '代码 MIT · 元数据 CC BY 4.0 · 素材依各来源许可')))
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(html, encoding='utf-8')


# ─────────────────────────── 生成文档 ───────────────────────────
def render_text(reg: dict) -> str:
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
            ((f'`{e["path"]}`' if e.get('path') else e.get('note', '另有留存'))
             + (f'（含 `{e["contains"]}`）' if e.get('contains') else ''))
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
        acq = s.get('acquired') or {}
        if acq.get('date'):
            L.append(f'- **取得时点**：{acq["date"]}（依据：{acq.get("basis","?")}'
                     + (f' · {acq.get("evidence")}' if acq.get('evidence') else '') + '）')
        L.append(f'- **复核时间线**：核验于 {s["verified_on"]}'
                 + (f'；下次复核不晚于 {s["next_review_due"]}' if s.get('next_review_due') else ''))
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
    L.append('## 五、复核周期')
    L.append('')
    L.append('台账设**180 天复核周期**：`next_review_due` 到期时，`tools/provenance.py` 会给出提醒，')
    L.append('届时重新核验各地址（重跑 `--hash` / `--online`），并把新日期追加进 `reverified`、顺延 `next_review_due`。')
    L.append('「永久可复核」的含义是：**不是核验一次就永远成立，而是永远有一条可复跑的核验路径 + 一个到期提醒。**')
    L.append('')
    L.append('## 六、变更纪律')
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
    return '\n'.join(L) + '\n'


def render(reg: dict, out_md: Path) -> None:
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text(render_text(reg), encoding='utf-8')


def main(argv):
    ap = argparse.ArgumentParser(description='来源台账复核 / 文档生成')
    ap.add_argument('--root', help='数据工作副本（含 sources/ 与 release/site-repo/）')
    ap.add_argument('--registry', help='台账 JSON 路径（默认 <root>/docs/provenance.json）')
    ap.add_argument('--hash', action='store_true', help='复核整包 MD5 与字节数')
    ap.add_argument('--online', action='store_true', help='探测各地址当前可达性')
    ap.add_argument('--render', action='store_true', help='生成 docs/PROVENANCE.md')
    ap.add_argument('--mirror', help='--render 时同时写入的另一目录（如数据仓 docs/）')
    ap.add_argument('--page', help='生成站内台账页（如 release/site-repo/provenance.html）')
    # ⚠️ 顺序约束：`render_page()` 会用本文件的模板**整页重写**目标文件，
    #    因此**必须**在它之后再跑 tools/_apply_site_shell.py（页头/页脚/SEO 注入），
    #    否则统一外壳会被冲掉（本地 e2e【12】会拦下，别忽略）。
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
        dests = [reg_path.parent / 'PROVENANCE.md']
        if args.mirror:
            dests.append(Path(args.mirror) / 'PROVENANCE.md')
        for dest in dests:
            render(reg, dest)
            print('已生成', dest, f'({dest.stat().st_size/1024:.1f}KB)')
        if args.page:
            page = (root / args.page) if root else Path(args.page)
            render_page(reg, page)
            print('已生成站内页', page, f'({page.stat().st_size/1024:.1f}KB)')

            # ⚠️ render_page 会用本文件的模板**整页重写**目标文件，会冲掉统一页头/页脚/SEO。
            #    因此渲染完成后**自动补跑**外壳注入器，避免「忘了顺序」造成线上掉外壳
            #    （本地 e2e 的「统一外壳」断言会拦下）。
            _shells = sorted((ROOT_DIR / 'tools').glob('*site_shell*.py'))
            if _shells:
                import subprocess as _sp
                _r = _sp.run([sys.executable, str(_shells[0])], capture_output=True, text=True)
                if _r.returncode == 0:
                    print('  已自动重注入统一外壳（页头/页脚/SEO）')
                else:
                    print('  ⚠ 外壳注入器执行失败（页头/页脚/SEO 未注入），请检查该工具是否可运行')
                    print((_r.stdout or '')[-400:] + (_r.stderr or '')[-400:])
        return 0

    return verify(reg, root, args.hash, args.online, reg_path)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
