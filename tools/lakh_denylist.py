#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""lakh 版权风险三分类词表（F1）。

背景
----
`tools/ingest_lakh.py` 的 KEEP_PAT 含 `christmas|carol`，DROP_PAT 不含任何现代流行
艺人名 → lakh 9,630 首中混入**在版权保护期内**的现代商业音乐，且 zone=study 不在
SKIP_ZONES 里，会全部公开发布。这是真实侵权暴露。

为什么不能只用一条正则
----------------------
`christmas|carol` 泛匹配共 420 首，其中混着三类截然不同的内容：
  · 现代版权作品（要剔）  White Christmas（Irving Berlin, d.1989）
  · 传统公有领域（要留）  Carol of the Bells（乌克兰传统）、O Christmas Tree
  · 纯误命中（要留）      Caroline / Carolina / Barcarolle / O'Carolan（人名）

一刀切会同时造成「误删公有领域内容」与「漏掉现代版权作品」两种错误。
因此这里用三张表显式区分，并由 tools/exclude_lakh_modern.py 产出人工复核台账。

维护约定
--------
  MODERN_COPYRIGHT  作品名/作者名 → 剔除（verify_flag=broken）
  TRADITIONAL_PD    明确公有领域 → 保留（写入排除器的白名单，避免误判）
  FALSE_POSITIVE    正则误命中 → 保留
