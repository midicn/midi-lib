# midicn-lib · Open MIDI Library (Curated Edition)

> **124,179** tracks · **19** public sources · **14** categories · per-track licence tier · full provenance
>
> Portal & player: <https://lib.midicn.com> · Downloads: <https://lib.midicn.com/download.html>
> Provenance ledger (how each address was obtained, with checksums): <https://lib.midicn.com/provenance.html>

This repository is the **data release repository** of midicn-lib: catalogue, indexes, field
documentation, licence audit and the curation tool chain. The site source lives in
[midicn/midi-lib-site](https://github.com/midicn/midi-lib-site).

## 📦 Packages (split by usage tier, not by genre)

| Directory | Meaning | Tier | Tracks | Download |
|---|---|---|---:|---|
| `main/` | licences permit commercial use | **C1** | 69,197 | `midicn-lib-<VER>-main.zip` |
| `piano-special/` | non-commercial only | **C2** | 34,869 | `midicn-lib-<VER>-piano-special.zip` |
| `study/` | study / research only | **C3** | 20,113 | `midicn-lib-<VER>-study.zip` |
| `meta/` | catalogue / indexes / field docs / documents | **CC0-1.0** | — | `midicn-lib-<VER>-meta.zip` |
| **Total** | | | **124,179** | plus 19 per-source packages (`-source-<id>.zip`) |

> Assets per release: [Releases](https://github.com/midicn/midi-lib/releases). The current version always
> matches <https://lib.midicn.com/download.html>.

## 🗂️ Categories (14)

**`main/` (C1 · 69,197)** — `folk-ireland/` 26,689 · `hymn/` 10,945 · `folk-world/` 10,818 ·
`piano-performance/` 10,112 · `classical-open/` 6,624 · `klezmer-balkan/` 1,487 · `maestro/` 1,276 ·
`drum/` 1,149 · `emopia/` 1,071 · `folk-british/` 1,033 · `game/` 340

**`piano-special/` (C2 · 34,869)** — `piano/` 32,522 · `maestro/` 1,276 · `emopia/` 1,071

**`study/` (C3 · 20,113)** — `folk-china/` 10,473 · `classical-traditional/` 9,640

## 🚀 Quick start

```python
import json
cat = json.load(open('meta/catalog.json', encoding='utf-8'))
# 20 fields per record (see schema.md)
# handy: id / t title / c composer / z tier / l licence / f path / du seconds / nn notes
piano = [r for r in cat['tracks'] if r['z'] == 'piano-special']
```

Indexes in `meta/`: `index-by-composer.json` · `index-by-period.json` · `index-by-region.json` ·
`index-by-source.json` · `MD5SUMS.txt` (per-file checksums).

## 🏷️ Fields

20 fields (`id,t,c,cn,g,p,r,i,z,l,v,f,opus,no,form,ctry,diff,yr,du,nn`) — full definitions in
[`schema.md`](schema.md). Coverage: composer **100%** · duration/note count **100%** · title 90.0% ·
genre/instrument 95.4% · period 88.1% · form 46.0% · opus 26.0%.
**Empty beats a vague placeholder** — unknown values are left blank.

## ✅ Quality

File integrity, structural compliance, per-file duration/note recount, duplicate control, licence zoning
and minefield exclusion — each verified programmatically and backed by audit reports; trust boundaries
(e.g. no note-by-note human listening) are disclosed honestly. See
[`DATA-QUALITY-STATEMENT.md`](DATA-QUALITY-STATEMENT.md).

## 📜 Licence

- Per-track licence in field `l`; tier (C1 / C2 / C3) in field `z`
- Full legal terms: [`LICENSE.md`](LICENSE.md) · attributions: [`NOTICE.md`](NOTICE.md) ·
  audit: [`docs/LICENSE-AUDIT.md`](docs/LICENSE-AUDIT.md)
- ⚠️ **`thesession` additional term**: on top of CC BY-SA 4.0, **use with large language models is
  prohibited** (LLM training, LLM-tool processing, or incorporation into LLM-related applications;
  accessibility use is the only exception)
- The `meta/` directory, curation documents and tool chain are released under **CC0-1.0**

## 📖 Citation

```bibtex
@misc{midicnlib,
  title  = {midicn-lib: an open MIDI library with per-track licence tagging},
  author = {midicn project},
  year   = {2026},
  url    = {https://lib.midicn.com},
  note   = {124,179 tracks aggregated from 19 public datasets, unified catalogue,
            per-track licence tiers. Access version: see the Releases page.}
}
```

Using `piano-special/` requires additionally citing the Aria-MIDI paper
(see [`DATASET-CARD.md`](DATASET-CARD.md) §7).

## 🙏 Sources (19)

**Addresses are the places we actually obtained the data from** — method, evidence and checksums in
[PROVENANCE.md](PROVENANCE.md) (on-site version: <https://lib.midicn.com/provenance.html>).

| Source | Tracks | Tier | Acquisition address |
|---|---:|---|---|
| Aria-MIDI (Unique subset) | 32,522 | C2 | github.com/loubbrad/aria-midi |
| The Session | 23,250 | C1 | github.com/adactio/TheSession-data |
| The Cyber Hymnal | 10,945 | C1 | hymntime.com/tch |
| Anthology of Chinese Folk Songs (OMR) | 10,473 | C3 | github.com/m-july/Anthology-of-Chinese-Folk-Songs |
| ESAC folk-song archive | 10,373 | C1 | esac-data.org |
| GiantMIDI-Piano | 10,112 | C1 | github.com/bytedance/GiantMIDI-Piano |
| Lakh MIDI Dataset (filtered) | 9,640 | C3 | colinraffel.com/projects/lmd/ |
| Norbeck ABC collections | 3,439 | C1 | norbeck.nu/abc/ |
| music21 CoreCorpus | 3,029 | C1 | github.com/cuthbertLab/music21 |
| Mutopia Project | 1,860 | C1 | mutopiaproject.org |
| ABC Misc (John Chambers) | 1,487 | C1 | trillian.mit.edu/~jc/music/abc/ |
| OpenScore Lieder | 1,438 | C1 | github.com/OpenScore/Lieder |
| MAESTRO v3 | 1,276 | C2 | magenta.tensorflow.org/datasets/maestro |
| Groove MIDI Dataset | 1,149 | C1 | magenta.tensorflow.org/datasets/groove |
| EMOPIA v2.2 | 1,071 | C2 | zenodo.org/records/5257995 |
| Nottingham Music Database (corrected) | 1,033 | C1 | ifdo.ca/~seymour/nottingham/ |
| Wikifonia (PD subset) | 445 | C1 | synthzone.com/files/Wikifonia/Wikifonia.zip |
| OpenGameArt | 340 | C1 | opengameart.org |
| MusicNet | 297 | C1 | zenodo.org/records/5120004 |

Sources examined but **not included** (redistribution not permitted, etc.): [SOURCE-CATALOG.md](SOURCE-CATALOG.md).

## 🛠️ Tool chain (open source, reproducible)

`tools/ingest_*.py` (19 ingesters) · `tools/build_release.py` (release tree + catalogue + indexes) ·
`tools/enrich_*.py` (metadata enrichment) · `tools/dedup*.py` (two-stage dedup) ·
`tools/music_verify.py` (statistical music verification) ·
`tools/provenance.py` (**provenance verifier**) · `tools/sync_docs.py` (single-source docs sync) ·
`tools/preflight.py` (**release pre-flight gate**).

---

**中文**：见 [README.md](README.md) · Dataset card: [DATASET-CARD.md](DATASET-CARD.md) ·
Provenance: [PROVENANCE.md](PROVENANCE.md) · Licence: [LICENSE.md](LICENSE.md)
