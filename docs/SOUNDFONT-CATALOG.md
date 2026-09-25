# SOUNDFONT CATALOG · 音色库台账

> **用途**：为「lib 站固定音色 + 音色站（分站）」两站规划提供依据。
> **数据来源**：`musical-artifacts.com`（tag `soundfont`）**全量 1,067 条**，2026-09-25 抓取。
> **可复现**：`tools/sf_crawl.py`（抓取）→ `tools/sf_ledger.py --build`（生成本文件）。
> **机器可读版**：[`soundfonts.json`](soundfonts.json)。

## 一、总览

| 项 | 值 |
|---|---|
| 登记条目 | **1067** |
| **许可允许再分发** | **595（56%）** ← 可进入我们候选池 |
| **不可再分发（含站点自标存疑）** | **472（44%）** |
| 含 `.sf2` 格式的可分发条数 | 541 |

## 二、许可分布（全部 1067 条）

| 许可 | 数量 | 占比 | 档位 | 可再分发 |
|---|---:|---:|---|---|
| 站点自标「存疑」 | 358 | 33.6% | F4 | ❌ |
| CC BY 3.0 | 306 | 28.7% | F2 | ✅ |
| WTFPL（等同公有领域） | 107 | 10.0% | F1 | ✅ |
| 公有领域（站点标注） | 93 | 8.7% | F1 | ✅ |
| CC BY | 52 | 4.9% | F2 | ✅ |
| 版权受限 | 52 | 4.9% | F4 | ❌ |
| 混合 / 不明 | 38 | 3.6% | F4 | ❌ |
| CC BY-SA | 17 | 1.6% | F3 | ✅ |
| GPL v3 | 17 | 1.6% | F3 | ✅ |
| 未识别码 cc-sample | 7 | 0.7% | F4 | ❌ |
| 未识别码 falv13 | 4 | 0.4% | F4 | ❌ |
| CC BY-NC-ND 3.0 | 4 | 0.4% | F4 | ❌ |
| CC BY-NC | 4 | 0.4% | F4 | ❌ |
| CC BY-NC-SA | 3 | 0.3% | F4 | ❌ |
| GPL | 2 | 0.2% | F3 | ✅ |
| GPL v2 | 1 | 0.1% | F3 | ✅ |
| CC BY-NC-SA 3.0 | 1 | 0.1% | F4 | ❌ |
| 未识别码 by-nd | 1 | 0.1% | F4 | ❌ |

**档位说明**（沿用 MIDI 侧思路）：
- **F1 可自由分发**：CC0 / 公有领域 / WTFPL / Unlicense —— 站内可直接托管
- **F2 署名后可分发**：CC BY / MIT / BSD —— 站内可托管，须署名
- **F3 相同方式共享（传染）**：CC BY-SA / GPL —— 站内可托管，但衍生作品须同许可
- **F4 不可分发**：NC 系列 / 版权受限 / **站点自标存疑** / 未标注 —— **不托管、不推荐**

## 三、按用途分类（可分发候选 595 个）

| 分类 | 数量 | 说明 |
|---|---:|---|
| 游戏音源 | 541 | |
| 历史合成器/硬件音源 | 132 | |
| 钢琴 | 33 | |
| 管弦 / 古典 | 22 | |
| 民族 / 世界 | 3 | |
| 打击乐 / 鼓组 | 37 | |
| 电子 / 合成 | 23 | |
| 音效 / 其他 | 11 | |
| 通用 GM 音色库 | 47 | |
| 其他 / 未归类 | 218 | |

### 游戏音源（264 个 · 按下载量前 12）

