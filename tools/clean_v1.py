#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""D8 清洗 v1 · 作曲家归并 + region 白名单

处理：
  1. 作曲家 slug 归并：已知映射表 + 目录名残留（mutopia 的 BeethovenLv 式、m21 的语料目录名）
  2. region 清洗：只保留国家/地区级名称，噪声值移入 extra.region_note
  3. 统计输出：归并前后对比、region 覆盖率变化

用法：
  python tools/clean_v1.py [--dry-run]
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
from collections import Counter
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACKS = ROOT / "midi_db" / "tracks"
REPORT = ROOT / "midi_db" / "stats" / "clean-report.md"

# ---- 标准作曲家表（正确拼写；用于「姓氏+名缩写」式 slug 的归并，如 czernyc -> czerny）----
CANON = """
bach mozart beethoven chopin liszt schubert schumann czerny scarlatti bartok
mendelssohn haydn brahms wagner verdi tchaikovsky rachmaninoff debussy ravel satie
grieg dvorak purcell handel vivaldi corelli monteverdi palestrina scriabin faure
saint-saens franck bruckner mahler strauss prokofiev shostakovich rimsky-korsakov
mussorgsky borodin glinka balakirev borodin weber hummel clementi kuhlau field
albeniz granados de-falla turina moszkowski sinding godowsky balakirew
gabrieli lassus byrd gibbons tallis dowland farnaby bull morley weelkes
couperin rameau lully charpentier albinoni telemann scarlatti pachelbel buxtehude
boccherini salieri gluck haydn clementi czerny kalkbrenner hummel
sor giuliani carcassi mertz aguado tarrega segovia barrios villa-lobos
joplin lamb blake scott gottschalk foster billings
dufay dunstable desprez janequin isaac senfl praetorius schein scheidt
schutz buxtehude bruhns tunder froberger kerll murschhauser
albeniz alkan arensky atterberg balakirev bax berwald bloch boguslawski
bortkiewicz bridge busoni carpenter casella chabrier chaminade chausson
dalcroze dukas d'indy duparc durey elgar encina ernst fabini falla farrenc
fauré ferguson flotow foote françaix franck frescobaldi fuchs furlant
albeniz alyabyev archangelsky arne arriaga auber bainton bakfark balbastre
bangs bantock bargiel barnby beethoven bellini benjamin benserade berlioz
bertin bertoni biber bishop bizet bloch boccherini boehm boieldieu bona bonis
bortniansky boulanger boyce brahms breval bridge bronsart bruch bruckner
buntingsburghes burleigh busoni busser butterworth buxtehude byrd
cabanilles caldara campagnoli campra cannABich caplet carissimi carulli
casella castelnuovo-tedesco catalani cavallini cellier cesti charpentier
chausson cherubini chopin cigliano cimarosa clementi coates colle coleridge-taylor
copland corelli coronado costa couperin crawford croce cruft cui
d'ambrosio dalayrac dandrieu danzi david debussy delibes delius denza
destouches diabelli diepenbrock dittersdorf dohnanyi donizetti dragonetti
dubois dukas duparc durand durey durosoir dvorak
eberl eckert egk eigeldinger elgar ellerton encina engel erb eslava
falla fanny-hensel farrenc faure fibich field finck fiorillo flotow foddis
foster francaix franck francoeur frederick frescoaldi fuchs furlant
gabrieli gaertner galuppi garcia gassmann geminiani genzmer gerhard
gershwin gibbons gigout giordani giuliani glazunov glinka gluck godard
godowsky goldmark gomes gounod grainger granados grechaninov gretchaninov
grieg griffes grovlez guerini guilmant gumpert hahn halffter halvorsen
handel haque hasse hauber hauptmann haydn heller hensel herbert hermann
herz hiller hoffmeister hofmann hohmann holst holzbauer homan hopkins
hubay hummel humperdinck hure hurlebusch ives jacobi jadassohn janequin
janacek jarnefelt jenkins joachim joplin josquin judd juon kalkbrenner
kalliwoda kaminski karłowicz karg-elert keyser kirchner kjerulf klein
klengel knorr kocian koechlin koetsier kohler kollo komitas koppel
kornauth korngold kraus krebs kreisler krenek krommer kuhlau kuhnau
labitzky lachenmann lalo lambert lang laos lassus leclair lecocq lefebvre
legrenzi lehmann lekeu leo leveridge lidarti liebling lipatti liszt
locatelli loeffler loewe lortzing lotze ludebuehl lully lumbye luzzaschi
macdowell machaut macmillan madetoja magnard mahler malipiero mangold
manfredini marais marchand marschner martini martinu mascagni
massenet mathias mattheson mccabe mclean medtner melartin mello mendelssohn
merikanto meridith messiaen meyerbeer miaskovsky milhaud moeran mompou
monn monteverdi moore moreau mosaiques moscheles moszkowski mozart
muffat müller murcia musorgsky mussorgsky nardini neefe neukomm nichelmann
nielsen nigg nilsson nobre novak nowowiejski oberthuer ockeghem
offenbach onslow orff orthel pachelbel paderewski paganini palestrina
paradis pardini parker pasquini pejacevic penderecki perosi persichetti
peterson petrassi pfitzner philidor piccinni pierne pijper pinkham
pisendel pleyel ponce ponchielli popov poulenc praetorius prokofiev
puccini purcell quantz rachmaninoff raffe raff raimann rameau rathaus
ravel ravel-reger reber rebikov reffice reger reicha reinecke reinhold
resphigi respighi reubke reutter rhene-baton rieu rimsky-korsakov riisager
riley ritter rochberg rodrigo roger roldan romberg rontgen roslawez
rossini roussel rubinstein ruedinger ruggles russell ryuichi
saint-saens salieri sammartini sampson sarasate satie sauer scarlatti
scherber scheidt schein schenck scherer schmitt schneider schnittke
schoenberg schubert schulhoff schuman schumann schutz schonberg
sechter segal seitz serocki sessions sgardello shostakovich sibelius
simpson skalkottas skryabin smetana soler sor sorabji spohr staden
stanford starke steibelt steinberg stenhammar stepan sternfeld stockhausen
stojowski strauss stravinsky strozzi suk sullivan suppe szymanowski
taneev tartini tausig tchaikovsky telemann tippett toha tomlinson
toovey torelli traetta tubin tunder turina tveitt ury
vainberg valen valente vanhal vaughan-williams veracini verdi viadana
vieuxtemps villa-lobos villiers volta vranicky wagner walton ward
weber webern weelkes weill weinberg weiner weiss wesley widor
wieniawski wilbye wolf wolff woolf worgan xenakis ysaÿe zelter zimmermann
zelenka zandonai
""".split()

