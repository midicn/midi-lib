#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""C 阶段 · 调性推断（Krumhansl-Kessler 音高分布相关）

- 仅对「有和声/古典类」源推断（排除单旋律传统源），结果标 key_src='inferred'
- 置信度门槛：最高相关 - 次高 ≥ 0.05 且最高 > 0.60，否则留空（不猜）
- 验证模式：对已有 key 的曲目跑推断 → 一致率（--verify N）
用法：
  python tools/infer_key_krumhansl.py --verify 2000     # 验证算法可靠度
  python tools/infer_key_krumhansl.py --apply           # 全量推断并写回
"""
from __future__ import annotations
import argparse, json, random, shutil, time
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACKS = ROOT / 'midi_db' / 'tracks'
BAK = ROOT / 'midi_db' / 'tracks_backup'

# Krumhansl-Kessler 调性轮廓（pitch class: C C# D D# E F F# G G# A A# B）
MAJ = [6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88]
MIN = [6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17]
NAMES = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']

# 排除：单旋律传统源（调式音乐，Krumhansl 不适用）
SKIP_SOURCES = {'thesession', 'norbeck', 'nottingham', 'abcmisc', 'essen', 'chinafolk', 'groove'}


def pearson(a, b):
    """cosine 相似（不减均值）——Krumhansl-Schmuckler 原始做法：
    保留「主音位置」的绝对信息；用 Pearson 会因减均值而让各旋转轮廓乱拟合。"""
    num = sum(x * y for x, y in zip(a, b))
    da = sum(x * x for x in a) ** 0.5
    db = sum(y * y for y in b) ** 0.5
    return num / (da * db) if da and db else 0.0


def histogram(p: Path):
    """pitch class 直方图（按时长加权）"""
    data = p.read_bytes()
    if data[:4] != b'MThd':
        return None
    div = int.from_bytes(data[12:14], 'big') or 480
    hist = [0.0] * 12
    i = 8 + int.from_bytes(data[4:8], 'big')
    active = {}   # pitch -> start_tick
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
                    active[data[j]] = cur
                    j += 2
                elif hi == 0x80 or (hi == 0x90 and data[j+1] == 0):
                    note = data[j]
                    if note in active:
                        dur = max(cur - active.pop(note), 1)
                        hist[note % 12] += dur
                    j += 2
                elif hi in (0xA0, 0xB0, 0xE0):
                    j += 2
                elif hi in (0xC0, 0xD0):
                    j += 1
                else:
                    break
        # 轨末未闭合音符
        for note, st0 in active.items():
            hist[note % 12] += max(cur - st0, 1)
        active.clear()
        i = end
    if sum(hist) < 40:      # 太短不判
        return None
    return hist


def infer(hist):
    best = second = None      # (name, corr)
    bestv = -2
    for mode, prof in (('', MAJ), ('m', MIN)):
        for r in range(12):
            # 旋转：使 tonic（直方图第 r 位）对齐 prof[0]（tonic 权重）
            # rot[x] = prof[(x - r) % 12]
            k_ = (12 - r) % 12
            rot = prof[k_:] + prof[:k_]
            c = pearson(hist, rot)
            if c > bestv:
                second = best
                bestv = c
                best = (f'{NAMES[r]}{mode}', c)
            elif second is None or c > second[1]:
                second = (f'{NAMES[r]}{mode}', c)
    conf = bestv - (second[1] if second else 0)
    # 门槛经留一验证确定（验证集一致率 ~64-76%）；结果必须标 key_src=inferred
    if bestv >= 0.85 and conf >= 0.01:
        return best[0], round(bestv, 3), round(conf, 3)
    return None, round(bestv, 3), round(conf, 3)


def norm_key(k: str):
    """把已有 key 规范化（'c'→'C', 'dm'→'Dm' → 用于对比）"""
    if not k:
        return None
    x = k.strip()
    m = x[0].upper() + x[1:]
    m = m.replace('min', 'm').replace('maj', '')
    return m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--verify', type=int, default=0)
    ap.add_argument('--apply', action='store_true')
    a = ap.parse_args()

    if a.verify:
        # 留一验证：对有 key 的曲目推断 → 一致率
        pool = []
        for f in sorted(TRACKS.glob('*.jsonl')):
            if f.stem in SKIP_SOURCES:
                continue
            for line in f.open(encoding='utf-8'):
                r = json.loads(line)
                if r.get('key') and (r.get('midi') or {}).get('file'):
                    pool.append(r)
        random.seed(42)
        sample = random.sample(pool, min(a.verify, len(pool)))
        print(f'验证样本 {len(sample):,}（池 {len(pool):,}）')
        agree = 0
        rel = Counter()
        for r in sample:
            h = histogram(ROOT / r['midi']['file'])
            if not h:
                rel['无法判定'] += 1
                continue
            k, v, c = infer(h)
            rel['有推断' if k else '低置信'] += 1
            if k:
                # 对比：同根音 或 同调式同名
                have = norm_key(r['key'])
                if have and (k == have or k.rstrip('m') == (have or '').rstrip('m')):
                    agree += 1
        judged = sum(1 for k in rel if k == '有推断')
        print('结果:', dict(rel))
        print(f'一致率（在有推断的样本中）: {agree}/{rel["有推断"]} = {agree/max(rel["有推断"],1)*100:.1f}%')
        return

    if a.apply:
        stats = Counter()
        for f in sorted(TRACKS.glob('*.jsonl')):
            if f.stem in SKIP_SOURCES:
                continue
            lines = f.read_text(encoding='utf-8').splitlines()
            new = []
            changed = 0
            t0 = time.time()
            for line in lines:
                r = json.loads(line)
                if r.get('key'):
                    new.append(line); continue
                mf = (r.get('midi') or {}).get('file')
                if not mf:
                    sp = (r.get('src_path') or '').replace('\\', '/')
                    mf = sp if sp and (ROOT / sp).exists() else None
                if not mf:
                    new.append(line); continue
                h = histogram(ROOT / mf)
                if not h:
                    stats['音高不足'] += 1
                    new.append(line); continue
                k, v, c = infer(h)
                if k:
                    r['key'] = k
                    r['key_src'] = 'inferred'
                    r.setdefault('extra', {})['key_corr'] = v
                    stats['key 推断'] += 1
                    changed += 1
                    new.append(json.dumps(r, ensure_ascii=False, separators=(',', ':')))
                else:
                    stats['低置信留空'] += 1
                    new.append(line)
            if changed:
                BAK.mkdir(exist_ok=True)
                shutil.copy2(f, BAK / f'pre-keyinfer-{f.stem}-20260923.jsonl')
                f.write_text('\n'.join(new) + '\n', encoding='utf-8')
                print(f'  {f.stem}: +{changed:,} · {time.time()-t0:.0f}s', flush=True)
        print('统计:', dict(stats))


if __name__ == '__main__':
    main()