| 名称 | 作者 | 许可 | .sf2 | 下载 |
|---|---|---|---:|---:|
| Touhou Soundfont | Team Shanghai Alice (g | CC BY | ✓ | 385457 |
| Nintendo Soundfont | hakerg | CC BY | ✓ | 53270 |
| OPL-3 FM 128M Soundfont | Zandro Reveille | CC BY-SA | ✓ | 49476 |
| Hedsound's MT32 Soundfont (CM64-L / LAPC-1) [GM remap fi | stgiga, hakerg, Ziya M | CC BY-SA | ✓ | 37765 |
| Casio CTK-230 SoundFont | Dekyo Ongen | CC BY | ✓ | 28588 |
| Minecraft Note Block Studio 3.3.4 Soundfont | Stuff by David | CC BY | ✓ | 27112 |
| General Game Boy Advance Soundfont 2.0 | BuskinCothurn | WTFPL（等同公有领域） | ✓ | 26032 |
| Gameboy GM Soundfont | CynthiaCelestic+ASIALU | WTFPL（等同公有领域） | ✓ | 22815 |
| Touhou Roland SRX EoSD Romantic Trumpet | Palto, DrKoupop | WTFPL（等同公有领域） | ✓ | 21449 |
| The Absolute Sega FM Soundfont Version 1.75!!! | Mx. K | WTFPL（等同公有领域） | ✓ | 17713 |
| Yamaha RX7 | Reza Chaniago Hartono  | CC BY | ✓ | 17583 |
| SampleSynthesis (an attempt to emulate/recreate toy keyb | Dekyo Ongen | CC BY | ✓ | 17045 |

### 历史合成器/硬件音源（67 个 · 按下载量前 12）

| 名称 | 作者 | 许可 | .sf2 | 下载 |
|---|---|---|---:|---:|
| Roland SC-88 (Full Version) | Mr.Sanic | WTFPL（等同公有领域） | ✓ | 116935 |
| Roland SC-8820 SoundFont | Mr.Sanic | WTFPL（等同公有领域） | ✓ | 26551 |
| Kurzweil K2000 Stereo Grand (Soundfont) | The GP | CC BY 3.0 | ✓ | 22903 |
| Kurzweil K2000 Acous 12 Strings (Soundfont) | The GP | CC BY 3.0 | ✓ | 14717 |
| Yamaha C3 Grand Piano | Ctech2021 | CC BY 3.0 | ✓ | 13227 |
| Florestan Basic GM GS | Nando Florestan | 公有领域（站点标注） | ✓ | 12837 |
| EVE burst error (PC-98) Soundfont | Ryu Umemoto | WTFPL（等同公有领域） | ✓ | 12696 |
| Live HQ Natural SoundFont GM V3.0 | UnderxPipe1985 | CC BY | — | 12693 |
| Galaxy Electric Pianos | Strix Soundfont Team a | GPL v3 | ✓ | 12622 |
| St. GIGA's HQ FM General MIDI Set | stgiga/stgiga | CC BY | ✓ | 12031 |
| Kurzweil K2000 Steel String Guitar (Soundfont) | The GP | CC BY 3.0 | ✓ | 12020 |
| Roland MV-30 (SC-55 Version) | MAG2001 | CC BY 3.0 | ✓ | 9291 |

### 钢琴（18 个 · 按下载量前 12）

| 名称 | 作者 | 许可 | .sf2 | 下载 |
|---|---|---|---:|---:|
| Alex's gm soundfont version 1.3 | High quality sfs | CC BY 3.0 | ✓ | 69780 |
| Keppy's Steinway Piano (Version 5.2) | KaleidonKep99 & Frozen | CC BY-SA | — | 32674 |
| S90ES | Henrique Gogó | CC BY 3.0 | ✓ | 27220 |
| Real Honky tonk piano by Milton Paredes | Milton Paredes, mpj fa | CC BY | ✓ | 10965 |
| Rhodes EVP73 Soundfont | OK73 | 公有领域（站点标注） | ✓ | 9433 |
| FM Electric Piano | Strix SoundFont Team | 公有领域（站点标注） | ✓ | 8273 |
| [DEPRECATED] NeoVST Piano One (sf2 version) | Exthayan | CC BY 3.0 | ✓ | 7128 |
| Campbells Grand Piano Beta 2 Soundfont | Campbell Barton | 公有领域（站点标注） | ✓ | 7046 |
| Freepats Rhodes | Unknown | GPL | ✓ | 6488 |
| Yamaha YPT 220 soundfont studio version | TheSoundfontMaker | CC BY 3.0 | ✓ | 6287 |
| VS Upright Piano lite (soundfont version) | Versilian Studios | 公有领域（站点标注） | ✓ | 6112 |
| Florestan Piano | Nando Florestan | 公有领域（站点标注） | ✓ | 5787 |

### 管弦 / 古典（15 个 · 按下载量前 12）

| 名称 | 作者 | 许可 | .sf2 | 下载 |
|---|---|---|---:|---:|
| Squidfont Orchestral Soundfont | the guy2 (soundfont by | WTFPL（等同公有领域） | ✓ | 47867 |
| Musescore General HQ Soundfont (.sf2 Converted) | Frank Wen, Michael Cow | CC BY 3.0 | ✓ | 21853 |
| Florestan String Quartet | Nando Florestan | 公有领域（站点标注） | ✓ | 18620 |
| Florestan Woodwinds | Nando Florestan | 公有领域（站点标注） | ✓ | 14177 |
| tuba-ff | isis999 | WTFPL（等同公有领域） | ✓ | 6893 |
| Synth Brass 1 | Strix Soundfont Team | GPL v3 | ✓ | 6561 |
| Florestan Strings | Nando Florestan | 公有领域（站点标注） | ✓ | 5594 |
| Dizi from Freesound | Placeholder Stick | 公有领域（站点标注） | ✓ | 4728 |
| Florestan Trumpet Metallic | Nando Florestan | 公有领域（站点标注） | ✓ | 4452 |
| tenor-trombone-gig | isis999 | WTFPL（等同公有领域） | — | 3720 |
| Tin Whistle | misc | CC BY | ✓ | 3599 |
| Synth Brass 2 | Strix SoundFont Team | 公有领域（站点标注） | ✓ | 3324 |

### 民族 / 世界（2 个 · 按下载量前 12）

| 名称 | 作者 | 许可 | .sf2 | 下载 |
|---|---|---|---:|---:|
| (Wii U) Super Mario 3D World Soundfont (2019) | Mr.Sanic | 公有领域（站点标注） | ✓ | 13239 |
| Celtic Soundfont | Michel Cöme | 公有领域（站点标注） | ✓ | 6516 |

### 打击乐 / 鼓组（22 个 · 按下载量前 12）

| 名称 | 作者 | 许可 | .sf2 | 下载 |
|---|---|---|---:|---:|
| Metal drums | Justjaytrack | CC BY 3.0 | ✓ | 23336 |
| vibraphone-sustain-ff-sf2 | isis999 | WTFPL（等同公有领域） | ✓ | 9888 |
| marimba-deadstroke-ff-sf2 | isis999 | WTFPL（等同公有领域） | ✓ | 6861 |
| Industromatic v1.0 Soundfont | Erik Hermansen | 公有领域（站点标注） | ✓ | 6396 |
| small-balafon-from-Burkina-Faso-sf2 | Isis999 | WTFPL（等同公有领域） | ✓ | 5291 |
| Shaun's Drum Loops 1 Soundfont | Shaun Hunt | 公有领域（站点标注） | ✓ | 4903 |
| Custom Drums by JJ MH v2 | JJ MH | WTFPL（等同公有领域） | ✓ | 4387 |
| Rythm Set (PvZ Drumkits) | dzrt | CC BY 3.0 | ✓ | 4335 |
| Basement Noise v1.0 Soundfont | Erik Hermansen | 公有领域（站点标注） | ✓ | 4233 |
| Ai Basic Drums | daryl | CC BY 3.0 | ✓ | 4012 |
| Melodic Cuica Soundfont | Sizz Tuna | CC BY-SA | ✓ | 3447 |
| Shaun's Drum Loops 4 Soundfont | Shaun Hunt | 公有领域（站点标注） | ✓ | 3242 |

### 电子 / 合成（18 个 · 按下载量前 12）

| 名称 | 作者 | 许可 | .sf2 | 下载 |
|---|---|---|---:|---:|
| 20 synths | Stephen Rich | 公有领域（站点标注） | ✓ | 12337 |
| Supersaw Collection 2 | Strix SF2 | GPL v3 | ✓ | 11017 |
| Pleasure! (Beta 2) | Yingchun Soul (Elf of  | 公有领域（站点标注） | ✓ | 8623 |
| RCKTNEO SND316X soundfont (version 3.0, GM compatible, f | RCKTNEO | CC BY | ✓ | 7700 |
| Massive Pad 1 | Strix SoundFont Team | 公有领域（站点标注） | ✓ | 5583 |
| Classic House Organ 2 Bass | Aleksandr Bykov | CC BY 3.0 | ✓ | 4862 |
| Saw 8-Detune | Strix Soundfont Team | 公有领域（站点标注） | ✓ | 4609 |
| ReVintage World | Elf of Happy and Love, | GPL v3 | ✓ | 3584 |
| GM Soundtrack Pad Recreation | Darko747 | CC BY 3.0 | ✓ | 3296 |
| Mauifm | N/A | CC BY 3.0 | ✓ | 2887 |
| synthetic soundfont 1.0 | Piotr Grochowski | 公有领域（站点标注） | ✓ | 2484 |
| Yousuke Yasui Guitar And Drums +Tek Drums SoundFont | VentusArranger | 公有领域（站点标注） | ✓ | 2430 |

### 音效 / 其他（8 个 · 按下载量前 12）

| 名称 | 作者 | 许可 | .sf2 | 下载 |
|---|---|---|---:|---:|
| Florestan Ahh Choir | Nando Florestan | 公有领域（站点标注） | ✓ | 16429 |
| Mpj  vocal collection, my voice | Milton Paredes, mpj fa | CC BY-SA | ✓ | 7745 |
| Eevee Soundfont (2.5) | Renderite | CC BY 3.0 | ✓ | 6850 |
| StarEevee SoundFont | Renderite | CC BY 3.0 | ✓ | 4854 |
| Discord Soundfont | Mildanner | CC BY 3.0 | ✓ | 3140 |
| Acapella GM/GS for AWE32 and DLS | Juicestain | WTFPL（等同公有领域） | — | 2721 |
| Thurston Waffles Meow Soundfont | Anapan | 公有领域（站点标注） | ✓ | 653 |
| Árvore Leitor SFX Soundfont | Mildanner | CC BY 3.0 | ✓ | 557 |

### 通用 GM 音色库（22 个 · 按下载量前 12）

| 名称 | 作者 | 许可 | .sf2 | 下载 |
|---|---|---|---:|---:|
| SGM Soundfont | SonicLover 19 | CC BY 3.0 | ✓ | 289628 |
| The Ultimate Roblox Soundfont Pack V1.8 | NotRoblox | CC BY | ✓ | 57041 |
| DSoundFont | strix Soundfont Team | 公有领域（站点标注） | ✓ | 23391 |
| airfont 380Final | Milton Paredes, mpj fa | 公有领域（站点标注） | ✓ | 22233 |
| DSoundFont Plus | Strix SoundFont Team | 公有领域（站点标注） | ✓ | 21129 |
| Xiaod Bank Soundfont | Xiaod | 公有领域（站点标注） | ✓ | 9604 |
| airfont 340 | Milton Paredes, Mpj fa | WTFPL（等同公有领域） | ✓ | 9173 |
| BalancedGM 1 | sleaf | GPL v3 | ✓ | 9168 |
| DSOUNDFONT Lite | strixSF2 | 公有领域（站点标注） | ✓ | 7728 |
| Series 30 Synth (Original) | Nokia Corporation | 公有领域（站点标注） | ✓ | 6466 |
| Nokia S40 3rd Edition (2.04 WIP) | Zenxia | CC BY | ✓ | 6420 |
| GeneralTrash Soundfont | Alif Maharendra Sihomb | 公有领域（站点标注） | ✓ | 4270 |

### 其他 / 未归类（159 个 · 按下载量前 12）

| 名称 | 作者 | 许可 | .sf2 | 下载 |
|---|---|---|---:|---:|
| Strix's Guitar and Bass Pack | Strix Soundfont Team | GPL v3 | ✓ | 45253 |
| KBH Real and Swelling Choirs | lfz | CC BY | ✓ | 37872 |
| Amen Break Soundfont | ASmolBoy, VEXST | CC BY 3.0 | ✓ | 22647 |
| Proteus | Proteus | CC BY | ✓ | 20017 |
| Friday Night Funkin' Voice Soundfont | SkullMasked | WTFPL（等同公有领域） | ✓ | 18665 |
| Arab and Turk instruments | Fernando A. Martin (co | 公有领域（站点标注） | ✓ | 14081 |
| STYVELL ORCHESTRA SOUNDFONT SAXO-ALTO-VIB-FF | olof | CC BY-SA | ✓ | 13764 |
| Samsung Ch@t 222 (GT-E2220) Soundfont (122MB + 120KB) | Sonic Network Inc. | CC BY 3.0 | ✓ | 9923 |
| Sci-Fi & Supernatural | Joshua R (Soundfont Co | CC BY | ✓ | 9815 |
| Aeolus Soundfont | Strix Soundfont Team | GPL v3 | ✓ | 9674 |
| Concert Harp Soundfont (from Sonatina sfz) | Fernando A. Martin | CC BY | ✓ | 9178 |
| Organs Pack #8 | Strix Soundfont Team | GPL v3 | ✓ | 9172 |

## 四、未收录（472 个）

> 与 MIDI 侧同一纪律：**许可不清或不许再分发的一律不进候选池**。
> 其中 **358 个（34%）被该站自己标记为「存疑」（`gray`）** ——
> 多为**从商业游戏 ROM 提取的音色**，站点无法确认其再分发权。

| 未收录原因 | 数量 |
|---|---:|
| 站点自标「存疑」 | 358 |
| 版权受限 | 52 |
| 混合 / 不明 | 38 |
| 未识别码 cc-sample | 7 |
| 未识别码 falv13 | 4 |
| CC BY-NC-ND 3.0 | 4 |
| CC BY-NC | 4 |
| CC BY-NC-SA | 3 |
| CC BY-NC-SA 3.0 | 1 |
| 未识别码 by-nd | 1 |

## 五、对两站规划的含义

1. **lib 站**：固定**一个**音色库（默认 GeneralUser GS），不随曲目增多而增大体积；
   用户想换音色 → 去音色站。
2. **音色站**：内容分两层 ——
   - **可托管层（F1/F2/F3 共 595 个）**：许可明确，可直接站内分发；
     优先做 **F1**（CC0/PD，**200 个**，零署名负担）。
   - **指引层（F4）**：只写「来源 + 查询地址」，**不托管、不直链下载**。
3. **版权纪律**：与数据来源目录一致 —— **许可不明即不收录**；
   该站自标的 `gray` 一律按不可分发处理。

---

*本台账由 `tools/sf_ledger.py` 生成，勿手改；改动请改抓取数据后重跑。*
