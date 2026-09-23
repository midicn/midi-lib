# NOTICE · 第三方归属声明 / Third-party Notices

> 本文件列出 midicn-lib 所聚合的各来源数据集的归属信息。使用对应曲目时，请同时遵守其许可要求。
> This file lists attributions for the source datasets aggregated in midicn-lib.
> When using tracks from a source, comply with its license requirements.

## Included in this release / 本版包含（21 个来源 · 133,667 首）

| 来源 / Source | 归属 / Attribution | 许可 / License | 使用要求 / Requirements |
|---|---|---|---|
| ariamidi | ariamidi 项目（自动转录古典钢琴） | CC BY-NC-SA 4.0 | 署名 + 非商用 + 相同方式共享 |
| TheSession.org | TheSession 社区（tunes 由多位提交者贡献） | CC BY-SA 4.0 **+ 禁止用于大语言模型** | 署名 + 相同方式共享；**不得用于 LLM 训练/处理**（无障碍用途除外）；建议同时注明提交者 |
| **The Cyber Hymnal** | Richard W. Adams 等（hymntime.com/tch） | Public Domain | 自由使用；建议署名 |
| Essenfolkdance (EsAC) | EsAC 项目（Helmut Schaffrath 等采集） | 开放声明（学术用途） | 建议署名；商业使用前确认 |
| Norbeck Abby | Norbeck 个人站点（多位转录者） | 站点自声明 | 建议署名；商业使用前确认 |
| **Nottingham Music Database** | Eric Foxley 建立；Seymour Shlien 校订为 ABC | 站点自声明 | 建议署名（数据库与 ABC 校订者） |
| Mutopia Project | Mutopia 贡献者 | 逐曲 PD / CC BY-SA 等（随曲标注） | 按曲目标注执行 |
| ABCMisc | 各 ABC 整理者 | 站点自声明 | 建议署名 |
| OpenScore Lieder Corpus | OpenScore 项目 | CC0-1.0 | 自由使用 |
| Groove MIDI Dataset | Google Magenta 团队 | CC BY 4.0 | 署名（Google Magenta） |
| OpenGameArt.org | 各资源作者 | CC0 / CC BY / CC BY-SA / GPL（逐曲） | 按曲目标注执行 |
| MusicNet | University of Washington | CC BY 4.0 | 署名（MusicNet, UW） |
| Wikifonia 档案（PD 子集） | Wikifonia 社区 | PD（仅保留传统/民歌类） | 自由使用 |
| music21 CoreCorpus | MIT Music21 项目 | PD | 自由使用 |
| MAESTRO v3 | Google Magenta 团队 | CC BY-NC-SA 4.0 | 署名 + 非商用 + 相同方式共享 |
| EMOPIA v2.2 | EMOPIA 团队 | CC BY-NC-SA 4.0 | 署名 + 非商用 + 相同方式共享 |
| Lakh MIDI（已过滤子集） | Colin Raffel 等 | CC BY 4.0 | 署名；本库按其声明归入研究/学习用途。**已剔除 521 首在保护期内的现代商业作品**（圣诞流行曲、影视/流行歌等），见 `internal/lakh-review-2026-09-23.md` |
| **GiantMIDI-Piano v1.2** | Kong, Q. 等（字节跳动）；github.com/bytedance/GiantMIDI-Piano（论文 arXiv:2010.07061） | **CC BY 4.0** | 署名数据集与论文；可商用 |
| **中国民间歌曲集成（OMR 数据集）** | **《中国民间歌曲集成》各省卷；数据集由 m-july 制作并公开于 github.com/m-july/Anthology-of-Chinese-Folk-Songs（论文 arXiv:2512.14758）** | **TRADITIONAL-STUDY** | **必须署名上述数据集与底本；仅限研究/教学/学习；禁止商用与公开表演** |

## Not distributed / 未随本版发布