CANON_SET = set(CANON)
# 变体 -> 标准
CANON_ALIAS = {
    "saint-saens": "saint-saens", "saens": "saint-saens", "saintsaens": "saint-saens",
    "rimskykorsakov": "rimsky-korsakov", "korsakov": "rimsky-korsakov",
    "vaughanwilliams": "vaughan-williams", "williams-vaughan": "vaughan-williams",
    "dindy": "d-indy", "mussorgsky": "mussorgsky", "musorgsky": "mussorgsky",
    "schonberg": "schoenberg", "schoenberg": "schoenberg",
    "skryabin": "scriabin", "skrjabin": "scriabin", "scriabin": "scriabin",
    "rachmaninov": "rachmaninoff", "rachmaninow": "rachmaninoff",
    "tschaikowsky": "tchaikovsky", "tchaikowsky": "tchaikovsky", "chaikovsky": "tchaikovsky",
    "dvorak": "dvorak", "dvorzak": "dvorak",
    "debussy": "debussy", "rachmaninoff": "rachmaninoff",
    "gretchaninov": "grechaninov", "gretschaninow": "grechaninov",
    "strauss-j": "strauss", "strauss-r": "strauss", "strauss-ii": "strauss",
    "fanny-hensel": "fanny-hensel", "henschel": "hensel",
    "cpe-bach": "bach-cpe", "jc-bach": "bach-jc", "wfbach": "bach-wf",
    # 全名式（名-姓）特殊：多段名需显式指定，防被尾名误并
    "wilhelm-friedemann-bach": "bach-wf",
    "carl-philipp-emanuel-bach": "bach-cpe",
    "johann-christian-bach": "bach-jc",
    "johann-sebastian-bach": "bach",
    "carl-maria-von-weber": "weber",
    "franz-joseph-haydn": "haydn",
    "johann-strauss-ii": "strauss", "johann-strauss": "strauss",
    "richard-strauss": "strauss", "josef-strauss": "strauss",
    "clara-schumann": "schumann-clara", "robert-schumann": "schumann",
    "fanny-mendelssohn": "fanny-hensel", "fanny-hensel": "fanny-hensel",
    "felix-mendelssohn": "mendelssohn",
    "antonio-vivaldi": "vivaldi", "antonio-soler": "soler",
    "francois-couperin": "couperin", "louis-couperin": "couperin",
    "jean-philippe-rameau": "rameau", "jean-baptiste-lully": "lully",
}


