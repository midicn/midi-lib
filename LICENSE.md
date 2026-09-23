# LICENSE · 许可与法律条款 / License & Legal Terms

> 本文件说明 midicn-lib 的整体许可结构、各来源的许可归属、二次分发规则、免责声明与权利救济。
> This file describes the overall licensing structure of midicn-lib, per-source license attribution,
> redistribution rules, disclaimers, and remedies.

> **中文** | [English](#english)

---

# 中文部分

## 1. 总体结构

midicn-lib 是 **21 个来源数据集**的系统性二次整理。我们**不重新授权任何 MIDI 文件**——每个文件遵循其原始来源的许可：

1. **`meta/` 目录**（目录、索引、校验文件）与**全部整理文档、审计报告、工具脚本**：由 midicn 项目发布，采用 **CC0 1.0（公有领域贡献）**。你可以自由使用、修改、再分发，无需署名（但欢迎注明来源）。
2. **MIDI 文件**：遵循各来源数据集的许可，**逐曲标注于 `l` 字段**（详见 `meta/catalog.json` 与 [LICENSE-AUDIT.md](docs/LICENSE-AUDIT.md)）。
3. **分区规则**：
   - `main/`——来源许可允许再分发（CC BY / CC BY-SA / 公有领域 / 开放声明）
   - `piano-special/`——**CC BY-NC-SA 4.0：仅限非商业目的**，使用时须署名并以相同方式共享
   - `study/`——**仅限学习与研究**（如 TRADITIONAL-STUDY、Lakh 过滤子集）：不得再分发、不得商用
   - 未收录任何许可不明确或禁止再分发的来源（全量考察范围见 `SOURCE-CATALOG.md`）

## 2. 使用义务（按许可类型）

使用 `main/` 或 `piano-special/` 中的曲目时，你必须遵守该曲目 `l` 字段所标注许可的全部义务：

| 许可 | 署名 | 相同方式共享 | 非商业 | 附加要求 |
|---|---|---|---|---|
| CC BY 4.0 | ✅ 必须 | — | — | 注明作者、来源、许可链接、修改说明 |
| CC BY-SA 4.0 | ✅ 必须 | ✅ 必须 | — | 演绎作品须以相同许可发布 |
| CC BY-NC-SA 4.0 | ✅ 必须 | ✅ 必须 | ✅ 禁止商用 | 仅限非商业目的 |
| CC0 / 公有领域 | 建议 | — | — | 自由使用 |
| 开放声明 | 建议注明来源 | — | 视声明而定 | 见 LICENSE-AUDIT.md 各源说明 |

**署名的最低要求**：在显著位置注明「来源：midicn-lib（github.com/midicn/midi-lib）」及对应原始数据集名称。对于网站播放场景，请在页面或「关于」页集中署名。

### 2.1 TRADITIONAL-STUDY（传统民歌 · 仅研究/学习）

适用于 `l = TRADITIONAL-STUDY` 的曲目（本版为中国民间歌曲集成 10,473 首）：

- **旋律本身**：属传统民间文学艺术，作者不可考、流传久远，作为音乐作品通常已进入公有领域
- **但转录底本受保护**：本批文件依据《中国民间歌曲集成》的记谱／整理稿光学识别而来，该整理与汇编成果受版权保护
- **允许**：研究、教学、学习用途下的使用与共享
- **禁止**：任何商业使用；公开表演／广播；录音制品；去除或篡改来源标注后分发
- **必须**：显著标注来源为「中国民间歌曲集成（Anthology of Chinese Folk Songs，OMR 数据集，
  github.com/m-july/Anthology-of-Chinese-Folk-Songs）」
- **商用需另行授权**：若需商业使用，请自行向底本权利人取得许可，本站不提供该授权

### 2.2 TheSession · 附加条款（禁止用于大语言模型）

`thesession` 来源（23,250 首）在 **CC BY-SA 4.0** 授权之外**附加了「禁止用于大语言模型」条款**：

- **禁止**：以大语言模型使用、改编、修改或处理该素材——包括但不限于**训练大模型**、
  借助 **LLM 工具**处理、并入任何 **LLM 相关应用或系统**
- **唯一豁免**：为残障人士（如视障者）提供**无障碍方案**所必需的使用
- 依据：上游数据仓 `LICENSE.md` 的 *Prohibition on LLM Use* 一节（见本库 `PROVENANCE.md`）
- 该条款与 CC BY-SA 4.0 的署名、相同方式共享义务**并行**，不因本库的格式转换而消失

> 换言之：`thesession` 部分可以自由用于一般用途（含商业用途、须署名并相同方式共享），
> **但不得投入大模型相关的训练或处理流程**。

### 2.3 内嵌歌词 · 独立权利层（仅研究/学习）

部分曲目文件内含 **MIDI lyric meta-event（内嵌歌词文本）**。本版发布侧共 **2,778 首**带内嵌歌词，
按来源分布：openscore 1,436（CC0）· m21 563（PD）· wikifonia 365（PD）· mutopia 250（PD）·
lakh 136（C3）· cyberhymnal 28（PD）。

**歌词是独立于曲目的另一层权利对象，单独适用以下规则：**

- **不随曲目档位授予商用许可**：即使某曲目属 `main`（可商用），其**内嵌歌词文本**仍
  **仅限研究、教学、学习**用途；不得将歌词文本单独用于商业用途、出版、录制或再分发。
- **不主张权利**：本库对任何歌词文本**不主张著作权**，也不构成歌词权利人的授权表示。
  歌词权利（如有）属于其原作者／词作者／出版商。
- **为什么必须单列**：上游数据集对 **MIDI 文件本身**授予的许可（CC BY 4.0 / PD / CC0）
  **不能自动延伸**到文件中可能由第三方写入的歌词文本——**许可人只能授权自己拥有的权利**，
  「容器被授权」不等于「容器内第三方内容被授权」。因此本库**不作"歌词随文件一并授权"的主张**，
  而是保守地把歌词整体限定为研究用途。
- **风险实测分级**：2,778 首中约 **2,642 首**来自以公有领域内容为限的来源
  （OpenScore Lieder 的歌词作者如歌德、海涅等；Mutopia 仅收 PD 作品；hymnal 为赞美诗），
  其歌词本身即属公有领域，实质无风险；**风险集中在 lakh 的 136 首**（歌词多为 20 世纪
  商业歌曲），该批曲目本身已定级 **C3（study）**，且其中在保护期内者已被剔除。
- **歌词库**：中国民歌歌词（`midi_db/lyrics/`，10,035 首）**不在发布包内**，仅站内检索展示。
- **被要求时**：若歌词权利人提出异议，按第 7 节流程移除对应文件或其中的歌词事件。

> 实践含义：把本数据集当**乐谱／演奏数据**使用不受影响；若要**抽取并再使用歌词文本**，
> 请仅限研究/学习，并自行清理权利。

## 3. 二次分发规则

- 允许再分发本数据集的全部或部分内容，**前提是**：
  1. 保留或不破坏随附的许可信息（逐曲 `l` 字段、本文件、`LICENSE-AUDIT.md`）；
  2. 遵守每首曲目所标许可的全部义务（上表）；
  3. 不以任何方式暗示该内容由你原创。
- **禁止**：
  - 去除、隐藏或篡改许可标注后分发；
  - 将 `piano-special/`（CC BY-NC-SA）内容用于任何商业用途；
  - 声称对原始作品或本整理成果拥有排他性权利。

## 4. 免责声明（DISCLAIMER）

**本数据集按「现状」（AS IS）提供，不附任何形式的明示或默示担保。**

在适用法律允许的最大范围内：

1. **不保证准确性**：MIDI 文件来自各来源数据集的既有转录。我们完成了文件完整性、结构合规与统计级音乐内容验证（详见 [DATA-QUALITY-STATEMENT.md](DATA-QUALITY-STATEMENT.md)），但**未逐音符比对原始乐谱**。个别曲目可能存在转录误差（错音、省略反复、力度缺失等），此类问题继承自原始数据集。
2. **不保证可用性**：不保证数据适用于任何特定用途（包括但不限于商业发行、训练机器学习模型、公开表演等）。
3. **不保证权利链完整**：我们核实了各来源数据集自身的许可声明，但**无法穿透验证上游转录者对原始作品的授权链**。若任何权利人认为某曲目侵犯其权利，请通过第七节的流程联系我们，我们将在核实后移除。
4. **责任限制**：对于因使用或无法使用本数据集而产生的任何直接、间接、附带、特殊、惩罚性损失（包括但不限于商誉损失、数据丢失、营业中断），midicn 项目及其贡献者在适用法律允许的最大范围内**不承担责任**。
5. **你独自承担使用责任**：下载数据即表示你理解并接受上述条款；商业使用前请自行完成尽职调查。

## 5. 商标

「midicn」「midicn.com」「midicn-lib」及相关的项目名称与标识是 midicn 项目的名称与商标。本许可**不授予**使用这些名称推广衍生产品的权利；引用数据集时的客观描述性使用（如「数据来自 midicn-lib」）不在此限。

## 6. 第三方归属（NOTICE 摘要）

本数据集聚合了以下来源的数据（完整审计见 [LICENSE-AUDIT.md](docs/LICENSE-AUDIT.md)）：

ariamidi · TheSession.org · The Cyber Hymnal · 中国民间歌曲集成（OMR）· Essenfolkdance (EsAC) · GiantMIDI-Piano · Lakh MIDI（已过滤子集）· Norbeck Abby · music21 CoreCorpus · Mutopia Project · ABCMisc · OpenScore Lieder Corpus · MAESTRO v3 · Groove MIDI Dataset · EMOPIA v2.2 · Nottingham ABC · Wikifonia 档案（PD 子集）· OpenGameArt.org · MusicNet · **ATEPP（钢琴演奏转录）· PDMX（公有领域钢琴乐谱）**

（21 个来源；MuseData/CCARH 因许可禁止分发而永久排除。）
各来源的**实际采集地址、取得方式与校验值**见 [PROVENANCE.md](PROVENANCE.md)；
许可与核实状态见 [LICENSE-AUDIT.md](docs/LICENSE-AUDIT.md)。使用对应曲目时，请同时遵守来源数据集的署名要求。

> **Lakh MIDI 过滤说明**：该来源（`l` = CC-BY-4.0，`z` = study）在入库时已剔除含版权声明、
> 流行/影视/游戏路径，以及**经人工逐条复核确认仍在保护期内的 521 首**现代商业作品
> （圣诞流行曲、影视/流行/游戏配乐、晚卒于公有领域线的作曲家作品）。台账见
> 逐首处置记录留存于项目内部台账（不随发布包分发），并由 `tools/audit_license.py` 在每次发布前断言为 0。

## 7. 权利救济与移除流程（Takedown）

如你认为本数据集中的任何内容侵犯了你的权利（包括但不限于著作权、改编权）：

1. 通过 GitHub Issues（github.com/midicn/midi-lib/issues）提交通知，注明：涉嫌侵权的曲目 id（`catalog.json` 中可查）、你的权利依据、联系方式；
2. 我们将在收到有效通知后**及时**核实并采取必要措施（移除或隔离相关内容），并在后续版本中同步更新；
   > 我们依通知所涉内容的具体情形判断处置的紧迫性，不另设固定时限；
3. 恶意或虚假的侵权通知由通知方自行承担法律责任。

本数据集托管于 GitHub，同时受 GitHub 服务条款与 DMCA 政策约束（可通过 GitHub 官方 DMCA 流程提交移除请求）。

## 8. 管辖与适用法律

midicn 项目主要面向中文用户，数据整理工作在中国境内完成。本条款的解释优先适用**中华人民共和国法律**（不含港澳台地区法律冲突规范）。因本数据集产生的争议，双方应友好协商；协商不成的，提交数据整理方所在地有管辖权的人民法院。

**本条款不排除任何适用法律赋予你的不可排除的消费者权利。**

---

# English

## 1. Overall Structure

midicn-lib is a systematic re-curation of **21 source datasets**. We **do not re-license any MIDI
file** — every file follows the license of its original source:

1. **The `meta/` directory** and **all curation documents, audit reports, and tool scripts**:
   published by the midicn project under **CC0 1.0**. Free to use, modify and redistribute
   without attribution (though attribution is appreciated).
2. **MIDI files**: follow the license of their source dataset, annotated **per track in field `l`**
   (see `meta/catalog.json` and [LICENSE-AUDIT.md](docs/LICENSE-AUDIT.md)).
3. **Zoning**:
   - `main/` — source licenses permit redistribution (CC BY / CC BY-SA / public domain / open declarations)
   - `piano-special/` — **CC BY-NC-SA 4.0: non-commercial purposes only**, attribution + share-alike required
   - `study/` — **study and research only** (e.g. TRADITIONAL-STUDY, the filtered Lakh subset):
     no redistribution, no commercial use
   - no source with unclear or redistribution-prohibiting terms is included (see `SOURCE-CATALOG.md`)

## 2. Obligations by License Type

When using tracks from `main/` or `piano-special/`, you must comply with all obligations of the
license annotated in field `l`:

| License | Attribution | Share-alike | Non-commercial | Notes |
|---|---|---|---|---|
| CC BY 4.0 | Required | — | — | Credit authors, source, license link, indicate changes |
| CC BY-SA 4.0 | Required | Required | — | Derivatives under the same license |
| CC BY-NC-SA 4.0 | Required | Required | **No commercial use** | Non-commercial purposes only |
| CC0 / Public domain | Appreciated | — | — | Free to use |
| Open declaration | Source appreciated | — | Varies | See per-source notes in LICENSE-AUDIT.md |

**Minimum attribution**: prominently display "Source: midicn-lib (github.com/midicn/midi-lib)"
plus the corresponding source dataset name. For websites, a consolidated credit on the page or
an "About" page is acceptable.

### 2.1 TRADITIONAL-STUDY (traditional folk · study only)

Applies to tracks with `l = TRADITIONAL-STUDY` (in this release: 10,473 Chinese folk songs):

- **The melodies** are traditional — anonymous, transmitted over generations, and generally in the
  public domain as musical works
- **But the source edition is protected**: these files were optically recognised from the notated /
  edited edition published in the *Anthology of Chinese Folk Songs*; that editorial and compilation
  work is protected
- **Permitted**: use and sharing for research, teaching and study
- **Prohibited**: any commercial use; public performance or broadcast; sound recordings; redistribution
  with attribution removed or altered
- **Required**: prominent attribution to "Anthology of Chinese Folk Songs (OMR dataset,
  github.com/m-july/Anthology-of-Chinese-Folk-Songs)"
