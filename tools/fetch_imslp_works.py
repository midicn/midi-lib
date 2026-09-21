#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""IMSLP 作品目录抓取（HTML 分类页 + from= 续页）

API 的 categorymembers 只给前 500 且无续页令牌，改用分类页 HTML：
  https://imslp.org/wiki/Category:Liszt,_Franz
  → 每页约 230 个作品链接，页面含 "from=..." 可续页
按作曲家存 sources/imslp/{slug}.json（可续跑，已存则跳过）。

用法：python tools/fetch_imslp_works.py --min-tracks 50 [--max-pages 12]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARIA = ROOT / "midi_db/tracks/aria.jsonl"
OUT = ROOT / "sources/imslp"
UA = {"User-Agent": "midicn-lib/1.0 (open MIDI dataset; metadata cross-reference; https://lib.midicn.com)"}


def get(url: str, tries: int = 3):
    last = None
    for a in range(tries):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=90).read().decode("utf-8", "replace")
        except Exception as e:      # noqa: BLE001
            last = e
            time.sleep(2 + a * 2)
    print(f"    [失败] {last}", flush=True)
    return ""


def api(params: dict):
    url = "https://imslp.org/api.php?" + urllib.parse.urlencode(params)
    txt = get(url)
    try:
        return json.loads(txt)
    except Exception:
        return {}


def resolve_category(slug: str, full: str | None):
    """定位 IMSLP 分类名（Category:Last, First）。全名优先，再用搜索校正。"""
    cands = []
    if full:
        parts = [p for p in re.split(r"\s+", full.strip()) if p]
        if len(parts) >= 2:
            cands.append(f"Category:{parts[-1]}, {' '.join(parts[:-1])}")
    d = api({"action": "query", "list": "search", "srsearch": slug,
             "srnamespace": "14", "srlimit": "8", "format": "json"})
    for it in (d.get("query", {}).get("search") or []):
        t = it.get("title") or ""
        if t.lower().startswith(f"category:{slug.lower()},"):
            cands.append(t)
    seen = set()
    for c in cands:
        if c in seen:
            continue
        seen.add(c)
        html = get("https://imslp.org/wiki/" + urllib.parse.quote(c.replace(" ", "_")))
        if "/wiki/" in html and "does not exist" not in html[:4000]:
            # 优选作品数多的（粗略：链接数）
            n = len(set(re.findall(r"/wiki/([^\"#]+?\([^\"#]*?)\)\"", html)))
            if n >= 5:
                return c, n
    return None, 0


LINK_RE = re.compile(r'/wiki/([^"#]+?\([^"#]*?)\)"')


def resolve_redirect(cat: str):
    """分类可能是重定向；用 redirects=1 解析到真实分类名，并校验存在性。"""
    d = api({"action": "query", "titles": cat, "redirects": "1", "format": "json"})
    q = d.get("query", {}) or {}
    for rd in (q.get("redirects") or []):
        if (rd.get("from") or "").lower() == cat.lower():
            return rd.get("to") or cat
    for _, pg in (q.get("pages") or {}).items():
        if not pg.get("pageid") or pg.get("missing") is not None and pg.get("missing") is not False:
            if pg.get("missing"):
                return None
    return cat


def best_category(cands):
    """在若干候选分类里选成员最多的（避开子分类/局部分类）。"""
    best, best_n = None, -1
    for c in cands:
        if not c:
            continue
        rc = resolve_redirect(c)
        if not rc:
            continue
        n = len(fetch_members(rc))
        if n > best_n:
            best, best_n = rc, n
    return best


def fetch_members(cat: str, prefix: str | None = None):
    p = {"action": "query", "list": "categorymembers", "cmtitle": cat,
         "cmlimit": "500", "cmnamespace": "0", "format": "json"}
    if prefix:
        p["cmstartsortkeyprefix"] = prefix
    d = api(p)
    return [x.get("title") for x in ((d.get("query", {}) or {}).get("categorymembers") or [])]


def fetch_works(cat: str, _unused: int = 0):
    """抓取分类下全部作品标题。

    API 的 categorymembers 上限 500 且无续页令牌，但 **cmstartsortkeyprefix**
    可按字母前缀分段；仅在首次查询被截断时才做 26 字母扫描。
    """
    first = fetch_members(cat)
    works = set(first)
    if len(first) >= 500:
        for ch in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            works.update(fetch_members(cat, ch))
            time.sleep(0.5)
    return sorted(works)


