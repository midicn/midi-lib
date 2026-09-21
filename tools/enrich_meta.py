#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""全库元数据富化 · Phase 1（本地可执行项）

覆盖五个来源的定向修复，写入 midi_db/tracks/*.jsonl（先备份）：
  1. lakh      —— 从 src_path 目录解析作曲家（人名目录/前缀规律）+ 标题清洗 + 时期推断
  2. essen     —— region 编码清洗（ÿ 坏字节 / 音调数字拼音 / 少量 mojibake / 垃圾值置空）
  3. norbeck   —— 「爱尔兰/瑞士」→「爱尔兰」（hn*.abc 为 Henrik Norbeck 爱尔兰曲集）
  4. thesession / nottingham —— region 宽泛值置空（逐曲不可证，遵循"不知道就空"）
  5. giantmidi —— 上游 composers_manually_checked.csv 补国籍/生卒 → 重算时期（仅填空，不覆盖）

用法：
  python tools/enrich_meta.py --dry-run     # 只出报告
  python tools/enrich_meta.py               # 备份后写回
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import time
import urllib.request
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACKS = ROOT / "midi_db" / "tracks"
BACKUP = ROOT / "midi_db" / "tracks_backup"

# 作曲家 → 生卒（用于时期推断；与 infer_period.py 同源口径的子集）
Y = {
    "bach": (1685, 1750), "handel": (1685, 1759), "mozart": (1756, 1791),
    "beethoven": (1770, 1827), "haydn": (1732, 1809), "schubert": (1797, 1828),
    "schumann": (1810, 1856), "chopin": (1810, 1849), "liszt": (1811, 1886),
    "brahms": (1833, 1897), "mendelssohn": (1809, 1847), "schubertf": (1797, 1828),
    "telemann": (1681, 1767), "vivaldi": (1678, 1741), "corelli": (1653, 1713),
    "purcell": (1659, 1695), "scarlatti": (1685, 1757), "rachmaninoff": (1873, 1943),
    "rachmaninof": (1873, 1943), "satie": (1866, 1925), "debussy": (1862, 1918),
    "grieg": (1843, 1907), "tchaikovsky": (1840, 1893), "dvorak": (1841, 1904),
    "weber": (1786, 1826), "maykapar": (1867, 1938), "frank": (1822, 1890),
    "franck": (1822, 1890), "giuliani": (1781, 1829), "sorsa": (1929, 2016),
    "sor": (1778, 1839), "tarrega": (1852, 1909), "albeniz": (1860, 1909),
    "granados": (1867, 1916), "carcassi": (1792, 1853), "carcassi": (1792, 1853),
    "aguado": (1784, 1849), "legahn": None, "coste": (1806, 1883),
}
LAKH_PREFIX = {
    "bwv": ("Johann Sebastian Bach", "bach"),
    "mozk": ("Wolfgang Amadeus Mozart", "mozart"),
}


def slugify(s: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", (s or "").lower()).strip("-")
    return s or "unknown"


def period_from_years(y):
    try:
        y = int(str(y).strip())
    except Exception:
        return None
    if y < 1600: return "renaissance"
    if y < 1750: return "baroque"
    if y < 1820: return "classical"
    if y < 1900: return "romantic"
    if y < 1945: return "modern"
    return "contemporary"


def period_of_composer(slug: str):
    m = re.search(r"([a-z]+)$", slug or "")
    key = m.group(1) if m else ""
    y = Y.get(key)
    if not y:
        return None
    return period_from_years(y[1] or y[0])


# ── 1. lakh ────────────────────────────────────────────────────
LAKH_NAME_DIRS = {
    "bach": ("Johann Sebastian Bach", "bach"),
    "beethoven": ("Ludwig van Beethoven", "beethoven"),
    "mozart": ("Wolfgang Amadeus Mozart", "mozart"),
    "chopin": ("Frederic Chopin", "chopin"),
}
LAKH_DIR_MAP = {
    "bwv001- 400 chorales": ("Johann Sebastian Bach", "bach"),
}


def fix_lakh(r):
    sp = r.get("src_path") or ""
    parts = sp.split("/")
    d1 = parts[2] if len(parts) > 3 else ""      # parts[2] = sources/lakh/<一级目录>
    stem = Path(sp).stem
    changes = {}

    comp = r.get("composer_name")
    slug = r.get("composer_slug")
    if not comp or comp == "Traditional":
        m = re.match(r"^([A-Za-zÀ-ž' \-]+?),\s*([A-Za-zÀ-ž' \-]+?)$", d1)
        full = None
        if m and not any(ch.isdigit() for ch in d1):
            full = f"{m.group(2).strip()} {m.group(1).strip()}"
        else:
            key = d1.lower().strip()
            if key in LAKH_NAME_DIRS:
                full = LAKH_NAME_DIRS[key][0]
            elif key in LAKH_DIR_MAP:
                full = LAKH_DIR_MAP[key][0]
            else:
                low = stem.lower()
                for pre, (fn, sl) in LAKH_PREFIX.items():
                    if low.startswith(pre):
                        full = fn
                        break
        if full:
            changes["composer_name"] = full
            changes["composer_slug"] = slugify(full)

    # 标题清洗：下划线/连字符转空格、去尾部空白
    tt = re.sub(r"[_\-]+", " ", stem).strip()
    tt = re.sub(r"\s+", " ", tt)
    if tt and tt != (r.get("title") or "").strip():
        changes["title"] = tt

    # 时期：作曲家生卒推断（仅填空；Y 表 → giantmidi 官方 CSV 兜底）
    if not r.get("period"):
        sl = changes.get("composer_slug") or r.get("composer_slug")
        pr = period_of_composer(sl)
        if pr:
            changes["period"] = pr

    # genre（阶段 A）：已知古典作曲家 → classical；圣诞/颂歌目录 → christmas/hymn
    if not r.get("genre"):
        sl2 = changes.get("composer_slug") or slug or ""
        d1l = d1.lower()
        if "christmas" in d1l or "kerst" in d1l:
            changes["genre"] = "christmas"
        elif d1l == "hymns":
            changes["genre"] = "hymn"
        elif sl2 in Y and Y[sl2]:
            changes["genre"] = "classical"
        elif "classical" in d1l:
            changes["genre"] = "classical"
    return changes or None


# ── 2b. m21：时期 + 标题规范化 ─────────────────────────────────
M21_PERIOD = {
    "palestrina": "renaissance", "bach": "baroque", "monteverdi": "baroque",
    "beethoven": "classical", "anonymous (trecento, 14th c.)": "renaissance",
}
M21_NAME = {
    "Palestrina": "Giovanni Pierluigi da Palestrina",
    "Bach": "Johann Sebastian Bach",
    "Beethoven": "Ludwig van Beethoven",
    "Monteverdi": "Claudio Monteverdi",
}


def fix_m21(r):
    ch = {}
    cn = (r.get("composer_name") or "").strip()
    if not r.get("period"):
        p = M21_PERIOD.get(cn.lower())
        if p:
            ch["period"] = p
    if not r.get("period"):
        # Ryan's Mammoth Collection（19 世纪美国曲集，用户已审定 romantic）
        if "ryan" in cn.lower():
            ch["period"] = "romantic"
    tt = str(r.get("title") or "").strip()
    m = re.match(r"^bwv(\d+)\.(\d+)$", tt, re.I)
    if m:
        ch["title"] = f"Chorale BWV {m.group(1)}/{m.group(2)}"
    if cn in M21_NAME:
        ch["composer_name"] = M21_NAME[cn]
        ch["composer_slug"] = slugify(M21_NAME[cn])
    return ch or None


# ── 2c. openscore：作曲家生卒推断 ──────────────────────────────
OPENSCORE_Y = {
    "schubert": (1797, 1828), "arne": (1710, 1778), "faisst": (1838, 1892),
    "clementi": (1752, 1832), "dussek": (1760, 1812), "hummel": (1778, 1837),
    "beethoven": (1770, 1827), "mozart": (1756, 1791),
    "haydn": (1732, 1809), "bach": (1685, 1750), "handel": (1685, 1759),
    "brahms": (1833, 1897), "schumann": (1810, 1856), "chopin": (1810, 1849),
    "liszt": (1811, 1886), "mendelssohn": (1809, 1847), "grieg": (1843, 1907),
    "tchaikovsky": (1840, 1893), "ravel": (1875, 1937), "debussy": (1862, 1918),
    "satie": (1866, 1925), "scarlatti": (1685, 1757), "purcell": (1659, 1695),
    # openscore 缺时期的高频作曲家（OpenScore Lieder Corpus，多为 19 世纪德奥艺术歌曲）
    "holms": (1856, 1923), "franz": (1815, 1892), "kinkel": (1817, 1863),
    "reichardt": (1752, 1823), "lehmann": (1814, 1861), "cornelius": (1824, 1874),
    "wolf": (1860, 1903), "schrter": (1750, 1802), "warlock": (1894, 1930),
    "viardot": (1821, 1910), "faur": (1845, 1924), "faure": (1845, 1924),
    "stanford": (1852, 1924), "kralik": (1853, 1911), "jall": (1844, 1927),
    "henschel": (1850, 1934), "jensen": (1837, 1879), "gade": (1817, 1890),
    "rheinberger": (1839, 1901), "gress": None, "brandes": (1846, 1928),
    "lachner": (1803, 1890), "taubert": (1811, 1891), "abt": (1819, 1885),
    "rubinstein": (1829, 1894), "scharwenka": (1850, 1924), "nesler": None,
    "rntgen": (1858, 1932), "berger": (1862, 1948), "somervell": (1863, 1937),
}


def fix_openscore(r):
    if r.get("period"):
        return None
    slug = r.get("composer_slug") or ""
    key = re.search(r"([a-z]+)$", slug)
    y = OPENSCORE_Y.get(key.group(1)) if key else None
    if y:
        p = period_from_years(y[1] or y[0])
        if p:
            return {"period": p}
    return None


# ── 2d. cyberhymnal：tune_year 透出到顶层 yr ───────────────────
def fix_cyberhymnal(r):
    ex = r.get("extra") or {}
    ty = ex.get("tune_year")
    if ty and not r.get("yr"):
        return {"yr": int(ty)}
    return None


# ── 3. musicnet：官方 metadata.csv（Zenodo 5120004） ───────────
def load_musicnet_csv():
    p = ROOT / "sources/musicnet/musicnet_metadata.csv"
    if not p.exists():
        return {}
    import csv as _csv
    out = {}
    for row in _csv.DictReader(p.open(encoding="utf-8", newline="")):
        rid = str(row.get("id") or "").strip()
        if rid:
            out[rid] = row
    print(f"[mn] musicnet_metadata.csv 载入 {len(out)} 行")
    return out


def fix_musicnet(r, mn):
    if not mn:
        return None
    m = re.search(r"(\d{3,4})_", r.get("src_path") or "")
    if not m:
        return None
    row = mn.get(m.group(1))
    if not row:
        return None
    ch = {}
    comp = (row.get("composer") or "").strip()
    work = (row.get("composition") or "").strip()
    mov = (row.get("movement") or "").strip()
    cat = (row.get("catalog_name") or "").strip()
    ens = (row.get("ensemble") or "").strip()
    if comp and r.get("composer_name") != comp:
        ch["composer_name"] = comp
        ch["composer_slug"] = slugify(comp)
    if work:
        tt = work + (f" · {mov}" if mov else "")
        if tt != (r.get("title") or "").strip():
            ch["title"] = tt
    if cat and cat.upper() not in ("", "NONE") and not r.get("opus"):
        ch["opus"] = cat
    if ens:
        el = ens.lower()
        inst = ("voice_piano" if ("voice" in el and "piano" in el)
                else "voice" if "voice" in el or "song" in el or "opera" in el
                else "piano" if "piano" in el
                else "ensemble")
        if r.get("instrument") != inst:
            ch["instrument"] = inst
    if not r.get("period"):
        p = period_of_composer(slugify(comp))
        if p:
            ch["period"] = p
    return ch or None


# ── 4. mutopia：.ly 头文件（已缓存 _headers/{Init}/{Work}.ly） ─
def ly_header_fields(txt):
    i = txt.find(r"\header")
    if i < 0:
        return {}
    body = txt[i:txt.find("}", i)]
    fields = {}
    for line in body.splitlines():
        m = re.match(r'\s*(\w+)\s*=\s*"(.*)"\s*$', line)
        if m:
            fields[m.group(1)] = m.group(2).strip()
    return fields


def fix_mutopia(r, headers_exist):
    sp = r.get("src_path") or ""
    m = re.match(r"sources/mutopia/([^/]+)/([^/]+)/", sp)
    if not m or not headers_exist:
        return None
    hf = ROOT / "sources/mutopia/_headers" / m.group(1) / f"{m.group(2)}.ly"
    if not hf.exists() or hf.stat().st_size < 50:
        return None
    f = ly_header_fields(hf.read_text(encoding="utf-8", errors="replace"))
    if not f:
        return None
    ch = {}
    tt = f.get("title") or f.get("mutopiatitle")
    if tt and tt != (r.get("title") or "").strip():
        ch["title"] = tt
    comp = f.get("composer") or ""
    cm = re.match(r"^(.*?)\s*\((\d{4})\s*[-–]\s*(\d{4})\)", comp)
    if cm:
        ch["composer_name"] = cm.group(1).strip()
        ch["composer_slug"] = slugify(cm.group(1))
        if not r.get("period"):
            p = period_from_years(cm.group(3) or cm.group(2))
            if p:
                ch["period"] = p
        if not r.get("yr"):
            ch["yr"] = int(cm.group(2))
    elif comp and comp != r.get("composer_name"):
        ch["composer_name"] = comp
        ch["composer_slug"] = slugify(comp)
    op = (f.get("opus") or f.get("mutopiaopus") or "").strip()
    if op and op.upper() not in ("", "NONE", " ") and op != r.get("opus"):
        ch["opus"] = op
    ins = (f.get("instrument") or f.get("mutopiainstrument") or "").strip()
    if ins:
        il = ins.lower()
        inst = ("voice_piano" if ("voice" in il and "piano" in il)
                else "voice" if "voice" in il or "song" in il
                else "piano" if "piano solo" in il or il == "piano"
                else "guitar" if "guitar" in il
                else "melody" if "melody" in il
                else r.get("instrument"))
        if inst and inst != r.get("instrument"):
            ch["instrument"] = inst
    yr = (f.get("date") or f.get("mutopiadate") or "").strip()
    ym = re.search(r"(\d{4})", yr)
    if ym and not r.get("yr"):
        ch["yr"] = int(ym.group(1))
    if not r.get("period"):
        sl = ch.get("composer_slug") or r.get("composer_slug")
        p = period_of_composer(sl) if sl else None
        if p:
            ch["period"] = p
    return ch or None


# ── 5. abcmisc：本地 5 个 .abc 头重解析（T:/C:/R:） ────────────
def load_abc_index():
    """(file, title_lower) -> {C:, R:}（按 X: 块收集，C:/R: 常在 T: 之后）"""
    d = ROOT / "sources/abc-misc"
    if not d.exists():
        return {}
    idx = {}
    for f in sorted(d.glob("*.abc")):
        blocks = []
        cur = {}
        for line in f.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.rstrip()
            if len(line) >= 2 and line[1:2] == ":":
                k, v = line[:2], line[2:].strip()
                if k == "X:":
                    if cur.get("title"):
                        blocks.append(cur)
                    cur = {}
                elif k == "T:" and v and "title" not in cur:
                    cur["title"] = v
                elif k == "C:" and v:
                    cur.setdefault("c", v)
                elif k == "R:" and v:
                    cur.setdefault("r", v)
        if cur.get("title"):
            blocks.append(cur)
        for b in blocks:
            if b.get("c") or b.get("r"):
                idx.setdefault((f.name.lower(), b["title"].strip().lower()),
                               {"c": b.get("c"), "r": b.get("r")})
    print(f"[abc] abc-misc 索引 {len(idx):,} 首（含 C:/R: 者）")
    return idx


def fix_abcmisc(r, abcidx):
    sp = (r.get("src_path") or "").lower()
    fname = sp.split("/")[-1]
    key = (fname, str(r.get("title") or "").strip().lower())
    hit = abcidx.get(key)
    if not hit:
        return None
    ch = {}
    c = (hit.get("c") or "").strip()
    if c and (not r.get("composer_name") or r.get("composer_name") == "Traditional"):
        ch["composer_name"] = c
        ch["composer_slug"] = slugify(c)
    rr = (hit.get("r") or "").strip()
    if rr and not r.get("form"):
        ch["form"] = rr
    return ch or None


# ── 2. essen ───────────────────────────────────────────────────
ESS_JUNK = {"komposition", "ort", "???", "diqu", "osten", "westen", "nord", "innere)", "ostteil"}
ESS_FIX = {
    "Si4chua1n": "Sichuan", "Sha1nxi1": "Shanxi", "S\x81d)": "Süden)", "S\x81den)": "Süden)",
    "S\x81": "Sü", "Jianxi": "Jiangxi", "Zibuo": "Zibo", "Yngshan": "Yingshan",
    "Geixian": "Hexian", "Jongding": "Yongding", "Liaochen": "Liaocheng",
}


def clean_form_value(v):
    if not v:
        return None
    s = str(v).strip().rstrip("]").rstrip(";").strip()
    s = re.sub(r"\s*\]\s*$", "", s).strip()
    return s or None


def fix_form_junk(r):
    v = r.get("form")
    if not v:
        return None
    c = clean_form_value(v)
    if c and c != str(v).strip():
        return {"form": c}
    return None


def fix_essen(r, canon=None):
    v = r.get("region")
    if v is None:
        return None
    s = str(v).strip()
    s2 = s.replace("ÿ", "")
    s2 = ESS_FIX.get(s2, s2)
    if s2.lower() in ESS_JUNK:
        return {"region": None}
    # 碎片清理：尾分号/尾问号/未配对右括号
    s2 = s2.rstrip(";").rstrip("?").strip()
    if s2.endswith(")") and s2.count(")") > s2.count("("):
        s2 = s2[:-1].rstrip()
    # 大小写归并（同级变体取最高频写法）
    if canon:
        s2 = canon.get(s2.lower(), s2)
    if s2 != s:
        return {"region": s2}
    return None


# ── 3. norbeck ─────────────────────────────────────────────────
def fix_norbeck(r):
    if r.get("region") == "爱尔兰/瑞士" and "/hn" in (r.get("src_path") or ""):
        return {"region": "爱尔兰"}
    return None


# ── 4. thesession / nottingham：宽泛值置空 ─────────────────────
def fix_blanket(r):
    if r.get("region"):
        return {"region": None}
    return None


# ── 5. giantmidi：上游 CSV 补国籍/生卒（仅填空） ───────────────
GM_CSV = "https://raw.githubusercontent.com/bytedance/GiantMIDI-Piano/master/resources/composers_manually_checked.csv"


def load_gm_csv():
    try:
        req = urllib.request.Request(GM_CSV, headers={"User-Agent": "midicn"})
        txt = urllib.request.urlopen(req, timeout=60).read().decode("utf-8", "replace")
    except Exception as e:
        print(f"[gm] CSV 下载失败（跳过）：{e}")
        return {}, {}
    import csv, io
    by_full, by_surname = {}, {}
    for row in csv.reader(io.StringIO(txt), delimiter="\t"):
        if not row or not row[0].strip():
            continue
        cells = [c.strip() for c in row]
        if cells[0].lower() == "composer_name":
            continue
        name = cells[0]
        nat = cells[1] if len(cells) > 1 else ""
        birth = cells[2] if len(cells) > 2 else ""
        death = cells[3] if len(cells) > 3 else ""
        rec = {"name": name, "nat": nat, "birth": birth, "death": death}
        by_full[name.lower()] = rec
        sur = name.split()[-1].lower() if name.split() else ""
        if sur and sur not in by_surname:      # 首见优先，避免同名冲突
            by_surname[sur] = rec
    print(f"[gm] composers CSV 载入 {len(by_full):,} 行（姓氏索引 {len(by_surname):,}）")
    return by_full, by_surname


def fix_giantmidi(r, gm):
    if r.get("region") and r.get("period"):
        return None
    by_full, by_surname = gm
    name = (r.get("composer_name") or "").strip()
    sur = name.split()[-1].lower() if name.split() else ""
    rec = by_full.get(name.lower()) or by_surname.get(sur)
    if not rec:
        return None
    ch = {}
    nat = rec["nat"] if rec["nat"].lower() != "unknown" else ""
    birth = rec["birth"] if str(rec["birth"]).isdigit() else None
    death = rec["death"] if str(rec["death"]).isdigit() else None
    # 作曲家全名（上游缩写 → 官方全名）
    if rec["name"] and rec["name"] != name and len(rec["name"]) > len(name):
        ch["composer_name"] = rec["name"]
        ch["composer_slug"] = slugify(rec["name"])
    if not r.get("region") and nat:
        ch["region"] = nat
    if not r.get("period"):
        p = period_from_years(death or birth)
        if p:
            ch["period"] = p
    if ch:
        ex2 = dict(r.get("extra") or {})
        ex2.setdefault("birth", int(birth) if birth else None)
        ex2.setdefault("death", int(death) if death else None)
        ch["extra"] = ex2
    return ch or None


def period_from_years(y):
    try:
        y = int(str(y).strip())
    except Exception:
        return None
    if y < 1600: return "renaissance"
    if y < 1750: return "baroque"
    if y < 1820: return "classical"
    if y < 1900: return "romantic"
    if y < 1945: return "modern"
    return "contemporary"



def period_via_csv(slug: str, by_surname: dict):
    """用 giantmidi 官方作曲家表（姓氏索引）补时期。"""
    key = re.sub(r"[^a-z]", "", (slug or "").lower())
    rec = by_surname.get(key)
    if not rec:
        return None
    death = rec["death"] if str(rec["death"]).isdigit() else None
    birth = rec["birth"] if str(rec["birth"]).isdigit() else None
    return period_from_years(death or birth)


# ── 6. aria：上游 difficulty + 时期交叉补全 ────────────────────
def load_aria_meta():
    p = ROOT / "sources/ariamidi/metadata.json"
    if not p.exists():
        return {}
    return json.loads(p.read_text(encoding="utf-8"))


def fix_aria(r, ameta, by_surname):
    ch = {}
    if not r.get("diff"):
        fid = (r.get("id") or "").split("-")[-1].lstrip("0")
        ent = ameta.get(fid) or ameta.get(str(int(fid)) if fid.isdigit() else fid)
        if ent:
            d = (ent.get("metadata") or {}).get("difficulty")
            if d:
                ch["diff"] = d
    if not r.get("period"):
        p2 = period_of_composer(r.get("composer_slug") or "") or period_via_csv(r.get("composer_slug"), by_surname)
        if p2:
            ch["period"] = p2
    return ch or None



# ── 7. 作曲家身份归并（人工甄别，仅高置信同人变体） ─────────────
# 注意：不做相似度自动合并——bach/beach、weber/webern、wolf/wolff、szymanowski/szymanowska、
# drummer1..10 都是不同的人/角色，自动合并会造成严重错误。
COMPOSER_MERGE = {
    "cherny": "czerny", "czerny-c": "czerny", "czerney": "czerny", "cerny": "czerny", "czerni": "czerny",
    "list": "liszt", "f-liszt": "liszt", "franz-liszt": "liszt",
    "skriabin": "scriabin", "liadov": "lyadov", "prokofieff": "prokofiev",
    "prokofjew": "prokofiev", "prokofjev": "prokofiev",
    "faur": "faure", "burgmueller": "burgmuller", "brugmuller": "burgmuller",
    "metner": "medtner", "gretchaninoff": "grechaninov", "gretchaninow": "grechaninov",
    "gedike": "goedicke", "glier": "gliere", "o-halloran": "ohalloran",
    "majkapar": "maykapar", "maikapar": "maykapar",
    "loeschhorn": "loschhorn", "grndahl": "grondahl",
    "rakhmaninov": "rachmaninoff", "rahmaninov": "rachmaninoff",
    "george-frideric-handel": "handel", "georg-friedrich-h-ndel": "handel",
    "fr-d-ric-chopin": "chopin", "frederic-chopin": "chopin", "f-chopin": "chopin",
    "shubert": "schubert", "schuman": "schumann", "shumann": "schumann", "shuman": "schumann",
    "hayden": "haydn", "m-haydn": "haydn", "cherny-c": "czerny",
    "tschaikowski": "tchaikovsky", "tchaikovski": "tchaikovsky", "chaikovsky": "tchaikovsky",
    "moshkovsky": "moszkowski", "moszkowsky": "moszkowski",
    "kabalewski": "kabalevsky", "kabalevski": "kabalevsky",
    "kulau": "kuhlau", "greig": "grieg", "dusik": "dussek",
    "meraux": "mereaux", "sains-saens": "saint-saens",
    "mozar": "mozart", "moart": "mozart", "shopin": "chopin",
    "skarlatti": "scarlatti", "d-scarlatti": "scarlatti",
    "sati": "satie", "beach": "beach",  # 保留 beach（Amy Beach 是独立作曲家）
}


def fix_composer_alias(r):
    slug = (r.get("composer_slug") or "").strip()
    canon = COMPOSER_MERGE.get(slug)
    if canon and canon != slug:
        return {"composer_slug": canon}
    return None



# ── 8. 由地域推国家（三源；仅高置信映射，流派值不硬套国家） ─────
# abcmisc 的 region 混着流派（克莱兹梅尔/klezmer/Hassidic）与宏观地区（巴尔干），
# 这些**不**分配国家；只有明确的国家值才映射。
ABCMISC_COUNTRY = {
    "israel": "以色列", "以色列": "以色列", "bulgaria": "保加利亚", "serbia": "塞尔维亚",
    "romania": "罗马尼亚", "macedonia": "北马其顿", "greece": "希腊", "croatia": "克罗地亚",
    "armenia": "亚美尼亚", "hungary": "匈牙利", "russia": "俄罗斯", "turkey": "土耳其",
    "albania": "阿尔巴尼亚", "德国": "德国", "ukraine": "乌克兰", "波兰": "波兰",
    "transylvania": "罗马尼亚", "moldova": "摩尔多瓦", "bosnia": "波斯尼亚和黑塞哥维那",
}
# norbeck：爱尔兰曲集 + 瑞典省份 + 各地曲集
NORBECK_COUNTRY = {
    "ireland": "爱尔兰", "irish": "爱尔兰", "scotland": "英国", "scottish": "英国",
    "shetland": "英国", "england": "英国", "bretagne": "法国", "france": "法国",
    "quebec": "加拿大", "american": "美国", "bulgaria": "保加利亚", "sweden": "瑞典",
    "norway": "挪威", "denmark": "丹麦", "spain": "西班牙", "italy": "意大利",
    "finland": "芬兰", "estonia": "爱沙尼亚", "hungary": "匈牙利", "romania": "罗马尼亚",
}
NORBECK_SE = {"ostergotland", "smaland", "dalarna", "skane", "halsingland", "sormland",
              "gotland", "uppland", "varmland", "vastmanland", "narke", "vastmanland",
              "gastrikland", "harmedal", "jam­tland", "bohuslan", "harjedalen"}


def _norm_region(v):
    """清掉 LaTeX 残码与花括号：\\"Osterg\\"otland → ostergotland"""
    t = str(v or "").replace("\\", "").replace("\"", "").replace("{", "").replace("}", "")
    t = t.replace("å", "a").replace("ä", "a").replace("ö", "o").replace("ø", "o")
    t = re.sub(r"\s+", " ", t).strip().lower()
    return t


def fix_country_from_region(r):
    """chinafolk / abcmisc / norbeck：由地域推国家（仅高置信）。"""
    src = r.get("source")
    cur = r.get("country")
    reg = r.get("region")
    if not reg:
        return None
    ch = {}
    if src == "chinafolk":
        if not cur:
            ch["country"] = "中国"
    elif src == "abcmisc":
        c = ABCMISC_COUNTRY.get(_norm_region(reg)) or ABCMISC_COUNTRY.get(str(reg).strip())
        if c and not cur:
            ch["country"] = c
    elif src == "norbeck":
        key = _norm_region(reg)
        if key in NORBECK_SE or key in ("sweden",):
            c = "瑞典"
        elif key.startswith("ireland") or key.startswith("爱尔兰"):
            c = "爱尔兰"
        else:
            c = NORBECK_COUNTRY.get(key)
        if c and not cur:
            ch["country"] = c
    # norbeck region 残码在源 jsonl 里清洗一次（站点原本在分片层清）
    if src == "norbeck" and reg and ("\\" in str(reg) or "{" in str(reg) or "\"" in str(reg)):
        cleaned = str(reg).replace("\\", "").replace("\"", "")
        cleaned = cleaned.replace("{", "").replace("}", "").strip()
        if cleaned and cleaned != reg:
            ch["region"] = cleaned
    return ch or None



# ── 9. 作曲家 slug 规范化（全名式 → 短式，消除身份碎片） ────────
# v1.8 的 lakh fixer 曾把 slug 写成 slugify(full name) → "wolfgang-amadeus-mozart"，
# 与全库其它源的 "mozart" 分裂成两个身份。这里统一为短式（取姓氏段，且必须是库内已存在的规范 slug）。
def build_canonical_slugs(rows_by_src):
    """库内「短式」规范 slug 集合：不带连字符的多段全名式一律不算。"""
    canon = Counter()
    for src, rows in rows_by_src.items():
        for r in rows:
            sl = (r.get("composer_slug") or "").strip()
            if sl and sl.count("-") <= 1:
                canon[sl] += 1
    return set(canon)


def fix_slug_normalize(r, canon):
    sl = (r.get("composer_slug") or "").strip()
    if not sl or sl.count("-") < 2:
        return None
    parts = sl.split("-")
    for cand in ("-".join(parts[1:]), parts[-1], "-".join(parts[-2:])):
        if cand in canon:
            return {"composer_slug": cand}
    return None


# ── 主流程 ────────────────────────────────────────────────────
def out_get_rows(f):
    return [json.loads(l) for l in f.open(encoding='utf-8')]


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv[1:])

    gm = ({}, {})
    files = {f.stem: f for f in sorted(TRACKS.glob("*.jsonl"))}
    if "giantmidi" in files:
        gm = load_gm_csv()
    mn = load_musicnet_csv() if "musicnet" in files else {}
    abcidx = load_abc_index() if "abcmisc" in files else {}
    ameta = load_aria_meta() if "aria" in files else {}
    _, gm_by_surname = gm if isinstance(gm, tuple) else ({}, {})
    # 规范 slug 集（用于全名式 slug 归一）
    rows_by_src = {}
    for _n, _f in files.items():
        rows_by_src[_n] = [json.loads(l) for l in _f.open(encoding="utf-8")]
    canon_slugs = build_canonical_slugs(rows_by_src)
    print(f"[slug] 规范化 slug 集 {len(canon_slugs):,}")
    essen_canon = None
    if "essen" in files:
        from collections import Counter as _C
        _cnt = {}
        for _r in out_get_rows(files["essen"]):
            v = _r.get("region")
            if v:
                _cnt.setdefault(str(v).strip().lower(), _C())[str(v).strip()] += 1
        essen_canon = {k: c.most_common(1)[0][0] for k, c in _cnt.items()}
        print(f"[essen] 地域值 {len(essen_canon):,} 个（大小写归并后）")

    report = {}
    out_lines = {}
    for name, f in files.items():
        rows = [json.loads(l) for l in f.open(encoding="utf-8")]
        fixer = {
            "lakh": fix_lakh, "essen": fix_essen, "norbeck": fix_norbeck,
            "thesession": fix_blanket, "nottingham": fix_blanket,
            "m21": fix_m21, "openscore": fix_openscore, "cyberhymnal": fix_cyberhymnal,
        }.get(name)
        changed = 0
        kinds = Counter()
        new_rows = []
        for r in rows:
            ch = None
            if name == "essen":
                ch = fix_essen(r, essen_canon)
            elif fixer:
                ch = fixer(r)
            elif name == "giantmidi":
                ch = fix_giantmidi(r, gm)
            elif name == "musicnet":
                ch = fix_musicnet(r, mn)
            elif name == "mutopia":
                ch = fix_mutopia(r, True)
            elif name == "abcmisc":
                ch = fix_abcmisc(r, abcidx)
            elif name == "aria":
                ch = fix_aria(r, ameta, gm_by_surname)
            sn = fix_slug_normalize(r, canon_slugs)
            if sn:
                ch = dict(ch or {})
                ch.update(sn)
            cc = fix_country_from_region(r)
            if cc:
                ch = dict(ch or {})
                ch.update(cc)
            ca = fix_composer_alias(r)
            if ca:
                ch = dict(ch or {})
                ch.update(ca)
            if ch is None:
                ch = fix_form_junk(r)
            elif isinstance(ch, dict) and "form" not in ch:
                fj = fix_form_junk(r)
                if fj:
                    ch.update(fj)
            if ch:
                changed += 1
                for k in ch:
                    kinds[k] += 1
                r2 = dict(r)
                for k, v in ch.items():
                    r2[k] = v
                new_rows.append(r2)
            else:
                new_rows.append(r)
        report[name] = (len(rows), changed, dict(kinds))
        out_lines[name] = new_rows

    print()
    print("=== 富化报告 ===")
    gtotal_c = gtotal_n = 0
    for name in sorted(report):
        n, c, kinds = report[name]
        gtotal_c += c
        gtotal_n += n
        if c:
            print(f"  {name:12s} {n:>7,} 条 · 改动 {c:>7,} · 字段 {dict(kinds)}")
    print(f"  合计改动 {gtotal_c:,} / {gtotal_n:,}")

    if args.dry_run:
        print("\n[dry-run] 未写回。确认后去掉 --dry-run 执行。")
        return 0

    # 备份
    ts = time.strftime("%Y%m%d-%H%M%S")
    bdir = BACKUP / f"pre-enrich-{ts}"
    bdir.mkdir(parents=True, exist_ok=True)
    for f in files.values():
        shutil.copy2(f, bdir / f.name)
    print(f"\n[backup] 原始 jsonl → {bdir}")

    for name, rows in out_lines.items():
        with (TRACKS / f"{name}.jsonl").open("w", encoding="utf-8", newline="\n") as fh:
            for r in rows:
                fh.write(json.dumps(r, ensure_ascii=False, separators=(",", ":")) + "\n")
    print("[write] 已写回 jsonl（下一步：重建 release）")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