# 独立作曲家（其姓氏恰好 = 标准名 + 1~2 字母）——**禁止归并**（人工审核确认）
EXCLUDE_SLUGS = {
    "henselt",     # Adolf von Henselt ≠ Fanny Hensel
    "bachmann",    # P. Bachmann ≠ Bach
    "bertini",     # Bertini ≠ Bertin
    "bonamici",    # Bonamici ≠ Bona
    "clementini",  # Clementini ≠ Clementi
    "engelmann",   # Engelmann ≠ Engel
    "kollontay",   # Kollontay ≠ Kollo
    "bullard",     # Bullard ≠ Bull
    "bullow",      # Bülow ≠ Bull
    "aubert",      # Aubert ≠ Auber
    "humorist",    # 兜底
}


def canonical(slug: str) -> str:
    """把「姓氏+名缩写」式 slug 归并到标准拼写：czernyc -> czerny、beethovenlv -> beethoven。

    规则（v2，收紧）：
      1. 显式排除名单优先（独立作曲家，防误伤）
      2. 别名表精确匹配
      3. 标准表精确匹配
      4. 标准名 + **1~2 个字母**的名缩写后缀（如 T / LV / FF）
         —— 后缀 ≥3 字母一律不归并（bertini / clementini / bachmann 等会被保护）
    """
    s = norm_slug(slug)
    if not s:
        return s
    if s in EXCLUDE_SLUGS:
        return s
    if s in CANON_ALIAS:
        return CANON_ALIAS[s]
    if s in CANON_SET:
        return s
    # 全名式（名-姓）：frdric-chopin -> chopin、franz-schubert -> schubert
    if "-" in s:
        tail = s.rsplit("-", 1)[-1]
        if tail in CANON_SET and tail not in EXCLUDE_SLUGS:
            return tail
    for c in CANON:
        if len(c) >= 4 and s.startswith(c):
            suffix = s[len(c):]
            if 0 < len(suffix) <= 2 and suffix.isalpha():   # 仅 1~2 字母的名缩写
                return c
    return s



MERGE = {
    # mutopia 目录名式
    "beethovenlv": ("beethoven", "Ludwig van Beethoven"),
    "mozartwa": ("mozart", "Wolfgang Amadeus Mozart"),
    "bachjs": ("bach", "Johann Sebastian Bach"),
    "bachcpe": ("bach-cpe", "Carl Philipp Emanuel Bach"),
    "handelgf": ("handel", "George Frideric Handel"),
    "haydnfj": ("haydn", "Joseph Haydn"),
    "schubertf": ("schubert", "Franz Schubert"),
    "schumannr": ("schumann", "Robert Schumann"),
    "chopinf": ("chopin", "Frédéric Chopin"),
    "lisztf": ("liszt", "Franz Liszt"),
    "giulianim": ("giuliani", "Mauro Giuliani"),
    "sorf": ("sor", "Fernando Sor"),
    "horetzkyf": ("horetzky", "Felix Horetzky"),
    "carcassim": ("carcassi", "Matteo Carcassi"),
    "czernyc": ("czerny", "Carl Czerny"),
    "mertzjk": ("mertz", "Johann Kaspar Mertz"),
    "diabellia": ("diabelli", "Anton Diabelli"),
    "tchaikovskypi": ("tchaikovsky", "Pyotr Ilyich Tchaikovsky"),
    "joplins": ("joplin", "Scott Joplin"),
    "monteverdic": ("monteverdi", "Claudio Monteverdi"),
    "weelkesT": ("weelkes", "Thomas Weelkes"),
    "purcellh": ("purcell", "Henry Purcell"),
    "satiee": ("satie", "Erik Satie"),
    "griege": ("grieg", "Edvard Grieg"),
    "mendelssohnf": ("mendelssohn", "Felix Mendelssohn"),
    "brahmsj": ("brahms", "Johannes Brahms"),
    "debussyc": ("debussy", "Claude Debussy"),
    "vivaldia": ("vivaldi", "Antonio Vivaldi"),
    # m21 语料目录名（非作曲家）
    "ryansmammoth": ("traditional", "Traditional (Ryan's Mammoth Collection)"),
    "trecento": ("anonymous-trecento", "Anonymous (Trecento, 14th c.)"),
    "demos": ("various-demos", "Various (music21 demos)"),
    "leadsheet": ("various-leadsheets", "Various (lead sheets)"),
    "schumann-robert": ("schumann", "Robert Schumann"),
    "schumann-clara": ("schumann-clara", "Clara Schumann"),
    "bach-jc": ("bach-jc", "Johann Christian Bach"),
    "bach-wf": ("bach-wf", "Wilhelm Friedemann Bach"),
}

