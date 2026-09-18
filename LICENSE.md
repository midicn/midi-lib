# LICENSE · 许可与法律条款 / License & Legal Terms

> 本文件说明 midicn-lib 的整体许可结构、各来源的许可归属、二次分发规则、免责声明与权利救济。
> This file describes the overall licensing structure of midicn-lib, per-source license attribution,
> redistribution rules, disclaimers, and remedies.

> **中文** | [English](#english)

---

# 中文部分

## 1. 总体结构

midicn-lib 是 **17 个来源数据集**的系统性二次整理。我们**不重新授权任何 MIDI 文件**——每个文件遵循其原始来源的许可：

1. **`meta/` 目录**（目录、索引、校验文件）与**全部整理文档、审计报告、工具脚本**：由 midicn 项目发布，采用 **CC0 1.0（公有领域贡献）**。你可以自由使用、修改、再分发，无需署名（但欢迎注明来源）。
2. **MIDI 文件**：遵循各来源数据集的许可，**逐曲标注于 `l` 字段**（详见 `meta/catalog.json` 与 [LICENSE-AUDIT.md](docs/LICENSE-AUDIT.md)）。
3. **分区规则**：
   - `main/`——来源许可允许再分发（CC BY / CC BY-SA / 公有领域 / 开放声明）
   - `piano-special/`——**CC BY-NC-SA 4.0：仅限非商业目的**，使用时须署名并以相同方式共享
   - `pending` 区与 `research` 区**未包含在本发布中**

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

ariamidi · TheSession.org · 中国民歌集成（未随本版发布）· Essenfolkdance (EsAC) · Norbeck Abby · Mutopia Project · ABCMisc · OpenScore Lieder Corpus · MAESTRO（未随本版发布）· Groove MIDI Dataset · EMOPIA（未随本版发布）· Nottingham ABC · MuseData（未随本版发布）· OpenGameArt.org · MusicNet · Wikifonia 档案（PD 子集）· music21 CoreCorpus

各来源的许可、依据链接与核实状态见 [LICENSE-AUDIT.md](docs/LICENSE-AUDIT.md)。使用对应曲目时，请同时遵守来源数据集的署名要求。

## 7. 权利救济与移除流程（Takedown）

如你认为本数据集中的任何内容侵犯了你的权利（包括但不限于著作权、改编权）：

1. 通过 GitHub Issues（github.com/midicn/midi-lib/issues）提交通知，注明：涉嫌侵权的曲目 id（`catalog.json` 中可查）、你的权利依据、联系方式；
2. 我们将在**核实后 7 个工作日内**移除或隔离相关内容，并在后续版本中更新；
3. 恶意或虚假的侵权通知由通知方自行承担法律责任。

本数据集托管于 GitHub，同时受 GitHub 服务条款与 DMCA 政策约束（可通过 GitHub 官方 DMCA 流程提交移除请求）。

## 8. 管辖与适用法律

midicn 项目主要面向中文用户，数据整理工作在中国境内完成。本条款的解释优先适用**中华人民共和国法律**（不含港澳台地区法律冲突规范）。因本数据集产生的争议，双方应友好协商；协商不成的，提交数据整理方所在地有管辖权的人民法院。

**本条款不排除任何适用法律赋予你的不可排除的消费者权利。**

---

# English

## 1. Overall Structure

midicn-lib is a systematic re-curation of **17 source datasets**. We **do not re-license any MIDI
file** — every file follows the license of its original source:

1. **The `meta/` directory** and **all curation documents, audit reports, and tool scripts**:
   published by the midicn project under **CC0 1.0**. Free to use, modify and redistribute
   without attribution (though attribution is appreciated).
2. **MIDI files**: follow the license of their source dataset, annotated **per track in field `l`**
   (see `meta/catalog.json` and [LICENSE-AUDIT.md](docs/LICENSE-AUDIT.md)).
3. **Zoning**:
   - `main/` — source licenses permit redistribution (CC BY / CC BY-SA / public domain / open declarations)
   - `piano-special/` — **CC BY-NC-SA 4.0: non-commercial purposes only**, attribution + share-alike required
   - `pending` and `research` zones are **not included** in this release

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

This dataset aggregates data from: ariamidi · TheSession.org · Chinese Folk Collection (not in this
release) · Essenfolkdance (EsAC) · Norbeck Abby · Mutopia Project · ABCMisc · OpenScore Lieder
Corpus · MAESTRO (not distributed) · Groove MIDI Dataset · EMOPIA (not distributed) ·
Nottingham ABC · MuseData (not distributed) · OpenGameArt.org · MusicNet · Wikifonia archive (PD
subset) · music21 CoreCorpus.

Per-source licenses, evidence links and verification status: [LICENSE-AUDIT.md](docs/LICENSE-AUDIT.md).
When using tracks from a source, also comply with that source dataset's attribution requirements.

## 7. Takedown Process

If you believe any content in this dataset infringes your rights (including copyright and adaptation
rights):

1. File a notice via GitHub Issues (github.com/midicn/midi-lib/issues) including: the track id(s)
   (searchable in `catalog.json`), the basis of your claim, and your contact information;
2. We will remove or quarantine the content within **7 business days** after verification;
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
