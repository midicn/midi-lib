#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""曲式推断：从标题关键词提取 form 字段（纯本地 · 无网络 · dry-run 先行）

规则：只匹配标题中的**明确曲式关键词**（英/意/德/法），不确定的不猜。
优先级：长词优先（避免 "Sonatina" 被 "Sonata" 误匹配）。
不覆盖已有 form 值的行。
"""
from __future__ import annotations
import argparse, json, re, sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACKS = ROOT / 'midi_db' / 'tracks'

# 曲式模式表：slug → (正则, 中文名)。按长度降序排列（长词优先）。
# 只匹配明确乐式词，不匹配模糊关键词（如 "piece"、"work"）。
FORM_PATTERNS = [
    ('sonatina',      r'\bsonatina\b',                                    '小奏鸣曲'),
    ('sonata',        r'\bsonata\b|\bsonate\b',                            '奏鸣曲'),
    ('symphony',      r'\bsymphon(?:y|ie|ique)\b|\bsinfonia\b',            '交响曲'),
    ('concerto',      r'\bconcerto\b|\bkonzert\b',                         '协奏曲'),
    ('nocturne',      r'\bnocturne\b|\bnotturno\b',                        '夜曲'),
    ('prelude',       r'\bprelude\b|\bprélude\b|\bvorspiel\b',             '前奏曲'),
    ('fugue',         r'\bfugue\b|\bfuga\b|\bfugato\b',                    '赋格'),
    ('variations',    r'\bvariation|\bvar\.\s|\bvariazioni\b',             '变奏曲'),
    ('suite',         r'\bsuite\b|\bpartita\b|\bordo\b',                   '组曲'),
    ('waltz',         r'\bwaltz\b|\bwalse\b|\bvalzer\b|\bvalse\b',         '圆舞曲'),
    ('mazurka',       r'\bmazurka\b',                                      '玛祖卡'),
    ('polonaise',     r'\bpolonaise\b|\bpolonesa\b',                       '波兰舞曲'),
    ('etude',         r'\bé?tude\b|\bstudium\b|\bstudi\b',                 '练习曲'),
    ('impromptu',     r'\bimpromptu\b',                                    '即兴曲'),
    ('scherzo',       r'\bscherzo\b',                                      '谐谑曲'),
    ('rondo',         r'\brondo\b|\brondò\b',                              '回旋曲'),
    ('fantasy',       r'\bfantasy\b|\bfantaisie\b|\bfantasie\b|\bfantasia\b', '幻想曲'),
    ('overture',      r'\boverture\b|\bouverture\b',                       '序曲'),
    ('march',         r'\bmarch\b|\bmarsch\b|\bmarche\b',                  '进行曲'),
    ('minuet',        r'\bminuet\b|\bmenuet(t)?\b|\bminuetto\b',           '小步舞曲'),
    ('serenade',      r'\bserenade\b|\bserenata\b|\bstandchen\b',          '小夜曲'),
    ('bagatelle',     r'\bbagatelle\b',                                    '小品'),
    ('intermezzo',    r'\bintermezzo\b|\bintermezz(o|o)',                  '间奏曲'),
    ('barcarolle',    r'\bbarcarole\b|\bbarcarolle\b',                     '船歌'),
    ('berceuse',      r'\bberceuse\b',                                     '摇篮曲'),
    ('toccata',       r'\btoccata\b',                                      '托卡塔'),
    ('romance',       r'\bromance\b|\bromanze\b',                          '浪漫曲'),
    ('canon',         r'\bcanon\b',                                        '卡农'),
    ('invention',     r'\binvention(?:en)?\b',                             '创意曲'),
    ('aria',          r'\baria\b|\barie\b',                                '咏叹调'),
    ('ballade',       r'\bballade\b|\bballada\b',                          '叙事曲'),
    ('caprice',       r'\bcaprice\b|\bcapriccio\b',                        '随想曲'),
    ('elegy',         r'\belegy\b|\belegie\b',                             '悲歌'),
    ('humoresque',    r'\bhumoresque\b',                                   '幽默曲'),
    ('arabesque',     r'\barabesque\b',                                    '阿拉伯风'),
    ('quartet',       r'\bquartet(?:t)?\b',                                '四重奏'),
    ('quintet',       r'\bquintet(?:t)?\b',                                '五重奏'),
    ('trio',          r'\btrio\b',                                         '三重奏'),
    ('duet',          r'\bduet\b|\bduo\b',                                 '二重奏'),
    ('chorale',       r'\bchorale\b|\bchoral\b',                           '众赞歌'),
    ('madrigal',      r'\bmadrigal\b',                                     '牧歌'),
    ('mass',          r'\bmass\b|\bmesse\b|\bmisa\b',                      '弥撒'),
    ('requiem',       r'\brequiem\b',                                      '安魂曲'),
    ('cantata',       r'\bcantata\b',                                      '康塔塔'),
    ('divertimento',  r'\bdivertimento\b',                                 '嬉游曲'),
    ('gavotte',       r'\bgavotte\b|\bgavota\b',                           '加沃特'),
    ('gigue',         r'\bgigue\b|\bgiga\b',                               '吉格'),
    ('allemande',     r'\ballemande\b',                                    '阿勒曼德'),
    ('courante',      r'\bcourante\b|\bcorrente\b',                        '库朗特'),
    ('sarabande',     r'\bsarabande\b',                                    '萨拉班德'),
    ('bourree',       r'\bbourree\b|\bborrée\b',                           '布列'),
    ('tarantella',    r'\btarantella\b',                                   '塔兰泰拉'),
    ('bolero',        r'\bbolero\b',                                       '波莱罗'),
    ('tango',         r'\btango\b',                                        '探戈'),
    ('habanera',      r'\bhabanera\b',                                     '哈巴涅拉'),
    ('passacaglia',   r'\bpassacaglia\b',                                  '帕萨卡利亚'),
    ('chaconne',      r'\bchaconne\b|\bciaccona\b',                        '恰空'),
    ('lied',          r'\blied(?:er)?\b',                                  '艺术歌曲'),
    ('march_military', r'\bmilitary\s+march\b',                            '军进行曲'),
]

# 预编译
_COMPILED = [(slug, re.compile(pat, re.I), zh) for slug, pat, zh in FORM_PATTERNS]


def infer_form(title: str) -> str | None:
    """从标题推断曲式 slug；无匹配返回 None"""
    if not title:
        return None
    tl = title.lower()
    for slug, pat, zh in _COMPILED:
        if pat.search(tl):
            return slug
    return None


def run(dry_run: bool, backup: bool):
    files = sorted(TRACKS.glob('*.jsonl'))
    all_changes = []          # (file, line_idx, track_id, old_form, new_form)
    per_src = Counter()

    for f in files:
        lines = f.read_text(encoding='utf-8').splitlines()
        modified = False
        for i, line in enumerate(lines):
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            if r.get('form'):        # 已有值不覆盖
                continue
            title = r.get('title') or r.get('t') or ''
            form = infer_form(title)
            if form:
                all_changes.append((f.name, i, r['id'], r.get('form'), form))
                per_src[r.get('source', '?')] += 1
                modified = True
        # 回写
        if modified and not dry_run:
            # 收集本文件所有改动
            changes_for_file = {c[1]: c[4] for c in all_changes if c[0] == f.name}
            for i, new_form in changes_for_file.items():
                r = json.loads(lines[i])
                r['form'] = new_form
                lines[i] = json.dumps(r, ensure_ascii=False, separators=(',', ':'))
            f.write_text('\n'.join(lines) + '\n', encoding='utf-8')

    # 汇总
    print(f'{"=" * 72}')
    print(f'曲式推断 · {"DRY-RUN" if dry_run else "已写入"}')
    print(f'{"=" * 72}')
    print(f'可推断: {len(all_changes):,d} 首')
    print()
    print('按曲式:')
    form_dist = Counter(c[4] for c in all_changes)
    for slug, n in form_dist.most_common(30):
        zh = next(z for s, p, z in FORM_PATTERNS if s == slug)
        print(f'   {slug:20s} {zh:8s} {n:>6,d}')
    print()
    print('按来源:')
    for sid, n in per_src.most_common():
        print(f'   {sid:20s} {n:>6,d}')
    print()

    cur_form = sum(1 for f2 in files for line in f2.read_text(encoding='utf-8').splitlines()
                   if json.loads(line).get('form'))
    new_total = cur_form + (len(all_changes) if dry_run else 0)
    print(f'form 覆盖: {cur_form:,d} → {new_total:,d} ({new_total / 124179 * 100:.1f}%)')

    if dry_run:
        print('\n※ dry-run 确认后加 --apply 执行写回')
    else:
        print('\n※ 已写回 jsonl（build_release 后生效到站点）')
    return len(all_changes)


def main():
    ap = argparse.ArgumentParser(description='曲式推断（从标题提取 form）')
    ap.add_argument('--apply', action='store_true', help='执行写回（默认 dry-run）')
    args = ap.parse_args()
    run(dry_run=not args.apply, backup=True)
    return 0


if __name__ == '__main__':
    sys.exit(main())
