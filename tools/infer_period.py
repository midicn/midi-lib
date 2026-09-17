#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""D8 质量提升 · period（音乐时期）推断

原理：作曲家生卒年 → 主要创作时期（以逝世年为主判据，特例手工覆盖）。
覆盖所有 period 为空的记录；不覆盖已有值。

用法：
  python tools/infer_period.py [--dry-run]
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACKS = ROOT / "midi_db" / "tracks"
REPORT = ROOT / "midi_db" / "stats" / "period-report.md"

# 作曲家生卒年（slug -> birth, death）；特例可给第三项直接指定时期
Y = {
    # 中世纪 / 文艺复兴
    "machaut": (1300, 1377), "dufay": (1397, 1474), "dunstable": (1390, 1453),
    "desprez": (1440, 1521), "janequin": (1495, 1560), "isaac": (1450, 1517),
    "senfl": (1486, 1543), "palestrina": (1525, 1594), "lassus": (1532, 1594),
    "byrd": (1543, 1623), "gibbons": (1583, 1625), "tallis": (1505, 1585),
    "dowland": (1563, 1626), "morley": (1557, 1602), "weelkes": (1576, 1623),
    "encina": (1468, 1530), "ockeghem": (1410, 1497), "praetorius": (1571, 1621),
    "anonymous-trecento": (1300, 1400), "trecento": (1300, 1400),
    # 巴洛克
    "monteverdi": (1567, 1643), "gabrieli": (1557, 1612), "sweelinck": (1562, 1621),
    "frescobaldi": (1583, 1643), "schutz": (1585, 1672), "schein": (1586, 1630),
    "scheidt": (1587, 1654), "froberger": (1616, 1667), "buxtehude": (1637, 1707),
    "pachelbel": (1653, 1706), "purcell": (1659, 1695), "corelli": (1653, 1713),
    "couperin": (1668, 1733), "lully": (1632, 1687), "charpentier": (1643, 1704),
    "albinoni": (1671, 1751), "bach": (1685, 1750), "handel": (1685, 1759),
    "vivaldi": (1678, 1741), "telemann": (1681, 1767), "scarlatti": (1685, 1757),
    "rameau": (1683, 1764), "pergolesi": (1710, 1736), "bach-cpe": (1714, 1788),
    "bach-jc": (1735, 1782), "bach-wf": (1710, 1784), "muffat": (1653, 1704),
    "bruhns": (1665, 1697), "tunder": (1614, 1667), "biber": (1644, 1704),
    "marcello": (1673, 1747), "tartini": (1692, 1770), "locatelli": (1695, 1764),
    "geminiani": (1687, 1762), "veracini": (1690, 1768),
    # 古典主义
    "haydn": (1732, 1809), "mozart": (1756, 1791), "beethoven": (1770, 1827),
    "gluck": (1714, 1787), "boccherini": (1743, 1805), "clementi": (1752, 1832),
    "salieri": (1750, 1825), "hummel": (1778, 1837), "cimarosa": (1749, 1801),
    "dittersdorf": (1739, 1799), "vanhal": (1739, 1813), "pleyel": (1757, 1831),
    "kuhlau": (1786, 1832), "sor": (1778, 1839), "giuliani": (1781, 1829),
    "carcassi": (1792, 1853), "aguado": (1784, 1849), "diabelli": (1781, 1858),
    "czerny": (1791, 1857), "field": (1782, 1837), "dussek": (1760, 1812),
    "cartellieri": (1772, 1807), "cambini": (1746, 1825), "cannabich": (1731, 1798),
    "martini": (1706, 1784), "paisiello": (1740, 1816), "cherubini": (1760, 1842),
    "gretry": (1741, 1813), "sacchini": (1730, 1786),
    # 浪漫主义
    "schubert": (1797, 1828), "chopin": (1810, 1849), "liszt": (1811, 1886),
    "schumann": (1810, 1856), "brahms": (1833, 1897), "mendelssohn": (1809, 1847),
    "schumann-clara": (1819, 1896), "fanny-hensel": (1805, 1847), "hensel": (1805, 1847),
    "henselt": (1814, 1889), "bertini": (1798, 1876), "mertz": (1806, 1856),
    "horetzky": (1796, 1870), "tchaikovsky": (1840, 1893), "dvorak": (1841, 1904),
    "grieg": (1843, 1907), "wagner": (1813, 1883), "verdi": (1813, 1901),
    "berlioz": (1803, 1869), "mendelssohn-bartholdy": (1809, 1847),
    "schubert-f": (1797, 1828), "bruckner": (1824, 1896), "mahler": (1860, 1911),
    "johann-strauss": (1825, 1899), "strauss": (1864, 1949), "saint-saens": (1835, 1921),
    "franck": (1822, 1890), "faure": (1845, 1924), "faureg": (1845, 1924),
    "rubinstein": (1829, 1894), "balakirev": (1837, 1910), "borodin": (1833, 1887),
    "mussorgsky": (1839, 1881), "rimsky-korsakov": (1844, 1908), "glazunov": (1865, 1936),
    "scriabin": (1872, 1915), "rachmaninoff": (1873, 1943), "granados": (1867, 1916),
    "albeniz": (1860, 1909), "moszkowski": (1854, 1925), "sinding": (1856, 1941),
    "godowsky": (1870, 1938), "paderewski": (1860, 1941), "wieniawski": (1835, 1880),
    "bortkiewicz": (1877, 1952), "burgmuller": (1806, 1874), "heller": (1813, 1888),
    "alkan": (1813, 1888), "gottschalk": (1829, 1869), "foster": (1826, 1864),
    "offenbach": (1819, 1880), "puccini": (1858, 1924), "mascagni": (1863, 1945),
    "leoncavallo": (1857, 1919), "giordano": (1867, 1948), "catalani": (1854, 1893),
    "donizetti": (1797, 1848), "bellini": (1801, 1835), "rossini": (1792, 1868),
    "massenet": (1842, 1912), "delibes": (1836, 1891), "bizet": (1838, 1875),
    "gounod": (1818, 1893), "thomas": (1811, 1896), "lalo": (1823, 1892),
    # 印象派
    "debussy": (1862, 1918), "satie": (1866, 1925), "ravel": (1875, 1937),
    "d-indy": (1851, 1931), "chabrier": (1841, 1894), "dukas": (1865, 1935),
    "durey": (1888, 1979), "chausson": (1855, 1899), "duparc": (1848, 1933),
    # 现代
    "bartok": (1881, 1945), "stravinsky": (1882, 1971), "prokofiev": (1891, 1953),
    "shostakovich": (1906, 1975), "rachmaninoff-s": (1873, 1943), "schonberg": (1874, 1951),
    "berg": (1885, 1935), "webern": (1883, 1945), "hindemith": (1895, 1963),
    "gershwin": (1898, 1937), "copland": (1900, 1990), "britten": (1913, 1976),
    "joplin": (1868, 1917), "lamb": (1887, 1960), "blake": (1883, 1983),
    "janacek": (1854, 1928), "sibelius": (1865, 1957), "nielsen": (1865, 1931),
    "szymanowski": (1882, 1937), "kodaly": (1882, 1967), "enescu": (1881, 1955),
    "de-falla": (1876, 1946), "turina": (1882, 1949), "respighi": (1879, 1936),
    "malipiero": (1882, 1973), "casella": (1883, 1947), "pizzetti": (1880, 1968),
    "villa-lobos": (1887, 1959), "ginastera": (1916, 1983), "chavez": (1899, 1978),
    "messiaen": (1908, 1992), "dutilleux": (1916, 2013), "boulez": (1925, 2016),
    "stockhausen": (1928, 2007), "berio": (1925, 2003), "ligeti": (1923, 2006),
    "cage": (1912, 1992), "glass": (1937, 0), "reich": (1936, 0),
    "part": (1935, 0), "gorecki": (1933, 2010), "penderecki": (1933, 2020),
    "lutoslawski": (1913, 1994), "scelsi": (1905, 1988), "cowell": (1897, 1965),
    "ives": (1874, 1954), "varoese": (1883, 1965), "satie-e": (1866, 1925),
    # 民谣/传统（无时期）
    "traditional": None, "unknown": None, "anonymous": None,
    "various-demos": None, "various-leadsheets": None,
    # 第二轮补充（教学曲/女性作曲家/近现代）
    "gurlitt": (1820, 1901), "chaminade": (1857, 1944), "beyer": (1803, 1863),
    "holmes": (1847, 1903), "kapustin": (1937, 2020), "cramer": (1771, 1858),
    "barber": (1910, 1981), "lang": (1815, 1880), "streabbog": (1835, 1886),
    "kohler": (1820, 1886), "lemoine": (1786, 1854), "gobbaerts": (1835, 1886),
    "brunner": (1850, 1921), "krause": (1833, 1906), "maykapar": (1867, 1938),
    "rebikov": (1866, 1920), "lier": (1815, 1888), "spindler": (1817, 1885),
    "bertini-j": (1798, 1876), "hunten": (1793, 1878), "hünten": (1793, 1878),
    "gade": (1817, 1890), "kjerulf": (1815, 1868), "hartmann": (1805, 1900),
    "wachs": (1851, 1915), "klein": (1919, 2001), "milde": (1821, 1898),
    "sitt": (1850, 1922), "dont": (1815, 1888), "wieniawski": (1835, 1880),
    "kayser": (1815, 1888), "küchler": (1867, 1937), "kuchler": (1867, 1937),
    "seitz": (1848, 1918), "sonn": (1815, 1890), "mazas": (1782, 1849),
    "kreutzer": (1766, 1831), "roda": (1770, 1843), "fiocco": (1650, 1742),
    "marais": (1656, 1728), "forqueray": (1672, 1745), "duport": (1749, 1819),
    "dotzauer": (1783, 1860), "lee": (1806, 1876), "goltermann": (1824, 1898),
    "gounod-c": (1818, 1893), "fauré": (1845, 1924), "ravel-m": (1875, 1937),
    "poulenc": (1899, 1963), "milhaud": (1892, 1974), "honegger": (1892, 1955),
    "koechlin": (1867, 1950), "caplet": (1878, 1925), "aubert": (1877, 1968),
    "bachelet": (1864, 1944), "hahn": (1874, 1947), "messager": (1853, 1929),
    "indie": (1851, 1931), "magnard": (1865, 1914), "roparz": (1869, 1957),
    "vierne": (1870, 1937), "widör": (1844, 1937), "widor": (1844, 1937),
    "guilmant": (1837, 1911), "gigout": (1844, 1925), "boellmann": (1862, 1897),
    "dubois": (1837, 1924), "lefebure-wely": (1817, 1869), "bonnet": (1883, 1944),
    "tournemire": (1870, 1939), "dupre": (1886, 1971), "langlais": (1907, 1991),
}

