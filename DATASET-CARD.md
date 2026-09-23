---
license: mixed (per-track `license` field; see LICENSE-AUDIT.md · meta package CC0-1.0)
language: [zh, en, mul]
tags: [music, midi, symbolic-music, classical, folk, world-music, hymns, public-domain, creative-commons]
pretty_name: MIDI Lib CN (midicn-lib)
size_categories: [100K<n<1M]
task_categories: [text-to-music, audio-classification, other]
configs:
  - name: main
    description: 可商用曲目（C1）
  - name: piano-special
    description: 非商用钢琴演奏（C2）
  - name: study
    description: 学习研究专用（C3）
  - name: meta
    description: 全库统一元数据与索引（CC0-1.0）
---

# DATASET CARD · midicn-lib

> **133,667** 首曲目 · **21** 个公开来源 · **14** 个分类 · 逐首标注来源与许可档位 · 全程可溯源
>
> 本卡描述数据集的**内容、来源、字段、质量与实际使用限制**。
> 每个来源地址的取得方式与校验值见 [`PROVENANCE.md`](PROVENANCE.md)（含可执行复核脚本）。
>
> 门户：<https://lib.midicn.com> · 代码仓库：<https://github.com/midicn/midi-lib-site>

## 一、数据集概述

midicn-lib 是对 **21 个公开 MIDI / 记谱数据集**的系统性二次整理，产出**统一目录、统一字段、逐首标注许可**的开放曲库：

- **统一目录**：全部曲目规范命名为 `{source}-{序号}.mid`，按「使用方式」分为三包（见下）
- **统一字段**：20 个字段跨源语义一致（见 §四），并提供作曲家 / 时期 / 地域 / 来源四套索引
- **逐首许可**：每首曲目携带 `z`（档位：main / piano-special / study）与 `l`（许可标识）字段
- **可溯源**：每首曲目保留上游原始路径与作品级标识；来源侧证据与校验值见 `PROVENANCE.md`
- **可下架**：权利人如有异议，按 `LICENSE.md` §7 的 takedown 流程处理（7 个工作日内响应）

## 二、分包与规模

以「使用方式」分包（不是按风格分包），下载时只需取你需要的那一档：

| 分包 | 含义 | 档位 | 曲目数 | 打包文件 |
|---|---|---|---:|---|
| `main` | 许可允许商业使用 | **C1 可商用** | 79,216 | `midicn-lib-<VER>-main.zip` |
| `piano-special` | 仅限非商业用途 | **C2 非商用** | 34,869 | `midicn-lib-<VER>-piano-special.zip` |
| `study` | 仅限学习与研究 | **C3 学习研究** | 19,582 | `midicn-lib-<VER>-study.zip` |
| `meta` | 目录 / 索引 / 字段说明 / 文档 | **CC0-1.0** | — | `midicn-lib-<VER>-meta.zip` |
| **合计** | | | **133,667** | 另附 **400+ 个维度包**（zip.midicn.com） |

许可分布（按曲目计）：

| 许可标识 | 曲目数 | 主要来源 |
|---|---:|---|
| `CC-BY-NC-SA-4.0` | 34,869 | aria 32,522 · maestro 1,276 · emopia 1,071 |
| `CC-BY-SA-4.0` | 23,289 | thesession 23,250 · oga 39 |
| `CC-BY-4.0` | 21,200 | giantmidi 10,110 · lakh 9,630 · groove 1,149 · musicnet 297 · oga 14 |
| `OPEN`（站点开放声明） | 16,332 | essen 10,373 · norbeck 3,439 · abcmisc 1,487 · nottingham 1,033 |
| `PD`（公有领域） | 14,419 | cyberhymnal 10,945 · m21 3,029 · wikifonia 445 |
| `TRADITIONAL-STUDY` | 10,473 | chinafolk 10,473（C3） |
| `MUTOPIA-MIXED`（逐曲） | 1,860 | mutopia 1,860 |
| `CC0-1.0` | 1,704 | openscore 1,438 · oga 266 |
| 其他逐曲混合（CC BY 3.0 / CC BY-SA 3.0 / GPL） | 21 | oga 21 |

## 三、来源（19 个）

地址均为**我们实际取得数据的位置**；取得方式、证据文件与校验值见 [`PROVENANCE.md`](PROVENANCE.md)。

