# LICENSE · 许可说明 / License

> 本文件说明 midicn-lib 的整体许可结构与各来源的许可归属。
> This file describes the overall licensing structure of midicn-lib and the license attribution of each source.

## 中文说明

### 总体结构

midicn-lib 是 **17 个来源数据集**的二次整理。我们**不重新授权任何 MIDI 文件**——每个文件遵循其原始来源的许可：

1. **`meta/` 目录**（目录、索引、校验文件）与**全部整理文档、工具脚本**：由 midicn.com 发布，采用 **CC0 1.0**（公有领域贡献）。
2. **MIDI 文件**：遵循各来源数据集的许可（见下表）。`l` 字段逐曲标注。
3. **分区规则**：
   - `main/`——许可允许再分发（CC BY / CC BY-SA / PD / 开放声明）
   - `piano-special/`——**CC BY-NC-SA 4.0：仅限非商用**，使用时需署名并同等共享
   - `pending` 与 `research` 区**未包含在本发布中**

### 使用要求

- **CC BY 系**：使用时署名（引用本数据集 + 原始来源数据集）
- **CC BY-SA 系**：署名 + 相同方式共享
- **CC BY-NC-SA（piano-special）**：署名 + 非商用 + 相同方式共享
- **PD（公有领域）**：自由使用
- 引用格式见 [DATASET-CARD.md](DATASET-CARD.md) 第七节

### 重要提醒

- 各来源数据集的许可由**该数据集发布方声明**。我们对 17 个源逐一做了许可审计（[LICENSE-AUDIT.md](LICENSE-AUDIT.md)），但**无法穿透验证上游转录者的授权链**（详见 [DATA-QUALITY-STATEMENT.md](DATA-QUALITY-STATEMENT.md) §2.3）。
- 中国民歌集成（10,473 首）因许可未确认**未包含**在本发布中。
- 商业使用前，请核对你所用曲目的 `l` 字段与对应来源的完整许可文本。

---

## English

### Overall Structure

midicn-lib is a curated re-distribution of **17 source datasets**. We **do not re-license any MIDI
file** — every file follows the license of its original source:

1. **The `meta/` directory** (catalog, indexes, checksums) and **all curation documents and tool
   scripts**: published by midicn.com under **CC0 1.0**.
2. **MIDI files**: follow the license of their source dataset (see table below), annotated per
   track in field `l`.
3. **Zoning**:
   - `main/` — redistribution permitted (CC BY / CC BY-SA / PD / open declarations)
   - `piano-special/` — **CC BY-NC-SA 4.0: non-commercial only**, attribution + share-alike required
   - `pending` and `research` zones are **not included** in this release

### Requirements

- **CC BY family**: attribute (cite this dataset + the original source dataset)
- **CC BY-SA family**: attribute + share alike
- **CC BY-NC-SA (piano-special)**: attribute + non-commercial + share alike
- **PD (public domain)**: free to use
- Citation format: [DATASET-CARD.md](DATASET-CARD.md) §7

### Important Notice

- Source-dataset licenses are **declared by their publishers**. We audited all 17 sources
  ([LICENSE-AUDIT.md](LICENSE-AUDIT.md)) but **cannot fully verify upstream transcribers'
  authorization chains** (see [DATA-QUALITY-STATEMENT.en.md](DATA-QUALITY-STATEMENT.en.md) §2.3).
- The Chinese folk collection (10,473 tracks) is **not included** pending license confirmation.
- Before commercial use, check the `l` field of your tracks and the full license text of the
  corresponding source.

## 许可对照表 / License Mapping

| 源 / Source | 内容 / Content | 曲目 / Tracks | 许可 / License | 分区 / Zone |
|---|---|---:|---|---|
| ariamidi | 古典钢琴转录 / Classical piano transcriptions | 32,522 | CC BY-NC-SA-4.0 | piano-special |
| TheSession.org | 爱尔兰传统 / Irish traditional | 23,294 | CC BY-SA-4.0 | main |
| Essenfolkdance | 世界民谣 / World folk | 10,448 | 开放声明 / Open declaration | main |
| Norbeck | 爱尔兰/瑞典传统 / Irish/Swedish | 3,473 | 开放声明 / Open declaration | main |
| Mutopia | 古典器乐 / Classical | 1,861 | 各曲不同（PD 为主）/ per-track (mostly PD) | main |
| ABCMisc | 克莱兹梅尔/巴尔干 / Klezmer/Balkan | 1,579 | 开放声明 / Open declaration | main |
| OpenScore | 艺术歌曲 / Lieder | 1,440 | CC0-1.0 | main |
| MAESTRO | 钢琴演奏 / Piano performances | 1,276 | CC BY-NC-SA-4.0 | research（不发布 / not distributed） |
| Groove MIDI | 鼓点 / Drums | 1,150 | CC BY-4.0 | main |
| EMOPIA | 流行钢琴 / Pop piano | 1,071 | CC BY-NC-SA-4.0 | research（不发布 / not distributed） |
| Nottingham | 英美民谣 / British-American folk | 1,037 | 开放声明 / Open declaration | main |
| MuseData | 古典器乐 / Classical | 924 | CCARH 限制 / restricted | research（不发布 / not distributed） |
| OpenGameArt | 游戏音乐 / Game music | 342 | CC0/CC-BY 逐曲 / per track | main |
| MusicNet | 古典室内乐 / Chamber | 330 | CC BY-4.0 | main |
| Wikifonia (PD) | 传统 lead sheets / Traditional lead sheets | 446 | PD | main |
| music21 corpus | 混合 / Mixed | 3,068 | PD | main |
| 中国民歌集成 / Chinese Folk | 中国民歌 / Chinese folk songs | 10,479 | 未确认 / pending | pending（不发布 / not distributed） |

> 「开放声明」= 来源站点声明可自由使用但无标准化许可文本 / "Open declaration" = the source site
> declares free use without a standardized license text. 详见 LICENSE-AUDIT.md / See LICENSE-AUDIT.md for details.