# 手工覆盖（时期特殊，不按逝世年）
OVERRIDE = {
    "monteverdi": "baroque", "beethoven": "classical",
    "bach": "baroque", "handel": "baroque", "scarlatti": "baroque",
    "schubert": "romantic", "shostakovich": "modern",
    "brahms": "romantic", "tchaikovsky": "romantic", "stravinsky": "modern",
    "mendelssohn": "romantic", "schumann": "romantic", "chopin": "romantic",
    "liszt": "romantic", "satie": "impressionist", "debussy": "impressionist",
    "ravel": "impressionist", "joplin": "modern", "gershwin": "modern",
    "scriabin": "romantic", "rachmaninoff": "romantic", "mahler": "romantic",
    "strauss": "romantic", "sibelius": "romantic", "saint-saens": "romantic",
    "faure": "romantic", "faureg": "romantic", "granados": "romantic",
    "albeniz": "romantic", "glazunov": "romantic", "dvorak": "romantic",
    "grieg": "romantic", "bartok": "modern", "prokofiev": "modern",
}


# 源级兜底（作曲家信息缺失时按源特性判定）
SOURCE_PERIOD = {
    "emopia": "contemporary",      # 现代流行钢琴
    "groove": "contemporary",      # 现代鼓手演奏
    "oga": "contemporary",         # 现代游戏音乐
    "mutopia": None,
    # 传统/民歌源 → traditional（民间音乐，不归入西方音乐史分期）
    "chinafolk": "traditional", "thesession": "traditional",
    "norbeck": "traditional", "abcmisc": "traditional",
    "nottingham": "traditional", "essen": "traditional",
    "wikifonia": "traditional",
}