# 拼写/别名 → IMSLP 分类名（官方全名可用时优先由 CSV 提供，这里补 CSV 缺失或写错的）
ALIAS_CAT = {
    "dvorak": "Dvořák, Antonín", "albeniz": "Albéniz, Isaac", "martinu": "Martinů, Bohuslav",
    "gliere": "Glière, Reinhold", "glier": "Glière, Reinhold", "kabalevsky": "Kabalevsky, Dmitry",
    "khachaturian": "Khachaturian, Aram", "ginastera": "Ginastera, Alberto",
    "pejacevic": "Pejačević, Dora", "saint-saens": "Saint-Saëns, Camille",
    "burgmueller": "Burgmüller, Friedrich", "burgmuller": "Burgmüller, Friedrich",
    "mereaux": "Méreaux, Jean-Amédée", "meraux": "Méreaux, Jean-Amédée",
    "zarebski": "Zarębski, Juliusz", "ciurlionis": "Čiurlionis, Mikalojus Konstantinas",
    "smetana": "Smetana, Bedřich", "fibich": "Fibich, Zdeněk", "vorisek": "Voříšek, Jan Václav",
    "janacek": "Janáček, Leoš", "novak": "Novák, Vítězslav", "suk": "Suk, Josef",
    "carreno": "Carreño, Teresa", "pierne": "Pierné, Gabriel", "grunfeld": "Grünfeld, Alfred",
    "grondahl": "Grøndahl, Agathe", "grndahl": "Grøndahl, Agathe",
    "loschhorn": "Löschhorn, Albert", "loeschhorn": "Löschhorn, Albert",
    "schutt": "Schütt, Eduard", "koelling": "Kölling, Carl", "takacs": "Takács, Jenő",
    "saygun": "Saygun, Ahmed Adnan", "say": "Say, Fazıl", "ligeti": "Ligeti, György",
    "silvestrov": "Silvestrov, Valentin", "muczynski": "Muczyński, Robert",
    "shchedrin": "Shchedrin, Rodion", "moshkovsky": "Moszkowski, Moritz",
    "moszkowski": "Moszkowski, Moritz", "gedike": "Goedicke, Alexander",
    "gretchaninoff": "Grechaninov, Aleksandr", "grechaninov": "Grechaninov, Aleksandr",
    "liadov": "Lyadov, Anatoly", "lyadov": "Lyadov, Anatoly",
    "skriabin": "Scriabin, Aleksandr", "scriabin": "Scriabin, Aleksandr",
    "rakhmaninov": "Rachmaninoff, Sergei", "rachmaninoff": "Rachmaninoff, Sergei",
    "chaminade": "Chaminade, Cécile", "faure": "Fauré, Gabriel",
    "turina": "Turina, Joaquín", "mompou": "Mompou, Federico",
    "vivaldi": "Vivaldi, Antonio", "soler": "Soler, Antonio",
}


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-tracks", type=int, default=50)
    ap.add_argument("--max-pages", type=int, default=12)
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args(argv[1:])

    rows = [json.loads(l) for l in ARIA.open(encoding="utf-8")]
    cnt = Counter(r.get("composer_slug") or "" for r in rows)
    # 官方作曲家全名（giantmidi CSV）
    # 官方作曲家全名：按「同姓氏出现次数最多的全名」定位（避免 Bach→August Wilhelm）
    import csv as _csv
    from collections import defaultdict as _dd
    votes = _dd(Counter)
    csvp = ROOT / "sources/giantmidi/extracted/GiantMIDI-PIano/metadata/full_music_pieces_youtube_similarity_pianosoloprob_split.csv"
    try:
        with csvp.open(encoding="utf-8", errors="replace") as fh:
            for row in _csv.DictReader(fh, delimiter="\t"):
                sn = (row.get("surname") or "").strip()
                fn = (row.get("firstname") or "").strip()
                if sn:
                    votes[sn.lower()][f"{fn} {sn}".strip()] += 1
        full_by_sur = {k: v.most_common(1)[0][0] for k, v in votes.items()}
        print(f"[imslp] 官方全名索引 {len(full_by_sur):,} 个姓氏", flush=True)
    except Exception as e:
        print(f"[imslp] CSV 读取失败: {e}", flush=True)
        full_by_sur = {}

    todo = [s for s, v in cnt.most_common() if v >= args.min_tracks and s]
    if args.limit:
        todo = todo[:args.limit]
    OUT.mkdir(parents=True, exist_ok=True)
    print(f"[imslp] 待抓 {len(todo)} 位作曲家（≥{args.min_tracks} 首）", flush=True)

    ok = skip = miss = 0
    for i, slug in enumerate(todo, 1):
        dest = OUT / f"{slug}.json"
        if dest.exists() and dest.stat().st_size > 30:
            skip += 1
            continue
        alias = ALIAS_CAT.get(slug)
        if alias:
            cat = best_category([alias, f"Category:{alias}" if not alias.startswith("Category:") else alias])
        else:
            cat, n0 = resolve_category(slug, full_by_sur.get(slug))
        if not cat:
            dest.write_text(json.dumps({"slug": slug, "category": None, "works": []}), encoding="utf-8")
            miss += 1
            print(f"  [{i}/{len(todo)}] {slug:20s} 未找到分类", flush=True)
            continue
        works = fetch_works(cat, args.max_pages)
        dest.write_text(json.dumps({"slug": slug, "category": cat, "works": works}, ensure_ascii=False), encoding="utf-8")
        ok += 1
        print(f"  [{i}/{len(todo)}] {slug:20s} {cat[9:44]:38s} {len(works):>4} 作品", flush=True)
        time.sleep(0.7)
    print(f"[imslp] 新抓 {ok} · 跳过 {skip} · 未找到 {miss}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
