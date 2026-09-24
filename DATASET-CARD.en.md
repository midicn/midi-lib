---
license: mixed (per-track `license` field; see LICENSE-AUDIT.md · meta package CC0-1.0)
language: [zh, en, mul]
tags: [music, midi, symbolic-music, classical, folk, world-music, hymns, public-domain, creative-commons]
pretty_name: MIDI Lib CN (midicn-lib)
size_categories: [100K<n<1M]
task_categories: [text-to-music, audio-classification, other]
configs:
  - name: main
    description: commercially usable tracks (C1)
  - name: piano-special
    description: non-commercial piano performances (C2)
  - name: study
    description: study / research only (C3)
  - name: meta
    description: unified catalogue and indexes (CC0-1.0)
---

# DATASET CARD · midicn-lib

> **133,667** tracks · **21** public sources · **14** categories · per-track source and licence tier ·
> full provenance
>
> This card describes the **contents, sources, fields, quality and practical usage restrictions** of the dataset.
> Each source's acquisition address, method and checksums are in [`PROVENANCE.md`](PROVENANCE.md)
> (with a re-runnable verification script).
>
> Portal: <https://lib.midicn.com> · Code repository: <https://github.com/midicn/lib>

## 1. Overview

midicn-lib is a systematic re-curation of **21 public MIDI / notation datasets** into one open
collection with a **unified catalogue, unified fields and per-track licence tagging**:

- **Unified catalogue** — every track is renamed `{source}-{index}.mid` and packaged by **usage tier** (see §2)
- **Unified fields** — 20 fields with consistent cross-source semantics (§4), plus composer / period /
  region / source indexes
- **Per-track licence** — each track carries `z` (tier: `main` / `piano-special` / `study`) and
  `l` (licence identifier)
- **Provenance** — upstream path and work-level identifiers are kept per track; source-side evidence and
  checksums are recorded in `PROVENANCE.md`
- **Takedown-ready** — rights-holder notices are handled per `LICENSE.md` §7 (acted upon promptly)

## 2. Splits and scale

Splits are by **usage tier**, not by genre — download only the tier you need:

| Split | Meaning | Tier | Tracks | Package |
|---|---|---|---:|---|
| `main` | licences permit commercial use | **C1** | 79,216 | `midicn-lib-<VER>-main.zip` |
| `piano-special` | non-commercial only | **C2** | 34,869 | `midicn-lib-<VER>-piano-special.zip` |
| `study` | study / research only | **C3** | 19,582 | `midicn-lib-<VER>-study.zip` |
| `meta` | catalogue / indexes / field docs / documents | **CC0-1.0** | — | `midicn-lib-<VER>-meta.zip` |
| **Total** | | | **133,667** | plus **400+ dimension packs** (zip.midicn.com) |

Licence distribution (by track):

| Licence tag | Tracks | Main sources |
|---|---:|---|
| `CC-BY-NC-SA-4.0` | 34,869 | aria 32,522 · maestro 1,276 · emopia 1,071 |
| `CC-BY-SA-4.0` | 23,289 | thesession 23,250 · oga 39 |
| `CC-BY-4.0` | 21,200 | giantmidi 10,110 · lakh 9,630 · groove 1,149 · musicnet 297 · oga 14 |
| `OPEN` (site open declaration) | 16,332 | essen 10,373 · norbeck 3,439 · abcmisc 1,487 · nottingham 1,033 |
| `PD` (public domain) | 14,419 | cyberhymnal 10,945 · m21 3,029 · wikifonia 445 |
| `TRADITIONAL-STUDY` | 10,473 | chinafolk 10,473 (C3) |
| `MUTOPIA-MIXED` (per piece) | 1,860 | mutopia 1,860 |
| `CC0-1.0` | 1,704 | openscore 1,438 · oga 266 |
| other per-piece (CC BY 3.0 / CC BY-SA 3.0 / GPL) | 21 | oga 21 |

## 3. Sources (19)

Addresses are the **places we actually obtained the data from**; method and checksums are in
[`PROVENANCE.md`](PROVENANCE.md).

| id | Source | Tracks | Tier | Acquisition address |
|---|---|---:|---|---|
| `aria` | Aria-MIDI (Unique subset) | 32,522 | C2 | github.com/loubbrad/aria-midi |
| `thesession` | The Session | 23,250 | C1 | github.com/adactio/TheSession-data |
| `cyberhymnal` | The Cyber Hymnal | 10,945 | C1 | hymntime.com/tch |
| `chinafolk` | Anthology of Chinese Folk Songs (OMR) | 10,473 | C3 | github.com/m-july/Anthology-of-Chinese-Folk-Songs |
| `essen` | ESAC European folk-song archive | 10,373 | C1 | esac-data.org |
| `giantmidi` | GiantMIDI-Piano | 10,110 | C1 | github.com/bytedance/GiantMIDI-Piano |
| `lakh` | Lakh MIDI Dataset (filtered) | 9,630 | C3 | colinraffel.com/projects/lmd/ |
| `norbeck` | Norbeck ABC collections | 3,439 | C1 | norbeck.nu/abc/ |
| `m21` | music21 CoreCorpus | 3,029 | C1 | github.com/cuthbertLab/music21 |
| `mutopia` | Mutopia Project | 1,860 | C1 | mutopiaproject.org |
| `abcmisc` | ABC Misc (John Chambers) | 1,487 | C1 | trillian.mit.edu/~jc/music/abc/ |
| `openscore` | OpenScore Lieder | 1,438 | C1 | github.com/OpenScore/Lieder |
| `maestro` | MAESTRO v3 | 1,276 | C2 | magenta.tensorflow.org/datasets/maestro |
| `groove` | Groove MIDI Dataset | 1,149 | C1 | magenta.tensorflow.org/datasets/groove |
| `emopia` | EMOPIA v2.2 | 1,071 | C2 | zenodo.org/records/5257995 |
| `nottingham` | Nottingham Music Database (corrected ABC) | 1,033 | C1 | ifdo.ca/~seymour/nottingham/ |
| `wikifonia` | Wikifonia (PD subset) | 445 | C1 | synthzone.com/files/Wikifonia/Wikifonia.zip |
| `oga` | OpenGameArt | 340 | C1 | opengameart.org |
| `musicnet` | MusicNet | 297 | C1 | zenodo.org/records/5120004 |
| **Total** | | **133,667** | | |

