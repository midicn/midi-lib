#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""essen 地理二级化 + 曲式补全（数据源：本地 ESAC ABC 的 O: / R: 字段）

- 国家：O: 若为层级（"Europa, Mitteleuropa, Deutschland"）取末段；若为单一地区
  （"Lothringen"）走地区→国家映射表；中国相关一律标 中国 / 中国台湾 等。
  未命中映射者留空（不猜）。
- 曲式：R: 首段清洗（ballade / romanze / xiaodiao / shange …），保留源语言原词。

用法：python tools/enrich_essen_geo.py [--dry-run]
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import time
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JSONL = ROOT / "midi_db" / "tracks" / "essen.jsonl"
ABC = ROOT / "sources" / "essen" / "esac"
BACKUP = ROOT / "midi_db" / "tracks_backup"

# ── 国家名（德语/英语 → 中文） ─────────────────────────────────
COUNTRY = {
    "deutschland": "德国", "germany": "德国", "nord - deutschland": "德国", "sueddeutschland": "德国",
    "niederdeutschland": "德国", "norddeutschland": "德国", "deutschland / niederlande": "德国",
    "oesterreich": "奥地利", "osterreich": "奥地利", "austria": "奥地利",
    "schweiz": "瑞士", "switzerland": "瑞士", "schweizland": "瑞士",
    "luxemburg": "卢森堡", "luxembourg": "卢森堡",
    "lothringen": "法国", "elsass": "法国", "frankreich": "法国", "france": "法国",
    "bretagne": "法国", "savoie": "法国", "faucigny": "法国", "jura": "法国", "sundgau": "法国",
    "polen": "波兰", "poland": "波兰", "galizien": "乌克兰", "posen": "波兰", "breslau": "波兰",
    "danzig": "波兰", "westpreussen": "波兰", "ostpreussen": "俄罗斯", "schlesien": "波兰",
    "oberschlesien": "波兰", "niederschlesien": "波兰", "sudetenschlesien": "捷克",
    "boehmen": "捷克", "bohmen": "捷克", "mahren": "捷克", "maehren": "捷克",
    "sudetenland": "捷克", "egerland": "捷克", "kuhlаendchen": "捷克", "kuhlaendchen": "捷克",
    "bessarabien": "摩尔多瓦", "zips": "斯洛伐克", "kremnitz": "斯洛伐克", "slowakei": "斯洛伐克",
    "gottschee": "斯洛文尼亚", "krain": "斯洛文尼亚", "slovenien": "斯洛文尼亚",
    "kroatien": "克罗地亚", "slawonien": "克罗地亚", "sotin": "克罗地亚", "zagorja": "克罗地亚",
    "siebenbuergen": "罗马尼亚", "rumaenien": "罗马尼亚", "banat": "罗马尼亚",
    "batschka": "塞尔维亚", "neusatz": "塞尔维亚", "jugoslawien": "塞尔维亚",
    "ungarn": "匈牙利", "hungary": "匈牙利", "tolnau": "匈牙利", "bataapati": "匈牙利",
    "dunakoemloed": "匈牙利", "solymar": "匈牙利", "nemetker": "匈牙利", "szakadat": "匈牙利",
    "wolga": "俄罗斯", "wolgakolonie": "俄罗斯", "wolgakolonien": "俄罗斯", "wolgagebiet": "俄罗斯",
    "russland": "俄罗斯", "russia": "俄罗斯", "samara": "俄罗斯", "kamenka": "俄罗斯",
    "ukraine": "乌克兰", "daenemark": "丹麦", "danmark": "丹麦", "vendsyssel": "丹麦",
    "schweden": "瑞典", "sweden": "瑞典", "norwegen": "挪威", "norway": "挪威",
    "niederlande": "荷兰", "holland": "荷兰", "brabant": "荷兰",
    "belgien": "比利时", "flandern": "比利时", "flaemisch": "比利时", "nevele": "比利时",
    "duynkerke": "荷兰", "italien": "意大利", "italy": "意大利", "sizilien": "意大利",
    "lombardei": "意大利", "meran": "意大利", "tirol": "奥地利",
    "spanien": "西班牙", "griechenland": "希腊", "england": "英国",
    "usa": "美国", "neuengland": "美国", "carolina": "美国",
    "saskatoon": "加拿大", "brasilien": "巴西", "mexiko": "墨西哥",
    "java": "印度尼西亚", "island": "冰岛", "faeroer": "法罗群岛",
    "japan": "日本", "indien": "印度", "israel": "以色列",
    "china": "中国", "taiwan": "中国台湾", "taiwan, china": "中国台湾",
    "ostasien": "中国", "asien": "中国",
    "mitteleuropa": "中欧", "europa": "欧洲", "baltikum": "波罗的海地区",
}

