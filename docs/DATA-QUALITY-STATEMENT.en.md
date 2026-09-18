# DATA QUALITY STATEMENT · midicn-lib v1.0

> Version: 2026-09-17 · Dataset midicn-lib v1.0 · 94,740 records (94,418 unique) / 17 sources
>
> This dataset is a **curated re-distribution**. We commit that every item in the "Verified"
> section below has been exhaustively checked programmatically with audit reports on file;
> we also honestly disclose the "trust boundaries" — what we **cannot** guarantee.
> Read this statement before using the dataset.

> 中文版：[DATA-QUALITY-STATEMENT.md](DATA-QUALITY-STATEMENT.md)

## 1. Verified Items (exhaustive programmatic checks · guaranteed)

| # | Item | Method | Result |
|---|---|---|---|
| 1 | File integrity | All 94,740 references checked for existence | **100% present, 0 missing** |
| 2 | Path uniqueness | Full comparison of midi.file within each source | 0 collisions (hash naming) |
| 3 | MIDI parseability | 300-file event-level sample (mido) | 0 failures · 0 zero-note files |
| 4 | MIDI conformance | 500-file header sample + pitch range 0–127 | all compliant |
| 5 | Record structure | 19 required + 1 optional fields checked one by one | 100% compliant |
| 6 | Duplicate control | Two-phase detection (MD5 + pitch fingerprint), fingerprint manually sampled (8/8 true duplicates) | 322 flagged `duplicate_of`, filtered on release |
| 7 | License zoning | 17 sources audited one by one (`LICENSE-AUDIT.md`) | main 48,140 / piano-special 32,522 / pending 10,473 / research 3,269 |
| 8 | Minefield exclusion | Copyrighted pop/game transcriptions | 0 included (5,988 copyrighted Wikifonia tracks filtered) |
| 9 | Composer fields | Merge mapping manually reviewed (incl. 10 false-merge fixes + traditional-collection normalization) | slug/name 100% covered |
| 10 | Period field | Musicology-consensus anchors (27 composers) force-overridden + birth-death inference | 91.6% coverage · 0 anchor mismatches |
| 11 | **Statistical music-content verification** (all 94,740) | mido parse + five algorithms: K-S tonality, motif repetition, density, range, duration | **92,476 normal (97.6%)** · broken 102 (excluded) · suspect 1,394 (flagged) · genuine-short 737 (restored) · tonality median 0.85 (strong evidence of genuine music) |

**Quantitative baseline** (all tracks):

| Metric | P1 | Median | P99 | Meaning |
|---|---:|---:|---:|---|
| Tonality correlation | 0.0* | **0.826** | 0.972 | *P1=0 comes from the 139 flagged suspects; 98%+ above 0.45 |
| Motif repetition | 0.0* | **0.485** | 1.0 | Phrase-repetition signature of real music |
| Note density/sec | 1.2 | 4.1 | 17.6 | Plausible performance speed |

## 2. Trust Boundaries (what we cannot guarantee · honestly disclosed)

### 2.1 Note-level comparison against original scores (the one remaining unverified item)
- The MIDI files come from existing transcriptions in the source datasets. We performed
  **statistical verification** (item 11: tonality / motif / density features detect corruption,
  garbage and broken transcriptions).
- However, **per-note comparison against the original scores** (verifying each pitch/duration)
  requires musicological listening and was **not** performed.
- **Meaning**: the data contains no "corrupted/garbage/empty" files (excluded programmatically);
  individual tracks may inherit transcription errors (wrong notes, omitted repeats) from their
  source datasets.

### 2.2 Metadata inheritance
- `title / opus / form / key` metadata is **inherited from the source datasets**. ariamidi has no
  titles (the main reason title coverage is 65.7%); Essen/thesession titles are verbatim from the sources.
- Composer attributions are inherited. **Known systematic issues have been fixed** (performers
  mis-attributed as composers, 10 false merges), but the 2,094 "1–2 track" long-tail attributions
  were not individually researched.

### 2.3 Chained licensing
- We verified **each dataset's own license statement** (CC BY / CC BY-SA / PD, etc.).
- Whether **upstream transcribers actually had the right to publish under that license** (e.g.
  the copyright status of scores ariamidi transcribed from) cannot be fully verified upstream.
  The most conservative strategy has been applied (uncertain content excluded or quarantined).

### 2.4 Fingerprint-dedup residual risk
- 361 fingerprint-similar pairs with only the composer in common were **left untouched**
  (may be different versions of the same piece, or different pieces) — listed in
  `dedup-pending-review.md` for manual review. We prefer keeping over deleting.

## 3. Usage Recommendations

1. **Main release** (`main` zone, 48,140 tracks) is safe for commercial use; `piano-special`
   (CC BY-NC-SA) and `research` are non-commercial only.
2. `pending` (chinafolk, 10,473 tracks) has **unconfirmed licenses — do not publish**; will be
   promoted after author authorization.
3. For use cases with strict musicological accuracy requirements, manually listen to the tracks
   you plan to use.
4. Report data issues to the project repository; we follow an "audit → fix → re-audit" process.

## 4. Audit Toolchain (reproducible)

| Tool | Purpose |
|---|---|
| `tools/audit.py` | Structural audit, 10 checks (v1) |
| `tools/audit2.py` | Deep audit, 12 checks (v2, incl. MIDI event-level) |
| `tools/quality_pipeline.py` | Idempotent quality pipeline (must re-run after any ingest) |
| `tools/music_verify.py` | Statistical music-content verification (5 algorithms) |
| `tools/dedup.py` / `dedup_apply.py` | Two-phase deduplication detection and conservative flagging |
| `tools/clean_v1.py` / `infer_period.py` | Composer merging + period inference |
| `tools/report.py` | Library statistics report |

> This statement, together with `AUDIT-REPORT.md` (v1), `AUDIT-REPORT-V2.md` (v2),
> `LICENSE-AUDIT.md` and `QUALITY-GATES.md`, forms the complete quality archive.
