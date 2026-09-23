#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A1 · MIDI 深度解析（全量）：tempo / timesig / instrument_gm / pitch_range / 内嵌歌词

- 数据源：各 jsonl 的 midi.file（规范化文件，data/midi/<source>/...）
- 解析器：手写（已验证与 mido 一致），速度 ~5ms/文件
- 写入：midi.tempo · midi.timesig · instrument_gm（主乐器 GM 英文名）· instruments_gm · pitch_range · midi.lyrics_inline
用法：
  python tools/analyze_midi_deep.py --sample 100     # 抽样验证（不写回）
  python tools/analyze_midi_deep.py --apply          # 全量写回
  python tools/analyze_midi_deep.py --apply --only atepp
"""
from __future__ import annotations
import argparse, json, re, shutil, time
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACKS = ROOT / 'midi_db' / 'tracks'
BAK = ROOT / 'midi_db' / 'tracks_backup'

GM = ['Acoustic Grand Piano', 'Bright Acoustic Piano', 'Electric Grand Piano', 'Honky-tonk Piano',
      'Electric Piano 1', 'Electric Piano 2', 'Harpsichord', 'Clavi', 'Celesta', 'Glockenspiel',
      'Music Box', 'Vibraphone', 'Marimba', 'Xylophone', 'Tubular Bells', 'Dulcimer',
      'Drawbar Organ', 'Percussive Organ', 'Rock Organ', 'Church Organ', 'Reed Organ', 'Accordion',
      'Harmonica', 'Tango Accordion', 'Acoustic Guitar (nylon)', 'Acoustic Guitar (steel)',
      'Electric Guitar (jazz)', 'Electric Guitar (clean)', 'Electric Guitar (muted)', 'Overdriven Guitar',
      'Distortion Guitar', 'Guitar Harmonics', 'Acoustic Bass', 'Electric Bass (finger)',
      'Electric Bass (pick)', 'Fretless Bass', 'Slap Bass 1', 'Slap Bass 2', 'Synth Bass 1', 'Synth Bass 2',
      'Violin', 'Viola', 'Cello', 'Contrabass', 'Tremolo Strings', 'Pizzicato Strings', 'Orchestral Harp',
      'Timpani', 'String Ensemble 1', 'String Ensemble 2', 'Synth Strings 1', 'Synth Strings 2',
      'Choir Aahs', 'Voice Oohs', 'Synth Voice', 'Orchestra Hit', 'Trumpet', 'Trombone', 'Tuba',
      'Muted Trumpet', 'French Horn', 'Brass Section', 'Synth Brass 1', 'Synth Brass 2',
      'Soprano Sax', 'Alto Sax', 'Tenor Sax', 'Baritone Sax', 'Oboe', 'English Horn', 'Bassoon',
      'Clarinet', 'Piccolo', 'Flute', 'Recorder', 'Pan Flute', 'Blown Bottle', 'Shakuhachi', 'Whistle',
      'Ocarina', 'Lead 1 (square)', 'Lead 2 (sawtooth)', 'Lead 3 (calliope)', 'Lead 4 (chiff)',
      'Lead 5 (charang)', 'Lead 6 (voice)', 'Lead 7 (fifths)', 'Lead 8 (bass + lead)', 'Pad 1 (new age)',
      'Pad 2 (warm)', 'Pad 3 (polysynth)', 'Pad 4 (choir)', 'Pad 5 (bowed)', 'Pad 6 (metallic)',
      'Pad 7 (halo)', 'Pad 8 (sweep)', 'FX 1 (rain)', 'FX 2 (soundtrack)', 'FX 3 (crystal)',
      'FX 4 (atmosphere)', 'FX 5 (brightness)', 'FX 6 (goblins)', 'FX 7 (echoes)', 'FX 8 (sci-fi)',
      'Sitar', 'Banjo', 'Shamisen', 'Koto', 'Kalimba', 'Bagpipe', 'Fiddle', 'Shanai', 'Tinkle Bell',
      'Agogo', 'Steel Drums', 'Woodblock', 'Taiko Drum', 'Melodic Tom', 'Synth Drum', 'Reverse Cymbal',
      'Guitar Fret Noise', 'Breath Noise', 'Seashore', 'Bird Tweet', 'Telephone Ring', 'Helicopter',
      'Applause', 'Gunshot']


def analyze(p: Path):
    data = p.read_bytes()
    if data[:4] != b'MThd':
        return None
    div = int.from_bytes(data[12:14], 'big') or 480
    i = 8 + int.from_bytes(data[4:8], 'big')
    tempo = timesig = None
    pitch_min = 128
    pitch_max = -1
    pitch_sum = pcount = 0
    lyrics = []
    # 每 track：note 数 + program
    trk_stats = []
    while i < len(data) - 8:
        if data[i:i+4] != b'MTrk':
            break
        ln = int.from_bytes(data[i+4:i+8], 'big')
        j = i + 8
        end = j + ln
        running = None
        t_notes = 0
        t_prog = None
        while j < end:
            d = 0
            for _ in range(4):
                b0 = data[j]; j += 1
                d = (d << 7) | (b0 & 0x7F)
                if not (b0 & 0x80):
                    break
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
                if mt == 0x51 and l2 >= 3 and tempo is None:
                    us = int.from_bytes(data[j:j+3], 'big')
                    if us:
                        tempo = round(60_000_000 / us)
                elif mt == 0x58 and l2 >= 2 and timesig is None:
                    timesig = f'{data[j]}/{2 ** data[j+1]}'
                elif mt == 0x05 and l2:
                    try:
                        tx = data[j:j+l2].decode('utf-8', 'replace').strip()
                        if tx and len(tx) < 200:
                            lyrics.append(tx)
                    except Exception:
                        pass
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
                if hi == 0x90:
                    v = data[j+1]
                    if v > 0:
                        note = data[j]
                        t_notes += 1
                        pcount += 1
                        pitch_sum += note
                        if note < pitch_min:
                            pitch_min = note
                        if note > pitch_max:
                            pitch_max = note
                    j += 2
                elif hi in (0x80, 0xA0, 0xB0, 0xE0):
                    j += 2
                elif hi == 0xC0:
                    if t_prog is None:
                        t_prog = data[j]
                    j += 1
                elif hi == 0xD0:
                    j += 1
                else:
                    break
        trk_stats.append((t_notes, t_prog))
        i = end

    if pcount == 0:
        return None
    # 主乐器：note 最多的 track；无 program_change 时返回 None（由上层按源语义决定）
    trk_stats.sort(key=lambda x: -x[0])
    main_prog = None
    for n, pr in trk_stats:
        if n > 0:
            main_prog = pr          # 该轨的 program（可能 None）
            break
    progs = sorted({pr for n, pr in trk_stats if n > 0 and pr is not None})
    return {
        'tempo': tempo, 'timesig': timesig,
        'program': main_prog,       # None = 无 program_change 事件
        'instruments_gm': [GM[p] for p in progs if 0 <= p < 128][:8],
        'pitch_range': [pitch_min, pitch_max],
        'pitch_avg': round(pitch_sum / pcount, 1),
        'lyrics_inline': (' | '.join(lyrics))[:500] if lyrics else None,
        'tracks': len(trk_stats),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    ap.add_argument('--sample', type=int, default=0)
    ap.add_argument('--only', default='')
    ap.add_argument('--limit', type=int, default=0, help='每源最多处理 N 首（调试）')
    a = ap.parse_args()

    files = sorted(TRACKS.glob('*.jsonl'))
    if a.only:
        files = [f for f in files if f.stem == a.only]

    grand = Counter()
    t0 = time.time()
    done = 0
    for f in files:
        lines = f.read_text(encoding='utf-8').splitlines()
        new_lines = []
        for line in lines:
            r = json.loads(line)
            mf = (r.get('midi') or {}).get('file')
            # 回退：新源（未规范化到 data/midi）用 src_path
            if not mf:
                sp = (r.get('src_path') or '').replace('\\', '/')
                if sp and (ROOT / sp).exists():
                    mf = sp
            if not mf:
                new_lines.append(line)
                continue
            p = ROOT / mf
            if not p.exists():
                grand['文件缺失'] += 1
                new_lines.append(line)
                continue
            if a.sample and done >= a.sample:
                new_lines.append(line)
                continue
            st = analyze(p)
            if not st:
                grand['解析失败'] += 1
                new_lines.append(line)
                continue
            done += 1
            md = r.setdefault('midi', {})
            if st['tempo']:
                md['tempo'] = st['tempo']; grand['tempo'] += 1
            if st['timesig']:
                md['timesig'] = st['timesig']; grand['timesig'] += 1
            if st['program'] is not None:
                gm = GM[st['program']] if 0 <= st['program'] < 128 else None
                if gm:
                    r['instrument_gm'] = gm
                    grand['instrument_gm(program)'] += 1
            elif (r.get('instrument') or '') == 'piano':
                # 无 program_change 且原字段为钢琴 → GM 默认（Acoustic Grand Piano）
                r['instrument_gm'] = GM[0]
                grand['instrument_gm(默认钢琴)'] += 1
            if st['instruments_gm']:
                r['instruments_gm'] = st['instruments_gm']
            if st['pitch_range'][1] >= 0:
                r['pitch_range'] = st['pitch_range']; grand['pitch_range'] += 1
            if st['lyrics_inline']:
                md['lyrics_inline'] = st['lyrics_inline']; grand['lyrics_inline'] += 1
            new_lines.append(json.dumps(r, ensure_ascii=False, separators=(',', ':')))
            if done % 5000 == 0:
                print(f'  {done:,} · {time.time()-t0:.0f}s · {done/max(time.time()-t0,1):.0f}/s', flush=True)
        if a.apply and not a.sample:
            BAK.mkdir(exist_ok=True)
            shutil.copy2(f, BAK / f'pre-deepmidi-{f.stem}-20260923.jsonl')
            f.write_text('\n'.join(new_lines) + '\n', encoding='utf-8')
            print(f'  [saved] {f.name}', flush=True)
    print(f'处理 {done:,} 首 · {time.time()-t0:.0f}s')
    print('统计:', dict(grand))


if __name__ == '__main__':
    main()