# 前缀归并（同姓氏不同写法，前 6 字符相同且一方是另一方前缀）
PREFIX_MIN = 6

# ---- 2) region 白名单（国家/地区级）----
REGION_ALLOW = set("""
中国 北京 天津 上海 广东 海南 河北 河南 江苏 吉林 陕西 四川 山东 山西 浙江 福建 湖南 湖北 安徽 江西 云南 贵州 广西 甘肃 青海 宁夏 新疆 西藏 内蒙古 辽宁 黑龙江 重庆
Ireland 爱尔兰 英国 美国 苏格兰 威尔士 英格兰 法国 德国 意大利 西班牙 葡萄牙 荷兰 比利时 瑞士 奥地利 瑞典 挪威 丹麦 芬兰 冰岛 波兰 捷克 斯洛伐克 匈牙利 罗马尼亚 保加利亚 塞尔维亚 克罗地亚 斯洛文尼亚 波黑 黑山 马其顿 希腊 土耳其 阿尔巴尼亚 乌克兰 俄罗斯 白俄罗斯 立陶宛 拉脱维亚 爱沙尼亚 摩尔多瓦 亚美尼亚 格鲁吉亚 阿塞拜疆 以色列 黎巴嫩 叙利亚 约旦 埃及 摩洛哥 阿尔及利亚 突尼斯 利比亚 伊朗 伊拉克 沙特阿拉伯 也门 阿曼 阿联酋 印度 巴基斯坦 孟加拉 斯里兰卡 尼泊尔 不丹 缅甸 泰国 越南 老挝 柬埔寨 马来西亚 新加坡 印度尼西亚 菲律宾 文莱 日本 韩国 蒙古 中国台湾 中国香港 中国澳门
Mexico 墨西哥 古巴 牙买加 海地 多米尼加 波多黎各 特立尼达 巴西 阿根廷 智利 秘鲁 玻利维亚 厄瓜多尔 哥伦比亚 委内瑞拉 乌拉圭 巴拉圭 圭亚那 苏里南
Canada 加拿大 澳大利亚 新西兰 南非 尼日利亚 加纳 肯尼亚 埃塞俄比亚 塞内加尔 马里 几内亚 喀麦隆 刚果 赞比亚 津巴布韦 坦桑尼亚 乌干达
巴尔干 克莱兹梅尔 以色列 国际民歌 斯堪的纳维亚 北欧 东欧 西欧 中欧 地中海 加勒比 拉丁美洲 中东 中亚 东南亚 南亚 东亚 西非 北非 东非 中非 南部非洲
Deutschland Bulgaria Serbia Romania Macedonia Greece Croatia Armenia Hungary Russia Albania Poland France Italy Norway Sweden Denmark England Scotland Ireland Israel Turkey Ukraine Finland Slovakia Czechoslovakia Yugoslavia Austria Netherlands Portugal Spain Mexico Bolivia Peru Cuba Venezuela Zambia Japan Taiwan Lebanon SouthAfrica America USA Austria Basque Germany Armenia Bosnia Dagestan Azerbaijan Kosovo Lithuania Slovakia Finland Belgium Portugal Spain
""".split())

NOISE = re.compile(r"kammen|klez camp|trad|played by|collected by|orchestra|"
                   r"^\d+$|^\d{4}$|^[a-z]+\s\d+#|\.", re.I)


def norm_slug(s: str | None) -> str:
    if not s:
        return ""
    return re.sub(r"[^a-z0-9\-]", "-", s.strip().lower()).strip("-")