| 来源 / Source | 归属 / Attribution | 许可 / License | 状态 |
|---|---|---|---|
| MuseData (CCARH) | CCARH, Stanford | 限制性声明 / restricted | **永久排除**：许可原文第 (4)(5) 条禁止任何分发（含非商业教学材料）与多人使用 |

## 关于 TRADITIONAL-STUDY / About TRADITIONAL-STUDY

- 中国民歌的**旋律本身**属传统民间文学艺术，作者不可考、流传久远，作为音乐作品通常已进入公有领域。
- 但本批 MIDI 是依据**《中国民间歌曲集成》的记谱／整理稿**光学识别（OMR）而来，**该整理与汇编成果受版权保护**——
  上游数据集作者亦声明原始扫描图属受版权作品、不予公开。
- 因此本库**不授予商用权利**：该批曲目归入 C3 研究/学习，限研究、教学、学习用途，**禁止商业使用与公开表演**。
- 使用必须标注来源；如权利方提出异议，我们将**及时**下架该批数据（与 `LICENSE.md` §7 及站点许可页一致）。
- The melodies are traditional and generally public domain as musical works, but these files were recognised
  from a copyrighted notated edition. We therefore grant **no commercial rights**: research, teaching and
  study only; commercial use and public performance are prohibited. Attribution is required.

> 各曲目的具体许可以 `meta/catalog.json` 的 `l` 字段为准。
> The authoritative per-track license is field `l` in `meta/catalog.json`.

## 内嵌歌词 / Embedded lyrics

**歌词是独立于曲目的另一层权利对象**，不随曲目的档位（`z` 字段）授予商用许可。

- 本版 **2,778 首**文件内含 MIDI 歌词事件（lyric meta-event）：openscore 1,436（CC0）·
  m21 563（PD）· wikifonia 365（PD）· mutopia 250（PD）· lakh 136（C3）· cyberhymnal 28（PD）。
- 其中约 **2,642 首**来自以公有领域内容为限的来源，歌词本身即属公有领域；
  风险集中在 **lakh 的 136 首**（多为 20 世纪商业歌曲），该批曲目已定级 C3，其中在保护期内者已剔除。
- **无论曲目档位如何，内嵌歌词文本仅限研究/教学/学习用途**；不得单独提取用于商业用途、出版、
  录制或再分发。本库**不主张歌词著作权**，也不构成歌词权利人的授权表示。
- 上游对 MIDI 文件本身授予的许可**不能自动延伸**到文件内可能由第三方写入的歌词——
  许可人只能授权自己拥有的权利。故本库保守地把歌词整体限定为研究用途。
- 中国民歌歌词库（`midi_db/lyrics/`，10,035 首）**不在发布包内**，仅站内检索展示。
- If a lyric rights holder objects, the corresponding file or its lyric events will be removed
  promptly. The Chinese folk-lyrics library is **not shipped** in any package.

---

## v1.23 数据增强（2026-09-23）

本轮新增 **2 个来源**（ATEPP 7,130 首演奏版 + PDMX 2,893 首乐谱型）与 **15 个字段**；
完整字段语义、覆盖率与标注规范见 `FIELD-DICTIONARY.md`。

**新增字段**：`difficulty` 演奏难度 · `cn_zh` 作曲家中文名 · `birth`/`death` 生卒年 ·
`instrument_gm` GM 标准乐器 · `velocity_avg`/`velocity_range` 演奏力度 · `notes_per_sec` 音符密度 ·
`pitch_range` 音域 · `midi.tempo` 速度 · `midi.timesig` 拍号 · `version_type` 版本类型（score/performance）·
`performer`/`album`（演奏版）· `topic`/`topics_zh` 题材 · 歌词库（10,035 首中国民歌，独立分片）

**标注规范**：算法推断字段一律带 `*_src`（如 `key_src="inferred"`，附 `extra.key_corr` 置信度），可筛选；
未知留空不猜（拍号推断因验证准确率 26.8% 已弃用）。
