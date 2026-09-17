# LICENSE-AUDIT · 36 源逐项许可核对表

> 规则：**每源入库前必须完成本表一行**——结论（可重分发/仅链接）+ 依据（原文条款 URL 或本地 LICENSE 文件路径）+ 日期。
> 结论为「仅链接」的源不进入 dist 发布包，仅在门户 /sources/ 页提供外链。

| # | 源 id | 源名 | 规模 | 声称许可 | 核实结论 | 依据 | zone | 审计日期 |
|---|---|---|---|---|---|---|---|---|
| 1 | `aria` | Aria-MIDI (Unique) | 32,522 | CC BY-NC-SA 4.0 | ✅ 可重分发（须署名+NC+SA） | 本地 `sources/ariamidi/LICENSE.txt`；ICLR 2025 论文页 | piano-special | 2026-09-17 |
| 2 | `mutopia` | Mutopia Project | ~2,124 | 逐曲 CC / PD | ✅ 可重分发（逐曲 CC/PD；CC BY/SA 需署名） | 官网明文 "free to download, modify, print, copy, distribute, perform, and record – all in the Public Domain or under Creative Commons" · https://www.mutopiaproject.org/ | main | 2026-09-17 |
| 3 | `openscore` | OpenScore Lieder | ~1,300 | CC0 | ✅ 可重分发（CC0 无义务） | GitHub API license=CC0-1.0 · OpenScore/Lieder | main | 2026-09-17 |
| 4 | `musedata` | MuseData (CCARH) | ~1,200 作品 | ⚠️ **受限许可** | ❌ **不可重分发**（明文禁止任何分发，含非商业教学材料；禁商用/公演/录音） | GitHub musedata/* 仓库 LICENSE.txt 原文：“under no circumstance is the data to be embedded or included in teaching materials for commercial or non-commercial distribution” · 仅个人使用+学术研究 | research（**本地研究收录，永不进发布包，门户仅链接**） | 2026-09-17 |
| 5 | `sonatica` | sonatica.fm | ~11,000 | 声明生成自 PD 乐谱 | 待核（重点：转录者权利） | — | main | — |
| 6 | `pianomidi` | piano-midi.de | ~571 | **CC BY-SA (Germany)** | ✅ 可重分发（署名 Bernd Krueger + http://www.piano-midi.de + 同许可） | 官方版权页 http://piano-midi.de/copy.htm：「licensed under the cc-by-sa Germany License…distribution or public playback only allowed under identical license conditions」 | main | 2026-09-17 |
| 7 | `chinafolk` | 中国民间歌曲集成 | 10,479 | ⚠️ **未声明** | ⚠️ 本地收录、**不重分发**（门户仅链接原仓库）；待联系作者确认后升级 | README 无 LICENSE 文件；原扫描图声明有版权 · github.com/m-july/Anthology-of-Chinese-Folk-Songs | main | 2026-09-17 |
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
| 33 | `emopia` | EMOPIA | 387 | CC BY-NC-SA 4.0 | 待核 | — | research | — |
| 34 | `maestro` | MAESTRO | 1,282 | CC BY-NC-SA 4.0 | 待核 | — | research | — |
| 35 | `lakh` | Lakh MIDI | 174,533 | 学术 | 待核（v0.2 再议） | — | research | — |
| 36 | `ossq` | OpenScore String Quartets | 进行中 | CC0 | 待核 | — | main | — |
| 37 | `giantmidi` | GiantMIDI-Piano（新发现·重要） | ~10,855 作品 | 待核（论文数据集） | 待核（获取渠道另查：官方非 GitHub 直链） | arXiv 2010.07061 · github.com/bytedance/GiantMIDI-Piano | main(待核) | — |

## 审计流程

1. 找源官方许可声明页（或仓库 LICENSE 文件），存档快照到 `tools/reports/license-evidence/<source>/`
2. 判定三问：① 允许再分发吗？② 允许修改/转换吗？③ 有附加义务吗（署名格式/SA/NC）？
3. 结论写入本表 + 对应接入器内置 `license` 常量
4. **不明或有争议 → 「仅链接」**：不重分发，门户只给原站链接

## 永不收录（雷区）

受版权保护的**流行歌 / 游戏音乐** MIDI 转录（含 VGMusic、BitMidi、FreeMidi.org 等无授权托管站内容）——衍生作品侵权，非商用亦不豁免。