def build_prefix_index(slugs: set[str]) -> dict[str, str]:
    """把拼写变体归并到**更完整的拼写**（较长的 slug），如 schuman -> schumann。"""
    out = {}
    sl = sorted(slugs, key=len)          # 短 -> 长
    for i, a in enumerate(sl):
        if len(a) < 4:
            continue
        for b in sl[i + 1:]:             # b 更长
            if len(a) >= PREFIX_MIN and b.startswith(a) and b != a:
                out[a] = b               # 短变体 -> 完整拼写
            elif len(a) >= PREFIX_MIN and a.startswith(b):
                out[b] = a
    return out


def region_ok(v: str | None) -> bool:
    if not v:
        return False
    if v in REGION_ALLOW:
        return True
    if NOISE.search(v):
        return False
    # 长度过长（句子式）也视为噪声
    return len(v) <= 24 and not v.count(" ")


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv[1:])

    all_slugs = set()
    files = sorted(TRACKS.glob("*.jsonl"))
    data = {}
    for f in files:
        rows = [json.loads(l) for l in f.open(encoding="utf-8")]
        data[f] = rows
        all_slugs |= {r["composer_slug"] for r in rows if r.get("composer_slug")}

    prefix_idx = build_prefix_index(all_slugs)
    print(f"[scan] {len(files)} 源 · {len(all_slugs)} 个作曲家 slug · 前缀归并候选 {len(prefix_idx)}", flush=True)

    stats = {"composer_merged": 0, "region_cleaned": 0}
    for f, rows in data.items():
        for r in rows:
            slug = norm_slug(r.get("composer_slug"))
            if slug in MERGE:
                new_slug, new_name = MERGE[slug]
                if r.get("composer_slug") != new_slug:
                    stats["composer_merged"] += 1
                r["composer_slug"], r["composer_name"] = new_slug, new_name
            else:
                canon = canonical(slug)          # 标准名 + 缩写后缀规则
                if canon and canon != r.get("composer_slug"):
                    stats["composer_merged"] += 1
                    r["composer_slug"] = canon
                    r["composer_name"] = canon.replace("-", " ").title()
                elif canon:
                    r["composer_slug"] = canon

            # region 清洗
            reg = r.get("region")
            if reg and not region_ok(reg):
                r.setdefault("extra", {})["region_note"] = reg
                r["region"] = None
                stats["region_cleaned"] += 1

    print(f"[clean] 作曲家归并 {stats['composer_merged']} 条 · region 清理 {stats['region_cleaned']} 条",
          flush=True)

    if not args.dry_run:
        # 备份后写回
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        bdir = ROOT / "midi_trash" / f"pre-clean-{ts}"
        bdir.mkdir(parents=True, exist_ok=True)
        for f, rows in data.items():
            shutil.copy2(f, bdir / f.name)
            with f.open("w", encoding="utf-8", newline="\n") as fh:
                for r in rows:
                    fh.write(json.dumps(r, ensure_ascii=False, separators=(",", ":")) + "\n")
        print(f"[write] 已写回 {len(data)} 个 jsonl（备份于 {bdir.relative_to(ROOT)}）", flush=True)

    # 报告
    rows_all = [r for rows in data.values() for r in rows]
    total = len(rows_all)
    comp_after = Counter(r["composer_slug"] for r in rows_all if r.get("composer_slug"))
    reg_cov = sum(1 for r in rows_all if r.get("region")) / total * 100
    lines = [
        "# D8 清洗报告 v1（作曲家归并 + region 白名单）",
        "",
        f"> 生成：{datetime.now().isoformat(timespec='seconds')} · {'（试运行）' if args.dry_run else '（已写回）'}",
        "",
        f"- 作曲家 slug：{len(all_slugs)} → **{len(comp_after)}**（归并 {stats['composer_merged']} 条记录）",
        f"- region 清理：{stats['region_cleaned']} 条噪声值（移入 extra.region_note）· 现覆盖率 {reg_cov:.1f}%",
        "",
        "## 归并后 Top 20 作曲家",
        "",
        "| 作曲家 | 曲目数 |",
        "|---|---:|",
    ]
    for c, n in comp_after.most_common(20):
        lines.append(f"| `{c}` | {n:,} |")
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"[report] {REPORT.relative_to(ROOT)}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(__import__("sys").argv))
