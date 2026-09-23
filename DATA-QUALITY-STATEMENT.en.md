# DATA QUALITY STATEMENT · midicn-lib

> Verified on **2026-09-21** · dataset midicn-lib (current) · **133,667** tracks / **21** sources ·
> tiers: main 79,216 / piano-special 34,869 / study 19,582
>
> This dataset is a **curated re-distribution**. Every item in the "Verified" section has been checked
> programmatically with audit reports on file; we also disclose the "trust boundaries" — what we
> **cannot** promise. The original v1.0 wording (94,740 tracks / 17 sources, 2026-09-17) is retained as a
> historical baseline at the end of this file (Chinese version).

## 1. Verified items

| # | Item | Method | Result (current, 133,667 tracks) |
|---|---|---|---|
| 1 | **File integrity** | release tree compared one-to-one with the catalogue (re-checked 2026-09-21) | **133,667 MIDI files present, 0 missing** |
| 2 | Path uniqueness | full comparison of `midi.file` per source | 0 conflicts |
| 3 | **MIDI parseability** | every file re-parsed with mido at ingest; duration & note count recomputed | `du` / `nn` coverage **100%** |
| 4 | MIDI conformity | header + pitch range 0–127 (v1.0: 500-file sample) | all conformant |
| 5 | Record structure | 20 fields (19 required + optional `duplicate_of`) | 100% compliant |
| 6 | Duplicate control | two-stage detection (MD5 + pitch fingerprint), fingerprint sampling verified | `duplicate_of` filtered at release; 742 same-content GiantMIDI transcriptions removed in v1.5 |
| 7 | **Licence zoning** | 19 sources audited one by one (`docs/LICENSE-AUDIT.md`) | main 79,216 / piano-special 34,869 / study 19,582 |
| 8 | Minefield exclusion | copyrighted pop/game transcriptions | 0 included (5,988 Wikifonia copyrighted files filtered; Lakh filtered by copyright notice and pop/film paths) |
| 9 | Composer field | merge mapping manually reviewed | slug/name **100%** coverage |
| 10 | Period field | musicological anchors + life-date inference | 88.1% coverage, 0 anchor mismatches |
| 11 | **Statistical music verification** | mido + five algorithms (tonality K-S, motif repetition, density, range, duration) | **baseline: all 94,740 tracks at v1.0** (97.6% normal); later batches verified per file (item 3) |

Quantitative evidence (v1.0 full baseline, 94,740 tracks): tonality correlation median **0.826** (P99 0.972),
motif repetition median **0.485**, note density median 4.1/s. Report: `docs/music-verify-report.md`
(regenerable via `tools/music_verify.py`).

## 2. Trust boundaries (disclosed honestly)

1. **Note-level comparison against original scores** is the only unperformed check. We did statistical
   verification (item 11) plus per-file parsing (item 3); individual transcription errors inherited from
   upstream datasets may remain.
2. **Inherited metadata**: titles/opus/form trust the upstream datasets, enriched from multiple sources
   (IMSLP work catalogues, Essen geography, official composer tables — tens of thousands of fixes).
   Title coverage is now 90.0%; untitled tracks get a composer+number display name (100% distinguishable).
3. **Chained licensing**: we verified each dataset's own licence statement, but cannot fully verify
   upstream transcribers' authorisation chains. Conservative zoning (exclusion or isolation) applied.
4. **Fingerprint dedup residue**: fingerprint-similar pairs sharing only a composer were kept
   ("keep over delete") and listed for manual review.

## 3. Usage advice

1. `main` (C1, 79,216) — commercial use allowed with attribution per source.
2. `piano-special` (C2, 34,869) — CC BY-NC-SA 4.0: non-commercial only.
3. `study` (C3, 19,582) — study/research only: no redistribution, no commercial use.
   - `chinafolk` (10,473): traditional melodies, but the MIDI was recognised from the protected notated
     edition of the *Anthology of Chinese Folk Songs* → published as C3 with mandatory attribution.
   - `lakh` (9,630): dataset is CC BY 4.0, but the content-filtered subset is **conservatively C3**.
4. ⚠️ **`thesession` (23,250)**: CC BY-SA 4.0 **plus a "Prohibition on LLM Use"** term (see `LICENSE.md` §2.2).
5. For musicologically strict use, listen to the tracks you rely on.
6. Report issues via the project repository; we follow an audit → fix → re-audit loop.

## 4. Tool chain

`tools/audit*.py` (structural & deep audits) · `tools/quality_pipeline.py` · `tools/dedup*.py` ·
`tools/music_verify.py` · `tools/provenance.py` (**provenance verifier**) ·
`tools/sync_docs.py` / `tools/preflight.py` (single-source docs sync / **release pre-flight gate**).

Together with `AUDIT-REPORT*.md`, `LICENSE-AUDIT.md`, `QUALITY-GATES.md` and `PROVENANCE.md` this forms
the complete quality and provenance archive.

## 5. Version history

- **v1.0 (2026-09-17)**: 94,740 tracks / 17 sources — the original statement and the full statistical
  music verification were executed at that point.
- **Current (re-verified 2026-09-21)**: 133,667 tracks / 19 sources. Later sources were per-file parse
  verified (`du`/`nn` 100%) and admitted under the same licence gate; release-tree integrity confirmed in
  this review. Zoning is main / piano-special / study since v1.6 (the `pending` and `research` zones were
  retired: chinafolk published as C3 after licence assessment; maestro & emopia published as C2).

---

## v1.23 Data Enhancement (2026-09-23)

Two new sources (ATEPP: 7,131 performance MIDIs; PDMX: 2,895 score-derived MIDIs) and 15 new fields.
See `FIELD-DICTIONARY.md` for full field semantics, coverage and provenance-marking conventions.

**New fields**: `difficulty` · `cn_zh` (Chinese composer names) · `birth`/`death` · `instrument_gm` (GM names) ·
`velocity_avg`/`velocity_range` · `notes_per_sec` · `pitch_range` · `midi.tempo` · `midi.timesig` ·
`version_type` (score/performance) · `performer`/`album` · `topic` · lyrics library (10,035 Chinese folk songs).

**Marking policy**: all algorithmically inferred fields carry a `*_src` marker (e.g. `key_src="inferred"`
with `extra.key_corr` confidence); unknown values are left empty rather than guessed.