| 源 id | 来源 | 曲目数 | 档位 | 原始地址 |
|---|---|---:|---|---|
| `aria` | Aria-MIDI（Unique 子集） | 32,522 | C2 | github.com/loubbrad/aria-midi |
| `thesession` | The Session | 23,250 | C1 | github.com/adactio/TheSession-data |
| `cyberhymnal` | The Cyber Hymnal | 10,945 | C1 | hymntime.com/tch |
| `chinafolk` | 中国民间歌曲集成（OMR 数字化） | 10,473 | C3 | github.com/m-july/Anthology-of-Chinese-Folk-Songs |
| `essen` | ESAC 欧洲民歌档案 | 10,373 | C1 | esac-data.org |
| `giantmidi` | GiantMIDI-Piano | 10,110 | C1 | github.com/bytedance/GiantMIDI-Piano |
| `lakh` | Lakh MIDI Dataset（已过滤） | 9,630 | C3 | colinraffel.com/projects/lmd/ |
| `norbeck` | Norbeck ABC 曲集 | 3,439 | C1 | norbeck.nu/abc/ |
| `m21` | music21 CoreCorpus | 3,029 | C1 | github.com/cuthbertLab/music21 |
| `mutopia` | Mutopia Project | 1,860 | C1 | mutopiaproject.org |
| `abcmisc` | ABC Misc（John Chambers 曲集） | 1,487 | C1 | trillian.mit.edu/~jc/music/abc/ |
| `openscore` | OpenScore Lieder | 1,438 | C1 | github.com/OpenScore/Lieder |
| `maestro` | MAESTRO v3 | 1,276 | C2 | magenta.tensorflow.org/datasets/maestro |
| `groove` | Groove MIDI Dataset | 1,149 | C1 | magenta.tensorflow.org/datasets/groove |
| `emopia` | EMOPIA v2.2 | 1,071 | C2 | zenodo.org/records/5257995 |
| `nottingham` | Nottingham Music Database（校订版） | 1,033 | C1 | ifdo.ca/~seymour/nottingham/ |
| `wikifonia` | Wikifonia（PD 子集） | 445 | C1 | synthzone.com/files/Wikifonia/Wikifonia.zip |
| `oga` | OpenGameArt | 340 | C1 | opengameart.org |
| `musicnet` | MusicNet | 297 | C1 | zenodo.org/records/5120004 |
| **合计** | | **133,667** | | |

> 考察但**未收录**的来源（许可不允许再分发等）及其原因，见 `SOURCE-CATALOG.md`。

## 四、字段（`meta/catalog.json`，20 字段）

| 字段 | 含义 | 覆盖 |
|---|---|---:|
| `id` | 唯一标识（`{source}-{6 位序号}`） | 100% |
| `t` | 标题（无标题者由作曲家 + 编号合成，保证可分辨 100%） | 90.0% |
| `c` / `cn` | 作曲家 slug / 显示名 | 100% |
| `g` | 风格（genre） | 95.4% |
| `i` | 乐器 | 95.4% |
| `p` | 时期 | 88.4% |
| `form` | 曲式 | 46.8% |
| `opus` / `no` | 作品号 / 编号（依各作曲家编号体系） | 30.2% / 29.7% |
| `yr` | 年代（作品首次出版年份） | 16.0% |
| `r` | 地域（国家 / 中国省级 / 地区） | 72.1% |
| `du` / `nn` | 时长（秒）/ 音符数 | **100%** |
| `z` | 档位（`main` / `piano-special` / `study`） | 100% |
| `l` | 许可标识 | 100% |
| `v` | 质量标记 | 100% |
| `f` | 相对文件路径 | 100% |
| `diff` | 难度（钢琴类） | 部分 |

字段完整度按「空字段优于模糊占位」原则统计——**未知一律留空，不做猜测性填充**。
四套索引：`index-by-composer.json` · `index-by-period.json` · `index-by-region.json` · `index-by-source.json`。

## 五、许可与使用