新增判定必须写明理由与依据（作者 + 卒年 / 传统来源）。
"""
from __future__ import annotations

import re

# ── ① 现代版权作品：剔除 ────────────────────────────────────────────────
# 判据：词曲作者卒年在保护期内（或仍在世），作品为 20 世纪商业出版。
MODERN_COPYRIGHT = [
    # 作品名 → (作者, 卒年/在世)
    (r"white\s*christmas",            "Irving Berlin", 1989),
    (r"merry\s*little\s*christmas",   "Hugh Martin / Ralph Blane", 2011),
    (r"holly\s*jolly\s*christmas",    "Johnny Marks", 1985),
    (r"be\s*home\s*for\s*christmas",  "Walter Kent / Kim Gannon", 1973),
    (r"beg(?:in|i)ning\s*to\s*look",  "Meredith Willson", 1984),
    (r"please\s*come\s*home\s*for\s*christmas", "Charles Brown", 1999),
    (r"drivin'?\s*home\s*for\s*christmas", "Chris Rea", "在世"),
    (r"so\s*this\s*is\s*christmas",   "Jule Styne / Sammy Cahn", 1994),
    (r"christmas\s*waltz",            "Jule Styne / Sammy Cahn", 1994),
    (r"christmas\s*song|chestnuts",   "Mel Tormé / Robert Wells", 1999),
    (r"granma'?s\s*christmas",        "—（现代创作）", None),
    (r"do\s*they\s*know\s*it'?s\s*christmas", "Bob Geldof / Midge Ure", "在世"),
    (r"last\s*christmas",             "George Michael", 2016),
    (r"blue\s*christmas",             "Billy Hayes / Jay Johnson", 2008),
    (r"wonderful\s*christmastime",    "Paul McCartney", "在世"),
    (r"christmas\s*lights",           "Coldplay", "在世"),
    (r"magic\s*of\s*christmas\s*day", "Celine Dion 团队", None),
    (r"christmas\s*in\s*killarney",   "—（现代创作）", None),
    (r"christmas\s*fancy",            "—（现代改编）", None),
    (r"merry\s*christmas\s*baby",     "Lou Baxter / Johnny Moore", 1973),
    (r"sweet\s*caroline",             "Neil Diamond", "在世"),
    (r"oh\s*carol\b|ohcarol\b|oh\s*carole", "Neil Sedaka / Howard Greenfield", 1981),
    (r"takin'?\s*care\s*of\s*business", "Randy Bachman", "在世"),
    (r"roll\s*over\s*beethoven|rolloverbeethoven", "Chuck Berry", 2017),
    (r"i\s*feel\s*the\s*earth\s*move", "Carole King", "在世"),
    (r"it'?s\s*too\s*late",           "Carole King / Toni Stern", "在世"),
    (r"you'?v?e?\s*got\s*a\s*friend", "Carole King", "在世"),
    (r"so\s*far\s*away",              "Carole King", "在世"),
    (r"will\s*you\s*love\s*me\s*tomorrow", "Carole King / Gerry Goffin", 2014),
    (r"homeagain",                    "Carole King", "在世"),
    (r"carolina\s*in\s*my\s*mind",    "James Taylor", "在世"),
    (r"tennessee\s*waltz",            "Pee Wee King / Redd Stewart", 2000),
    (r"anniversary\s*waltz",          "Dave Franklin / Al Dubin", 1969),
    (r"guantanamera",                 "Joseíto Fernández（改编链）", 1979),
    (r"albachiara",                   "Vasco Rossi", "在世"),
    (r"l'?hymne\s*[aà]\s*l'?amour",   "Édith Piaf / Marguerite Monnot", 1963),
    (r"crying\s*in\s*the\s*rain",     "Howard Greenfield / Carole King", 1981),
    (r"back\s*home\s*again",          "John Denver", 1997),
    (r"piano\s*man",                  "Billy Joel", "在世"),
    (r"tormento\s*d'?amore",          "—（现代意大利流行）", None),
    (r"\bchandelier\b",               "Sia / Jesse Shatkin", "在世"),
    (r"xmas\s*mann|morgen\s*kommt\s*der\s*xmas", "—（现代德语流行）", None),
    # ── 2026-09-23 人工复核 ⑤ other 段补入 ──────────────────────────────
    # 判据：作品 20 世纪商业出版，词曲作者仍在保护期内（美国 95 年 / 中国 50 年）。
    # 注意：lakh 文件名普遍带数字后缀（frosty07 / rudolph3），因此**不要用 \b 收尾**
    #       —— '0' 也是 \w，会吃掉词边界。改用可选后缀或直接无边界。
    (r"frosty",                       "Steve Nelson / Jack Rollins 1950", 1983),
    (r"rudolph|rudolf|red[\s-]*nosed\s*reindeer", "Johnny Marks 1949", 1985),
    # 注意：不要用裸 `\bsanta\b` —— 会误伤「Azpiazu Barrio de Santa Cruz」
    #       （古典吉他曲，Santa Cruz 是地名）。只认 Santa Claus / 结尾的 Santa。
    (r"santa\s*claus\s*is\s*com(?:ing|in)|santaclausiscoming|santa\s*is\s*com|santaistill|\bsanta\s*claus|\bsanta\s*$",
     "John Frederick Coots / Haven Gillespie 1934", 1985),
    (r"i\s*saw\s*mo+m?y\s*kissing|saw\s*mother\s*kiss", "Tommie Connor 1952", 1993),
    (r"all\s*i\s*want\s*for\s*christmas", "Mariah Carey / Walter Afanasieff 1994", "在世"),
    (r"last\s*xmas|lastxmas",         "George Michael 1984", 2016),
    (r"merry\s*christmas\s*darling",  "Richard Carpenter / Frank Pooler 1970", "在世"),
    (r"we\s*need\s*a\s*little\s*christmas", "Jerry Herman 1966", 2019),
    (r"nightmare\s*before\s*christmas|nightmarebefore", "Danny Elfman 1993", "在世"),
    (r"mr\.?\s*lawrence",             "坂本龍一 1983", 2023),
    (r"wonderful\s*christmas|wonderfulworldofchristmas", "Paul McCartney 1979", "在世"),
    (r"dominick|italian\s*christmas.?donkey", "Lou Monte / Kelly 1960", "在世"),
    (r"merry\s*christmas\s*everyone", "Shakin' Stevens 1985", "在世"),
    (r"i\s*believe\s*in\s*father\s*christmas", "Greg Lake / Peter Sinfield 1975", 2016),
    (r"christmas\s*without\s*you",    "Kenny Rogers / Dolly Parton", "在世"),
    (r"christmas\s*island",           "Lyle Moraine 1946", 1986),
    (r"little\s*boy\s*that\s*santa\s*claus\s*forgot", "1937 商业曲（作者在保护期）", None),
    (r"fairy\s*on\s*the\s*christmas\s*tree", "1936 英国商业曲（作者在保护期）", None),
    (r"never\s*merry\s*christmas\s*when", "1910 商业曲（作者在保护期）", None),
    (r"everywhere\s*is\s*christmas|heading\s*home\s*for\s*christmas|coming\s*home\s*for\s*christmas|look\s*like\s*christmas|traditions\s*of\s*christmas|wonder\s*of\s*christmas|once\s*upon\s*a\s*christmas|christmas\s*morning|lonely\s*christmas|so\s*it\s*is\s*christmas|father\s*christmas|christmas\s*is\s*coming|keep\s*christmas\s*with\s*you|if\s*every\s*day\s*was\s*like\s*christmas|i\s*wish\s*it\s*could\s*be\s*christmas|crown\s*of\s*rose\s*christmas|christmas\s*im\s*dreaming",
     "—（20/21 世纪现代创作，非传统颂歌）", None),
    (r"grown[\s-]*up\s*christmas\s*list|kelly\s*clarkson", "Mariah Carey / Kelly Clarkson 团队", "在世"),
    (r"give\s*love\s*on\s*christmas\s*day|jackson\s*5", "Jackson 5 / Motown 1970", None),
    (r"christmas\s*polka|jim\s*reeves", "Jim Reeves 1963", 1964),
    (r"hard\s*candy\s*christmas|hardcandychristmas", "—（现代影视配乐）", None),
    (r"snoopy",                       "Vince Guaraldi 1965（史努比圣诞，d.1976）", 1976),
    (r"christmas\s*time",             "Ray Charles / Paul Simon 等现代同名作品", None),
    (r"christmastime\s*is\s*here",    "—（现代创作；疑 Lee Mendelson / Guaraldi）", None),
    (r"ragnarok\s*online",            "游戏配乐（版权属于游戏公司）", None),
    (r"sander\s*van\s*doorn|carol\s*lee", "Sander van Doorn 2011", "在世"),
    (r"christmas\s*eve\s*sarejevo|christmas\s*eve\s*sarajevo", "Trans-Siberian Orchestra / Savatage 1995", "在世"),
    # ── 2026-09-23 内嵌歌词审计补入 ──────────────────────────────────────
    # 来由：审计 2,778 首内嵌歌词时，在 lakh 里发现一批**带歌词的现代作品**
    #       此前被 FALSE_POSITIVE 的 carol/caroline 规则误放行（见 classify 注释）。
    #       这些曲子 MIDI 内嵌的正是现代歌词文本，是歌词版权的真实风险点。
    (r"the\s*christmas\s*song|thechristmassong|christmassong", "Mel Tormé / Robert Wells 1946", 1999),
    (r"baby\s*it'?s\s*cold\s*outside|baby\s*its\s*cold", "Frank Loesser 1944", 1969),
    (r"a\s*lover'?s\s*concerto|lovers?\s*concerto", "Sandy Linzer / Denny Randell 1965（改编自 Bach）", "在世"),
    (r"crystal\s*chandeliers?",       "Ted Harris / Charley Pride 1967", None),
    (r"caballo\s*prieto\s*azabache",  "José Alfredo Jiménez 1947（墨西哥 corrido）", 1973),
    (r"mazurka\s*di\s*periferia|casadei", "Raoul Casadei 1950s（意大利）", 2021),
    # 注意：`home\s*again` 过宽，会误伤传统曲「I'll Take You Home Again Kathleen」(1875)，
    #       故只认 Carole King 那种连写形式 homeagain。
    (r"carole\s*king|caroleking|its\s*too\s*late|it'?s\s*too\s*late|you'?v?e?\s*got\s*a\s*friend|will\s*you\s*love\s*me|so\s*far\s*away|homeagain|i\s*feel\s*the\s*earth\s*move|now\s*and\s*forever",
     "Carole King 等（在世）", "在世"),
    (r"caroli[ne][ae]?\s*in\s*my\s*mind|carolin\w*\s*in\s*the\s*morning|taylor\.\s*carolin|james\s*taylor",
     "James Taylor 1968（在世）", "在世"),
    (r"beatles\s*carol",              "The Beatles（版税方在世）", None),
    (r"tennesse+e\s*waltz|alma\s*cogan", "Pee Wee King / Redd Stewart 1946", 2000),
    (r"hymn\s*4\s*my\s*soul|joe\s*cocker", "Joe Cocker (d.2014)", 2014),
    (r"the\s*lords\s*prayer",         "—（现代配乐改编）", None),
    (r"last\s*waltz\s*of\s*the\s*evening", "—（现代流行）", None),
    (r"time\s*to\s*say\s*goodbye|timetosaygoodbye", "—（现代创作）", None),
    (r"cowgirl\s*de\s*ville|kadison", "—（现代）", None),
    (r"duo\s*din[aâ]mico",            "Duo Dinâmico（葡萄牙，在世）", "在世"),
    (r"a\s*scottish\s*soldier|andy\s*stewart", "Andy Stewart 1961", 1993),
    (r"daddy\s*sang\s*bass|daddysang", "Johnny Cash / Carl Perkins 1968", 2003),
    (r"baroque\s*hoedown",            "Jean-Jacques Perrey / Gershon Kingsley 1967", 2016),
    (r"alunni\s*de[l]?\s*sole|new\s*trolls|signore\s*io\s*sono", "—（1970s 意大利流行/摇滚乐队，在世）", "在世"),
    (r"viadolor",                     "Via Dolorosa（Sandi Patty 1980s，现代）", "在世"),
    (r"crying\s*in\s*the\s*rain",     "已列（Carole King / Greenfield）", None),
]

# ── ② 传统 / 公有领域：保留（并作为排除器白名单） ──────────────────────
TRADITIONAL_PD = [
    (r"carol\s*of\s*the\s*bells|carolof\s*bells|carolbel|carolbl", "乌克兰传统（Leontovych 改编 1916，PD）"),
    (r"we\s*wish\s*you\s*a\s*merry\s*christmas|wewish", "16 世纪英格兰传统（PD）"),
    (r"o(?:h)?\s*christmas\s*tree|ochristmastree", "德国传统 O Tannenbaum（PD）"),
    (r"twelve\s*days\s*of\s*christmas|twelvedays", "英格兰传统（PD）"),
    (r"first\s*noel",                 "16 世纪英格兰传统（PD）"),
    (r"wexford\s*carol",              "爱尔兰传统（PD）"),
    (r"jingle\s*bells|jinglebells",   "Pierpont 1857（PD）"),
    (r"silent\s*night|stille\s*nacht", "Gruber 1818（PD）"),
    (r"adeste\s*fideles|o\s*come\s*all\s*ye", "18 世纪传统（PD）"),
    (r"deck\s*the\s*halls",           "威尔士传统（PD）"),
    (r"angels\s*from\s*the\s*realms", "James Montgomery 1816（PD）"),
    (r"once\s*in\s*royal\s*david'?s\s*city", "传统（PD）"),
    (r"good\s*king\s*wen(?:c|z)eslas", "传统（PD）"),
    (r"god\s*rest\s*ye\s*merry",      "传统（PD）"),
    (r"hark!?\s*the\s*herald",        "Mendelssohn 1840（PD）"),
    (r"joy\s*to\s*the\s*world",       "Handel / Watts（PD）"),
    (r"o\s*little\s*town\s*of\s*bethlehem", "Brooks / Redner 1868（PD）"),
    (r"it\s*came\s*upon\s*the\s*midnight\s*clear", "传统（PD）"),
    (r"coventry\s*carol",             "传统（PD）"),
    (r"sans\s*day\s*carol",           "传统（PD）"),
    (r"sussex\s*carol",               "传统（PD）"),
    (r"boar'?s\s*head\s*carol",       "传统（PD）"),
    (r"holly\s*and\s*the\s*ivy",      "传统（PD）"),
    (r"walking\s*in\s*the\s*air",     "传统（PD）"),
    (r"veni\s*veni\s*emmanuel",       "传统（PD）"),
    (r"dona\s*nobis\s*pacem",         "传统（PD）"),
    (r"patapan|il\s*est\s*ne\s*le\s*divin\s*enfant", "传统（PD）"),
    (r"masters\s*in\s*this\s*hall",   "Cornish 传统（PD）"),
    (r"i\s*saw\s*three\s*ships",      "传统（PD）"),
    (r"what\s*child\s*is\s*this",     "传统（PD）"),
    (r"in\s*dulci\s*jubilo",          "传统（PD）"),
    (r"gabe'?s\s*christmas",           "传统（PD）"),
    (r"es\s*ist\s*ein\s*ros",         "传统（PD）"),
    (r"jolly\s*old\s*saint\s*nicholas", "传统（PD）"),
    (r"amazing\s*grace",              "Newton 1779（PD）"),
    (r"hymn\b",                       "一般赞美诗（PD，且非现代作品名命中）"),
    (r"christmas\s*medley|christmas\s*nr|christmas\s*jam|christmas\s*rhapsody|tchristmas|christmas\s*night|merrychristmas|\bxmas\b|\bnoel\b|caroling|caroloft", "泛指/传统汇编（PD）"),
    # ── 2026-09-23 人工复核 ⑤ other 段补入 ──────────────────────────────
    (r"jingle\s*b|jjjingle",          "Jingle Bells 缩写（Pierpont 1857，PD）"),
    (r"12\s*days|twelve\s*days|12daysof|christmas\s*twelve", "英格兰传统 The Twelve Days of Christmas（PD）"),
    (r"deck\s*the\s*hall",            "威尔士传统（PD）"),
    (r"holy\s*night",                 "Cantique de Noël（Adam 1847，PD）"),
    (r"come\s*all\s*ye\s*faithful|adeste", "18 世纪传统（PD）"),
    (r"what\s*child",                 "What Child Is This（Greensleeves，PD）"),
    (r"heard\s*the\s*bells",          "Longfellow / Baptiste 1872（PD）"),
    (r"care\s*bell|bellcarol|christmas\s*carol.*bell", "Carol of the Bells（乌克兰传统，PD）"),
    (r"1stnoel|first\s*noel|jazzy\s*noel|christmas\s*noel", "The First Noel（16 世纪，PD）"),
    (r"wassail",                      "Wassail / Gloucester 传统（PD）"),
    (r"sing\s*we\s*now\s*of\s*christmas", "传统颂歌（PD）"),
    (r"sugar\s*plu[mn]e|sugarplum",   "糖梅仙子（Tchaikovsky 1892，PD）"),
    (r"christmas\s*tree|christmastree", "O Tannenbaum / 圣诞树主题（PD）"),
    (r"gade",                         "Niels Gade (d.1890) 作品（PD）"),
    (r"christmas\s*carol.*suite|christmas\s*carol\s*suite|a\s*christmas\s*carol\b.*ri",
     "圣诞颂歌组曲（多用传统曲调，PD）"),
    (r"calypso\s*carol",              "以色列传统（PD）"),
    (r"carol\s*of\s*the\s*bells|belcarol", "同上（PD）"),
    (r"christmas\s*carols?|christmas\s*songs?|xmas\s*medley|xmasmedley|xmasmix|christmas\s*carol\b",
     "泛指圣诞颂歌汇编（传统曲调，PD）"),
    # ── 剩余 14 条「泛名」：标题不含任何可识别现代作品 → 按传统处理 ──────
    # 判据：无作者线索、无商业作品对应；宁可保留（本就不含可识别版权内容）。
    (r"^christmas\s*\d*$|^c\s*christmas\s*suite|^xmas\w*$|^home\s*for\s*christmas\d*$|^happy\s*christmas\d*$|^china\s*xmas$|^merry\s*christmas\d*$|^the\s*night\s*before\s*christmas$|^carol\s*~?\d*$|^christmas\s*syn$|^it'?s\s*gonna\s*be\s*a\s*cold\s*christmas$",
     "泛名/不可识别（无对应现代作品，传统处理）"),
]

# ── ③ 正则误命中：保留 ─────────────────────────────────────────────────
FALSE_POSITIVE = [
    (r"caroline|carolina|carolineno", "人名 Caroline / Carolina"),
    (r"carol\s*ann\b|carol\s*ann\s*king", "人名 Carol Ann King"),
    (r"carole\b|caroleking|carole\s*king", "人名 Carole King（姓氏含 carol）"),
    (r"barcarol\b|barcarolle|barcarol\s", "船歌曲式 barcarolle"),
    (r"o'?carolan|carolans\s*concerto", "人名 Turlough O'Carolan"),
    (r"scaroli", "无意义串"),
    (r"carol\s*\d|carol\s*l\b|carols?-?b", "文件名残留"),
    (r"\bcarol\b\s*$", "泛指（无名传统圣诞颂歌）"),
    # ── 2026-09-23 人工复核 ⑤ other 段补入 ──────────────────────────────
    (r"barrio\s*de\s*santa\s*cruz",   "西班牙语地名 Santa Cruz 区（José Azpiazu 吉他曲）"),
    (r"claudio\s*villa|barcarolo",    "意大利歌手 Claudio Villa / 船歌体裁（Barcarolo Romano）"),
    (r"bachovich|barrios?\s*mangore|mangore|barcarol",  "Bachovich / Barrios Mangoré 古典吉他 Barcarola（体裁）"),
    (r"carolan'?s?\s*(?:draught|welcome|concerto|farewell|lament|cup|tune)|o'?\s*carolan|carolan", "Turlough O'Carolan (d.1738) 爱尔兰作曲家"),
    (r"^carol[a-z]*\d*$",             "人名/文件名残留（Carola/Carolien 等）"),
    (r"carolaf|carolien|belcarol|mlchristmas|lacaroln", "人名/无意义串"),
    (r"^happy\s*x?mas|^hapy|^hojo|^w\s*christmas|^merriest|^s\s*di\s*xmas|^\d+\s*xmas|^1lookxmas|^iswthreeships",
     "文件名缩写残留（无可识别作品）"),
]

# 编译后的匹配器（统一大小写不敏感）
MODERN_RE = re.compile("|".join(f"(?:{p})" for p, _a, _d in MODERN_COPYRIGHT), re.I)
TRAD_RE = re.compile("|".join(f"(?:{p})" for p, _d in TRADITIONAL_PD), re.I)
FALSE_RE = re.compile("|".join(f"(?:{p})" for p, _d in FALSE_POSITIVE), re.I)

# ── ④ 艺人 / 团体名：剔除 ──────────────────────────────────────────────
ARTIST_NAMES = [
    (r"\bbeatles\b", "The Beatles"),
    (r"\blennon\b", "John Lennon (d.1980)"),
    (r"\bmccartney\b", "Paul McCartney（在世）"),
    (r"\belvis\b|\bpresley\b", "Elvis Presley (d.1977)"),
    (r"carole\s*king|caroleking", "Carole King（在世）"),
    (r"\bcoldplay\b", "Coldplay（在世）"),
    (r"\bsia\b", "Sia（在世）"),
    (r"celine\s*dion", "Celine Dion（在世）"),
    (r"edith\s*piaf", "Édith Piaf (d.1963)"),
    (r"\bsinatra\b", "Frank Sinatra (d.1998)"),
    (r"james\s*taylor", "James Taylor（在世）"),
    (r"billy\s*joel|\bbillyjoel\b", "Billy Joel（在世）"),
    (r"john\s*denver|\bjdenver\b", "John Denver (d.1997)"),
    (r"neil\s*diamond", "Neil Diamond（在世）"),
    (r"neil\s*sedaka|\bsedaka\b", "Neil Sedaka（在世）"),
    (r"cliff\s*richard", "Cliff Richard（在世）"),
    (r"bachman", "Bachman-Turner Overdrive"),
    (r"everly", "The Everly Brothers"),
    (r"joe\s*cocker", "Joe Cocker (d.2014)"),
    (r"george\s*michael|\bwham\b", "George Michael / Wham! (d.2016)"),
    (r"duo\s*din[aâ]mico", "Duo Dinâmico"),
    (r"pearl\s*jam", "Pearl Jam（在世）"),
    (r"\bnirvana\b", "Nirvana"),
    (r"\babba\b", "ABBA"),
    (r"\bmadonna\b", "Madonna（在世）"),
    (r"\bmariah\b", "Mariah Carey（在世）"),
    (r"bee\s*gees", "Bee Gees"),
    (r"beach\s*boys", "The Beach Boys"),
    (r"bob\s*dylan", "Bob Dylan（在世）"),
    (r"paul\s*simon|garfunkel", "Simon & Garfunkel"),
    (r"springsteen", "Bruce Springsteen（在世）"),
    (r"michael\s*jackson", "Michael Jackson (d.2009)"),
    (r"stevie\s*wonder", "Stevie Wonder（在世）"),
    (r"nat\s*kin|natalie\s*cole|mel\s*torme", "Nat King Cole / Mel Tormé"),
    (r"rolf\s*harris", "Rolf Harris（在世）"),
    (r"gene\s*raskin", "Gene Raskin (d.2004)"),
    (r"sonny\s*rollins", "Sonny Rollins（在世）"),
    (r"peter\s*yarrow|mary\s*travers|paul\s*stookey|milton\s*okun", "Peter, Paul and Mary 改编者"),
    (r"huddie\s*ledbetter|\bledbetter\b", "Lead Belly (d.1949)"),
    (r"atkins\b.*jazz", "—"),
    (r"hunter\.?jazz", "—"),
]
ARTIST_RE = re.compile("|".join(f"(?:{p})" for p, _n in ARTIST_NAMES), re.I)


# ── ⑤ 现代艺人 / 游戏 / 商业包**目录**：整目录剔除 ──────────────────────
# 来由：lakh 的路径里大量以艺人/乐队/游戏/商业 MIDI 包命名一级目录，标题本身
# 完全看不出是版权作品（如 `BachmanTurnerOverdrive/Hey You.mid`、`F/Fire Emblem …`）。
# 只排除**具名**目录 —— 单字母桶（c/m/f/j/C/F/J/M）实测是混合桶
# （含 Cherubichymn/mozk310a/fuguein2 等古典与赞美诗），**不可整桶剔除**。
MODERN_DIRS = {
    # 摇滚 / 金属 / 流行乐队
    "sonata arctica", "symphonyx", "stratovarius", "graveworm", "falkenbach",
    "megadeth", "megadeth midi", "metallica", "queen", "queen midi pack",
    "cranberries", "verve", "verve pipe, the", "blink182", "beatles", "beach boys",
    "supremes", "jethro-tull", "yes", "zappa frank", "zappa, frank & fairport convention",
    "police", "cultureclub", "folk implosion", "perplexer", "blue system", "gazebo",
    "eav (erste allgemeine verunsicherung)", "883", "dc talk", "bob dylan",
    "bachman turner overdrive", "bachmanturneroverdrive", "status quo", "elvis",
    # 流行 / 乡村 / 爵士艺人
    "joel_billy", "joel, billy", "caroleking", "mariahcarey", "celine",
    "rodstewart", "andywilliams", "ronny", "harrychapin", "bjork",
    "crosbystillsnashuand;young", "cole, nat 'king'", "cogan, alma",
    "morgan, lorrie", "morgan, george", "morgan, michael", "tubb, ernest",
    "jennings, waylon", "fogelberg, dan", "williams, mason", "mason willams",
    "stewart, james", "noble, ray", "walton, cedar", "corea, chick", "ciani, suzanne",
    "oldfield, mike", "rieu, andre", "brassens georges", "biste, paul",
    "butler, henry", "humperdinck, engelbert", "bacharach, burt", "burtbacharach",
    "grant & forsyth", "disney", "music instructor", "reprogrammed",
    # 游戏 / 影视 / 商业包 / 铃声 / 爵士扒带站
    "castlevania", "fire emblem", "final_fantasy_three",
    "003 commercial midis-teamtnd [02.15.0", "commercial midi pack 002",
    "kids midi", "polyphone ringtones 2", "poliphone ringtones",
    "jazz_www.thejazzpage.de_midirip",
    # 电视/流行来源
    "australian traditional",
}

# 卒年下限：晚于此年的作曲家，其作品按仍受保护处理（美国 PD 截止线 1928）
COMPOSER_DEATH_CUTOFF = 1928

# 卒年晚于 PD 截止线的作曲家 —— 用**正则片段**而非全名。
# ⚠️ 全名匹配会漏两种常见写法（实测漏掉 5 首）：
#   ① 语序：数据里常见「Bolling, Claude」而词表写「Claude Bolling」
#   ② 分隔符：路径写「Villa_Lobos_Etude」「Siloti, Alexander」
#   故这里只锚定**姓氏/独特词**，并允许任意分隔。
LATE_COMPOSER_PATTERNS = [
    (r"villa[\s_\-]*lobos|villalobos",        "Heitor Villa-Lobos",    1959),
    (r"prokofiev|prokofiew",                  "Sergei Prokofiev",      1953),
    (r"rachmanin(?:ov|off)",                  "Sergei Rachmaninov",    1943),
    (r"shostakovich|schostakowitsch",         "Dmitri Shostakovich",   1975),
    (r"chaminade",                            "Cécile Chaminade",      1944),
    (r"leh[aá]r",                             "Franz Lehár",           1948),
    (r"bolling",                              "Claude Bolling",        1999),
    (r"ginastera",                            "Alberto Ginastera",     1983),
    (r"cedar\s+walton|walton,?\s+cedar",      "Cedar Walton",          1983),
    (r"\bcorea\b",                            "Chick Corea",           2021),
    (r"bacharach",                            "Burt Bacharach",        2023),
    (r"siloti",                               "Alexander Siloti",      1945),
]
LATE_COMPOSER_RE = re.compile(
    "|".join(f"(?:{p})" for p, _n, _d in LATE_COMPOSER_PATTERNS), re.I)

# 向后兼容：名字 → 卒年（供需要精确卒年的调用方）
LATE_COMPOSER_NAMES = {n.lower(): d for _p, n, d in LATE_COMPOSER_PATTERNS}


def composer_is_copyrighted(r: dict) -> tuple[bool, str]:
    """作曲家卒年是否晚于 PD 截止线。返回 (是否受保护, 说明)。"""
    for src in (r, r.get("extra") or {}):
        d = src.get("death")
        if isinstance(d, int) and d > COMPOSER_DEATH_CUTOFF:
            return True, f"卒年 {d} > {COMPOSER_DEATH_CUTOFF}"
    name = ((r.get("composer_name") or "") + " " + (r.get("composer_slug") or "")).replace("-", " ")
    m = LATE_COMPOSER_RE.search(name)
    if m:
        return True, f"作曲家人名命中「{m.group(0)}」"
    return False, ""


# 通用路径分量（不是艺人名，跳过）
GENERIC_DIRS = {"", "sources", "lakh", "midi", "mid"}


def dir_hit(parts) -> str:
    """在目录分量列表中找出命中 `MODERN_DIRS` 的那一个（无则返回空串）。

    ⚠️ **不能假设固定层级**：jsonl 的 `src_path` 写作 `sources/lakh/<X>/…`，
    而 `sources/lakh/md5_to_paths.json` 里存的是 `<X>/…`（无前缀）。
    固定取 `parts[2]` 会在后者上错位——曾因此让 96 首现代作品的目录信号失效。
    故这里扫描**所有目录分量**（排除通用分量与文件名本身）。
    """
    for p in parts:
        d = str(p).strip().lower()
        if d in GENERIC_DIRS:
            continue
        if d in MODERN_DIRS:
            return d
    return ""


def top_dir(r: dict) -> str:
    """从记录取「命中 MODERN_DIRS 的目录名」（无则空串）。"""
    sp = (r.get("src_path") or "").replace("\\", "/")
    return dir_hit(sp.split("/")[:-1])


def classify_record(r: dict) -> str:
    """在 classify(title) 之外，叠加**目录**与**作曲家卒年**两个信号。

    这是 2026-09-23 第二轮排查新增的：仅看标题会漏掉 `BachmanTurnerOverdrive/Hey You`、
    `F/Fire Emblem …`、`ELVIS/Blue 2` 这类「标题干净、路径暴露身份」的现代作品。

    两个信号的强度不同：
      · **目录信号一律生效** —— 目录名是结构性证据（整个 `Beatles/` 目录都是披头士）。
      · **卒年信号只在标题未判为 traditional / false-positive 时生效** ——
        否则会被脏元数据误伤：如「Amazing Grace」(Newton 1779, PD) 的 composer 字段
        被填成乐团名「The Scottish Military Band」(d.1945)，按卒年就会被错杀。
    """
    base = classify(r.get("title") or "")
    if base in ("modern", "artist"):
        return base
    if top_dir(r) in MODERN_DIRS:
        return "modern-dir"
    if base not in ("traditional", "false-positive"):
        hit, _why = composer_is_copyrighted(r)
        if hit:
            return "modern-composer"
    return base


def classify(title: str) -> str:
    """返回 'modern' | 'traditional' | 'false-positive' | 'artist' | 'other'。

    判定顺序很重要（三次踩坑实测），**MODERN → ARTIST → TRAD → FALSE**：
      ① MODERN 若排在 FALSE 之后 —— FALSE_POSITIVE 里宽泛的 `caroline|carolina|carol`
         会吃掉真正的现代作品，漏掉「James Taylor Caroline in My Mind」「Neil Diamond
         Sweet Caroline」「Neil Sedaka Oh Carol」「Carole King ...」一整批。
      ② MODERN 若排在 TRAD 之后 —— TRAD 的兜底词 `hymn\\b`、`tchristmas`、`\\bxmas\\b`
         会吞掉「joecocker hymn」「Thechristmassong」等现代作品。
      ③ **ARTIST 若排在 TRAD 之后** —— TRAD 的 `\\bxmas\\b` 会把「John Lennon Xmas」
         判成 traditional 而放行（真实漏网，第二轮排查发现）。
    """
    t = title or ""
    if MODERN_RE.search(t):
        return "modern"
    if ARTIST_RE.search(t):
        return "artist"
    if TRAD_RE.search(t):
        return "traditional"
    if FALSE_RE.search(t):
        return "false-positive"
    return "other"
