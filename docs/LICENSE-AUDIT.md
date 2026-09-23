# LICENSE-AUDIT · 来源许可核对表（36 个候选 → **21 个入发布包**）

> 规则：**每源入库前必须完成本表一行**——结论（可重分发/仅链接）+ 依据（原文条款 URL 或本地 LICENSE 文件路径）+ 日期。
> 结论为「仅链接」的源不进入 dist 发布包，仅在门户 /sources/ 页提供外链。
>
> **⚠️ 本表是全量候选审计（36 个）**，其中**只有 21 个最终进入 v1.23 发布包**。
> 本表的「待核」行表示该候选**未通过**或**已放弃**（详见 `SOURCE-CATALOG.md`）；
> 发布包的实际来源集合以 `docs/provenance.json`（21 条）为准。
> 逐曲实际许可以 `meta/catalog.json` 的 `l` 字段为准。

| # | 源 id | 源名 | 规模 | 声称许可 | 核实结论 | 依据 | zone | 审计日期 |
|---|---|---|---|---|---|---|---|---|
| 1 | `aria` | Aria-MIDI (Unique) | 32,522 | CC BY-NC-SA 4.0 | ✅ 可重分发（须署名+NC+SA） | 本地 `sources/ariamidi/LICENSE.txt`；ICLR 2025 论文页 | piano-special | 2026-09-17 |
| 2 | `mutopia` | Mutopia Project | ~2,124 | 逐曲 CC / PD | ✅ 可重分发（逐曲 CC/PD；CC BY/SA 需署名） | 官网明文 "free to download, modify, print, copy, distribute, perform, and record – all in the Public Domain or under Creative Commons" · https://www.mutopiaproject.org/ | main | 2026-09-17 |
| 3 | `openscore` | OpenScore Lieder | ~1,300 | CC0 | ✅ 可重分发（CC0 无义务） | GitHub API license=CC0-1.0 · OpenScore/Lieder | main | 2026-09-17 |
| 4 | `musedata` | MuseData (CCARH) | ~1,200 作品 | ⚠️ **受限许可** | ❌ **不可重分发**（明文禁止任何分发，含非商业教学材料；禁商用/公演/录音） | GitHub musedata/* 仓库 LICENSE.txt 原文：“under no circumstance is the data to be embedded or included in teaching materials for commercial or non-commercial distribution” · 仅个人使用+学术研究 | research（**本地研究收录，永不进发布包，门户仅链接**） | 2026-09-17 |
| 5 | `sonatica` | sonatica.fm | ~11,000 | 声明生成自 PD 乐谱 | 待核（重点：转录者权利） | — | main | — |
| 6 | `pianomidi` | piano-midi.de | ~571 | **CC BY-SA (Germany)** | ✅ 可重分发（署名 Bernd Krueger + http://www.piano-midi.de + 同许可） | 官方版权页 http://piano-midi.de/copy.htm：「licensed under the cc-by-sa Germany License…distribution or public playback only allowed under identical license conditions」 | main | 2026-09-17 |
| 7 | `chinafolk` | 中国民间歌曲集成 | 10,473 | ⚠️ 上游未声明 | ✅ **已发布（C3 · TRADITIONAL-STUDY）** —— 旋律本身属传统民间文艺、通常已进入公有领域；但**转录底本**（记谱/整理稿）受版权保护，故**仅限研究/教学/学习**，禁止商用与公开表演，必须署名上游数据集 | 上游 README 无 LICENSE 文件、扫描图声明有版权 · github.com/m-july/Anthology-of-Chinese-Folk-Songs（arXiv:2512.14758）；本库据此**自行定级 C3** 并逐曲写入 `l` 字段 | study | 2026-09-23 |
| 8 | `figshare` | figshare 中国经典 | 14 | CC BY 4.0 | ✅ 可重分发（署名） | figshare 数据集页 DOI 10.6084/m9.figshare.5436022 | main | 2026-09-17 |
| 9 | `essen` | Essen Folk Song DB | 9,034 | EsAC 开放 | 待核 | — | main | — |
| 10 | `nottingham` | Nottingham Music DB | 1,200 | 开放 | 待核 | — | main | — |
| 11 | `norbeck` | Henrik Norbeck ABC | 2,800 | 开放 | 待核 | — | main | — |
| 12 | `thesession` | thesession.org | ~40,000 | CC BY-SA | 待核（确认版本 4.0） | — | main | — |
| 13 | `gregobase` | Gregobase | ~6,000 | CC BY-SA | 待核 | — | main | — |
| 14 | `josquin` | Josquin RP + CMME | ~1,000 | 开放 | 待核 | — | main | — |
| 15 | `hymnal` | Hymnal Tune Dataset | 1,756 | PD/开放 | 待核 | — | main | — |
| 16 | `groove` | Groove MIDI | 1,150 | CC BY 4.0 | 待核 | — | main | — |
| 17 | `musicnet` | MusicNet | 323 | CC BY 4.0 | 待核 | — | main | — |
| 18 | `jsbach` | JSB Chorales + music21 | ~1,000 | MIT/开放 | 待核 | — | main | — |
| 19 | `weimar` | Weimar Jazz DB | ~2,000 | 学术 | 待核（申请制） | — | research | — |
| 20 | `nesdb` | NES Music DB | 5,278 | 研究 | 待核 | — | research | — |
| 21 | `ccmusic` | 复旦 ccmusic | 数百+ | 学术 | 待核 | — | main | — |
| 22 | `cpdl` | CPDL ChoralWiki | ~25,000 | 逐曲 PD/CC | 待核（逐曲标签） | — | main | — |
| 23 | `kdf` | Kunst der Fuge | ~19,300 | 待核 | ❌ **不收录**（双重障碍：① 免费限流 5 首/天 → 全量需 10 年 ② 转录者权利不明）→ **门户仅链接** | 站点限流政策 + 无明确再分发许可 | — (仅链接) | 2026-09-17 |
| 24 | `imslp` | IMSLP 附件 | 数千 | 逐曲标签 | 待核 | — | main | — |
| 25 | `abcn` | abcnotation 各集合 | ~20,000 | 逐集合 | 待核 | — | main | — |
| 26 | `digtra` | Digital Tradition | 数万 | 待核 | 待核 | — | main | — |
| 27 | `hymnary` | Hymnary.org | 数千 | PD 为主 | 待核 | — | main | — |
| 28 | `kern` | KernScores | 选择性 | ⚠️ 混合 | ⚠️ **逐集合核**：站点 open access，但含 MuseData 派生数据（受限）→ **只取开放子集**（EsAC/民谣/原住民旋律等），MuseData 派生部分不取 | kern.ccarh.org（实测 200；注意与 kern.humdrum.org 是不同站点，后者 503） | main（开放子集） | 2026-09-17 |
| 29 | `oga` | OpenGameArt | 342（实测） | CC0 / CC-BY / CC-BY-SA / GPL | ✅ 可重分发（逐 asset 标注；342 个 asset 页许可标签已逐一回填核实：CC0 267 · CC-BY-SA 43 · CC-BY 29 · GPL 3） | opengameart.org 各 asset 页 `license-name` 标签 | main | 2026-09-17 |
| 30 | `wikifonia` | Wikifonia 遗存 | 6,434 → **PD 子集 446** | 混合 | ⚠️ **仅 PD 子集收录**：全库 6,434 首中 5,988 首为 20 世纪流行曲/爵士标准曲（版权内，已过滤）；保留 446 首传统/民歌（Traditional/Anonymous/Hungarian folk song…） | 署名关键词白名单过滤（tools/ingest_wikifonia.py） | main（446） | 2026-09-17 |
| 31 | `ia` | Internet Archive 精选 | 数千+ | 逐集合 | 待核（**筛掉游戏/流行**） | — | main | — |
| 32 | `midiworld` | MIDIWorld | 数千 | 站方声明 PD | 待核 | — | main | — |
| 33 | `emopia` | EMOPIA | 1,071 | CC BY-NC-SA 4.0 | ✅ **已发布（C2）** 须署名+非商用+相同方式共享 | Zenodo 5257995 数据集页明文 CC BY-NC-SA 4.0 | piano-special | 2026-09-23 |
| 34 | `maestro` | MAESTRO | 1,276 | CC BY-NC-SA 4.0 | ✅ **已发布（C2）** 须署名+非商用+相同方式共享 | magenta.tensorflow.org/datasets/maestro 明文 CC BY-NC-SA 4.0 | piano-special | 2026-09-23 |
| 35 | `lakh` | Lakh MIDI | 174,533 原始 | 数据集声明 CC BY 4.0 | ⚠️ **已发布（C3 · study）但内容层须过滤** —— 数据集许可**只覆盖其自身的整理**，不覆盖所收录曲目的词曲著作权（原作者明言「均从公开来源抓取、未转录」）。已剔除含版权声明 / 流行·影视·游戏路径 / **以及经人工逐条复核确认在保护期内的 521 首** | colinraffel.com/projects/lmd 声明 CC BY 4.0；台账 `internal/lakh-review-2026-09-23.md`；审计器 `tools/audit_license.py` | study | 2026-09-23 |
| 36 | `ossq` | OpenScore String Quartets | 进行中 | CC0 | ⏸ 未收录（尚未接入） | — | — | — |
| 37 | `giantmidi` | GiantMIDI-Piano | 10,112 | CC BY 4.0 | ✅ **已发布（C1）** 可商用，署名数据集与论文 | arXiv 2010.07061 · github.com/bytedance/GiantMIDI-Piano | main | 2026-09-23 |
| 38 | `atepp` | ATEPP（钢琴演奏转录） | 7,130 | CC BY 4.0 | ✅ **已发布（C1）** 可商用，署名数据集与论文；**一作品多演奏版**为设计特性 | github.com/tangjjbetsy/ATEPP（CC BY 4.0）· 论文 DOI | main | 2026-09-23 |
| 39 | `pdmx` | PDMX（公有领域钢琴乐谱） | 2,893 | CC0 1.0 / PD | ✅ **已发布（C1）** 自由使用；仅取 `no_license_conflict` 且 genre 属古典/民谣/世界/宗教的子集，并拦下「现代类自标 CC0」2,500 首 | github.com/pnlong/PDMX · Long et al. ICASSP 2025 · Zenodo 发布 | main | 2026-09-23 |

> **内嵌歌词（独立权利层 · 仅研究/学习）**：发布侧 2,778 首曲目内含 MIDI lyric meta-event。
> 歌词是**独立于曲目的另一层权利对象**，**不随曲目档位授予商用许可**；本库**不主张歌词著作权**。
> 上游对 MIDI 文件本身的许可**不能自动延伸**到第三方写入的歌词。约 2,642 首来自 PD-only 来源
> （歌词本身即 PD），风险集中在 lakh 的 136 首（该批已定级 C3 且保护期内者已剔）。
> 详见 `LICENSE.md §2.3` · `NOTICE.md`「内嵌歌词」节。

## 审计流程

1. 找源官方许可声明页（或仓库 LICENSE 文件），存档快照到 `tools/reports/license-evidence/<source>/`
2. 判定三问：① 允许再分发吗？② 允许修改/转换吗？③ 有附加义务吗（署名格式/SA/NC）？
3. 结论写入本表 + 对应接入器内置 `license` 常量
4. **不明或有争议 → 「仅链接」**：不重分发，门户只给原站链接

## 永不收录（雷区）

受版权保护的**流行歌 / 游戏音乐** MIDI 转录（含 VGMusic、BitMidi、FreeMidi.org 等无授权托管站内容）——衍生作品侵权，非商用亦不豁免。


## 风险分级说明（二次发布视角 · 2026-09-18 补充）

上表中的「开放声明」类来源（essen / norbeck / abcmisc / nottingham）使用的是**站点自声明式许可**——
即来源网站以文字声明可自由使用，但**没有标准化的许可文本（如 CC 法律文本）**。二次发布时此类声明的
法律强度弱于 CC 系列，特分级标注如下：

| 级别 | 来源 | 声明原文要点 | 二次发布评估 |
|---|---|---|---|
| 🟢 强 | thesession | 网站明确 CC BY-SA 3.0 | 可商用，须署名+相同共享 |
| 🟢 强 | openscore | CC0-1.0 正式文本 | 可商用 |
| 🟢 强 | oga / musicnet / groove | CC0/CC-BY-4.0 正式文本（逐曲/整库） | 可商用，按曲署名 |
| 🟢 强 | mutopia | PD 为主，逐曲标明 | 可商用（个别 CC BY-SA 曲目按标注） |
| 🟡 中 | essen (EsAC) | 「供学术研究自由使用」类声明 | **商用前建议进一步确认**；非商用/研究用途风险低 |
| 🟡 中 | norbeck | 站长个人声明「免费获取」 | 同上 |
| 🟡 中 | abcmisc | 各整理者提交，站点声明自由 | 同上 |
| 🟡 中 | nottingham | John Chambers 声明公开使用 | 同上 |
| ⚪ 特区 | aria | CC BY-NC-SA-4.0 正式文本 | 仅非商用（piano-special 区） |
| 🟠 自定 | chinafolk | 上游未声明；旋律传统 PD、**转录底本受保护** | **已发布，但自定级 C3（study）**：仅研究/教学/学习，禁商用与公开表演，必须署名（2026-09-23 定案） |
| 🟢 强 | atep / pdmx | CC BY 4.0 / CC0 1.0 正式文本 | 可商用（C1），按数据集署名 |
| 🔵 独立层 | 内嵌歌词 | 词作著作权独立于乐曲；上游对文件的许可**不覆盖**第三方歌词 | **不随档位授权**：无论曲目档位，歌词文本仅限研究/学习；本库不主张歌词著作权（`LICENSE.md §2.3`） |

**网站播放策略建议**：🟡 级源内容可上线但建议在「关于」页声明来源与用途；若网站完全非商业，🟡 级风险进一步降低。

## 隐私与合规自查（2026-09-18 执行）

- 仓库内容已全量扫描：无用户名、无本机路径、无私人邮箱、无 IP 泄露 ✅
- 每条记录保留 src_path（相对路径）以实现溯源，不含任何本机信息 ✅
- takedown 流程：见 LICENSE.md §7