- 逐首许可记录在 `l` 字段；档位汇总见 §二；审计依据见 `LICENSE-AUDIT.md`
- **`main`（C1）**：允许商业使用，须按各来源要求署名
- **`piano-special`（C2）**：仅限非商业用途（CC BY-NC-SA 4.0），商用需另行获得授权
- **`study`（C3）**：仅限学习与研究，不得再分发、不得商用
  - `chinafolk` 的中国民歌：旋律为传统民间音乐，但本批 MIDI 来自《中国民间歌曲集成》记谱稿的光学识别，
    整理与汇编成果受版权保护 → 归 C3，使用须显著标注数据集与底本
  - `lakh`：数据集本身 CC BY 4.0，但内容层已剔除含版权声明与流行/影视路径的曲目，**保守归 C3**
- ⚠️ **`thesession` 的特别条款**：其数据仓 `LICENSE.md` 在 CC BY-SA 4.0 授权基础上
  **附加「禁止用于大语言模型」条款**——不得用大模型使用、改编、修改或处理该素材
  （训练大模型、借助 LLM 工具处理、并入 LLM 相关应用均属禁止），
  仅「为残障人士提供无障碍方案」有豁免。**使用 `thesession` 部分时请遵守此条款。**
- `meta` 包（目录 / 索引 / 字段说明 / 文档）由本库制作，以 **CC0-1.0** 释出，可自由使用
- 本库**不含**受版权保护的流行歌 / 影视 / 游戏音乐转录

## 六、局限与已知问题

- 元数据源自各上游数据集：作曲家拼写存在变体（归并表见 `meta` 包）；编号体系依各作曲家而异（BWV/K./D./S./Hob. 等）
- 部分 ABC → MIDI 为机械转换，**力度与速度不代表原曲演绎意图**
- `yr`（年代）与 `ctry`（国家）覆盖偏低：上游多数无此字段，按「宁缺勿错」留空
- 少数来源以「本地快照」方式留证（上游未公布校验值），见 `PROVENANCE.md` 的校验值分级说明

## 七、引用

见 `CITATION.bib`。使用 `piano-special` 包须同时引用 Aria-MIDI 原文：

```bibtex
@inproceedings{bradshawaria,
  title={Aria-MIDI: A Dataset of Piano MIDI Files for Symbolic Music Modeling},
  author={Bradshaw, Louis and Colton, Simon},
  booktitle={International Conference on Learning Representations (ICLR)},
  year={2025}
}
```

---

## English (summary)

midicn-lib is a curated aggregation of **21 public MIDI / notation datasets** — **133,667 tracks**,
normalised into one catalogue with 20 consistent fields and **per-track** licence tagging.

Splits are by **usage tier**, not by genre: `main` (79,216 · commercial use allowed),
`piano-special` (34,869 · non-commercial only, CC BY-NC-SA 4.0),
`study` (19,582 · study/research only) and `meta` (catalogue, indexes, docs · CC0-1.0).
Nineteen additional per-source packages are published alongside.

Every track keeps its upstream path and licence tag; each source's **actual acquisition address**,
method and checksum are recorded in [`PROVENANCE.md`](PROVENANCE.md).
Note the special term on **The Session** data: its licence adds a **prohibition on LLM use**
(no training, processing or incorporating the material via large language models, with an
accessibility-only exception) on top of CC BY-SA 4.0.

---

## v1.23 数据增强（2026-09-23）

本轮新增 **2 个来源**（ATEPP 7,131 首演奏版 + PDMX 2,895 首乐谱型）与 **15 个字段**；
完整字段语义、覆盖率与标注规范见 `FIELD-DICTIONARY.md`。

**新增字段**：`difficulty` 演奏难度 · `cn_zh` 作曲家中文名 · `birth`/`death` 生卒年 ·
`instrument_gm` GM 标准乐器 · `velocity_avg`/`velocity_range` 演奏力度 · `notes_per_sec` 音符密度 ·
`pitch_range` 音域 · `midi.tempo` 速度 · `midi.timesig` 拍号 · `version_type` 版本类型（score/performance）·
`performer`/`album`（演奏版）· `topic`/`topics_zh` 题材 · 歌词库（10,035 首中国民歌，独立分片）

**标注规范**：算法推断字段一律带 `*_src`（如 `key_src="inferred"`，附 `extra.key_corr` 置信度），可筛选；
未知留空不猜（拍号推断因验证准确率 26.8% 已弃用）。
