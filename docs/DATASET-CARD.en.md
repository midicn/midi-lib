# DATASET CARD · midicn-lib v1.0

> 94,740 records · 17 source datasets · unified 21-field schema · five-level quality flags · full provenance
>
> This card describes the contents, sources, quality verification, and usage restrictions of midicn-lib.

> 中文版：[DATASET-CARD.md](DATASET-CARD.md)

## 1. Overview

midicn-lib is a systematic re-curation of 17 public MIDI datasets:

- **Unified schema**: every record converted to a 21-field structure (19 required + 2 optional) with consistent cross-source semantics
- **Quality verification**: structural audit (10 checks) + deep audit (12 checks) all passed; statistical music-content verification executed on all tracks
- **License zoning**: tracks partitioned into main / piano-special / pending / research by commercial usability
- **Provenance**: every record keeps its original dataset path (`src_path`); the license audit of all 17 sources is public

## 2. Sources and Counts

| Source | Dataset | Tracks | Content | License | Zone |
|---|---|---:|---|---|---|
| `aria` | ariamidi | 32,522 | Classical piano (auto-transcribed) | CC BY-NC-SA-4.0 | piano-special |
| `thesession` | TheSession.org | 23,294 | Irish traditional tunes | CC BY-SA-4.0 | main |
| `chinafolk` | Chinese Folk Collection | 10,479 | Folk songs of China | UNSPECIFIED (pending) | pending |
| `essen` | Essenfolkdance (EsAC) | 10,448 | World folk songs | Open declaration | main |
| `norbeck` | Norbeck Abby | 3,473 | Irish/Swedish traditional | Open declaration | main |
| `mutopia` | Mutopia Project | 1,861 | Classical instruments (from PD scores) | Per-track (mostly PD) | main |
| `abcmisc` | ABC standard collections | 1,579 | Klezmer/Balkan/folk | Open declaration | main |
| `openscore` | OpenScore Lieder Corpus | 1,440 | Art songs (incl. women composers) | CC0-1.0 | main |
| `maestro` | MAESTRO v3 | 1,276 | Piano performance alignment | CC BY-NC-SA-4.0 | research |
| `groove` | Groove MIDI Dataset | 1,150 | Professional drum performances | CC BY-4.0 | main |
| `emopia` | EMOPIA v2.2 | 1,071 | Pop piano + emotion quadrants | CC BY-NC-SA-4.0 | research |
| `nottingham` | Nottingham ABC | 1,037 | British/American folk | Open declaration | main |
| `musedata` | MuseData (CCARH) | 924 | Classical instruments | CCARH restricted | research |
| `oga` | OpenGameArt.org | 342 | Original game music | CC0/CC-BY per track | main |
| `musicnet` | MusicNet | 330 | Classical chamber | CC BY-4.0 | main |
| `wikifonia` | Wikifonia archive (PD subset) | 446 | Traditional/folk lead sheets | PD | main |
| `m21` | music21 CoreCorpus | 3,068 | Classical/folk mixture | PD | main |

## 3. Zones

| Zone | Count | Usage rights |
|---|---:|---|
| `main` | 48,140 | ✅ Commercial use allowed (license annotated per track) |
| `piano-special` | 32,522 | ⚠️ Non-commercial only (CC BY-NC-SA) |
| `pending` | 10,473 | ❌ Not distributed in this release (Chinese collection, license pending) |
| `research` | 3,269 | ❌ Not distributed in this release (NC academic use) |

## 4. Quality Verification Summary

| Layer | Checks | Result |
|---|---|---|
| Structural v1 (10) | file integrity / path uniqueness / JSON / fields / enums / zoning / dedup refs / composers / region / MIDI header | ✅ all pass |
| Deep v2 (12) | MIDI events / pitch range / id prefix / provenance / name-slug / duplicate keep / cross-zone priority / period anchors / value ranges / synonyms / title / license semantics | ✅ all pass |
| **Music content** (all tracks) | tonality correlation (median 0.826) · motif repetition (0.485) · density/range/duration | 102 broken excluded · 1,394 suspect flagged |

Full reports: `docs/AUDIT-REPORT.md` (v1), `docs/AUDIT-REPORT-V2.md` (v2), `midi_db/stats/music-verify-report.md`.

## 5. Fields

See [schema.md](schema.md). Key: `c/cn` composer · `t` title · `g` genre · `p` period · `r` region · `z` zone · `l` license · `v` quality flag · `f` file path.

## 6. Limitations (honest disclosure)

1. **Transcription accuracy**: MIDI files come from the source datasets' existing transcriptions. This library performs statistical verification (detects corruption/garbage), but **note-level comparison against original scores** was not performed.
2. **Metadata**: inherited from source datasets; ariamidi has no titles (main reason title coverage is 65.7%).
3. **Chained licensing**: each dataset's own license statement was verified; upstream transcribers' authorization chains cannot be fully verified.
4. **Chinese collection**: 10,473 tracks pending license confirmation, not included in this release.
5. **Long-tail attributions**: 2,094 composer names appearing only 1–2 times were not individually researched.

## 7. Citation (BibTeX)

```bibtex
@dataset{midicn_lib_2026,
  title     = {midicn-lib: A Curated Multi-Source MIDI Library},
  author    = {midicn.com},
  year      = {2026},
  version   = {v1.0},
  url       = {https://github.com/midicn/midi-lib},
  note      = {104,380 tracks from 18 public datasets, unified schema,
               quality-verified and license-zoned}
}
```

Please also cite the source datasets you actually use (table in §2).

## 8. Maintenance

- Project page: midicn.com
- Issues: GitHub Issues
- Updates follow the "audit → fix → re-audit" process; all changes keep an audit trail
