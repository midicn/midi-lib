#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""D 终审修复：坏文件标记 + no=0 脏值清理

- duration<=0 / note_count<=0 的**非排除源**记录 → verify_flag='broken'（发布时由 build 自动跳过）
- no=0 脏值 → 清空
用法：python tools/fix_audit_leftovers.py [--dry-run]
"""
from __future__ import annotations
import argparse, json, shutil
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACKS = ROOT / 'midi_db' / 'tracks'
BAK = ROOT / 'midi_db' / 'tracks_backup'


def main(dry: bool):
    stats = Counter()
    for f in sorted(TRACKS.glob('*.jsonl')):
        if f.stem == 'musedata':          # 排除源，不处理
            continue
        lines = f.read_text(encoding='utf-8').splitlines()
        new = []
        changed = 0
        for line in lines:
            r = json.loads(line)
            md = r.get('midi') or {}
            upd = False
            if (md.get('duration_sec') or 0) <= 0 or (md.get('note_count') or 0) <= 0:
                r['verify_flag'] = 'broken'
                stats[f'broken:{f.stem}'] += 1
                upd = True
            if str(r.get('no')) == '0':
                r['no'] = None
                stats['no=0 清理'] += 1
                upd = True
            if upd:
                changed += 1
                new.append(json.dumps(r, ensure_ascii=False, separators=(',', ':')))
            else:
                new.append(line)
        if changed and not dry:
            BAK.mkdir(exist_ok=True)
            shutil.copy2(f, BAK / f'pre-auditfix-{f.stem}-20260923.jsonl')
            f.write_text('\n'.join(new) + '\n', encoding='utf-8')
    print('修复:', dict(stats))
    if dry:
        print('[dry-run] 未写回')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    main(ap.parse_args().dry_run)