> Sources examined but **not included** (redistribution not permitted, etc.) and the reasons are in `SOURCE-CATALOG.md`.

## 4. Fields (`meta/catalog.json`, 20 fields)

`id` · `t` title (90.0%) · `c`/`cn` composer slug / display name (100%) · `g` genre (95.4%) ·
`i` instrument (95.4%) · `p` period (88.4%) · `form` (46.8%) · `opus`/`no` (30.2% / 29.7%) ·
`yr` year (16.0%) · `r` region (72.1%) · `du` duration (100%) ·
`nn` note count (100%) · `z` tier (100%) · `l` licence (100%) · `v` quality flag (100%) ·
`f` relative path (100%) · `diff` difficulty (partial).

Completeness follows the rule **"empty is better than a vague placeholder"** — unknown values are left
blank rather than guessed. Four indexes: `index-by-composer.json` · `index-by-period.json` ·
`index-by-region.json` · `index-by-source.json`.

## 5. Licence and usage

- Per-track licence in field `l`; tier summary in §2; audit basis in `LICENSE-AUDIT.md`
- **`main` (C1)**: commercial use permitted, with attribution per source
- **`piano-special` (C2)**: non-commercial only (CC BY-NC-SA 4.0); commercial use needs separate permission
- **`study` (C3)**: study and research only — no redistribution, no commercial use
  - `chinafolk`: the melodies are traditional, but these files were optically recognised from the
    notated edition of the *Anthology of Chinese Folk Songs*, whose editorial/compilation work is
    protected → C3; attribution to the dataset and the underlying edition is required
  - `lakh`: the dataset itself is CC BY 4.0, but the content layer was filtered to remove tracks
    carrying copyright notices or pop/film paths → **conservatively C3**
- ⚠️ **Special term on `thesession`**: its data repository `LICENSE.md` adds a
  **"Prohibition on LLM Use"** on top of CC BY-SA 4.0 — the material must not be used, adapted,
  modified or processed with large language models (including LLM training, processing with LLM tools,
  or incorporation into LLM-related applications or systems), with an accessibility-only exception.
  **Please comply when using the `thesession` portion.**
- The `meta` package (catalogue / indexes / field docs / documents) is produced by this project and
  released under **CC0-1.0**
- This library contains **no** transcriptions of copyrighted pop, film or game music

## 6. Limitations

- Metadata comes from upstream datasets: composer spellings vary (merge table in the `meta` package);
  catalogue-number systems differ per composer (BWV / K. / D. / S. / Hob. …)
- Parts of the ABC → MIDI conversion are mechanical: **dynamics and tempo do not represent the original
  performance intention**
- `yr` and `ctry` coverage is low because most upstreams lack these fields — left blank rather than guessed
- A few sources are evidenced as **local snapshots** (no upstream-published checksum); see the checksum
  grading notes in `PROVENANCE.md`

## 7. Citation

See `CITATION.bib`. Using the `piano-special` package requires additionally citing the Aria-MIDI paper:

```bibtex
@inproceedings{bradshawaria,
  title={Aria-MIDI: A Dataset of Piano MIDI Files for Symbolic Music Modeling},
  author={Bradshaw, Louis and Colton, Simon},
  booktitle={International Conference on Learning Representations (ICLR)},
  year={2025}
}
```

---

## 中文摘要

midicn-lib 是对 **21 个公开 MIDI / 记谱数据集**的系统性二次整理，共 **133,667 首**，
统一为一份目录、20 个字段，并**逐首标注许可档位**。分包按**使用方式**（`main` 可商用 79,216 ·
`piano-special` 非商用 34,869 · `study` 学习研究 19,582 · `meta` 目录文档 CC0-1.0），
另附 19 个按来源分包。每个来源的**实际采集地址、取得方式与校验值**见 `PROVENANCE.md`。
特别注意 **TheSession** 数据在 CC BY-SA 4.0 之外附加了**禁止用于大语言模型**的条款。

---

## v1.23 Data Enhancement (2026-09-23)

Two new sources (ATEPP: 7,131 performance MIDIs; PDMX: 2,895 score-derived MIDIs) and 15 new fields.
See `FIELD-DICTIONARY.md` for full field semantics, coverage and provenance-marking conventions.

**New fields**: `difficulty` · `cn_zh` (Chinese composer names) · `birth`/`death` · `instrument_gm` (GM names) ·
`velocity_avg`/`velocity_range` · `notes_per_sec` · `pitch_range` · `midi.tempo` · `midi.timesig` ·
`version_type` (score/performance) · `performer`/`album` · `topic` · lyrics library (10,035 Chinese folk songs).

**Marking policy**: all algorithmically inferred fields carry a `*_src` marker (e.g. `key_src="inferred"`
with `extra.key_corr` confidence); unknown values are left empty rather than guessed.