# ── 地区 → 国家（单段 O: 与末段为地区时用） ────────────────────
REGION = {
    # 德国
    "niederrhein": "德国", "westfalen": "德国", "rheinland": "德国", "rheinprovinz": "德国",
    "franken": "德国", "oberfranken": "德国", "unterfranken": "德国", "niederfranken": "德国",
    "schwaben": "德国", "thueringen": "德国", "brandenburg": "德国", "sachsen": "德国",
    "bayern": "德国", "oberbayern": "德国", "niederbayern": "德国", "rheinbayern": "德国",
    "darmstadt": "德国", "nassau": "德国", "odenwald": "德国", "wetterau": "德国",
    "siebengebirge": "德国", "spessart": "德国", "altmark": "德国", "uckermark": "德国",
    "wuerttemberg": "德国", "baden": "德国", "koeln": "德国", "paderborn": "德国",
    "dresden": "德国", "muenster": "德国", "westerwald": "德国", "oberwesterwald": "德国",
    "unterwesterwald": "德国", "dill - kreis": "德国", "dillkreis": "德国",
    "hildburghausen": "德国", "meurs": "德国", "bergisches land": "德国", "herzogtum berg": "德国",
    "weiler": "德国", "hambach": "德国", "stotternheim": "德国", "lichtenbach": "德国",
    "schleswig": "德国", "holstein": "德国", "schleswig - holstein": "德国",
    "rheinpfalz": "德国", "pfalz": "德国", "rhein": "德国", "mittelrhein": "德国",
    "rheinland-pfalz": "德国", "hessen": "德国", "oberhessen": "德国", "kurhessen": "德国",
    "kassel": "德国", "berlin": "德国", "pommern": "德国", "rugen": "德国", "ruegen": "德国",
    "mecklenburg": "德国", "lausitz": "德国", "oberlausitz": "德国", "niederlausitz": "德国",
    "harz": "德国", "eifel": "德国", "taunus": "德国", "hunsrueck": "德国",
    "bergstrasse": "德国", "hoerde": "德国", "barmen": "德国", "elberfeld": "德国",
    "solingen": "德国", "gummersbach": "德国", "attendorn": "德国", "wipperfuerth": "德国",
    "paffrath": "德国", "bensberg": "德国", "wiehl": "德国", "moers": "德国", "wesel": "德国",
    "kleve": "德国", "xanten": "德国", "soest": "德国", "bielefeld": "德国", "minden": "德国",
    "bielefeld": "德国", "herford": "德国", "pommern": "德国", "nordmark": "德国",
    # 奥地利
    "steiermark": "奥地利", "tirol": "奥地利", "salzburg": "奥地利", "kaernten": "奥地利",
    "wien": "奥地利", "burgenland": "奥地利", "niederoesterreich": "奥地利",
    "oberoesterreich": "奥地利", "traismauer": "奥地利", "illmitz": "奥地利",
    "pamhagen": "奥地利", "goggendorf": "奥地利", "waltdorf": "奥地利", "weitra": "奥地利",
    # 瑞士
    "bern": "瑞士", "zuerich": "瑞士", "aargau": "瑞士", "graubuenden": "瑞士",
    "wallis": "瑞士", "oberwallis": "瑞士", "appenzell": "瑞士", "emmental": "瑞士",
    "emmenthal": "瑞士", "entlebuch": "瑞士", "escholzmatt": "瑞士", "brienzwyler": "瑞士",
    "oberhaslithal": "瑞士", "oberhasel": "瑞士", "schleitheim": "瑞士", "chur": "瑞士",
    "wimmis": "瑞士", "oberterzen": "瑞士", "tenna": "瑞士", "portein": "瑞士",
    "vals": "瑞士", "zufikon": "瑞士", "basel": "瑞士", "aargau": "瑞士",
    # 法国 / 卢森堡
    "lothringen": "法国", "elsass": "法国", "sundgau": "法国", "rechicourt": "法国",
    "kerbach": "法国", "bousbach": "法国", "hellimer": "法国", "walschbronn": "法国",
    "loudrefing": "法国", "schneckenbusch": "法国",
    # 波兰（含华沙周边地名）
    "warszawy": "波兰", "grodziska": "波兰", "szarlatowo": "波兰", "chocholow": "波兰",
    "bielitz": "波兰", "gleiwitz": "波兰", "oppeln": "波兰", "glatz": "波兰",
    "liegnitz": "波兰", "glogau": "波兰", "fraustadt": "波兰", "kosten": "波兰",
    "bentschen": "波兰", "prittisch": "波兰", "schwerin": "波兰", "birnbaum": "波兰",
    "tirschtiegel": "波兰", "bomst": "波兰", "meseritz": "波兰", "schwerin an der warthe": "波兰",
    # 捷克
    "kaaden": "捷克", "komotau": "捷克", "bruennsee": "捷克", "bruenn": "捷克",
    "oehringen": "捷克", "bischofteinitz": "捷克", "reichenberg": "捷克",
    "weisskirch": "捷克", "dobring": "捷克", "erwinsdorf": "捷克", "baumbiedersdorf": "捷克",
    "hainau": "捷克", "goettenitz": "捷克", "tichov": "捷克",
    "chocholow": "波兰", "gnidawa": "波兰",
    # 匈牙利
    "solymar": "匈牙利", "nemetker": "匈牙利", "bataapati": "匈牙利", "budakeszi": "匈牙利",
    "tatabanya": "匈牙利", "tarjan": "匈牙利", "hajos": "匈牙利", "csavoly": "匈牙利",
    "ujfutak": "匈牙利", "oroszlany": "匈牙利",
    # 罗马尼亚 / 塞尔维亚 / 斯洛文尼亚 / 克罗地亚
    "sathmar": "罗马尼亚", "neudorf": "罗马尼亚", "batschka": "塞尔维亚",
    "kroatien": "克罗地亚", "slawonien": "克罗地亚", "sotin": "克罗地亚",
    "krain": "斯洛文尼亚", "gottschee": "斯洛文尼亚",
    # 中国（县/地区级 pinyin；省份名另由 ÿ 前缀表处理）
    "zizhou": "中国", "shanbei": "中国", "hequ": "中国", "chongqing": "中国",
    "suzhou": "中国", "guangzhou": "中国", "nanjing": "中国", "kunming": "中国",
    "hangzhou": "中国", "wenzhou": "中国", "ningbo": "中国", "changsha": "中国",
    "chengdu": "中国", "xian": "中国", "yinchuan": "中国", "lasa": "中国",
    "shenyang": "中国", "dalian": "中国", "haicheng": "中国", "qiqihar": "中国",
    "hailun": "中国", "yichun": "中国", "mudanjiang": "中国", "changchun": "中国",
    "shenchi": "中国", "jinzhong": "中国", "jixian": "中国", "shijiazhuang": "中国",
    "zhangjiakou": "中国", "xingtai": "中国", "kaifeng": "中国", "zhenping": "中国",
    "wuhu": "中国", "anqing": "中国", "bengbu": "中国", "huainan": "中国",
    "fuzhou": "中国", "xiamen": "中国", "quanzhou": "中国", "zhangzhou": "中国",
    "nanchang": "中国", "ganzhou": "中国", "jiujiang": "中国", "jingdezhen": "中国",
    "wuhan": "中国", "yichang": "中国", "xiangxi": "中国", "changde": "中国",
    "meixian": "中国", "chaozhou": "中国", "shantou": "中国", "zhongshan": "中国",
    "haifeng": "中国", "danxian": "中国", "wenchang": "中国", "haikou": "中国",
    "nanning": "中国", "liuzhou": "中国", "guilin": "中国", "beihai": "中国",
    "guiyang": "中国", "zunyi": "中国", "dushan": "中国", "anning": "中国",
    "gejiu": "中国", "jianshui": "中国", "dali": "中国", "lijiang": "中国",
    "menghai": "中国", "mianyang": "中国", "yibin": "中国", "zigong": "中国",
    "nanchong": "中国", "daxian": "中国", "lanzhou": "中国", "tianshui": "中国",
    "xining": "中国", "urumqi": "中国", "qitai": "中国", "heze": "中国",
    "jinan": "中国", "qingdao": "中国", "rizhao": "中国", "weifang": "中国",
    "taian": "中国", "zaozhuang": "中国", "linqing": "中国", "dezhou": "中国",
}

