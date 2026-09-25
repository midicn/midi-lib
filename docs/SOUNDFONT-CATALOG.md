# SOUNDFONT CATALOG · 音色库台账

> **用途**：音色站（`sf.midicn.com`）的内容真源 —— 目录三层的全部依据。
> **可复现**：`tools/sf_crawl.py`（抓四个来源）→ `tools/sf_ledger.py --build`（生成本文件）。
> **机器可读版**：[`soundfonts.json`](soundfonts.json)（音色站直接读它）。
> **本文件为全量明细** —— 不只是「收录了什么」，还包括**我们审过什么、以及为什么排除**。

## 一、总览

| 项 | 值 |
|---|---|
| 登记条目（四来源合计） | **1776** |
| **许可允许再分发** | **950（53%）** ← 进入候选池 |
| **不可再分发** | **826（47%）** |
| 含 `.sf2` 格式的可分发条目 | **671** |
| **F1 且 `.sf2` 且 ≤50 MB**（可直接托管） | **57** |

**四档分布**（判「这个音色文件能不能再分发」）：

| 档位 | 含义 | 数量 | 占比 |
|---|---|---:|---:|
| **F1** | 可自由分发（CC0 / 公有领域 / WTFPL / Unlicense） | **304** | 17.1% |
| **F2** | 署名后可分发（CC BY / MIT / BSD / ISC） | **589** | 33.2% |
| **F3** | 相同方式共享（有传染性：CC BY-SA / GPL） | **57** | 3.2% |
| **F4** | 不收录（禁止商用 / 禁止改作 / Sampling 系列 / 存疑 / 版权受限 / 未标注） | **826** | 46.5% |

**按来源**：

| 来源 | 抓法 | 条目 | 可分发 |
|---|---|---:|---:|
| **musical-artifacts.com** | artifacts.json API（tags=soundfont） | 1067 | 595 |
| **FreePats** | 36 个乐器页 HTML 解析 | 57 | 57 |
| **sfzinstruments** | data/sfz/instruments.yml | 148 | 62 |
| **MuseScore 官方音色分发** | Apache 目录索引 + HEAD 实测体积 | 5 | 4 |
| **FluidSynth 官方 wiki 清单** | 官方 wiki 页（仓库内 doc/wiki/SoundFont.md） | 9 | 0 |
| **GitHub topic:soundfont** | 搜索 API 取仓 + git/trees 列文件（许可取仓 LICENSE 的 SPDX） | 290 | 212 |
| **archive.org** | 搜索 API + 逐条目 metadata（许可 licenseurl 机器可读、文件体积可查） | 200 | 20 |

**按用途分类**（两口径并列 —— 全部条目 / 可分发候选）：

| 分类 | 全部 | 可分发 |
|---|---:|---:|
| 游戏音源 | 605 | 282 |
| 历史合成器/硬件音源 | 140 | 68 |
| 钢琴 | 123 | 60 |
| 管弦 / 古典 | 85 | 52 |
| 民族 / 世界 | 31 | 21 |
| 打击乐 / 鼓组 | 83 | 53 |
| 电子 / 合成 | 177 | 157 |
| 音效 / 其他 | 12 | 10 |
| 通用 GM 音色库 | 56 | 28 |
| 吉他 / 贝斯 / 拨弦 | 55 | 34 |
| 风琴 / 键盘乐器 | 13 | 12 |
| 人声 / 合唱 | 19 | 9 |
| 管乐独奏 | 11 | 9 |
| 其他 / 未归类 | 366 | 155 |

**体积已知情况**（共 1776 条）：

| 体积来源 | 条数 | 说明 |
|---|---:|---|
| 我们**实测**（Range / HEAD） | 322 | musical-artifacts 里可访问的直链 |
| **来源页标注** | 177 | FreePats / sfzinstruments / MuseScore 页面自带 |
| **未提供** | 1277 | 上游不提供、且直链拒绝访问（见 §二）—— **宁缺勿错，不猜** |

### 1.1 三个口径必须分清（读表前先看这段）

- **全部条目**：四个来源抓到的**全部**记录（含明确不可分发的）。
- **可分发候选**：许可允许再分发的（F1 + F2 + F3）—— 音色站目录收录这些。
- **可直接托管**：F1 且是 `.sf2` 且体积 ≤50 MB —— 站内直下只有这一档。

> 历史沿革：早期版本台账只有 musical-artifacts 一个来源（1,067 条 / 595 候选）。
> S0 补抓 FreePats / sfzinstruments / MuseScore 之后，来源覆盖与条目数均上升。

## 二、⚠️ 数据来源与覆盖度（诚实说明）

**已覆盖（累计 7 个来源）**：

| 来源 | 抓法 | 为什么抓它 |
|---|---|---|
| musical-artifacts.com | artifacts.json API（tags=soundfont） | 唯一的**批量结构化许可字段**来源（可按许可程序化筛选） |
| FreePats | 36 个乐器页 HTML 解析 | **DFSG 合规 · 质量经实践检验**；有 `.sf2` 且体积适中；**民族/世界乐器的主要来源**（bagpipe / kalimba / jaw harp / ukulele…） |
| sfzinstruments | data/sfz/instruments.yml | 钢琴与鼓组名品（Salamander / Bigcat Cello / SM Drums…）；YAML 自带许可与体积 |
| MuseScore 官方音色分发 | Apache 目录索引 + HEAD 实测体积 | **FluidR3_GM / MuseScore_General（MIT）** —— 社区最广泛推荐的两个 |
| FluidSynth 官方 wiki 清单 | 官方 wiki 页（仓库内 doc/wiki/SoundFont.md） | **引擎官方推荐过的**（策展信号）—— 该清单不写许可，故只进台账作指引 |
| GitHub topic:soundfont | 搜索 API 取仓 + git/trees 列文件（许可取仓 LICENSE 的 SPDX） | 长尾与新品；**许可取自仓库 LICENSE（机器可读）**，且 `git/trees` **自带文件体积** |
| archive.org | 搜索 API + 逐条目 metadata（许可 licenseurl 机器可读、文件体积可查） | 历史归档（含公有领域素材）；**licenseurl 与文件体积都可查**；⚠️ 本机直连不通，需经转发/代理 |

**尚未覆盖（诚实列出，不假装已全网）**：

| 优先级 | 来源 | 状态 | 为什么 |
|---|---|---|---|
| — | MuseScore 社区策展表格 | ✅ **已核实：不是音色清单** | 抓下来逐列看过：它是 Musescore 的**乐器分类 / 预设映射表**（Genre / Group / Family / Instrument / Unique ID，656 行），并不列音色文件 → **不作为台账来源**（不硬凑） |
| P2 | Polyphone Soundfont Collection | ⏳ 待抓 | 另一处活跃的社区合集，站点结构需先摸 |
| P3 | 各站点自建的「soundfont 索引页」 | ⏳ 长尾 | 多为一页链接，量小且许可需逐条核 |

> 复现提示：`archive.org` 的搜索与条目接口在部分网络下**不可直接访问**，
> 此时可用任意可用的 HTTP 转发取同样的公开 JSON；本表的条目即由此得到。

### 2.1 ⚠️ 两个来源的**限度**（必须一起读，否则会误判）

**① GitHub `topic:soundfont` 的许可口径**：许可取自**仓库的 LICENSE（SPDX）**——
那是作者对该仓内容的正式声明，与 musical-artifacts 用其 `license` 字段同源。
但**仓级许可不等于仓内每个采样都没有第三方权利**（有的仓是把零散素材打包重发）。
所以：条目里如实记「仓库 LICENSE: <SPDX>」，**没有声明许可的仓一律归 F4**；
真要托管时必须逐个再过一遍 —— 本线目前**不托管** GitHub 源的文件。

**② GitHub 源的境内可达性**：它的直链是 `raw.githubusercontent.com`。
实测**本机可达**（Range 206），但该域名在境内访客侧**不稳** —— 
所以它只作**目录与来源指引**：`url` 给仓库页，直链照给（能不能下取决于访客网络），
但我们**不复刻、不托管**该来源的文件（站点直下只做 FreePats 那批稳定可达的）。

> 说明：`sfzinstruments` 绝大多数条目是 **SFZ + WAV/FLAC**（不是 `.sf2`），
> 浏览器（WebAudioFont / soundfont-player）只吃 `.sf2` —— 故它们进**目录与指引层**，
> 不进「站内托管」层。这一点在台账里由 `formats` 字段如实体现，不做暗示。

**⚠️ 关于体积：musical-artifacts 这一项拿不到完整数据（实测结论）**

它的 API **不带体积字段**（详情 JSON 18 个字段里没有 size/bytes），
所以只能对直链**实测**（`Range: bytes=0-0` 读 `Content-Range` 的总长）。实测发现：

| 直链类型 | 条数 | 实测结果 |
|---|---:|---|
| 可访问（多为归档 `.zip` / `.rar` / `.7z`） | 235 | ✅ 体积已回填（本表「我们实测」） |
| **被拒绝访问**（直接 `.sf2` 一类，403 防盗链） | 786 | ❌ 抽样 21/21 全 403 → 统一按不可直连归类 |
| 无直链（只有 `mirrors` 等外链） | 46 | — 无法测 |

两个后果，都写清楚了：

1. **体积留空**：这些条目的体积在台账与页面上标为「**未提供**」，
   而不是编一个数字 —— 这也是「≤50 MB 才托管」这条红线对它们不生效的原因。
2. **下载按钮改走来源页**：既然直链会被 403 拒绝，页面就不再给「来源下载」按钮，
   改给「**来源页** ↗」——不把用户送到打不开的链接。

## 三、处置规则（每一档怎么处理，以及为什么）

| 档位 | 授权性质 | 本站处置 | 理由 |
|---|---|---|---|
| **F1** | CC0 / 公有领域 / WTFPL / Unlicense | ✅ **站内托管 + 直链下载** | 零署名负担、零传染、无合规悬案 |
| **F2** | CC BY / MIT / BSD / ISC | ✅ 站内托管（**F2 专区**） | 须**逐条附署名与许可原文摘录** |
| **F3** | CC BY-SA / GPL | ⚠️ **只给指引，不托管** | 有**传染性** —— 衍生作品须同许可，会把义务传给使用者 |
| **F4** | NC / ND / Sampling 系列 / 存疑 / 版权受限 / 未标注 | ❌ **不托管、不直链** | 见下方逐类说明 |

> **入档规则（两条都要满足）**：① 允许**商用**再分发；② 允许**改作**。
> 只满足一条的（如 CC BY-ND 允许再分发但禁改作、CC BY-NC 允许改作但禁商用）一律归 F4 —— 
> 因为音色的**主要用途就是衍生使用**，收了会误导使用者。这条规则让 F4 的含义是「**本站不收录**」，
> 而不只是「法律上不可分发」—— 台账里逐条写明**具体是哪一条不满足**。

### 3.1 为什么 F4 一律不收（逐类给原因）

| 原因 | 数量 | 说明 |
|---|---:|---|
| **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 | 358 | |
| **未标注许可** → 许可不明即不收录 | 268 | |
| 商业授权 / 需付费购买 | 59 | |
| 版权受限（原权利人保留全部权利） | 52 | |
| 混合 / 不明（同一包内多种来源，无法逐项确认） | 38 | |
| NC 系列：禁止商业使用 → 我们不代管、不直链 | 14 | |
| 自定义许可，条款未明 → **许可不明即不收录** | 11 | |
| NC-ND：禁商用且禁改作 → 我们不代管、不直链 | 9 | |
| CC Sampling 系列：整包原样再分发受限（仅非商业）→ 只给来源 | 7 | |
| **许可码未识别**（`falv13`）→ 不猜、不收录 | 4 | |
| 免费增值（免费版许可不明） | 2 | |
| CC Sampling Plus 1.0：整包原样再分发仅限非商业 → 只给来源 | 2 | |
| 标注 Free 但未指明具体许可 → 视为许可不明 | 1 | |
| **ND 禁改作**：音色的主要用途就是衍生（用采样做音乐/改编）→ 收录会误导使用者 | 1 | |

### 3.2 ⭐ 曲目的 C1/C2/C3 与音色的 F1–F4 是**两套独立的分级**

> 前者判「**这首曲子**能不能商用」，后者判「**这个音色文件**能不能再分发」。
> **同一个 F1 音色可以用来演奏 C3 曲目** —— 两者互不推导。

### 3.3 许可优先：同一音色多来源时取哪一条

同一音色可能同时出现在多个来源（例：Salamander Grand Piano 在 FreePats 与 sfzinstruments 都有）。
台账**两条都留**（各自记明来源与格式），并给出 `group` 字段供站点聚合展示；
若要**托管控件**，优先取：**① F1 优于 F2 优于 F3** → ② **`.sf2` 优于其余格式** → ③ **体积小者**。

## 四、F1 · 可自由分发（CC0 / 公有领域 / WTFPL / Unlicense） · 全量 304 条

> 本档**逐条列明**：名称 / 作者 / 来源 / 许可 / 是否 `.sf2` / 体积 / 下载量 / 分类。

**其中可直接托管的（`.sf2` 且 ≤50 MB）**：57 条 —— 见 §十。

