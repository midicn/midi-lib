#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""region 推导与归一化（纯本地 · dry-run 先行 · 不覆盖已有值）

三步：
  1) 归一化：无歧义国籍形容词 → 中文国名（German→德国 等；地区名如 Lothringen 保留不动）
  2) 来源级：thesession→爱尔兰（TheSession 数据集即爱尔兰传统音乐库，与 norbeck 口径一致）·
     nottingham→英国（Nottingham ABC 曲集=英国民间舞蹈音乐）
  3) 作曲家映射：composer_slug → 中文国名。**只写 100% 确定的音乐史常识项**，
     不确定的（giantmidi 当代钢琴家、groove 鼓手、emopia unknown、oga 游戏作者）一律留空不猜。

红线：未知留空不猜 · 不覆盖已有 region 值 · 值域用中文国名（与 norbeck/abcmisc 一致）。
"""
from __future__ import annotations
import argparse, json, sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACKS = ROOT / 'midi_db' / 'tracks'

# ── 1) 无歧义国籍形容词归一化（en/nationality adjective → 中文国名）──
NORM = {
    'German': '德国', 'French': '法国', 'American': '美国', 'British': '英国',
    'Russian': '俄罗斯', 'Italian': '意大利', 'Austrian': '奥地利', 'Spanish': '西班牙',
    'Polish': '波兰', 'Hungarian': '匈牙利', 'Belgian': '比利时', 'Norwegian': '挪威',
    'Bulgaria': '保加利亚', 'Serbia': '塞尔维亚', 'Romania': '罗马尼亚',
    'Macedonia': '北马其顿', 'klezmer': '克莱兹梅尔', 'Klezmer': '克莱兹梅尔',
}

# ── 2) 来源级默认（数据集本身的定义，非猜测）──
SOURCE_REGION = {
    'thesession': '爱尔兰',      # TheSession-data = 爱尔兰传统音乐数据库（norbeck 同口径）
    'nottingham': '英国',        # Nottingham Music Database = 英国民间舞蹈音乐 ABC
}

# ── 3) 作曲家 slug → 中文国名（100% 确定项；不确定的不写）──
COMPOSER_REGION = {
    # 巴洛克与古典核心
    'bach': '德国', 'johann-sebastian-bach': '德国', 'j-s-bach': '德国',
    'mozart': '奥地利', 'wolfgang-amadeus-mozart': '奥地利', 'w-a-mozart': '奥地利',
    'beethoven': '德国', 'ludwig-van-beethoven': '德国',
    'haydn': '奥地利', 'joseph-haydn': '奥地利', 'f-j-haydn': '奥地利',
    'schubert': '奥地利', 'franz-schubert': '奥地利',
    'handel': '德国', 'g-f-h-ndel': '德国', 'gfhandel': '德国', 'george-frideric-handel': '德国',
    'vivaldi': '意大利', 'antonio-vivaldi': '意大利',
    'corelli': '意大利', 'arcangelo-corelli': '意大利',
    'scarlatti': '意大利', 'domenico-scarlatti': '意大利', 'alessandro-scarlatti': '意大利',
    'purcell': '英国', 'henry-purcell': '英国',
    'telemann': '德国', 'georg-philipp-telemann': '德国',
    'rameau': '法国', 'jean-philippe-rameau': '法国',
    'couperin': '法国', 'francois-couperin': '法国',
    'palestrina': '意大利', 'giovanni-pierluigi-da-palestrina': '意大利',
    'monteverdi': '意大利', 'claudio-monteverdi': '意大利',
    'lully': '法国', 'jean-baptiste-lully': '法国',
    'buxtehude': '德国', 'dieterich-buxtehude': '德国',
    'albinoni': '意大利', 'tomaso-albinoni': '意大利',
    'marcello': '意大利', 'cpe-bach': '德国', 'carl-philipp-emanuel-bach': '德国',
    'jc-bach': '德国', 'jf-bach': '德国', 'wf-bach': '德国',
    'soler': '西班牙', 'antonio-soler': '西班牙',
    # 浪漫派
    'chopin': '波兰', 'frederic-chopin': '波兰', 'f-chopin': '波兰',
    'liszt': '匈牙利', 'franz-liszt': '匈牙利',
    'schumann': '德国', 'robert-schumann': '德国',
    'schumann-clara': '德国', 'clara-schumann': '德国',
    'mendelssohn': '德国', 'felix-mendelssohn': '德国', 'mendelssohn-bartholdy': '德国',
    'brahms': '德国', 'johannes-brahms': '德国', 'j-brahms': '德国',
    'bruckner': '奥地利', 'anton-bruckner': '奥地利',
    'mahler': '奥地利', 'gustav-mahler': '奥地利',
    'wagner': '德国', 'richard-wagner': '德国',
    'verdi': '意大利', 'giuseppe-verdi': '意大利',
    'puccini': '意大利', 'giacomo-puccini': '意大利',
    'rossini': '意大利', 'gioachino-rossini': '意大利',
    'donizetti': '意大利', 'gaetano-donizetti': '意大利',
    'bellini': '意大利', 'vincenzo-bellini': '意大利',
    'bizet': '法国', 'georges-bizet': '法国',
    'berlioz': '法国', 'hector-berlioz': '法国',
    'gounod': '法国', 'charles-gounod': '法国',
    'offenbach': '法国', 'jacques-offenbach': '法国',
    'saint-saens': '法国', 'camille-saint-saens': '法国',
    'faure': '法国', 'gabriel-faure': '法国', 'gabriel-fauré': '法国',
    'ravel': '法国', 'maurice-ravel': '法国',
    'debussy': '法国', 'claude-debussy': '法国',
    'chaminade': '法国', 'cecile-chaminade': '法国',
    'cesar-franck': '比利时', 'franck': '比利时',
    'lalo': '法国', 'edouard-lalo': '法国',
    'massenet': '法国', 'jules-massenet': '法国',
    'dukas': '法国', 'paul-dukas': '法国',
    'tchaikovsky': '俄罗斯', 'pyotr-tchaikovsky': '俄罗斯', 'tschaikowsky': '俄罗斯',
    'rachmaninoff': '俄罗斯', 'sergei-rachmaninoff': '俄罗斯', 'rachmaninov': '俄罗斯',
    'scriabin': '俄罗斯', 'alexander-scriabin': '俄罗斯',
    ' Mussorgsky': '俄罗斯', 'mussorgsky': '俄罗斯', 'modest-mussorgsky': '俄罗斯',
    'rimsky-korsakov': '俄罗斯', 'nikolai-rimsky-korsakov': '俄罗斯',
    'borodin': '俄罗斯', 'alexander-borodin': '俄罗斯',
    'glinka': '俄罗斯', 'mikhail-glinka': '俄罗斯',
    'balakirev': '俄罗斯', 'lyadov': '俄罗斯', 'arends': '俄罗斯',
    'prokofiev': '俄罗斯', 'sergei-prokofiev': '俄罗斯',
    'shostakovich': '俄罗斯', 'dmitri-shostakovich': '俄罗斯',
    'dvorak': '捷克', 'antonin-dvorak': '捷克', 'dvořák': '捷克',
    'smetana': '捷克', 'bedrich-smetana': '捷克',
    'janacek': '捷克', 'leos-janacek': '捷克',
    'grieg': '挪威', 'edvard-grieg': '挪威',
    'sibelius': '芬兰', 'jean-sibelius': '芬兰',
    'elgar': '英国', 'edward-elgar': '英国',
    'holst': '英国', 'gustav-holst': '英国',
    'vaughan-williams': '英国', 'ralph-vaughan-williams': '英国',
    'britten': '英国', 'benjamin-britten': '英国',
    'stanford': '英国', 'charles-villiers-stanford': '英国',
    'parry': '英国', 'hubert-parry': '英国',
    'sullivan': '英国', 'arthur-sullivan': '英国',
    'brahms-j': '德国',
    'hugo-wolf': '奥地利',
    'bruch': '德国', 'max-bruch': '德国',
    'reincke': '德国', 'carl-reinecke': '德国', 'reinecke': '德国',
    'schoenberg': '奥地利', 'arnold-schoenberg': '奥地利', 'schonberg': '奥地利',
    'alban-berg': '奥地利',
    'webern': '奥地利', 'anton-webern': '奥地利',
    'kreisler': '奥地利', 'fritz-kreisler': '奥地利',
    'lehar': '奥地利', 'franz-lehar': '奥地利',
    'suppe': '奥地利', 'franz-von-suppe': '奥地利',
    'johann-strauss': '奥地利', 'strauss-j': '奥地利', 'j-strauss': '奥地利',
    'richard-strauss': '德国', 'r-strauss': '德国', 'strauss-r': '德国',
    'lehmann': '英国', 'liza-lehmann': '英国',
    'albeniz': '西班牙', 'isaac-albniz': '西班牙', 'isaac-albeniz': '西班牙',
    'granados': '西班牙', 'enrique-granados': '西班牙',
    'de-falla': '西班牙', 'manuel-de-falla': '西班牙', 'falla': '西班牙',
    'tárrega': '西班牙', 'tarrega': '西班牙', 'francisco-tarrega': '西班牙',
    'sor': '西班牙', 'fernando-sor': '西班牙',
    'aguado': '西班牙', 'dionisio-aguado': '西班牙',
    'pagannini': '意大利', 'paganini': '意大利', 'niccolo-paganini': '意大利',
    'giuliani': '意大利', 'mauro-giuliani': '意大利',
    'carulli': '意大利', 'ferdinando-carulli': '意大利',
    'carcassi': '意大利', 'matteo-carcassi': '意大利',
    'veracini': '意大利', 'locatelli': '意大利', 'pietro-locatelli': '意大利',
    'tartini': '意大利', 'giuseppe-tartini': '意大利',
    'boccherini': '意大利', 'luigi-boccherini': '意大利',
    'clementi': '意大利', 'muzio-clementi': '意大利',
    'cherubini': '意大利', 'luigi-cherubini': '意大利',
    'donizetti-b': '意大利',
    'cesar-cui': '俄罗斯',
    'mertz-j-k': '匈牙利', 'mertz': '匈牙利', 'johann-kaspar-mertz': '匈牙利',
    'bartok': '匈牙利', 'bela-bartok': '匈牙利', 'b-artok': '匈牙利',
    'kodaly': '匈牙利', 'zoltan-kodaly': '匈牙利',
    'dohnanyi': '匈牙利', 'ernst-von-dohnanyi': '匈牙利',
    'lehar-f': '奥地利',
    'liszt-f': '匈牙利',
    'moniuszko': '波兰', 'stanislaw-moniuszko': '波兰',
    'wieniawski': '波兰', 'henryk-wieniawski': '波兰',
    'paderewski': '波兰', 'ignacy-paderewski': '波兰',
    'szymanowski': '波兰', 'karol-szymanowski': '波兰',
    'gottschalk': '美国', 'louis-moreau-gottschalk': '美国',
    'mcdowell': '美国', 'edward-macdowell': '美国',
    'ives': '美国', 'charles-ives': '美国',
    'gershwin': '美国', 'george-gershwin': '美国',
    'copland': '美国', 'aaron-copland': '美国',
    'beach': '美国', 'amy-beach': '美国',
    'joplin': '美国', 'scott-joplin': '美国',
    'stephen-foster': '美国', 'stephen-collins-foster': '美国',
    'sousa': '美国', 'john-philip-sousa': '美国',
    ' bernstein': '美国', 'leonard-bernstein': '美国',
    'griffes': '美国', 'charles-tomlinson-griffes': '美国',
    'grieg-e': '挪威',
    'satie': '法国', 'erik-satie': '法国',
    'martini': '意大利', 'padre-martini': '意大利',
    # 练习曲/教学法名家
    'czerny': '奥地利', 'carl-czerny': '奥地利',
    'cramer': '德国', 'johann-baptist-cramer': '德国',
    'clementi-f': '意大利',
    'kohlerr': '德国', 'kohler': '德国', 'louis-kohler': '德国',
    'heller': '匈牙利', 'stephen-heller': '匈牙利',
    'burgmuller': '德国', 'friedrich-burgmuller': '德国', 'burgmller': '德国',
    'hanon': '法国', 'charles-louis-hanon': '法国',
    'diabelli': '奥地利', 'anton-diabelli': '奥地利',
    'kuhlau': '丹麦', 'friedrich-kuhlau': '丹麦',
    'moscheles': '捷克', 'ignaz-moscheles': '捷克',
    'hummel': '奥地利', 'johann-nepomuk-hummel': '奥地利',
    'john-field': '爱尔兰',
    'duvernoy': '法国', 'jean-baptiste-duvernoy': '法国',
    ' bertini': '法国', 'bertini': '法国', 'henri-bertini': '法国',
    'loeschhorn': '德国', 'carl-albert-loeschhorn': '德国',
    'gurlitt': '德国', 'cornelius-gurlitt': '德国',
    'streabbog': '比利时', 'louis-streabbog': '比利时',
    # 浪漫后期/现代（确定项）
    'sinding': '挪威', 'christian-sinding': '挪威',
    'macdowell-e': '美国',
    'ornstein': '美国', 'leo-ornstein': '美国',
    'granados-e': '西班牙',
    'moszkowski': '波兰', 'moritz-moszkowski': '波兰',
    'scharwenka': '波兰', 'xaver-scharwenka': '波兰',
    'stanchinsky': '俄罗斯', 'aleksei-stanchinsky': '俄罗斯',
    'rosenthal': '波兰', 'moriz-rosenthal': '波兰',
    'friedman': '波兰', 'ignaz-friedman': '波兰',
    'godowsky': '波兰', 'leopold-godowsky': '波兰',
    'tauskig': '波兰', 'tausig': '波兰', 'carl-tausig': '波兰',
    'schytte': '丹麦', 'ludvig-schytte': '丹麦',
    'concone': '意大利', 'giuseppe-concone': '意大利',
    'panofka': '德国', 'heinrich-panofka': '德国',
    'marchesi': '德国', 'mathilde-marchesi': '德国',
    'vaccai': '意大利', 'nicola-vaccai': '意大利',
    'giuseppe-seidler': '德国',
    'abt': '德国', 'franz-abt': '德国',
    # 圣诗作曲家（cyberhymnal 高频 · 全部为确定的美国圣诗名家）
    'charles-hutchinson-gabriel': '美国',
    'william-james-kirkpatrick': '美国', 'kirkpatrick': '美国',
    'john-robson-sweney': '美国', 'sweney': '美国',
    'william-howard-doane': '美国', 'doane': '美国',
    'robert-lowry': '美国', 'lowry': '美国',
    'daniel-brink-towner': '美国', 'towner': '美国',
    'james-mcgranahan': '美国', 'mcgranahan': '美国',
    'ira-david-sankey': '美国', 'sankey': '美国',
    'lowell-mason': '美国', 'mason-lowell': '美国', 'adam-geibel': '美国', 'geibel': '美国',
    'george-coles-stebbins': '美国', 'stebbins': '美国',
    'peter-philip-bilhorn': '美国', 'bilhorn': '美国',
    'joseph-lincoln-hall': '美国', 'john-h-stockton': '美国', 'stockton': '美国',
    'william-g-fischer': '美国', 'fischer': '美国',
    'john-r-sweney': '美国',
    'howard-e-smith': '美国',
    'e-o-excell': '美国', 'excell': '美国',
    'charles-converse': '美国', 'converse': '美国',
    'john-b-dykes': '英国', 'dykes': '英国',
    'william-h-monk': '英国', 'monk': '英国',
    'henry-t-smart': '英国', 'smart': '英国',
    'arthur-s-sullivan': '英国', 's-sullivan': '英国',
    'john-zundel': '德国', 'zundel': '德国',
    'conrad-kocher': '德国', 'kocher': '德国',
    'hans-georg-nagli': '瑞士', 'nagli': '瑞士',
    'george-j-elvey': '英国', 'elvey': '英国',
    'samuel-s-wesley': '英国', 'wesley-s-s': '英国',
    'edward-hodges': '英国', 'hodges': '英国',
    'felix-mendelssohn-b': '德国',
    'joseph-haydn-b': '奥地利',
    'john-newton-w': '英国',
    'joseph-m-scriven': '加拿大', 'scriven': '加拿大',
    'rowland-prichard': '英国', 'prichard': '英国',
    'evan-h-lewis': '美国',
    'james-walch': '英国', 'walch': '英国',
    'frederick-c-maker': '英国', 'maker': '英国',
    'william-b-bradbury': '美国', 'bradbury': '美国',
    'thomas-c-oleary': '美国', 'oleary': '美国',
    'anthony-j-showalter': '美国', 'showalter': '美国',
    'charles-h-gabriel': '美国',
    'h-r-palmer': '美国', 'horatio-r-palmer': '美国',
    'john-r-sweneys': '美国',
    'george-f-root': '美国', 'root': '美国', 'george-root': '美国',
    'henry-j-gauntlett': '英国', 'gauntlett': '英国',
    'john-bacchus-dykes': '英国',
    'william-h-havergal': '英国', 'havergal': '英国',
    'arthur-h-messiter': '英国', 'samuel-smith-h': '英国',
    ' felix-mendelssohn-b': '德国',
    # 现代具体人物（giantmidi 等确定项）
    'joplin-s': '美国',
    'granados-p': '西班牙',
    'albniz-i': '西班牙',
    'mompou': '西班牙', 'frederic-mompou': '西班牙',
    'victoria': '西班牙', 'tomas-luis-de-victoria': '西班牙',
    'morales': '西班牙', 'cristobal-de-morales': '西班牙',
    'guerrero': '西班牙', 'francisco-guerrero': '西班牙',
    'encina': '西班牙', 'juan-del-encina': '西班牙',
    'milan': '西班牙', 'luis-milan': '西班牙',
    'narvaez': '西班牙', 'luis-de-narvaez': '西班牙',
    'sanzz': '西班牙', 'sanz': '西班牙', 'gaspar-sanz': '西班牙',
    'cabezón': '西班牙', 'cabezon': '西班牙', 'antonio-de-cabezon': '西班牙',
    # 吉他浪漫派补充
    'horetzky': '波兰', 'felix-horetzky': '波兰',
    'legnani': '意大利', 'luigi-legnani': '意大利',
    'regondi': '意大利', 'giulio-regondi': '意大利',
    'coste': '法国', 'napoleon-coste': '法国',
    'call': '奥地利', 'leonhard-von-call': '奥地利',
    'arcas': '西班牙', 'julian-arcas': '西班牙',
    'jose-ferrer': '西班牙', # openscore/lieder 补充（确定项）
    'franz': '德国', 'robert-franz': '德国',
    'kinkel': '德国', 'johanna-kinkel': '德国',
    'reichardt': '德国', 'louise-reichardt': '德国',
    'peter-cornelius': '德国',
    'hensel': '德国', 'fanny-mendelssohn-hensel': '德国',
    'jensen': '德国', 'adolf-jensen': '德国',
    'lichtenthal': '德国',
    'taubert': '德国', 'karl-taubert': '德国', 'wilhelm-taubert': '德国',
    'gade': '丹麦', 'niels-gade': '丹麦',
    'kjerulf': '挪威', 'halfdan-kjerulf': '挪威',
    'soderman': '瑞典', 'august-sderman': '瑞典', 'sderman': '瑞典',
    'norlind': '瑞典',
    'smit': '荷兰', 'smeets': '荷兰',
    'rummel': '德国', 'christian-rummel': '德国',
    'faisst': '德国', 'immanuel-faisst': '德国',
    'holms': '法国', 'theodor-holms': '法国',
    'josephine-lang': '奥地利',
    'kohler-l': '丹麦',
    'graben-hoffmann': '德国', 'grabenhoffmann': '德国',
    'schulz': '德国', 'johann-abraham-peter-schulz': '德国',
    'zelter': '德国', 'carl-friedrich-zelter': '德国',
    'reichardt-j-f': '德国', 'johann-friedrich-reichardt': '德国',
    'zumsteeg': '德国', 'emilie-zumsteeg': '德国',
    'carl-maria-von-weber': '德国',
    'spohr': '德国', 'louis-spohr': '德国',
    'molique': '德国', 'wilhelm-molique': '德国',
    'riedel': '德国',
    'kroll': '德国', 'william-kroll': '德国',
    'regnard': '法国',
    'widor': '法国', 'charles-marie-widor': '法国',
    'gigout': '法国', 'eugene-gigout': '法国',
    'franck-e': '比利时',
    'guilmant': '法国', 'alexandre-guilmant': '法国',
    'boellmann': '法国', 'leon-boellmann': '法国',
    'viernes': '法国', 'louis-vierne': '法国', 'vierne': '法国',
    'lefebure-wely': '法国', 'wely': '法国',
    'batiste': '法国',
    # m21 补充
    'anonymous-trecento': '意大利',   # trecento=意大利 14 世纪音乐史时期（匿名但地域明确）
    'various-demos': None, 'theoryexercises': None, 'various-leadsheets': None,
    # musicnet 补充
    'cambini': '意大利', 'giuseppe-maria-cambini': '意大利',
    # aria/其它高频
    'moszkowski-m': '波兰',
    'rubinstein': '俄罗斯', 'anton-rubinstein': '俄罗斯',
    'arends-r': '俄罗斯',
    'bunin': '俄罗斯',
    'medtner': '俄罗斯', 'nikolai-medtner': '俄罗斯',
    'balakirev-m': '俄罗斯',
    'glazunov': '俄罗斯', 'alexander-glazunov': '俄罗斯',
    'glinka-m': '俄罗斯',
    'kabalevsky': '俄罗斯', 'dmitri-kabalevsky': '俄罗斯',
    'taneev': '俄罗斯', 'sergei-taneev': '俄罗斯',
    'lyapunov': '俄罗斯', 'sergei-lyapunov': '俄罗斯',
    ' mily-balakirev': '俄罗斯',
    'nanini': '意大利',
    'giovannelli': '意大利', 'ruggero-giovannelli': '意大利',
    'merulo': '意大利', 'claudio-merulo': '意大利',
    'andrea-gabrieli': '意大利', 'gabrieli-andrea': '意大利',
    'gabrieli-giovanni': '意大利', 'giovanni-gabrieli': '意大利',
    'frescobaldi': '意大利', 'girolamo-frescobaldi': '意大利',
    'cavazzoni': '意大利',
    'valente': '意大利', 'antonio-de-cabezn': '西班牙',
    'william-byrd': '英国',
    'gibbons': '英国', 'orlando-gibbons': '英国',
    'tomkins': '英国', 'thomas-tomkins': '英国',
    'bull': '英国', 'john-bull': '英国',
    'farnaby': '英国', 'giles-farnaby': '英国',
    'sweelinck': '荷兰', 'jan-pieterszoon-sweelinck': '荷兰',
    'beros': '荷兰',
    'reincken': '德国', 'johann-adam-reincken': '德国',
    'grigny': '法国', 'nicolas-de-grigny': '法国',
    'marchand': '法国', 'louis-marchand': '法国',
    'clrambault': '法国', 'clrambault-l': '法国', 'louis-clrambault': '法国',
    'dandrieu': '法国', 'jean-francois-dandrieu': '法国',
    'corrette': '法国', 'michel-corrette': '法国',
    'dufsour': '法国',
    'balbastre': '法国', 'claude-balbastre': '法国',
    'dandrieu-j-f': '法国',
    'charpentier': '法国', 'marc-antoine-charpentier': '法国',
    'campra': '法国', 'andr-campra': '法国', 'andrcampra': '法国',
    'destouches': '法国',
    'mondonville': '法国', 'jean-joseph-mondonville': '法国',
    'rebels': '法国', 'jean-fry-rebels': '法国',
    'boismortier': '法国', 'joseph-bodin-de-boismortier': '法国',
    'leclair': '法国', 'jean-marie-leclair': '法国',
    'blavet': '法国', 'michel-blavet': '法国',
    'guillemain': '法国',
    'pla': '法国',
    'gedalge': '法国',
    'heller-s': '法国',
    'dupr': '法国', 'marcel-dupr': '法国',
    'tournemire': '法国',
    'alain': '法国', 'jehan-alain': '法国',
    'langlais': '法国', 'jean-langlais': '法国',
    'durufle': '法国', 'maurice-durufle': '法国',
    'messiaen': '法国', 'olivier-messiaen': '法国',
    'poulenc': '法国', 'francis-poulenc': '法国',
    'hahn': '法国', 'reynaldo-hahn': '法国',
    'hahn-reynaldo': '法国',
    'chas-parry': '英国',
    'ireland': '英国', 'john-ireland': '英国',
    'bax': '英国', 'arnold-bax': '英国',
    'bliss': '美国', 'arthur-bliss': '英国',
    'william-walton': '英国',
    'finzi': '英国', 'gerald-finzi': '英国',
    'delius': '英国', 'frederick-delius': '英国',
    'quilter': '英国', 'roger-quilter': '英国',
    'bridge': '英国', 'frank-bridge': '英国',
    'duparc': '法国', 'henri-duparc': '法国',
    'chausson': '法国', 'ernest-chausson': '法国',
    'dindy': '法国', 'vincent-dindy': '法国', 'indy': '法国',
    'satie-e': '法国',
    'ganne': '法国', 'louis-ganne': '法国',
    'planquette': '法国',
    'audran': '法国', 'edmond-audran': '法国',
    'lecoq': '法国', 'charles-lecoq': '法国',
    # ── 第二轮扩充（v1.21 · 仅 100% 确定项）──
    # aria 高频（古典/近现代钢琴名家）
    'alkan': '法国', 'charles-valentin-alkan': '法国',
    'kapustin': '俄罗斯', 'nikolai-kapustin': '俄罗斯',
    'barber': '美国', 'samuel-barber': '美国',
    'bortkiewicz': '乌克兰', 'sergei-bortkiewicz': '乌克兰',
    'glass': '美国', 'philip-glass': '美国',
    'turina': '西班牙', 'joaquin-turina': '西班牙',
    'thalberg': '瑞士', 'sigismond-thalberg': '瑞士',
    'reger': '德国', 'max-reger': '德国',
    'grechaninov': '俄罗斯', 'alexander-grechaninov': '俄罗斯',
    'bowen': '英国', 'york-bowen': '英国',
    'busoni': '意大利', 'ferruccio-busoni': '意大利',
    'blumenfeld': '乌克兰', 'felix-blumenfeld': '乌克兰',
    'pejacevic': '克罗地亚', 'dora-pejacevic': '克罗地亚',
    'beyer': '德国', 'ferdinand-beyer': '德国',
    'bonis': '法国', 'mel-bonis': '法国',
    'cimarosa': '意大利', 'domenico-cimarosa': '意大利',
    'goedicke': '俄罗斯', 'alexander-goedicke': '俄罗斯',
    'farrenc': '法国', 'louise-farrenc': '法国',
    'maykapar': '俄罗斯', 'samuel-maykapar': '俄罗斯',
    'gliere': '乌克兰', 'reinhold-gliere': '乌克兰',
    'macdowell': '美国', 'edward-macdowell': '美国',
    'merikanto': '芬兰', 'oskar-merikanto': '芬兰',
    'ligeti': '匈牙利', 'gyorgy-ligeti': '匈牙利',
    'yoshimatsu': '日本', 'takashi-yoshimatsu': '日本',
    # cyberhymnal 全名圣诗名家（美国为主）
    'lorenz': '美国', 'ellen-jane-lorenz': '美国',
    'william-batchelder-bradbury': '美国',
    'george-frederick-root': '美国',
    'bentley-deforest-ackley': '美国', 'ackley': '美国',
    'joseph-barnby': '英国', 'barnby': '英国',
    'haldor-lillenas': '美国', 'lillenas': '美国',
    'hubert-platt-main': '美国',
    'william-augustine-ogden': '美国', 'ogden': '美国',
    'edwin-othello-excell': '美国',
    'william-fiske-sherwin': '美国', 'sherwin': '美国',
    'james-holmes-rosecrans': '美国', 'rosecrans': '美国',
    'james-henry-fillmore-sr': '美国', 'fillmore': '美国',
    'james-ramsey-murray': '美国', 'murray': '美国',
    'george-crawford-hugg': '美国', 'hugg': '美国',
    'charles-austin-miles': '美国', 'miles': '美国',
    'robert-harkness': '英国', 'harkness': '英国',
    'asa-hull': '美国', 'hull': '美国',
    'anthony-johnson-showalter': '美国',
    'john-harrison-tenney': '美国', 'tenney': '美国',
    'isaac-hickman-meredith': '美国', 'meredith': '美国',
    # lakh / mutopia / maestro / m21 补充
    'villa-lobos': '巴西', 'heitor-villa-lobos': '巴西',
    'antony-dvorak': '捷克',
    'tschaikovsky': '俄罗斯', 'tchaikovsky-p': '俄罗斯', 'pyotr-ilyich-tchaikovsky': '俄罗斯',
    'bing-crosby': '美国', 'the-beatles': '英国', 'john-lennon': '英国',
    'claude-bolling': '法国', 'nat-king-cole': '美国',
    'neil-diamond': '美国', 'carole-king': '美国', 'neil-sedaka': '美国',
    'elvis-presley': '美国', 'burt-bacharach': '美国', 'chris-rea': '英国',
    'stefanie-hertel': '德国', 'henry-litolff': '英国', 'john-blow': '英国',
    'anatoly-liadov': '俄罗斯',
    'd-aguado': '西班牙', 'johann-friedrich-franz-burgm-ller': '德国',
    'f-sor': '西班牙', 'titelouzej': '法国', 'jean-titelouze': '法国',
    'mendelssohn-bartholdyf': '德国',
    'johann-sebastian-bach-165-1750': '德国', 'johann-sebastian-bach-1685-1750': '德国',
    'gabriel-faur': '法国', 'a-scriabin': '俄罗斯', 'mateo-carcassi': '意大利',
    'niccol-paganini': '意大利', 'a-vivaldi': '意大利',
    'johann-pachelbel': '德国', 'pachelbel': '德国',
    'warlock': '英国', 'peter-warlock': '英国',
    'viardot': '法国', 'pauline-viardot': '法国',
    'boulanger': '法国', 'lili-boulanger': '法国', 'nadia-boulanger': '法国',
    'parratt': '英国', 'walter-parratt': '英国',
    'paradis': '奥地利', 'maria-theresia-paradis': '奥地利',
    'butterworth': '英国', 'george-butterworth': '英国',
    'grandval': '法国', 'clemence-de-grandval': '法国',
    'munktell': '瑞典', 'helena-munktell': '瑞典',
    'arne': '英国', 'thomas-arne': '英国',
    'somervell': '英国', 'arthur-somervell': '英国',
    'hardelot': '法国', 'guy-dhardelot': '法国',
    'coleridge-taylor': '英国', 'samuel-coleridge-taylor': '英国',
    'burleigh': '美国', 'harry-burleigh': '美国',
    'mackenzie': '英国', 'alexander-mackenzie': '英国',
    'mounseybartholomew': '英国', 'ann-mounsey-bartholomew': '英国',
    'netzel': '瑞典', 'laura-netzel': '瑞典',
    'mayer': '德国', 'emilie-mayer': '德国',
    'leo-janek': '捷克', 'janacek-l': '捷克', 'leos-janacek': '捷克',
    'george-enescu': '罗马尼亚', 'enescu': '罗马尼亚',
    'grainger': '澳大利亚', 'percy-grainger': '澳大利亚',
    'lusitano': '葡萄牙', 'vicente-lusitano': '葡萄牙',
    'cpebach': '德国',
    'friedrich-silcher': '德国', 'silcher': '德国',
    'adriano-banchieri': '意大利', 'banchieri': '意大利',
    'ernesto-cavallini': '意大利', 'cavallini': '意大利',
    'florimond-van-duyse': '比利时', 'van-duyse': '比利时',
    'heinrich-scheidemann-ca-1595-1663': '德国', 'scheidemann': '德国',
}

# 分源作曲家映射：同一 slug 在不同来源指向不同人（来源语境消歧）
SOURCE_COMPOSER_REGION = {
    'openscore': {          # OpenScore Lieder 语料：德法艺术歌曲语境
        'lang': '奥地利',       # Josephine Lang（数据内 name 全部为 Josephine Lang）
        'cornelius': '德国',    # Peter Cornelius
        'wolf': '奥地利',       # Hugo Wolf
    },
    'wikifonia': {
        'hungarian-song': '匈牙利',   # slug 语义即「匈牙利歌曲」
    },
}

# 预处理：去掉 None 值（显式不猜项）；key 统一 strip+lower（与查询侧一致）
COMPOSER_REGION = {k.strip().lower(): v for k, v in COMPOSER_REGION.items() if v}


def run(dry_run: bool):
    files = sorted(TRACKS.glob('*.jsonl'))
    stats = Counter()
    per_src = Counter()
    samples = []
    norm_changes = Counter()

    for f in files:
        lines = f.read_text(encoding='utf-8').splitlines()
        modified = False
        for i, line in enumerate(lines):
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            sid = r.get('source', '?')
            region = r.get('region')

            # ① 归一化：已是国籍形容词 → 中文国名（覆盖式，语义不变）
            if region in NORM and NORM[region] != region:
                r['region'] = NORM[region]
                stats['norm'] += 1
                norm_changes[f'{region}→{NORM[region]}'] += 1
                lines[i] = json.dumps(r, ensure_ascii=False, separators=(',', ':'))
                modified = True
                region = r['region']

            # ②③ 推导：region 为空才写
            if not region:
                new = SOURCE_REGION.get(sid)
                slug = (r.get('composer_slug') or '').strip().lower()
                if not new and slug:
                    new = COMPOSER_REGION.get(slug)
                if not new and slug:
                    # maestro 等「作曲家--编曲者」格式：按作曲家（-- 前半）判断
                    if '--' in slug:
                        new = COMPOSER_REGION.get(slug.split('--')[0])
                if not new and slug:
                    # 分源映射：同 slug 在不同来源指向不同人
                    new = SOURCE_COMPOSER_REGION.get(sid, {}).get(slug)
                if new:
                    r['region'] = new
                    stats['inferred'] += 1
                    per_src[sid] += 1
                    lines[i] = json.dumps(r, ensure_ascii=False, separators=(',', ':'))
                    modified = True
                    if len(samples) < 8:
                        samples.append((r['id'], (r.get('composer_name') or '')[:24], new))

        if modified and not dry_run:
            f.write_text('\n'.join(lines) + '\n', encoding='utf-8')

    print('=' * 72)
    print(f'region 推导 · {"DRY-RUN" if dry_run else "已写入"}')
    print('=' * 72)
    print(f'归一化（形容词→中文国名）: {stats["norm"]:,d}')
    for k, n in norm_changes.most_common(20):
        print(f'   {k:24s} {n:>7,d}')
    print()
    print(f'推导（来源级 + 作曲家映射）: {stats["inferred"]:,d}')
    for sid, n in per_src.most_common():
        print(f'   {sid:16s} {n:>7,d}')
    print()
    print('样例:')
    for sid, c, rg in samples:
        print(f'   {sid}  {c:26s} → {rg}')
    if dry_run:
        print('\n※ dry-run 确认后加 --apply 执行写回')
    return stats


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    args = ap.parse_args()
    run(dry_run=not args.apply)
    return 0


if __name__ == '__main__':
    sys.exit(main())