# O: 里的中文省份字样（ÿShanxi 等）与省份名
CN_PROV = {
    "shanxi": "中国·山西", "shaanxi": "中国·陕西", "yunnan": "中国·云南",
    "hubei": "中国·湖北", "anhui": "中国·安徽", "henan": "中国·河南",
    "jiangsu": "中国·江苏", "guangdong": "中国·广东", "fujian": "中国·福建",
    "guizhou": "中国·贵州", "jiangxi": "中国·江西", "neimeng": "中国·内蒙古",
    "qinghai": "中国·青海", "ningxia": "中国·宁夏", "hainan": "中国·海南",
    "hebei": "中国·河北", "hunan": "中国·湖南", "sichuan": "中国·四川",
    "zhejiang": "中国·浙江", "gansu": "中国·甘肃", "liaoning": "中国·辽宁",
    "heilongjiang": "中国·黑龙江", "jilin": "中国·吉林", "taiwan": "中国台湾",
    "guangxi": "中国·广西", "shandong": "中国·山东", "xinjiang": "中国·新疆",
    "xizang": "中国·西藏", "tibet": "中国·西藏",
}


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").replace("ÿ", "").strip().rstrip(";").rstrip("?").strip()).lower()


CJK_PROV = {
    "山西": "中国·山西", "陕西": "中国·陕西", "云南": "中国·云南", "湖北": "中国·湖北",
    "安徽": "中国·安徽", "河南": "中国·河南", "江苏": "中国·江苏", "广东": "中国·广东",
    "福建": "中国·福建", "贵州": "中国·贵州", "江西": "中国·江西", "内蒙古": "中国·内蒙古",
    "青海": "中国·青海", "宁夏": "中国·宁夏", "海南": "中国·海南", "河北": "中国·河北",
    "湖南": "中国·湖南", "四川": "中国·四川", "浙江": "中国·浙江", "甘肃": "中国·甘肃",
    "辽宁": "中国·辽宁", "黑龙江": "中国·黑龙江", "吉林": "中国·吉林", "台湾": "中国台湾",
    "广西": "中国·广西", "山东": "中国·山东", "新疆": "中国·新疆", "西藏": "中国·西藏",
    "北京": "中国·北京", "天津": "中国·天津", "上海": "中国·上海", "重庆": "中国·重庆",
}


