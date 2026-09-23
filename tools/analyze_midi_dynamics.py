#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""补漏 2 · MIDI 力度 + 音符密度 + 拍号推断（一次遍历）

- midi.velocity_avg / velocity_range（演奏力度统计 → 表现力指标）
- notes_per_sec（音符密度）
- timesig 推断（对无拍号者：onset 强度自相关 → 3/4 vs 4/4 vs 6/8；标 timesig_src=inferred）
用法：python tools/analyze_midi_dynamics.py [--apply] [--verify N]
"""
from __future__ import annotations
import argparse, json, random, shutil, time
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACKS = ROOT / 'midi_db' / 'tracks'
BAK = ROOT / 'midi_db' / 'tracks_backup'


def analyze(p: Path):
    data = p.read_bytes()
    if data[:4] != b'MThd':
        return None
    div = int.from_bytes(data[12:14], 'big') or 480
    vel_sum = vel_n = 0
    vel_min, vel_max = 128, -1
    onsets = []           # (tick, velocity)
    notes = 0
    i = 8 + int.from_bytes(data[4:8], 'big')
    while i < len(data) - 8:
        if data[i:i+4] != b'MTrk':
            break
        ln = int.from_bytes(data[i+4:i+8], 'big')
        j = i + 8
        end = j + ln
        running = None
        cur = 0
        while j < end:
            d = 0
            for _ in range(4):
                b0 = data[j]; j += 1
                d = (d << 7) | (b0 & 0x7F)
                if not (b0 & 0x80):
                    break
            cur += d
            if j >= end:
                break
            st = data[j]
            if st & 0x80:
                j += 1
                running = st
            else:
                st = running
            if st == 0xFF:
                mt = data[j]; j += 1
                l2 = 0
                while True:
                    b0 = data[j]; j += 1
                    l2 = (l2 << 7) | (b0 & 0x7F)
                    if not (b0 & 0x80):
                        break
                j += l2
            elif st in (0xF0, 0xF7):
                l2 = 0
                while True:
                    b0 = data[j]; j += 1
                    l2 = (l2 << 7) | (b0 & 0x7F)
                    if not (b0 & 0x80):
                        break
                j += l2
            else:
                hi = st & 0xF0
                if hi == 0x90 and data[j+1] > 0:
                    v = data[j+1]
                    vel_sum += v; vel_n += 1
                    if v < vel_min: vel_min = v
                    if v > vel_max: vel_max = v
                    onsets.append((cur, v))
                    notes += 1
                    j += 2
                elif hi in (0x80, 0x90, 0xA0, 0xB0, 0xE0):
                    j += 2
                elif hi in (0xC0, 0xD0):
                    j += 1
                else:
                    break
        i = end
    if not vel_n:
        return None
    return {'velocity_avg': round(vel_sum / vel_n, 1),
            'velocity_range': [vel_min, vel_max],
            'notes': notes, 'div': div, 'onsets': onsets}


def infer_timesig(onsets, div, notes):
    """onset 强度自相关 → 每小节拍数（2/3/4/6）；返回 (拍号, 置信)"""
    if len(onsets) < 60:
        return None, 0
    # 网格化到 1/4 拍
    step = max(div // 4, 1)
    last = onsets[-1][0]
    nb = min(int(last / step) + 1, 40000)
    grid = [0.0] * nb
    for t, v in onsets:
        b = t // step
        if b < nb:
            grid[b] += v
    # 归一化
    mx = max(grid) or 1
    g = [x / mx for x in grid]
    # 对候选周期（拍数 × 4 个 1/4 拍）做自相关
    best, bestv = None, 0
    for beats in (2, 3, 4, 6):
        lag = beats * 4
        if lag >= len(g):
            continue
        num = sum(g[i] * g[i + lag] for i in range(len(g) - lag))
        den = sum(x * x for x in g[:len(g) - lag]) ** 0.5 * sum(x * x for x in g[lag:]) ** 0.5
        c = num / den if den else 0
        if c > bestv:
            bestv = c
            best = beats
    if best is None or bestv < 0.30:
        return None, round(bestv, 3)
    return f'{best}/4', round(bestv, 3)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    ap.add_argument('--verify', type=int, default=0)
    a = ap.parse_args()

    if a.verify:
        pool = []
        for f in sorted(TRACKS.glob('*.jsonl')):
            if f.stem in ('thesession', 'norbeck', 'nottingham', 'abcmisc', 'essen', 'chinafolk', 'groove', 'musedata'):
                continue
            for line in f.open(encoding='utf-8'):
                r = json.loads(line)
                md = r.get('midi') or {}
                if md.get('timesig') and md.get('file'):
                    pool.append(r)
        random.seed(3)
        sample = random.sample(pool, min(a.verify, len(pool)))
        print(f'验证样本 {len(sample):,}（池 {len(pool):,}）')
        ok = tot = 0
        for r in sample:
            st = analyze(ROOT / r['midi']['file'])
            if not st:
                continue
            ts, conf = infer_timesig(st['onsets'], st['div'], st['notes'])
            if not ts:
                continue
            tot += 1
            have = (r['midi']['timesig'] or '').strip()
            if ts == have:
                ok += 1
        print(f'拍号一致率（有推断样本）: {ok}/{tot} = {ok/max(tot,1)*100:.1f}%')
        return

    stats = Counter()
    for f in sorted(TRACKS.glob('*.jsonl')):
        lines = f.read_text(encoding='utf-8').splitlines()
        new = []
        changed = 0
        t0 = time.time()
        for line in lines:
            r = json.loads(line)
            mf = (r.get('midi') or {}).get('file')
            if not mf:
                sp = (r.get('src_path') or '').replace('\\', '/')
                mf = sp if sp and (ROOT / sp).exists() else None
            if not mf:
                new.append(line); continue
            md = r.setdefault('midi', {})
            if md.get('velocity_avg'):
                new.append(line); continue
            st = analyze(ROOT / mf)
            if not st:
                new.append(line); continue
            md['velocity_avg'] = st['velocity_avg']
            md['velocity_range'] = st['velocity_range']
            dur = md.get('duration_sec') or 0
            if dur > 0:
                md['notes_per_sec'] = round(st['notes'] / dur, 2)
            stats['velocity'] += 1
            # 拍号推断已弃用：留一验证一致率仅 26.8%（不可靠，不进库——宁缺勿错）
            changed += 1
            new.append(json.dumps(r, ensure_ascii=False, separators=(',', ':')))
        if changed and a.apply:
            BAK.mkdir(exist_ok=True)
            shutil.copy2(f, BAK / f'pre-dynamics-{f.stem}-20260923.jsonl')
            f.write_text('\n'.join(new) + '\n', encoding='utf-8')
            print(f'  {f.stem}: +{changed:,} · {time.time()-t0:.0f}s', flush=True)
    print('统计:', dict(stats))


if __name__ == '__main__':
    main()
