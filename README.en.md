# midicn-lib v1.0 · MIDI Library (Curated Edition)

> 94,740 records · 17 source datasets · Unified 21-field schema · Five-level quality flags · Full provenance
>
> This library is a **systematic re-curation** of 17 public MIDI datasets: unified fields, quality
> verification, license zoning, and index construction. We publish not only the audio files but the
> **complete curation process and audit trail** — every step reproducible, traceable, and open to scrutiny.

> [中文版 README](README.md)

## 📦 Package Structure

| Directory | Contents | Count | License |
|---|---|---:|---|
| `main/` | Commercially usable: Irish folk, world folk, British folk, Klezmer/Balkan, classical (open), game, drum | ~48,140 | CC BY / CC BY-SA / PD |
| `piano-special/` | Classical piano (auto-transcribed) | 32,522 | CC BY-NC-SA (**non-commercial**) |
| `meta/` | Full catalog `catalog.json` + 4 navigation indexes + MD5 checksums | — | CC0 |
| `research/` | Research use (not distributed with this release) | — | — |

**Not included**:
- Chinese folk collection (10,473 tracks) — pending license confirmation; will ship as a separate package
- Broken files (102; parse failures / empty) — excluded after verification
- Duplicated files (322; MD5 / pitch-fingerprint detection) — excluded after verification

## 🗂️ main/ Breakdown

| Subdirectory | Contents | Count | Sources |
|---|---|---:|---|
| `folk-ireland/` | Irish traditional dance tunes & songs | 26,689 | TheSession, Norbeck |
| `folk-world/` | World folk songs (China, Germany, Nordic, …) | 10,818 | Essen, Wikifonia (PD) |
| `klezmer-balkan/` | Klezmer & Balkan tunes | 1,487 | ABCMisc |
| `folk-british/` | British & American folk | 1,033 | Nottingham |
| `classical-open/` | Classical, open license (Renaissance–Romantic) | 6,624 | Mutopia, OpenScore, music21, MusicNet |
| `game/` | Original game music | 340 | OpenGameArt |
| `drum/` | Drum grooves & patterns | 1,149 | Groove MIDI |

## 🚀 Quick Start

```python
import json
catalog = json.load(open("meta/catalog.json"))["tracks"]

main_only = [t for t in catalog if t["z"] == "main"]            # commercial only
bach      = [t for t in catalog if t["c"] == "bach"]            # by composer
romantic  = [t for t in catalog if t["p"] == "romantic"]        # by period
games     = [t for t in catalog if t["g"] == "game"]            # by genre
clean     = [t for t in catalog if not t["v"]]                  # fully verified only
```

The four index files in `meta/` (`index-by-composer.json`, `index-by-region.json`,
`index-by-period.json`, `index-by-source.json`) map keys to track-id lists and can be used
directly for front-end navigation without loading the full catalog.

## 🏷️ Field Reference (full definitions in [schema.md](schema.md))

Each track carries 21 fields (19 required + 2 optional). Key fields:

| Field | Meaning |
|---|---|
| `c` / `cn` | Composer slug / display name (traditional tunes are unified to `traditional`) |
| `t` | Title (Chinese folk titles preserved in Chinese) |
| `g` / `p` / `r` / `i` | Genre / musical period / region / instrument |
| `z` | Zone: `main` commercial · `piano-special` non-commercial |
| `l` | License (per-track annotation) |
| `v` | Quality flag: `broken` excluded · `suspect` feature anomaly, review advised · `verified-short` genuine short piece · `extreme-range` extreme pitch range |
| `f` | File path (unified `{id}.mid` naming) |
| `duplicate_of` | If a duplicate, points to the retained record (excluded from this release) |

## ✅ Quality Assurance (see [DATA-QUALITY-STATEMENT.en.md](DATA-QUALITY-STATEMENT.en.md))

Every item below is exhaustively verified programmatically; audit reports ship with this release:

1. **File integrity**: all 94,740 references verified, zero missing
2. **Path uniqueness**: zero collisions within each source
3. **MIDI parseability**: 300-file event-level sample, zero failures
4. **Statistical music-content verification** (all 94,740): tonality correlation median **0.826**, motif-repetition median **0.485** — strong evidence of genuine musical content; corrupted/garbage files excluded
5. **Duplicate control**: two-phase detection (MD5 + pitch fingerprint); 322 high-confidence duplicates flagged and excluded
6. **License audit**: 17 sources reviewed one by one; zero copyrighted pop/game transcriptions included
7. **Composer fields**: merge mapping manually reviewed, zero false merges

**Honestly disclosed trust boundaries** (Statement §2): note-level comparison against original scores not performed; metadata inherited from source datasets; chained licensing cannot be fully verified upstream.

## 📜 License

Licenses differ per source — **consult [LICENSE-AUDIT.md](docs/LICENSE-AUDIT.md) before use**:

- `main/`: per-track license in field `l` — predominantly CC BY / CC BY-SA / public domain
- `piano-special/`: **CC BY-NC-SA 4.0 — non-commercial use only**, attribution required
- Cite the whole dataset using the BibTeX below

## 📖 Citation (BibTeX)

```bibtex
@dataset{midicn_lib_2026,
  title     = {midicn-lib: A Curated Multi-Source MIDI Library},
  author    = {midicn.com},
  year      = {2026},
  version   = {v1.0},
  url       = {https://github.com/midicn/midi-lib},
  note      = {94,740 tracks from 17 public datasets, unified schema,
               quality-verified and license-zoned}
}
```

## 🙏 Source Datasets (17)

ariamidi · TheSession · Chinese Folk Collection · Essenfolkdance · Norbeck · Mutopia ·
ABCMisc · OpenScore Lieder Corpus · MAESTRO · Groove MIDI · EMOPIA · Nottingham ·
MuseData · OpenGameArt · MusicNet · Wikifonia (PD subset) · music21 corpus

Full provenance and license audit: [LICENSE-AUDIT.md](docs/LICENSE-AUDIT.md). Per-source counts: [DATASET-CARD.md](DATASET-CARD.md).

## 🛠️ Curation Toolchain (fully open source, reproducible)

All curation scripts ship with the repository (`tools/`):
`quality_pipeline.py` (quality pipeline) · `music_verify.py` (music-content verification) ·
`dedup.py` (deduplication) · `clean_v1.py` (composer merging) · `infer_period.py` (period inference) ·
`audit.py` / `audit2.py` (final audits)

Anyone can re-run the entire pipeline on the original datasets and obtain results consistent with this release.