def country_of(region_val: str, o_field: str):
    """返回 (country, province_hint)。中国曲目优先给到省级。"""
    if o_field:
        parts = [p.strip() for p in o_field.split(",") if p.strip()]
        norms = [norm(x) for x in parts]
        # 中国层级：扫全部段找省份
        if norms and norms[0] in ("china", "ostasien", "asien"):
            for n in norms[1:]:
                if n in CN_PROV:
                    return CN_PROV[n], None
            # 中间无省份 → 用 region 里的中文省名/县名
            rv = norm(region_val)
            for k, v in CN_PROV.items():
                if rv.startswith(k):
                    return v, None
            if rv in REGION:
                return REGION[rv], None
            return "中国", None
        if parts:
            last = norms[-1]
            if last in COUNTRY:
                return COUNTRY[last], None
            if last in REGION:
                return REGION[last], None
            if last in CN_PROV:
                return CN_PROV[last], None
    rv = norm(region_val)
    if rv in CJK_PROV:
        return CJK_PROV[rv], None
    if re.search(r"[\u4e00-\u9fff]", region_val or ""):
        for k, v in CJK_PROV.items():
            if k in region_val:
                return v, None
        return "中国", None
    rv = norm(region_val)
    if not rv:
        return None, None
    for k, v in CN_PROV.items():
        if rv.startswith(k):
            return v, None
    if re.match(r"^(z|od) warszawy", rv) or rv.startswith("od ") or rv.startswith("z "):
        return "波兰", None
    if rv in COUNTRY:
        return COUNTRY[rv], None
    if rv in REGION:
        return REGION[rv], None
    return None, None


