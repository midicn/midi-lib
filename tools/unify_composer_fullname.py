#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A3 补 2 · 高频作曲家规范全名（覆盖数据驱动的姓氏派结果）

用法：python tools/unify_composer_fullname.py [--dry-run]
"""
from __future__ import annotations
import argparse, json, shutil
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACKS = ROOT / 'midi_db' / 'tracks'
BAK = ROOT / 'midi_db' / 'tracks_backup'

FULL = {
    'johann-sebastian-bach': 'Johann Sebastian Bach',
    'carl-philipp-emanuel-bach': 'Carl Philipp Emanuel Bach',
    'ludwig-van-beethoven': 'Ludwig van Beethoven',
    'wolfgang-amadeus-mozart': 'Wolfgang Amadeus Mozart',
    'franz-schubert': 'Franz Schubert', 'frederic-chopin': 'Frédéric Chopin',
    'franz-liszt': 'Franz Liszt', 'robert-schumann': 'Robert Schumann',
    'johannes-brahms': 'Johannes Brahms', 'pyotr-ilyich-tchaikovsky': 'Pyotr Ilyich Tchaikovsky',
    'claude-debussy': 'Claude Debussy', 'maurice-ravel': 'Maurice Ravel', 'erik-satie': 'Erik Satie',
    'domenico-scarlatti': 'Domenico Scarlatti', 'franz-joseph-haydn': 'Franz Joseph Haydn',
    'george-frideric-handel': 'George Frideric Handel', 'carl-czerny': 'Carl Czerny',
    'alexander-scriabin': 'Alexander Scriabin', 'sergei-rachmaninoff': 'Sergei Rachmaninoff',
    'felix-mendelssohn': 'Felix Mendelssohn', 'edvard-grieg': 'Edvard Grieg',
    'sergei-prokofiev': 'Sergei Prokofiev', 'bela-bartok': 'Béla Bartók',
    'muzio-clementi': 'Muzio Clementi', 'moritz-moszkowski': 'Moritz Moszkowski',
    'charles-valentin-alkan': 'Charles-Valentin Alkan', 'cecile-chaminade': 'Cécile Chaminade',
    'cornelius-gurlitt': 'Cornelius Gurlitt', 'mauro-giuliani': 'Mauro Giuliani',
    'arcangelo-corelli': 'Arcangelo Corelli', 'carl-maria-von-weber': 'Carl Maria von Weber',
    'giovanni-pierluigi-da-palestrina': 'Giovanni Pierluigi da Palestrina',
    'antonio-vivaldi': 'Antonio Vivaldi', 'henry-purcell': 'Henry Purcell',
    'georg-philipp-telemann': 'Georg Philipp Telemann', 'tomaso-albinoni': 'Tomaso Albinoni',
    'luigi-boccherini': 'Luigi Boccherini', 'niccolo-paganini': 'Niccolò Paganini',
    'gioachino-rossini': 'Gioachino Rossini', 'giuseppe-verdi': 'Giuseppe Verdi',
    'giacomo-puccini': 'Giacomo Puccini', 'vincenzo-bellini': 'Vincenzo Bellini',
    'gaetano-donizetti': 'Gaetano Donizetti', 'hector-berlioz': 'Hector Berlioz',
    'cesar-franck': 'César Franck', 'camille-saint-saens': 'Camille Saint-Saëns',
    'georges-bizet': 'Georges Bizet', 'charles-gounod': 'Charles Gounod',
    'jules-massenet': 'Jules Massenet', 'gabriel-faure': 'Gabriel Fauré',
    'modest-mussorgsky': 'Modest Mussorgsky', 'alexander-borodin': 'Alexander Borodin',
    'nikolai-rimsky-korsakov': 'Nikolai Rimsky-Korsakov', 'mikhail-glinka': 'Mikhail Glinka',
    'milij-balakirev': 'Mily Balakirev', 'alexander-glazunov': 'Alexander Glazunov',
    'dmitri-shostakovich': 'Dmitri Shostakovich', 'dmitry-kabalevsky': 'Dmitry Kabalevsky',
    'aram-khachaturian': 'Aram Khachaturian', 'gustav-mahler': 'Gustav Mahler',
    'anton-bruckner': 'Anton Bruckner', 'richard-wagner': 'Richard Wagner',
    'richard-strauss': 'Richard Strauss', 'jean-sibelius': 'Jean Sibelius',
    'carl-nielsen': 'Carl Nielsen', 'niels-gade': 'Niels Gade', 'johan-svendsen': 'Johan Svendsen',
    'franz-berwald': 'Franz Berwald', 'edward-elgar': 'Edward Elgar',
    'ralph-vaughan-williams': 'Ralph Vaughan Williams', 'gustav-holst': 'Gustav Holst',
    'frederick-delius': 'Frederick Delius', 'benjamin-britten': 'Benjamin Britten',
    'enrique-granados': 'Enrique Granados', 'isaac-albeniz': 'Isaac Albéniz',
    'manuel-de-falla': 'Manuel de Falla', 'joaquin-turina': 'Joaquín Turina',
    'joaquin-rodrigo': 'Joaquín Rodrigo', 'fernando-sor': 'Fernando Sor',
    'francisco-tarrega': 'Francisco Tárrega', 'heitor-villa-lobos': 'Heitor Villa-Lobos',
    'alberto-ginastera': 'Alberto Ginastera', 'astor-piazzolla': 'Astor Piazzolla',
    'louis-moreau-gottschalk': 'Louis Moreau Gottschalk', 'edward-macdowell': 'Edward MacDowell',
    'aaron-copland': 'Aaron Copland', 'samuel-barber': 'Samuel Barber',
    'george-gershwin': 'George Gershwin', 'charles-ives': 'Charles Ives', 'john-cage': 'John Cage',
    'philip-glass': 'Philip Glass', 'steve-reich': 'Steve Reich', 'john-adams': 'John Adams',
    'olivier-messiaen': 'Olivier Messiaen', 'pierre-boulez': 'Pierre Boulez',
    'karlheinz-stockhausen': 'Karlheinz Stockhausen', 'gyorgy-ligeti': 'György Ligeti',
    'krzysztof-penderecki': 'Krzysztof Penderecki', 'henryk-gorecki': 'Henryk Górecki',
    'arvo-part': 'Arvo Pärt', 'john-tavener': 'John Tavener', 'hans-werner-henze': 'Hans Werner Henze',
    'kurt-weill': 'Kurt Weill', 'paul-hindemith': 'Paul Hindemith', 'carl-orff': 'Carl Orff',
    'leos-janacek': 'Leoš Janáček', 'antonin-dvorak': 'Antonín Dvořák', 'bedrich-smetana': 'Bedřich Smetana',
    'lili-boulanger': 'Lili Boulanger', 'germaine-tailleferre': 'Germaine Tailleferre',
    'rebecca-clarke': 'Rebecca Clarke', 'amy-beach': 'Amy Beach', 'florence-price': 'Florence Price',
    'william-grant-still': 'William Grant Still', 'scott-joplin': 'Scott Joplin',
    'toru-takemitsu': 'Toru Takemitsu', 'joe-hisaishi': 'Joe Hisaishi',
    'ryuichi-sakamoto': 'Ryuichi Sakamoto', 'isang-yun': 'Isang Yun',
    'zhao-yuanren': 'Zhao Yuanren', 'huang-zi': 'Huang Zi', 'he-luting': 'He Luting',
    'nie-er': 'Nie Er', 'xian-xinghai': 'Xian Xinghai', 'ding-shande': 'Ding Shande',
    'wang-jianzhong': 'Wang Jianzhong', 'chu-wanghua': 'Chu Wanghua', 'wang-lisan': 'Wang Lisan',
    'li-yinghai': 'Li Yinghai', 'chen-peixun': 'Chen Peixun', 'tan-dun': 'Tan Dun',
    'chen-qigang': 'Chen Qigang', 'ye-xiaogang': 'Ye Xiaogang', 'guo-wenjing': 'Guo Wenjing',
    'zhou-long': 'Zhou Long', 'sheng-zong': 'Sheng Zongliang',
}


def main(dry: bool):
    total = 0
    for f in sorted(TRACKS.glob('*.jsonl')):
        lines = f.read_text(encoding='utf-8').splitlines()
        new = []
        changed = 0
        for line in lines:
            r = json.loads(line)
            want = FULL.get(r.get('composer_slug') or '')
            if want and r.get('composer_name') != want:
                r['composer_name'] = want
                changed += 1
                new.append(json.dumps(r, ensure_ascii=False, separators=(',', ':')))
            else:
                new.append(line)
        if changed and not dry:
            BAK.mkdir(exist_ok=True)
            shutil.copy2(f, BAK / f'pre-fullname-{f.stem}-20260923.jsonl')
            f.write_text('\n'.join(new) + '\n', encoding='utf-8')
        if changed:
            print(f'  {f.stem}: {changed:,}')
        total += changed
    print(f'全名统一 {total:,} 处（{len(FULL)} 位作曲家）')
    if dry:
        print('[dry-run] 未写回')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    main(ap.parse_args().dry_run)