| # | 名称 | 作者 | 来源 | 许可 | .sf2 | 体积 | 下载 | 分类 |
|---:|---|---|---|---|---:|---|---:|---|
| 1 | FreePats synthesizer percussion | FreePats project | FreePats | CC0 | ✓ | 1.0 MB | — | drum |
| 2 | Xylophone | Versilian Studios LLC | FreePats | CC0 | ✓ | 1.7 MB | — | drum |
| 3 | SM Drums | Scott McLean, Tod Stillwell, S | sfzinstruments | 公有领域 | — | 2.3 MB | — | drum |
| 4 | jd_rockkit1.sf2 | no idea | musical-artifacts | WTFPL（等同公有领域） | ✓ | 3.3 MB | 366 | drum |
| 5 | Tubular Bells | Versilian Studios LLC | FreePats | CC0 | ✓ | 4.3 MB | — | drum |
| 6 | Timpani | Versilian Studios LLC | FreePats | CC0 | ✓ | 4.5 MB | — | drum |
| 7 | World percussion | Versilian Studios LLC | FreePats | CC0 | ✓ | 4.9 MB | — | drum |
| 8 | Glasses of water | FreePats project | FreePats | CC0 | ✓ | 9.8 MB | — | drum |
| 9 | Hang tuned in D minor | FreePats project | FreePats | CC0 | ✓ | 11.0 MB | — | drum |
| 10 | Gogodze Phu Vol II | Karoryfer Samples | sfzinstruments | CC0 | — | 133.0 MB | — | drum |
| 11 | Frankensnare | Karoryfer Samples | sfzinstruments | CC0 | — | 900.0 MB | — | drum |
| 12 | Swirly Drums | Karoryfer Samples | sfzinstruments | CC0 | — | 1638.4 MB | — | drum |
| 13 | Unruly Drums | Karoryfer Samples | sfzinstruments | CC0 | — | 2048.0 MB | — | drum |
| 14 | Big Rusty Drums | Karoryfer Samples | sfzinstruments | CC0 | — | 2355.2 MB | — | drum |
| 15 | vibraphone-sustain-ff-sf2 | isis999 | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 9888 | drum |
| 16 | marimba-deadstroke-ff-sf2 | isis999 | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 6861 | drum |
| 17 | Industromatic v1.0 Soundfont | Erik Hermansen | musical-artifacts | 公有领域（站点标注） | ✓ | — | 6396 | drum |
| 18 | Shaun's Drum Loops 1 Soundfont | Shaun Hunt | musical-artifacts | 公有领域（站点标注） | ✓ | — | 4903 | drum |
| 19 | Custom Drums by JJ MH v2 | JJ MH | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 4387 | drum |
| 20 | Basement Noise v1.0 Soundfont | Erik Hermansen | musical-artifacts | 公有领域（站点标注） | ✓ | — | 4233 | drum |
| 21 | Shaun's Drum Loops 4 Soundfont | Shaun Hunt | musical-artifacts | 公有领域（站点标注） | ✓ | — | 3242 | drum |
| 22 | Shaun's Drum Loops 3 Soundfont | Shaun Hunt | musical-artifacts | 公有领域（站点标注） | ✓ | — | 3016 | drum |
| 23 | Shaun's Drum Loops 2 Soundfont | Shaun Hunt | musical-artifacts | 公有领域（站点标注） | ✓ | — | 2880 | drum |
| 24 | Gogodze Phu Vol I | Karoryfer Samples | sfzinstruments | CC0 | — | — | — | drum |
| 25 | The Definitive Perfect Drums Soundfont (V1, Fixed Banks) | TEC Again (original by lukinha | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 0 | drum |
| 26 | Jaw Harp | FreePats project | FreePats | CC0 | ✓ | 1.8 MB | — | ethnic |
| 27 | Kalimba | FreePats project | FreePats | CC0 | ✓ | 3.7 MB | — | ethnic |
| 28 | small-balafon-from-Burkina-Faso-sf2 | Isis999 | musical-artifacts | WTFPL（等同公有领域） | ✓ | 3.9 MB | 5291 | ethnic |
| 29 | Bagpipe | FreePats project | FreePats | CC0 | ✓ | 6.7 MB | — | ethnic |
| 30 | ganjo | itsclipping | sfzinstruments | CC0 | — | 23.0 MB | — | ethnic |
| 31 | Horse Pulse | Karoryfer Samples | sfzinstruments | CC0 | — | 180.0 MB | — | ethnic |
| 32 | Etherealwinds Harp II CE | Versilian Studios LLC | sfzinstruments | CC0 | — | 200.0 MB | — | ethnic |
| 33 | Celtic Soundfont | Michel Cöme | musical-artifacts | 公有领域（站点标注） | ✓ | — | 6516 | ethnic |
| 34 | little-scale's Ukulele | Placeholder Stick, little-scal | musical-artifacts | 公有领域（站点标注） | ✓ | — | 5841 | ethnic |
| 35 | Makala Ukulele Plucked | SuP3r_P1ckL3 | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 441 | ethnic |
| 36 | Rhythmfont | Charlie | musical-artifacts | 公有领域（站点标注） | ✓ | 0.1 MB | 1532 | game |
| 37 | Kirby 64 Flute Push Restored | Reza Khadafi | musical-artifacts | 公有领域（站点标注） | — | 0.1 MB | 1176 | game |
| 38 | Module'90 (free retro synth module) | Vini (2) | musical-artifacts | 公有领域（站点标注） | ✓ | 1.2 MB | 7621 | game |
| 39 | Module'89 (free retro synth module) | Vini (2) | musical-artifacts | 公有领域（站点标注） | ✓ | 1.2 MB | 2813 | game |
| 40 | Densetsu No Starfy GBA Soundfont | AJ Mendez | musical-artifacts | WTFPL（等同公有领域） | — | 2.8 MB | 1061 | game |
| 41 | (Wii U) Super Mario 3D World Soundfont (2019) | Mr.Sanic | musical-artifacts | 公有领域（站点标注） | ✓ | 8.6 MB | 13239 | game |
| 42 | Virtuosity Drums | Versilian Studios LLC | sfzinstruments | CC0 | — | 1126.4 MB | — | game |
| 43 | General Game Boy Advance Soundfont 2.0 | BuskinCothurn | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 26032 | game |
| 44 | Gameboy GM Soundfont | CynthiaCelestic+ASIALUNAR+Moet | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 22815 | game |
| 45 | Touhou Roland SRX EoSD Romantic Trumpet | Palto, DrKoupop | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 21449 | game |
| 46 | Friday Night Funkin' Voice Soundfont | SkullMasked | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 18665 | game |
| 47 | The Absolute Sega FM Soundfont Version 1.75!!! | Mx. K | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 17713 | game |
| 48 | Knuckles Chaotix soundfont | Veninator1207 | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 14659 | game |
| 49 | Retro Wave Paradise | strixSF2, 迎春心情 (Yingchun Soul) | musical-artifacts | 公有领域（站点标注） | ✓ | — | 10098 | game |
| 50 | midi arcade soundfont, full  collection | Milton Paredes, Mpj factory st | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 9928 | game |
| 51 | KK Slider Soundfont | coffeebug | musical-artifacts | 公有领域（站点标注） | ✓ | — | 7489 | game |
| 52 | DefleGB | Mx. K | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 6993 | game |
| 53 | OPLL(YM2413) Soundfont v1.5 | src3453 | musical-artifacts | 公有领域（站点标注） | ✓ | — | 6993 | game |
| 54 | Super Italo DiscoFont: Director's Cut | strixSF2, Yingchun Soul for th | musical-artifacts | 公有领域（站点标注） | ✓ | — | 6717 | game |
| 55 | PC-98 YM2608 SoundFont | Studio Emiko (original by Erik | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 6455 | game |
| 56 | The oringator soundfont | Milton Paredes, mpj factory st | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 5591 | game |
| 57 | HL4MGM | strixSF2, Yingchun Soul for th | musical-artifacts | 公有领域（站点标注） | ✓ | — | 5515 | game |
| 58 | Sonic Mania Soundfont v1.2 (INCOMPLETE) | MylesDG | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 5271 | game |
| 59 | pokemon emerald soundfont | nintendo (ripped by me) | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 4581 | game |
| 60 | Toejam and Earl soundfont v3 | Veninator1207 | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 4459 | game |
| 61 | Defle2151 GM | Mx. K | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 4458 | game |
| 62 | The DEFINITIVE BED LUMP Soundfont! (Undertale) | ASmolBoy | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 4352 | game |
| 63 | Boy Band Soundfont | S. Christian Collins | musical-artifacts | 公有领域（站点标注） | ✓ | — | 4289 | game |
| 64 | Beavis and Butt-Head soundfont (Genesis) | Veninator1207 | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 3956 | game |
| 65 | LG GX200 | jamisson tavares | musical-artifacts | 公有领域（站点标注） | ✓ | — | 3861 | game |
| 66 | High Quality Super Mario 64 Slider SF2 | EggsCantFly | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 3386 | game |
| 67 | Homebrew Browser (addicti.mod) Soundfont | hbaoymb | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 3300 | game |
| 68 | Super Battletoads Soundfont V1.0 | JJ MH | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 3216 | game |
| 69 | the midi arcade series, A P B - All poynts bulletin | Milton Paredes, MPJ factory st | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 3050 | game |
| 70 | Deus Ex (2000) Soundfont (Version _1) | Jordan Moore | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 2942 | game |
| 71 | Stinkofont 20X6 v2.1 | Gfdgsgxgzgdrc (me) | musical-artifacts | 公有领域（站点标注） | ✓ | — | 2857 | game |
| 72 | HL1MGM | strixSF2, 迎春心情 (Yingchunsoul)  | musical-artifacts | 公有领域（站点标注） | ✓ | — | 2834 | game |
| 73 | Overdriven Guitar Catalog V1 V2 is out!!! | Marigold | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 2824 | game |
| 74 | Growtopia Soundfont | coffeebug | musical-artifacts | 公有领域（站点标注） | ✓ | — | 2798 | game |
| 75 | Power rangers SNES V2 | longlong2004 | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 2777 | game |
| 76 | Fabricio Soundbank | legendfabricio | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 2775 | game |
| 77 | Sonic the Hedgehog - Genesis (GBA) Soundfont | TEC Again | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 2711 | game |
| 78 | Some Splatoon Sounds (Soundfont) | Marv :) | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 2423 | game |
| 79 | PopocacaGM (v3.1) | Mangonesse on 29/3/25 | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 2245 | game |
| 80 | Mario Golf: Toadstool Tour (2003) | LuckyPrincess  (original by Th | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 2110 | game |
| 81 | F-Zero GP Legend GBA | TheBlackHand28 | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 2080 | game |
| 82 | Densetsu no Starfy 4 Soundfont | Anthro | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 1978 | game |
| 83 | Tomodachi Life: Living the Dream Soundfont | plippy | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 1973 | game |
| 84 | Tomodachi Life Soundfont (Heavy WIP) | TEC Again | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 1854 | game |
| 85 | Rayman 2 N64 Soundfont | Dr. Kiwis | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 1718 | game |
| 86 | Stinkofont 20X6 (Old Version) | Gfdgsgxgzgdrc (me) | musical-artifacts | 公有领域（站点标注） | ✓ | — | 1494 | game |
| 87 | Shinobi III: Return Of The Ninja Master Soundfont (INCOMPLETE) | Blental | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 1389 | game |
| 88 | Square wave soundfont (well temperament version) | Piotr Grochowski | musical-artifacts | 公有领域（站点标注） | ✓ | — | 1354 | game |
| 89 | Updated Majora's Mask Soundfont (2024) | supermumbo | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 1338 | game |
| 90 | Square wave soundfont (meantone version) | Piotr Grochowski | musical-artifacts | 公有领域（站点标注） | ✓ | — | 1251 | game |
| 91 | Monster House DS/GBA Soundfont | Memex87 | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 1226 | game |
| 92 | Tonic Trouble N64 Soundfont | Dr. Kiwis | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 1186 | game |
| 93 | Cloudcones Instruments + XM Soundfont Dump | Zabutom and Nagz (and many oth | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 1157 | game |
| 94 | The Distraction Dance Soundfont | FerikkusuSF2s | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 1127 | game |
| 95 | Korg Triton Noisy Funky Synth Soundfont | Mildanner | musical-artifacts | 公有领域（站点标注） | ✓ | — | 1097 | game |
| 96 | Square wave soundfont (equal temperament version) | Piotr Grochowski | musical-artifacts | 公有领域（站点标注） | ✓ | — | 1021 | game |
| 97 | Roblox OOF! Soundfont | Anapan | musical-artifacts | 公有领域（站点标注） | ✓ | — | 1018 | game |
| 98 | Robots (GBA) Soundfont | RoxyGaming | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 954 | game |
| 99 | Ranma 1/2: Hard Battle Soundfont | ShiverThermal | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 923 | game |
| 100 | The SpongeBob SquarePants Movie (Nintendo GBA) Soundfont | TEC Again | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 882 | game |
| 101 | Lilo & Stitch 2 - Haemsterviel Havoc (Nintendo GBA) Soundfont | TEC Again | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 665 | game |
| 102 | Lilo & Stitch (Nintendo GBA) Soundfont | TEC Again | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 637 | game |
| 103 | [OUTDATED] The Compiled Sonic Battle Soundfont (also read desc) | AsalTheBunMoth | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 548 | game |
| 104 | Sonic Boom (ROM Hack) Drum Soundfont | Mildanner | musical-artifacts | 公有领域（站点标注） | ✓ | — | 437 | game |
| 105 | The Soul Hackers Soundfont | Spidergenius10 | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 436 | game |
| 106 | Shrek: Ogre's and Dronkey's (Nintendo DS) Soundfont | Someone On The Internet | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 421 | game |
| 107 | Sheep (Nintendo GBA) Soundfont | TEC Again | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 348 | game |
| 108 | Uniracers (SNES) Soundfont | Justaguy95 | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 274 | game |
| 109 | NSMB World 1 Soundfont(sf2) | me | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 184 | game |
| 110 | March of the Penguins (GBA) | Skyworks Interactive, DSI Game | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 94 | game |
| 111 | Roland Fantom X SoundFont | schforby6805 | musical-artifacts | 公有领域（站点标注） | ✓ | — | 0 | game |
| 112 | Silent Animal Park (Nintendo DS, Nintendo GameCube, PlayStation 2) sou | Wintersoft Game Studios | archive | 公有领域 | — | — | — | game |
| 113 | Sonic The Hedgehog (Sega Genesis Soundfont) (DLS Version) | — | archive | 公有领域 | — | — | — | game |
| 114 | Touhou Retrologue Pack 0.2 | DrKoupop | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 0 | game |
| 115 | DSoundFont | strix Soundfont Team | musical-artifacts | 公有领域（站点标注） | ✓ | — | 23391 | gm |
| 116 | airfont 380Final | Milton Paredes, mpj factory st | musical-artifacts | 公有领域（站点标注） | ✓ | — | 22233 | gm |
| 117 | DSoundFont Plus | Strix SoundFont Team | musical-artifacts | 公有领域（站点标注） | ✓ | — | 21129 | gm |
| 118 | Xiaod Bank Soundfont | Xiaod | musical-artifacts | 公有领域（站点标注） | ✓ | — | 9604 | gm |
| 119 | airfont 340 | Milton Paredes, Mpj factory st | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 9173 | gm |
| 120 | DSOUNDFONT Lite | strixSF2 | musical-artifacts | 公有领域（站点标注） | ✓ | — | 7728 | gm |
| 121 | Series 30 Synth (Original) | Nokia Corporation | musical-artifacts | 公有领域（站点标注） | ✓ | — | 6466 | gm |
| 122 | GeneralTrash Soundfont | Alif Maharendra Sihombing | musical-artifacts | 公有领域（站点标注） | ✓ | — | 4270 | gm |
| 123 | SumterNokia Ultimate Embedded GM Soundbank (26.62 MB) | Roe_2012 | musical-artifacts | 公有领域（站点标注） | ✓ | — | 3528 | gm |
| 124 | Half Life 1 Crowbar GM Soundfont | TheFunnyMan | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 3158 | gm |
| 125 | airfont 350 for MuseScore | Milton Paredes | musical-artifacts | 公有领域（站点标注） | — | — | 3129 | gm |
| 126 | SumterNokia Ultra Embedded GM Soundbank (21.53 MB) | Roe_2012 | musical-artifacts | 公有领域（站点标注） | ✓ | — | 2418 | gm |
| 127 | Baby font for musescore | Milton Paredes, MPJ factory st | musical-artifacts | 公有领域（站点标注） | — | — | 2125 | gm |
| 128 | Ukulele | FreePats project | FreePats | CC0 | ✓ | 1.5 MB | — | guitar |
| 129 | Bass Guitar YR | Andrea Biasior | FreePats | CC0 | ✓ | 2.2 MB | — | guitar |
| 130 | FSBS Electric Guitar Clean #2 (Jazz) | FreePats project | FreePats | CC0 | ✓ | 5.0 MB | — | guitar |
| 131 | FSBS Electric Guitar Clean #1 | FreePats project | FreePats | CC0 | ✓ | 6.3 MB | — | guitar |
| 132 | Spanish classical guitar | FreePats project | FreePats | CC0 | ✓ | 9.5 MB | — | guitar |
| 133 | FSBS Electric Guitar Direct | FreePats project | FreePats | CC0 | ✓ | 60.0 MB | — | guitar |
| 134 | FSBS Electric Guitar Distorted #2 | FreePats project | FreePats | CC0 | ✓ | 121.0 MB | — | guitar |
| 135 | Swagbass | Karoryfer Samples | sfzinstruments | CC0 | — | 138.0 MB | — | guitar |
| 136 | Growlybass | Karoryfer Samples | sfzinstruments | CC0 | — | 160.0 MB | — | guitar |
| 137 | Pastabass | Karoryfer Samples | sfzinstruments | CC0 | — | 301.0 MB | — | guitar |
| 138 | Fashionbass | Karoryfer Samples | sfzinstruments | CC0 | — | 302.0 MB | — | guitar |
| 139 | FSBS Electric Guitar Distorted #1 | FreePats project | FreePats | CC0 | ✓ | 317.0 MB | — | guitar |
| 140 | Shinyguitar | Karoryfer Samples | sfzinstruments | CC0 | — | 352.0 MB | — | guitar |
| 141 | Black_And_Green_Guitars | Karoryfer Samples | sfzinstruments | CC0 | — | 500.0 MB | — | guitar |
| 142 | Black And Blue Basses | Karoryfer Samples | sfzinstruments | CC0 | — | 961.0 MB | — | guitar |
| 143 | Dirty Major Power Chords Soundfont | CDGillis | musical-artifacts | 公有领域（站点标注） | ✓ | — | 7307 | guitar |
| 144 | Otto's Fretlessbass Soundfont | C.W.Budde & Otto's Bass | musical-artifacts | 公有领域（站点标注） | ✓ | — | 6396 | guitar |
| 145 | Kona K2 Series K2T Acoustic-Electric Guitar | Kaesufurr | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 6287 | guitar |
| 146 | Marigold's Power Guitar Soundfont | Marigold | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 3758 | guitar |
| 147 | Florestan Contrabassoon | Nando Florestan | musical-artifacts | 公有领域（站点标注） | ✓ | — | 2273 | guitar |
| 148 | Emilyguitar | Karoryfer Samples | sfzinstruments | CC0 | — | — | — | guitar |
| 149 | Korg M1EX Pipe Organ Restored | Reza Khadafi | musical-artifacts | 公有领域（站点标注） | — | 0.3 MB | 1902 | hist |
| 150 | roland cr-78 general midi soundfont (+ rhythm midi files) | barrelhead | musical-artifacts | WTFPL（等同公有领域） | ✓ | 0.3 MB | 801 | hist |
| 151 | Roland JD-800 Nylon Guitar Restored | Reza Khadafi | musical-artifacts | 公有领域（站点标注） | — | 0.9 MB | 3774 | hist |
| 152 | Korg M1 Guitar Restored | Reza Khadafi | musical-artifacts | 公有领域（站点标注） | — | 1.2 MB | 2435 | hist |
| 153 | Korg Wavestation Koto Restored | Reza Khadafi | musical-artifacts | 公有领域（站点标注） | — | 1.3 MB | 1949 | hist |
| 154 | Roland SC-88 (Full Version) | Mr.Sanic | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 116935 | hist |
| 155 | Roland SC-8820 SoundFont | Mr.Sanic | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 26551 | hist |
| 156 | Florestan Basic GM GS | Nando Florestan | musical-artifacts | 公有领域（站点标注） | ✓ | — | 12837 | hist |
| 157 | EVE burst error (PC-98) Soundfont | Ryu Umemoto | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 12696 | hist |
| 158 | little-scale's Yamaha MX100II Disklavier | Placeholder Stick, little-scal | musical-artifacts | 公有领域（站点标注） | ✓ | — | 7036 | hist |
| 159 | Acapella Group XG(S)MT88* | stgiga, stin/HighCPU/YoshiLove | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 6818 | hist |
| 160 | ZFont | Zalka | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 5533 | hist |
| 161 | The Mega Musical Soundfont | SandisBergvalds2008 | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 4155 | hist |
| 162 | Furnace FM General Midi | Mx. K | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 3969 | hist |
| 163 | Furnace OPL (General Midi Compatable) | Mx. K | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 2912 | hist |
| 164 | Vintage Ecuador sample pack | Milton Paredes, MPJ Factory st | musical-artifacts | WTFPL（等同公有领域） | — | — | 1905 | hist |
| 165 | Microsoft GS Wavetable SF2 | Roland, Microsoft | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 1397 | hist |
| 166 | HappyTreeFriends Recreated Midi Soundbanks. (my 3 versions) | CupheadKrasueHTFBewilderHouseF | musical-artifacts | 公有领域（站点标注） | ✓ | — | 1085 | hist |
| 167 | Pablemo 2023 | Pablemo | musical-artifacts | WTFPL（等同公有领域） | — | — | 876 | hist |
| 168 | Korg Triton Orchestra Hit Soundfont | Mildanner | musical-artifacts | 公有领域（站点标注） | ✓ | — | 812 | hist |
| 169 | Korg WAVESTATION Touch Organ Soundfont | Mildanner, KORG | musical-artifacts | 公有领域（站点标注） | ✓ | — | 710 | hist |
| 170 | Korg Triton Square Roots Soundfont | Mildanner | musical-artifacts | 公有领域（站点标注） | ✓ | — | 689 | hist |
| 171 | E-Mu Emax II South American Pipe and 2MGM + SC-55 Ice Rain in SF2 | BloodEater2704 | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 508 | hist |
| 172 | Ocarina | FreePats project | FreePats | CC0 | ✓ | 3.0 MB | — | orch |
| 173 | Concert Harp | Versilian Studios LLC | FreePats | CC0 | ✓ | 4.9 MB | — | orch |
| 174 | Tenor Saxophone | Versilian Studios LLC | FreePats | CC0 | ✓ | 6.5 MB | — | orch |
| 175 | Clarinet | FreePats project | FreePats | CC0 | ✓ | 6.7 MB | — | orch |
| 176 | Wooden Recorder | Eugene Vlaskin | FreePats | CC0 | ✓ | 7.9 MB | — | orch |
| 177 | War Tuba | Karoryfer Samples | sfzinstruments | CC0 | — | 104.0 MB | — | orch |
| 178 | Sneakybass | Karoryfer Samples | sfzinstruments | CC0 | — | 324.0 MB | — | orch |
| 179 | VS Chamber Orchestra: Community Edition | Versilian Studios LLC | sfzinstruments | CC0 | — | 2355.2 MB | — | orch |
| 180 | Squidfont Orchestral Soundfont | the guy2 (soundfont by bigsqui | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 47867 | orch |
| 181 | Florestan String Quartet | Nando Florestan | musical-artifacts | 公有领域（站点标注） | ✓ | — | 18620 | orch |
| 182 | Florestan Woodwinds | Nando Florestan | musical-artifacts | 公有领域（站点标注） | ✓ | — | 14177 | orch |
| 183 | tuba-ff | isis999 | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 6893 | orch |
| 184 | Florestan Strings | Nando Florestan | musical-artifacts | 公有领域（站点标注） | ✓ | — | 5594 | orch |
| 185 | Dizi from Freesound | Placeholder Stick | musical-artifacts | 公有领域（站点标注） | ✓ | — | 4728 | orch |
| 186 | Florestan Trumpet Metallic | Nando Florestan | musical-artifacts | 公有领域（站点标注） | ✓ | — | 4452 | orch |
| 187 | tenor-trombone-gig | isis999 | musical-artifacts | WTFPL（等同公有领域） | — | — | 3720 | orch |
| 188 | Synth Brass 2 | Strix SoundFont Team | musical-artifacts | 公有领域（站点标注） | ✓ | — | 3324 | orch |
| 189 | Kiara Klarinet | Duplex | musical-artifacts | 公有领域（站点标注） | ✓ | — | 2408 | orch |
| 190 | Bear Sax | Karoryfer Samples | sfzinstruments | CC0 | — | — | — | orch |
| 191 | Bigcat Cello | Karoryfer Samples | sfzinstruments | CC0 | — | — | — | orch |
| 192 | D. Smolken Double Bass | Karoryfer Samples | sfzinstruments | CC0 | — | — | — | orch |
| 193 | Meatbass | Karoryfer Samples | sfzinstruments | CC0 | — | — | — | orch |
| 194 | Squidpipes | Karoryfer Samples | sfzinstruments | CC0 | — | — | — | orch |
| 195 | String Cyborgs | Karoryfer Samples | sfzinstruments | CC0 | — | — | — | orch |
| 196 | Weresax | Karoryfer Samples | sfzinstruments | CC0 | — | — | — | orch |
| 197 | Button Accordion HN | Jeff Stauffer | FreePats | CC0 | — | 4.8 MB | — | organ |
| 198 | Drawbar organ emulation | Roberto | FreePats | CC0 | ✓ | 5.8 MB | — | organ |
| 199 | Percussive organ emulation | FreePats project | FreePats | CC0 | ✓ | 12.0 MB | — | organ |
| 200 | Rock organ emulation | FreePats project | FreePats | CC0 | ✓ | 12.0 MB | — | organ |
| 201 | Church Organ Emulation | Fons Adriaensen | FreePats | CC0 | ✓ | 13.0 MB | — | organ |
| 202 | DJ's Hip Hop Kit | DJ Incendration | musical-artifacts | WTFPL（等同公有领域） | — | 0.1 MB | 1820 | other |
| 203 | Milo Murphy's Law Soundfont | RunTheCoins | archive | CC0 | ✓ | 0.4 MB | — | other |
| 204 | RemyMarshal's worlds smallest soundfont (electric piano) | RemyMarshal | musical-artifacts | WTFPL（等同公有领域） | ✓ | 0.7 MB | 129 | other |
| 205 | Gamer’s Tracker-MIDI(nSF2) Extracted Collection | Gamer45, technically also by m | musical-artifacts | WTFPL（等同公有领域） | ✓ | 12.5 MB | 445 | other |
| 206 | Ethan Winer Collection | Ethan Winer | sfzinstruments | 公有领域 | — | 17.0 MB | — | other |
| 207 | Kasey's World - The (Un-official) Soundfont | Greg Klas | archive | CC0 | ✓ | 427.4 MB | — | other |
| 208 | Mickey Mouse Clubhouse (Un-Official Soundfont) | Mike Himelstein and Mike Turne | archive | CC0 | ✓ | 567.4 MB | — | other |
| 209 | Versilian Community Sample Library | Versilian Studios LLC | sfzinstruments | CC0 | — | 4096.0 MB | — | other |
| 210 | Arab and Turk instruments | Fernando A. Martin (compilatio | musical-artifacts | 公有领域（站点标注） | ✓ | — | 14081 | other |
| 211 | The Discord Soundfont | Tyrone Monroe | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 6503 | other |
| 212 | Florestan Tubular Bells | Nando Florestan | musical-artifacts | 公有领域（站点标注） | ✓ | — | 4530 | other |
| 213 | Vine Boom Sound Effect | BlueKirby | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 4381 | other |
| 214 | EAWpats the soundfont | jamisson tavares | musical-artifacts | 公有领域（站点标注） | ✓ | — | 3974 | other |
| 215 | Florestan Pizzicato | Nando Florestan | musical-artifacts | 公有领域（站点标注） | ✓ | — | 3879 | other |
| 216 | MR BEAST soundfont | by a Literally unmentioned per | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 3577 | other |
| 217 | Rave Stab SoundFont | Strix SoundFont Team | musical-artifacts | 公有领域（站点标注） | ✓ | — | 3455 | other |
| 218 | Campbell's Verby Vocal Soundfont | Campbell Barton | musical-artifacts | 公有领域（站点标注） | ✓ | — | 3137 | other |
| 219 | Rayman 3 GBA Soundfont | Dr. Kiwis | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 2753 | other |
| 220 | LG_T375 Soundfont | jamisson tavares | musical-artifacts | 公有领域（站点标注） | ✓ | — | 2338 | other |
| 221 | Pixitracker Soundfont | hqc | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 2314 | other |
| 222 | Mega Man Zero 1 4 Soundfont ( VER 1) | Jordan Moore | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 2265 | other |
| 223 | Cat Meow Soundfont | Unknown | musical-artifacts | 公有领域（站点标注） | ✓ | — | 1952 | other |
| 224 | Nokia 3310 Soundfont | Nokia | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 1943 | other |
| 225 | Air.ogg SoundFont | boq | musical-artifacts | 公有领域（站点标注） | ✓ | — | 1915 | other |
| 226 | MSG-8x | Arsi | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 1676 | other |
| 227 | Trombone.sf2 V.0.4 | Guy | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 1409 | other |
| 228 | MicroSalterDroid (SONiVOX BAE Style) | Roe_2012 | musical-artifacts | 公有领域（站点标注） | ✓ | — | 1121 | other |
| 229 | Megadimension Neptunia VII - Nep Nep Nep | James Monroe | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 1099 | other |
| 230 | John Tay Marble Zone Good Future SF2 | Jojo Witstar | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 1082 | other |
| 231 | John Tay's Hydro City Act 2 Remix SF2 | Mx. K | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 1064 | other |
| 232 | Pokémon DPPt HQ GM | TheIndigoShine | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 863 | other |
| 233 | COMS (Collection of my samples) - 1.1 | Bernardo Jose | musical-artifacts | 公有领域（站点标注） | ✓ | — | 506 | other |
| 234 | FoxOG.sf2 V6 Test (SRB2 Soundfont) | LusterArtz | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 442 | other |
| 235 | Plusho's Soundfont (V0.01) | PlushoRR | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 284 | other |
| 236 | Sunset Brass | Wallo | musical-artifacts | 公有领域（站点标注） | ✓ | — | 226 | other |
| 237 | Diner Dash: Sizzle & Serve [DS] ripped soundfonts and midis | Secret Stash Games/Syrox Devel | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 225 | other |
| 238 | Dalores "Hm" Soundfont (Encanto) | Landon & Emma | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 182 | other |
| 239 | SheZow Soundfont (WIP) | ShiverThermal | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 164 | other |
| 240 | hoy es domingo full | Milton Paredes, MPJ Factory st | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 131 | other |
| 241 | fofo soundfont (halloween: just the facts) | lakery | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 117 | other |
| 242 | Dr Who Toy Soundfont | BBC | archive | CC0 | — | — | — | other |
| 243 | DTS Soundfont | Swarm | archive | 公有领域 | — | — | — | other |
| 244 | Ergo electric upright bass | Karoryfer Samples | sfzinstruments | CC0 | — | — | — | other |
| 245 | Helper for MusESequenzer | Bernd Mullet | musical-artifacts | WTFPL（等同公有领域） | — | — | 0 | other |
| 246 | Minecraft Noteblock Soundfont v4.00 | happy_mimimix | archive | 公有领域 | — | — | — | other |
| 247 | Nickleus SF2 SoundFont Collection | — | archive | 公有领域 | — | — | — | other |
| 248 | Online Sequencer Soundfont | Landon & Emma | archive | CC0 | — | — | — | other |
| 249 | OXOP SoundSet | OXOP | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 0 | other |
| 250 | Random Soundfont Public Version 1 | DamonCat | archive | 公有领域 | — | — | — | other |
| 251 | updated SM64 Soundfont | JackJamesMacdonald5 | archive | CC0 | — | — | — | other |
| 252 | Windows Soundfont GM Standard No Banks and Modulators 128+1_Drumset | Conp Et Sepohk | musical-artifacts | 公有领域（站点标注） | ✓ | — | 0 | other |
| 253 | FM Synthesized Piano #2 | FreePats project | FreePats | CC0 | ✓ | 4.6 MB | — | piano |
| 254 | Upright Piano KW | Gonzalo | FreePats | CC0 | ✓ | 5.8 MB | — | piano |
| 255 | Old Piano FB | FreePats project | FreePats | CC0 | ✓ | 8.8 MB | — | piano |
| 256 | FM Synthesized Piano #1 | FreePats project | FreePats | CC0 | ✓ | 13.0 MB | — | piano |
| 257 | FM Electric Piano | Strix SoundFont Team | musical-artifacts | 公有领域（站点标注） | ✓ | 53.7 MB | 8273 | piano |
| 258 | Splendid Grand Piano | AKAI | sfzinstruments | 公有领域 | — | 77.0 MB | — | piano |
| 259 | VCSL Keys | Versilian Studios LLC | sfzinstruments | CC0 | — | 680.0 MB | — | piano |
| 260 | Rhodes EVP73 Soundfont | OK73 | musical-artifacts | 公有领域（站点标注） | ✓ | — | 9433 | piano |
| 261 | Campbells Grand Piano Beta 2 Soundfont | Campbell Barton | musical-artifacts | 公有领域（站点标注） | ✓ | — | 7046 | piano |
| 262 | VS Upright Piano lite (soundfont version) | Versilian Studios | musical-artifacts | 公有领域（站点标注） | ✓ | — | 6112 | piano |
| 263 | Florestan Piano | Nando Florestan | musical-artifacts | 公有领域（站点标注） | ✓ | — | 5787 | piano |
| 264 | Super 5 | Myself - Aaron Gleason | musical-artifacts | 公有领域（站点标注） | ✓ | — | 208 | piano |
| 265 | ILIO Sinclavier Essential Percussion (Soundfont/.sf2 Conversion) | — | archive | CC0 | — | — | — | piano |
| 266 | Scarypiano | Karoryfer Samples | sfzinstruments | CC0 | — | — | — | piano |
| 267 | Thurston Waffles Meow Soundfont | Anapan | musical-artifacts | 公有领域（站点标注） | ✓ | — | 653 | sfx |
| 268 | Synth Bass #2 | FreePats project | FreePats | CC0 | ✓ | 1.7 MB | — | synth |
| 269 | Lately Bass | FreePats project | FreePats | CC0 | ✓ | 2.0 MB | — | synth |
| 270 | Synth Bass #1 | FreePats project | FreePats | CC0 | ✓ | 3.2 MB | — | synth |
| 271 | Synth Brass #2 | FreePats project | FreePats | CC0 | ✓ | 3.4 MB | — | synth |
| 272 | Synth Strings #1 | FreePats project | FreePats | CC0 | ✓ | 4.2 MB | — | synth |
| 273 | Synth Crystal | FreePats project | FreePats | CC0 | ✓ | 4.4 MB | — | synth |
| 274 | Synth Brass #1 | FreePats project | FreePats | CC0 | ✓ | 5.2 MB | — | synth |
| 275 | Synth Bass & Lead | FreePats project | FreePats | CC0 | ✓ | 6.1 MB | — | synth |
| 276 | Sweep Pad | FreePats project | FreePats | CC0 | ✓ | 7.2 MB | — | synth |
| 277 | New Age | FreePats project | FreePats | CC0 | ✓ | 7.4 MB | — | synth |
| 278 | Synth Strings #2 | FreePats project | FreePats | CC0 | ✓ | 7.4 MB | — | synth |
| 279 | Synth Lead Calliope | FreePats project | FreePats | CC0 | ✓ | 7.5 MB | — | synth |
| 280 | Synth Lead Square | FreePats project | FreePats | CC0 | ✓ | 9.0 MB | — | synth |
| 281 | Synth Fifths | FreePats project | FreePats | CC0 | ✓ | 12.0 MB | — | synth |
| 282 | Synth Pad Choir | FreePats project | FreePats | CC0 | ✓ | 12.0 MB | — | synth |
| 283 | Synth Soundtrack | FreePats project | FreePats | CC0 | ✓ | 17.0 MB | — | synth |
| 284 | Synth Goblins | FreePats project | FreePats | CC0 | ✓ | 19.0 MB | — | synth |
| 285 | Synth Pad Bowed | FreePats project | FreePats | CC0 | ✓ | 21.0 MB | — | synth |
| 286 | Synth Sci-Fi | FreePats project | FreePats | CC0 | ✓ | 22.0 MB | — | synth |
| 287 | Wavestate Pads | SHLD Music | sfzinstruments | CC0 | — | 160.0 MB | — | synth |
| 288 | Minifreak Pads | SHLD Music | sfzinstruments | CC0 | — | 265.0 MB | — | synth |
| 289 | 20 synths | Stephen Rich | musical-artifacts | 公有领域（站点标注） | ✓ | — | 12337 | synth |
| 290 | Pleasure! (Beta 2) | Yingchun Soul (Elf of Happy an | musical-artifacts | 公有领域（站点标注） | ✓ | — | 8623 | synth |
| 291 | Massive Pad 1 | Strix SoundFont Team | musical-artifacts | 公有领域（站点标注） | ✓ | — | 5583 | synth |
| 292 | Saw 8-Detune | Strix Soundfont Team | musical-artifacts | 公有领域（站点标注） | ✓ | — | 4609 | synth |
| 293 | synthetic soundfont 1.0 | Piotr Grochowski | musical-artifacts | 公有领域（站点标注） | ✓ | — | 2484 | synth |
| 294 | Yousuke Yasui Guitar And Drums +Tek Drums SoundFont | VentusArranger | musical-artifacts | 公有领域（站点标注） | ✓ | — | 2430 | synth |
| 295 | synthetic soundfont 2.0 | Piotr Grochowski | musical-artifacts | 公有领域（站点标注） | ✓ | — | 1342 | synth |
| 296 | <- /Discord Discord Revolution Soundfont/ -> | Melodii (AKA. MelodiiMilmshake | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 202 | synth |
| 297 | Caveman Cosmonaut | Karoryfer Samples | sfzinstruments | CC0 | — | — | — | synth |
| 298 | Cowsynth | Karoryfer Samples | sfzinstruments | CC0 | — | — | — | synth |
| 299 | Witch's Strat | Witch's Cadence | musical-artifacts | 公有领域（站点标注） | ✓ | — | 0 | synth |
| 300 | Acapella GM/GS for AWE32 and DLS | Juicestain | musical-artifacts | WTFPL（等同公有领域） | — | 80.5 MB | 2721 | vocal |
| 301 | Florestan Ahh Choir | Nando Florestan | musical-artifacts | 公有领域（站点标注） | ✓ | — | 16429 | vocal |
| 302 | 272 Merry Orks | Karoryfer Samples | sfzinstruments | CC0 | — | — | — | vocal |
| 303 | Angelic Clarinet Soundfont | Archangel | musical-artifacts | 公有领域（站点标注） | ✓ | — | 4760 | wind |
| 304 | Florestan Harmonica | Nando Florestan | musical-artifacts | 公有领域（站点标注） | ✓ | — | 4596 | wind |

## 五、F2 · 署名后可分发（CC BY / MIT / BSD / ISC） · 全量 589 条

> 本档**逐条列明**：名称 / 作者 / 来源 / 许可 / 是否 `.sf2` / 体积 / 下载量 / 分类。

| # | 名称 | 作者 | 来源 | 许可 | .sf2 | 体积 | 下载 | 分类 |
|---:|---|---|---|---|---:|---|---:|---|
| 1 | ElectronicDrumKit | gregogiudici | github | MIT | ✓ | 0.4 MB | — | drum |
| 2 | StandardDrumKit | gregogiudici | github | MIT | ✓ | 2.0 MB | — | drum |
| 3 | Dim Cabasa | kinwie | sfzinstruments | CC BY 4.0 | — | 12.0 MB | — | drum |
| 4 | MSLP Vibes | Bandshed Records | sfzinstruments | CC BY 3.0 | — | 19.0 MB | — | drum |
| 5 | MuldjordKit | FreePats project | FreePats | CC BY 4.0 | ✓ | 53.0 MB | — | drum |
| 6 | Muldjord Kit | DrumGizmo Team | sfzinstruments | CC BY 4.0 | — | 347.3 MB | — | drum |
| 7 | DRS Kit | DrumGizmo Team | sfzinstruments | CC BY 4.0 | — | 754.2 MB | — | drum |
| 8 | Naked Drums | Wilkinson Audio | sfzinstruments | CC BY 4.0 | — | 1331.2 MB | — | drum |
| 9 | Metal drums | Justjaytrack | musical-artifacts | CC BY 3.0 | ✓ | — | 23336 | drum |
| 10 | Rythm Set (PvZ Drumkits) | dzrt | musical-artifacts | CC BY 3.0 | ✓ | — | 4335 | drum |
| 11 | Ai Basic Drums | daryl | musical-artifacts | CC BY 3.0 | ✓ | — | 4012 | drum |
| 12 | Tenorion-On  Original Drumkits Soundfont | meri + alec brady for samples | musical-artifacts | CC BY | ✓ | — | 2864 | drum |
| 13 | 5b Drums | YoylePlant | musical-artifacts | CC BY 3.0 | ✓ | — | 2040 | drum |
| 14 | Talking Tom 2 Drum Soundfont | Mildanner, Outfit7 | musical-artifacts | CC BY 3.0 | ✓ | — | 853 | drum |
| 15 | FlashThemes Outro Drum Soundfont | Mildanner, FlashThemes | musical-artifacts | CC BY 3.0 | ✓ | — | 834 | drum |
| 16 | Breezy Day | Malaclypse the Younger | sfzinstruments | MIT | — | — | — | drum |
| 17 | Celesta_minimal | alnitak | github | MIT | — | — | — | drum |
| 18 | RatAttack | alnitak | github | MIT | ✓ | — | — | drum |
| 19 | SFX_StarWars_weapons | alnitak | github | MIT | ✓ | — | — | drum |
| 20 | SteelDrums | sinshu | github | MIT | — | — | — | drum |
| 21 | SynthDrum | sinshu | github | MIT | — | — | — | drum |
| 22 | TerribleDanger | alnitak | github | MIT | ✓ | — | — | drum |
| 23 | The Clap | Malaclypse the Younger | sfzinstruments | MIT | — | — | — | drum |
| 24 | Multi Kalimba | A1219 | musical-artifacts | CC BY | ✓ | — | 2876 | ethnic |
| 25 | Metal Pipe Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 1141 | ethnic |
| 26 | Bagpipe | sinshu | github | MIT | — | — | — | ethnic |
| 27 | Banjo | sinshu | github | MIT | — | — | — | ethnic |
| 28 | Kalimba | sinshu | github | MIT | — | — | — | ethnic |
| 29 | Koto | sinshu | github | MIT | — | — | — | ethnic |
| 30 | Shakuhachi | sinshu | github | MIT | — | — | — | ethnic |
| 31 | Shamisen | sinshu | github | MIT | — | — | — | ethnic |
| 32 | Sitar | sinshu | github | MIT | — | — | — | ethnic |
| 33 | GBFont Soundfont | MaliceX | musical-artifacts | CC BY | ✓ | 0.1 MB | 15694 | game |
| 34 | GXSCC GM v0.33 SoundFont | Zandro Reveille | musical-artifacts | CC BY | ✓ | 0.1 MB | 5884 | game |
| 35 | Toy Story Genesis PCM Mod RAW Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | — | 0.3 MB | 398 | game |
| 36 | Dangerous Seed TFI Instrument Pack | Mildanner | musical-artifacts | CC BY 3.0 | — | 0.7 MB | 172 | game |
| 37 | YM2612 FM Piano (Instrument Patch + Soundfont) | Mildanner | musical-artifacts | CC BY 3.0 | — | 0.9 MB | 796 | game |
| 38 | Sonic The Hedgehog Genesis (GBA) Samples and Midis | Jackstarreal_yt | musical-artifacts | CC BY 3.0 | — | 1.3 MB | 2288 | game |
| 39 | Super Putty (SNES) Soundfont and WAV Samples | Darko747 | musical-artifacts | CC BY 3.0 | ✓ | 1.5 MB | 1986 | game |
| 40 | Fullmetal Alchemist: Sonata of Memories Soundfont (UPDATE 4/28/2026) | VideoGameKid | musical-artifacts | CC BY 3.0 | ✓ | 1.5 MB | 788 | game |
| 41 | Winds Of Fjords (Better Samples) Soundfont [2.5.1] | Motionwave (MW) | musical-artifacts | CC BY | ✓ | 3.0 MB | 14460 | game |
| 42 | 3DS Soundfont + MIDI Collection | Stupid (Local WarioWare Enjoye | musical-artifacts | CC BY 3.0 | ✓ | 7.6 MB | 951 | game |
| 43 | Sonic Advance MIDI + Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | — | 8.7 MB | 6381 | game |
| 44 | Pac-in-Time Soundfont (outdated) | Frédéric Motte | musical-artifacts | CC BY 3.0 | ✓ | 9.8 MB | 1677 | game |
| 45 | Code Geass: Lelouch of the Rebellion R2 - Geass Theatric Boardgame Sou | VideoGameKid | musical-artifacts | CC BY 3.0 | — | 13.8 MB | 492 | game |
| 46 | MediaTek Soundfont GM (Wasteyarded) | XXtherobloxx21, MediaTek | musical-artifacts | CC BY | — | 17.6 MB | 782 | game |
| 47 | Guilty Gear Dust Strikers Soundfont (UPDATE 5/23/2026) | VideoGameKid (Originally rippe | musical-artifacts | CC BY 3.0 | ✓ | 18.2 MB | 1283 | game |
| 48 | Bleach DS 4th: Flame Bringer Soundfont (UPDATE 5/29/26) | VideoGameKid | musical-artifacts | CC BY 3.0 | ✓ | 19.1 MB | 1045 | game |
| 49 | Code Geass: Lelouch of the Rebellion DS Soundfont (UPDATE 5/26/2026) | VideoGameKid | musical-artifacts | CC BY 3.0 | ✓ | 24.7 MB | 895 | game |
| 50 | (Android) MIDI Player Synth Stock | Mildanner | musical-artifacts | CC BY 3.0 | — | 27.1 MB | 1185 | game |
| 51 | Super Mario 64 DS (MIDI + Soundfont) | Mildanner | musical-artifacts | CC BY 3.0 | — | 51.0 MB | 5769 | game |
| 52 | New Super Mario Bros. DS - MIDI and Soundfont | Mildanner, Nintendo | musical-artifacts | CC BY 3.0 | — | 74.1 MB | 4308 | game |
| 53 | Metal Slug 7 MIDI + Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | — | 95.4 MB | 864 | game |
| 54 | Touhou Soundfont | Team Shanghai Alice (game), un | musical-artifacts | CC BY | ✓ | — | 385457 | game |
| 55 | Nintendo Soundfont | hakerg | musical-artifacts | CC BY | ✓ | — | 53270 | game |
| 56 | Casio CTK-230 SoundFont | Dekyo Ongen | musical-artifacts | CC BY | ✓ | — | 28588 | game |
| 57 | Minecraft Note Block Studio 3.3.4 Soundfont | Stuff by David | musical-artifacts | CC BY | ✓ | — | 27112 | game |
| 58 | Yamaha RX7 | Reza Chaniago Hartono W. Walan | musical-artifacts | CC BY | ✓ | — | 17583 | game |
| 59 | SampleSynthesis (an attempt to emulate/recreate toy keyboards and lo-f | Dekyo Ongen | musical-artifacts | CC BY | ✓ | — | 17045 | game |
| 60 | ExpressiveSNES - General MIDI Super Nintendo Soundfont | DitherEmotion | musical-artifacts | CC BY 3.0 | ✓ | — | 12575 | game |
| 61 | YM2612 Guitar & Bass Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 12546 | game |
| 62 | Super Mario Bros Soundfont | Kirb7890 (Nintendo) | musical-artifacts | CC BY 3.0 | ✓ | — | 12205 | game |
| 63 | Korg Triton Instrument Pack Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 10876 | game |
| 64 | Drawn to Life: The Next Chapter (DS) Soundfont | 48 LAC | musical-artifacts | CC BY 3.0 | ✓ | — | 10177 | game |
| 65 | Super Mario World Soundfont v1.3 (2025) | Jechucam | musical-artifacts | CC BY 3.0 | ✓ | — | 9883 | game |
| 66 | Sega Genesis (ym2612) electric guitars soundfont | Iskalim | musical-artifacts | CC BY 3.0 | ✓ | — | 9482 | game |
| 67 | Studio Pixel Drums Soundfont | me :) | musical-artifacts | CC BY | ✓ | — | 9404 | game |
| 68 | Sonic 3D Blast Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 9223 | game |
| 69 | SONiVOX EAS GM Wavetable Ver. 1.83 | Sonic Network Inc. | musical-artifacts | CC BY 3.0 | ✓ | — | 8733 | game |
| 70 | DOOM (SNES) Soundfont | Zackie | musical-artifacts | CC BY | ✓ | — | 8326 | game |
| 71 | A tiny ~128ish sample 11khz Mobile Ice Cream Truck TI SN7 filtered PSG | stgiga, [nowanonymous], Zmey K | musical-artifacts | CC BY 3.0 | ✓ | — | 7658 | game |
| 72 | SONiVOX EAS GM Wavetable Ver. 1.92 | Sonic Network Inc. | musical-artifacts | CC BY 3.0 | ✓ | — | 7574 | game |
| 73 | aobu's chiptune soundfont v0.03 | aobunau | musical-artifacts | CC BY | ✓ | — | 6855 | game |
| 74 | Eevee Soundfont (2.5) | Renderite | musical-artifacts | CC BY 3.0 | ✓ | — | 6850 | game |
| 75 | SONiVOX EAS GM Wavetable Ver. 2.10 | Sonic Network Inc. | musical-artifacts | CC BY 3.0 | ✓ | — | 6453 | game |
| 76 | FPD 2.6 "PCMV2" | Dekyo Ongen | musical-artifacts | CC BY | ✓ | — | 6398 | game |
| 77 | Atari 2600 GM Bank | stgiga, little-scale, drunkenj | musical-artifacts | CC BY 3.0 | ✓ | — | 6095 | game |
| 78 | SONiVOX EAS GM Wavetable Ver. 2.00 | Sonic Network Inc. | musical-artifacts | CC BY 3.0 | ✓ | — | 5755 | game |
| 79 | Drawn to Life (DS) Soundfont | 48 LAC | musical-artifacts | CC BY 3.0 | ✓ | — | 5550 | game |
| 80 | The Smurfs (SNES) Soundfont | 48 LAC | musical-artifacts | CC BY 3.0 | ✓ | — | 5427 | game |
| 81 | Old School RuneScape (OSRS) Soundfont [GM] | Feem | musical-artifacts | CC BY 3.0 | ✓ | — | 5417 | game |
| 82 | Jam with the Band P. Soundfont (GM compatible) | TKMT_Aniki & RolandKnight | musical-artifacts | CC BY 3.0 | ✓ | — | 4938 | game |
| 83 | StarEevee SoundFont | Renderite | musical-artifacts | CC BY 3.0 | ✓ | — | 4854 | game |
| 84 | FM tone nº 101 from EFFEC.FF | Dekyo Ongen | musical-artifacts | CC BY | ✓ | — | 4761 | game |
| 85 | Mickey's Speedway USA derekSiZZLE's Soundfont (Fixed) | derekSiZZLE (Fixed Broken Loop | musical-artifacts | CC BY 3.0 | ✓ | — | 4648 | game |
| 86 | SONiVOX EAS GM Wavetable Ver. 1.91A | Sonic Network Inc. | musical-artifacts | CC BY 3.0 | ✓ | — | 4625 | game |
| 87 | Nesfont advance | Cat333pokemon, et al | musical-artifacts | CC BY 3.0 | ✓ | — | 4416 | game |
| 88 | Xadra's Legend of Zelda soundfont | Xadra | musical-artifacts | CC BY 3.0 | ✓ | — | 4319 | game |
| 89 | Club Penguin: Elite Penguin Force SoundFonts | tha SuuS | musical-artifacts | CC BY 3.0 | ✓ | — | 4318 | game |
| 90 | Sega Genesis Custom Drum Kit Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 4093 | game |
| 91 | SONiVOX EAS GM Wavetable Ver. 1.90 | Sonic Network Inc. | musical-artifacts | CC BY 3.0 | ✓ | — | 4088 | game |
| 92 | Micro Machines 2 (SNES) Soundfont | 48 LAC | musical-artifacts | CC BY 3.0 | ✓ | — | 4027 | game |
| 93 | Dr. Robotnik Mean Bean Machine Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 3885 | game |
| 94 | Marko's Magic Football (SNES) Soundfont | 48 LAC | musical-artifacts | CC BY 3.0 | ✓ | — | 3776 | game |
| 95 | SONiVOX EAS GM Wavetable Ver. 1.91 | Sonic Network Inc. | musical-artifacts | CC BY 3.0 | ✓ | — | 3718 | game |
| 96 | Dead Body Reported Soundfont | NH1507 | musical-artifacts | CC BY 3.0 | ✓ | — | 3710 | game |
| 97 | SONiVOX EAS GM Wavetable Ver. 1.81 | Sonic Network Inc. | musical-artifacts | CC BY 3.0 | ✓ | — | 3672 | game |
| 98 | SONiVOX EAS GM Wavetable Ver. 1.80 | Sonic Network Inc. | musical-artifacts | CC BY 3.0 | ✓ | — | 3496 | game |
| 99 | SonicMT.bin - Drum Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 3449 | game |
| 100 | GBA MegaMan Battle Network Soundfont Pack (1-6, 4.5, & BCC) | Nintenducc | musical-artifacts | CC BY 3.0 | ✓ | — | 3356 | game |
| 101 | The Kirby's Dream Land Soundfont! (V1.1) (OLD) | ArtifactedSonicMusical | musical-artifacts | CC BY 3.0 | ✓ | — | 3338 | game |
| 102 | Brandish 2 Soundfont | Carter Venom | musical-artifacts | CC BY 3.0 | ✓ | — | 3291 | game |
| 103 | Sonic the Hedgehog Genesis (GBA) Soundfont | Mildanner, SEGA Sonic Team | musical-artifacts | CC BY 3.0 | ✓ | — | 3217 | game |
| 104 | SONiVOX EAS GM Wavetable Ver. 1.82 | Sonic Network Inc. | musical-artifacts | CC BY 3.0 | ✓ | — | 3151 | game |
| 105 | TR-626 Drum Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 3118 | game |
| 106 | 02. St. Piano 2 Remastered | 白いチャンネル | musical-artifacts | CC BY 3.0 | ✓ | — | 3050 | game |
| 107 | MegaMan Battle Chip Challenge Soundfont | Nintenducc | musical-artifacts | CC BY 3.0 | ✓ | — | 3048 | game |
| 108 | Mario Party 2 Soundfont | tahutoa | musical-artifacts | CC BY 3.0 | ✓ | — | 3027 | game |
| 109 | Pac-in-Time Soundfont (Update) | NAMCO | musical-artifacts | CC BY 3.0 | ✓ | — | 3015 | game |
| 110 | Banjo-Tooie Soundfont | rareware | musical-artifacts | CC BY 3.0 | ✓ | — | 2918 | game |
| 111 | Sonic Crackers Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 2794 | game |
| 112 | Gimmick Sunsoft Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 2748 | game |
| 113 | Sonic 3 Clean Drum Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 2723 | game |
| 114 | Sonic Pocket Adventure Soundfont (Redux) | Mildanner, SEGA Sonic Team | musical-artifacts | CC BY 3.0 | ✓ | — | 2713 | game |
| 115 | Mischief Makers soundfont | HandlebarOrionX | musical-artifacts | CC BY 3.0 | ✓ | — | 2703 | game |
| 116 | Analog toy effects | Milton paredes, mpj factoy stu | musical-artifacts | CC BY | ✓ | — | 2675 | game |
| 117 | YM2612 Piano Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 2535 | game |
| 118 | Sega Master System Game Gear Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 2521 | game |
| 119 | Distraction Dance Soundfont | NH1507 | musical-artifacts | CC BY 3.0 | ✓ | — | 2477 | game |
| 120 | Sonic 3 Drum Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 2453 | game |
| 121 | SaGa 2 (NDS) Soundfont + Midis | Dusk | musical-artifacts | CC BY 3.0 | — | — | 2408 | game |
| 122 | Pokémon FireRed and LeafGreen Soundfont (VGM & Pokémon Sound Sources C | VideoGameKid | musical-artifacts | CC BY 3.0 | ✓ | — | 2372 | game |
| 123 | Gameboy Furnace Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 2368 | game |
| 124 | Sonic 1 South Island Expedition Drum Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 2300 | game |
| 125 | Kick Square Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 2253 | game |
| 126 | Remix 10 Bass Soundfont | Mildanner, Rhythm Heaven Fever | musical-artifacts | CC BY 3.0 | ✓ | — | 2242 | game |
| 127 | Sonic 1 Mixed Drum Soundfont | Mildanner, Hame | musical-artifacts | CC BY 3.0 | ✓ | — | 2204 | game |
| 128 | Segapede (Prototype) Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 2201 | game |
| 129 | Power Piggs of the Dark Age (SNES) Soundfont | 48 LAC | musical-artifacts | CC BY 3.0 | ✓ | — | 2195 | game |
| 130 | PSP Soundfont | XXtherobloxx21 (Fixed drums),  | musical-artifacts | CC BY 3.0 | ✓ | — | 2182 | game |
| 131 | Plants Vs. Zombies Soundfont (Improved) | VladTheFatman | musical-artifacts | CC BY 3.0 | ✓ | — | 2093 | game |
| 132 | Old Towers Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 2070 | game |
| 133 | Sonic Eraser Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 2019 | game |
| 134 | WWF No Mercy soundfont | HandlebarOrionX | musical-artifacts | CC BY 3.0 | ✓ | — | 1964 | game |
| 135 | Minecraft Soundfont (Improved) | UWFanaticSF2 | musical-artifacts | CC BY 3.0 | ✓ | — | 1936 | game |
| 136 | Wario Master Of Disguise Soundfont | HopefulSpread | musical-artifacts | CC BY 3.0 | ✓ | — | 1869 | game |
| 137 | WWF Wrestlemania 2000/Virtual Pro Wrestling 2 soundfont | HandlebarOrionX | musical-artifacts | CC BY 3.0 | ✓ | — | 1869 | game |
| 138 | Mighty Milky Way Soundfont | Lexicon86 | musical-artifacts | CC BY 3.0 | ✓ | — | 1868 | game |
| 139 | Mario Kart: Super Circuit Soundfont | Rosetta | musical-artifacts | CC BY 3.0 | — | — | 1854 | game |
| 140 | Sonic Advance Soundfont | OnuteWORLD Server Ltd. | musical-artifacts | CC BY 3.0 | ✓ | — | 1842 | game |
| 141 | Sonic the Hedgehog (Nintendo DS) Soundfont | Mildanner, Stealth | musical-artifacts | CC BY 3.0 | ✓ | — | 1838 | game |
| 142 | Knuckles Chaotix Drum Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 1806 | game |
| 143 | Sonic Hacking Contest Splash Screen Soundfont | Mildanner, Naoto, MDTravis | musical-artifacts | CC BY 3.0 | ✓ | — | 1783 | game |
| 144 | F-Zero: GP Legend GBA 2.0 | TheBlackHand28 | musical-artifacts | CC BY 3.0 | ✓ | — | 1776 | game |
| 145 | Yeah Jam Fury - Piano Block Soundfont | Mildanner, McLeodGaming, Willy | musical-artifacts | CC BY 3.0 | ✓ | — | 1764 | game |
| 146 | Segapede Soundfont Remake | Mildanner, Howard Drossin | musical-artifacts | CC BY 3.0 | ✓ | — | 1734 | game |
| 147 | MegaMan Battle Network 4.5 Soundfont | Nintenducc | musical-artifacts | CC BY 3.0 | ✓ | — | 1657 | game |
| 148 | Pantufa the Cat Orchestral Hit Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 1631 | game |
| 149 | Master System Game Gear Drum Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 1555 | game |
| 150 | MegaMan Battle Network 6 Soundfont | Nintenducc | musical-artifacts | CC BY 3.0 | ✓ | — | 1514 | game |
| 151 | Sonic the Hedgehog 2 Prototype Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 1508 | game |
| 152 | Izzy's Quest for the Olympic Rings (Genesis) | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 1498 | game |
| 153 | Sonic Robo Blast 2 Genesis Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 1491 | game |
| 154 | Sonic Jam (Sega Saturn) Soundfont | GAB64 | musical-artifacts | CC BY 3.0 | ✓ | — | 1396 | game |
| 155 | C700 VST Soundfont | Mildanner, osoumen | musical-artifacts | CC BY 3.0 | ✓ | — | 1389 | game |
| 156 | SoniNeko Drum Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 1380 | game |
| 157 | Super Mario Advance Soundfont V2 | OnuteWORLD Server Ltd. | musical-artifacts | CC BY 3.0 | ✓ | — | 1342 | game |
| 158 | MegaMan Battle Network 3 Soundfont | Nintenducc | musical-artifacts | CC BY 3.0 | ✓ | — | 1273 | game |
| 159 | Pana Der Hejhog Soundfont | Mildanner, MarkeyJester | musical-artifacts | CC BY 3.0 | ✓ | — | 1261 | game |
| 160 | Sonic 3 Movie Promo Cart Soundfont | Mildanner, Paramount Pictures | musical-artifacts | CC BY 3.0 | ✓ | — | 1247 | game |
| 161 | Ristar (Sega Genesis) Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 1215 | game |
| 162 | FIFA Soccer 95 Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 1200 | game |
| 163 | NBA LIVE 95 (Genesis) Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 1198 | game |
| 164 | MegaMan Battle Network 5 Soundfont | Nintenducc | musical-artifacts | CC BY 3.0 | ✓ | — | 1193 | game |
| 165 | MegaMan Battle Network 1 Soundfont | Nintenducc | musical-artifacts | CC BY 3.0 | ✓ | — | 1179 | game |
| 166 | Jump Super Stars Soundfont (UPDATE 8/16/26) | VideoGameKid | musical-artifacts | CC BY 3.0 | ✓ | — | 1126 | game |
| 167 | Betray US Chrom | Bubby293 | musical-artifacts | CC BY 3.0 | ✓ | — | 1118 | game |
| 168 | MegaMan Battle Network 4 Soundfont | Nintenducc | musical-artifacts | CC BY 3.0 | ✓ | — | 1094 | game |
| 169 | MegaMan Battle Network 2 Soundfont | Nintenducc | musical-artifacts | CC BY 3.0 | ✓ | — | 1077 | game |
| 170 | Sonic the Hedgehog - To Be A Star Soundfont | Mildanner, Katsushimi, KGL, MD | musical-artifacts | CC BY 3.0 | ✓ | — | 1068 | game |
| 171 | DOOM (32X) Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 1050 | game |
| 172 | Fullmetal Alchemist: Stray Rondo Soundfont (UPDATE 8/18/2026) | VideoGameKid | musical-artifacts | CC BY 3.0 | ✓ | — | 1043 | game |
| 173 | Mega Man Zero 1 Soundfont (1/4) (UPDATE 8/16/2026) | VideoGameKid | musical-artifacts | CC BY 3.0 | ✓ | — | 1033 | game |
| 174 | Sonic Battle (USA) Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 1008 | game |
| 175 | Sonic 2 + Knuckles Chaotix Buzzer Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 971 | game |
| 176 | Mega Man 10 Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 938 | game |
| 177 | Sonic Eraser Frying Pan Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 845 | game |
| 178 | Sega Genesis Soundfont (More Complete, I Guess) | VladTheFatman | musical-artifacts | CC BY 3.0 | ✓ | — | 839 | game |
| 179 | Thunder Force IV Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 836 | game |
| 180 | Olympic Summer Games: Atlanta '96 (SNES) Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 823 | game |
| 181 | F-Zero GP Legend & Climax Soundfont (UPDATE 8/16/26) | VideoGameKid | musical-artifacts | CC BY 3.0 | ✓ | — | 791 | game |
| 182 | Sonic ERaZor (ROM hack) Soundfont | Mildanner, Selbi, Amphobius an | musical-artifacts | CC BY 3.0 | ✓ | — | 778 | game |
| 183 | The Complete Sonic Advance 1/2/3 Soundfont Combined | Bouncy Glow's Music Room, robt | musical-artifacts | CC BY 3.0 | ✓ | — | 767 | game |
| 184 | Izzy's Quest for the Olympic Rings (SNES) | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 744 | game |
| 185 | Pinball Tycoon | MLP DJ Gamer Appledash FIM | musical-artifacts | CC BY 3.0 | ✓ | — | 740 | game |
| 186 | NEW Fist of the North Star DS Soundfont (UPDATE 5/17/2026) | VideoGameKid | musical-artifacts | CC BY 3.0 | ✓ | — | 678 | game |
| 187 | Pucca Power Up (DS) Soundfont | Athosworld | musical-artifacts | CC BY 3.0 | ✓ | — | 673 | game |
| 188 | Top Gear (SNES) Soundfont | Mildanner, Gremlin | musical-artifacts | CC BY 3.0 | ✓ | — | 654 | game |
| 189 | Simpsons, The - Bart's Nightmare (SNES) Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 642 | game |
| 190 | Genesis Sonic HQ Bass Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 620 | game |
| 191 | Dangerous Seed (Genesis) Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 619 | game |
| 192 | Ristar FM Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 597 | game |
| 193 | Sesame Street Counting Cafe Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 593 | game |
| 194 | Sonic 1 Definitive - SHC 2021 Drum Soundfont | Mildanner, Inferno, RadiantNex | musical-artifacts | CC BY 3.0 | ✓ | — | 574 | game |
| 195 | SNES FM Pick Bass DWP (Hooded Edge) | Mildanner, Hooded Edge | musical-artifacts | CC BY 3.0 | — | — | 555 | game |
| 196 | Sonic 2 ARZ Piano HQ Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 551 | game |
| 197 | Socket Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 540 | game |
| 198 | GAX Sound Engine Soundfont | Novo Lubub Music/Shin'en Multi | musical-artifacts | CC BY | ✓ | — | 534 | game |
| 199 | Battle Mania Daiginjou (Genesis) Soundfont | Mildanner, SEGA | musical-artifacts | CC BY 3.0 | ✓ | — | 517 | game |
| 200 | Top Gear 2 (Genesis) Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 472 | game |
| 201 | Nintendo Famicon Soundfont | Bernardo Jose | musical-artifacts | CC BY 3.0 | ✓ | — | 453 | game |
| 202 | The Flintstones (SNES) Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 452 | game |
| 203 | XBOX GM Soundfont | Microsoft, XXtherobloxx21 | musical-artifacts | CC BY 3.0 | ✓ | — | 440 | game |
| 204 | Sonic ERaZor - Drum Soundfont | Mildanner, Selbi, Eduardo Knuc | musical-artifacts | CC BY 3.0 | ✓ | — | 434 | game |
| 205 | Shin Megami Tensei II (SNES) soundfont | Vènatus aka YaBoiVen on youtub | musical-artifacts | CC BY 3.0 | ✓ | — | 411 | game |
| 206 | Casino Night Zone Soundfont | Sonicluver1, SEGA | musical-artifacts | CC BY 3.0 | ✓ | — | 383 | game |
| 207 | Care Bears - Care Quest (Game Boy Advance) Soundfont | Novo Lubub Music/Mildanner/The | musical-artifacts | CC BY | ✓ | — | 374 | game |
| 208 | Ristar Drum Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 373 | game |
| 209 | VAdaPEGA Logo YM2612 Horn Soundfont | Mildanner, VAdaPEGA | musical-artifacts | CC BY 3.0 | ✓ | — | 368 | game |
| 210 | Nineko Vibraphone YM2612 Soundfont | Mildanner, Nineko | musical-artifacts | CC BY 3.0 | ✓ | — | 365 | game |
| 211 | Time Trax (SNES) Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 364 | game |
| 212 | Sonic the Reborn 2025 - PCM Soundfont | Mildanner, HipSnake | musical-artifacts | CC BY 3.0 | ✓ | — | 357 | game |
| 213 | Zero the Kamikaze Sequel SNES Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 326 | game |
| 214 | The Jetzons Mini Instrument Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 323 | game |
| 215 | Iridion 3D (Game Boy Advance) GM Soundfont | Majesco Entertainment/Shin'en  | musical-artifacts | CC BY | ✓ | — | 290 | game |
| 216 | Kirby's Dream Land Soundfont Rework! | ArtifactedSonicMusical | musical-artifacts | CC BY 3.0 | ✓ | — | 270 | game |
| 217 | Coronation Day/'the Soundfont | owerkadower | musical-artifacts | CC BY 3.0 | ✓ | — | 154 | game |
| 218 | Socket (Time Dominator) - TFI Instrument Pack | Mildanner | musical-artifacts | CC BY 3.0 | — | — | 138 | game |
| 219 | Math Play | MrPropper | musical-artifacts | CC BY 3.0 | ✓ | — | 75 | game |
| 220 | BaritoneSax | sinshu | github | MIT | — | — | — | game |
| 221 | Brightness | sinshu | github | MIT | — | — | — | game |
| 222 | Plants vs. Zombies 2 Complete Soundfont Pack | Peter McConnell, sampled by Ga | musical-artifacts | CC BY 3.0 | ✓ | — | 0 | game |
| 223 | RetroNoises | TheHartCorei5 | musical-artifacts | CC BY 3.0 | — | — | 0 | game |
| 224 | Super Mario 3D Land SF2 (2025/GM Compatible!) | MasonMasterMusic | musical-artifacts | CC BY 3.0 | ✓ | — | 0 | game |
| 225 | touhou | Tseku210 | github | MIT | ✓ | — | — | game |
| 226 | Touhou Phantom Bullet | 白いチャンネル | musical-artifacts | CC BY 3.0 | ✓ | — | 0 | game |
| 227 | XXtherobloxx21s Soundfont | XXtherobloxx21 | musical-artifacts | CC BY 3.0 | ✓ | — | 0 | game |
| 228 | MuseScore_General（.sf3 压缩版） | S. Christian Collins | MuseScore | MIT | — | 38.1 MB | — | gm |
| 229 | The Ultimate Roblox Soundfont V1.7 | NotRoblox, SurelyNotRoblox, ro | musical-artifacts | CC BY 3.0 | ✓ | 79.3 MB | 3645 | gm |
| 230 | FluidR3_GM（tar.gz 同内容） | Frank Wen | MuseScore | MIT | ✓ | 124.3 MB | — | gm |
| 231 | SGM Soundfont | SonicLover 19 | musical-artifacts | CC BY 3.0 | ✓ | — | 289628 | gm |
| 232 | The Ultimate Roblox Soundfont Pack V1.8 | NotRoblox | musical-artifacts | CC BY | ✓ | — | 57041 | gm |
| 233 | Nokia S40 3rd Edition (2.04 WIP) | Zenxia | musical-artifacts | CC BY | ✓ | — | 6420 | gm |
| 234 | 3D Maze Man (1998) Soundfont | tahutoa | musical-artifacts | CC BY 3.0 | ✓ | — | 1201 | gm |
| 235 | Hpcarl Jupiter 2 | Hpcarl | musical-artifacts | CC BY | ✓ | — | 0 | gm |
| 236 | Bass | gregogiudici | github | MIT | ✓ | 2.3 MB | — | guitar |
| 237 | FDL Bass | FDLBricks | musical-artifacts | CC BY | ✓ | 3.8 MB | 576 | guitar |
| 238 | Deep Bass (based on pasta bass) | j_e_f_f_g | musical-artifacts | CC BY | — | 9.8 MB | 3411 | guitar |
| 239 | Fender Squire Bass | Bill Brown | musical-artifacts | CC BY | ✓ | — | 6209 | guitar |
| 240 | Fender Knockoff Strat | Bill Brown | musical-artifacts | CC BY | ✓ | — | 5423 | guitar |
| 241 | Buddy Holly Riff | XXtherobloxx21 | musical-artifacts | CC BY 3.0 | ✓ | — | 2324 | guitar |
| 242 | Blue Jeans And Moonbeams | Malaclypse the Younger | sfzinstruments | MIT | — | — | — | guitar |
| 243 | Kalimbass | Malaclypse the Younger | sfzinstruments | MIT | — | — | — | guitar |
| 244 | Slap Bass | gregogiudici | github | MIT | ✓ | — | — | guitar |
| 245 | RolandNicePiano | bradhowes | github | MIT | ✓ | 6.2 MB | — | hist |
| 246 | RolandNicePiano | bradhowes | github | MIT | ✓ | 6.2 MB | — | hist |
| 247 | Casio Privia PX-860 Concert Grand Piano | Casio, sampled by Caed | musical-artifacts | CC BY 3.0 | ✓ | 32.3 MB | 7846 | hist |
| 248 | The 90-2000's Famous House Kit | Aleksandr Bykov, other | musical-artifacts | CC BY 3.0 | — | 157.0 MB | 3836 | hist |
| 249 | Classic Dream House, Trance Kit | Aleksandr Bykov, other | musical-artifacts | CC BY 3.0 | — | 175.3 MB | 2556 | hist |
| 250 | Kurzweil K2000 Stereo Grand (Soundfont) | The GP | musical-artifacts | CC BY 3.0 | ✓ | — | 22903 | hist |
| 251 | Kurzweil K2000 Acous 12 Strings (Soundfont) | The GP | musical-artifacts | CC BY 3.0 | ✓ | — | 14717 | hist |
| 252 | Yamaha C3 Grand Piano | Ctech2021 | musical-artifacts | CC BY 3.0 | ✓ | — | 13227 | hist |
| 253 | Live HQ Natural SoundFont GM V3.0 | UnderxPipe1985 | musical-artifacts | CC BY | — | — | 12693 | hist |
| 254 | St. GIGA's HQ FM General MIDI Set | stgiga/stgiga | musical-artifacts | CC BY | ✓ | — | 12031 | hist |
| 255 | Kurzweil K2000 Steel String Guitar (Soundfont) | The GP | musical-artifacts | CC BY 3.0 | ✓ | — | 12020 | hist |
| 256 | Roland MV-30 (SC-55 Version) | MAG2001 | musical-artifacts | CC BY 3.0 | ✓ | — | 9291 | hist |
| 257 | YAMAHA SHS-10 + YM2413 (GM mapped) | stgiga, NESMaster96, little-sc | musical-artifacts | CC BY 3.0 | ✓ | — | 8663 | hist |
| 258 | E3Kay's Roland Juno-60 Soundfont v2.0 | E3Kay | musical-artifacts | CC BY 3.0 | ✓ | — | 8556 | hist |
| 259 | Kurzweil K2000 Brite Piano (Soundfont) | The GP | musical-artifacts | CC BY 3.0 | ✓ | — | 8432 | hist |
| 260 | FPD98 | Dekyo Ongen | musical-artifacts | CC BY | ✓ | — | 7686 | hist |
| 261 | Chaos V20 Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 6327 | hist |
| 262 | Kurzweil K2000 Tine Elec Piano (673Mb Soundfont) | The GP | musical-artifacts | CC BY 3.0 | ✓ | — | 5885 | hist |
| 263 | Yamaha MA2 fm soundfont | Yamaha | musical-artifacts | CC BY 3.0 | ✓ | — | 4926 | hist |
| 264 | Reality GM/GS FalcoMod | FalcoMod | musical-artifacts | CC BY 3.0 | ✓ | — | 4732 | hist |
| 265 | Kurzweil K2000 All In The Fader (704Mb Soundfont) | The GP | musical-artifacts | CC BY 3.0 | — | — | 4530 | hist |
| 266 | Caed’s Trash GMGS Version 1.1 | Caed | musical-artifacts | CC BY 3.0 | ✓ | — | 4440 | hist |
| 267 | Kurzweil K2000 Dual Elec Piano (Rhodes 680Mb Soundfont) | The GP | musical-artifacts | CC BY 3.0 | — | — | 4360 | hist |
| 268 | - | eeeeeeee | musical-artifacts | CC BY 3.0 | ✓ | — | 3458 | hist |
| 269 | YAMAHA SHS-10 + YM2413 (GM mapped Redesigned) | stgiga, NESMaster96, little-sc | musical-artifacts | CC BY 3.0 | ✓ | — | 3264 | hist |
| 270 | YM2612 SMPS Brass Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 3044 | hist |
| 271 | 91 Slow Chorus Guitar | Username_Tony | musical-artifacts | CC BY 3.0 | ✓ | — | 2351 | hist |
| 272 | E3Kay's Roland Juno-60 Soundfont | E3Kay | musical-artifacts | CC BY 3.0 | ✓ | — | 1962 | hist |
| 273 | Ensoniq ESQ-1 Fantabell | Ensoniq | musical-artifacts | CC BY | ✓ | — | 1874 | hist |
| 274 | Korg M1 HipHop Bass Soundfont | Mildanner, KORG | musical-artifacts | CC BY 3.0 | ✓ | — | 1353 | hist |
| 275 | Korg Triton Sax Ensemble Soundfont | Mildanner, KORG | musical-artifacts | CC BY 3.0 | ✓ | — | 1260 | hist |
| 276 | Korg Triton 30303 Mega Bass Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 1242 | hist |
| 277 | Korg Triton Acoustic Piano Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 1232 | hist |
| 278 | Caed’s Trash GMGS Version 1 | Caed | musical-artifacts | CC BY 3.0 | — | — | 1165 | hist |
| 279 | Korg Triton Strings Ensemble Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 1070 | hist |
| 280 | Korg Triton Euro 8va Bass Soundfont | Mildanner, KORG | musical-artifacts | CC BY 3.0 | ✓ | — | 1001 | hist |
| 281 | Korg Triton Spiky & Tight Instrument Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 601 | hist |
| 282 | Robotnik's theme (AoSTH) synth soundfont | CloudyJolt | musical-artifacts | CC BY 3.0 | ✓ | — | 439 | hist |
| 283 | Korg Triton Rock Organ Soundfont | Mildanner, KORG | musical-artifacts | CC BY 3.0 | ✓ | — | 402 | hist |
| 284 | XXtherob-malik-dan GM 2.0 | XXtherobloxx21, CupheadKrasueH | musical-artifacts | CC BY | ✓ | — | 179 | hist |
| 285 | Roland Disney Soundfont | XXtherobloxx21, Disney | musical-artifacts | CC BY 3.0 | — | — | 0 | hist |
| 286 | The 90's Dreams II (599Mb Soundfont Collection) | Aleksandr Bykov, The GP and ot | musical-artifacts | CC BY 3.0 | — | — | 0 | hist |
| 287 | harmonium | ledlaux | github | MIT | ✓ | 6.3 MB | — | orch |
| 288 | Ixox Flute | Xavier Hosxe | sfzinstruments | CC BY 4.0 | — | 10.7 MB | — | orch |
| 289 | MTG Solo Sax | Music Technology Group (MTG) | sfzinstruments | CC BY 4.0 | — | 110.0 MB | — | orch |
| 290 | Musescore General HQ Soundfont (.sf2 Converted) | Frank Wen, Michael Cowgill, S. | musical-artifacts | CC BY 3.0 | ✓ | — | 21853 | orch |
| 291 | Tin Whistle | misc | musical-artifacts | CC BY | ✓ | — | 3599 | orch |
| 292 | Mellotron 02 Soundfont | Mildanner, Image-Line | musical-artifacts | CC BY 3.0 | ✓ | — | 1391 | orch |
| 293 | Beakman Orchestral Hit Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 444 | orch |
| 294 | Brass1 | sinshu | github | MIT | — | — | — | orch |
| 295 | Cello | sinshu | github | MIT | — | — | — | orch |
| 296 | EnglishHorn | sinshu | github | MIT | — | — | — | orch |
| 297 | Flute | sinshu | github | MIT | — | — | — | orch |
| 298 | FrenchHorns | sinshu | github | MIT | — | — | — | orch |
| 299 | MuteTrumpet | sinshu | github | MIT | — | — | — | orch |
| 300 | Oboe | sinshu | github | MIT | — | — | — | orch |
| 301 | Orchestra | sinshu | github | MIT | — | — | — | orch |
| 302 | OrchestraHit | sinshu | github | MIT | — | — | — | orch |
| 303 | PanFlute | sinshu | github | MIT | — | — | — | orch |
| 304 | Party Pipes | Malaclypse the Younger | sfzinstruments | MIT | — | — | — | orch |
| 305 | SlowStrings | sinshu | github | MIT | — | — | — | orch |
| 306 | Strings | sinshu | github | MIT | — | — | — | orch |
| 307 | SynthBrass1 | sinshu | github | MIT | — | — | — | orch |
| 308 | SynthBrass2 | sinshu | github | MIT | — | — | — | orch |
| 309 | SynthStrings1 | sinshu | github | MIT | — | — | — | orch |
| 310 | SynthStrings2 | sinshu | github | MIT | — | — | — | orch |
| 311 | Trumpet | sinshu | github | MIT | — | — | — | orch |
| 312 | Violin | sinshu | github | MIT | — | — | — | orch |
| 313 | Gordon’s Whistle | Gabriel Ferrante | musical-artifacts | CC BY 3.0 | — | 0.3 MB | 329 | other |
| 314 | Beatnik Mobile Banks (SF2) | Beatnik Inc. | musical-artifacts | CC BY 3.0 | ✓ | 0.6 MB | 4070 | other |
| 315 | Rhodes | gregogiudici | github | MIT | ✓ | 0.8 MB | — | other |
| 316 | Square | gregogiudici | github | MIT | ✓ | 0.8 MB | — | other |
| 317 | FreeFont | bradhowes | github | MIT | ✓ | 3.1 MB | — | other |
| 318 | FreeFont | bradhowes | github | MIT | ✓ | 3.1 MB | — | other |
| 319 | scc1t2 | misterhat | github | MIT | ✓ | 3.1 MB | — | other |
| 320 | Saw | gregogiudici | github | MIT | ✓ | 3.2 MB | — | other |
| 321 | default | yakari | github | MIT | ✓ | 5.7 MB | — | other |
| 322 | Pulse | gregogiudici | github | MIT | ✓ | 7.4 MB | — | other |
| 323 | SuperSponge (PSX) Soundfont | tahutoa | musical-artifacts | CC BY 3.0 | — | 9.5 MB | 1908 | other |
| 324 | The King of Fighters 2002: Challenge to Ultimate Battle Soundfont (UPD | VideoGameKid (Originally rippe | musical-artifacts | CC BY 3.0 | ✓ | 13.8 MB | 1303 | other |
| 325 | SONiVOX EAS GM Wavetable 12 Variants | Sonic Network Inc. | musical-artifacts | CC BY 3.0 | ✓ | 17.8 MB | 6361 | other |
| 326 | GeneralUser GS MuseScore v1.442 | bradhowes | github | MIT | ✓ | 29.8 MB | — | other |
| 327 | Proteus | Proteus | musical-artifacts | CC BY | ✓ | 34.8 MB | 20017 | other |
| 328 | Pizza Tower Soundfont | XXtherobloxx21, PeterGriffin10 | musical-artifacts | CC BY | — | 37.3 MB | 4734 | other |
| 329 | WOTJA X | Intermorphic | musical-artifacts | CC BY | ✓ | 37.4 MB | 1639 | other |
| 330 | Synth Pack 1 | Joshua R (Soundfont Collector) | musical-artifacts | CC BY | ✓ | 51.8 MB | 7510 | other |
| 331 | Sci-Fi & Supernatural | Joshua R (Soundfont Collector) | musical-artifacts | CC BY | ✓ | 60.1 MB | 9815 | other |
| 332 | PerfectPiano Soundfont Instrument Package | Mildanner, Revontulet Soft | musical-artifacts | CC BY 3.0 | — | 98.1 MB | 2576 | other |
| 333 | Synth Pack 2 | Joshua R (Soundfont Collector) | musical-artifacts | CC BY | ✓ | 122.5 MB | 7178 | other |
| 334 | OnuteFont | OnuteWORLD Server Ltd. | musical-artifacts | CC BY 3.0 | ✓ | 164.4 MB | 7896 | other |
| 335 | Beats CodeNameHippie Collection | Motionwave (MW) | musical-artifacts | CC BY 3.0 | ✓ | 209.1 MB | 1348 | other |
| 336 | Amen Break Soundfont | ASmolBoy, VEXST | musical-artifacts | CC BY 3.0 | ✓ | — | 22647 | other |
| 337 | Samsung Ch@t 222 (GT-E2220) Soundfont (122MB + 120KB) | Sonic Network Inc. | musical-artifacts | CC BY 3.0 | ✓ | — | 9923 | other |
| 338 | Concert Harp Soundfont (from Sonatina sfz) | Fernando A. Martin | musical-artifacts | CC BY | ✓ | — | 9178 | other |
| 339 | Metal Slug (Direct Sampling) | Josh R. | musical-artifacts | CC BY | ✓ | — | 7225 | other |
| 340 | E3Kay's Fairlight CMI Collection v2.0 | E3Kay, stgiga | musical-artifacts | CC BY 3.0 | ✓ | — | 6253 | other |
| 341 | General User GS! | SpessaSus and XXtherobloxx21 | musical-artifacts | CC BY 3.0 | ✓ | — | 6117 | other |
| 342 | Styx Soundfont v1.1 | Arsi | musical-artifacts | CC BY | ✓ | — | 5543 | other |
| 343 | Sinfon36Plus.sf2 | Anugrah Pratama | musical-artifacts | CC BY 3.0 | ✓ | — | 4823 | other |
| 344 | LG G5400 SoundFont (aka Casio Mobile, OKI ML2870) | © OKI, Casio, 2003; | musical-artifacts | CC BY 3.0 | ✓ | — | 4205 | other |
| 345 | Damn daniel soundfont (sf2) | weggyisawesome | musical-artifacts | CC BY 3.0 | ✓ | — | 3772 | other |
| 346 | GeneralUser GS Live-Audigy v1.44_custom Soundfont | Unknown | musical-artifacts | CC BY 3.0 | ✓ | — | 3595 | other |
| 347 | Super Smash Flash 2 - Mr. Saturn SFX Soundfont | Mildanner, McLeodGaming | musical-artifacts | CC BY 3.0 | ✓ | — | 3485 | other |
| 348 | Leapster | iusmaker777 | musical-artifacts | CC BY 3.0 | ✓ | — | 3424 | other |
| 349 | Female Vocalizer | Bubby293 | musical-artifacts | CC BY 3.0 | ✓ | — | 3365 | other |
| 350 | Amiga 5S - SF2 | ThatOneWiiMattFan | musical-artifacts | CC BY 3.0 | ✓ | — | 3114 | other |
| 351 | Just Shapes and Beats Inspired Soundfont | XXtherobloxx21, Berzerk Studio | musical-artifacts | CC BY 3.0 | ✓ | — | 3069 | other |
| 352 | SONiVOX EAS GM Wavetable | Anugrah Pratama | musical-artifacts | CC BY 3.0 | ✓ | — | 2963 | other |
| 353 | Yee Soundfonts | M. Reza Khadafi | musical-artifacts | CC BY | ✓ | — | 2783 | other |
| 354 | LG B2000 SoundFont (aka Casio Mobile, OKI ML2871) | © OKI, Casio, 2003; | musical-artifacts | CC BY 3.0 | ✓ | — | 2681 | other |
| 355 | WalkBand Default Instruments Soundfont | Mildanner, Revontulet Soft, Ma | musical-artifacts | CC BY 3.0 | ✓ | — | 2680 | other |
| 356 | Macintosh Startup Soundfont | Polter | musical-artifacts | CC BY 3.0 | ✓ | — | 2355 | other |
| 357 | E3Kay's Fairlight CMI Collection | E3Kay | musical-artifacts | CC BY 3.0 | ✓ | — | 2135 | other |
| 358 | PhoeniXG v2.1 | Jexu | musical-artifacts | CC BY 3.0 | ✓ | — | 2103 | other |
| 359 | yamaha combo organ soundfont | TheSoundfontMaker | musical-artifacts | CC BY 3.0 | — | — | 2102 | other |
| 360 | Scratch 2.0 Alpha Soundfont (2010-2011) | OnuteWORLD Server Ltd. | musical-artifacts | CC BY 3.0 | ✓ | — | 1837 | other |
| 361 | bell soundfont | TheSoundfontMaker | musical-artifacts | CC BY 3.0 | — | — | 1742 | other |
| 362 | Macintosh Startup Soundfont 2.0 | N.Z | musical-artifacts | CC BY 3.0 | ✓ | — | 1697 | other |
| 363 | Ba Soundfont 2017 | M. Reza Khadafi | musical-artifacts | CC BY | ✓ | — | 1469 | other |
| 364 | 42 All-Time Classics/Clubhouse Games (DS) Soundfont | tahutoa | musical-artifacts | CC BY 3.0 | ✓ | — | 1160 | other |
| 365 | LG G5400 SoundFont Samples | © OKI, Casio, 2003; | musical-artifacts | CC BY 3.0 | — | — | 1134 | other |
| 366 | Discord Stage Music Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 1125 | other |
| 367 | Aria Math Hand Pan Soundfont | Bryson Lemere | musical-artifacts | CC BY 3.0 | ✓ | — | 1119 | other |
| 368 | The Wav Soundfont | Bubby293 | musical-artifacts | CC BY 3.0 | ✓ | — | 1111 | other |
| 369 | The Ultimate (american) DTMF Soundfont | sylavenn | musical-artifacts | CC BY 3.0 | ✓ | — | 1107 | other |
| 370 | Caed's Small Trash GM v1.06 | Caed | musical-artifacts | CC BY 3.0 | ✓ | — | 1103 | other |
| 371 | Discord Keyboard Combo Soundfont | Mildanner, Discord | musical-artifacts | CC BY 3.0 | ✓ | — | 1094 | other |
| 372 | New Face Trumpet (PSY) Soundfont | Mason (2022) | musical-artifacts | CC BY | ✓ | — | 1040 | other |
| 373 | Voxatron SF2 | BarOS | musical-artifacts | CC BY 3.0 | ✓ | — | 914 | other |
| 374 | Instagram Piano Ringtone Soundfont | Mildanner, Meta | musical-artifacts | CC BY 3.0 | ✓ | — | 895 | other |
| 375 | Scratch Video Game Loop Soundfont | Mildanner, Scratch Team | musical-artifacts | CC BY 3.0 | ✓ | — | 884 | other |
| 376 | Buh bah dahdah Sounfont | Bubby293 | musical-artifacts | CC BY 3.0 | ✓ | — | 866 | other |
| 377 | Boeing 737 Soundfont | a human | musical-artifacts | CC BY 3.0 | ✓ | — | 840 | other |
| 378 | Fire Emblem 4 Soundfont Concept | Mahmoud Ehab | musical-artifacts | CC BY 3.0 | ✓ | — | 805 | other |
| 379 | YouTube Microphone Search Soundfont | Mildanner, Google LLC | musical-artifacts | CC BY 3.0 | ✓ | — | 768 | other |
| 380 | Jeffersonbi's chromatics scale | Bubby293 | musical-artifacts | CC BY 3.0 | ✓ | — | 762 | other |
| 381 | Discord Snake 404 Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 695 | other |
| 382 | RAW Buzzer SB2 Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 672 | other |
| 383 | Doodle Suno Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 628 | other |
| 384 | Discord Main Synths (FIXED) Soundfont | Mildanner, Tarty9810 | musical-artifacts | CC BY 3.0 | ✓ | — | 619 | other |
| 385 | Xpand!2 Basic Square Lead Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 524 | other |
| 386 | Madagascar (2005) DS/GBA HD Soundfont (Incomplete) | Nicolas Soliz-12 | musical-artifacts | CC BY 3.0 | ✓ | — | 441 | other |
| 387 | Game Creator Soundfont | PikaNoob | musical-artifacts | CC BY 3.0 | ✓ | — | 406 | other |
| 388 | LMMS TripleOscillator Mini Custom Instrument Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 392 | other |
| 389 | Opera GX Ad Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 384 | other |
| 390 | MidiTrail iOS Soundfont lookalike (Wasteyarded) | MidiTrail, XXtherobloxx21 | musical-artifacts | CC BY 3.0 | ✓ | — | 361 | other |
| 391 | Discord Halloween 2022 Soundfont | Mildanner, Discord | musical-artifacts | CC BY 3.0 | ✓ | — | 355 | other |
| 392 | 99 Food Ad Soundfont | Mildanner, 99 | musical-artifacts | CC BY 3.0 | ✓ | — | 353 | other |
| 393 | Harry Styles - As It Was Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 335 | other |
| 394 | Amazon Ad Promotion Soundfont | Mildanner, Amazon | musical-artifacts | CC BY 3.0 | ✓ | — | 287 | other |
| 395 | MagicSF (Soundfont) Jampea | Jampea | musical-artifacts | CC BY 3.0 | ✓ | — | 259 | other |
| 396 | Keeta Ad Soundfont | Mildanner, Keeta | musical-artifacts | CC BY 3.0 | ✓ | — | 235 | other |
| 397 | Stoat Notification Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 196 | other |
| 398 | (Unfinished) Waveworld Soundfont | Linksab | musical-artifacts | CC BY 3.0 | — | — | 188 | other |
| 399 | Beeper | gregogiudici | github | MIT | ✓ | — | — | other |
| 400 | loopool - LFRP Soundfont Bundle sf2. | loopool / Jean-Paul Garnier | archive | CC BY 3.0 | — | — | — | other |
| 401 | Pocoyo Soundfont | MasonMasterMusic | musical-artifacts | CC BY 3.0 | ✓ | — | 0 | other |
| 402 | Scrimblo Bimblo's Scrunky Adventure Soundfont | Aquacycle | musical-artifacts | CC BY 3.0 | ✓ | — | 0 | other |
| 403 | soundfont | markus tornow | archive | CC BY 4.0 | — | — | — | other |
| 404 | Theremin | gregogiudici | github | MIT | ✓ | — | — | other |
| 405 | Time Gear - PMD2 Moonbase Alpha - Microsoft Sam (Bah) Soundfont Cover | Ben K. | archive | CC BY 3.0 | — | — | — | other |
| 406 | Trombone | gregogiudici | github | MIT | ✓ | — | — | other |
| 407 | what a mario world Overworld (Super Mario Advance Soundfont) | Yodel Boi | archive | CC BY 4.0 | — | — | — | other |
| 408 | ZZZ1 | bradhowes | github | MIT | ✓ | — | — | other |
| 409 | ZZZ2 | bradhowes | github | MIT | ✓ | — | — | other |
| 410 | nylon_guitar | constcut | github | MIT | ✓ | 0.1 MB | — | piano |
| 411 | guitar | constcut | github | MIT | ✓ | 0.2 MB | — | piano |
| 412 | eguitar | constcut | github | MIT | ✓ | 0.4 MB | — | piano |
| 413 | piano | constcut | github | MIT | ✓ | 0.6 MB | — | piano |
| 414 | drums | constcut | github | MIT | ✓ | 0.7 MB | — | piano |
| 415 | Tiny piano (ogg version) | Signal Experiments | musical-artifacts | CC BY | — | 2.1 MB | 2448 | piano |
| 416 | fullset | constcut | github | MIT | ✓ | 5.7 MB | — | piano |
| 417 | Tiny Piano 00 (SFZ) | Signal Experiments | musical-artifacts | CC BY | — | 7.2 MB | 1765 | piano |
| 418 | UprightPianoKW-small-20190703 | AnonN10 | github | MIT | ✓ | 9.0 MB | — | piano |
| 419 | Greg Sullivan E-Pianos | Greg Sullivan | sfzinstruments | CC BY 3.0 | — | 21.5 MB | — | piano |
| 420 | Piano | gregogiudici | github | MIT | ✓ | 22.0 MB | — | piano |
| 421 | GeneralUser-GS | patakuti | github | MIT | ✓ | 30.8 MB | — | piano |
| 422 | GeneralUserGS | isssifre-arch | github | MIT | ✓ | 30.8 MB | — | piano |
| 423 | floppy disk soundfont V2 | TheSoundfontMaker | musical-artifacts | CC BY 3.0 | — | 33.6 MB | 1541 | piano |
| 424 | YDP Grand Piano | FreePats project | FreePats | CC BY 3.0 | ✓ | 36.0 MB | — | piano |
| 425 | Equinox_Grand_Pianos | SpaceShaman | github | MIT | ✓ | 91.7 MB | — | piano |
| 426 | FluidR3_GM | Frank Wen | MuseScore | MIT | ✓ | 125.7 MB | — | piano |
| 427 | Headroom Piano | Bengt Nilsson | sfzinstruments | CC BY 4.0 | — | 156.2 MB | — | piano |
| 428 | MuseScore_General | S. Christian Collins（改编自 Fluid | MuseScore | MIT | ✓ | 205.6 MB | — | piano |
| 429 | Salamander Grand Piano | FreePats project | FreePats | CC BY 3.0 | ✓ | 296.0 MB | — | piano |
| 430 | Salamander Grand Piano | Alexander Holm | sfzinstruments | CC BY 3.0 | — | 394.0 MB | — | piano |
| 431 | Accurate-Salamander Project | Chisato Yamauchi | sfzinstruments | CC BY | — | 1638.4 MB | — | piano |
| 432 | Alex's gm soundfont version 1.3 | High quality sfs | musical-artifacts | CC BY 3.0 | ✓ | — | 69780 | piano |
| 433 | S90ES | Henrique Gogó | musical-artifacts | CC BY 3.0 | ✓ | — | 27220 | piano |
| 434 | Real Honky tonk piano by Milton Paredes | Milton Paredes, mpj factory st | musical-artifacts | CC BY | ✓ | — | 10965 | piano |
| 435 | [DEPRECATED] NeoVST Piano One (sf2 version) | Exthayan | musical-artifacts | CC BY 3.0 | ✓ | — | 7128 | piano |
| 436 | Yamaha YPT 220 soundfont studio version | TheSoundfontMaker | musical-artifacts | CC BY 3.0 | ✓ | — | 6287 | piano |
| 437 | Piano Sample Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 2050 | piano |
| 438 | WalkBand Complete Drum Soundfont | Mildanner, WalkBand, Revontule | musical-artifacts | CC BY 3.0 | ✓ | — | 1890 | piano |
| 439 | Clav | sinshu | github | MIT | — | — | — | piano |
| 440 | Electric Piano | gregogiudici | github | MIT | ✓ | — | — | piano |
| 441 | ElectricPiano1 | sinshu | github | MIT | — | — | — | piano |
| 442 | ElectricPiano2 | sinshu | github | MIT | — | — | — | piano |
| 443 | epiano | constcut | github | MIT | ✓ | — | — | piano |
| 444 | Piano1 | sinshu | github | MIT | — | — | — | piano |
| 445 | Piano2 | sinshu | github | MIT | — | — | — | piano |
| 446 | Piano3 | sinshu | github | MIT | — | — | — | piano |
| 447 | TX Brass | AudioKit | github | MIT | — | — | — | piano |
| 448 | TX LoTine81z | AudioKit | github | MIT | — | — | — | piano |
| 449 | TX Metalimba | AudioKit | github | MIT | — | — | — | piano |
| 450 | TX Pluck Bass | AudioKit | github | MIT | — | — | — | piano |
| 451 | unbolted_min | io7m-com | github | ISC | ✓ | 0.3 MB | — | sfx |
| 452 | Árvore Leitor SFX Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 557 | sfx |
| 453 | complex0 | io7m-com | github | ISC | ✓ | — | — | sfx |
| 454 | empty | io7m-com | github | ISC | ✓ | — | — | sfx |
| 455 | inst1 | io7m-com | github | ISC | ✓ | — | — | sfx |
| 456 | inst1_with_modulator | io7m-com | github | ISC | ✓ | — | — | sfx |
| 457 | preset1 | io7m-com | github | ISC | ✓ | — | — | sfx |
| 458 | preset1_with_modulator | io7m-com | github | ISC | ✓ | — | — | sfx |
| 459 | sample0 | io7m-com | github | ISC | ✓ | — | — | sfx |
| 460 | Classic House Organ 2 Bass | Aleksandr Bykov | musical-artifacts | CC BY 3.0 | ✓ | 0.3 MB | 4862 | synth |
| 461 | florestan-subset | schellingb | github | MIT | ✓ | 0.5 MB | — | synth |
| 462 | Synth | gregogiudici | github | MIT | ✓ | 0.6 MB | — | synth |
| 463 | 2MBGMGS | copych | github | MIT | ✓ | 2.0 MB | — | synth |
| 464 | Various synths | SpaceShaman | github | MIT | ✓ | 2.2 MB | — | synth |
| 465 | Papelmedia_Irina_Brochin | SpaceShaman | github | MIT | ✓ | 4.8 MB | — | synth |
| 466 | Electric Keys | SpaceShaman | github | MIT | ✓ | 14.2 MB | — | synth |
| 467 | FluidR3Mono_GM | atsushieno | github | MIT | — | 22.5 MB | — | synth |
| 468 | RCKTNEO SND316X soundfont (version 3.0, GM compatible, feel free to re | RCKTNEO | musical-artifacts | CC BY | ✓ | — | 7700 | synth |
| 469 | GM Soundtrack Pad Recreation | Darko747 | musical-artifacts | CC BY 3.0 | ✓ | — | 3296 | synth |
| 470 | Mauifm | N/A | musical-artifacts | CC BY 3.0 | ✓ | — | 2887 | synth |
| 471 | MediaTek GM Synth [Nokia 108 Profile] "BASS" | DERFJECK | musical-artifacts | CC BY | ✓ | — | 2422 | synth |
| 472 | Bass Meme Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 2163 | synth |
| 473 | SNES FM Pick Bass Soundfont (Hooded Edge) | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 498 | synth |
| 474 | 5thSawWave | sinshu | github | MIT | — | — | — | synth |
| 475 | Accordion | sinshu | github | MIT | — | — | — | synth |
| 476 | AcousticBass | sinshu | github | MIT | — | — | — | synth |
| 477 | Agogo | sinshu | github | MIT | — | — | — | synth |
| 478 | AltoSax | sinshu | github | MIT | — | — | — | synth |
| 479 | Applause | sinshu | github | MIT | — | — | — | synth |
| 480 | Atmosphere | sinshu | github | MIT | — | — | — | synth |
| 481 | Bandoneon | sinshu | github | MIT | — | — | — | synth |
| 482 | BassLead | sinshu | github | MIT | — | — | — | synth |
| 483 | Bassoon | sinshu | github | MIT | — | — | — | synth |
| 484 | Bird | sinshu | github | MIT | — | — | — | synth |
| 485 | BottleBlow | sinshu | github | MIT | — | — | — | synth |
| 486 | BowedGlass | sinshu | github | MIT | — | — | — | synth |
| 487 | BreathNoise | sinshu | github | MIT | — | — | — | synth |
| 488 | Brush | sinshu | github | MIT | — | — | — | synth |
| 489 | Celesta | sinshu | github | MIT | — | — | — | synth |
| 490 | Charang | sinshu | github | MIT | — | — | — | synth |
| 491 | ChifferLead | sinshu | github | MIT | — | — | — | synth |
| 492 | ChoirAahs | sinshu | github | MIT | — | — | — | synth |
| 493 | ChurchOrgan1 | sinshu | github | MIT | — | — | — | synth |
| 494 | Clarinet | sinshu | github | MIT | — | — | — | synth |
| 495 | CleanGtr | sinshu | github | MIT | — | — | — | synth |
| 496 | Contrabass | sinshu | github | MIT | — | — | — | synth |
| 497 | Crystal | sinshu | github | MIT | — | — | — | synth |
| 498 | DistortionGtr | sinshu | github | MIT | — | — | — | synth |
| 499 | EchoDrops | sinshu | github | MIT | — | — | — | synth |
| 500 | Electronic | sinshu | github | MIT | — | — | — | synth |
| 501 | Fantasia | sinshu | github | MIT | — | — | — | synth |
| 502 | Fiddle | sinshu | github | MIT | — | — | — | synth |
| 503 | FingerBass | sinshu | github | MIT | — | — | — | synth |
| 504 | FretlessBass | sinshu | github | MIT | — | — | — | synth |
| 505 | Glockenspiel | sinshu | github | MIT | — | — | — | synth |
| 506 | Goblin | sinshu | github | MIT | — | — | — | synth |
| 507 | GtFretNoise | sinshu | github | MIT | — | — | — | synth |
| 508 | Gunshot | sinshu | github | MIT | — | — | — | synth |
| 509 | HaloPad | sinshu | github | MIT | — | — | — | synth |
| 510 | Harmonica | sinshu | github | MIT | — | — | — | synth |
| 511 | HarmonicGtr | sinshu | github | MIT | — | — | — | synth |
| 512 | Harp | sinshu | github | MIT | — | — | — | synth |
| 513 | Harpsichord | sinshu | github | MIT | — | — | — | synth |
| 514 | Helicopter | sinshu | github | MIT | — | — | — | synth |
| 515 | Honkytonk | sinshu | github | MIT | — | — | — | synth |
| 516 | IceRain | sinshu | github | MIT | — | — | — | synth |
| 517 | Jazz | sinshu | github | MIT | — | — | — | synth |
| 518 | JazzGtr | sinshu | github | MIT | — | — | — | synth |
| 519 | Marimba | sinshu | github | MIT | — | — | — | synth |
| 520 | Mellopad | gregogiudici | github | MIT | ✓ | — | — | synth |
| 521 | MeloTom1 | sinshu | github | MIT | — | — | — | synth |
| 522 | MetalPad | sinshu | github | MIT | — | — | — | synth |
| 523 | MusicBox | sinshu | github | MIT | — | — | — | synth |
| 524 | MuteGtr | sinshu | github | MIT | — | — | — | synth |
| 525 | NylonGtr | sinshu | github | MIT | — | — | — | synth |
| 526 | Ocarina | sinshu | github | MIT | — | — | — | synth |
| 527 | Organ1 | sinshu | github | MIT | — | — | — | synth |
| 528 | Organ2 | sinshu | github | MIT | — | — | — | synth |
| 529 | Organ3 | sinshu | github | MIT | — | — | — | synth |
| 530 | OverdriveGtr | sinshu | github | MIT | — | — | — | synth |
| 531 | Piccolo | sinshu | github | MIT | — | — | — | synth |
| 532 | PickedBass | sinshu | github | MIT | — | — | — | synth |
| 533 | PizzicatoStr | sinshu | github | MIT | — | — | — | synth |
| 534 | Polysynth | sinshu | github | MIT | — | — | — | synth |
| 535 | Power | sinshu | github | MIT | — | — | — | synth |
| 536 | Recorder | sinshu | github | MIT | — | — | — | synth |
| 537 | ReedOrgan | sinshu | github | MIT | — | — | — | synth |
| 538 | ReverseCym | sinshu | github | MIT | — | — | — | synth |
| 539 | Room | sinshu | github | MIT | — | — | — | synth |
| 540 | Santur | sinshu | github | MIT | — | — | — | synth |
| 541 | Sawtooth Pad | gregogiudici | github | MIT | ✓ | — | — | synth |
| 542 | SawWave | sinshu | github | MIT | — | — | — | synth |
| 543 | Seashore | sinshu | github | MIT | — | — | — | synth |
| 544 | SFX | sinshu | github | MIT | — | — | — | synth |
| 545 | Shanai | sinshu | github | MIT | — | — | — | synth |
| 546 | SlapBass1 | sinshu | github | MIT | — | — | — | synth |
| 547 | SlapBass2 | sinshu | github | MIT | — | — | — | synth |
| 548 | SoloVox | sinshu | github | MIT | — | — | — | synth |
| 549 | SopranoSax | sinshu | github | MIT | — | — | — | synth |
| 550 | Soundfont - FluidR3 GM (20011225) | newzik | github | MIT | ✓ | — | — | synth |
| 551 | Soundtrack | sinshu | github | MIT | — | — | — | synth |
| 552 | SpaceVoice | sinshu | github | MIT | — | — | — | synth |
| 553 | SquareWave | sinshu | github | MIT | — | — | — | synth |
| 554 | Standard | sinshu | github | MIT | — | — | — | synth |
| 555 | StarTheme | sinshu | github | MIT | — | — | — | synth |
| 556 | SteelGtr | sinshu | github | MIT | — | — | — | synth |
| 557 | SuperSmallFont | Wh1teDuke | github | MIT | ✓ | — | — | synth |
| 558 | SweepPad | sinshu | github | MIT | — | — | — | synth |
| 559 | SynthBass1 | sinshu | github | MIT | — | — | — | synth |
| 560 | SynthBass2 | sinshu | github | MIT | — | — | — | synth |
| 561 | SynthCalliope | sinshu | github | MIT | — | — | — | synth |
| 562 | SynthVox | sinshu | github | MIT | — | — | — | synth |
| 563 | Taiko | sinshu | github | MIT | — | — | — | synth |
| 564 | Telephone1 | sinshu | github | MIT | — | — | — | synth |
| 565 | TenorSax | sinshu | github | MIT | — | — | — | synth |
| 566 | Timpani | sinshu | github | MIT | — | — | — | synth |
| 567 | TinkleBell | sinshu | github | MIT | — | — | — | synth |
| 568 | Tofurkey | Malaclypse the Younger | sfzinstruments | MIT | — | — | — | synth |
| 569 | TR-808 | sinshu | github | MIT | — | — | — | synth |
| 570 | TremoloStr | sinshu | github | MIT | — | — | — | synth |
| 571 | Trombone | sinshu | github | MIT | — | — | — | synth |
| 572 | Tuba | sinshu | github | MIT | — | — | — | synth |
| 573 | TubularBell | sinshu | github | MIT | — | — | — | synth |
| 574 | Vibraphone | sinshu | github | MIT | — | — | — | synth |
| 575 | Viola | sinshu | github | MIT | — | — | — | synth |
| 576 | VoiceOohs | sinshu | github | MIT | — | — | — | synth |
| 577 | WarmPad | sinshu | github | MIT | — | — | — | synth |
| 578 | Whistle | sinshu | github | MIT | — | — | — | synth |
| 579 | Woodblock | sinshu | github | MIT | — | — | — | synth |
| 580 | Xylophone | sinshu | github | MIT | — | — | — | synth |
| 581 | Oohs | gregogiudici | github | MIT | ✓ | 0.1 MB | — | vocal |
| 582 | KBH Real and Swelling Choirs | lfz | musical-artifacts | CC BY | ✓ | — | 37872 | vocal |
| 583 | Discord Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 3140 | vocal |
| 584 | Sampled Choir Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 1540 | vocal |
| 585 | The Choral Soundfont Pack Freemium | Rick Blues from RE MEDIA PRODU | musical-artifacts | CC BY 3.0 | ✓ | — | 0 | vocal |
| 586 | Clarinet | gregogiudici | github | MIT | ✓ | 0.1 MB | — | wind |
| 587 | Tenor Saxophone | gregogiudici | github | MIT | ✓ | 0.3 MB | — | wind |
| 588 | harmonica soundfont | TheSoundfontMaker | musical-artifacts | CC BY 3.0 | — | — | 4936 | wind |
| 589 | Harmonica | gregogiudici | github | MIT | ✓ | — | — | wind |

## 六、F3 · 相同方式共享（有传染性：CC BY-SA / GPL） · 全量 57 条

> 本档**逐条列明**：名称 / 作者 / 来源 / 许可 / 是否 `.sf2` / 体积 / 下载量 / 分类。

| # | 名称 | 作者 | 来源 | 许可 | .sf2 | 体积 | 下载 | 分类 |
|---:|---|---|---|---|---:|---|---:|---|
| 1 | BJDNielPercussions | Yi Yunseok | sfzinstruments | CC BY-SA 4.0 | — | 4.2 MB | — | drum |
| 2 | Salamander Drumkit | Alexander Holm | sfzinstruments | CC BY-SA 3.0 | — | 7.0 MB | — | drum |
| 3 | Brazilian Bateria Percussion | JasperCodes | github | GPL v3 | ✓ | 10.3 MB | — | drum |
| 4 | Melodic Cuica Soundfont | Sizz Tuna | musical-artifacts | CC BY-SA | ✓ | — | 3447 | drum |
| 5 | Sam's Sonor | Sam Greene | sfzinstruments | CC BY-SA 4.0 | — | — | — | drum |
| 6 | Kay 5-String Banjo | FlameStudios | sfzinstruments | GPL v3 | — | 425.0 MB | — | ethnic |
| 7 | Kalimba Soundfont | Sizz Tuna | musical-artifacts | CC BY-SA | ✓ | — | 3002 | ethnic |
| 8 | OPL-3 FM 128M Soundfont | Zandro Reveille | musical-artifacts | CC BY-SA | ✓ | 113.2 MB | 49476 | game |
| 9 | Hedsound's MT32 Soundfont (CM64-L / LAPC-1) [GM remap fix with MSB127  | stgiga, hakerg, Ziya Mete Demi | musical-artifacts | CC BY-SA | ✓ | — | 37765 | game |
| 10 | RetroHybrid! | strixSF2 | musical-artifacts | GPL v3 | ✓ | — | 14863 | game |
| 11 | Sonic 4 Episode 2 Soundfont | Mildanner | musical-artifacts | GPL v2 | ✓ | — | 1665 | game |
| 12 | CMI Orchestra Hit SOUNDFONT | Max Gianelli | musical-artifacts | GPL | ✓ | — | 871 | game |
| 13 | Megaman Zero GM Soundfont | 0P | musical-artifacts | GPL v3 | ✓ | — | 850 | game |
| 14 | F-Zero GM Soundfont | 0P | musical-artifacts | GPL v3 | ✓ | — | 820 | game |
| 15 | Final Fantasy VI Advance GM Soundfont | 0P | musical-artifacts | GPL v3 | ✓ | — | 474 | game |
| 16 | FreePats General MIDI percussion set | FreePats project | FreePats | GPL v3 | ✓ | 15.0 MB | — | gm |
| 17 | FreePats General MIDI set | FreePats project | FreePats | GPL v3 | ✓ | 227.0 MB | — | gm |
| 18 | BalancedGM 1 | sleaf | musical-artifacts | GPL v3 | ✓ | — | 9168 | gm |
| 19 | NanoGM | SG studio | musical-artifacts | CC BY-SA | ✓ | — | 149 | gm |
| 20 | ColomboGMGS2 SoundFont v15.0 | W. Duwindu Tharinda Perera | archive | CC BY-SA 4.0 | — | — | — | gm |
| 21 | ColomboGMGS2 SoundFont V16.7 | W. Duwindu Tharinda Perera | archive | CC BY-SA 4.0 | — | — | — | gm |
| 22 | Matrix SoundFont v1.4 | Matrix369 | musical-artifacts | CC BY-SA | — | — | 0 | gm |
| 23 | FSS Steel-String Acoustic Guitar | FreePats project | FreePats | GPL v3 | ✓ | 2.7 MB | — | guitar |
| 24 | Strix's Guitar and Bass Pack | Strix Soundfont Team | musical-artifacts | GPL v3 | ✓ | — | 45253 | guitar |
| 25 | Alesis sr-18 bass | Milton Paredes, MPJ factory st | musical-artifacts | CC BY-SA | ✓ | — | 3022 | guitar |
| 26 | Ibanez RG350EX Electric Guitar | Bernhard Trummer (Uploaded By  | musical-artifacts | CC BY-SA | ✓ | — | 0 | guitar |
| 27 | Galaxy Electric Pianos | Strix Soundfont Team and Elf o | musical-artifacts | GPL v3 | ✓ | — | 12622 | hist |
| 28 | XXtherob-malik-dan GMGS 0.6 | XXtherobloxx21, CupheadKrasueH | musical-artifacts | CC BY-SA | ✓ | — | 262 | hist |
| 29 | MT32  (CM64-L / LAPC-1) Hedsound version Soundfont sf2 | Ziya Mete Demircan | musical-artifacts | CC BY-SA | ✓ | — | 0 | hist |
| 30 | Synth Brass 1 | Strix Soundfont Team | musical-artifacts | GPL v3 | ✓ | — | 6561 | orch |
| 31 | Aeolus Soundfont | Strix Soundfont Team | musical-artifacts | GPL v3 | ✓ | — | 9674 | organ |
| 32 | Organs Pack #8 | Strix Soundfont Team | musical-artifacts | GPL v3 | ✓ | — | 9172 | organ |
| 33 | Organs Pack #7 | Strix Soundfont Team | musical-artifacts | GPL v3 | ✓ | — | 5529 | organ |
| 34 | Organs Pack #6 | Strix Soundfont Team | musical-artifacts | GPL v3 | ✓ | — | 4794 | organ |
| 35 | Organs Pack #3 | Strix Soundfont Team | musical-artifacts | GPL v3 | ✓ | — | 4582 | organ |
| 36 | Organs Pack #4 | Strix Soundfont Team | musical-artifacts | GPL v3 | ✓ | — | 4284 | organ |
| 37 | Organs Pack #5 | Strix Soundfont Team | musical-artifacts | GPL v3 | ✓ | — | 3873 | organ |
| 38 | test_output | sevonj | github | GPL v3 | ✓ | 0.1 MB | — | other |
| 39 | gm | Rainbow-Dreamer | github | GPL v2 | ✓ | 3.1 MB | — | other |
| 40 | FM_GM_SoundFont_v0_2_1_mini | zeittresor | github | GPL v3 | ✓ | 13.7 MB | — | other |
| 41 | FM_GM_SoundFont_v0_4_1_Balanced | zeittresor | github | GPL v3 | ✓ | 22.5 MB | — | other |
| 42 | Styvell Orchestra soundfont bassoon | olof | musical-artifacts | CC BY-SA | ✓ | — | 3884 | other |
| 43 | Online Sequencer Soundfont | James Webb Truckin%27 (Zachary | archive | CC BY-SA 4.0 | — | — | — | other |
| 44 | Realistic Soundfont V2: Libre Edition | SonicLover 19, sleaf | musical-artifacts | CC BY-SA | — | — | 0 | other |
| 45 | piano | ThomasKiljanczykDev | github | GPL v3 | — | 2.4 MB | — | piano |
| 46 | LivingRoom Upright - Micro SFZ | KeyPleezer | sfzinstruments | CC BY-SA 4.0 | — | 107.0 MB | — | piano |
| 47 | Keppy's Steinway Piano (Version 5.2) | KaleidonKep99 & Frozen Snow Pr | musical-artifacts | CC BY-SA | — | — | 32674 | piano |
| 48 | Freepats Rhodes | Unknown | musical-artifacts | GPL | ✓ | — | 6488 | piano |
| 49 | sine | ssankko | github | GPL v3 | ✓ | — | — | piano |
| 50 | GeneralUser GS 1.35 | Piskocis | github | GPL v3 | ✓ | 25.4 MB | — | synth |
| 51 | GeneralUser-GS | ItalianJoker | github | GPL v3 | ✓ | 30.8 MB | — | synth |
| 52 | Supersaw Collection 2 | Strix SF2 | musical-artifacts | GPL v3 | ✓ | — | 11017 | synth |
| 53 | ReVintage World | Elf of Happy and Love, mirrore | musical-artifacts | GPL v3 | ✓ | — | 3584 | synth |
| 54 | Mpj  vocal collection, my voice | Milton Paredes, mpj factory st | musical-artifacts | CC BY-SA | ✓ | — | 7745 | vocal |
| 55 | STYVELL ORCHESTRA SOUNDFONT SAXO-ALTO-VIB-FF | olof | musical-artifacts | CC BY-SA | ✓ | — | 13764 | wind |
| 56 | STYVELL ORCHESTRA SOUNDFONT SAXO-SOPRANO-FF | olof | musical-artifacts | CC BY-SA | ✓ | — | 8120 | wind |
| 57 | STYVELL ORCHESTRA SOUNDFONT SAXO-SOPRANO-VIB-FF | olof | musical-artifacts | CC BY-SA | ✓ | — | 8051 | wind |

## 七、F4 · **不收录** · 全量 826 条（**逐条写明为什么不收录**）

| # | 名称 | 作者 | 来源 | 许可 | 分类 | 不收录原因 |
|---:|---|---|---|---|---|---|
| 1 | Terkelsen's Marimba | Lars Terkelsen, S Christia | sfzinstruments | 未标注 | drum | **未标注许可** → 许可不明即不收录 |
| 2 | Difarem - Difarem - sunsetter shoved through a percussion so | Difarem | archive | 未标注 | drum | **未标注许可** → 许可不明即不收录 |
| 3 | E-MU Classic Series Vol. 6 - World Percussion/Ensembles (WAV | E-mu | archive | 未标注 | drum | **未标注许可** → 许可不明即不收录 |
| 4 | Ken Ardency's Drum Soundfont | Ken Ardency | archive | 未标注 | drum | **未标注许可** → 许可不明即不收录 |
| 5 | SPORE Soundfont SF2 ( V2, Now has drumkit ) | Nonhuman | archive | 未标注 | drum | **未标注许可** → 许可不明即不收录 |
| 6 | florestan-subset | paladin-t | github | 未标注 | game | **未标注许可** → 许可不明即不收录 |
| 7 | ins | paladin-t | github | 未标注 | game | **未标注许可** → 许可不明即不收录 |
| 8 | Game Boy Drum Kit | Bedroom Producers Blog | sfzinstruments | 未标注 | game | **未标注许可** → 许可不明即不收录 |
| 9 | 8bit | paladin-t | github | 未标注 | game | **未标注许可** → 许可不明即不收录 |
| 10 | MFB Tanzbar Drum Samples | Wave Alchemy | sfzinstruments | 未标注 | game | **未标注许可** → 许可不明即不收录 |
| 11 | GeneralUser | ad-si | github | 未标注 | game | **未标注许可** → 许可不明即不收录 |
| 12 | 8-bit twisted sister - we're not gonna take it NES soundfont | Soundfont Central | archive | 未标注 | game | **未标注许可** → 许可不明即不收录 |
| 13 | Apotos Daytime / Windmill Isle ( Touhou Soundfont) | SEGA | archive | 未标注 | game | **未标注许可** → 许可不明即不收录 |
| 14 | Bonetrousle SNES Remix - Undertale (EarthBound 16 Bit Soundf | Bulby | archive | 未标注 | game | **未标注许可** → 许可不明即不收录 |
| 15 | Deltarune Rude Buster ( Pokemon B 2 W 2 Soundfont) | — | archive | 未标注 | game | **未标注许可** → 许可不明即不收录 |
| 16 | Final Nightmare (pokemon rse soundfont version) | shinyjiggly | archive | 未标注 | game | **未标注许可** → 许可不明即不收录 |
| 17 | Gounod: Faust - Ballet Music (Les Nubiennes) (SBSC 2003 Soun | Charles Gounod, Andy Stree | archive | 未标注 | game | **未标注许可** → 许可不明即不收录 |
| 18 | It's A Small World (Doraemon And The 3 Fairy Spirit Stones S | The Sherman Brothers | archive | 未标注 | game | **未标注许可** → 许可不明即不收录 |
| 19 | Katyusha (Soviet War Song) but it's the Undertale Soundfont | Clockenspiel | archive | 未标注 | game | **未标注许可** → 许可不明即不收录 |
| 20 | LG VX6100 ringtones on Samsung Swift soundfont | Floomsy Tech | archive | 未标注 | game | **未标注许可** → 许可不明即不收录 |
| 21 | Little Einsteins - Theme Song (Super Mario SNES Soundfont) | Billy Straus | archive | 未标注 | game | **未标注许可** → 许可不明即不收录 |
| 22 | Mediatek Startup and Shutdown Tones in Spreadtrum Soundfont | New Some Phonez Videos | archive | 未标注 | game | **未标注许可** → 许可不明即不收录 |
| 23 | minimal_gs | libraz | github | 未标注 | game | **未标注许可** → 许可不明即不收录 |
| 24 | Nintendo Wii Channel Soundfont | idk | archive | 未标注 | game | **未标注许可** → 许可不明即不收录 |
| 25 | Pokemon Dppt Soundfont Collection | Franson Langinblik 19 | archive | 未标注 | game | **未标注许可** → 许可不明即不收录 |
| 26 | Pokemon Generations Soundfont | — | archive | 未标注 | game | **未标注许可** → 许可不明即不收录 |
| 27 | Pokemon HGSS SOUNDFONT Collection | Franson Langinblik | archive | 未标注 | game | **未标注许可** → 许可不明即不收录 |
| 28 | Pokemon Mystery Dungeon Explorers Of Sky Full Soundfont | — | archive | 未标注 | game | **未标注许可** → 许可不明即不收录 |
| 29 | Realistic Soundfont V 2 Libre V 1 ( 16bit) Sub 2 Gi B.sf 2.7 | — | archive | 未标注 | game | **未标注许可** → 许可不明即不收录 |
| 30 | shinyjiggly - Final Nightmare (pokemon Rse Soundfont Version | shinyjiggly | archive | 未标注 | game | **未标注许可** → 许可不明即不收录 |
| 31 | Sonic 3D Blast Soundfont | — | archive | 未标注 | game | **未标注许可** → 许可不明即不收录 |
| 32 | Sonic Pinball Party Midi + SoundFont Rip | Sonic Team | archive | 未标注 | game | **未标注许可** → 许可不明即不收录 |
| 33 | South Park's Parents: Magic Alliance (Nintendo DS) soundfont | Parker-stone Interactive S | archive | 未标注 | game | **未标注许可** → 许可不明即不收录 |
| 34 | Take On Me but it's the OldSchool RuneScape soundfont | Unpragmatic Covers | archive | 未标注 | game | **未标注许可** → 许可不明即不收录 |
| 35 | The Definitive FNF Soundfont (ALL CHARACTERS + EXTRAS) | SuperStamps | archive | 未标注 | game | **未标注许可** → 许可不明即不收录 |
| 36 | The Entire Undertale OST but it uses the 2009 ROBLOX Soundfo | DownFrown | archive | 未标注 | game | **未标注许可** → 许可不明即不收录 |
| 37 | the entire undertale soundtrack but with the Whitty soundfon | SnapBack | archive | 未标注 | game | **未标注许可** → 许可不明即不收录 |
| 38 | The Wellington March - Doraemon: Nobita And The 3 Fairy Spir | Stephanie Kim, Wilhelm Zeh | archive | 未标注 | game | **未标注许可** → 许可不明即不收录 |
| 39 | tiny | not-hanjo-mei | github | 未标注 | game | **未标注许可** → 许可不明即不收录 |
| 40 | tv room - sonic spinball soundfont 👀 | tv room | archive | 未标注 | game | **未标注许可** → 许可不明即不收录 |
| 41 | UNDERTALE Soundfont 2 | — | archive | 未标注 | game | **未标注许可** → 许可不明即不收录 |
| 42 | ファノンパーク GO GO! 真夜中の逃走 (GBA) Soundfont ~ Demos + Resources | Parker-Stone Interactive S | archive | 未标注 | game | **未标注许可** → 许可不明即不收录 |
| 43 | TimGM6mb | — | fluidsynth | 未标注 | gm | **未标注许可** → 许可不明即不收录 |
| 44 | Demo MIDIs for ColomboGMGS2 SoundFont | Duwindu Tharinda Perera | archive | 未标注 | gm | **未标注许可** → 许可不明即不收录 |
| 45 | SGM Soundfont Archive | Shan | archive | 未标注 | gm | **未标注许可** → 许可不明即不收录 |
| 46 | Shan SGM Pro / X64 / X28 / ES8 Soundfont | Shan | archive | 未标注 | gm | **未标注许可** → 许可不明即不收录 |
| 47 | E-MU Classic Series Vol. 15 – Bass Collection Dan Dean Produ | E-mu | archive | 未标注 | guitar | **未标注许可** → 许可不明即不收录 |
| 48 | Guitar GM SoundFont + conversions | Andrei | archive | 未标注 | guitar | **未标注许可** → 许可不明即不收录 |
| 49 | N64 SDK Soundfont and BassDrive.mid | Nintendo | archive | 未标注 | guitar | **未标注许可** → 许可不明即不收录 |
| 50 | Xploshi - The actual strumming sound added to a virtual guit | Xploshi | archive | 未标注 | guitar | **未标注许可** → 许可不明即不收录 |
| 51 | E-MU Classic Series Vol. 2 - More Emulator Standards (WAV, S | E-mu | archive | 未标注 | hist | **未标注许可** → 许可不明即不收录 |
| 52 | KORG M1 Waveforms Soundfont | KORG | archive | 未标注 | hist | **未标注许可** → 许可不明即不收录 |
| 53 | Nickelodeon MIDI w/ Roland SC-55 Soundfont | Nickelodeon | archive | 未标注 | hist | **未标注许可** → 许可不明即不收录 |
| 54 | Roland SC-55 Soundfont by EmperorGrieferus | EmperorGrieferus | archive | 未标注 | hist | **未标注许可** → 许可不明即不收录 |
| 55 | Roland SC-55 Soundfont by EmperorGrieferus | EmperorGrieferus | archive | 未标注 | hist | **未标注许可** → 许可不明即不收录 |
| 56 | Roland Sound Canvas SC-55 Soundfont | EmperorGrieferus | archive | 未标注 | hist | **未标注许可** → 许可不明即不收录 |
| 57 | Roland Sound Canvas SoundFont ( 24 Bit XGD Edition) | W. Duwindu Tharinda Perera | archive | 未标注 | hist | **未标注许可** → 许可不明即不收录 |
| 58 | The Zealand Story - Kiwi Kraze Main Theme (Cookie Run Ovenbr | — | archive | 未标注 | hist | **未标注许可** → 许可不明即不收录 |
| 59 | Virtual Playing Orchestra | Paul Battersby | sfzinstruments | 未标注 | orch | **未标注许可** → 许可不明即不收录 |
| 60 | Aegean Symphonic Orchestra v2.5 universal | — | fluidsynth | 未标注 | orch | **未标注许可** → 许可不明即不收录 |
| 61 | Sonatina Symphonic Orchestra | — | fluidsynth | 未标注 | orch | **未标注许可** → 许可不明即不收录 |
| 62 | 1 HQ Orchestral Soundfont Collection V 2.0 | — | archive | 未标注 | orch | **未标注许可** → 许可不明即不收录 |
| 63 | Hades Strings (Soundfont) | Hade | archive | 未标注 | orch | **未标注许可** → 许可不明即不收录 |
| 64 | CFaz Keys IV (3s Release, No-Pan) | mbms0 | github | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 65 | CFaz Keys IV (No-Pan) | mbms0 | github | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 66 | CFaz Keys IV (Old Tuned, 3s Release, No-Pan) | mbms0 | github | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 67 | CFaz Keys IV (Old Tuned, No-Pan) | mbms0 | github | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 68 | CFaz Keys IV (Random Offset) | mbms0 | github | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 69 | CFaz Keys IV (Random Offset, 3s Release) | mbms0 | github | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 70 | CFaz Keys IV (Random Offset, 3s Release, No-Pan) | mbms0 | github | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 71 | CFaz Keys IV (Random Offset, No-Pan) | mbms0 | github | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 72 | GB | kmatze | github | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 73 | CFaz Keys IV | mbms0 | github | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 74 | CFaz Keys IV (3s Release) | mbms0 | github | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 75 | CFaz Keys IV (Old Tuned) | mbms0 | github | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 76 | CFaz Keys IV (Old Tuned, 3s Release) | mbms0 | github | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 77 | FluidR3_GS | Jacalz | github | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 78 | soundbank | 59de44955ebd | github | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 79 | FluidR3 | Jacalz | github | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 80 | Salamander C5 Light | — | fluidsynth | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 81 | S. Christian Collins GeneralUser GS | — | fluidsynth | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 82 | 233_poprockbank | Rezonality | github | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 83 | Magic Sound Font, version 2.0 | — | fluidsynth | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 84 | Fluid (R3) General MIDI SoundFont (GM) | — | fluidsynth | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 85 | Arachno SoundFont, version 1.0 | — | fluidsynth | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 86 | "WST 25 FStein 00 Sep 22" Soundfont | Warren Trachtman | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 87 | 0x 39 D 5 F Mii Maker ( CTR N HEDE) ( U) Midi & Soundfont. 7 | 0x 39 D 5 F Mii Maker ( CT | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 88 | 1930 1970 Music Soundfont | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 89 | 4Kids TV Soundfont (UNOFFICIAL AND INSPIRED) | Ralph Dion Shuckett, John  | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 90 | 909 Day! Mystery Soundfont Demo with TR-909 | David "SgtPepperArc360" Eg | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 91 | Ace Attorney: Phoenix Wright: Court Begins 2005 DS .MID And  | CAPCOM | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 92 | After The End MIDI Soundtrack (SC-55 Soundfont) | Kraisoft Entertainment | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 93 | Aladdin And The Adventure Of All-Time (Movie Based Un-Offici | Ferris Ellen Gluck, Mary E | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 94 | ALL IN ONE Android App Soundfont Collection | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 95 | All MediaTek Startup/Shutdown with MT6250 SoundFont | Cyberphones | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 96 | alphabet soundfont | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 97 | Andy Hopper Soundfont MIDI Collection | Frank Gari And Let's Go Lu | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 98 | Aphex Twin - Aisatsana (Super Mario 64 Soundfont) | on4word | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 99 | Baby Einstein Soundfont (6 Versions) | Baby Einstein, The Baby Ei | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 100 | Baby Einstein Soundfont (Version 3) | Baby Einstein, The Baby Ei | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 101 | Bad Mii Theme Soundfont | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 102 | Beach House - Space Song (Super Mario 64 Soundfont) | on4word | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 103 | Bee Swarm Simulator Soundfont (2020 Version) | Onett | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 104 | Ben 10: Protector of Earth (DS) SoundFont | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 105 | Bloons DSiWare Soundfont | MarioW | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 106 | boards of canada - kid for today (animal crossing soundfont) | psych | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 107 | Bro got Opps in 2011 [2009 Roblox Soundfont remix] | Retro Legend | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 108 | Canon Lexus 185 Soundfont | Canon | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 109 | Captain Claw (1997) - Full OST (CLAW4.SF2 Soundfont) | Virgin Snake | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 110 | CFaz Keys IV (Extended Layers) | mbms0 | github | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 111 | CFaz Keys IV (Extended Layers, 3s Release) | mbms0 | github | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 112 | CFaz Keys IV (Extended Layers, 3s Release, No-Pan) | mbms0 | github | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 113 | CFaz Keys IV (Extended Layers, No-Pan) | mbms0 | github | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 114 | CFaz Keys IV (No Layers) | mbms0 | github | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 115 | CFaz Keys IV (No Layers, 3s Release) | mbms0 | github | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 116 | CFaz Keys IV (No Layers, 3s Release, No-Pan) | mbms0 | github | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 117 | CFaz Keys IV (No Layers, No-Pan) | mbms0 | github | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 118 | Cradle Of Filth Mannequin! ( With Pokémon Ruby And Sapphire  | Midian-P | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 119 | Daft Punk - Get Lucky ft. Pharrell but with the SM64 soundfo | verymilkee | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 120 | Death Grips - I've Seen Footage (DK Rap / DK64 Soundfont) | on4word | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 121 | Donkey Kong Country Fandmade Soundfont Soundtracks | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 122 | DOOM E1M1 (OSRS Soundfont) | Brian Espinoza / ICFreeze | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 123 | Dora the Explorer: Soundfont Collection (WIP) | Steve Sandberg | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 124 | E-MU Classic Series Vol. 10 – Elements of Sound 1MB (WAV, So | E-mu | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 125 | E-MU Classic Series Vol. 14 – ESI 32 General Midi Collection | E-mu | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 126 | E5M1 Sweet Dreams (DOOM Soundfont Remix) | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 127 | Fanon Park Nostalgia Soundfont ~ PREMIUM EDITION – Demo File | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 128 | Fat Boy GM/GS SoundFont v0.790 | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 129 | Fluid R3 Mobile GM Soundfont | Frank Wen | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 130 | FluidR3_GM | Jacalz | github | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 131 | Frank Gari And Let's Go Luna Team Soundfont Collection (Down | Frank Gari And Let's Go Lu | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 132 | Gangsta Rap - Ni**a Ni**a Ni**a (SMA2 Soundfont) | yodel boi | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 133 | Giant Land - Super Mario Brothers 3 / Super Mario 64 Soundfo | Greenio, too | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 134 | Gigapack 1 & 2 (Soundfont) | Best Service | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 135 | God Bless America! (Imagine: Figure Skater And Ice Champions | Irving Berlin, Stephanie K | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 136 | GZDoom Soundfont | Randi Heit | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 137 | Hava Nagila ( Mario Party DS Soundfont) | Stephanie Kim | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 138 | Hopla Soundfont | Bert Smets Productions | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 139 | Hotel Mario Soundfont | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 140 | I'd Like To Teach The World To Sing (Super Mario 64 Soundfon | Billy Davis, Billy Backer, | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 141 | In Rainbow Roads (Radiohead - In Rainbows / Mario 64 Soundfo | on4word | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 142 | Laugh and Learn - The ("Un-Official") Soundfont | Timothy Steven Clarke, Nic | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 143 | LeapFrog Leap-font: Official Release - Soundfont Demonstrati | Jeanne Parson, Richard Mar | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 144 | Mega Man Zero 1 4 Soundfont ( VER 1) | Jordan Moore | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 145 | MIDI Soundfont | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 146 | Monster Tale Soundfont | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 147 | Mystery Soundfont - you won't guess! | David "SgtPepperArc360" Eg | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 148 | New Super Mario Bros. DS Soundfont | Nintendo, Koji Kondo | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 149 | New Super Mario Bros. U And Super Mario World Custom Music - | Nintendo, Koji Kondo | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 150 | Nirvana's Bleach But With The SM 64 Soundfont ( 320 K) | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 151 | Nokia (6610) Arabic Ringtone played on an iPhone 13 Noob (so | The Mariocrafter | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 152 | Nokia 3110c (Lloyd Bank) Soundfont | Nokia | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 153 | OHAGI Official Soundfont | Enoki_1997 | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 154 | Online Sequencer - Soundfont V1.0 | Online Sequencer | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 155 | OST - SimCity 2000 (Mac OS Soundfont) | Maxis | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 156 | Passport.mid - PC Audacious - Arachno SoundFont Version 1.0 | Petr Mach | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 157 | Patch93's SC-55 Soundfont | Patch93 | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 158 | Patrick Beatbox (#3) N64 Soundfont Cover | CurtisTRY | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 159 | Paul Speer & David Lanz - Behind The Waterfall (SM64 Soundfo | Unknown | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 160 | Perfect Nothing (SMRPG SoundFont Remix) ://: Cutila-Mun | Florageist / Hyacinth Orch | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 161 | Phoenix Soundfont | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 162 | PMD Explorers Of Sky Full Soundfont | u/RatelRaichu | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 163 | Pudata in the Big City soundfont (SF2) | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 164 | Roarsputin (Rasputin / SM64 Soundfont) | Deadz64 | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 165 | RSE SOUNDFONT COLLECTION | Franson Langinbelik 19 | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 166 | Sammy Soundfont | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 167 | Santana X Rob Thomas: Smooth ( MKSC Soundfont) | Itaal Shur, Santana, Rob T | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 168 | SC2KMac.zip (Sim City 2000 MIDI files with Mac soundfont) | Rich Nagel | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 169 | Serial Experiments Lain PS 1 Soundfont Ver. 0.1 | kju, Tsuruoka Yota, Kasama | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 170 | Sforzatron | Plogue | sfzinstruments | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 171 | SgtPepperArc360 XG (The Mystery Soundfont) | David "SgtPepperArc360" Eg | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 172 | SgtPepperArc360 XG Soundfont V2.0 | David "SgtPepperArc360" Eg | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 173 | SgtPepperArc360's Soundfont Collections | David "SgtPepperArc360" Eg | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 174 | Shadow Queen on the Paper Mario 64 SoundFont | Joe Capo | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 175 | Smiley World: Island Challenge (NDS) Soundfont | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 176 | Soccer Shootout Soundfont | TheJosh347 | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 177 | Soundfont - The Collection | Zandro | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 178 | SOUNDFONT CD II by Creative Labs | Creative Labs. AWE32 | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 179 | Soundfont collection 1 | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 180 | Soundfont Collection Download | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 181 | SoundFont Shuffle Vol. 1 | Larry RMX | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 182 | Soundfont Spectacular Presents: The Classics | Stephanie Kim | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 183 | Spanish Flea (SMA2 Soundfont) | yodel boi | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 184 | Strawberry Shortcake Soundfont Collection | Andy Street | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 185 | Super Black Parade 64 - My Chemical Romance / Super Mario So | Microplastic Brain | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 186 | Super Mario 64 Midis And Soundfont | Pablo's Corner + Unknown M | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 187 | Super Mario 64 Soundfont by sm64pie | sm64pie | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 188 | Super Mario CD Soundfont ( Both Versions) | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 189 | Super Mario CD Soundfont ( Both Versions) ( 2022 Update) | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 190 | TADC - Your New Home - SM64 Soundfont ❨V2❩-[aO8q2iP5XoM] | Garfield, VeeDoesStuff1 | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 191 | The Amazing Digital Circus : Your New Home - SM64 Soundfont  | Garfield, VeeDoesStuff1 | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 192 | The Cedarmont Kids Soundfont Collection | Christopher Davis, Matt Hu | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 193 | The Lock Song In The Super Mario 64 Soundfont | Billy West | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 194 | The Mystery Soundfont has been unveiled! + And the winner is | David "SgtPepperArc360" Eg | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 195 | The Pixies - Where Is My Mind SM 64 Soundfont | @somethingisreal on YouTub | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 196 | Timbres Of Heaven soundfont | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 197 | Timidity++ Soundfont [for Opentouch] | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 198 | Tomahawk Head - Shameful MIDI / soundfont swap edition | Tirantbacon | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 199 | toy_xylophone_V2_soundfont_fixed | TheSoundfontMaker | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 200 | TurboGrafx-16 Soundfont (PC-Engine Soundfont) | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 201 | TURKISH-ARAB3 (.sf2) soundfont | [unknown] | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 202 | tv room - good soundfont names | tv room | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 203 | UHD3 SoundFont | cwadge | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 204 | Ultimate Soundfont v1.00 | MediaCollector | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 205 | UrChinchillaElcie - Fanon Park Nostalgia SoundFont Remixes v | UrChinchillaElcie | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 206 | Viena SoundFont Editor 0.980 | SynthFont | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 207 | Vs! Zinnia - Pokémon Black & White 2 Soundfont Remix | Instro | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 208 | VSCO 2 Community Edition (CE) SoundFont | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 209 | Windows MIDI Demos: SC-55 soundfont | Microsoft Corporation | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 210 | Winds of Fjords (.it file and soundfont) | minomus | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 211 | Yoshi Story 64 Soundfont | Reza Khadafi | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 212 | You're Mine but it's SM64 soundfont | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 213 | Arataki's Great and Glorious Drum | StarryCosmosPiano | github | 未标注 | piano | **未标注许可** → 许可不明即不收录 |
| 214 | Djem Djem Drum | StarryCosmosPiano | github | 未标注 | piano | **未标注许可** → 许可不明即不收录 |
| 215 | Ukulele | StarryCosmosPiano | github | 未标注 | piano | **未标注许可** → 许可不明即不收录 |
| 216 | GeneralUserGS | pinkpixel-dev | github | 未标注 | piano | **未标注许可** → 许可不明即不收录 |
| 217 | Lingering Euphonia | StarryCosmosPiano | github | 未标注 | piano | **未标注许可** → 许可不明即不收录 |
| 218 | Lingering Euphonia (Original with Chords) | StarryCosmosPiano | github | 未标注 | piano | **未标注许可** → 许可不明即不收录 |
| 219 | Ukulele (Original with Chords) | StarryCosmosPiano | github | 未标注 | piano | **未标注许可** → 许可不明即不收录 |
| 220 | Windsong Lyre | StarryCosmosPiano | github | 未标注 | piano | **未标注许可** → 许可不明即不收录 |
| 221 | Leaping Spirit Piano | StarryCosmosPiano | github | 未标注 | piano | **未标注许可** → 许可不明即不收录 |
| 222 | Vodyanitsa | StarryCosmosPiano | github | 未标注 | piano | **未标注许可** → 许可不明即不收录 |
| 223 | Harmonic Keys | StarryCosmosPiano | github | 未标注 | piano | **未标注许可** → 许可不明即不收录 |
| 224 | Floral Zither | StarryCosmosPiano | github | 未标注 | piano | **未标注许可** → 许可不明即不收录 |
| 225 | Nightwind Horn | StarryCosmosPiano | github | 未标注 | piano | **未标注许可** → 许可不明即不收录 |
| 226 | Vintage Lyre | StarryCosmosPiano | github | 未标注 | piano | **未标注许可** → 许可不明即不收录 |
| 227 | Nice-Steinway-Lite-v3.0 | ales-tsurko | github | 未标注 | piano | **未标注许可** → 许可不明即不收录 |
| 228 | Church Steinway | Pianobook | sfzinstruments | 未标注 | piano | **未标注许可** → 许可不明即不收录 |
| 229 | Estate Grand LE | Production Voices | sfzinstruments | 未标注 | piano | **未标注许可** → 许可不明即不收录 |
| 230 | Piano in 162 | Ivy Audio | sfzinstruments | 未标注 | piano | **未标注许可** → 许可不明即不收录 |
| 231 | Amethyst Imperial Grand - Imperial Hall | mbms0 | github | 未标注 | piano | **未标注许可** → 许可不明即不收录 |
| 232 | Amethyst Imperial Grand - Imperial Hall - Strings Accompanim | mbms0 | github | 未标注 | piano | **未标注许可** → 许可不明即不收录 |
| 233 | Amethyst Imperial Grand - Studio | mbms0 | github | 未标注 | piano | **未标注许可** → 许可不明即不收录 |
| 234 | Amethyst Imperial Grand - Studio - Strings Accompaniment | mbms0 | github | 未标注 | piano | **未标注许可** → 许可不明即不收录 |
| 235 | Cathan Concert Grand | mbms0 | github | 未标注 | piano | **未标注许可** → 许可不明即不收录 |
| 236 | Cathan Concert Grand (Long Release) | mbms0 | github | 未标注 | piano | **未标注许可** → 许可不明即不收录 |
| 237 | Cathan Concert Grand (Long Release, No Pan) | mbms0 | github | 未标注 | piano | **未标注许可** → 许可不明即不收录 |
| 238 | Cathan Concert Grand (No Pan) | mbms0 | github | 未标注 | piano | **未标注许可** → 许可不明即不收录 |
| 239 | Cathan Concert Grand - Detuned | mbms0 | github | 未标注 | piano | **未标注许可** → 许可不明即不收录 |
| 240 | Cathan Concert Grand - Detuned (Long Release) | mbms0 | github | 未标注 | piano | **未标注许可** → 许可不明即不收录 |
| 241 | Cathan Concert Grand - Detuned (Long Release, No Pan) | mbms0 | github | 未标注 | piano | **未标注许可** → 许可不明即不收录 |
| 242 | Cathan Concert Grand - Detuned (No Pan) | mbms0 | github | 未标注 | piano | **未标注许可** → 许可不明即不收录 |
| 243 | Cathan Concert Grand - Random Offset | mbms0 | github | 未标注 | piano | **未标注许可** → 许可不明即不收录 |
| 244 | Cathan Concert Grand - Random Offset (Long Release) | mbms0 | github | 未标注 | piano | **未标注许可** → 许可不明即不收录 |
| 245 | Cathan Concert Grand - Random Offset (Long Release, No Pan) | mbms0 | github | 未标注 | piano | **未标注许可** → 许可不明即不收录 |
| 246 | Cathan Concert Grand - Random Offset (No Pan) | mbms0 | github | 未标注 | piano | **未标注许可** → 许可不明即不收录 |
| 247 | Sheet Music Boss Piano Soundfont | — | archive | 未标注 | piano | **未标注许可** → 许可不明即不收录 |
| 248 | Southerncafe24's Toy Piano + Lyre Soundfont ~ demo files | The Southerncafe24 Project | archive | 未标注 | piano | **未标注许可** → 许可不明即不收录 |
| 249 | Warren S. Trachtman - Steinway Model-C Soundfont | Warren S. Trachtman | archive | 未标注 | piano | **未标注许可** → 许可不明即不收录 |
| 250 | Timbres Of Heaven GM_GS_XG_SFX V 3.4 | — | fluidsynth | 未标注 | sfx | **未标注许可** → 许可不明即不收录 |
| 251 | VintageDreams | fcarvajalbrown | github | 未标注 | synth | **未标注许可** → 许可不明即不收录 |
| 252 | florestan-subset | fynv | github | 未标注 | synth | **未标注许可** → 许可不明即不收录 |
| 253 | florestan-subset | fynv | github | 未标注 | synth | **未标注许可** → 许可不明即不收录 |
| 254 | florestan-subset | Wally869 | github | 未标注 | synth | **未标注许可** → 许可不明即不收录 |
| 255 | TimGM6mbEdit | chipweinberger | github | 未标注 | synth | **未标注许可** → 许可不明即不收录 |
| 256 | soundfont | Electric-ray | github | 未标注 | synth | **未标注许可** → 许可不明即不收录 |
| 257 | GeneralUserGS | spessasus | github | 未标注 | synth | **未标注许可** → 许可不明即不收录 |
| 258 | GeneralUser GS v1.471 | arkark2010arkark | github | 未标注 | synth | **未标注许可** → 许可不明即不收录 |
| 259 | GeneralUser_GS_SoftSynth_v1.44 | arkark2010arkark | github | 未标注 | synth | **未标注许可** → 许可不明即不收录 |
| 260 | GeneralUser-GS | Misterscan | github | 未标注 | synth | **未标注许可** → 许可不明即不收录 |
| 261 | GeneralUser_GS | fcarvajalbrown | github | 未标注 | synth | **未标注许可** → 许可不明即不收录 |
| 262 | Custom instrumental variant of Dragon Tales theme with leapf | — | archive | 未标注 | synth | **未标注许可** → 许可不明即不收录 |
| 263 | dummy | sinshu | github | 未标注 | synth | **未标注许可** → 许可不明即不收录 |
| 264 | GS For HTF ( Redmi Oct) Soundfont | — | archive | 未标注 | synth | **未标注许可** → 许可不明即不收录 |
| 265 | test_empty_samples | sinshu | github | 未标注 | synth | **未标注许可** → 许可不明即不收录 |
| 266 | GeneralUserGS | birkeeper | github | 未标注 | vocal | **未标注许可** → 许可不明即不收录 |
| 267 | Choir_practice | birkeeper | github | 未标注 | vocal | **未标注许可** → 许可不明即不收录 |
| 268 | Radiohead - Follow Me Around From The Lost Woods (Ocarina of | on4word | archive | 未标注 | wind | **未标注许可** → 许可不明即不收录 |
| 269 | Sonic the Hedgehog (Prototype) Soundfont | Mildanner, ProjectFM, Sega | musical-artifacts | CC BY-NC | game | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 270 | Korg WAVESTATION Vektor Organ Soundfont | Mildanner, KORG | musical-artifacts | CC BY-NC | hist | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 271 | Aegean Symphonic Orchestra sf2 | Ziya Mete Demircan | musical-artifacts | CC BY-NC | gm | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 272 | KoЯn Got The Life In The DOOM Soundfont | cooper | archive | CC BY-NC | other | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 273 | jRhodes3d | Jeff Learman | sfzinstruments | CC BY-NC | piano | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 274 | Salamander C5 Light sf2 | Ziya Mete Demircan | musical-artifacts | CC BY-NC | piano | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 275 | The DEFINITIVE MEGALOVANIA Soundfont! V1.19 | Willie Aton | musical-artifacts | CC BY-NC-ND 3.0 | game | NC-ND：禁商用且禁改作 → 我们不代管、不直链 |
| 276 | Christian Zell Harpsichord 1737 (Equal temperament) | Pere Casulleras | musical-artifacts | CC BY-NC-ND 3.0 | other | NC-ND：禁商用且禁改作 → 我们不代管、不直链 |
| 277 | Christian Zell Harpsichord 1737 (Original fifth-comma meanto | Pere Casulleras | musical-artifacts | CC BY-NC-ND 3.0 | other | NC-ND：禁商用且禁改作 → 我们不代管、不直链 |
| 278 | Dr. Mario 64 Soundfont | Mildanner, Nintendo | musical-artifacts | CC BY-NC-ND 3.0 | game | NC-ND：禁商用且禁改作 → 我们不代管、不直链 |
| 279 | NECROFANTASIA (Sonic 3 & Knuckles Soundfont Remix) | ThePerfectCanadianDBFan | archive | CC BY-NC-ND 3.0 | game | NC-ND：禁商用且禁改作 → 我们不代管、不直链 |
| 280 | Sonic 3 (Prototype) Credits (Touhou Soundfont Remix) | Eternal Archivist 17 | archive | CC BY-NC-ND 3.0 | game | NC-ND：禁商用且禁改作 → 我们不代管、不直链 |
| 281 | loopool soundfont collection | loopool / Jean-Paul Garnie | archive | CC BY-NC-ND 3.0 | other | NC-ND：禁商用且禁改作 → 我们不代管、不直链 |
| 282 | The Mega Musical Soundfont | SandisBergvalds2008 | archive | CC BY-NC-ND 3.0 | other | NC-ND：禁商用且禁改作 → 我们不代管、不直链 |
| 283 | Unicom 62172 Door Chime soundfont V4 [UPDATED] | Unicom | archive | CC BY-NC-ND 3.0 | other | NC-ND：禁商用且禁改作 → 我们不代管、不直链 |
| 284 | Titanic 200 GM-GS v1.2 | Luke Sena - Titanic Soundf | musical-artifacts | CC BY-NC-SA | other | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 285 | VirtuOrgan Soundfont | Fernando A. Martin | musical-artifacts | CC BY-NC-SA | organ | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 286 | Caed's Ultimate Adequate GM Version 1.00 (3.97 GB GM Soundfo | Caed | musical-artifacts | CC BY-NC-SA | gm | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 287 | jRhodes3c | Jeff Learman | sfzinstruments | CC BY-NC-SA | piano | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 288 | Sonic 4 Ep. 1 & 2 Accurate Drum (Soundfont Port) | Mildanner, Speedy the Dog | musical-artifacts | CC BY-NC-SA 3.0 | game | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 289 | MF Tin Whistle | Markus Fiedler | sfzinstruments | CC BY-NC-SA 3.0 | ethnic | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 290 | shinyjiggly - Landsweep (Kirby 64 soundfont) | shinyjiggly | archive | CC BY-NC-SA 3.0 | game | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 291 | Rickenbacker 4001 | Project 16 | sfzinstruments | CC BY-NC-SA 3.0 | guitar | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 292 | Orpheus GM V1.047e | Virtuon | musical-artifacts | CC BY-ND（禁改作） | orch | **ND 禁改作**：音色的主要用途就是衍生（用采样做音乐/改编）→ 收录会误导使用者 |
| 293 | Just t4, yamaha tyros 4 gm soundfont | Milton Paredes, MP factory | musical-artifacts | CC Sampling（整包分发受限） | hist | CC Sampling 系列：整包原样再分发受限（仅非商业）→ 只给来源 |
| 294 | Sonatina Symphonic Orchestra (Full SF2) | SonicLover 19 | musical-artifacts | CC Sampling（整包分发受限） | orch | CC Sampling 系列：整包原样再分发受限（仅非商业）→ 只给来源 |
| 295 | Sonatina Symphonic Orchestra | Mattias Westlund | musical-artifacts | CC Sampling（整包分发受限） | orch | CC Sampling 系列：整包原样再分发受限（仅非商业）→ 只给来源 |
| 296 | G-Town Church Sampling Project (kontakt) | Tobias Marberger | musical-artifacts | CC Sampling（整包分发受限） | drum | CC Sampling 系列：整包原样再分发受限（仅非商业）→ 只给来源 |
| 297 | MrSanic's (me) NES Soundfont | MrSanic | musical-artifacts | CC Sampling（整包分发受限） | game | CC Sampling 系列：整包原样再分发受限（仅非商业）→ 只给来源 |
| 298 | Mellowtron | j_e_f_f_g | musical-artifacts | CC Sampling（整包分发受限） | other | CC Sampling 系列：整包原样再分发受限（仅非商业）→ 只给来源 |
| 299 | Sonic Adventure Soundfont | Redhotsupermario, SEGA for | musical-artifacts | CC Sampling（整包分发受限） | other | CC Sampling 系列：整包原样再分发受限（仅非商业）→ 只给来源 |
| 300 | Sonatina Symphonic Orchestra | Mattias Westlund, Peter Ea | sfzinstruments | CC Sampling Plus 1.0 | orch | CC Sampling Plus 1.0：整包原样再分发仅限非商业 → 只给来源 |
| 301 | G-Town Church Sampling Project | Tobias Marberger | sfzinstruments | CC Sampling Plus 1.0 | other | CC Sampling Plus 1.0：整包原样再分发仅限非商业 → 只给来源 |
| 302 | Ghana Drums | Karoryfer Samples | sfzinstruments | 商业授权 / 付费产品 | drum | 商业授权 / 需付费购买 |
| 303 | Tubular Bells II | Versilian Studios LLC | sfzinstruments | 商业授权 / 付费产品 | drum | 商业授权 / 需付费购买 |
| 304 | Castanets | TKDrums | sfzinstruments | 商业授权 / 付费产品 | drum | 商业授权 / 需付费购买 |
| 305 | RawCowbell | TKDrums | sfzinstruments | 商业授权 / 付费产品 | drum | 商业授权 / 需付费购买 |
| 306 | Simple Tamb | TKDrums | sfzinstruments | 商业授权 / 付费产品 | drum | 商业授权 / 需付费购买 |
| 307 | Turkish Rebab | Karoryfer Samples | sfzinstruments | 商业授权 / 付费产品 | ethnic | 商业授权 / 需付费购买 |
| 308 | Fourth Tagelharpa | Karoryfer Samples | sfzinstruments | 商业授权 / 付费产品 | ethnic | 商业授权 / 需付费购买 |
| 309 | Kemençe Of The Black Sea | Karoryfer Samples | sfzinstruments | 商业授权 / 付费产品 | ethnic | 商业授权 / 需付费购买 |
| 310 | Nanfo | Karoryfer Samples | sfzinstruments | 商业授权 / 付费产品 | ethnic | 商业授权 / 需付费购买 |
| 311 | Three Tagelharpas | Karoryfer Samples | sfzinstruments | 商业授权 / 付费产品 | ethnic | 商业授权 / 需付费购买 |
| 312 | World Instruments | Garritan | sfzinstruments | 商业授权 / 付费产品 | ethnic | 商业授权 / 需付费购买 |
| 313 | (various) | Wave Alchemy | sfzinstruments | 商业授权 / 付费产品 | game | 商业授权 / 需付费购买 |
| 314 | (various) | Samples From Mars | sfzinstruments | 商业授权 / 付费产品 | game | 商业授权 / 需付费购买 |
| 315 | Beefowulf Bass | Karoryfer Samples | sfzinstruments | 商业授权 / 付费产品 | guitar | 商业授权 / 需付费购买 |
| 316 | Karniszbass | Karoryfer Samples | sfzinstruments | 商业授权 / 付费产品 | guitar | 商业授权 / 需付费购买 |
| 317 | Glockenskull Guitar | Karoryfer Samples | sfzinstruments | 商业授权 / 付费产品 | guitar | 商业授权 / 需付费购买 |
| 318 | Secret Agent Guitar | Karoryfer Samples | sfzinstruments | 商业授权 / 付费产品 | guitar | 商业授权 / 需付费购买 |
| 319 | Surfkiss | Karoryfer Samples | sfzinstruments | 商业授权 / 付费产品 | guitar | 商业授权 / 需付费购买 |
| 320 | Baconwulf | Karoryfer Samples | sfzinstruments | 商业授权 / 付费产品 | guitar | 商业授权 / 需付费购买 |
| 321 | Secret Agent Bass | Karoryfer Samples | sfzinstruments | 商业授权 / 付费产品 | guitar | 商业授权 / 需付费购买 |
| 322 | Snowkiss Guitar | Karoryfer Samples | sfzinstruments | 商业授权 / 付费产品 | guitar | 商业授权 / 需付费购买 |
| 323 | VG Soul Trumpet | VGTrumpet | sfzinstruments | 商业授权 / 付费产品 | orch | 商业授权 / 需付费购买 |
| 324 | VG Trumpet Harmon muted | VGTrumpet | sfzinstruments | 商业授权 / 付费产品 | orch | 商业授权 / 需付费购买 |
| 325 | VG Trombone | VGTrumpet | sfzinstruments | 商业授权 / 付费产品 | orch | 商业授权 / 需付费购买 |
| 326 | VG Soprano Saxophone | VGTrumpet | sfzinstruments | 商业授权 / 付费产品 | orch | 商业授权 / 需付费购买 |
| 327 | VG Tenor Saxophone | VGTrumpet | sfzinstruments | 商业授权 / 付费产品 | orch | 商业授权 / 需付费购买 |
| 328 | VG Clarinet | VGTrumpet | sfzinstruments | 商业授权 / 付费产品 | orch | 商业授权 / 需付费购买 |
| 329 | VG Flugelhorn | VGTrumpet | sfzinstruments | 商业授权 / 付费产品 | orch | 商业授权 / 需付费购买 |
| 330 | VG Alto Saxophone | VGTrumpet | sfzinstruments | 商业授权 / 付费产品 | orch | 商业授权 / 需付费购买 |
| 331 | Vengeful Viola | Karoryfer Samples | sfzinstruments | 商业授权 / 付费产品 | orch | 商业授权 / 需付费购买 |
| 332 | Vengeful Violin | Karoryfer Samples | sfzinstruments | 商业授权 / 付费产品 | orch | 商业授权 / 需付费购买 |
| 333 | Merciful Cello | Karoryfer Samples | sfzinstruments | 商业授权 / 付费产品 | orch | 商业授权 / 需付费购买 |
| 334 | Strange String Summer | Karoryfer Samples | sfzinstruments | 商业授权 / 付费产品 | orch | 商业授权 / 需付费购买 |
| 335 | Vengeful Cello | Karoryfer Samples | sfzinstruments | 商业授权 / 付费产品 | orch | 商业授权 / 需付费购买 |
| 336 | Vengeful Bass | Karoryfer Samples | sfzinstruments | 商业授权 / 付费产品 | orch | 商业授权 / 需付费购买 |
| 337 | All SFZ Bundle | VGTrumpet | sfzinstruments | 商业授权 / 付费产品 | orch | 商业授权 / 需付费购买 |
| 338 | Harps | Garritan | sfzinstruments | 商业授权 / 付费产品 | orch | 商业授权 / 需付费购买 |
| 339 | Instant Orchestra | Garritan | sfzinstruments | 商业授权 / 付费产品 | orch | 商业授权 / 需付费购买 |
| 340 | Personal Orchestra 5 | Garritan | sfzinstruments | 商业授权 / 付费产品 | orch | 商业授权 / 需付费购买 |
| 341 | Concert and Marching Band 2 | Garritan | sfzinstruments | 商业授权 / 付费产品 | other | 商业授权 / 需付费购买 |
| 342 | Classic Series Collection | Versilian Studios LLC | sfzinstruments | 商业授权 / 付费产品 | other | 商业授权 / 需付费购买 |
| 343 | Orcophony | Karoryfer Samples | sfzinstruments | 商业授权 / 付费产品 | other | 商业授权 / 需付费购买 |
| 344 | Classic Pipe Organs | Garritan | sfzinstruments | 商业授权 / 付费产品 | other | 商业授权 / 需付费购买 |
| 345 | Jazz and Big Band 3 | Garritan | sfzinstruments | 商业授权 / 付费产品 | other | 商业授权 / 需付费购买 |
| 346 | The Halfling | Production Voices | sfzinstruments | 商业授权 / 付费产品 | other | 商业授权 / 需付费购买 |
| 347 | PiAnnette | fisound | sfzinstruments | 商业授权 / 付费产品 | piano | 商业授权 / 需付费购买 |
| 348 | Estate Grand | Production Voices | sfzinstruments | 商业授权 / 付费产品 | piano | 商业授权 / 需付费购买 |
| 349 | CFX Concert Grand | Garritan | sfzinstruments | 商业授权 / 付费产品 | piano | 商业授权 / 需付费购买 |
| 350 | CFX Lite | Garritan | sfzinstruments | 商业授权 / 付费产品 | piano | 商业授权 / 需付费购买 |
| 351 | Concert Grand Compact | Production Voices | sfzinstruments | 商业授权 / 付费产品 | piano | 商业授权 / 需付费购买 |
| 352 | Death Piano | Production Voices | sfzinstruments | 商业授权 / 付费产品 | piano | 商业授权 / 需付费购买 |
| 353 | Electric V | Production Voices | sfzinstruments | 商业授权 / 付费产品 | piano | 商业授权 / 需付费购买 |
| 354 | Production Grand Compact | Production Voices | sfzinstruments | 商业授权 / 付费产品 | piano | 商业授权 / 需付费购买 |
| 355 | Dandelion Witch | Karoryfer Samples | sfzinstruments | 商业授权 / 付费产品 | vocal | 商业授权 / 需付费购买 |
| 356 | Hadziha | Karoryfer Samples | sfzinstruments | 商业授权 / 付费产品 | vocal | 商业授权 / 需付费购买 |
| 357 | Hster | Karoryfer Samples | sfzinstruments | 商业授权 / 付费产品 | vocal | 商业授权 / 需付费购买 |
| 358 | Torgbe | Karoryfer Samples | sfzinstruments | 商业授权 / 付费产品 | vocal | 商业授权 / 需付费购买 |
| 359 | Hadzi-Hevi | Karoryfer Samples | sfzinstruments | 商业授权 / 付费产品 | vocal | 商业授权 / 需付费购买 |
| 360 | Hadzi-Fia | Karoryfer Samples | sfzinstruments | 商业授权 / 付费产品 | vocal | 商业授权 / 需付费购买 |
| 361 | The Megalovania Library V2 (FL Studio Mobile Compatible) | Micasddsa | musical-artifacts | 版权受限 | other | 版权受限（原权利人保留全部权利） |
| 362 | CT-7000 (Retro Synth) [Free Version] | Michael Picher | musical-artifacts | 版权受限 | game | 版权受限（原权利人保留全部权利） |
| 363 | Among Us Soundfont | Inky Nic | musical-artifacts | 版权受限 | game | 版权受限（原权利人保留全部权利） |
| 364 | Vintage Dreams Waves v 2.0 Soundfont | Ian Wilson | musical-artifacts | 版权受限 | synth | 版权受限（原权利人保留全部权利） |
| 365 | Cave Story Soundfont | Pixel | musical-artifacts | 版权受限 | game | 版权受限（原权利人保留全部权利） |
| 366 | Wurlitzer Soundfont | John R. Tay | musical-artifacts | 版权受限 | other | 版权受限（原权利人保留全部权利） |
| 367 | Wii Grand Piano (Sampled) | Created and ripped by MrSa | musical-artifacts | 版权受限 | game | 版权受限（原权利人保留全部权利） |
| 368 | Binaural Upright Piano | Michael Picher | musical-artifacts | 版权受限 | piano | 版权受限（原权利人保留全部权利） |
| 369 | Casio SA-76 (+GM Soundfont) | Casio Computer Co., Underx | musical-artifacts | 版权受限 | hist | 版权受限（原权利人保留全部权利） |
| 370 | SF2 Comp "GM" | Unknown | musical-artifacts | 版权受限 | other | 版权受限（原权利人保留全部权利） |
| 371 | Shreddage Zero | Unknown Creator For Soundf | musical-artifacts | 版权受限 | guitar | 版权受限（原权利人保留全部权利） |
| 372 | HS Synthetic Electronic v1.0 Soundfont | Thomas Hammer | musical-artifacts | 版权受限 | hist | 版权受限（原权利人保留全部权利） |
| 373 | HS Synth Collection I Soundfont | Thomas Hammer | musical-artifacts | 版权受限 | hist | 版权受限（原权利人保留全部权利） |
| 374 | TR-808 Drums Soundfont | Thomas Hammer | musical-artifacts | 版权受限 | drum | 版权受限（原权利人保留全部权利） |
| 375 | Ana gaby voice, Soundfont version. | Milton  Paredes, mpj facto | musical-artifacts | 版权受限 | vocal | 版权受限（原权利人保留全部权利） |
| 376 | HS TB-303 Soundfont | Thomas Hammer | musical-artifacts | 版权受限 | hist | 版权受限（原权利人保留全部权利） |
| 377 | Shreddage Soundfont Beta | Unknown Creator For Soundf | musical-artifacts | 版权受限 | guitar | 版权受限（原权利人保留全部权利） |
| 378 | amiga st20 lite soundfont | respective autorhts, and m | musical-artifacts | 版权受限 | game | 版权受限（原权利人保留全部权利） |
| 379 | HS Strings Soundfont | Thomas Hammer | musical-artifacts | 版权受限 | hist | 版权受限（原权利人保留全部权利） |
| 380 | Xhomie3 - Drums For Dubstep And HardStyle (SoundFonts) with  | Xhomie3 | musical-artifacts | 版权受限 | drum | 版权受限（原权利人保留全部权利） |
| 381 | HS M1 Drums Soundfont | Thomas Hammer | musical-artifacts | 版权受限 | drum | 版权受限（原权利人保留全部权利） |
| 382 | HS Pads and Textures II Soundfont | Thomas Hammer | musical-artifacts | 版权受限 | synth | 版权受限（原权利人保留全部权利） |
| 383 | HS Linn Drums Soundfont | Thomas Hammer | musical-artifacts | 版权受限 | drum | 版权受限（原权利人保留全部权利） |
| 384 | Kururin Paradise Soundfont | Nintendo/Eighting, ripped  | musical-artifacts | 版权受限 | gm | 版权受限（原权利人保留全部权利） |
| 385 | Cuckoo's Taped Piano SFZ (wav version) | Cuckoo Music | musical-artifacts | 版权受限 | piano | 版权受限（原权利人保留全部权利） |
| 386 | HS Boss DR-550 Drums Soundfont | Thomas Hammer | musical-artifacts | 版权受限 | drum | 版权受限（原权利人保留全部权利） |
| 387 | HS Acoustic Percussion Soundfont | Thomas Hammer | musical-artifacts | 版权受限 | drum | 版权受限（原权利人保留全部权利） |
| 388 | HS R8 Drums Soundfont | Thomas Hammer | musical-artifacts | 版权受限 | drum | 版权受限（原权利人保留全部权利） |
| 389 | Nena, gm soundfont set | Milton Paredes, mpj factor | musical-artifacts | 版权受限 | ethnic | 版权受限（原权利人保留全部权利） |
| 390 | Magic Techno Drums Soundfont | Thomas Hammer | musical-artifacts | 版权受限 | drum | 版权受限（原权利人保留全部权利） |
| 391 | HS African Percussion Soundfont | Thomas Hammer | musical-artifacts | 版权受限 | drum | 版权受限（原权利人保留全部权利） |
| 392 | Bassoon Ethan Nando | Ethan Winer | musical-artifacts | 版权受限 | guitar | 版权受限（原权利人保留全部权利） |
| 393 | HS Pads and Textures I Soundfont | Thomas Hammer | musical-artifacts | 版权受限 | synth | 版权受限（原权利人保留全部权利） |
| 394 | Bejeweled 3 Samples (Soundfont) | Peter Hajba & Alexander Br | musical-artifacts | 版权受限 | orch | 版权受限（原权利人保留全部权利） |
| 395 | HS Vox Soundfont | Thomas Hammer | musical-artifacts | 版权受限 | vocal | 版权受限（原权利人保留全部权利） |
| 396 | Bejeweled 3 Percussions (Soundfont) | Peter Hajba & Alexander Br | musical-artifacts | 版权受限 | drum | 版权受限（原权利人保留全部权利） |
| 397 | Cuckoo's Taped Piano SFZ (flac version) | Cuckoo Music | musical-artifacts | 版权受限 | piano | 版权受限（原权利人保留全部权利） |
| 398 | HS StarTrekFX Soundfont | Thomas Hammer | musical-artifacts | 版权受限 | sfx | 版权受限（原权利人保留全部权利） |
| 399 | Tonewheel Organ and MORE!! | Michael Picher | musical-artifacts | 版权受限 | piano | 版权受限（原权利人保留全部权利） |
| 400 | RCKTNEO SND316X soundfont (beta version, read description fo | RCKTNEO | musical-artifacts | 版权受限 | synth | 版权受限（原权利人保留全部权利） |
| 401 | Famicom Detective Club | Nintendo | musical-artifacts | 版权受限 | game | 版权受限（原权利人保留全部权利） |
| 402 | RE Library Manager 1.0 | Rick Blues from RE MEDIA P | musical-artifacts | 版权受限 | other | 版权受限（原权利人保留全部权利） |
| 403 | Native Instruments - Brass ensemble And Strings ensemble Sou | Xhomie3 or XNX team | musical-artifacts | 版权受限 | other | 版权受限（原权利人保留全部权利） |
| 404 | WTBleep | Sampled by Shiru 08'2019 | musical-artifacts | 版权受限 | game | 版权受限（原权利人保留全部权利） |
| 405 | SME Sequencer 2.0 | Rick Blues from RE MEDIA P | musical-artifacts | 版权受限 | other | 版权受限（原权利人保留全部权利） |
| 406 | SME Studio 1.0 | Rick Blues from RE MEDIA P | musical-artifacts | 版权受限 | other | 版权受限（原权利人保留全部权利） |
| 407 | Anaconda (Genesis) Soundfont | Mildanner, DevWorks Game T | musical-artifacts | 版权受限 | game | 版权受限（原权利人保留全部权利） |
| 408 | Korg TRITON Techno Rock Organ Soundfont | Mildanner, KORG | musical-artifacts | 版权受限 | hist | 版权受限（原权利人保留全部权利） |
| 409 | A LOT OF NEW INSTRUMENTS HERE! | Rick Blues from RE MEDIA P | musical-artifacts | 版权受限 | other | 版权受限（原权利人保留全部权利） |
| 410 | MPJ sound escentials for kontakt | Milton paredes, Mpj factor | musical-artifacts | 版权受限 | other | 版权受限（原权利人保留全部权利） |
| 411 | Our FIRST DAW--SME(Soundfont MIDI Editor) SEQUENCER EDITION! | Rick Blues from RE MEDIA P | musical-artifacts | 版权受限 | other | 版权受限（原权利人保留全部权利） |
| 412 | House Piano's soundfont version | Xhomie3 | musical-artifacts | 版权受限 | piano | 版权受限（原权利人保留全部权利） |
| 413 | Epic Tom | Unreal Instruments | sfzinstruments | 自定义许可（未明） | drum | 自定义许可，条款未明 → **许可不明即不收录** |
| 414 | Kitchen X | Unreal Instruments | sfzinstruments | 自定义许可（未明） | drum | 自定义许可，条款未明 → **许可不明即不收录** |
| 415 | Wind Chime | Unreal Instruments | sfzinstruments | 自定义许可（未明） | drum | 自定义许可，条款未明 → **许可不明即不收录** |
| 416 | Koto | Unreal Instruments | sfzinstruments | 自定义许可（未明） | ethnic | 自定义许可，条款未明 → **许可不明即不收录** |
| 417 | 1912 | Unreal Instruments | sfzinstruments | 自定义许可（未明） | ethnic | 自定义许可，条款未明 → **许可不明即不收录** |
| 418 | Standard Bass | Unreal Instruments | sfzinstruments | 自定义许可（未明） | guitar | 自定义许可，条款未明 → **许可不明即不收录** |
| 419 | Standard Guitar | Unreal Instruments | sfzinstruments | 自定义许可（未明） | guitar | 自定义许可，条款未明 → **许可不明即不收录** |
| 420 | The Slapper | Unreal Instruments | sfzinstruments | 自定义许可（未明） | guitar | 自定义许可，条款未明 → **许可不明即不收录** |
| 421 | Metal GTX | Unreal Instruments | sfzinstruments | 自定义许可（未明） | guitar | 自定义许可，条款未明 → **许可不明即不收录** |
| 422 | Sonatina Symphonic Orchestra | Mattias Westlund | MuseScore | 自定义许可（未明） | orch | 自定义许可，条款未明 → **许可不明即不收录** |
| 423 | Maestro Concert Grand Piano | Mats Helgesson | sfzinstruments | 自定义许可（未明） | piano | 自定义许可，条款未明 → **许可不明即不收录** |
| 424 | Pablemo 2020 | Pablemo | musical-artifacts | 未识别许可码 falv13 | game | **许可码未识别**（`falv13`）→ 不猜、不收录 |
| 425 | Alesis Drum Module 4 SoundFont | VentusArranger | musical-artifacts | 未识别许可码 falv13 | drum | **许可码未识别**（`falv13`）→ 不猜、不收录 |
| 426 | Clay Fighter 63 1/3 NOW HAVE A SOUNDFONT!!! | JJ MH | musical-artifacts | 未识别许可码 falv13 | game | **许可码未识别**（`falv13`）→ 不猜、不收录 |
| 427 | Custom Drums by JJ MH | JJ MH | musical-artifacts | 未识别许可码 falv13 | game | **许可码未识别**（`falv13`）→ 不猜、不收录 |
| 428 | Northern Trumpets | VGTrumpet | sfzinstruments | 标注 Free 但未指明许可 | orch | 标注 Free 但未指明具体许可 → 视为许可不明 |
| 429 | G1 | TKDrums | sfzinstruments | Freemium（免费增值） | drum | 免费增值（免费版许可不明） |
| 430 | L1 | TKDrums | sfzinstruments | Freemium（免费增值） | drum | 免费增值（免费版许可不明） |
| 431 | The Ultimate Megadrive Soundfont | TheEighthBit | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 432 | [REUPLOAD] The DEFINITIVE MEGALOVANIA Soundfont! V1.17 | DannieloCQ Music! | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 433 | 8bitSF ( The Nes Soundfont ) | TheEighthBit | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 434 | Default Windows MIDI Soundfont | Roland / Microsoft Corpora | musical-artifacts | 站点自标「存疑」 | other | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 435 | Super Nintendo Entertainment System General MIDI Soundfont | dotsarecool | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 436 | Edirol SD-90 Pack I (Complete) | rosntdoxot, DrKoupop, Spoo | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 437 | Earthbound Soundfont | SleepyTimeJesse | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 438 | NEW! Mother 3 Soundfont 2023 Update (1.0) | Shigisato Itoi & Nintendo | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 439 | KORG M1 GM soundfont Second Beta | Various artists | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 440 | Super Mario World (Full version) | MrSanic | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 441 | New Super Mario Bros DS Soundfont | M. Reza Khadafi | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 442 | The Ultimate Wii Soundfont | Mr.Sanic | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 443 | MOTHER 3 Soundfont | fluidvolt | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 444 | MEGALOVANIA (Shreddage) Bass Guitar Soundfont [Bigger range] | ASmolBoy | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 445 | SNES Mario Paint Soundfont 2.0 | ASmolBoy | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 446 | THE WORLD REVOLVING Soundfont (From DELTARUNE) | ASmolBoy | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 447 | HQ Orchestral Soundfont Collection | Unknown | musical-artifacts | 站点自标「存疑」 | orch | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 448 | Crisis 3.51 GM Soundfont [UNOFFICIAL UPDATE FROM CrisisGener | SonicLover 19 | musical-artifacts | 站点自标「存疑」 | gm | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 449 | KEYGEN / CHIPTUNE Soundfont | ASmolBoy | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 450 | Mother 1+2 (Game Boy Advance) Soundfont (1.0) | Wrapped | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 451 | Earthbound/Megalovania restored Overdrive Guitar | The guy2 | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 452 | Legend of Zelda: Majora's Mask Soundfont | exciter | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 453 | -Sonic The Hedgehog 2- | Mr.Sanic | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 454 | Mario Kart 64 Soundfont | M. Reza Khadafi | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 455 | Super Smash Bros 64 Soundfont | M. Reza Khadafi | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 456 | Chrono Trigger Soundfont | Mathew Valente [TSSF] | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 457 | jRhodes 1977 Mark | Learjeff | musical-artifacts | 站点自标「存疑」 | piano | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 458 | EarthBound Soundfont (2012) (Unused Instruments) | ASmolBoy, SleepyTimeJesse | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 459 | Kirby Super Star soundfont | fluidvolt | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 460 | The Beepbox Soundfont | Micasddsa4000 | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 461 | (OUTDATED) Roxie's Nintendo 64 General MIDI Soundfont | IkaMusumeYiyaRoxie | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 462 | Super Mario World Soundfont | Blitz Lunar | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 463 | SNES Plok Soundfont (V1.02) | ASmolBoy | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 464 | SEGA Samples | Zackie | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 465 | Kirby Super Star Ultra DS Soundfont | M. Reza Khadafi | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 466 | Mega Man X Soundfont | Blitzlunar | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 467 | WarioWare D.I.Y. Soundfont | M. Reza Khadafi | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 468 | Kiarchive (Soundfont Version) | Sodichi | musical-artifacts | 站点自标「存疑」 | other | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 469 | Bomberman Hero soundfont | HandlebarOrionX | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 470 | Banjo Kazooie Donkey Kong 64 Banjo Tooie Diddy Kong Racing S | M. Reza Khadafi | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 471 | Mario Kart Wii Soundfont | Mr.Sanic | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 472 | Mario & Luigi: Superstar Saga | Nintendo | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 473 | Cave Story Soundfont (OrgMaker) | ASmolBoy | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 474 | Famicom Soundfont | Kitt | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 475 | Sonic Spinball (Soundfont) | Mr.Sanic | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 476 | Pokemon Emerald XQ++ SC-88Pro Soundfont (read description) | stgiga, Zandro Reville, GA | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 477 | Android System Synth | Yamaha Corporation (1998) | musical-artifacts | 站点自标「存疑」 | other | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 478 | TrianGMGS Soundfont | Thomas K. | musical-artifacts | 站点自标「存疑」 | orch | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 479 | Yamaha TX16w GM compatible soundfont | McCheeseBob | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 480 | Kirby 64 Soundfont | fluidvolt | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 481 | Wii System Menu SoundFont | MrSanic | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 482 | Donkey Kong Country Soundfont Collection | William Kage | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 483 | SeinFont (The Seinfeld Soundfont) | ASmolBoy | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 484 | SNES Kirby's Dream Course Soundfont (V1.1) | ASmolBoy | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 485 | Mega Man Soundfont | Capcom | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 486 | Kirby 64 The Crystal Shards Soundfont | M. Reza Khadafi | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 487 | SILENT HILL (PS1) Midis + Soundfonts | Nolann59860 | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 488 | The Legend of Zelda Spirit Tracks DS Soundfont | M. Reza Khadafi | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 489 | Teenage Mutant Ninja Turtles 4: Turtles in Time Soundfont | Ehehe~ | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 490 | Super Mario World HD soundfont (UPDATED: v1.1) | justsomegal | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 491 | Realistic SF V2 | SonicLover 19 | musical-artifacts | 站点自标「存疑」 | other | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 492 | Sonic the Hedgehog 4: Episode 1 Soundfont + midis | Nolann59860 | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 493 | Super Mario Advance 4 | Dekyo Ongen | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 494 | Wii U Soundfont | Mr.Sanic | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 495 | ebhalloween002 | Toby Fox and Nintendo | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 496 | Bass Legends (Spectrasonics) | shrodedokaedro | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 497 | Glover 64 Soundfont | fluidvolt | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 498 | Mario Party DS Soundfont | M. Reza Khadafi | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 499 | Animal Crossing Nintendo 64/GameCube Soundfont Demo W.I.P. | IkaMusumeYiyaRoxie | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 500 | The Ultimate Piano Collection (East West) | shrodedokaedro | musical-artifacts | 站点自标「存疑」 | piano | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 501 | Sonic Jam Soundfont | type_a | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 502 | (sf2) Kontakt Factory Library - Pop Drums | Kontakt 6 Player / Native  | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 503 | Super Metroid Soundfont | Brian Crawford | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 504 | (OUTDATED, See Desc.) SNES Mario Paint Soundfont | Lil'Alien | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 505 | Super Mario Kart Soundfont | Blitz Lunar | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 506 | Splendid piano (136 MB) | High quality sfs | musical-artifacts | 站点自标「存疑」 | piano | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 507 | Yoshi's Island Soundfont | William Kage | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 508 | Roland JV-1010 GM Soundfont | Thomas K. | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 509 | SILENT HILL 2 (PS2) Midis + Soundfonts | Nolann59860 | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 510 | Star Fox 64 Soundfont | M. Reza Khadafi | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 511 | NES Sunsoft DPCM Bass Soundfont | ASmolBoy | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 512 | Super Mario RPG Soundfont | Mike Crain | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 513 | Mario & Luigi Partners in Time Soundfont | M. Reza Khadafi | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 514 | Pokemon: Ruby/Sapphire/Emerald [GBA] | Exabyte U | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 515 | Retro Synth PC | SONiVOX | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 516 | Nintendo Medley Soundfont | hakerg | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 517 | Rugrats Search For Reptar (Playstation 1) Soundfont | Wrapped | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 518 | Rock Bass | Edirol | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 519 | Groove Agent 3 Pack | Steinberg | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 520 | Roland EDIROL SD-90 Intim8String | Hayde | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 521 | TLoZ: A Link To The Past | Mr.Sanic | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 522 | Korg AG-10 GM Soundfont | Thomas K. | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 523 | Proteus GM soundfont | SonicLover 19 | musical-artifacts | 站点自标「存疑」 | gm | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 524 | Twilight Princess | Anonymous | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 525 | GoldenEye 64 Soundfont (N64Vault.com Versión) | JJ MH (RePost ir N64Vault. | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 526 | Kirby Mass Attack DS Soundfont | M. Reza Khadafi | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 527 | Nine Hours, Nine Persons, Nine Doors - Soundfonts + MIDIs | Ed_IT | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 528 | Sonic 3 Credits Soundfont and Samples | ElPavo613 | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 529 | Square Soundfont | Steven Rhodes | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 530 | Rockman & Forte Soundfont | fluidvolt | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 531 | Rock Man X/X2 Soundfont | Harumi Makoto | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 532 | Final Fantasy 6 Soundfont | Vienna Master | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 533 | Kirby's Dream Land 3 Soundfont | Blitz Lunar | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 534 | Diddy Kong Racing Nintendo 64 Soundfont | M. Reza Khadafi | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 535 | Minecraft GM Soundfont 1.1.1 | HYWT | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 536 | Jazz Bass | Edirol | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 537 | Mega Man Battle Network 5 DS Soundfont | M. Reza Khadafi | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 538 | The Legend of Zelda Phantom Hourglass DS Soundfont | M. Reza Khadafi | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 539 | South Park N64 Sountfont | IkaMusumeYiyaRoxie | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 540 | The Kawasaki Sax-A-Boom Soundfont (Jack Black) | Wrapped | musical-artifacts | 站点自标「存疑」 | wind | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 541 | Doom SNES Soundfont | Patricio Herrera | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 542 | Steve Stevens Guitar Samples Collection (East West) | shrodedokaedro | musical-artifacts | 站点自标「存疑」 | guitar | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 543 | Zelda A Link to The Past Soundfont | Blitz Lunar | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 544 | Ephesus GM v1.00 [WIP] | Simone Piervergili | musical-artifacts | 站点自标「存疑」 | gm | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 545 | Fire Emblem 8: The Sacred Stones Soundfont | circleseverywhere | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 546 | Diddy Kong Racing Nintendo DS Soundfont | M. Reza Khadafi | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 547 | WCW/NWO Revenge soundfont | HandlebarOrionX | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 548 | Pokemon: Firered/Leafgreen [GBA] | Exabyte U | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 549 | Earthworm Jim DSi Soundfont 2017 | M. Reza Khadafi | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 550 | F-Zero X (N64) Percussion Soundfont | Stephen Bereznicki | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 551 | Kirby Squeak Squad Soundfont | M. Reza Khadafi | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 552 | FatBoy-v0.786 | Simone Piervergili, Chris  | musical-artifacts | 站点自标「存疑」 | other | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 553 | Wario Ware: Smooth Moves Soundfont (W.I.P) | Mr.Sanic | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 554 | Nokia 30 Soundfont | Bryan Bilocura | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 555 | (OUTDATED, See Desc.) Seinfeld (Korg M1) Slap Bass Soundfont | Lil'Alien | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 556 | Setzer's SPC Soundfont Soundfont | Setzer | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 557 | Street Fighter 2 CPS1 Drum/Percussion Kit | Stephen Bereznicki | musical-artifacts | 站点自标「存疑」 | drum | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 558 | Secret of Mana Soundfont | Blitz Lunar | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 559 | Yoshi Island DS Soundfont | M. Reza Khadafi | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 560 | Samsung One UI 5.0 sounds | Samsung | musical-artifacts | 站点自标「存疑」 | piano | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 561 | Cookie Run: Ovenbreak Soundfont (.zip, includes SF2 & DLS) | luna (+squib, unknown - og | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 562 | F-Zero Soundfont | Blitz Lunar | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 563 | Zelda The Minish Cap Soundfont | Mathew Valente [TSSF] | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 564 | nylon guitar V3 soundfont | TheSoundfontMaker | musical-artifacts | 站点自标「存疑」 | other | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 565 | Yamaha YPT 220 piano V4 - fixed | TheSoundfontMaker | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 566 | Mario Hoops 3 on 3 DS Soundfont | M. Reza Khadafi | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 567 | Ghost Trick: Phantom Detective DS Soundfont Rip | Ed_IT | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 568 | Illusion of Gaia Soundfont | Felix Flywheel | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 569 | Mario VS Donkey Kong Mini Land Mayhem DS Soundfont | M. Reza Khadafi | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 570 | Pootis Soundfont | IkaMusumeYiyaRoxie | musical-artifacts | 站点自标「存疑」 | other | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 571 | The Legend Zelda Four Swords Anniversary Edition DSi Soundfo | M. Reza Khadafi | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 572 | CP80 (Yamaha PSR-SX700) | Simone Piervergili | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 573 | NES Soundfont V1.0 | iand255 | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 574 | Mystical Ninja Starring Goemon Soundfont | Blitz Lunar | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 575 | Fairlight CMI IIx GM compatible soundfont | McCheeseBob | musical-artifacts | 站点自标「存疑」 | gm | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 576 | Mario Paint Composer Nes Soundfont | Awpwr | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 577 | Kirby Canvas Curse DS Soundfont | M. Reza Khadafi | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 578 | Mii Channel Soundfont | Kazumi Totaka, Ripped By B | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 579 | Castlevania - Harmony of Dissonance Soundfont | Teuthida | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 580 | Yoshi Touch And Go DS Soundfont | M. Reza Khadafi | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 581 | Super Bomberman 2, 3, 4 , 5 Soundfont | Dont / YFU | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 582 | Fat-Man OPL-2 v2 Soundfont | George "The Fat Man" Sange | musical-artifacts | 站点自标「存疑」 | other | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 583 | Bomberman 64 The Second Attack soundfont | HandlebarOrionX | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 584 | Industrial Dance PC | SONiVOX | musical-artifacts | 站点自标「存疑」 | other | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 585 | Diddy Kong Racing Nintendo DS Soundfonts 2017 | M. Reza Khadafi | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 586 | Star Fox Soundfont | iteachvader | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 587 | SNES Rock n' Roll Racing Soundfont (and WAV pack) | ASmolBoy | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 588 | SD-90 SP1 004 Atomstrings | Hayde | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 589 | Samsung 2020 soundfont | TheSoundfontMaker | musical-artifacts | 站点自标「存疑」 | piano | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 590 | Cooking Mama Series Nintendo DS Official Soundfont | M. Reza Khadafi | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 591 | St.Concert | Edirol | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 592 | Puyo Puyo ~ n Soundfont [v 0.1] | Nintedo [ripped by Sozuke] | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 593 | Rugrats: Scavenger Hunt (Nintendo 64) Soundfont | Wrapped | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 594 | Hip-Hop | Steinberg | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 595 | Mario VS Donkey Kong 2 March of the Minis DS Soundfont | M. Reza Khadafi | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 596 | SD-90 SP1 005 Noo Tongs | Hayde | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 597 | The ULTIMATE LeapFrog Leap-font (4 Instrument Packs in 1 fil | Richard Marriott, Brad Ful | musical-artifacts | 站点自标「存疑」 | other | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 598 | Rushing Beat Shura (SFC) SoundFont | Dekyo Ongen | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 599 | SNES Alcahest Soundfont (and WAV pack) | ASmolBoy | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 600 | Rugrats in Paris: The Movie (Nintendo 64) Soundfont 1.0. 1 | Wrapped | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 601 | Kirby Dreamland 3 SNES GM Soundfont | M. Reza Khadafi | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 602 | Mario Kart 64 DLS Soundfont | M. Reza Khadafi | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 603 | Pingas Soundfont | IkaMusumeYiyaRoxie | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 604 | LiLVintage Soundfont | Thomas K. | musical-artifacts | 站点自标「存疑」 | other | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 605 | Battletoads: Battlemaniacs Soundfont | fluidvolt | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 606 | SD-90 SP1 001 D.L.A.Pad | Hayde | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 607 | Drill Dozer Soundfont | fluidvolt | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 608 | Conker Soundfont Collection | SonicLover 19 | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 609 | The Grand 3 Model D Close | Unknown | musical-artifacts | 站点自标「存疑」 | other | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 610 | SNES Bubsy in Claws Encounters of the Furred Kind Soundfont | ASmolBoy | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 611 | Blast Corps Nintendo 64 Soundfont | M. Reza Khadafi | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 612 | Final Fantasy: Mystic Quest Soundfont | Zetshiro | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 613 | Chrome Song Maker Soundfont | I don't know. | musical-artifacts | 站点自标「存疑」 | other | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 614 | Groove Agent 4/5 - Elementic | Unknown | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 615 | Doraemon - Nobita to Mittsu no Seireiseki Soundfont W.I.P | IkaMusumeYiyaRoxie | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 616 | WCW/NWO World Tour/Virtual Pro Wrestling 64  soundfont | HandlebarOrionX | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 617 | Final Fantasy 5 Soundfont | Mathew Valente [TSSF] | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 618 | Style Savvy Soundfont (Updated) | Atsuhiro Motoyama | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 619 | Burning Grooves (Spectrasonics) FIXED Cutoff | shrodedokaedro | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 620 | Triebwerk - Drum Kit 6 | Unknown | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 621 | 64 Trump Collection Soundfont | M. Reza Khadafi | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 622 | Groove Agent 4/5 - 8Bit | Unknown | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 623 | Buck Bumble soundfont | HandlebarOrionX | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 624 | LeapFrog Leap-font Complete Instrument Bundle (1999-2007) | LuckyPrincess (under LeapF | musical-artifacts | 站点自标「存疑」 | other | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 625 | TerrariaInstrumentPackV1 | Eternal Wonder | musical-artifacts | 站点自标「存疑」 | other | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 626 | SD-90 SP1 003 Xtremities | Hayde | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 627 | HALion Sonic - Beauty Pop Bell | Unknown | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 628 | Castlevania: Dracula X Soundfont | Patricio Herrera | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 629 | Super Castlevania 4 Soundfont | Mike Crain | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 630 | Final Fantasy 4 Soundfont | Mathew Valente [TSSF] | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 631 | Wonder Project J2: Cloro no Mori no Josette | IkaMusumeYiyaRoxie | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 632 | Rugrats: I Gotta Go Party (Game Boy Advance) Soundfont 1.0 | Wrapped | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 633 | Star Fox SNES GM Soundfont | M. Reza Khadafi | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 634 | Groove Agent ONE - Elecktro Kit | Steinberg | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 635 | SD-90 SP1 002 BrushingSaw | Hayde | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 636 | Hebereke's Popoon Soundfont v1.2 | LucianoTheWindowsFan | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 637 | Final Fantasy 8 Demo Disc Soundfont | Mathew Valente [TSSF] | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 638 | Romancing SaGa 3 | _Scribbly | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 639 | Magic Castle (PS1) Soundfont | Sodichi | musical-artifacts | 站点自标「存疑」 | other | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 640 | Groove Agent 4/5 - Dam Hard | Unknown | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 641 | Jurassic Park (SNES) Soundfont | deinolite | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 642 | SILENT HILL 3 (PS2) MIDIs and SF2s | Nolann59860 | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 643 | Yoshi's Island Small samples Collection | Mr.Sanic | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 644 | Groove Agent 4/5 - Ambiences | Unknown | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 645 | NONNTUTTI SoundFont | Simone Piervergili | musical-artifacts | 站点自标「存疑」 | gm | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 646 | SNES U.N. Squadron Soundfont (and WAV pack) | ASmolBoy | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 647 | Pilotwings Soundfont | fluidvolt | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 648 | SILENT HILL 4 THE ROOM (Windows) Soundfonts | Nolann59860 | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 649 | Kirby & The Amazing Mirror [GBA] | Exabyte U | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 650 | Cooking Mama DS Sound Rip SFX Collection | M. Reza Khadafi | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 651 | EMU Liveware ESC SoundFont Library | E-MU Systems | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 652 | Fire Emblem: Genealogy of the Holy War Soundfont | Mahmoud Ehab, EpitaphEpito | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 653 | Harvest Moon Soundfont | fluidvolt | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 654 | Battletoads and Double Dragon Soundfont | fluidvolt | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 655 | Magical Drop Soundfont | fluidvolt | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 656 | Secret of Evermore Soundfont | William Kage | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 657 | Kirby: Nightmare in Dreamland [GBA] | Exabyte U | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 658 | GenieVoice GM64Pro 2.0 - All Sets | Simone Piervergili, Studio | musical-artifacts | 站点自标「存疑」 | other | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 659 | Diddy Kong Racing DS Sound Rip SFX Collection | M. Reza Khadafi | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 660 | Mighty Morphin Power Rangers Soundfont | Patricio Herrera | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 661 | Carnival Games DS Soundfont | Salutanis Orkonus | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 662 | (outdated) PrismSynth | Vini (2) | musical-artifacts | 站点自标「存疑」 | synth | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 663 | LIT (Wiiware) Soundfont + Midis | Nolann59860 | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 664 | Sounds of the Learning Screen and Fridge DJ (Learning Screen | Richard Marriott, Brad Ful | musical-artifacts | 站点自标「存疑」 | other | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 665 | Piano Tiles Soundfont | Cab | musical-artifacts | 站点自标「存疑」 | piano | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 666 | Mario Kart DS Credits Soundfont | Shinobu Nagata, Makarthenu | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 667 | Contra 3: The Alien Wars Soundfont | Patricio Herrera | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 668 | Game Watch DSi Collection Soundfont | M. Reza Khadafi | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 669 | Music MonStars (DS) Soundfont | JappaWakka | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 670 | Kingdom Hearts: Chain of Memories [GBA] | Exabyte U | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 671 | Scooby Doo 2: Monsters Unleashed [GBA] SoundFont | nickboy6 | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 672 | Giana Sisters DS / 2D Soundfonts | Poké-Brother | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 673 | Sim City Soundfont | Mike Crain | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 674 | Tales of Phantasia Soundfont | Christian Esquivel | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 675 | Super Bomberman Soundfont | Blitz Lunar | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 676 | Final Fantasy I & II : Dawn of Souls [GBA] | Exabyte U | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 677 | AliceGM v1.1 | Alice "Radiomicrowave" S.S | musical-artifacts | 站点自标「存疑」 | gm | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 678 | X-Men: Mutant Apocalypse Soundfont | Patricio Herrera | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 679 | NEW! Mother 1+2 Soundfont (1.01) | Shigesato Itoi & Nintendo | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 680 | Ninja Gaiden Trilogy Soundfont | Patricio Herrera | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 681 | Final Fantasy VI: Advance [GBA] | Exabyte U | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 682 | Zhu Zhu Pets DS soundfont | That Animatronic Person | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 683 | Romancing Saga Soundfont | Zetshiro | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 684 | Prince of Persia Soundfont Soundfont | Patricio Herrera | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 685 | Samsung TV 2015 nostalgia TV sound test sound effect | Samsung | musical-artifacts | 站点自标「存疑」 | piano | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 686 | Final Fantasy IV: Advance [GBA] | Exabyte U | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 687 | Marvel Super Heroes War of The Gems Soundfont | Patricio Herrera | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 688 | Sunset Riders Soundfont | Mike Crain | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 689 | Final Fantasy V: Advance [GBA] | Exabyte U | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 690 | Legend of Zelda: Four Swords [GBA] | Exabyte U | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 691 | Chamberlin Marimba Soundfont | sleepnsound | musical-artifacts | 站点自标「存疑」 | other | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 692 | College Slam Basketball Soundfont | fluidvolt | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 693 | Mario Kart 8 Campaign Software MIDI and Soundfont | Landon & Emma | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 694 | Alcahest Soundfont | William Kage | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 695 | Lufia Soundfont | Felix Flywheel | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 696 | WWF Raw Soundfont | Patricio Herrera | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 697 | Megaman & Bass [GBA] | Exabyte U | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 698 | Dry Snap [Native Instruments DrumLab] | kitty-cat-satellite | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 699 | The Legend Zelda Four Swords Anniversary Edition DSi Sound R | M. Reza Khadafi | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 700 | Advanced Wars+ [GBA] | Exabyte U | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 701 | Nokia E71 TMobile sounds V2 | TheSoundfontMaker | musical-artifacts | 站点自标「存疑」 | other | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 702 | Final Fantasy Tactics Advance [GBA] | Exabyte U | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 703 | 7th Dragon - Soundfonts and Midis | flamentnagel | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 704 | Spider-Man 2 (NDS) Midis + SoundFonts | Nolann59860 | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 705 | Bird & Beans & Paper Airplane Chase (NDS) MIDIs + SoundFonts | Tailx | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 706 | Breath of Fire 2 Soundfont | Felix Flywheel | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 707 | Final Fight Soundfont | Mike Crain | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 708 | Ellen Whitaker's Horse Life 2 DS soundfont | @IzzBloxian on YouTube (*I | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 709 | Growth Or Devolution SNES 2.0 Soundfont | Witch's Cadence | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 710 | Failed Distorted Rip Soundfont | Salutanis Orkonus | musical-artifacts | 站点自标「存疑」 | other | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 711 | Breath of Fire Soundfont | Felix Flywheel | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 712 | Tekken Advanced [GBA] | Exabyte U | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 713 | Clay Fighter Soundfont | Mike Crain | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 714 | Metal Slug: Advance 2.0 [GBA] | Exabyte U | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 715 | Old Phone Tones | onj3.andrelouis.com | musical-artifacts | 站点自标「存疑」 | other | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 716 | Drill Dozer [GBA] | Exabyte U | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 717 | GAX Engine (GBA) Sample Pack | Shin'en Multimedia | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 718 | Style Savvy Soundfont | Atsuhiro Motoyama | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 719 | Nokia E71 TMobile version sound assets | TheSoundfontMaker | musical-artifacts | 站点自标「存疑」 | other | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 720 | Gemfire Soundfont | Mike Crain | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 721 | F-Zero: GP Legend [GBA] | Exabyte U | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 722 | Planning Permission soundfont V2 | TheSoundfontMaker | musical-artifacts | 站点自标「存疑」 | other | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 723 | Ensoniq ESQ-1 "SAX 1" synth soundfont | unknown | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 724 | Cello Cocoto | @IzzBloxian on YouTube (*I | musical-artifacts | 站点自标「存疑」 | orch | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 725 | Ensoniq ESQ-1 "PIANO2" synth soundfont | unknown | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 726 | Ensoniq ESQ-1 "ORGAN1" synth soundfont | unknown | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 727 | Ensoniq ESQ-1 "WAVBEL" synth soundfont | unknown | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 728 | Ensoniq ESQ-1 "HI-RES" synth soundfont | unknown | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 729 | Ensoniq ESQ-1 "SINPAD" synth soundfont | unknown | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 730 | Ensoniq ESQ-1 "PIANO1" synth soundfont | unknown | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 731 | Aladdin [GBA] | Exabyte U | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 732 | King of Fighters EX2: Howling Blood [GBA] | Exabyte U | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 733 | Ensoniq ESQ-1 "VELBAS" synth soundfont | unknown | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 734 | Ensoniq ESQ-1 "SHAKER" synth soundfont | unknown | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 735 | Ensoniq ESQ-1 "SYNBAZ" synth soundfont | unknown | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 736 | Lufia: Ruins of Lore [GBA] | Exabyte U | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 737 | Ensoniq ESQ-1 "SLOSTR" synth soundfont | unknown | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 738 | Lunar Legend [GBA] | Exabyte U | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 739 | Ensoniq ESQ-1 "MIXED" synth soundfont | unknown | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 740 | Airforce Delta Storm: Deadly Skies [GBA] | Exabyte U | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 741 | Ensoniq ESQ-1 "MOODS" synth soundfont | unknown | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 742 | Ensoniq ESQ-1 "PLKMTL" synth soundfont | unknown | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 743 | Ensoniq ESQ-1 "NOISTR" synth soundfont | unknown | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 744 | Ensoniq ESQ-1 "MINI M" synth soundfont | unknown | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 745 | Ensoniq ESQ-1 "TRIBEL" synth soundfont | unknown | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 746 | Ensoniq ESQ-1 +KOTO2 Soundfont | unknown | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 747 | Ensoniq ESQ-1 "PLKBRS" synth soundfont | unknown | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 748 | Ensoniq ESQ-1 "SNAPS1" synth soundfont | unknown | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 749 | Britney's Dance Beat [GBA] | Exabyte U | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 750 | Ensoniq ESQ-1 "BL PNO" synth soundfont | unknown | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 751 | Ensoniq ESQ-1 "CLAV 1" synth soundfont | unknown | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 752 | Ensoniq ESQ-1 "HARP2" synth soundfont | unknown | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 753 | Ensoniq ESQ-1 "DIGPNO" synth soundfont | unknown | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 754 | Ensoniq ESQ-1 "SLDRUM" synth soundfont | unknown | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 755 | Ensoniq ESQ-1 "BRASTR" synth soundfont | unknown | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 756 | Ensoniq ESQ-1 "BOTTLS" synth soundfont | unknown | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 757 | Ensoniq ESQ-1 "ICYORG" synth soundfont | unknown | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 758 | Ensoniq ESQ-1 "ECHO1" synth soundfont | unknown | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 759 | Ensoniq ESQ-1 "ANABRS" synth soundfont | unknown | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 760 | Ensoniq ESQ-1 "KLUNKS" synth soundfont | unknown | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 761 | Ensoniq ESQ-1 "3TRUMS" synth soundfont | unknown | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 762 | Yu Yu Hakasho: Tournament Tactics [GBA] | Exabyte U | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 763 | Ensoniq ESQ-1 "4XFADE" synth soundfont | unknown | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 764 | Ensoniq ESQ-1 "HEVBRS" synth soundfont | unknown | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 765 | Atomic Betty [GBA] | Exabyte U | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 766 | Hamtaro: Ham-Ham Heartbreak Soundfont | Datasette Trax | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 767 | Ensoniq ESQ-1 "KICK" synth soundfont | unknown | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 768 | Ensoniq ESQ-1 "MRIMBA" synth soundfont | unknown | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 769 | Ensoniq ESQ-1 "2 COOL" synth soundfont | unknown | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 770 | Sarukh's Nintendo DS General MIDI Soundfont | Sarukh_Animates | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 771 | Altered Beasts: Guardian of the Realms [GBA] | Exabyte U | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 772 | Ensoniq ESQ-1 "ISLAND" synth soundfont | unknown | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 773 | Hot Wheels: Burning Rubber [GBA] | Exabyte U | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 774 | Strike Force Hydra [GBA] | Exabyte U | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 775 | Ace Combat: Advance 2.5 [GBA] | Exabyte U | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 776 | Ensoniq ESQ-1 "KALMBA" synth soundfont | unknown | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 777 | Boscombe pier vibraphone soundfont | TheSoundfontMaker | musical-artifacts | 站点自标「存疑」 | other | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 778 | Ensoniq ESQ-1 "K+SIMS" synth soundfont | unknown | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 779 | Super Bust-A-Move [GBA] | Exabyte U | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 780 | ILIO Sinclavier Essential Percussion (Soundfont/.sf2 Convers | supermumbo | musical-artifacts | 站点自标「存疑」 | piano | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 781 | Spider-Man and the X-Men in Arcade's Revenge Soundfont | KiwiFlare | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 782 | Edirol SD-90 Pack II | rosntdoxot, DrKoupop, Spoo | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 783 | Stolen Soundfont (Update V2.03) | ME! | musical-artifacts | 站点自标「存疑」 | gm | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 784 | Stolen Soundfont v2.05 | ME! | musical-artifacts | 站点自标「存疑」 | gm | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 785 | Stolen Soundfont v2.07 | ME! | musical-artifacts | 站点自标「存疑」 | gm | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 786 | Apollo GMGS v1.051 (3.89 GiB GM+GS soundfont) | Caed | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 787 | Edirol SD-20 ~ Contemporary Soundfont | Thomas K. | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 788 | Kingdom Hearts - Soundfont Bundle 2024 | not me | musical-artifacts | 站点自标「存疑」 | other | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 789 | DSOUNDFONT Ultimate | Strix Soundfont Team | musical-artifacts | 混合 / 不明 | gm | 混合 / 不明（同一包内多种来源，无法逐项确认） |
| 790 | "Ultimate" Roblox Soundfont (Old) | AquaDoesStuff | musical-artifacts | 混合 / 不明 | game | 混合 / 不明（同一包内多种来源，无法逐项确认） |
| 791 | DSoundFont Gaming Edition | Strix SoundFont Team | musical-artifacts | 混合 / 不明 | gm | 混合 / 不明（同一包内多种来源，无法逐项确认） |
| 792 | Taiko Drum Collection | Jason Champion, S. Christi | musical-artifacts | 混合 / 不明 | game | 混合 / 不明（同一包内多种来源，无法逐项确认） |
| 793 | Monalisa GM v2.06 | Simone Piervergili | musical-artifacts | 混合 / 不明 | gm | 混合 / 不明（同一包内多种来源，无法逐项确认） |
| 794 | Ephesus GM v1.00 (WIP) | Simone Piervergili | musical-artifacts | 混合 / 不明 | gm | 混合 / 不明（同一包内多种来源，无法逐项确认） |
| 795 | Arachno SoundFont | Arachnosoft - Maxime Abbey | musical-artifacts | 混合 / 不明 | game | 混合 / 不明（同一包内多种来源，无法逐项确认） |
| 796 | Monalisa GM v2.105 (14th June, 2025!!!) | Simone Piervergili | musical-artifacts | 混合 / 不明 | gm | 混合 / 不明（同一包内多种来源，无法逐项确认） |
| 797 | Cocoto Platform Jumper WiiWare Soundfont | @IzzBloxian("IsHungry" on  | musical-artifacts | 混合 / 不明 | game | 混合 / 不明（同一包内多种来源，无法逐项确认） |
| 798 | ROCCHETTA PLIN PLIN SoundFont V1 (probably a Beta version) | Simone Piervergili | musical-artifacts | 混合 / 不明 | game | 混合 / 不明（同一包内多种来源，无法逐项确认） |
| 799 | Hight HD SoundFont SynthFont | Simone Piervergili | musical-artifacts | 混合 / 不明 | gm | 混合 / 不明（同一包内多种来源，无法逐项确认） |
| 800 | mpj minibox demo | MPJ factory studios | musical-artifacts | 混合 / 不明 | game | 混合 / 不明（同一包内多种来源，无法逐项确认） |
| 801 | Unleash The Beast SoundFont v1.2 (Not complete) | Simone Piervergili | musical-artifacts | 混合 / 不明 | other | 混合 / 不明（同一包内多种来源，无法逐项确认） |
| 802 | Orchestra HQ Traditional Realistic SoundFont (2024 Edition) | Simone Piervergili | musical-artifacts | 混合 / 不明 | other | 混合 / 不明（同一包内多种来源，无法逐项确认） |
| 803 | An old version of Rocchetta Plin Plin SoundFont | Simone Piervergili | musical-artifacts | 混合 / 不明 | other | 混合 / 不明（同一包内多种来源，无法逐项确认） |
| 804 | Antares SoundFont | Simone Piervergili | musical-artifacts | 混合 / 不明 | gm | 混合 / 不明（同一包内多种来源，无法逐项确认） |
| 805 | Unleash The Beast SoundFont | Simone Piervergili | musical-artifacts | 混合 / 不明 | other | 混合 / 不明（同一包内多种来源，无法逐项确认） |
| 806 | Unleash The Beast SoundFont v1.1 | Simone Piervergili | musical-artifacts | 混合 / 不明 | other | 混合 / 不明（同一包内多种来源，无法逐项确认） |
| 807 | Monalisa GM v1.0 (WIP) | Simone Piervergili | musical-artifacts | 混合 / 不明 | gm | 混合 / 不明（同一包内多种来源，无法逐项确认） |
| 808 | MelloSFZotron | Nathan Ingelbrecht | musical-artifacts | 混合 / 不明 | game | 混合 / 不明（同一包内多种来源，无法逐项确认） |
| 809 | Linnoleum SFZ-1 v2 | Nathan Ingelbrecht | musical-artifacts | 混合 / 不明 | drum | 混合 / 不明（同一包内多种来源，无法逐项确认） |
| 810 | ECHECAZ SoundFont | Simone Piervergili | musical-artifacts | 混合 / 不明 | other | 混合 / 不明（同一包内多种来源，无法逐项确认） |
| 811 | Phoenix GM-10 | Jexu | musical-artifacts | 混合 / 不明 | gm | 混合 / 不明（同一包内多种来源，无法逐项确认） |
| 812 | Cirnomiji Soundfont Archive | Cirnomiji (formerly known  | musical-artifacts | 混合 / 不明 | other | 混合 / 不明（同一包内多种来源，无法逐项确认） |
| 813 | Linnoleum SFZ-1 v1 | Nathan Ingelbrecht | musical-artifacts | 混合 / 不明 | drum | 混合 / 不明（同一包内多种来源，无法逐项确认） |
| 814 | The Fox and The Crow General MIDI SoundFont Ultimate | Simone Piervergili | musical-artifacts | 混合 / 不明 | other | 混合 / 不明（同一包内多种来源，无法逐项确认） |
| 815 | RetroFont2026 (WIP) | Simone Piervergili | musical-artifacts | 混合 / 不明 | game | 混合 / 不明（同一包内多种来源，无法逐项确认） |
| 816 | Sonic GBA Sound Collection [V1]: Advance 1, Advance 2, Pinba | AsalTheBunMoth/Reverie, Ne | musical-artifacts | 混合 / 不明 | game | 混合 / 不明（同一包内多种来源，无法逐项确认） |
| 817 | The Ultimate SoundFont Pack | IvyWolf and a lot of other | musical-artifacts | 混合 / 不明 | game | 混合 / 不明（同一包内多种来源，无法逐项确认） |
| 818 | Monalisa GM SoundFont v2.06.5 | Simone Piervergili | musical-artifacts | 混合 / 不明 | gm | 混合 / 不明（同一包内多种来源，无法逐项确认） |
| 819 | Monalisa GM v2.10 | Simone Piervergili | musical-artifacts | 混合 / 不明 | gm | 混合 / 不明（同一包内多种来源，无法逐项确认） |
| 820 | Monalisa GM v2.109 [Download new v2.109.5!!!] | Simone Piervergili | musical-artifacts | 混合 / 不明 | gm | 混合 / 不明（同一包内多种来源，无法逐项确认） |
| 821 | Caed's Ultimate Adequate GM version 1.04 (3.96GiB/4.26GB) | Caed, with some material b | musical-artifacts | 混合 / 不明 | hist | 混合 / 不明（同一包内多种来源，无法逐项确认） |
| 822 | Old Version of ROCCHETTA PLIN PLIN SoundFont | Simone Piervergili | musical-artifacts | 混合 / 不明 | hist | 混合 / 不明（同一包内多种来源，无法逐项确认） |
| 823 | Rocchetta Plin Plin SoundFont V2.022 | Simone Piervergili | musical-artifacts | 混合 / 不明 | hist | 混合 / 不明（同一包内多种来源，无法逐项确认） |
| 824 | Monalisa GM v2.109.5 (rev. 1) (6th September, 2026) | Simone Piervergili | musical-artifacts | 混合 / 不明 | other | 混合 / 不明（同一包内多种来源，无法逐项确认） |
| 825 | Unleash The Beast SoundFont v1.2 | Simone Piervergili | musical-artifacts | 混合 / 不明 | other | 混合 / 不明（同一包内多种来源，无法逐项确认） |
| 826 | GS for The Spy Teen (PUBLIC BETA) | Bento Media, Velzaic Studi | musical-artifacts | 混合 / 不明 | piano | 混合 / 不明（同一包内多种来源，无法逐项确认） |

> **关于「存疑」那 358 条**：不是我们不知道它们是什么，
> 而是**该站自己**标记了「来源存疑」—— 绝大多数是从**商业游戏 ROM** 里提取的音色，
> 原权利人从未授权再分发。**我们不做这种赌。**

## 八、从 lib 站继承的 5 个音色库（已全部并入本台账）

| 音色库 | 许可（**本次核实**） | 现在在台账里的落点 | 档位 |
|---|---|---|---|
| FluidR3_GM | **MIT** | `ms-fluid-soundfont-zip`（MuseScore 官方分发） | F2 |
| MuseScore_General | **MIT** | `ms-musescore-general-musescore-general-sf2` | F2 |
| Salamander Grand Piano | **CC BY 3.0**（此前「待核」→ 已核实） | `fp-piano-acoustic-grand-piano-salamander-grand-piano`（FreePats，**含 `.sf2`**）+ sfzinstruments 条目 | F2 |
| Yamaha Disklavier Pro Grand Piano（YDP） | **CC BY 3.0**（此前「待核」→ 已核实） | `fp-piano-acoustic-grand-piano-ydp-grand-piano` | F2 |
| The City Piano | **公有领域** | sfzinstruments `pianos/*` | F1 |

> 结论：**5 个全部落进台账**，两个「待核」项的许可靠页面原文核实完毕（不是凭印象）。
> **但注意**：这 5 个里只有 FreePats 的两个提供 `.sf2`；其余是 SFZ/WAV/FLAC 或 >50 MB，
> 属目录 + 指引层。

## 九、统计（三口径并列，**不要混用**）

| 口径 | 定义 | 数量 |
|---|---|---:|
| 全部条目 | 四来源抓到的全部记录 | **1776** |
| 可分发候选 | F1 + F2 + F3 | **950** |
| 可自由分发（F1） | CC0 / PD / WTFPL / Unlicense | **304** |
| F1 且 `.sf2` | 可直接站内分发 | **239** |
| **F1 且 `.sf2` 且 ≤50 MB** | **首批托管候选** | **57** |

**许可分布（全部 1776 条）**：

| 许可 | 数量 | 占比 | 档位 | 可再分发 |
|---|---:|---:|---|---|
| 站点自标「存疑」 | 358 | 20.2% | F4 | ❌ |
| CC BY 3.0 | 313 | 17.6% | F2 | ✅ |
| 未标注 | 268 | 15.1% | F4 | ❌ |
| MIT | 205 | 11.5% | F2 | ✅ |
| WTFPL（等同公有领域） | 107 | 6.0% | F1 | ✅ |
| CC0 | 95 | 5.3% | F1 | ✅ |
| 公有领域（站点标注） | 93 | 5.2% | F1 | ✅ |
| 商业授权 / 付费产品 | 59 | 3.3% | F4 | ❌ |
| CC BY | 53 | 3.0% | F2 | ✅ |
| 版权受限 | 52 | 2.9% | F4 | ❌ |
| 混合 / 不明 | 38 | 2.1% | F4 | ❌ |
| GPL v3 | 29 | 1.6% | F3 | ✅ |
| CC BY-SA | 17 | 1.0% | F3 | ✅ |
| 自定义许可（未明） | 11 | 0.6% | F4 | ❌ |
| CC BY 4.0 | 10 | 0.6% | F2 | ✅ |
| 公有领域 | 9 | 0.5% | F1 | ✅ |
| CC BY-NC-ND 3.0 | 9 | 0.5% | F4 | ❌ |
| ISC | 8 | 0.5% | F2 | ✅ |
| CC Sampling（整包分发受限） | 7 | 0.4% | F4 | ❌ |
| CC BY-SA 4.0 | 6 | 0.3% | F3 | ✅ |
| CC BY-NC | 6 | 0.3% | F4 | ❌ |
| 未识别许可码 falv13 | 4 | 0.2% | F4 | ❌ |
| CC BY-NC-SA 3.0 | 4 | 0.2% | F4 | ❌ |
| CC BY-NC-SA | 4 | 0.2% | F4 | ❌ |
| GPL v2 | 2 | 0.1% | F3 | ✅ |
| GPL | 2 | 0.1% | F3 | ✅ |
| Freemium（免费增值） | 2 | 0.1% | F4 | ❌ |
| CC Sampling Plus 1.0 | 2 | 0.1% | F4 | ❌ |
| CC BY-SA 3.0 | 1 | 0.1% | F3 | ✅ |
| 标注 Free 但未指明许可 | 1 | 0.1% | F4 | ❌ |
| CC BY-ND（禁改作） | 1 | 0.1% | F4 | ❌ |

## 十、对音色站的意义（三层的实际条数）

| 层 | 内容 | 条数 |
|---|---|---:|
| 第 1 层 · 目录 | 可分发候选（台账驱动、静态生成） | **950** |
| 第 2 层 · 托管 | F1 · `.sf2` · ≤50 MB（站内直下） | **57** |
| 第 3 层 · 指引 | F4（只写来源地址，**不托管、不直链**） | **826** |

### 10.1 首批托管候选（F1 · `.sf2` · ≤50 MB，按体积升序）

| # | 名称 | 作者 | 来源 | 许可 | 体积 | 分类 |
|---:|---|---|---|---|---:|---|
| 1 | Rhythmfont | Charlie | musical-artifacts | 公有领域（站点标注） | 0.1 MB | 游戏音源 |
| 2 | roland cr-78 general midi soundfont (+ rhythm midi files | barrelhead | musical-artifacts | WTFPL（等同公有领域） | 0.3 MB | 历史合成器/硬件音源 |
| 3 | Milo Murphy's Law Soundfont | RunTheCoins | archive | CC0 | 0.4 MB | 其他 / 未归类 |
| 4 | RemyMarshal's worlds smallest soundfont (electric piano) | RemyMarshal | musical-artifacts | WTFPL（等同公有领域） | 0.7 MB | 其他 / 未归类 |
| 5 | FreePats synthesizer percussion | FreePats project | FreePats | CC0 | 1.0 MB | 打击乐 / 鼓组 |
| 6 | Module'90 (free retro synth module) | Vini (2) | musical-artifacts | 公有领域（站点标注） | 1.2 MB | 游戏音源 |
| 7 | Module'89 (free retro synth module) | Vini (2) | musical-artifacts | 公有领域（站点标注） | 1.2 MB | 游戏音源 |
| 8 | Ukulele | FreePats project | FreePats | CC0 | 1.5 MB | 吉他 / 贝斯 / 拨弦 |
| 9 | Xylophone | Versilian Studios LLC | FreePats | CC0 | 1.7 MB | 打击乐 / 鼓组 |
| 10 | Synth Bass #2 | FreePats project | FreePats | CC0 | 1.7 MB | 电子 / 合成 |
| 11 | Jaw Harp | FreePats project | FreePats | CC0 | 1.8 MB | 民族 / 世界 |
| 12 | Lately Bass | FreePats project | FreePats | CC0 | 2.0 MB | 电子 / 合成 |
| 13 | Bass Guitar YR | Andrea Biasior | FreePats | CC0 | 2.2 MB | 吉他 / 贝斯 / 拨弦 |
| 14 | Ocarina | FreePats project | FreePats | CC0 | 3.0 MB | 管弦 / 古典 |
| 15 | Synth Bass #1 | FreePats project | FreePats | CC0 | 3.2 MB | 电子 / 合成 |
| 16 | jd_rockkit1.sf2 | no idea | musical-artifacts | WTFPL（等同公有领域） | 3.3 MB | 打击乐 / 鼓组 |
| 17 | Synth Brass #2 | FreePats project | FreePats | CC0 | 3.4 MB | 电子 / 合成 |
| 18 | Kalimba | FreePats project | FreePats | CC0 | 3.7 MB | 民族 / 世界 |
| 19 | small-balafon-from-Burkina-Faso-sf2 | Isis999 | musical-artifacts | WTFPL（等同公有领域） | 3.9 MB | 民族 / 世界 |
| 20 | Synth Strings #1 | FreePats project | FreePats | CC0 | 4.2 MB | 电子 / 合成 |
| 21 | Tubular Bells | Versilian Studios LLC | FreePats | CC0 | 4.3 MB | 打击乐 / 鼓组 |
| 22 | Synth Crystal | FreePats project | FreePats | CC0 | 4.4 MB | 电子 / 合成 |
| 23 | Timpani | Versilian Studios LLC | FreePats | CC0 | 4.5 MB | 打击乐 / 鼓组 |
| 24 | FM Synthesized Piano #2 | FreePats project | FreePats | CC0 | 4.6 MB | 钢琴 |
| 25 | World percussion | Versilian Studios LLC | FreePats | CC0 | 4.9 MB | 打击乐 / 鼓组 |
| 26 | Concert Harp | Versilian Studios LLC | FreePats | CC0 | 4.9 MB | 管弦 / 古典 |
| 27 | FSBS Electric Guitar Clean #2 (Jazz) | FreePats project | FreePats | CC0 | 5.0 MB | 吉他 / 贝斯 / 拨弦 |
| 28 | Synth Brass #1 | FreePats project | FreePats | CC0 | 5.2 MB | 电子 / 合成 |
| 29 | Drawbar organ emulation | Roberto | FreePats | CC0 | 5.8 MB | 风琴 / 键盘乐器 |
| 30 | Upright Piano KW | Gonzalo | FreePats | CC0 | 5.8 MB | 钢琴 |
| 31 | Synth Bass & Lead | FreePats project | FreePats | CC0 | 6.1 MB | 电子 / 合成 |
| 32 | FSBS Electric Guitar Clean #1 | FreePats project | FreePats | CC0 | 6.3 MB | 吉他 / 贝斯 / 拨弦 |
| 33 | Tenor Saxophone | Versilian Studios LLC | FreePats | CC0 | 6.5 MB | 管弦 / 古典 |
| 34 | Bagpipe | FreePats project | FreePats | CC0 | 6.7 MB | 民族 / 世界 |
| 35 | Clarinet | FreePats project | FreePats | CC0 | 6.7 MB | 管弦 / 古典 |
| 36 | Sweep Pad | FreePats project | FreePats | CC0 | 7.2 MB | 电子 / 合成 |
| 37 | New Age | FreePats project | FreePats | CC0 | 7.4 MB | 电子 / 合成 |
| 38 | Synth Strings #2 | FreePats project | FreePats | CC0 | 7.4 MB | 电子 / 合成 |
| 39 | Synth Lead Calliope | FreePats project | FreePats | CC0 | 7.5 MB | 电子 / 合成 |
| 40 | Wooden Recorder | Eugene Vlaskin | FreePats | CC0 | 7.9 MB | 管弦 / 古典 |
| 41 | (Wii U) Super Mario 3D World Soundfont (2019) | Mr.Sanic | musical-artifacts | 公有领域（站点标注） | 8.6 MB | 游戏音源 |
| 42 | Old Piano FB | FreePats project | FreePats | CC0 | 8.8 MB | 钢琴 |
| 43 | Synth Lead Square | FreePats project | FreePats | CC0 | 9.0 MB | 电子 / 合成 |
| 44 | Spanish classical guitar | FreePats project | FreePats | CC0 | 9.5 MB | 吉他 / 贝斯 / 拨弦 |
| 45 | Glasses of water | FreePats project | FreePats | CC0 | 9.8 MB | 打击乐 / 鼓组 |
| 46 | Hang tuned in D minor | FreePats project | FreePats | CC0 | 11.0 MB | 打击乐 / 鼓组 |
| 47 | Percussive organ emulation | FreePats project | FreePats | CC0 | 12.0 MB | 风琴 / 键盘乐器 |
| 48 | Rock organ emulation | FreePats project | FreePats | CC0 | 12.0 MB | 风琴 / 键盘乐器 |
| 49 | Synth Fifths | FreePats project | FreePats | CC0 | 12.0 MB | 电子 / 合成 |
| 50 | Synth Pad Choir | FreePats project | FreePats | CC0 | 12.0 MB | 电子 / 合成 |
| 51 | Gamer’s Tracker-MIDI(nSF2) Extracted Collection | Gamer45, technically als | musical-artifacts | WTFPL（等同公有领域） | 12.5 MB | 其他 / 未归类 |
| 52 | Church Organ Emulation | Fons Adriaensen | FreePats | CC0 | 13.0 MB | 风琴 / 键盘乐器 |
| 53 | FM Synthesized Piano #1 | FreePats project | FreePats | CC0 | 13.0 MB | 钢琴 |
| 54 | Synth Soundtrack | FreePats project | FreePats | CC0 | 17.0 MB | 电子 / 合成 |
| 55 | Synth Goblins | FreePats project | FreePats | CC0 | 19.0 MB | 电子 / 合成 |
| 56 | Synth Pad Bowed | FreePats project | FreePats | CC0 | 21.0 MB | 电子 / 合成 |
| 57 | Synth Sci-Fi | FreePats project | FreePats | CC0 | 22.0 MB | 电子 / 合成 |

### 10.2 民族 / 世界音色（原本只有 2 个，S0 后的实际改善）

可分发候选里的民族 / 世界音色 **21 条**：

| 名称 | 作者 | 来源 | 许可 | .sf2 | 体积 |
|---|---|---|---|---:|---|
| Jaw Harp | FreePats project | FreePats | CC0 | ✓ | 1.8 MB |
| Kalimba | FreePats project | FreePats | CC0 | ✓ | 3.7 MB |
| small-balafon-from-Burkina-Faso-sf2 | Isis999 | musical-artifacts | WTFPL（等同公有领域） | ✓ | 3.9 MB |
| Bagpipe | FreePats project | FreePats | CC0 | ✓ | 6.7 MB |
| ganjo | itsclipping | sfzinstruments | CC0 | — | 23.0 MB |
| Horse Pulse | Karoryfer Samples | sfzinstruments | CC0 | — | 180.0 MB |
| Etherealwinds Harp II CE | Versilian Studios LLC | sfzinstruments | CC0 | — | 200.0 MB |
| Celtic Soundfont | Michel Cöme | musical-artifacts | 公有领域（站点标注） | ✓ | — |
| little-scale's Ukulele | Placeholder Stick, littl | musical-artifacts | 公有领域（站点标注） | ✓ | — |
| Makala Ukulele Plucked | SuP3r_P1ckL3 | musical-artifacts | WTFPL（等同公有领域） | ✓ | — |
| Multi Kalimba | A1219 | musical-artifacts | CC BY | ✓ | — |
| Metal Pipe Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — |
| Bagpipe | sinshu | github | MIT | — | — |
| Banjo | sinshu | github | MIT | — | — |
| Kalimba | sinshu | github | MIT | — | — |
| Koto | sinshu | github | MIT | — | — |
| Shakuhachi | sinshu | github | MIT | — | — |
| Shamisen | sinshu | github | MIT | — | — |
| Sitar | sinshu | github | MIT | — | — |
| Kay 5-String Banjo | FlameStudios | sfzinstruments | GPL v3 | — | 425.0 MB |
| Kalimba Soundfont | Sizz Tuna | musical-artifacts | CC BY-SA | ✓ | — |

> FreePats 是民族音色的**主力来源**（bagpipe / jaw harp / kalimba / ukulele /
> world-and-rare-percussion 等），且多为 **CC0 + `.sf2`** —— 这是 S0 带来的最大改善，
> 直接回应了规划里「民族音色只有 2 个」的最大缺口。

---

*本台账由 `tools/sf_ledger.py --build` 生成，**勿手改**；改动请改抓取数据后重跑。*