def clean_form(r_field: str):
    if not r_field:
        return None
    first = r_field.split(",")[0].strip()
    first = first.rstrip("]").strip()
    first = re.sub(r"\s*-\s*", "-", first)
    first = re.sub(r"\s+", " ", first)
    return first or None


def load_blocks():
    idx = {}
    for f in sorted(ABC.glob("*.abc")):
        cur = {}
        blocks = []
        for line in f.read_text(encoding="utf-8", errors="replace").splitlines():
            if len(line) >= 2 and line[1:2] == ":":
                k, v = line[:2], line[2:].strip()
                if k == "X:":
                    if cur.get("T:"):
                        blocks.append(cur)
                    cur = {}
                elif k in ("T:", "O:", "R:"):
                    cur.setdefault(k, v)
        if cur.get("T:"):
            blocks.append(cur)
        for b in blocks:
            idx.setdefault((f.name.lower(), b["T:"].strip().lower()), b)
    return idx


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv[1:])

    blocks = load_blocks()
    print(f"[essen] ABC 块索引 {len(blocks):,} 条")
    rows = [json.loads(l) for l in JSONL.open(encoding="utf-8")]
    changed = 0
    kinds = Counter()
    samples = []
    out = []
    for r in rows:
        fn = (r.get("src_path") or "").split("/")[-1].lower()
        key = (fn, str(r.get("title") or "").strip().lower())
        b = blocks.get(key)
        ch = {}
        if b:
            c, _ = country_of(r.get("region") or "", b.get("O:") or "")
            if c and not r.get("country"):
                ch["country"] = c
            fm = clean_form(b.get("R:") or "")
            if fm and not r.get("form"):
                ch["form"] = fm
        if ch:
            changed += 1
            for k in ch:
                kinds[k] += 1
            if len(samples) < 5:
                samples.append((r["id"], ch, (b or {}).get("O:")))
            r2 = dict(r)
            r2.update(ch)
            out.append(r2)
        else:
            out.append(r)
    print()
    print("=== essen 地理/曲式富化报告 ===")
    print(f"  条数 {len(rows):,} · 改动 {changed:,} · 字段 {dict(kinds)}")
    for s in samples:
        print("   样例:", s)
    if args.dry_run:
        print("\n[dry-run] 未写回")
        return 0
    ts = time.strftime("%Y%m%d-%H%M%S")
    bdir = BACKUP / f"pre-essengeo-{ts}"
    bdir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(JSONL, bdir / JSONL.name)
    print(f"\n[backup] {bdir}")
    with JSONL.open("w", encoding="utf-8", newline="\n") as fh:
        for r in out:
            fh.write(json.dumps(r, ensure_ascii=False, separators=(",", ":")) + "\n")
    print("[write] 已写回 essen.jsonl")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