def period_of(slug: str, source: str = "") -> str | None:
    if slug in OVERRIDE:
        return OVERRIDE[slug]
    y = Y.get(slug)
    if y is None:
        return SOURCE_PERIOD.get(source)
    _, death = y
    if not death:            # 在世（0 = 仍在世）
        return "contemporary"
    if death < 1600:
        return "renaissance"
    if death < 1760:         # 巴赫 1750 / 亨德尔 1759 / 斯卡拉蒂 1757
        return "baroque"
    if death < 1830:         # 莫扎特 1791 / 海顿 1809 / 贝多芬 1827
        return "classical"
    if death < 1925:         # 舒伯特 1828 / 肖邦 1849 / 勃拉姆斯 1897 / 格里格 1907
        return "romantic"
    if death < 1970:         # 普罗科菲耶夫 1953 / 巴托克 1945
        return "modern"
    return "contemporary"


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv[1:])

    files = sorted(TRACKS.glob("*.jsonl"))
    data = {}
    filled = 0
    overrode = 0
    before_have = 0
    total = 0
    for f in files:
        rows = [json.loads(l) for l in f.open(encoding="utf-8")]
        for r in rows:
            total += 1
            slug = r.get("composer_slug") or ""
            if r.get("period"):
                before_have += 1
                # 锚点作曲家的源 period 可能有误（如 ariamidi 把 Bach 标 classical）：
                # OVERRIDE 是音乐学共识 → 强制覆盖；非锚点作曲家保留源值
                if slug not in OVERRIDE:
                    continue
            p = period_of(slug, r.get("source") or "")
            if p:
                if r.get("period"):
                    overrode += 1
                else:
                    filled += 1
                r["period"] = p
        data[f] = rows
    print(f"[infer] 总 {total:,} · 原有 {before_have:,} · 新推断 {filled:,} · 锚点覆盖 {overrode:,}", flush=True)
    print(f"[infer] 覆盖率 {before_have/total*100:.1f}% -> {(before_have+filled)/total*100:.1f}%", flush=True)

    if not args.dry_run:
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        bdir = ROOT / "midi_trash" / f"pre-period-{ts}"
        bdir.mkdir(parents=True, exist_ok=True)
        for f, rows in data.items():
            shutil.copy2(f, bdir / f.name)
            with f.open("w", encoding="utf-8", newline="\n") as fh:
                for r in rows:
                    fh.write(json.dumps(r, ensure_ascii=False, separators=(",", ":")) + "\n")
        print(f"[write] 已写回（备份 {bdir.relative_to(ROOT)}）", flush=True)

    rows_all = [r for rows in data.values() for r in rows]
    dist = Counter(r["period"] for r in rows_all if r.get("period"))
    lines = [
        "# period 推断报告",
        "",
        f"> 生成：{datetime.now().isoformat(timespec='seconds')} · {'（试运行）' if args.dry_run else '（已写回）'}",
        "",
        f"- 覆盖率：{before_have/total*100:.1f}% → **{(before_have+filled)/total*100:.1f}%**（新推断 {filled:,} 条）",
        "",
        "## 时期分布",
        "",
        "| 时期 | 曲目数 |",
        "|---|---:|",
    ]
    for k, v in dist.most_common():
        lines.append(f"| {k} | {v:,} |")
    unmatched = Counter(r.get("composer_slug") for r in rows_all
                        if not r.get("period") and r.get("composer_slug"))
    lines += ["", "## 仍未定时期（Top 20，缺生卒年数据）", "",
              "| 作曲家 | 曲目数 |", "|---|---:|"]
    for k, v in unmatched.most_common(20):
        lines.append(f"| `{k}` | {v:,} |")
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"[report] {REPORT.relative_to(ROOT)}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
