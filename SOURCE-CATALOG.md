# SOURCE CATALOG · 源清单与许可对照全表

> **中文** | [English](#english)
>
> 本文档完整披露 midicn-lib 的**源考察范围**：我们考察了 **36 个公开 MIDI 数据源**，
> 收录 **21 个**（133,667 首），并说明每个未收录源的**具体原因**与**自行获取指引**。
>
> 目的：让使用者清楚知道——**我们做了什么、没做什么、以及你可以自己去做什么**。

## 一、总览

| 项 | 数量 |
|---|---|
| 考察源总数 | **36** |
| 已收录源 | **21**（133,667 首） |
| 未收录源 | 17（含许可不符、待抓取、受限访问三类） |
| **准入标准** | 许可必须**允许二次分发**（不允许的一律不收） |
| 收录内容分级 | C1 可商用 · C2 不可商用 · C3 仅供研究/学习 |

## 二、已收录源（21 个 · 133,667 首）

| # | 源 | 曲目数 | 内容 | 许可 | 级别 | 分区 | 来源地址（实际采集处） |
|---|---|---:|---|---|---|---|---|
| 1 | **ariamidi** | 32,522 | 古典钢琴转录 | CC BY-NC-SA 4.0 | C2 | `piano-special` | github.com/loubbrad/aria-midi |
| 2 | **TheSession.org** | 23,250 | 爱尔兰传统舞曲 | CC BY-SA 4.0 | C1 | `main` | github.com/adactio/TheSession-data |
| 3 | **Cyber Hymnal** | 10,945 | 赞美诗（公有领域） | PD | C1 | `main` | hymntime.com/tch |
| 4 | **中国民歌集成** | 10,473 | 中国各省民歌 | TRADITIONAL-STUDY | C3 研究/学习 | `study` | github.com/m-july/Anthology-of-Chinese-Folk-Songs |
| 5 | **Essen (EsAC)** | 10,373 | 世界民谣（欧洲/中国为主） | 站点开放声明 | C1 | `main` | esac-data.org |
| 6 | **GiantMIDI-Piano** | 10,110 | 古典钢琴转录（大规模） | CC BY 4.0 | C1 | `main` | github.com/bytedance/GiantMIDI-Piano |
| 7 | **Lakh MIDI（过滤后）** | 9,630 | 古典与传统（已剔除流行/版权内容） | CC-BY-4.0 | **C3** | `study` | colinraffel.com/projects/lmd/ |
| 8 | **Norbeck ABC** | 3,439 | 爱尔兰/瑞典传统 | 站点开放声明 | C1 | `main` | norbeck.nu/abc/ |
| 9 | **music21 CoreCorpus** | 3,029 | 古典/民谣混合 | PD | C1 | `main` | github.com/cuthbertLab/music21 |
| 10 | **Mutopia Project** | 1,860 | 古典器乐（PD 乐谱） | 逐曲 PD/CC | C1 | `main` | mutopiaproject.org |
| 11 | **ABCMisc 集合** | 1,487 | 克莱兹梅尔/巴尔干/民谣 | 站点开放声明 | C1 | `main` | trillian.mit.edu/~jc/music/abc/ |
| 12 | **OpenScore Lieder** | 1,438 | 艺术歌曲（含女性作曲家） | CC0-1.0 | C1 | `main` | github.com/OpenScore/Lieder |
| 13 | **MAESTRO v3** | 1,276 | 钢琴演奏对齐 | CC BY-NC-SA 4.0 | C2 | `piano-special` | magenta.tensorflow.org/datasets/maestro |
| 14 | **Groove MIDI** | 1,149 | 专业鼓手节奏型 | CC BY 4.0 | C1 | `main` | magenta.tensorflow.org/datasets/groove |
| 15 | **EMOPIA v2.2** | 1,071 | 流行钢琴+情绪标注 | CC BY-NC-SA 4.0 | C2 | `piano-special` | zenodo.org/records/5257995 |
| 16 | **Nottingham ABC** | 1,033 | 英美民谣 | 站点开放声明 | C1 | `main` | ifdo.ca/~seymour/nottingham/ |
| 17 | **Wikifonia（PD 子集）** | 445 | 传统/民歌 lead sheets | PD | C1 | `main` | synthzone.com/files/Wikifonia/Wikifonia.zip |
| 18 | **OpenGameArt** | 340 | 游戏原创音乐 | CC0 / CC BY 逐曲 | C1 | `main` | opengameart.org |
| 19 | **MusicNet** | 297 | 古典室内乐 | CC BY 4.0 | C1 | `main` | zenodo.org/records/5120004 |
|  | **合计** | **133,667** | | | | | |

> 上表「来源地址」为**我们实际取得数据的位置**（各来源接入脚本 `tools/ingest_*.py` 与
> 站点台账 `PROVENANCE.md` 可复核；采集过程细节内部存档），不是泛泛的站点首页。

### 关于「中国民歌集成」（v1.4 起已发布 · C3 研究/学习）

- **规模**：**10,473 首**（已去除 6 组内容完全相同的重复；含中文标题，是本库最具中文特色的部分）
- **来源**：GitHub 上公开的《中国民间歌曲集成》数字化项目（14 卷，MIDI + MusicXML）
  —— `github.com/m-july/Anthology-of-Chinese-Folk-Songs`（论文 arXiv:2512.14758 的数据集）
- **许可判断**：
  - 民歌**旋律本身**属传统民间文学艺术，作者不可考、流传久远，作为音乐作品通常已进入公有领域
  - 但本批 MIDI 是依据《中国民间歌曲集成》的**记谱／整理稿**光学识别（OMR）而来，
    该**整理与汇编成果受版权保护**（上游亦声明原始扫描图属受版权作品、不予公开）
  - 因此定为 **`TRADITIONAL-STUDY`**：归 **C3 研究/学习**，限研究、教学、学习用途，
    **禁止商业使用与公开表演**；使用必须显著标注上述数据集与底本
- **我们的处置**：v1.4 起随 `study.zip` 发布；如权利方提出异议，我们将及时下架该批数据
- **商用**：本库不提供商用授权，需自行向底本权利人取得许可

## 三、未收录源（32 个 · 及原因）

### 3.1 因许可不符合准入标准（不允许二次分发）❌

| 源 | 规模 | 许可情况 | 结论 |
|---|---:|---|---|
| **Kunst der Fuge** | 19,300 | 站点声明「for personal use」 | ❌ 不允许再分发 → **不收** |
| **IMSLP「Music files」部分** | 数千（部分） | 部分附件标「no redistribution」 | ❌ 逐曲筛选后仅收允许的（当前未执行） |
| **NES Music Database** | 5,278 | 研究用途，再分发条款不明 | ❌ 保守不收 |
| **PianoCoRe** | 250,046 演奏 | CC BY-NC-SA 4.0，但附加条款「strictly for non-commercial research and educational purposes」（严于 NC） | ❌ 研究限定超出本库公开服务性质 → **不收** |
| **POP909** | 909 | 仓库 MIT 仅覆盖代码；内容为版权流行歌之钢琴改编，声明「non-commercial research/education」 | ❌ 改编 + 研究限定（双重问题）→ **不收** |
| **Piano-e-Competition** | 1,573 | 官网「免费下载」；第三方镜像仓自述「未找到任何许可信息」 | ❌ 免费下载≠可再分发 → **不收** |
| **VGMdb / vgmusic.com（游戏音乐）** | 28,419 | 以 fan 编配为主（对版权游戏原曲的改编，改编者无权授权原曲） | ❌ 版权风险 → **不收** |
| **CCMusic 流行库（M-W/BDoPM）** | 上百首 | 官方声明「因涉及版权协议，只对签订协议的大学授权研究使用」 | ❌ 研究授权限定 → **不收** |
| **Anthology of Chinese Folk Songs** | 5,000+（8 卷 OMR） | 与本站 chinafolk 同源（《中国民间歌曲集成》的另一 OMR）；扫描图自述版权受限 | ❌ 重复收录 + 版权链不清 → **不收** |
| **Weimar Jazz Database (WJazzD)** | 456 | 学术文献明确「copyright restrictions prevent access to note and contextual annotations」 | ❌ 版权受限 → **不收**（2026-09-22 查证） |

### 3.2 许可未明确 → **我们不下载**（附链接，你可自取）⭐

> **我们的原则**：许可文本未明确允许再分发的源，**即使数据质量很高、规模很大，我们也不下载收录**。
> 原因：我们无法确认二次分发的合法性——这是我们的合规底线。
>
> **但这不阻碍你**：以下源全部**公开可访问**，你可以自行前往获取并自行判断授权。

| 源 | 规模 | 我们考察到的许可状态 | 未收录原因 | 官方地址（你可自取） |
|---|---:|---|---|---|
| **KernScores (CCARH)** | 108,703 | 站点声明「for research and teaching」；许可专页 404/503；首页有「copyright restricted materials」登录区 | **许可未明确说明是否允许再分发**，且存在部分版权受限内容 | kern.ccarh.org |
| **Josquin Research Project** | ~1,000 | 数据可直接下载（MIDI 接口公开），但站点**无任何许可声明** | 许可文本缺失，无法确认再分发授权 | josquin.stanford.edu |
| **MuseData (CCARH)** | 924 | CCARH 站点无许可声明；原 Stanford 页面已 404 | 同上 | musedata.org / ccarh.org |
| **Digital Tradition (Mudcat)** | 数万 | 站点条款未澄清 | 同上 | mudcat.org |
| **MIDIWorld** | 数千 | 站方声称 public domain，但**无正式许可文本**可核实 | 声明不足以构成许可依据 | midiworld.com |
| **sonatica.fm** | 11,000 | 站点许可条款不明确 | 同上 | sonatica.fm |
| **piano-midi.de** | 332 | 站点许可不明确 | 同上 | piano-midi.de |
| **MetaMIDI** | 612,088 | PDMX 论文（NeurIPS 2024）明确点名「无明确许可信息，版权不安全」 | 许可未明确 | github.com/jeffreyjohnens/MetaMIDIDataset |
| **MMD（Multi-Modal MIDI）** | 1,524,557 | 同上（论文点名其许可证不清晰） | 许可未明确 | — |
| **SymphonyNet** | 46,359 | 同上（论文点名其许可证不清晰） | 许可未明确 | — |
| **Hymnal.net** | 3,358 | 站点未提供明确的内容再分发许可声明 | 许可文本缺失 | hymnal.net |
| **Sourdough MIDI Dataset** | ~5,000,000 | HuggingFace 公开，许可状态不明 | 同上 | huggingface.co/datasets/BreadAi/Sourdough-midi-dataset |
| **Various 大汇编（reddit 等）** | 800,000+ | 无许可文本可核实 | 同上 | — |

**自取提示**：这些源的数据都是公开可访问的（多数提供直接下载或批量抓取界面）。如果你需要，
建议：① 前往上述地址获取 ② 阅读其使用条款 ③ 若计划再分发，取得书面许可更稳妥。

### 3.3 其他待核实源（含版权内容风险）

| 源 | 规模 | 情况 | 官方地址 |
|---|---:|---|---|
| **Lakh MIDI Dataset** | 178,561 | ✅ 数据集许可 **CC-BY 4.0**（允许再分发）——已收录，但须过滤：22.3% 曲目自带版权声明，路径显示主体为流行音乐 | colinraffel.com/projects/lmd/ |
| **Internet Archive MIDI 集合** | 数万（需筛） | 逐集合许可不同（混有版权内容） | archive.org |
| **CIPI（中国钢琴作品）** | — | 全网检索**未证实存在**该数据集（2026-09-22 查证） | — |

### 3.4 许可清晰但尚未抓取（欢迎自取，或等我们后续批次）

| 源 | 规模 | 许可 | 官方地址 | 备注 |
|---|---:|---|---|---|
| **CPDL ChoralWiki** | ~25,000 | PD / CPDL License（类 CC BY-NC-SA） | cpdl.org | 逐曲抓取，站点限速约 1,000/天 |
| **Gregobase**（格里高利圣咏） | ~6,000 | CC BY-SA | gregobase.selab.ne.jp | 官网导出 |
| **Josquin Research Project** | ~1,000 | 开放 | josquin.stanford.edu | MusicXML 转换 |
| **Hymnal Tune Dataset** | 1,756 | PD/开放 | hymnary.org | 直下 |
| **Hymnary.org 赞美诗** | 数千 | PD 为主 | hymnary.org | 抓取 |
| **abcnotation.com 集合** | 2 万+ | 逐集合（本库 ABC Misc 1,487 首**并非**取自本站，而来自 John Chambers 曲集 `trillian.mit.edu/~jc/music/abc/`） | abcnotation.com | 逐集合接入（待办） |
| ~~Weimar Jazz Database~~ | ~2,000 | ~~学术（需申请）~~ → **已于 2026-09-22 查证：版权受限，不收（见 3.1）** | jazzomat.hfm-weimar.de | 不再列入待抓取 |
| **OpenScore String Quartets 等** | 进行中 | CC0 | github.com/OpenScore | 项目进行中 |
| **figshare 中国经典 MIDI** | 13 | CC BY 4.0 | figshare.com/articles/5436022 | 我们下载受阻（网络），**欢迎自取** |

| **PDMX** | 254,077 乐谱（MusicXML + 转换 MIDI） | **CC-0 / Public Domain**（论文明确「fully commercially viable」；须用 `no_license_conflict` 子集，排除 12.29% 许可冲突文件） | zenodo.org / github.com/pnlong/PDMX | 2026-09-22 查证通过 ✅ |
| **ATEPP** | 11,674 演奏（1,000h） | 免责声明无使用限制；许可标识 CC BY 4.0（据 TISMIR 论文对照表） | github.com/tangjjbetsy/ATEPP | 2026-09-22 查证通过 ✅ 每作品取代表版 |

## 四、你可以自己去获取的内容（自取指引）

以下源**许可清晰、允许自由获取**，你可以直接前往下载——我们的收录不构成排他性：

| 源 | 地址 | 适合谁 |
|---|---|---|
| CPDL 合唱作品（2.5 万） | cpdl.org | 合唱团、教堂音乐、声乐研究者 |
| KernScores（10.8 万） | kern.ccarh.org | 音乐学研究者（需核实条款） |
| Lakh MIDI（17.4 万） | colinraffel.com/projects/lmd/ | 机器学习研究者（非商用） |
| IMSLP 乐谱与 MIDI | imslp.org | 古典音乐学习者（注意逐曲许可） |
| Gregobase 圣咏 | gregobase.selab.ne.jp | 格里高利圣咏研究 |
| Internet Archive MIDI | archive.org | 历史录音与老 MIDI 收藏 |
| TheSession 原始数据 | thesession.org/data | 爱尔兰音乐爱好者 |

**自取时的合规提醒**：
1. 每个源的使用条款以**该站原文**为准（我们只负责我们已收录部分的合规）
2. 若许可要求署名/相同方式共享，请遵守
3. 若标注「personal use / no redistribution」，请勿再分发
4. 商业使用前请自行完成尽职调查

## 五、我们的收录原则（透明公开）

1. **准入硬门槛**：只收许可明确允许**二次分发**的内容
2. **分级标注**：C1 可商用 / C2 不可商用 / C3 仅供研究学习（逐曲写入 `z` 字段）
3. **宁缺毋滥**：许可不明或禁止再分发的源，**无论规模多大一律不收**（如 Kunst der Fuge 1.93 万、Lakh 17.4 万暂缓）
4. **可复核**：全部判定依据存档于 `docs/LICENSE-AUDIT.md` 与 `docs/EXPANSION-PLAN-BATCH34.md`
5. **可下架**：权利人如有异议，按 `LICENSE.md` §7 的 takedown 流程处理（及时核实并处理）

---

# English

## Overview

We surveyed **36 public MIDI sources** and included **21** (133,667 tracks).
This document discloses the full survey scope: what we included, what we excluded **and why**,
plus direct links so you can obtain the rest yourself.

**Admission rule**: only content whose license **permits redistribution** is included.
Sources marked "personal use only" or "no redistribution" are excluded regardless of size.

## Included sources (21 · 133,667 tracks)

See the Chinese table above — columns: source, track count, content, license, tier (C1 commercial /
C2 non-commercial / C3 research-and-study only), zone, official URL.

Notable: the Chinese Folk Collection (10,473 tracks) is published from v1.4 under a
**research/study-only (C3)** designation, because the compilation's editorial rights are protected.

## Excluded sources (32)

- **License does not permit redistribution** (excluded): Kunst der Fuge (19,300, "personal use"),
  parts of IMSLP, NES Music Database (5,278)
- **License under review** (C3 if confirmed): KernScores (108,703), Lakh MIDI (174,533),
  Mudcat, MIDIWorld, sonatica.fm, piano-midi.de, Internet Archive MIDI collections
- **License clear, not yet harvested** (self-service welcome): CPDL (25,000), Gregobase (6,000),
  Josquin Research Project, Hymnal Tune Dataset, Hymnary, abcnotation collections,
  Weimar Jazz Database, OpenScore String Quartets, figshare Chinese Classics (13)

## Obtain it yourself

CPDL · KernScores · Lakh MIDI · IMSLP · Gregobase · Internet Archive · TheSession —
direct links are in the Chinese section (§4). Please follow each site's own terms;
we are only responsible for the compliance of what *we* redistribute.


### Newly assessed sources (2026-09-22 · 法律查证批次)

**収录（verified redistributable）：**
- **PDMX** — 254,077 MusicXML scores (+ converted MIDI) — **CC-0 / Public Domain**, fully commercially viable
  (must use the `no_license_conflict` subset). Source: zenodo.org / github.com/pnlong/PDMX
- **ATEPP** — 11,674 expressive piano performances — disclaimer without usage restrictions;
  license indicated as CC BY 4.0 (per TISMIR cross-reference table). Source: github.com/tangjjbetsy/ATEPP

**Not included（原因）：**
- PianoCoRe (250k) — "strictly non-commercial research/educational" clause → excluded
- POP909 (909) — repo MIT covers code only; content is copyrighted pop-song arrangements → excluded
- Piano-e-Competition (1,573) — no license information found → excluded
- VGMdb / vgmusic (28,419 game music) — fan arrangements of copyrighted game music → excluded
- MetaMIDI (612k) / MMD (1.5M) / SymphonyNet (46k) — no clear license (per PDMX paper) → excluded
- CCMusic pop DB — university-agreement research access only → excluded
- Anthology of Chinese Folk Songs (5k+) — duplicate of our chinafolk source; scan rights unclear → excluded
- Weimar Jazz Database (WJazzD) — copyright restrictions on note data → excluded
- Hymnal.net (3,358) / Sourdough (~5M) / large reddit compilations — no explicit redistribution license → excluded
- CIPI — dataset existence not verified → excluded

## Our principles

1. **Redistribution required** — no redistribution permission, no inclusion
2. **Tiered labeling** — C1 / C2 / C3 written per-track into the `z` field
3. **Better safe than sorry** — unclear or restrictive licenses are excluded even at large scale
4. **Auditable** — every decision archived in `LICENSE-AUDIT.md` and `EXPANSION-PLAN-BATCH34.md`
5. **Takedown-ready** — rights-holder notices acted upon promptly (see LICENSE.md §7)

### 关于 GiantMIDI-Piano（v1.5 起发布 · C1 可商用）

- **规模**：**10,110 首**（原始 10,855 首，剔除 742 个内容完全相同的转录）
- **来源**：`github.com/bytedance/GiantMIDI-Piano`（论文 Kong et al., "GiantMIDI-Piano: A large-scale
  MIDI dataset for classical piano music", arXiv:2010.07061）
- **内容**：以高精度钢琴转谱系统从公开演奏录音转录的古典钢琴独奏（2,704 位作曲家，共 1,237 小时；
  90% 现场演奏 + 10% 序列输入），含力度与踏板信息
- **许可**：**CC BY 4.0**（仓库 README「License」段明示）；其 `disclaimer.md` 仅为标准免责
  （as-is / 不担保 / 不担责），不含任何使用限制 → 按我们的分级归 **C1 可商用**，使用需署名
- **质量**：入库时以 mido 逐文件重算时长与音符数（覆盖 100%）；按作曲家生卒年推断音乐时期

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