- **Commercial use needs separate permission** from the underlying rights holders; this project grants none

### 2.2 TheSession · Additional Term (prohibition on LLM use)

The `thesession` source (23,250 tracks) carries an **additional "Prohibition on LLM Use"** on top of
CC BY-SA 4.0:

- **Prohibited**: using, adapting, modifying or processing the material with large language models —
  including but not limited to **training LLMs**, processing it with **LLM tools**, or incorporating it
  into any **LLM-related application or system**
- **Sole exception**: use necessary to provide **accessibility solutions** for disabled individuals
- Basis: the *Prohibition on LLM Use* section of the upstream data repository's `LICENSE.md`
  (recorded in this library's `PROVENANCE.md`)
- This term applies **in parallel** with the attribution and share-alike obligations of CC BY-SA 4.0
  and is not removed by our format conversion

> In short: the `thesession` portion may be used freely for ordinary purposes (including commercially,
> with attribution and share-alike), **but must not be fed into LLM training or processing pipelines.**

### 2.3 Embedded Lyrics · Separate Rights Layer (study/research only)

Some track files contain **MIDI lyric meta-events (embedded lyric text)**. This release has
**2,778 tracks** carrying embedded lyrics, by source: openscore 1,436 (CC0) · m21 563 (PD) ·
wikifonia 365 (PD) · mutopia 250 (PD) · lakh 136 (C3) · cyberhymnal 28 (PD).

**Lyrics are a separate rights object from the track, and the following applies specifically to them:**

- **No commercial grant inherited from the track's zone**: even where a track is `main`
  (commercial use permitted), its **embedded lyric text** remains **study / teaching / learning
  use only**. The lyric text may not be used commercially, published, recorded or redistributed
  on its own.
- **No rights claimed**: this library **claims no copyright** in any lyric text and grants no
  rights in it. Any lyric rights belong to their respective authors, lyricists or publishers.
- **Why a separate layer is required**: a license granted by an upstream dataset over the
  **MIDI file itself** (CC BY 4.0 / PD / CC0) **does not automatically extend** to lyric text
  that a third party may have written into that file — **a licensor can only license what it owns**;
  "the container is licensed" is not "third-party content inside it is licensed". This library
  therefore **makes no claim that lyrics are licensed along with the file**, and conservatively
  restricts lyrics to study/research use.
- **Measured risk tiers**: of the 2,778 tracks, about **2,642** come from PD-only sources
  (OpenScore Lieder lyricists such as Goethe, Heine; Mutopia accepts PD works only; hymnals),
  whose lyrics are themselves public domain and therefore carry no real risk. **The risk is
  concentrated in 136 lakh tracks** (whose lyrics are mostly 20th-century commercial songs);
  those tracks are themselves graded **C3 (study)**, and the in-copyright ones among them have
  been removed.
- **Lyrics library**: the Chinese folk-song lyrics (`midi_db/lyrics/`, 10,035 entries) are
  **not included in any release package** and are shown on-site for search only.
- **On request**: if a lyric rights holder objects, the corresponding file or its lyric events
  will be removed under the process in Section 7.

> Practical effect: using this dataset as **score / performance data** is unaffected; if you
> **extract and reuse lyric text**, restrict it to study/research and clear the rights yourself.

## 3. Redistribution Rules

Redistribution of all or part of this dataset is permitted **provided that**:

1. License information is preserved or not obscured (per-track `l` field, this file, `LICENSE-AUDIT.md`);
2. All obligations of each track's license (table above) are complied with;
3. You do not imply in any way that the content is your original work.

**Prohibited**:

- Redistributing with license annotations removed, hidden or altered;
- Using `piano-special/` (CC BY-NC-SA) content for any commercial purpose;
- Claiming exclusive rights over the original works or this curation.

## 4. DISCLAIMER

**THE DATASET IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED.**

To the maximum extent permitted by applicable law:

1. **No accuracy warranty**: MIDI files come from existing transcriptions in the source datasets.
   We performed file-integrity, structural-compliance and statistical music-content verification
   (see DATA-QUALITY-STATEMENT.md), but **did not compare notes against original scores**.
   Individual tracks may contain transcription errors inherited from the source datasets.
2. **No fitness warranty**: no guarantee that the data is fit for any particular purpose
   (including commercial distribution, machine-learning training, or public performance).
3. **No complete rights-chain warranty**: we verified each source dataset's own license statement,
   but **cannot fully verify upstream transcribers' authorization chains**. If any rights holder
   believes a track infringes their rights, please follow the takedown process in §7.
4. **Limitation of liability**: to the maximum extent permitted by law, the midicn project and its
   contributors shall not be liable for any direct, indirect, incidental, special or consequential
   damages arising from use of, or inability to use, this dataset.
5. **You assume full responsibility for your use**. Perform your own due diligence before commercial use.

## 5. Trademarks

"midicn", "midicn.com" and "midicn-lib" are the names and marks of the midicn project. This license
does **not** grant the right to use these names to promote derivative products; descriptive fair use
when citing the dataset (e.g. "data from midicn-lib") is fine.

## 6. Third-party Notices (NOTICE summary)

This dataset aggregates data from 21 sources: ariamidi · TheSession.org · The Cyber Hymnal ·
Anthology of Chinese Folk Songs (OMR) · Essenfolkdance (EsAC) · GiantMIDI-Piano · Lakh MIDI
(filtered subset) · Norbeck Abby · music21 CoreCorpus · Mutopia Project · ABCMisc ·
OpenScore Lieder Corpus · MAESTRO v3 · Groove MIDI Dataset · EMOPIA v2.2 · Nottingham ABC ·
Wikifonia archive (PD subset) · OpenGameArt.org · MusicNet · **ATEPP (piano performance
transcriptions) · PDMX (public-domain piano scores)**.

(MuseData/CCARH is permanently excluded: its license prohibits any redistribution.)

> **Lakh MIDI filtering note**: this source (`l` = CC-BY-4.0, `z` = study) was filtered at ingest
> for copyright notices, pop/film/game paths, and additionally **521 commercially released works
> still in copyright**, each confirmed by manual review (Christmas pop, film/pop/game scores,
> and composers who died after the public-domain cut-off). The ledger is
> `internal/lakh-review-2026-09-23.md`, and `tools/audit_license.py` asserts this count is zero
> before every release.

(MuseData/CCARH is permanently excluded: its licence forbids redistribution.)
Each source's **actual acquisition address, method and checksums**: [PROVENANCE.md](PROVENANCE.md).
Per-source licenses and verification status: [LICENSE-AUDIT.md](docs/LICENSE-AUDIT.md).
When using tracks from a source, also comply with that source dataset's attribution requirements.

## 7. Takedown Process

If you believe any content in this dataset infringes your rights (including copyright and adaptation
rights):

1. File a notice via GitHub Issues (github.com/midicn/midi-lib/issues) including: the track id(s)
   (searchable in `catalog.json`), the basis of your claim, and your contact information;
2. We will **promptly** verify and take the necessary measures (remove or quarantine the content) after receiving a valid notice
(self-consistent with the commitment published on the website);
3. Knowingly false infringement notices are the sole responsibility of the notifier.

This dataset is hosted on GitHub and is also subject to GitHub's Terms of Service and DMCA policy
(you may submit removal requests through GitHub's official DMCA process).

## 8. Governing Law

The midicn project is primarily oriented toward Chinese users and the curation work was completed
in mainland China. These terms are governed by the laws of the **People's Republic of China**
(excluding conflict-of-law provisions for Hong Kong, Macao and Taiwan). Disputes shall first be
resolved through friendly negotiation; failing that, by the competent people's court at the
curation party's domicile.

**These terms do not exclude any non-excludable consumer rights granted by applicable law.**
