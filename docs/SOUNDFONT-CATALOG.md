# SOUNDFONT CATALOG · 音色库台账

> **用途**：音色站（`sf.midicn.com`）的内容真源 —— 目录三层的全部依据。
> **可复现**：`tools/sf_crawl.py`（抓四个来源）→ `tools/sf_ledger.py --build`（生成本文件）。
> **机器可读版**：[`soundfonts.json`](soundfonts.json)（音色站直接读它）。
> **本文件为全量明细** —— 不只是「收录了什么」，还包括**我们审过什么、以及为什么排除**。

## 一、总览

| 项 | 值 |
|---|---|
| 登记条目（四来源合计） | **3542** |
| **许可允许再分发** | **2492（70%）** ← 进入候选池 |
| **不可再分发** | **1050（30%）** |
| 含 `.sf2` 格式的可分发条目 | **2103** |
| **F1 且 `.sf2` 且 ≤50 MB**（可直接托管） | **69** |

**四档分布**（判「这个音色文件能不能再分发」）：

| 档位 | 含义 | 数量 | 占比 |
|---|---|---:|---:|
| **F1** | 可自由分发（CC0 / 公有领域 / WTFPL / Unlicense） | **741** | 20.9% |
| **F2** | 署名后可分发（CC BY / MIT / BSD / ISC） | **1691** | 47.7% |
| **F3** | 相同方式共享（有传染性：CC BY-SA / GPL） | **60** | 1.7% |
| **F4** | 不收录（禁止商用 / 禁止改作 / Sampling 系列 / 存疑 / 版权受限 / 未标注） | **1050** | 29.6% |

**按来源**：

| 来源 | 抓法 | 条目 | 可分发 |
|---|---|---:|---:|
| **musical-artifacts.com** | artifacts.json API（tags=soundfont） | 1067 | 595 |
| **FreePats** | 36 个乐器页 HTML 解析 | 57 | 57 |
| **sfzinstruments** | data/sfz/instruments.yml | 148 | 62 |
| **MuseScore 官方音色分发** | Apache 目录索引 + HEAD 实测体积 | 5 | 4 |
| **FluidSynth 官方 wiki 清单** | 官方 wiki 页（仓库内 doc/wiki/SoundFont.md） | 9 | 0 |
| **GitHub topic:soundfont** | 搜索 API 取仓 + git/trees 列文件（许可取仓 LICENSE 的 SPDX） | 290 | 212 |
| **Polyphone Soundfont Collection** | 列表页内嵌 data_soundfonts + 逐条详情页（许可键取自 /en/licenses） | 1567 | 1481 |
| **archive.org** | 搜索 API + 逐条目 metadata（许可 licenseurl 机器可读、文件体积可查） | 399 | 81 |

**按用途分类**（两口径并列 —— 全部条目 / 可分发候选）：

| 分类 | 全部 | 可分发 |
|---|---:|---:|
| 游戏音源 | 1160 | 830 |
| 历史合成器/硬件音源 | 235 | 142 |
| 钢琴 | 229 | 148 |
| 管弦 / 古典 | 203 | 155 |
| 民族 / 世界 | 48 | 35 |
| 打击乐 / 鼓组 | 164 | 130 |
| 电子 / 合成 | 308 | 277 |
| 音效 / 其他 | 42 | 36 |
| 通用 GM 音色库 | 288 | 250 |
| 吉他 / 贝斯 / 拨弦 | 95 | 69 |
| 风琴 / 键盘乐器 | 29 | 24 |
| 人声 / 合唱 | 40 | 28 |
| 管乐独奏 | 12 | 9 |
| 其他 / 未归类 | 689 | 359 |

**体积已知情况**（共 3542 条）：

| 体积来源 | 条数 | 说明 |
|---|---:|---|
| 我们**实测**（Range / HEAD） | 374 | musical-artifacts 里可访问的直链 |
| **来源页标注** | 177 | FreePats / sfzinstruments / MuseScore 页面自带 |
| **未提供** | 2991 | 上游不提供、且直链拒绝访问（见 §二）—— **宁缺勿错，不猜** |

### 1.1 三个口径必须分清（读表前先看这段）

- **全部条目**：四个来源抓到的**全部**记录（含明确不可分发的）。
- **可分发候选**：许可允许再分发的（F1 + F2 + F3）—— 音色站目录收录这些。
- **可直接托管**：F1 且是 `.sf2` 且体积 ≤50 MB —— 站内直下只有这一档。

> 历史沿革：早期版本台账只有 musical-artifacts 一个来源（1,067 条 / 595 候选）。
> S0 补抓 FreePats / sfzinstruments / MuseScore 之后，来源覆盖与条目数均上升。

## 二、⚠️ 数据来源与覆盖度（诚实说明）

**已覆盖（累计 8 个来源）**：

| 来源 | 抓法 | 为什么抓它 |
|---|---|---|
| musical-artifacts.com | artifacts.json API（tags=soundfont） | 唯一的**批量结构化许可字段**来源（可按许可程序化筛选） |
| FreePats | 36 个乐器页 HTML 解析 | **DFSG 合规 · 质量经实践检验**；有 `.sf2` 且体积适中；**民族/世界乐器的主要来源**（bagpipe / kalimba / jaw harp / ukulele…） |
| sfzinstruments | data/sfz/instruments.yml | 钢琴与鼓组名品（Salamander / Bigcat Cello / SM Drums…）；YAML 自带许可与体积 |
| MuseScore 官方音色分发 | Apache 目录索引 + HEAD 实测体积 | **FluidR3_GM / MuseScore_General（MIT）** —— 社区最广泛推荐的两个 |
| FluidSynth 官方 wiki 清单 | 官方 wiki 页（仓库内 doc/wiki/SoundFont.md） | **引擎官方推荐过的**（策展信号）—— 该清单不写许可，故只进台账作指引 |
| GitHub topic:soundfont | 搜索 API 取仓 + git/trees 列文件（许可取仓 LICENSE 的 SPDX） | 长尾与新品；**许可取自仓库 LICENSE（机器可读）**，且 `git/trees` **自带文件体积** |
| Polyphone Soundfont Collection | 列表页内嵌 data_soundfonts + 逐条详情页（许可键取自 /en/licenses） | 社区上传站（**会员制**：下载需注册 → 我们只给来源页）；许可用站点自带的 7 种键（`public-domain` / `give-credit*` / `modifications-forbidden` / `personal-use*`），逐条读自详情页 |
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
| **未标注许可** → 许可不明即不收录 | 399 | |
| **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 | 358 | |
| NC 系列：禁止商业使用 → 我们不代管、不直链 | 83 | |
| 商业授权 / 需付费购买 | 59 | |
| 版权受限（原权利人保留全部权利） | 52 | |
| 混合 / 不明（同一包内多种来源，无法逐项确认） | 38 | |
| NC-ND：禁商用且禁改作 → 我们不代管、不直链 | 15 | |
| 自定义许可，条款未明 → **许可不明即不收录** | 11 | |
| **许可码未识别**（`by-nc-nd`）→ 不猜、不收录 | 10 | |
| **ND 禁改作**：音色的主要用途就是衍生（用采样做音乐/改编）→ 收录会误导使用者 | 9 | |
| CC Sampling 系列：整包原样再分发受限（仅非商业）→ 只给来源 | 7 | |
| **许可码未识别**（`falv13`）→ 不猜、不收录 | 4 | |
| 免费增值（免费版许可不明） | 2 | |
| CC Sampling Plus 1.0：整包原样再分发仅限非商业 → 只给来源 | 2 | |
| 标注 Free 但未指明具体许可 → 视为许可不明 | 1 | |

### 3.2 ⭐ 曲目的 C1/C2/C3 与音色的 F1–F4 是**两套独立的分级**

> 前者判「**这首曲子**能不能商用」，后者判「**这个音色文件**能不能再分发」。
> **同一个 F1 音色可以用来演奏 C3 曲目** —— 两者互不推导。

### 3.3 许可优先：同一音色多来源时取哪一条

同一音色可能同时出现在多个来源（例：Salamander Grand Piano 在 FreePats 与 sfzinstruments 都有）。
台账**两条都留**（各自记明来源与格式），并给出 `group` 字段供站点聚合展示；
若要**托管控件**，优先取：**① F1 优于 F2 优于 F3** → ② **`.sf2` 优于其余格式** → ③ **体积小者**。

## 四、F1 · 可自由分发（CC0 / 公有领域 / WTFPL / Unlicense） · 全量 741 条

> 本档**逐条列明**：名称 / 作者 / 来源 / 许可 / 是否 `.sf2` / 体积 / 下载量 / 分类。

**其中可直接托管的（`.sf2` 且 ≤50 MB）**：69 条 —— 见 §十。

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
| 10 | Zappa Kit.sf2 | rabid47 | archive | CC0 | ✓ | 23.7 MB | — | drum |
| 11 | Gogodze Phu Vol II | Karoryfer Samples | sfzinstruments | CC0 | — | 133.0 MB | — | drum |
| 12 | Frankensnare | Karoryfer Samples | sfzinstruments | CC0 | — | 900.0 MB | — | drum |
| 13 | Swirly Drums | Karoryfer Samples | sfzinstruments | CC0 | — | 1638.4 MB | — | drum |
| 14 | Unruly Drums | Karoryfer Samples | sfzinstruments | CC0 | — | 2048.0 MB | — | drum |
| 15 | Big Rusty Drums | Karoryfer Samples | sfzinstruments | CC0 | — | 2355.2 MB | — | drum |
| 16 | vibraphone-sustain-ff-sf2 | isis999 | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 9888 | drum |
| 17 | marimba-deadstroke-ff-sf2 | isis999 | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 6861 | drum |
| 18 | Industromatic v1.0 Soundfont | Erik Hermansen | musical-artifacts | 公有领域（站点标注） | ✓ | — | 6396 | drum |
| 19 | Shaun's Drum Loops 1 Soundfont | Shaun Hunt | musical-artifacts | 公有领域（站点标注） | ✓ | — | 4903 | drum |
| 20 | Custom Drums by JJ MH v2 | JJ MH | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 4387 | drum |
| 21 | Basement Noise v1.0 Soundfont | Erik Hermansen | musical-artifacts | 公有领域（站点标注） | ✓ | — | 4233 | drum |
| 22 | Shaun's Drum Loops 4 Soundfont | Shaun Hunt | musical-artifacts | 公有领域（站点标注） | ✓ | — | 3242 | drum |
| 23 | Shaun's Drum Loops 3 Soundfont | Shaun Hunt | musical-artifacts | 公有领域（站点标注） | ✓ | — | 3016 | drum |
| 24 | Shaun's Drum Loops 2 Soundfont | Shaun Hunt | musical-artifacts | 公有领域（站点标注） | ✓ | — | 2880 | drum |
| 25 | MusicBox | — | polyphone | 公有领域 | ✓ | — | 1270 | drum |
| 26 | Cinematic Drum Set | — | polyphone | 公有领域 | ✓ | — | 1132 | drum |
| 27 | Bread Bread&#039;s Drum Kit (v1.03.1) | — | polyphone | 公有领域 | ✓ | — | 1023 | drum |
| 28 | Linn Drum LM-2 | ? | polyphone | 公有领域 | ✓ | — | 785 | drum |
| 29 | Various percussions | Fox-Gieg / Bailey / Dollee | polyphone | 公有领域 | ✓ | — | 646 | drum |
| 30 | Steel tongue soundfont | — | polyphone | 公有领域 | ✓ | — | 564 | drum |
| 31 | Timpani Roll &amp; Hit | ? | polyphone | 公有领域 | ✓ | — | 536 | drum |
| 32 | Oberheim DMX | ? | polyphone | 公有领域 | ✓ | — | 525 | drum |
| 33 | Finger Snaps | — | polyphone | 公有领域 | ✓ | — | 494 | drum |
| 34 | 4-Op FM Drums | Ian Wilson | polyphone | 公有领域 | ✓ | — | 473 | drum |
| 35 | 014 Florestan Tubular Bells and glide | Nando Florestan | polyphone | 公有领域 | ✓ | — | 438 | drum |
| 36 | Cajón (Ka-hone) | — | polyphone | 公有领域 | ✓ | — | 380 | drum |
| 37 | Orchestral Bass Drum | — | polyphone | 公有领域 | ✓ | — | 374 | drum |
| 38 | &#039;Decrescendo&#039; Guiro | — | polyphone | 公有领域 | ✓ | — | 313 | drum |
| 39 | Bowed Metal | — | polyphone | 公有领域 | — | — | 303 | drum |
| 40 | Yuca kit | ? | polyphone | 公有领域 | ✓ | — | 286 | drum |
| 41 | Various hits | Fox-Gieg | polyphone | 公有领域 | ✓ | — | 256 | drum |
| 42 | Thundersheet | — | polyphone | 公有领域 | ✓ | — | 253 | drum |
| 43 | Metronom | — | polyphone | 公有领域 | ✓ | — | 222 | drum |
| 44 | AnvilWhip | — | polyphone | 公有领域 | ✓ | — | 209 | drum |
| 45 | Roland CR Kit | — | polyphone | 公有领域 | ✓ | — | 207 | drum |
| 46 | Sony DRP-2 Digital Drum Pad | — | polyphone | 公有领域 | ✓ | — | 199 | drum |
| 47 | Heatsink | — | polyphone | 公有领域 | ✓ | — | 184 | drum |
| 48 | Punchy bassdrums | — | polyphone | 公有领域 | ✓ | — | 167 | drum |
| 49 | BOSS DR-55 | — | polyphone | 公有领域 | ✓ | — | 161 | drum |
| 50 | Simmons_SDS7 | — | polyphone | 公有领域 | ✓ | — | 159 | drum |
| 51 | Basic drumset | — | polyphone | 公有领域 | ✓ | — | 154 | drum |
| 52 | MetalDrums | — | polyphone | 公有领域 | ✓ | — | 136 | drum |
| 53 | Drum | — | polyphone | 公有领域 | ✓ | — | 135 | drum |
| 54 | Zil-Bel | — | polyphone | 公有领域 | ✓ | — | 127 | drum |
| 55 | Bottle Bell | — | polyphone | 公有领域 | ✓ | — | 125 | drum |
| 56 | Drums by Minii | — | polyphone | 公有领域 | ✓ | — | 111 | drum |
| 57 | Acces Virus B | — | polyphone | 公有领域 | ✓ | — | 101 | drum |
| 58 | Acetone Rhythm ACE | — | polyphone | 公有领域 | ✓ | — | 79 | drum |
| 59 | Found Sounds by MidJStudios | — | polyphone | 公有领域 | ✓ | — | 23 | drum |
| 60 | Gogodze Phu Vol I | Karoryfer Samples | sfzinstruments | CC0 | — | — | — | drum |
| 61 | The Definitive Perfect Drums Soundfont (V1, Fixed Banks) | TEC Again (original by lukinha | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 0 | drum |
| 62 | The Hakitas | — | archive | 公有领域 | — | — | — | drum |
| 63 | Jaw Harp | FreePats project | FreePats | CC0 | ✓ | 1.8 MB | — | ethnic |
| 64 | Kalimba | FreePats project | FreePats | CC0 | ✓ | 3.7 MB | — | ethnic |
| 65 | small-balafon-from-Burkina-Faso-sf2 | Isis999 | musical-artifacts | WTFPL（等同公有领域） | ✓ | 3.9 MB | 5291 | ethnic |
| 66 | Bagpipe | FreePats project | FreePats | CC0 | ✓ | 6.7 MB | — | ethnic |
| 67 | ganjo | itsclipping | sfzinstruments | CC0 | — | 23.0 MB | — | ethnic |
| 68 | Horse Pulse | Karoryfer Samples | sfzinstruments | CC0 | — | 180.0 MB | — | ethnic |
| 69 | Etherealwinds Harp II CE | Versilian Studios LLC | sfzinstruments | CC0 | — | 200.0 MB | — | ethnic |
| 70 | Celtic Soundfont | Michel Cöme | musical-artifacts | 公有领域（站点标注） | ✓ | — | 6516 | ethnic |
| 71 | little-scale's Ukulele | Placeholder Stick, little-scal | musical-artifacts | 公有领域（站点标注） | ✓ | — | 5841 | ethnic |
| 72 | Early European Instruments | — | polyphone | 公有领域 | ✓ | — | 943 | ethnic |
| 73 | Seagull Acoustic Guitar | ? | polyphone | 公有领域 | ✓ | — | 911 | ethnic |
| 74 | Lao Khaen | — | polyphone | 公有领域 | ✓ | — | 582 | ethnic |
| 75 | Spirit of Hope gamelan balungan pelog | — | polyphone | 公有领域 | ✓ | — | 498 | ethnic |
| 76 | Makala Ukulele Plucked | SuP3r_P1ckL3 | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 441 | ethnic |
| 77 | 022 Florestan Harmonica | Nando Florestan | polyphone | 公有领域 | ✓ | — | 436 | ethnic |
| 78 | Out of Africa | ? | polyphone | 公有领域 | ✓ | — | 427 | ethnic |
| 79 | Vhamp | — | polyphone | 公有领域 | ✓ | — | 288 | ethnic |
| 80 | Recorder 1.4 | — | polyphone | 公有领域 | ✓ | — | 118 | ethnic |
| 81 | Rhythmfont | Charlie | musical-artifacts | 公有领域（站点标注） | ✓ | 0.1 MB | 1532 | game |
| 82 | Kirby 64 Flute Push Restored | Reza Khadafi | musical-artifacts | 公有领域（站点标注） | — | 0.1 MB | 1176 | game |
| 83 | Module'90 (free retro synth module) | Vini (2) | musical-artifacts | 公有领域（站点标注） | ✓ | 1.2 MB | 7621 | game |
| 84 | Module'89 (free retro synth module) | Vini (2) | musical-artifacts | 公有领域（站点标注） | ✓ | 1.2 MB | 2813 | game |
| 85 | Densetsu No Starfy GBA Soundfont | AJ Mendez | musical-artifacts | WTFPL（等同公有领域） | — | 2.8 MB | 1061 | game |
| 86 | (Wii U) Super Mario 3D World Soundfont (2019) | Mr.Sanic | musical-artifacts | 公有领域（站点标注） | ✓ | 8.6 MB | 13239 | game |
| 87 | SML2 SNES OST Demo | LadiesMan217 | archive | 公有领域 | — | 13.2 MB | — | game |
| 88 | The Mini Deltarune Soundfont | SonicCD_Fan | archive | 公有领域 | ✓ | 312.8 MB | — | game |
| 89 | Southern Park's Parents: An Australian Rescue (GCN/PS2/XBOX) Soundfont | Parker-stone Interactive Studi | archive | CC0 | — | 361.8 MB | — | game |
| 90 | Southern Park: Read & Play (2013 Nintendo 3DS rerelease) soundfonts ~  | Parker-Stone Interactive Studi | archive | CC0 | — | 559.3 MB | — | game |
| 91 | Virtuosity Drums | Versilian Studios LLC | sfzinstruments | CC0 | — | 1126.4 MB | — | game |
| 92 | General Game Boy Advance Soundfont 2.0 | BuskinCothurn | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 26032 | game |
| 93 | Gameboy GM Soundfont | CynthiaCelestic+ASIALUNAR+Moet | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 22815 | game |
| 94 | Touhou Roland SRX EoSD Romantic Trumpet | Palto, DrKoupop | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 21449 | game |
| 95 | Friday Night Funkin' Voice Soundfont | SkullMasked | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 18665 | game |
| 96 | The Absolute Sega FM Soundfont Version 1.75!!! | Mx. K | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 17713 | game |
| 97 | Knuckles Chaotix soundfont | Veninator1207 | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 14659 | game |
| 98 | Retro Wave Paradise | strixSF2, 迎春心情 (Yingchun Soul) | musical-artifacts | 公有领域（站点标注） | ✓ | — | 10098 | game |
| 99 | midi arcade soundfont, full  collection | Milton Paredes, Mpj factory st | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 9928 | game |
| 100 | KK Slider Soundfont | coffeebug | musical-artifacts | 公有领域（站点标注） | ✓ | — | 7489 | game |
| 101 | DefleGB | Mx. K | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 6993 | game |
| 102 | OPLL(YM2413) Soundfont v1.5 | src3453 | musical-artifacts | 公有领域（站点标注） | ✓ | — | 6993 | game |
| 103 | Super Italo DiscoFont: Director's Cut | strixSF2, Yingchun Soul for th | musical-artifacts | 公有领域（站点标注） | ✓ | — | 6717 | game |
| 104 | PC-98 YM2608 SoundFont | Studio Emiko (original by Erik | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 6455 | game |
| 105 | The oringator soundfont | Milton Paredes, mpj factory st | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 5591 | game |
| 106 | HL4MGM | strixSF2, Yingchun Soul for th | musical-artifacts | 公有领域（站点标注） | ✓ | — | 5515 | game |
| 107 | Sonic Mania Soundfont v1.2 (INCOMPLETE) | MylesDG | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 5271 | game |
| 108 | pokemon emerald soundfont | nintendo (ripped by me) | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 4581 | game |
| 109 | Toejam and Earl soundfont v3 | Veninator1207 | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 4459 | game |
| 110 | Defle2151 GM | Mx. K | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 4458 | game |
| 111 | The DEFINITIVE BED LUMP Soundfont! (Undertale) | ASmolBoy | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 4352 | game |
| 112 | Boy Band Soundfont | S. Christian Collins | musical-artifacts | 公有领域（站点标注） | ✓ | — | 4289 | game |
| 113 | Beavis and Butt-Head soundfont (Genesis) | Veninator1207 | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 3956 | game |
| 114 | LG GX200 | jamisson tavares | musical-artifacts | 公有领域（站点标注） | ✓ | — | 3861 | game |
| 115 | High Quality Super Mario 64 Slider SF2 | EggsCantFly | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 3386 | game |
| 116 | Homebrew Browser (addicti.mod) Soundfont | hbaoymb | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 3300 | game |
| 117 | Super Battletoads Soundfont V1.0 | JJ MH | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 3216 | game |
| 118 | the midi arcade series, A P B - All poynts bulletin | Milton Paredes, MPJ factory st | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 3050 | game |
| 119 | Deus Ex (2000) Soundfont (Version _1) | Jordan Moore | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 2942 | game |
| 120 | Stinkofont 20X6 v2.1 | Gfdgsgxgzgdrc (me) | musical-artifacts | 公有领域（站点标注） | ✓ | — | 2857 | game |
| 121 | HL1MGM | strixSF2, 迎春心情 (Yingchunsoul)  | musical-artifacts | 公有领域（站点标注） | ✓ | — | 2834 | game |
| 122 | Overdriven Guitar Catalog V1 V2 is out!!! | Marigold | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 2824 | game |
| 123 | Growtopia Soundfont | coffeebug | musical-artifacts | 公有领域（站点标注） | ✓ | — | 2798 | game |
| 124 | Power rangers SNES V2 | longlong2004 | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 2777 | game |
| 125 | Fabricio Soundbank | legendfabricio | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 2775 | game |
| 126 | Sonic the Hedgehog - Genesis (GBA) Soundfont | TEC Again | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 2711 | game |
| 127 | Some Splatoon Sounds (Soundfont) | Marv :) | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 2423 | game |
| 128 | PopocacaGM (v3.1) | Mangonesse on 29/3/25 | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 2245 | game |
| 129 | Mario Golf: Toadstool Tour (2003) | LuckyPrincess  (original by Th | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 2110 | game |
| 130 | F-Zero GP Legend GBA | TheBlackHand28 | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 2080 | game |
| 131 | Densetsu no Starfy 4 Soundfont | Anthro | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 1978 | game |
| 132 | Tomodachi Life: Living the Dream Soundfont | plippy | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 1973 | game |
| 133 | Tomodachi Life Soundfont (Heavy WIP) | TEC Again | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 1854 | game |
| 134 | Rayman 2 N64 Soundfont | Dr. Kiwis | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 1718 | game |
| 135 | Stinkofont 20X6 (Old Version) | Gfdgsgxgzgdrc (me) | musical-artifacts | 公有领域（站点标注） | ✓ | — | 1494 | game |
| 136 | Shinobi III: Return Of The Ninja Master Soundfont (INCOMPLETE) | Blental | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 1389 | game |
| 137 | Square wave soundfont (well temperament version) | Piotr Grochowski | musical-artifacts | 公有领域（站点标注） | ✓ | — | 1354 | game |
| 138 | Updated Majora's Mask Soundfont (2024) | supermumbo | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 1338 | game |
| 139 | Square wave soundfont (meantone version) | Piotr Grochowski | musical-artifacts | 公有领域（站点标注） | ✓ | — | 1251 | game |
| 140 | Monster House DS/GBA Soundfont | Memex87 | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 1226 | game |
| 141 | Tonic Trouble N64 Soundfont | Dr. Kiwis | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 1186 | game |
| 142 | Cloudcones Instruments + XM Soundfont Dump | Zabutom and Nagz (and many oth | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 1157 | game |
| 143 | The Distraction Dance Soundfont | FerikkusuSF2s | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 1127 | game |
| 144 | Korg Triton Noisy Funky Synth Soundfont | Mildanner | musical-artifacts | 公有领域（站点标注） | ✓ | — | 1097 | game |
| 145 | Square wave soundfont (equal temperament version) | Piotr Grochowski | musical-artifacts | 公有领域（站点标注） | ✓ | — | 1021 | game |
| 146 | Roblox OOF! Soundfont | Anapan | musical-artifacts | 公有领域（站点标注） | ✓ | — | 1018 | game |
| 147 | Robots (GBA) Soundfont | RoxyGaming | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 954 | game |
| 148 | Ranma 1/2: Hard Battle Soundfont | ShiverThermal | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 923 | game |
| 149 | The SpongeBob SquarePants Movie (Nintendo GBA) Soundfont | TEC Again | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 882 | game |
| 150 | Spamton sf2 | — | polyphone | 公有领域 | ✓ | — | 695 | game |
| 151 | Lilo & Stitch 2 - Haemsterviel Havoc (Nintendo GBA) Soundfont | TEC Again | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 665 | game |
| 152 | Lilo & Stitch (Nintendo GBA) Soundfont | TEC Again | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 637 | game |
| 153 | [OUTDATED] The Compiled Sonic Battle Soundfont (also read desc) | AsalTheBunMoth | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 548 | game |
| 154 | Sonic Boom (ROM Hack) Drum Soundfont | Mildanner | musical-artifacts | 公有领域（站点标注） | ✓ | — | 437 | game |
| 155 | The Soul Hackers Soundfont | Spidergenius10 | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 436 | game |
| 156 | Shrek: Ogre's and Dronkey's (Nintendo DS) Soundfont | Someone On The Internet | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 421 | game |
| 157 | Undertale Last Breath Soundfont | — | polyphone | 公有领域 | — | — | 384 | game |
| 158 | Sheep (Nintendo GBA) Soundfont | TEC Again | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 348 | game |
| 159 | Dragon Ball Advanced Adventure (GBA) | — | polyphone | 公有领域 | ✓ | — | 313 | game |
| 160 | Uniracers (SNES) Soundfont | Justaguy95 | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 274 | game |
| 161 | 8-bit NES 2A03 Simulation | — | polyphone | 公有领域 | ✓ | — | 214 | game |
| 162 | NSMB World 1 Soundfont(sf2) | me | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 184 | game |
| 163 | Quality 8-Bit Soundfont (ignore placeholder soundfont) | — | polyphone | 公有领域 | ✓ | — | 170 | game |
| 164 | March of the Penguins (GBA) | Skyworks Interactive, DSI Game | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 94 | game |
| 165 | Home Alone Genesis 1992 Drumkit | — | polyphone | 公有领域 | ✓ | — | 84 | game |
| 166 | Custom MD Drums | — | polyphone | 公有领域 | ✓ | — | 51 | game |
| 167 | Speedy Gonzales SNES soundfont, help me to create complete Speedy Gonz | — | polyphone | 公有领域 | — | — | 14 | game |
| 168 | Fanon Park (2001, Nintendo 64/SEGA DreamCast) soundfont ~ Demo files | PROJECT FANON PARK, Parker-Sto | archive | CC0 | — | — | — | game |
| 169 | Roland Fantom X SoundFont | schforby6805 | musical-artifacts | 公有领域（站点标注） | ✓ | — | 0 | game |
| 170 | Silent Animal Park (Nintendo DS, Nintendo GameCube, PlayStation 2) sou | Wintersoft Game Studios | archive | 公有领域 | — | — | — | game |
| 171 | Sonic The Hedgehog (Sega Genesis Soundfont) (DLS Version) | — | archive | 公有领域 | — | — | — | game |
| 172 | Touhou Retrologue Pack 0.2 | DrKoupop | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 0 | game |
| 173 | DSoundFont | strix Soundfont Team | musical-artifacts | 公有领域（站点标注） | ✓ | — | 23391 | gm |
| 174 | airfont 380Final | Milton Paredes, mpj factory st | musical-artifacts | 公有领域（站点标注） | ✓ | — | 22233 | gm |
| 175 | DSoundFont Plus | Strix SoundFont Team | musical-artifacts | 公有领域（站点标注） | ✓ | — | 21129 | gm |
| 176 | Xiaod Bank Soundfont | Xiaod | musical-artifacts | 公有领域（站点标注） | ✓ | — | 9604 | gm |
| 177 | airfont 340 | Milton Paredes, Mpj factory st | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 9173 | gm |
| 178 | DSOUNDFONT Lite | strixSF2 | musical-artifacts | 公有领域（站点标注） | ✓ | — | 7728 | gm |
| 179 | Series 30 Synth (Original) | Nokia Corporation | musical-artifacts | 公有领域（站点标注） | ✓ | — | 6466 | gm |
| 180 | GeneralTrash Soundfont | Alif Maharendra Sihombing | musical-artifacts | 公有领域（站点标注） | ✓ | — | 4270 | gm |
| 181 | SumterNokia Ultimate Embedded GM Soundbank (26.62 MB) | Roe_2012 | musical-artifacts | 公有领域（站点标注） | ✓ | — | 3528 | gm |
| 182 | Half Life 1 Crowbar GM Soundfont | TheFunnyMan | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 3158 | gm |
| 183 | airfont 350 for MuseScore | Milton Paredes | musical-artifacts | 公有领域（站点标注） | — | — | 3129 | gm |
| 184 | SumterNokia Ultra Embedded GM Soundbank (21.53 MB) | Roe_2012 | musical-artifacts | 公有领域（站点标注） | ✓ | — | 2418 | gm |
| 185 | Baby font for musescore | Milton Paredes, MPJ factory st | musical-artifacts | 公有领域（站点标注） | — | — | 2125 | gm |
| 186 | Super Mario 64 General Midi Soundfont V1.3 | — | polyphone | 公有领域 | ✓ | — | 1555 | gm |
| 187 | Pokemon Diamond/Pearl/Platinum Soundfont [COMPILED] | — | polyphone | 公有领域 | ✓ | — | 1387 | gm |
| 188 | GM.sf2 | — | polyphone | 公有领域 | ✓ | — | 1249 | gm |
| 189 | JNS-GM 2.0 | Jordi Navarro Subirana | polyphone | 公有领域 | ✓ | — | 823 | gm |
| 190 | Musica theoria 2 | JeffD | polyphone | 公有领域 | ✓ | — | 552 | gm |
| 191 | Chaos bank 2.0 | ? | polyphone | 公有领域 | ✓ | — | 495 | gm |
| 192 | Masterpiece | Andrew MacLean | polyphone | 公有领域 | ✓ | — | 447 | gm |
| 193 | AWE rom | Skie | polyphone | 公有领域 | ✓ | — | 392 | gm |
| 194 | Mario and Luigi Superstar Saga Soundfont | — | polyphone | 公有领域 | ✓ | — | 375 | gm |
| 195 | Unison | Peter Jevnisek | polyphone | 公有领域 | ✓ | — | 315 | gm |
| 196 | LG GX200 | — | polyphone | 公有领域 | ✓ | — | 286 | gm |
| 197 | SM64 Soundfont (By Pablo’s Corner) | — | polyphone | 公有领域 | ✓ | — | 261 | gm |
| 198 | Windows Soundfont Lite | — | polyphone | 公有领域 | ✓ | — | 200 | gm |
| 199 | The Happy Tree Friends (Ashsha Kin) Soundfont, first blood. | — | polyphone | 公有领域 | ✓ | — | 185 | gm |
| 200 | Oscilloscope (All Instruments) | — | polyphone | 公有领域 | ✓ | — | 166 | gm |
| 201 | Rocket Power Zero Gravity Zone (GBA) | — | polyphone | 公有领域 | ✓ | — | 164 | gm |
| 202 | Lemmings Series | — | polyphone | 公有领域 | ✓ | — | 118 | gm |
| 203 | Dream SAM2635 Soundfont | — | polyphone | 公有领域 | ✓ | — | 101 | gm |
| 204 | HDT Premier 98i Karaoke QS6400 Soundfont | — | polyphone | 公有领域 | ✓ | — | 82 | gm |
| 205 | Super Mario Maker - Instruments (8-Bit Square And Drum, And Pizzicato) | — | polyphone | 公有领域 | ✓ | — | 77 | gm |
| 206 | Multilaser UP Play P9076 SC6531 | — | polyphone | 公有领域 | ✓ | — | 57 | gm |
| 207 | Huaji | — | polyphone | 公有领域 | ✓ | — | 49 | gm |
| 208 | spongebob creature from the krusty krab (ds) full | — | polyphone | 公有领域 | — | — | 44 | gm |
| 209 | Crash of the Titans GBA | — | polyphone | 公有领域 | ✓ | — | 40 | gm |
| 210 | KORG TRINITY - The rocky guitars | — | polyphone | 公有领域 | ✓ | — | 38 | gm |
| 211 | Earthworm Jim 1 &amp;amp; 2 soundfont | — | polyphone | 公有领域 | ✓ | — | 25 | gm |
| 212 | wonder boy | — | polyphone | 公有领域 | ✓ | — | 21 | gm |
| 213 | audio ltd | — | polyphone | 公有领域 | ✓ | — | 20 | gm |
| 214 | Madagascar ds sf2 and midi | — | polyphone | 公有领域 | — | — | 19 | gm |
| 215 | dafft puck | — | polyphone | 公有领域 | ✓ | — | 18 | gm |
| 216 | audio ltd 2 | — | polyphone | 公有领域 | ✓ | — | 12 | gm |
| 217 | My Come on! 285 enemies 1-2 (1999-2000 style) soundfont | — | polyphone | 公有领域 | ✓ | — | 11 | gm |
| 218 | ratatouille | — | polyphone | 公有领域 | ✓ | — | 10 | gm |
| 219 | itchy e scratchy snes | — | polyphone | 公有领域 | ✓ | — | 9 | gm |
| 220 | Goof Troop snes samples | — | polyphone | 公有领域 | — | — | 6 | gm |
| 221 | Ukulele | FreePats project | FreePats | CC0 | ✓ | 1.5 MB | — | guitar |
| 222 | Bass Guitar YR | Andrea Biasior | FreePats | CC0 | ✓ | 2.2 MB | — | guitar |
| 223 | FSBS Electric Guitar Clean #2 (Jazz) | FreePats project | FreePats | CC0 | ✓ | 5.0 MB | — | guitar |
| 224 | FSBS Electric Guitar Clean #1 | FreePats project | FreePats | CC0 | ✓ | 6.3 MB | — | guitar |
| 225 | Spanish classical guitar | FreePats project | FreePats | CC0 | ✓ | 9.5 MB | — | guitar |
| 226 | FSBS Electric Guitar Direct | FreePats project | FreePats | CC0 | ✓ | 60.0 MB | — | guitar |
| 227 | FSBS Electric Guitar Distorted #2 | FreePats project | FreePats | CC0 | ✓ | 121.0 MB | — | guitar |
| 228 | Swagbass | Karoryfer Samples | sfzinstruments | CC0 | — | 138.0 MB | — | guitar |
| 229 | Growlybass | Karoryfer Samples | sfzinstruments | CC0 | — | 160.0 MB | — | guitar |
| 230 | Pastabass | Karoryfer Samples | sfzinstruments | CC0 | — | 301.0 MB | — | guitar |
| 231 | Fashionbass | Karoryfer Samples | sfzinstruments | CC0 | — | 302.0 MB | — | guitar |
| 232 | FSBS Electric Guitar Distorted #1 | FreePats project | FreePats | CC0 | ✓ | 317.0 MB | — | guitar |
| 233 | Shinyguitar | Karoryfer Samples | sfzinstruments | CC0 | — | 352.0 MB | — | guitar |
| 234 | Black_And_Green_Guitars | Karoryfer Samples | sfzinstruments | CC0 | — | 500.0 MB | — | guitar |
| 235 | Black And Blue Basses | Karoryfer Samples | sfzinstruments | CC0 | — | 961.0 MB | — | guitar |
| 236 | Dirty Major Power Chords Soundfont | CDGillis | musical-artifacts | 公有领域（站点标注） | ✓ | — | 7307 | guitar |
| 237 | Otto's Fretlessbass Soundfont | C.W.Budde & Otto's Bass | musical-artifacts | 公有领域（站点标注） | ✓ | — | 6396 | guitar |
| 238 | Kona K2 Series K2T Acoustic-Electric Guitar | Kaesufurr | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 6287 | guitar |
| 239 | Marigold's Power Guitar Soundfont | Marigold | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 3758 | guitar |
| 240 | Florestan Contrabassoon | Nando Florestan | musical-artifacts | 公有领域（站点标注） | ✓ | — | 2273 | guitar |
| 241 | Monsoon&#039;s Maple Neck 1974 Fender Jazz Bass | — | polyphone | 公有领域 | ✓ | — | 2045 | guitar |
| 242 | Rock guitars | Tim Swartz | polyphone | 公有领域 | ✓ | — | 1971 | guitar |
| 243 | Bread Bread&#039;s Overdriven Guitar (1.0) | — | polyphone | 公有领域 | ✓ | — | 1007 | guitar |
| 244 | POWERMETAL - Picked Bass | — | polyphone | 公有领域 | ✓ | — | 1003 | guitar |
| 245 | 3 lead guitars | ? | polyphone | 公有领域 | ✓ | — | 928 | guitar |
| 246 | Minii&#039;s Electric Guitar | — | polyphone | 公有领域 | ✓ | — | 895 | guitar |
| 247 | Bread Bread&#039;s Distortion Bass Guitar (v1.1) | — | polyphone | 公有领域 | ✓ | — | 843 | guitar |
| 248 | Funky fretless bass | Todd Eaton | polyphone | 公有领域 | ✓ | — | 841 | guitar |
| 249 | Studio bass | ? | polyphone | 公有领域 | ✓ | — | 808 | guitar |
| 250 | Kick-arse bass | Ian Wilson | polyphone | 公有领域 | ✓ | — | 752 | guitar |
| 251 | Bass machine | ? | polyphone | 公有领域 | ✓ | — | 650 | guitar |
| 252 | 12 string | ? | polyphone | 公有领域 | ✓ | — | 597 | guitar |
| 253 | Strat Marshall | ? | polyphone | 公有领域 | ✓ | — | 581 | guitar |
| 254 | PSR433 Clean Gtr | — | polyphone | 公有领域 | ✓ | — | 580 | guitar |
| 255 | BASS FENDER JAZZ from INDONESIA | — | polyphone | 公有领域 | ✓ | — | 457 | guitar |
| 256 | JV 1080 bass | ? | polyphone | 公有领域 | ✓ | — | 437 | guitar |
| 257 | Metallic bass | ? | polyphone | 公有领域 | ✓ | — | 423 | guitar |
| 258 | Guitarra Worship 2026 | — | polyphone | 公有领域 | ✓ | — | 388 | guitar |
| 259 | Shamisen | — | polyphone | 公有领域 | ✓ | — | 364 | guitar |
| 260 | MuteGuitarEcho | — | polyphone | 公有领域 | ✓ | — | 328 | guitar |
| 261 | Melo guitarras sintéticas | — | polyphone | 公有领域 | ✓ | — | 315 | guitar |
| 262 | Guitar fret | ? | polyphone | 公有领域 | ✓ | — | 302 | guitar |
| 263 | Jazz guitar | — | polyphone | 公有领域 | ✓ | — | 180 | guitar |
| 264 | PoppaBass | — | polyphone | 公有领域 | ✓ | — | 172 | guitar |
| 265 | 3AZ NEW BASS2026 from INDONESIA | — | polyphone | 公有领域 | ✓ | — | 128 | guitar |
| 266 | Emilyguitar | Karoryfer Samples | sfzinstruments | CC0 | — | — | — | guitar |
| 267 | Korg M1EX Pipe Organ Restored | Reza Khadafi | musical-artifacts | 公有领域（站点标注） | — | 0.3 MB | 1902 | hist |
| 268 | roland cr-78 general midi soundfont (+ rhythm midi files) | barrelhead | musical-artifacts | WTFPL（等同公有领域） | ✓ | 0.3 MB | 801 | hist |
| 269 | Roland JD-800 Nylon Guitar Restored | Reza Khadafi | musical-artifacts | 公有领域（站点标注） | — | 0.9 MB | 3774 | hist |
| 270 | Korg M1 Guitar Restored | Reza Khadafi | musical-artifacts | 公有领域（站点标注） | — | 1.2 MB | 2435 | hist |
| 271 | Korg Wavestation Koto Restored | Reza Khadafi | musical-artifacts | 公有领域（站点标注） | — | 1.3 MB | 1949 | hist |
| 272 | Roland GS Wavetable Synth | Roland Corporation | archive | 公有领域 | ✓ | 3.1 MB | — | hist |
| 273 | Kurzweil K2000 STRUMMER GUITAR (SF2 Samples) | Aleksandr Bykov | archive | CC0 | ✓ | 60.7 MB | — | hist |
| 274 | Kurzweil K2000 STEEL STRING GUITAR (SF2 Samples) | The GP, Aleksandr Bykov | archive | CC0 | ✓ | 286.3 MB | — | hist |
| 275 | Kurzweil K2000 BRITE PIANO (SF2 Samples) | The GP, Aleksandr Bykov | archive | CC0 | ✓ | 378.0 MB | — | hist |
| 276 | Kurzweil K2000 STEREO GRAND (SF2 Samples) | The GP, Aleksandr Bykov | archive | CC0 | ✓ | 425.7 MB | — | hist |
| 277 | Yamaha TG 300 | — | archive | 公有领域 | ✓ | 566.3 MB | — | hist |
| 278 | Kurzweil K2000 ALL IN THE FADER (SF2 Samples) | The GP, Aleksandr Bykov | archive | CC0 | ✓ | 703.8 MB | — | hist |
| 279 | Roland SC-88 (Full Version) | Mr.Sanic | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 116935 | hist |
| 280 | Roland SC-8820 SoundFont | Mr.Sanic | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 26551 | hist |
| 281 | Florestan Basic GM GS | Nando Florestan | musical-artifacts | 公有领域（站点标注） | ✓ | — | 12837 | hist |
| 282 | EVE burst error (PC-98) Soundfont | Ryu Umemoto | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 12696 | hist |
| 283 | little-scale's Yamaha MX100II Disklavier | Placeholder Stick, little-scal | musical-artifacts | 公有领域（站点标注） | ✓ | — | 7036 | hist |
| 284 | Acapella Group XG(S)MT88* | stgiga, stin/HighCPU/YoshiLove | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 6818 | hist |
| 285 | ZFont | Zalka | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 5533 | hist |
| 286 | The Mega Musical Soundfont | SandisBergvalds2008 | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 4155 | hist |
| 287 | Furnace FM General Midi | Mx. K | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 3969 | hist |
| 288 | Furnace OPL (General Midi Compatable) | Mx. K | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 2912 | hist |
| 289 | Vintage Ecuador sample pack | Milton Paredes, MPJ Factory st | musical-artifacts | WTFPL（等同公有领域） | — | — | 1905 | hist |
| 290 | Microsoft GS Wavetable SF2 | Roland, Microsoft | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 1397 | hist |
| 291 | HappyTreeFriends Recreated Midi Soundbanks. (my 3 versions) | CupheadKrasueHTFBewilderHouseF | musical-artifacts | 公有领域（站点标注） | ✓ | — | 1085 | hist |
| 292 | Pablemo 2023 | Pablemo | musical-artifacts | WTFPL（等同公有领域） | — | — | 876 | hist |
| 293 | Korg Triton Orchestra Hit Soundfont | Mildanner | musical-artifacts | 公有领域（站点标注） | ✓ | — | 812 | hist |
| 294 | Korg WAVESTATION Touch Organ Soundfont | Mildanner, KORG | musical-artifacts | 公有领域（站点标注） | ✓ | — | 710 | hist |
| 295 | Korg Triton Square Roots Soundfont | Mildanner | musical-artifacts | 公有领域（站点标注） | ✓ | — | 689 | hist |
| 296 | E-Mu Emax II South American Pipe and 2MGM + SC-55 Ice Rain in SF2 | BloodEater2704 | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 508 | hist |
| 297 | Nokia 3510 Soundfonts/Chippy Bank | — | polyphone | 公有领域 | ✓ | — | 378 | hist |
| 298 | Hand Piano | — | polyphone | 公有领域 | ✓ | — | 261 | hist |
| 299 | French Horn Section | — | polyphone | 公有领域 | ✓ | — | 204 | hist |
| 300 | WBS Instruments GS Lite | — | polyphone | 公有领域 | — | — | 136 | hist |
| 301 | SpongeBob squigglepants nds (Prototype, really) | — | polyphone | 公有领域 | ✓ | — | 84 | hist |
| 302 | Yamaha Timpani | — | polyphone | 公有领域 | ✓ | — | 74 | hist |
| 303 | Timpani Symphony | — | polyphone | 公有领域 | ✓ | — | 48 | hist |
| 304 | Crash of the Titans ds Incomplete | — | polyphone | 公有领域 | ✓ | — | 15 | hist |
| 305 | Ocarina | FreePats project | FreePats | CC0 | ✓ | 3.0 MB | — | orch |
| 306 | Concert Harp | Versilian Studios LLC | FreePats | CC0 | ✓ | 4.9 MB | — | orch |
| 307 | Tenor Saxophone | Versilian Studios LLC | FreePats | CC0 | ✓ | 6.5 MB | — | orch |
| 308 | Clarinet | FreePats project | FreePats | CC0 | ✓ | 6.7 MB | — | orch |
| 309 | Wooden Recorder | Eugene Vlaskin | FreePats | CC0 | ✓ | 7.9 MB | — | orch |
| 310 | War Tuba | Karoryfer Samples | sfzinstruments | CC0 | — | 104.0 MB | — | orch |
| 311 | Realistic Brass and Woodwinds | Travekagent | archive | 公有领域 | ✓ | 267.2 MB | — | orch |
| 312 | Sneakybass | Karoryfer Samples | sfzinstruments | CC0 | — | 324.0 MB | — | orch |
| 313 | Thomas & Friends: Robert Hartshorne's Sound Font Instruments (Series 8 | Robert Hartshorne, ThomasFan19 | archive | 公有领域 | — | 614.8 MB | — | orch |
| 314 | VS Chamber Orchestra: Community Edition | Versilian Studios LLC | sfzinstruments | CC0 | — | 2355.2 MB | — | orch |
| 315 | Squidfont Orchestral Soundfont | the guy2 (soundfont by bigsqui | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 47867 | orch |
| 316 | Florestan String Quartet | Nando Florestan | musical-artifacts | 公有领域（站点标注） | ✓ | — | 18620 | orch |
| 317 | Florestan Woodwinds | Nando Florestan | musical-artifacts | 公有领域（站点标注） | ✓ | — | 14177 | orch |
| 318 | tuba-ff | isis999 | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 6893 | orch |
| 319 | Florestan Strings | Nando Florestan | musical-artifacts | 公有领域（站点标注） | ✓ | — | 5594 | orch |
| 320 | Dizi from Freesound | Placeholder Stick | musical-artifacts | 公有领域（站点标注） | ✓ | — | 4728 | orch |
| 321 | Florestan Trumpet Metallic | Nando Florestan | musical-artifacts | 公有领域（站点标注） | ✓ | — | 4452 | orch |
| 322 | All-Around Violin | ? | polyphone | 公有领域 | ✓ | — | 3846 | orch |
| 323 | tenor-trombone-gig | isis999 | musical-artifacts | WTFPL（等同公有领域） | — | — | 3720 | orch |
| 324 | Synth Brass 2 | Strix SoundFont Team | musical-artifacts | 公有领域（站点标注） | ✓ | — | 3324 | orch |
| 325 | Arianna&#039;s Violin | — | polyphone | 公有领域 | — | — | 2532 | orch |
| 326 | Kiara Klarinet | Duplex | musical-artifacts | 公有领域（站点标注） | ✓ | — | 2408 | orch |
| 327 | French horns | ? | polyphone | 公有领域 | ✓ | — | 2228 | orch |
| 328 | Good flute | ? | polyphone | 公有领域 | ✓ | — | 1582 | orch |
| 329 | SJ Staccato Strings Fixed | ? | polyphone | 公有领域 | ✓ | — | 1344 | orch |
| 330 | Strings Beautiful Lyrical | ? | polyphone | 公有领域 | ✓ | — | 1173 | orch |
| 331 | Orchestral Strings | ? | polyphone | 公有领域 | ✓ | — | 1037 | orch |
| 332 | SAXoz | — | polyphone | 公有领域 | — | — | 1024 | orch |
| 333 | Baritone Horn | — | polyphone | 公有领域 | ✓ | — | 1002 | orch |
| 334 | Various wood instruments | Fox-Gieg | polyphone | 公有领域 | ✓ | — | 939 | orch |
| 335 | Heroic horns | ? | polyphone | 公有领域 | ✓ | — | 893 | orch |
| 336 | KH trumpet | ? | polyphone | 公有领域 | ✓ | — | 814 | orch |
| 337 | Windsor Banjo c1920 -1930 | — | polyphone | 公有领域 | ✓ | — | 807 | orch |
| 338 | Genycis Orchestrings | ? | polyphone | 公有领域 | ✓ | — | 782 | orch |
| 339 | Concerto Cello | ? | polyphone | 公有领域 | ✓ | — | 770 | orch |
| 340 | ViolinMartele | — | polyphone | 公有领域 | ✓ | — | 765 | orch |
| 341 | KBH - Ultima strings | ? | polyphone | 公有领域 | ✓ | — | 735 | orch |
| 342 | Mountain Dulcimer - Experimental | — | polyphone | 公有领域 | ✓ | — | 728 | orch |
| 343 | Zemljak Overture | Viktor Zemljak | polyphone | 公有领域 | ✓ | — | 709 | orch |
| 344 | Section horns | ? | polyphone | 公有领域 | ✓ | — | 672 | orch |
| 345 | Mandolino | — | polyphone | 公有领域 | ✓ | — | 639 | orch |
| 346 | Strings orch. | ? | polyphone | 公有领域 | ✓ | — | 615 | orch |
| 347 | Alto flute | ? | polyphone | 公有领域 | ✓ | — | 585 | orch |
| 348 | ViolinCLASS | — | polyphone | 公有领域 | ✓ | — | 558 | orch |
| 349 | 024 Big Symphony | ? | polyphone | 公有领域 | — | — | 547 | orch |
| 350 | Ixox Flute Full v0.2 | ? | polyphone | 公有领域 | ✓ | — | 534 | orch |
| 351 | Pan Flute | — | polyphone | 公有领域 | ✓ | — | 530 | orch |
| 352 | Flugel horns | ? | polyphone | 公有领域 | ✓ | — | 520 | orch |
| 353 | Recorders | — | polyphone | 公有领域 | — | — | 485 | orch |
| 354 | Massive &amp; Slow strings | ? | polyphone | 公有领域 | ✓ | — | 453 | orch |
| 355 | Brass squirt | Fox-Gieg | polyphone | 公有领域 | ✓ | — | 448 | orch |
| 356 | Dirty Strings | Fox-Gieg | polyphone | 公有领域 | ✓ | — | 448 | orch |
| 357 | 060 Florestan French Horns | Nando Florestan | polyphone | 公有领域 | ✓ | — | 441 | orch |
| 358 | Violin Campbell&#039;s | ? | polyphone | 公有领域 | ✓ | — | 436 | orch |
| 359 | Violin | ? | polyphone | 公有领域 | ✓ | — | 432 | orch |
| 360 | Strings Trill | ? | polyphone | 公有领域 | ✓ | — | 420 | orch |
| 361 | 068-073 Florestan woodwinds | Nando Florestan | polyphone | 公有领域 | ✓ | — | 419 | orch |
| 362 | 2 trumpets | ? | polyphone | 公有领域 | ✓ | — | 413 | orch |
| 363 | Florestan strings | Nando Florestan | polyphone | 公有领域 | ✓ | — | 372 | orch |
| 364 | Arco celli | ? | polyphone | 公有领域 | ✓ | — | 355 | orch |
| 365 | Cams Flute | Campbell Barton | polyphone | 公有领域 | ✓ | — | 353 | orch |
| 366 | UnderFilm | ? | polyphone | 公有领域 | ✓ | — | 338 | orch |
| 367 | Dizi From Freesound | — | polyphone | 公有领域 | ✓ | — | 330 | orch |
| 368 | Nylon atmosphere | Fox-Gieg | polyphone | 公有领域 | ✓ | — | 330 | orch |
| 369 | Tubahs | — | polyphone | 公有领域 | ✓ | — | 280 | orch |
| 370 | String big sustain | ? | polyphone | 公有领域 | — | — | 275 | orch |
| 371 | Carter&#039;s Yamaha Recorders | — | polyphone | 公有领域 | ✓ | — | 268 | orch |
| 372 | Natural Flute | — | polyphone | 公有领域 | ✓ | — | 261 | orch |
| 373 | Flute Sound font | — | polyphone | 公有领域 | ✓ | — | 258 | orch |
| 374 | ViolinLDKone | — | polyphone | 公有领域 | ✓ | — | 254 | orch |
| 375 | Heckelphone | — | polyphone | 公有领域 | ✓ | — | 251 | orch |
| 376 | Violín Real | — | polyphone | 公有领域 | ✓ | — | 227 | orch |
| 377 | Acoustic Bass | — | polyphone | 公有领域 | ✓ | — | 222 | orch |
| 378 | Flute Test | — | polyphone | 公有领域 | ✓ | — | 184 | orch |
| 379 | Recorders | — | polyphone | 公有领域 | ✓ | — | 178 | orch |
| 380 | Synth Flute | — | polyphone | 公有领域 | ✓ | — | 172 | orch |
| 381 | Low strings | — | polyphone | 公有领域 | ✓ | — | 160 | orch |
| 382 | Recorder Synth | — | polyphone | 公有领域 | ✓ | — | 149 | orch |
| 383 | Alto Recorder | — | polyphone | 公有领域 | ✓ | — | 101 | orch |
| 384 | Harp 26 | — | polyphone | 公有领域 | ✓ | — | 56 | orch |
| 385 | Bear Sax | Karoryfer Samples | sfzinstruments | CC0 | — | — | — | orch |
| 386 | Bigcat Cello | Karoryfer Samples | sfzinstruments | CC0 | — | — | — | orch |
| 387 | D. Smolken Double Bass | Karoryfer Samples | sfzinstruments | CC0 | — | — | — | orch |
| 388 | Meatbass | Karoryfer Samples | sfzinstruments | CC0 | — | — | — | orch |
| 389 | Squidpipes | Karoryfer Samples | sfzinstruments | CC0 | — | — | — | orch |
| 390 | String Cyborgs | Karoryfer Samples | sfzinstruments | CC0 | — | — | — | orch |
| 391 | The Total Composure Orchestra V 1.0.zip | Xtant Audio | archive | 公有领域 | — | — | — | orch |
| 392 | Weresax | Karoryfer Samples | sfzinstruments | CC0 | — | — | — | orch |
| 393 | Button Accordion HN | Jeff Stauffer | FreePats | CC0 | — | 4.8 MB | — | organ |
| 394 | Drawbar organ emulation | Roberto | FreePats | CC0 | ✓ | 5.8 MB | — | organ |
| 395 | Percussive organ emulation | FreePats project | FreePats | CC0 | ✓ | 12.0 MB | — | organ |
| 396 | Rock organ emulation | FreePats project | FreePats | CC0 | ✓ | 12.0 MB | — | organ |
| 397 | Church Organ Emulation | Fons Adriaensen | FreePats | CC0 | ✓ | 13.0 MB | — | organ |
| 398 | Gothic organ | Adrian Wagner | polyphone | 公有领域 | ✓ | — | 1326 | organ |
| 399 | Various organs | Fox-Gieg | polyphone | 公有领域 | ✓ | — | 643 | organ |
| 400 | M3R organs | Guido Scognamiglio | polyphone | 公有领域 | ✓ | — | 546 | organ |
| 401 | Ambiant organ | ? | polyphone | 公有领域 | ✓ | — | 453 | organ |
| 402 | Hammond b organ | — | polyphone | 公有领域 | ✓ | — | 213 | organ |
| 403 | Hammond B3 | — | polyphone | 公有领域 | ✓ | — | 143 | organ |
| 404 | Hammond B3 Slow Leslie | — | polyphone | 公有领域 | ✓ | — | 108 | organ |
| 405 | FREAK!!PAD | — | polyphone | 公有领域 | ✓ | — | 106 | organ |
| 406 | DJ's Hip Hop Kit | DJ Incendration | musical-artifacts | WTFPL（等同公有领域） | — | 0.1 MB | 1820 | other |
| 407 | DTS Soundfont | Swarm | archive | 公有领域 | ✓ | 0.3 MB | — | other |
| 408 | Milo Murphy's Law Soundfont | RunTheCoins | archive | CC0 | ✓ | 0.4 MB | — | other |
| 409 | dirtyyy | NikkyHika | archive | CC0 | ✓ | 0.6 MB | — | other |
| 410 | RemyMarshal's worlds smallest soundfont (electric piano) | RemyMarshal | musical-artifacts | WTFPL（等同公有领域） | ✓ | 0.7 MB | 129 | other |
| 411 | Minecraft Noteblock Soundfont v4.00 | happy_mimimix | archive | 公有领域 | ✓ | 0.7 MB | — | other |
| 412 | Random Soundfont Public Version 1 | DamonCat | archive | 公有领域 | — | 1.3 MB | — | other |
| 413 | new super mario bros world 1 soundfont | nintendo ( ripped by me ) | archive | CC0 | ✓ | 1.7 MB | — | other |
| 414 | SM64 SF | JackJamesMacdonald5 | archive | CC0 | ✓ | 4.5 MB | — | other |
| 415 | Ravers & Gabbers 2 | ZwamTek Music | archive | 公有领域 | ✓ | 9.2 MB | — | other |
| 416 | Gamer’s Tracker-MIDI(nSF2) Extracted Collection | Gamer45, technically also by m | musical-artifacts | WTFPL（等同公有领域） | ✓ | 12.5 MB | 445 | other |
| 417 | Ethan Winer Collection | Ethan Winer | sfzinstruments | 公有领域 | — | 17.0 MB | — | other |
| 418 | Soundfonts | rabid47 | archive | CC0 | ✓ | 21.0 MB | — | other |
| 419 | Media Tek MT 6235 Soundfont | MediaTek | archive | CC0 | ✓ | 21.1 MB | — | other |
| 420 | PrismCorp's Soundfonts | Creative Technology, NTONYX, & | archive | 公有领域 | ✓ | 30.9 MB | — | other |
| 421 | Pokémon BW+ SoundFont ~ Demos & Resources) | — | archive | CC0 | — | 55.0 MB | — | other |
| 422 | Addictive Instruments | Abel Esteban | archive | CC0 | ✓ | 196.0 MB | — | other |
| 423 | Delta Touch 5.1 apk | — | archive | 公有领域 | — | 249.2 MB | — | other |
| 424 | Online Sequencer Soundfont | Landon & Emma | archive | CC0 | ✓ | 403.1 MB | — | other |
| 425 | The Beanies '94 soundfont ~ Demos & Resources | Mary Koelpin | archive | CC0 | — | 421.3 MB | — | other |
| 426 | Mystic Island Soundfonts ~ DIRECTOR'S CUT (Demos and resources | Village Roadshow, Imagine Tele | archive | CC0 | — | 456.9 MB | — | other |
| 427 | SOUNDFONTS of Sample Archives | Fahad Lami | archive | 公有领域 | ✓ | 526.9 MB | — | other |
| 428 | SF 2 Pack VI. 7z | 白いチャンネル | archive | 公有领域 | — | 820.9 MB | — | other |
| 429 | Families: The Soundfont (SF2) | Titmouse, inc., Film Roman, 9  | archive | CC0 | — | 955.1 MB | — | other |
| 430 | SF 2 Pack IV. 7z | 白いチャンネル | archive | 公有领域 | — | 1135.7 MB | — | other |
| 431 | Fanon Park SoundFont ~ Reworked (demos & resources) | PROJECT FANON PARK | archive | CC0 | — | 1395.9 MB | — | other |
| 432 | Soundfont Collection | William Borges dos Santos | archive | 公有领域 | ✓ | 1610.9 MB | — | other |
| 433 | SF 2 Pack. 7z | 白いチャンネル | archive | 公有领域 | — | 2034.5 MB | — | other |
| 434 | SF 2 Pack III. 7z | 白いチャンネル | archive | 公有领域 | — | 2229.6 MB | — | other |
| 435 | sf2-soundfonts(free-use) | — | archive | 公有领域 | — | 2731.0 MB | — | other |
| 436 | Versilian Community Sample Library | Versilian Studios LLC | sfzinstruments | CC0 | — | 4096.0 MB | — | other |
| 437 | Arab and Turk instruments | Fernando A. Martin (compilatio | musical-artifacts | 公有领域（站点标注） | ✓ | — | 14081 | other |
| 438 | Windows Soundfont HD (SC-55) | — | polyphone | 公有领域 | — | — | 8877 | other |
| 439 | Digidesign SampleCell II Factory Library Soundfont | — | polyphone | 公有领域 | — | — | 8621 | other |
| 440 | The Discord Soundfont | Tyrone Monroe | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 6503 | other |
| 441 | Florestan Tubular Bells | Nando Florestan | musical-artifacts | 公有领域（站点标注） | ✓ | — | 4530 | other |
| 442 | Vine Boom Sound Effect | BlueKirby | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 4381 | other |
| 443 | EAWpats the soundfont | jamisson tavares | musical-artifacts | 公有领域（站点标注） | ✓ | — | 3974 | other |
| 444 | Florestan Pizzicato | Nando Florestan | musical-artifacts | 公有领域（站点标注） | ✓ | — | 3879 | other |
| 445 | MR BEAST soundfont | by a Literally unmentioned per | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 3577 | other |
| 446 | Bellatrix Orchestra | ? | polyphone | 公有领域 | — | — | 3519 | other |
| 447 | Rave Stab SoundFont | Strix SoundFont Team | musical-artifacts | 公有领域（站点标注） | ✓ | — | 3455 | other |
| 448 | Campbell's Verby Vocal Soundfont | Campbell Barton | musical-artifacts | 公有领域（站点标注） | ✓ | — | 3137 | other |
| 449 | Rayman 3 GBA Soundfont | Dr. Kiwis | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 2753 | other |
| 450 | LG_T375 Soundfont | jamisson tavares | musical-artifacts | 公有领域（站点标注） | ✓ | — | 2338 | other |
| 451 | Pixitracker Soundfont | hqc | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 2314 | other |
| 452 | Mega Man Zero 1 4 Soundfont ( VER 1) | Jordan Moore | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 2265 | other |
| 453 | Cat Meow Soundfont | Unknown | musical-artifacts | 公有领域（站点标注） | ✓ | — | 1952 | other |
| 454 | Nokia 3310 Soundfont | Nokia | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 1943 | other |
| 455 | Air.ogg SoundFont | boq | musical-artifacts | 公有领域（站点标注） | ✓ | — | 1915 | other |
| 456 | MSG-8x | Arsi | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 1676 | other |
| 457 | Baroque Harpsichord | ? | polyphone | 公有领域 | ✓ | — | 1642 | other |
| 458 | PS1/PSX BIOS Soundfont | — | polyphone | 公有领域 | ✓ | — | 1496 | other |
| 459 | Trombone.sf2 V.0.4 | Guy | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 1409 | other |
| 460 | Vintage instruments | ? | polyphone | 公有领域 | ✓ | — | 1137 | other |
| 461 | MicroSalterDroid (SONiVOX BAE Style) | Roe_2012 | musical-artifacts | 公有领域（站点标注） | ✓ | — | 1121 | other |
| 462 | Jew&#039;s harp | ? | polyphone | 公有领域 | ✓ | — | 1115 | other |
| 463 | Megadimension Neptunia VII - Nep Nep Nep | James Monroe | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 1099 | other |
| 464 | John Tay Marble Zone Good Future SF2 | Jojo Witstar | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 1082 | other |
| 465 | German8 harpsichord | ? | polyphone | 公有领域 | ✓ | — | 1074 | other |
| 466 | John Tay's Hydro City Act 2 Remix SF2 | Mx. K | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 1064 | other |
| 467 | Monsoon&#039;s Hohner C Harmonica | — | polyphone | 公有领域 | ✓ | — | 1041 | other |
| 468 | Pokémon Black 2 and White 2 Soundfont (Compiled) | — | polyphone | 公有领域 | ✓ | — | 892 | other |
| 469 | Pokémon DPPt HQ GM | TheIndigoShine | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 863 | other |
| 470 | Oboe stereo | ? | polyphone | 公有领域 | ✓ | — | 832 | other |
| 471 | Pokemon Black 2 &amp; White 2 | — | polyphone | 公有领域 | ✓ | — | 772 | other |
| 472 | Various loops | Fox-Gieg / Wallin / Dollee | polyphone | 公有领域 | ✓ | — | 696 | other |
| 473 | Tired accordion | Timothy Quach | polyphone | 公有领域 | ✓ | — | 664 | other |
| 474 | Sonor Force 3007 Huge Drum Kit | — | polyphone | 公有领域 | ✓ | — | 626 | other |
| 475 | Plants Vs. Zombies | — | polyphone | 公有领域 | ✓ | — | 552 | other |
| 476 | EarthBound samples HQ | — | polyphone | 公有领域 | ✓ | — | 520 | other |
| 477 | COMS (Collection of my samples) - 1.1 | Bernardo Jose | musical-artifacts | 公有领域（站点标注） | ✓ | — | 506 | other |
| 478 | FoxOG.sf2 V6 Test (SRB2 Soundfont) | LusterArtz | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 442 | other |
| 479 | Clarinets 1 | ? | polyphone | 公有领域 | ✓ | — | 397 | other |
| 480 | English Horn Eddie&#039;s | ? | polyphone | 公有领域 | ✓ | — | 395 | other |
| 481 | Kazoo | — | polyphone | 公有领域 | ✓ | — | 374 | other |
| 482 | Jellyfish Jam W.I.P | — | polyphone | 公有领域 | ✓ | — | 366 | other |
| 483 | Alto oboe | ? | polyphone | 公有领域 | ✓ | — | 344 | other |
| 484 | roland boutique TR-09 (digital clon of roland) | — | polyphone | 公有领域 | ✓ | — | 344 | other |
| 485 | Clarinet Soundfont | — | polyphone | 公有领域 | ✓ | — | 340 | other |
| 486 | 076 Florestan Contrabassoon | Nando Florestan | polyphone | 公有领域 | ✓ | — | 292 | other |
| 487 | Plusho's Soundfont (V0.01) | PlushoRR | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 284 | other |
| 488 | Paradise | ? | polyphone | 公有领域 | ✓ | — | 280 | other |
| 489 | Bass Clarinet | — | polyphone | 公有领域 | ✓ | — | 279 | other |
| 490 | 8-bit Soundfont | — | polyphone | 公有领域 | ✓ | — | 278 | other |
| 491 | Alto Shawm | — | polyphone | 公有领域 | — | — | 263 | other |
| 492 | ROM samples | Fox-Gieg / Romo | polyphone | 公有领域 | ✓ | — | 243 | other |
| 493 | Illusion Bank | ? | polyphone | 公有领域 | ✓ | — | 242 | other |
| 494 | wah wah bassoon | — | polyphone | 公有领域 | ✓ | — | 231 | other |
| 495 | Sunset Brass | Wallo | musical-artifacts | 公有领域（站点标注） | ✓ | — | 226 | other |
| 496 | Diner Dash: Sizzle & Serve [DS] ripped soundfonts and midis | Secret Stash Games/Syrox Devel | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 225 | other |
| 497 | 1812 | ? | polyphone | 公有领域 | ✓ | — | 196 | other |
| 498 | ineedu32 | ? | polyphone | 公有领域 | ✓ | — | 192 | other |
| 499 | Various | ? | polyphone | 公有领域 | ✓ | — | 192 | other |
| 500 | Dalores "Hm" Soundfont (Encanto) | Landon & Emma | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 182 | other |
| 501 | Battle Network 3 - Incomplete | — | polyphone | 公有领域 | ✓ | — | 176 | other |
| 502 | SheZow Soundfont (WIP) | ShiverThermal | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 164 | other |
| 503 | Picturesque 1 - data moshing | — | polyphone | 公有领域 | ✓ | — | 163 | other |
| 504 | 8 bit beep | — | polyphone | 公有领域 | ✓ | — | 144 | other |
| 505 | hoy es domingo full | Milton Paredes, MPJ Factory st | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 131 | other |
| 506 | SpongeBob Sound Font Pack Volume 1 | — | polyphone | 公有领域 | ✓ | — | 125 | other |
| 507 | fofo soundfont (halloween: just the facts) | lakery | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 117 | other |
| 508 | DogFont V1 | — | polyphone | 公有领域 | ✓ | — | 110 | other |
| 509 | Memes the Soundfont | — | polyphone | 公有领域 | — | — | 97 | other |
| 510 | Bass Clarinet | — | polyphone | 公有领域 | ✓ | — | 91 | other |
| 511 | very bad quality sf2 | — | polyphone | 公有领域 | ✓ | — | 87 | other |
| 512 | NewOrder basic sounds | — | polyphone | 公有领域 | ✓ | — | 85 | other |
| 513 | The Florestan sf2 | — | polyphone | 公有领域 | ✓ | — | 82 | other |
| 514 | Hit de Orquesta (varios) | — | polyphone | 公有领域 | ✓ | — | 75 | other |
| 515 | Mellotron Samples (ignore placeholder soundfont) | — | polyphone | 公有领域 | ✓ | — | 66 | other |
| 516 | SpongeBob Sound Font Pack Volume 2 | — | polyphone | 公有领域 | ✓ | — | 55 | other |
| 517 | Megaman 0-33 | — | polyphone | 公有领域 | ✓ | — | 52 | other |
| 518 | SpongeBob SquarePants: SuperSponge Soundfont | — | polyphone | 公有领域 | ✓ | — | 52 | other |
| 519 | MiniiFont Giga 60 Instruments | — | polyphone | 公有领域 | ✓ | — | 51 | other |
| 520 | SpongeBob Sound Font Pack Volume 3 | — | polyphone | 公有领域 | ✓ | — | 48 | other |
| 521 | Daytona USA Soundfont | — | polyphone | 公有领域 | ✓ | — | 45 | other |
| 522 | BRUH Soundfont | — | polyphone | 公有领域 | ✓ | — | 43 | other |
| 523 | Deep Fried Laugh | — | polyphone | 公有领域 | ✓ | — | 40 | other |
| 524 | MiniiFont V11 | — | polyphone | 公有领域 | ✓ | — | 36 | other |
| 525 | Fang Brawl Stars FNF | — | polyphone | 公有领域 | ✓ | — | 32 | other |
| 526 | PublicSoundfont | — | polyphone | 公有领域 | ✓ | — | 31 | other |
| 527 | BATMAN FOREVER SNES | — | polyphone | 公有领域 | ✓ | — | 25 | other |
| 528 | SpongeBob Atlantis SquarePantis Altron SoundFont | — | polyphone | 公有领域 | ✓ | — | 24 | other |
| 529 | Crash of the Titans ds sounds instruments use this on fl studio mobile | — | polyphone | 公有领域 | — | — | 21 | other |
| 530 | Nicktoons_unite | — | polyphone | 公有领域 | ✓ | — | 21 | other |
| 531 | SpongeBob altron soundfonts | — | polyphone | 公有领域 | ✓ | — | 20 | other |
| 532 | BFPOR  Soundfont | — | polyphone | 公有领域 | ✓ | — | 19 | other |
| 533 | Le cleir de lune (Persona 2 Eternal Punishment) SF2 | — | polyphone | 公有领域 | ✓ | — | 18 | other |
| 534 | SRB2 Final Demo Soundfont | — | polyphone | 公有领域 | ✓ | — | 18 | other |
| 535 | Survivalcraft 2 | — | polyphone | 公有领域 | ✓ | — | 18 | other |
| 536 | Sla | — | polyphone | 公有领域 | — | — | 13 | other |
| 537 | Magicore Anomala Soundfont | — | polyphone | 公有领域 | ✓ | — | 8 | other |
| 538 | #RaduLucian1975 | #RaduLucian1975 | archive | 公有领域 | — | — | — | other |
| 539 | Dr Who Toy Soundfont | BBC | archive | CC0 | — | — | — | other |
| 540 | Easy Soundfont Player SF2 | — | archive | 公有领域 | — | — | — | other |
| 541 | Ergo electric upright bass | Karoryfer Samples | sfzinstruments | CC0 | — | — | — | other |
| 542 | Falling Away From Me (SM64 Soundfont) | Ultra Enzo | archive | 公有领域 | — | — | — | other |
| 543 | Fanon Park Nostalgia Soundfonts ~ DIRECTOR'S CUT – Demo Files | — | archive | CC0 | — | — | — | other |
| 544 | Goldberg Variations - Grossman (midis), Blanchet 1720 (soundfont), Leh | John T. Prince | archive | CC0 | — | — | — | other |
| 545 | Helper for MusESequenzer | Bernd Mullet | musical-artifacts | WTFPL（等同公有领域） | — | — | 0 | other |
| 546 | OXOP SoundSet | OXOP | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 0 | other |
| 547 | SF 2 Pack VII. 7z | 白いチャンネル | archive | 公有领域 | — | — | — | other |
| 548 | The Midnight Animal Show SoundFonts ~ demo files | MILKY CARTOON ltd. | archive | 公有领域 | — | — | — | other |
| 549 | Windows Soundfont GM Standard No Banks and Modulators 128+1_Drumset | Conp Et Sepohk | musical-artifacts | 公有领域（站点标注） | ✓ | — | 0 | other |
| 550 | FM Synthesized Piano #2 | FreePats project | FreePats | CC0 | ✓ | 4.6 MB | — | piano |
| 551 | LX Space Piano - Soundfont sf2 | LexSound | archive | 公有领域 | ✓ | 5.4 MB | — | piano |
| 552 | Upright Piano KW | Gonzalo | FreePats | CC0 | ✓ | 5.8 MB | — | piano |
| 553 | Old Piano FB | FreePats project | FreePats | CC0 | ✓ | 8.8 MB | — | piano |
| 554 | FM Synthesized Piano #1 | FreePats project | FreePats | CC0 | ✓ | 13.0 MB | — | piano |
| 555 | FM Electric Piano | Strix SoundFont Team | musical-artifacts | 公有领域（站点标注） | ✓ | 53.7 MB | 8273 | piano |
| 556 | Splendid Grand Piano | AKAI | sfzinstruments | 公有领域 | — | 77.0 MB | — | piano |
| 557 | ILIO Sinclavier Essential Percussion (Soundfont/.sf2 Conversion) | — | archive | CC0 | — | 232.1 MB | — | piano |
| 558 | ILIO Synclavier Essential Percussion (Disc 2): World & Orchestral (Sou | — | archive | CC0 | — | 394.0 MB | — | piano |
| 559 | VCSL Keys | Versilian Studios LLC | sfzinstruments | CC0 | — | 680.0 MB | — | piano |
| 560 | Rhodes EVP73 Soundfont | OK73 | musical-artifacts | 公有领域（站点标注） | ✓ | — | 9433 | piano |
| 561 | Campbells Grand Piano Beta 2 Soundfont | Campbell Barton | musical-artifacts | 公有领域（站点标注） | ✓ | — | 7046 | piano |
| 562 | VS Upright Piano lite (soundfont version) | Versilian Studios | musical-artifacts | 公有领域（站点标注） | ✓ | — | 6112 | piano |
| 563 | Florestan Piano | Nando Florestan | musical-artifacts | 公有领域（站点标注） | ✓ | — | 5787 | piano |
| 564 | Kawai Stereo Grand | Matias Rockas | polyphone | 公有领域 | ✓ | — | 1437 | piano |
| 565 | Crystal Rhodes Piano | ? | polyphone | 公有领域 | ✓ | — | 1252 | piano |
| 566 | J-Rhodes | Jeff Learman | polyphone | 公有领域 | ✓ | — | 931 | piano |
| 567 | 000 Florestan Piano | Nando Florestan | polyphone | 公有领域 | ✓ | — | 911 | piano |
| 568 | schpn Piano | ? | polyphone | 公有领域 | ✓ | — | 726 | piano |
| 569 | Nord Royal Grand 3D | — | polyphone | 公有领域 | ✓ | — | 723 | piano |
| 570 | Grand piano | ? | polyphone | 公有领域 | ✓ | — | 712 | piano |
| 571 | Soft Piano 1 | — | polyphone | 公有领域 | ✓ | — | 697 | piano |
| 572 | Velocity Grand Piano | ? | polyphone | 公有领域 | ✓ | — | 685 | piano |
| 573 | Piano and Strings | ? | polyphone | 公有领域 | ✓ | — | 532 | piano |
| 574 | Nord Warm Pad | — | polyphone | 公有领域 | ✓ | — | 477 | piano |
| 575 | U20 piano | Matias Rockas | polyphone | 公有领域 | ✓ | — | 430 | piano |
| 576 | Nine-foot grand | Tim Swartz | polyphone | 公有领域 | ✓ | — | 418 | piano |
| 577 | Baldi Soundfont | — | polyphone | 公有领域 | ✓ | — | 393 | piano |
| 578 | Little grand piano | ? | polyphone | 公有领域 | ✓ | — | 354 | piano |
| 579 | Nord Royal Grand Soft 2026 | — | polyphone | 公有领域 | ✓ | — | 354 | piano |
| 580 | Piano set | Stephane Bernard | polyphone | 公有领域 | ✓ | — | 340 | piano |
| 581 | CP80 PSR433 | — | polyphone | 公有领域 | ✓ | — | 338 | piano |
| 582 | BaconPlays&#039;s Grand Piano V0.9a | — | polyphone | 公有领域 | ✓ | — | 323 | piano |
| 583 | SS Steinway | — | polyphone | 公有领域 | ✓ | — | 300 | piano |
| 584 | Thrift Store Spinet Piano | — | polyphone | 公有领域 | ✓ | — | 294 | piano |
| 585 | Nord PCM Pad | — | polyphone | 公有领域 | ✓ | — | 277 | piano |
| 586 | Nord Electric DX Full | — | polyphone | 公有领域 | ✓ | — | 233 | piano |
| 587 | MK7 Chromatic MAJ CHORDS | — | polyphone | 公有领域 | ✓ | — | 216 | piano |
| 588 | Grand Piano HD | — | polyphone | 公有领域 | ✓ | — | 212 | piano |
| 589 | Super 5 | Myself - Aaron Gleason | musical-artifacts | 公有领域（站点标注） | ✓ | — | 208 | piano |
| 590 | SF2 Pack | — | polyphone | 公有领域 | ✓ | — | 204 | piano |
| 591 | Piano Grand 3 - Model D | — | polyphone | 公有领域 | ✓ | — | 203 | piano |
| 592 | Baldi&#039;s Least Favorite Tape | — | polyphone | 公有领域 | ✓ | — | 199 | piano |
| 593 | Concert Royal Grand Piano | — | polyphone | 公有领域 | ✓ | — | 192 | piano |
| 594 | Glitched Piano Soundfont | — | polyphone | 公有领域 | ✓ | — | 189 | piano |
| 595 | Stage Piano | — | polyphone | 公有领域 | ✓ | — | 182 | piano |
| 596 | Super Mario Bros. Soundfont - SMB (SMB1) (2022 UPDATE) - 2022 - Presen | — | polyphone | 公有领域 | ✓ | — | 180 | piano |
| 597 | Nord Dyno EP | — | polyphone | 公有领域 | ✓ | — | 177 | piano |
| 598 | Fuchs &amp; Möhr Felt Piano | — | polyphone | 公有领域 | — | — | 171 | piano |
| 599 | Nord Black Upright | — | polyphone | 公有领域 | ✓ | — | 171 | piano |
| 600 | Tallinfilm Instrument Kit (V1.2) | — | polyphone | 公有领域 | ✓ | — | 169 | piano |
| 601 | pspkvm soundfont | — | polyphone | 公有领域 | ✓ | — | 153 | piano |
| 602 | Nord White Grand | — | polyphone | 公有领域 | ✓ | — | 147 | piano |
| 603 | Nord Rhodes | — | polyphone | 公有领域 | ✓ | — | 138 | piano |
| 604 | Gaia Piano Not | — | polyphone | 公有领域 | ✓ | — | 132 | piano |
| 605 | Baby Einstein - Korg X5-X5D-X5DR Soundfont (PCM-PCM98) | — | polyphone | 公有领域 | ✓ | — | 125 | piano |
| 606 | Baldwin Studio Upright | — | polyphone | 公有领域 | ✓ | — | 124 | piano |
| 607 | Electric Piano 26 | — | polyphone | 公有领域 | ✓ | — | 112 | piano |
| 608 | Peggle Soundfont | — | polyphone | 公有领域 | ✓ | — | 89 | piano |
| 609 | Scratch - All Drums and All Instruments Soundfont - 8-Bit Soundfont (S | — | polyphone | 公有领域 | ✓ | — | 87 | piano |
| 610 | Nord Italian Grand | — | polyphone | 公有领域 | ✓ | — | 84 | piano |
| 611 | Super Mario 3D World Soundfont - SM3DW (2019 - 2026 - Present) | — | polyphone | 公有领域 | ✓ | — | 84 | piano |
| 612 | Super Mario Maker Music Box And Online Sequencer - Synthesizer (Soundf | — | polyphone | 公有领域 | ✓ | — | 82 | piano |
| 613 | Baby Einstein - GM Music Box and ILIO Celesta | — | polyphone | 公有领域 | ✓ | — | 79 | piano |
| 614 | Bubble&#039;s Hotel Soundfont - Piano | — | polyphone | 公有领域 | ✓ | — | 75 | piano |
| 615 | Marimba and Timpani Instrument - Super Mario Maker and Bee Swarm Simul | — | polyphone | 公有领域 | ✓ | — | 73 | piano |
| 616 | Scratch - Bass - NES 8-Bit Soundfont - Super Mario World (Soundfont SF | — | polyphone | 公有领域 | ✓ | — | 61 | piano |
| 617 | Upright Piano | — | polyphone | 公有领域 | ✓ | — | 54 | piano |
| 618 | Baby Einstein Soundfonts - GM Harp - Harp - Oboe | — | polyphone | 公有领域 | ✓ | — | 37 | piano |
| 619 | Tallinfilm Instrument Kit (V1.0) | — | polyphone | 公有领域 | ✓ | — | 37 | piano |
| 620 | Super Mario Maker - Harp And Accordion (Note Block Instrument Soundfon | — | polyphone | 公有领域 | ✓ | — | 24 | piano |
| 621 | Uma Rapariga E BUOM TUM TUM | — | polyphone | 公有领域 | — | — | 24 | piano |
| 622 | Super Mario Maker Organ And Drums Online Sequencer (SF2, Soundfont) | — | polyphone | 公有领域 | ✓ | — | 18 | piano |
| 623 | Sbgshsvs | — | polyphone | 公有领域 | — | — | 10 | piano |
| 624 | Scarypiano | Karoryfer Samples | sfzinstruments | CC0 | — | — | — | piano |
| 625 | square wave soundfont | — | polyphone | 公有领域 | ✓ | — | 826 | sfx |
| 626 | Thurston Waffles Meow Soundfont | Anapan | musical-artifacts | 公有领域（站点标注） | ✓ | — | 653 | sfx |
| 627 | Various sound effects | Fox-Gieg | polyphone | 公有领域 | ✓ | — | 633 | sfx |
| 628 | Nord Pad Worship 4 | — | polyphone | 公有领域 | ✓ | — | 612 | sfx |
| 629 | Silly synths ROM | ? | polyphone | 公有领域 | ✓ | — | 374 | sfx |
| 630 | Telephone Call Tone | — | polyphone | 公有领域 | ✓ | — | 221 | sfx |
| 631 | tesla coil | — | polyphone | 公有领域 | ✓ | — | 219 | sfx |
| 632 | Undertale - Mettaton&#039;s Dialogue | — | polyphone | 公有领域 | ✓ | — | 158 | sfx |
| 633 | Booms! FX | — | polyphone | 公有领域 | ✓ | — | 153 | sfx |
| 634 | Stupid soundfont | — | polyphone | 公有领域 | ✓ | — | 137 | sfx |
| 635 | glug | — | polyphone | 公有领域 | ✓ | — | 136 | sfx |
| 636 | Bone Crack | — | polyphone | 公有领域 | ✓ | — | 101 | sfx |
| 637 | ShyntSonar | — | polyphone | 公有领域 | ✓ | — | 97 | sfx |
| 638 | Cog soundfont | — | polyphone | 公有领域 | — | — | 95 | sfx |
| 639 | Jail Cell Door | — | polyphone | 公有领域 | — | — | 57 | sfx |
| 640 | Random stuff | — | polyphone | 公有领域 | ✓ | — | 56 | sfx |
| 641 | Toilet | — | polyphone | 公有领域 | ✓ | — | 43 | sfx |
| 642 | South Park Credit and Intro (Plus Pilot) Samples | — | polyphone | 公有领域 | — | — | 42 | sfx |
| 643 | Yooooooooooo | — | polyphone | 公有领域 | ✓ | — | 41 | sfx |
| 644 | bebe kids snes | — | polyphone | 公有领域 | ✓ | — | 29 | sfx |
| 645 | Synth Bass #2 | FreePats project | FreePats | CC0 | ✓ | 1.7 MB | — | synth |
| 646 | Lately Bass | FreePats project | FreePats | CC0 | ✓ | 2.0 MB | — | synth |
| 647 | Synth Bass #1 | FreePats project | FreePats | CC0 | ✓ | 3.2 MB | — | synth |
| 648 | Synth Brass #2 | FreePats project | FreePats | CC0 | ✓ | 3.4 MB | — | synth |
| 649 | Synth Strings #1 | FreePats project | FreePats | CC0 | ✓ | 4.2 MB | — | synth |
| 650 | Synth Crystal | FreePats project | FreePats | CC0 | ✓ | 4.4 MB | — | synth |
| 651 | Synth Brass #1 | FreePats project | FreePats | CC0 | ✓ | 5.2 MB | — | synth |
| 652 | Synth Bass & Lead | FreePats project | FreePats | CC0 | ✓ | 6.1 MB | — | synth |
| 653 | Sweep Pad | FreePats project | FreePats | CC0 | ✓ | 7.2 MB | — | synth |
| 654 | New Age | FreePats project | FreePats | CC0 | ✓ | 7.4 MB | — | synth |
| 655 | Synth Strings #2 | FreePats project | FreePats | CC0 | ✓ | 7.4 MB | — | synth |
| 656 | Synth Lead Calliope | FreePats project | FreePats | CC0 | ✓ | 7.5 MB | — | synth |
| 657 | Synth Lead Square | FreePats project | FreePats | CC0 | ✓ | 9.0 MB | — | synth |
| 658 | Synth Fifths | FreePats project | FreePats | CC0 | ✓ | 12.0 MB | — | synth |
| 659 | Synth Pad Choir | FreePats project | FreePats | CC0 | ✓ | 12.0 MB | — | synth |
| 660 | Synth Soundtrack | FreePats project | FreePats | CC0 | ✓ | 17.0 MB | — | synth |
| 661 | Synth Goblins | FreePats project | FreePats | CC0 | ✓ | 19.0 MB | — | synth |
| 662 | Synth Pad Bowed | FreePats project | FreePats | CC0 | ✓ | 21.0 MB | — | synth |
| 663 | Synth Sci-Fi | FreePats project | FreePats | CC0 | ✓ | 22.0 MB | — | synth |
| 664 | Wavestate Pads | SHLD Music | sfzinstruments | CC0 | — | 160.0 MB | — | synth |
| 665 | Minifreak Pads | SHLD Music | sfzinstruments | CC0 | — | 265.0 MB | — | synth |
| 666 | 20 synths | Stephen Rich | musical-artifacts | 公有领域（站点标注） | ✓ | — | 12337 | synth |
| 667 | Pleasure! (Beta 2) | Yingchun Soul (Elf of Happy an | musical-artifacts | 公有领域（站点标注） | ✓ | — | 8623 | synth |
| 668 | Waveblade house bass | — | polyphone | 公有领域 | — | — | 8266 | synth |
| 669 | Massive Pad 1 | Strix SoundFont Team | musical-artifacts | 公有领域（站点标注） | ✓ | — | 5583 | synth |
| 670 | Saw 8-Detune | Strix Soundfont Team | musical-artifacts | 公有领域（站点标注） | ✓ | — | 4609 | synth |
| 671 | synthetic soundfont 1.0 | Piotr Grochowski | musical-artifacts | 公有领域（站点标注） | ✓ | — | 2484 | synth |
| 672 | Yousuke Yasui Guitar And Drums +Tek Drums SoundFont | VentusArranger | musical-artifacts | 公有领域（站点标注） | ✓ | — | 2430 | synth |
| 673 | Various Synths | Fox-Gieg / DJ O.J.C. | polyphone | 公有领域 | ✓ | — | 2032 | synth |
| 674 | Bread Bread&#039;s Distortion Guitar (v2.1) | — | polyphone | 公有领域 | ✓ | — | 1659 | synth |
| 675 | synthetic soundfont 2.0 | Piotr Grochowski | musical-artifacts | 公有领域（站点标注） | ✓ | — | 1342 | synth |
| 676 | Pipe Organ Samples | — | polyphone | 公有领域 | ✓ | — | 1268 | synth |
| 677 | Clean Stratocaster | — | polyphone | 公有领域 | ✓ | — | 1229 | synth |
| 678 | Yooreek | — | polyphone | 公有领域 | ✓ | — | 1197 | synth |
| 679 | ULTRAKILL Breakbeats | — | polyphone | 公有领域 | ✓ | — | 1047 | synth |
| 680 | MOTHER 3 | — | polyphone | 公有领域 | ✓ | — | 1002 | synth |
| 681 | Meowsynth | — | polyphone | 公有领域 | ✓ | — | 816 | synth |
| 682 | Casio PT-10 | — | polyphone | 公有领域 | ✓ | — | 672 | synth |
| 683 | Otamatone | — | polyphone | 公有领域 | ✓ | — | 564 | synth |
| 684 | 8 Bit Sounds | — | polyphone | 公有领域 | ✓ | — | 555 | synth |
| 685 | Booker T | — | polyphone | 公有领域 | ✓ | — | 552 | synth |
| 686 | ModSynth | — | polyphone | 公有领域 | ✓ | — | 446 | synth |
| 687 | Super Nintendo Entertainment System Soundfont! | — | polyphone | 公有领域 | ✓ | — | 412 | synth |
| 688 | Sawtooth Piano | — | polyphone | 公有领域 | ✓ | — | 403 | synth |
| 689 | CMX 2.0 Soundbank | — | polyphone | 公有领域 | ✓ | — | 401 | synth |
| 690 | Casio HT700 | — | polyphone | 公有领域 | ✓ | — | 368 | synth |
| 691 | Black Knife Lead | — | polyphone | 公有领域 | ✓ | — | 359 | synth |
| 692 | Pokemon Black and White 2 Soundfont Updated | — | polyphone | 公有领域 | — | — | 343 | synth |
| 693 | m7Synth | — | polyphone | 公有领域 | ✓ | — | 301 | synth |
| 694 | WaveBlade SF2 | — | polyphone | 公有领域 | ✓ | — | 277 | synth |
| 695 | LG T375 soundfont | — | polyphone | 公有领域 | ✓ | — | 262 | synth |
| 696 | Sinewaves everywhere (except drumkit) | — | polyphone | 公有领域 | ✓ | — | 252 | synth |
| 697 | Za Easy Donk Bass | — | polyphone | 公有领域 | — | — | 251 | synth |
| 698 | Full Candy Set GM | — | polyphone | 公有领域 | ✓ | — | 243 | synth |
| 699 | <- /Discord Discord Revolution Soundfont/ -> | Melodii (AKA. MelodiiMilmshake | musical-artifacts | WTFPL（等同公有领域） | ✓ | — | 202 | synth |
| 700 | synthetic soundfont 2.0 | — | polyphone | 公有领域 | ✓ | — | 175 | synth |
| 701 | PaRappa The Rapper + UmJammer Lammy Sound Effects | — | polyphone | 公有领域 | ✓ | — | 151 | synth |
| 702 | Wasteland Kit | — | polyphone | 公有领域 | ✓ | — | 151 | synth |
| 703 | DutyCycleUTsf2 | — | polyphone | 公有领域 | ✓ | — | 139 | synth |
| 704 | 5C34M!! | — | polyphone | 公有领域 | ✓ | — | 138 | synth |
| 705 | Warm lead | — | polyphone | 公有领域 | ✓ | — | 131 | synth |
| 706 | Tranzo | — | polyphone | 公有领域 | ✓ | — | 126 | synth |
| 707 | Orchestral  Full | — | polyphone | 公有领域 | ✓ | — | 125 | synth |
| 708 | that specific sound when you dont connect the speakers too well | — | polyphone | 公有领域 | ✓ | — | 110 | synth |
| 709 | Clarinet FM | — | polyphone | 公有领域 | ✓ | — | 83 | synth |
| 710 | NiGHTS Into Dreams... Soundfont | — | polyphone | 公有领域 | ✓ | — | 66 | synth |
| 711 | Rubber band | — | polyphone | 公有领域 | ✓ | — | 59 | synth |
| 712 | ASKT Soundfont | — | polyphone | 公有领域 | ✓ | — | 50 | synth |
| 713 | Clarinet Synth | — | polyphone | 公有领域 | ✓ | — | 49 | synth |
| 714 | Small Soundfont | — | polyphone | 公有领域 | ✓ | — | 42 | synth |
| 715 | Playtender GBA Soundfont | — | polyphone | 公有领域 | ✓ | — | 34 | synth |
| 716 | aladdin snes | — | polyphone | 公有领域 | ✓ | — | 21 | synth |
| 717 | Lester the Unlikely (SNES) Soundfont | — | polyphone | 公有领域 | ✓ | — | 20 | synth |
| 718 | TopHatFont | — | polyphone | 公有领域 | ✓ | — | 18 | synth |
| 719 | Ultra Small SF but cover all 128 GM insts.!!! | — | polyphone | 公有领域 | ✓ | — | 18 | synth |
| 720 | TAZ MANIA SNES | — | polyphone | 公有领域 | ✓ | — | 15 | synth |
| 721 | CMX 1.1 (Unfinished) | — | polyphone | 公有领域 | ✓ | — | 10 | synth |
| 722 | dirtyyy | — | polyphone | 公有领域 | ✓ | — | 6 | synth |
| 723 | Caveman Cosmonaut | Karoryfer Samples | sfzinstruments | CC0 | — | — | — | synth |
| 724 | Cowsynth | Karoryfer Samples | sfzinstruments | CC0 | — | — | — | synth |
| 725 | Witch's Strat | Witch's Cadence | musical-artifacts | 公有领域（站点标注） | ✓ | — | 0 | synth |
| 726 | Acapella GM/GS for AWE32 and DLS | Juicestain | musical-artifacts | WTFPL（等同公有领域） | — | 80.5 MB | 2721 | vocal |
| 727 | Florestan Ahh Choir | Nando Florestan | musical-artifacts | 公有领域（站点标注） | ✓ | — | 16429 | vocal |
| 728 | KBH Real choir | ? | polyphone | 公有领域 | ✓ | — | 1693 | vocal |
| 729 | Various Vocals | Fox-Gieg | polyphone | 公有领域 | ✓ | — | 1272 | vocal |
| 730 | Papelmedia Vocals solo | — | polyphone | 公有领域 | ✓ | — | 785 | vocal |
| 731 | Choir Choral Aahhs | ? | polyphone | 公有领域 | ✓ | — | 778 | vocal |
| 732 | Choir bass | ? | polyphone | 公有领域 | ✓ | — | 747 | vocal |
| 733 | goofy ahh sounds | — | polyphone | 公有领域 | ✓ | — | 726 | vocal |
| 734 | ChorMaleFem | — | polyphone | 公有领域 | ✓ | — | 636 | vocal |
| 735 | 052 Florestan Ahh Choir | Nando Florestan | polyphone | 公有领域 | ✓ | — | 537 | vocal |
| 736 | Female-Vocalizer | — | polyphone | 公有领域 | ✓ | — | 427 | vocal |
| 737 | VoiceNoise | — | polyphone | 公有领域 | ✓ | — | 208 | vocal |
| 738 | Vocal Voice 26 | — | polyphone | 公有领域 | ✓ | — | 197 | vocal |
| 739 | 272 Merry Orks | Karoryfer Samples | sfzinstruments | CC0 | — | — | — | vocal |
| 740 | Angelic Clarinet Soundfont | Archangel | musical-artifacts | 公有领域（站点标注） | ✓ | — | 4760 | wind |
| 741 | Florestan Harmonica | Nando Florestan | musical-artifacts | 公有领域（站点标注） | ✓ | — | 4596 | wind |

## 五、F2 · 署名后可分发（CC BY / MIT / BSD / ISC） · 全量 1691 条

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
| 13 | Drum by KEN ARDENCY v2.1 | Ken Ardency | polyphone | CC BY | ✓ | — | 2101 | drum |
| 14 | 5b Drums | YoylePlant | musical-artifacts | CC BY 3.0 | ✓ | — | 2040 | drum |
| 15 | Glockenspiel | Ethan Winer | polyphone | CC BY | ✓ | — | 1005 | drum |
| 16 | Tubular Bells | Sonido media | polyphone | CC BY | ✓ | — | 922 | drum |
| 17 | Roland Orchestral Rhythm | Roland | polyphone | CC BY | ✓ | — | 895 | drum |
| 18 | Talking Tom 2 Drum Soundfont | Mildanner, Outfit7 | musical-artifacts | CC BY 3.0 | ✓ | — | 853 | drum |
| 19 | FlashThemes Outro Drum Soundfont | Mildanner, FlashThemes | musical-artifacts | CC BY 3.0 | ✓ | — | 834 | drum |
| 20 | Electro Drumkit | — | polyphone | CC BY | ✓ | — | 777 | drum |
| 21 | Japanese Taiko (Kumidaiko) Soundfont V1 | — | polyphone | CC BY | ✓ | — | 717 | drum |
| 22 | Wind chimes | Ethan Winer | polyphone | CC BY | ✓ | — | 646 | drum |
| 23 | Sleigh Bells | Ethan Winer | polyphone | CC BY | ✓ | — | 609 | drum |
| 24 | Tambourine | Ethan Winer | polyphone | CC BY | ✓ | — | 602 | drum |
| 25 | Westgate Studios - All percussion | Westgate Studios | polyphone | CC BY | — | — | 594 | drum |
| 26 | HS Acoustic Percussion | Thomas Hammer | polyphone | CC BY | ✓ | — | 514 | drum |
| 27 | Acoustic Kit M.B. | — | polyphone | CC BY | ✓ | — | 498 | drum |
| 28 | Douglas&#039; Concert Timpani | Douglas Whates | polyphone | CC BY | ✓ | — | 493 | drum |
| 29 | Dance kit 4 | Marco Peretti | polyphone | CC BY | ✓ | — | 455 | drum |
| 30 | Basic percussion | Project SAM | polyphone | CC BY | — | — | 451 | drum |
| 31 | Triangle | Ethan Winer | polyphone | CC BY | ✓ | — | 410 | drum |
| 32 | Shakers | Ethan Winer | polyphone | CC BY | ✓ | — | 391 | drum |
| 33 | Chuck&#039;s tubulars | Ethan Winer | polyphone | CC BY | ✓ | — | 367 | drum |
| 34 | Timpani | Project SAM | polyphone | CC BY | — | — | 360 | drum |
| 35 | Temple blocks | Ethan Winer | polyphone | CC BY | ✓ | — | 351 | drum |
| 36 | African slit drum | Ethan Winer | polyphone | CC BY | ✓ | — | 310 | drum |
| 37 | Sonic Implants Timbales A-F | Sonic Implants | polyphone | CC BY | ✓ | — | 309 | drum |
| 38 | Snare Brushed - Hits and Rolls | Ethan Winer | polyphone | CC BY | ✓ | — | 301 | drum |
| 39 | Bombo Leguero | — | polyphone | CC BY | ✓ | — | 278 | drum |
| 40 | Claves | Ethan Winer | polyphone | CC BY | ✓ | — | 265 | drum |
| 41 | MEEBKIN | — | polyphone | CC BY | ✓ | — | 247 | drum |
| 42 | Sonic Implants Afoxe A-F | Sonic Implants | polyphone | CC BY | ✓ | — | 218 | drum |
| 43 | Pearl Concert Snare - Full | — | polyphone | CC BY | ✓ | — | 214 | drum |
| 44 | Turtle drum | Ethan Winer | polyphone | CC BY | ✓ | — | 207 | drum |
| 45 | VGS Industrial Drums | — | polyphone | CC BY | ✓ | — | 168 | drum |
| 46 | Kendang Dangdut | — | polyphone | CC BY | ✓ | — | 161 | drum |
| 47 | Solar Studios&#039; Agogo | — | polyphone | CC BY | ✓ | — | 155 | drum |
| 48 | Damon&#039;s Kick&#039;n&#039;Snare Industrial Kit | — | polyphone | CC BY | ✓ | — | 150 | drum |
| 49 | BottlePerc | — | polyphone | CC BY | — | — | 140 | drum |
| 50 | Solar Studios&#039; Birch Melodic Tom | — | polyphone | CC BY | ✓ | — | 126 | drum |
| 51 | Batería con muestras | — | polyphone | CC BY | ✓ | — | 63 | drum |
| 52 | TIMPANI | — | polyphone | CC BY | ✓ | — | 63 | drum |
| 53 | TAITO Violence Fight Drumkit and SFX | — | polyphone | CC BY | ✓ | — | 17 | drum |
| 54 | Final Fight Arcade Drumkit | — | polyphone | CC BY | ✓ | — | 13 | drum |
| 55 | Breezy Day | Malaclypse the Younger | sfzinstruments | MIT | — | — | — | drum |
| 56 | Celesta_minimal | alnitak | github | MIT | — | — | — | drum |
| 57 | RatAttack | alnitak | github | MIT | ✓ | — | — | drum |
| 58 | SFX_StarWars_weapons | alnitak | github | MIT | ✓ | — | — | drum |
| 59 | SteelDrums | sinshu | github | MIT | — | — | — | drum |
| 60 | SynthDrum | sinshu | github | MIT | — | — | — | drum |
| 61 | TerribleDanger | alnitak | github | MIT | ✓ | — | — | drum |
| 62 | The Clap | Malaclypse the Younger | sfzinstruments | MIT | — | — | — | drum |
| 63 | Ancient Instruments Of The World | — | polyphone | CC BY | ✓ | — | 3479 | ethnic |
| 64 | Multi Kalimba | A1219 | musical-artifacts | CC BY | ✓ | — | 2876 | ethnic |
| 65 | Metal Pipe Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 1141 | ethnic |
| 66 | World percussion | Project SAM | polyphone | CC BY | — | — | 472 | ethnic |
| 67 | Africa 1 | Joe Ortiz | polyphone | CC BY | ✓ | — | 390 | ethnic |
| 68 | Woodblocks | Andreas Sumerauer | polyphone | CC BY | ✓ | — | 350 | ethnic |
| 69 | Krumhorn Alt | ? | polyphone | CC BY | ✓ | — | 314 | ethnic |
| 70 | Rindik | — | polyphone | CC BY | ✓ | — | 277 | ethnic |
| 71 | Bagpipe | sinshu | github | MIT | — | — | — | ethnic |
| 72 | Banjo | sinshu | github | MIT | — | — | — | ethnic |
| 73 | Kalimba | sinshu | github | MIT | — | — | — | ethnic |
| 74 | Koto | sinshu | github | MIT | — | — | — | ethnic |
| 75 | Shakuhachi | sinshu | github | MIT | — | — | — | ethnic |
| 76 | Shamisen | sinshu | github | MIT | — | — | — | ethnic |
| 77 | Sitar | sinshu | github | MIT | — | — | — | ethnic |
| 78 | GBFont Soundfont | MaliceX | musical-artifacts | CC BY | ✓ | 0.1 MB | 15694 | game |
| 79 | GXSCC GM v0.33 SoundFont | Zandro Reveille | musical-artifacts | CC BY | ✓ | 0.1 MB | 5884 | game |
| 80 | Toy Story Genesis PCM Mod RAW Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | — | 0.3 MB | 398 | game |
| 81 | Dangerous Seed TFI Instrument Pack | Mildanner | musical-artifacts | CC BY 3.0 | — | 0.7 MB | 172 | game |
| 82 | YM2612 FM Piano (Instrument Patch + Soundfont) | Mildanner | musical-artifacts | CC BY 3.0 | — | 0.9 MB | 796 | game |
| 83 | Sonic The Hedgehog Genesis (GBA) Samples and Midis | Jackstarreal_yt | musical-artifacts | CC BY 3.0 | — | 1.3 MB | 2288 | game |
| 84 | Super Putty (SNES) Soundfont and WAV Samples | Darko747 | musical-artifacts | CC BY 3.0 | ✓ | 1.5 MB | 1986 | game |
| 85 | Fullmetal Alchemist: Sonata of Memories Soundfont (UPDATE 4/28/2026) | VideoGameKid | musical-artifacts | CC BY 3.0 | ✓ | 1.5 MB | 788 | game |
| 86 | Winds Of Fjords (Better Samples) Soundfont [2.5.1] | Motionwave (MW) | musical-artifacts | CC BY | ✓ | 3.0 MB | 14460 | game |
| 87 | 3DS Soundfont + MIDI Collection | Stupid (Local WarioWare Enjoye | musical-artifacts | CC BY 3.0 | ✓ | 7.6 MB | 951 | game |
| 88 | Sonic Advance MIDI + Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | — | 8.7 MB | 6381 | game |
| 89 | Pac-in-Time Soundfont (outdated) | Frédéric Motte | musical-artifacts | CC BY 3.0 | ✓ | 9.8 MB | 1677 | game |
| 90 | Code Geass: Lelouch of the Rebellion R2 - Geass Theatric Boardgame Sou | VideoGameKid | musical-artifacts | CC BY 3.0 | — | 13.8 MB | 492 | game |
| 91 | MediaTek Soundfont GM (Wasteyarded) | XXtherobloxx21, MediaTek | musical-artifacts | CC BY | — | 17.6 MB | 782 | game |
| 92 | Guilty Gear Dust Strikers Soundfont (UPDATE 5/23/2026) | VideoGameKid (Originally rippe | musical-artifacts | CC BY 3.0 | ✓ | 18.2 MB | 1283 | game |
| 93 | Bleach DS 4th: Flame Bringer Soundfont (UPDATE 5/29/26) | VideoGameKid | musical-artifacts | CC BY 3.0 | ✓ | 19.1 MB | 1045 | game |
| 94 | Code Geass: Lelouch of the Rebellion DS Soundfont (UPDATE 5/26/2026) | VideoGameKid | musical-artifacts | CC BY 3.0 | ✓ | 24.7 MB | 895 | game |
| 95 | (Android) MIDI Player Synth Stock | Mildanner | musical-artifacts | CC BY 3.0 | — | 27.1 MB | 1185 | game |
| 96 | Super Mario 64 DS (MIDI + Soundfont) | Mildanner | musical-artifacts | CC BY 3.0 | — | 51.0 MB | 5769 | game |
| 97 | New Super Mario Bros. DS - MIDI and Soundfont | Mildanner, Nintendo | musical-artifacts | CC BY 3.0 | — | 74.1 MB | 4308 | game |
| 98 | Metal Slug 7 MIDI + Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | — | 95.4 MB | 864 | game |
| 99 | Touhou Soundfont | Team Shanghai Alice (game), un | musical-artifacts | CC BY | ✓ | — | 385457 | game |
| 100 | Nintendo Soundfont | hakerg | musical-artifacts | CC BY | ✓ | — | 53270 | game |
| 101 | Casio CTK-230 SoundFont | Dekyo Ongen | musical-artifacts | CC BY | ✓ | — | 28588 | game |
| 102 | Minecraft Note Block Studio 3.3.4 Soundfont | Stuff by David | musical-artifacts | CC BY | ✓ | — | 27112 | game |
| 103 | Yamaha RX7 | Reza Chaniago Hartono W. Walan | musical-artifacts | CC BY | ✓ | — | 17583 | game |
| 104 | SampleSynthesis (an attempt to emulate/recreate toy keyboards and lo-f | Dekyo Ongen | musical-artifacts | CC BY | ✓ | — | 17045 | game |
| 105 | ExpressiveSNES - General MIDI Super Nintendo Soundfont | DitherEmotion | musical-artifacts | CC BY 3.0 | ✓ | — | 12575 | game |
| 106 | YM2612 Guitar & Bass Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 12546 | game |
| 107 | Super Mario Bros Soundfont | Kirb7890 (Nintendo) | musical-artifacts | CC BY 3.0 | ✓ | — | 12205 | game |
| 108 | Korg Triton Instrument Pack Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 10876 | game |
| 109 | Drawn to Life: The Next Chapter (DS) Soundfont | 48 LAC | musical-artifacts | CC BY 3.0 | ✓ | — | 10177 | game |
| 110 | Super Mario World Soundfont v1.3 (2025) | Jechucam | musical-artifacts | CC BY 3.0 | ✓ | — | 9883 | game |
| 111 | Sega Genesis (ym2612) electric guitars soundfont | Iskalim | musical-artifacts | CC BY 3.0 | ✓ | — | 9482 | game |
| 112 | Studio Pixel Drums Soundfont | me :) | musical-artifacts | CC BY | ✓ | — | 9404 | game |
| 113 | Sonic 3D Blast Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 9223 | game |
| 114 | SONiVOX EAS GM Wavetable Ver. 1.83 | Sonic Network Inc. | musical-artifacts | CC BY 3.0 | ✓ | — | 8733 | game |
| 115 | DOOM (SNES) Soundfont | Zackie | musical-artifacts | CC BY | ✓ | — | 8326 | game |
| 116 | 90 Minutes European Prime Goal 3 Instrument set Soundfont | — | polyphone | CC BY | ✓ | — | 7989 | game |
| 117 | A tiny ~128ish sample 11khz Mobile Ice Cream Truck TI SN7 filtered PSG | stgiga, [nowanonymous], Zmey K | musical-artifacts | CC BY 3.0 | ✓ | — | 7658 | game |
| 118 | SONiVOX EAS GM Wavetable Ver. 1.92 | Sonic Network Inc. | musical-artifacts | CC BY 3.0 | ✓ | — | 7574 | game |
| 119 | aobu's chiptune soundfont v0.03 | aobunau | musical-artifacts | CC BY | ✓ | — | 6855 | game |
| 120 | Eevee Soundfont (2.5) | Renderite | musical-artifacts | CC BY 3.0 | ✓ | — | 6850 | game |
| 121 | SONiVOX EAS GM Wavetable Ver. 2.10 | Sonic Network Inc. | musical-artifacts | CC BY 3.0 | ✓ | — | 6453 | game |
| 122 | FPD 2.6 "PCMV2" | Dekyo Ongen | musical-artifacts | CC BY | ✓ | — | 6398 | game |
| 123 | Atari 2600 GM Bank | stgiga, little-scale, drunkenj | musical-artifacts | CC BY 3.0 | ✓ | — | 6095 | game |
| 124 | SONiVOX EAS GM Wavetable Ver. 2.00 | Sonic Network Inc. | musical-artifacts | CC BY 3.0 | ✓ | — | 5755 | game |
| 125 | Drawn to Life (DS) Soundfont | 48 LAC | musical-artifacts | CC BY 3.0 | ✓ | — | 5550 | game |
| 126 | The Smurfs (SNES) Soundfont | 48 LAC | musical-artifacts | CC BY 3.0 | ✓ | — | 5427 | game |
| 127 | Old School RuneScape (OSRS) Soundfont [GM] | Feem | musical-artifacts | CC BY 3.0 | ✓ | — | 5417 | game |
| 128 | Jam with the Band P. Soundfont (GM compatible) | TKMT_Aniki & RolandKnight | musical-artifacts | CC BY 3.0 | ✓ | — | 4938 | game |
| 129 | StarEevee SoundFont | Renderite | musical-artifacts | CC BY 3.0 | ✓ | — | 4854 | game |
| 130 | FM tone nº 101 from EFFEC.FF | Dekyo Ongen | musical-artifacts | CC BY | ✓ | — | 4761 | game |
| 131 | Mickey's Speedway USA derekSiZZLE's Soundfont (Fixed) | derekSiZZLE (Fixed Broken Loop | musical-artifacts | CC BY 3.0 | ✓ | — | 4648 | game |
| 132 | SONiVOX EAS GM Wavetable Ver. 1.91A | Sonic Network Inc. | musical-artifacts | CC BY 3.0 | ✓ | — | 4625 | game |
| 133 | Nesfont advance | Cat333pokemon, et al | musical-artifacts | CC BY 3.0 | ✓ | — | 4416 | game |
| 134 | Xadra's Legend of Zelda soundfont | Xadra | musical-artifacts | CC BY 3.0 | ✓ | — | 4319 | game |
| 135 | Club Penguin: Elite Penguin Force SoundFonts | tha SuuS | musical-artifacts | CC BY 3.0 | ✓ | — | 4318 | game |
| 136 | Sega Genesis Custom Drum Kit Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 4093 | game |
| 137 | SONiVOX EAS GM Wavetable Ver. 1.90 | Sonic Network Inc. | musical-artifacts | CC BY 3.0 | ✓ | — | 4088 | game |
| 138 | Micro Machines 2 (SNES) Soundfont | 48 LAC | musical-artifacts | CC BY 3.0 | ✓ | — | 4027 | game |
| 139 | Dr. Robotnik Mean Bean Machine Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 3885 | game |
| 140 | Marko's Magic Football (SNES) Soundfont | 48 LAC | musical-artifacts | CC BY 3.0 | ✓ | — | 3776 | game |
| 141 | SONiVOX EAS GM Wavetable Ver. 1.91 | Sonic Network Inc. | musical-artifacts | CC BY 3.0 | ✓ | — | 3718 | game |
| 142 | Dead Body Reported Soundfont | NH1507 | musical-artifacts | CC BY 3.0 | ✓ | — | 3710 | game |
| 143 | SONiVOX EAS GM Wavetable Ver. 1.81 | Sonic Network Inc. | musical-artifacts | CC BY 3.0 | ✓ | — | 3672 | game |
| 144 | SONiVOX EAS GM Wavetable Ver. 1.80 | Sonic Network Inc. | musical-artifacts | CC BY 3.0 | ✓ | — | 3496 | game |
| 145 | SonicMT.bin - Drum Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 3449 | game |
| 146 | GBA MegaMan Battle Network Soundfont Pack (1-6, 4.5, & BCC) | Nintenducc | musical-artifacts | CC BY 3.0 | ✓ | — | 3356 | game |
| 147 | The Kirby's Dream Land Soundfont! (V1.1) (OLD) | ArtifactedSonicMusical | musical-artifacts | CC BY 3.0 | ✓ | — | 3338 | game |
| 148 | Brandish 2 Soundfont | Carter Venom | musical-artifacts | CC BY 3.0 | ✓ | — | 3291 | game |
| 149 | Sonic the Hedgehog Genesis (GBA) Soundfont | Mildanner, SEGA Sonic Team | musical-artifacts | CC BY 3.0 | ✓ | — | 3217 | game |
| 150 | SONiVOX EAS GM Wavetable Ver. 1.82 | Sonic Network Inc. | musical-artifacts | CC BY 3.0 | ✓ | — | 3151 | game |
| 151 | TR-626 Drum Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 3118 | game |
| 152 | 02. St. Piano 2 Remastered | 白いチャンネル | musical-artifacts | CC BY 3.0 | ✓ | — | 3050 | game |
| 153 | MegaMan Battle Chip Challenge Soundfont | Nintenducc | musical-artifacts | CC BY 3.0 | ✓ | — | 3048 | game |
| 154 | Mario Party 2 Soundfont | tahutoa | musical-artifacts | CC BY 3.0 | ✓ | — | 3027 | game |
| 155 | Pac-in-Time Soundfont (Update) | NAMCO | musical-artifacts | CC BY 3.0 | ✓ | — | 3015 | game |
| 156 | Banjo-Tooie Soundfont | rareware | musical-artifacts | CC BY 3.0 | ✓ | — | 2918 | game |
| 157 | Sonic Crackers Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 2794 | game |
| 158 | Gimmick Sunsoft Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 2748 | game |
| 159 | Sonic 3 Clean Drum Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 2723 | game |
| 160 | Sonic Pocket Adventure Soundfont (Redux) | Mildanner, SEGA Sonic Team | musical-artifacts | CC BY 3.0 | ✓ | — | 2713 | game |
| 161 | Mischief Makers soundfont | HandlebarOrionX | musical-artifacts | CC BY 3.0 | ✓ | — | 2703 | game |
| 162 | Analog toy effects | Milton paredes, mpj factoy stu | musical-artifacts | CC BY | ✓ | — | 2675 | game |
| 163 | YM2612 Piano Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 2535 | game |
| 164 | Sega Master System Game Gear Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 2521 | game |
| 165 | Distraction Dance Soundfont | NH1507 | musical-artifacts | CC BY 3.0 | ✓ | — | 2477 | game |
| 166 | Sonic 3 Drum Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 2453 | game |
| 167 | SaGa 2 (NDS) Soundfont + Midis | Dusk | musical-artifacts | CC BY 3.0 | — | — | 2408 | game |
| 168 | Pokémon FireRed and LeafGreen Soundfont (VGM & Pokémon Sound Sources C | VideoGameKid | musical-artifacts | CC BY 3.0 | ✓ | — | 2372 | game |
| 169 | Gameboy Furnace Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 2368 | game |
| 170 | Sonic 1 South Island Expedition Drum Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 2300 | game |
| 171 | Kick Square Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 2253 | game |
| 172 | Remix 10 Bass Soundfont | Mildanner, Rhythm Heaven Fever | musical-artifacts | CC BY 3.0 | ✓ | — | 2242 | game |
| 173 | Sonic 1 Mixed Drum Soundfont | Mildanner, Hame | musical-artifacts | CC BY 3.0 | ✓ | — | 2204 | game |
| 174 | Segapede (Prototype) Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 2201 | game |
| 175 | Power Piggs of the Dark Age (SNES) Soundfont | 48 LAC | musical-artifacts | CC BY 3.0 | ✓ | — | 2195 | game |
| 176 | PSP Soundfont | XXtherobloxx21 (Fixed drums),  | musical-artifacts | CC BY 3.0 | ✓ | — | 2182 | game |
| 177 | Plants Vs. Zombies Soundfont (Improved) | VladTheFatman | musical-artifacts | CC BY 3.0 | ✓ | — | 2093 | game |
| 178 | Sonic the Hedgehog Soundfont (1/2/3K) | — | polyphone | CC BY | — | — | 2080 | game |
| 179 | Old Towers Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 2070 | game |
| 180 | Sonic Eraser Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 2019 | game |
| 181 | WWF No Mercy soundfont | HandlebarOrionX | musical-artifacts | CC BY 3.0 | ✓ | — | 1964 | game |
| 182 | Minecraft Soundfont (Improved) | UWFanaticSF2 | musical-artifacts | CC BY 3.0 | ✓ | — | 1936 | game |
| 183 | Wario Master Of Disguise Soundfont | HopefulSpread | musical-artifacts | CC BY 3.0 | ✓ | — | 1869 | game |
| 184 | WWF Wrestlemania 2000/Virtual Pro Wrestling 2 soundfont | HandlebarOrionX | musical-artifacts | CC BY 3.0 | ✓ | — | 1869 | game |
| 185 | Mighty Milky Way Soundfont | Lexicon86 | musical-artifacts | CC BY 3.0 | ✓ | — | 1868 | game |
| 186 | Mario Kart: Super Circuit Soundfont | Rosetta | musical-artifacts | CC BY 3.0 | — | — | 1854 | game |
| 187 | Sonic Advance Soundfont | OnuteWORLD Server Ltd. | musical-artifacts | CC BY 3.0 | ✓ | — | 1842 | game |
| 188 | Sonic the Hedgehog (Nintendo DS) Soundfont | Mildanner, Stealth | musical-artifacts | CC BY 3.0 | ✓ | — | 1838 | game |
| 189 | Knuckles Chaotix Drum Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 1806 | game |
| 190 | Sonic Hacking Contest Splash Screen Soundfont | Mildanner, Naoto, MDTravis | musical-artifacts | CC BY 3.0 | ✓ | — | 1783 | game |
| 191 | F-Zero: GP Legend GBA 2.0 | TheBlackHand28 | musical-artifacts | CC BY 3.0 | ✓ | — | 1776 | game |
| 192 | Yeah Jam Fury - Piano Block Soundfont | Mildanner, McLeodGaming, Willy | musical-artifacts | CC BY 3.0 | ✓ | — | 1764 | game |
| 193 | Segapede Soundfont Remake | Mildanner, Howard Drossin | musical-artifacts | CC BY 3.0 | ✓ | — | 1734 | game |
| 194 | MegaMan Battle Network 4.5 Soundfont | Nintenducc | musical-artifacts | CC BY 3.0 | ✓ | — | 1657 | game |
| 195 | Pantufa the Cat Orchestral Hit Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 1631 | game |
| 196 | Master System Game Gear Drum Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 1555 | game |
| 197 | MegaMan Battle Network 6 Soundfont | Nintenducc | musical-artifacts | CC BY 3.0 | ✓ | — | 1514 | game |
| 198 | Sonic the Hedgehog 2 Prototype Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 1508 | game |
| 199 | Izzy's Quest for the Olympic Rings (Genesis) | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 1498 | game |
| 200 | Sonic Robo Blast 2 Genesis Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 1491 | game |
| 201 | Sonic Jam (Sega Saturn) Soundfont | GAB64 | musical-artifacts | CC BY 3.0 | ✓ | — | 1396 | game |
| 202 | C700 VST Soundfont | Mildanner, osoumen | musical-artifacts | CC BY 3.0 | ✓ | — | 1389 | game |
| 203 | SoniNeko Drum Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 1380 | game |
| 204 | Super Mario Advance Soundfont V2 | OnuteWORLD Server Ltd. | musical-artifacts | CC BY 3.0 | ✓ | — | 1342 | game |
| 205 | MegaMan Battle Network 3 Soundfont | Nintenducc | musical-artifacts | CC BY 3.0 | ✓ | — | 1273 | game |
| 206 | Pana Der Hejhog Soundfont | Mildanner, MarkeyJester | musical-artifacts | CC BY 3.0 | ✓ | — | 1261 | game |
| 207 | Sonic 3 Movie Promo Cart Soundfont | Mildanner, Paramount Pictures | musical-artifacts | CC BY 3.0 | ✓ | — | 1247 | game |
| 208 | Ristar (Sega Genesis) Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 1215 | game |
| 209 | FIFA Soccer 95 Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 1200 | game |
| 210 | NBA LIVE 95 (Genesis) Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 1198 | game |
| 211 | MegaMan Battle Network 5 Soundfont | Nintenducc | musical-artifacts | CC BY 3.0 | ✓ | — | 1193 | game |
| 212 | MegaMan Battle Network 1 Soundfont | Nintenducc | musical-artifacts | CC BY 3.0 | ✓ | — | 1179 | game |
| 213 | Jump Super Stars Soundfont (UPDATE 8/16/26) | VideoGameKid | musical-artifacts | CC BY 3.0 | ✓ | — | 1126 | game |
| 214 | Betray US Chrom | Bubby293 | musical-artifacts | CC BY 3.0 | ✓ | — | 1118 | game |
| 215 | MegaMan Battle Network 4 Soundfont | Nintenducc | musical-artifacts | CC BY 3.0 | ✓ | — | 1094 | game |
| 216 | MegaMan Battle Network 2 Soundfont | Nintenducc | musical-artifacts | CC BY 3.0 | ✓ | — | 1077 | game |
| 217 | Sonic the Hedgehog - To Be A Star Soundfont | Mildanner, Katsushimi, KGL, MD | musical-artifacts | CC BY 3.0 | ✓ | — | 1068 | game |
| 218 | DOOM (32X) Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 1050 | game |
| 219 | Fullmetal Alchemist: Stray Rondo Soundfont (UPDATE 8/18/2026) | VideoGameKid | musical-artifacts | CC BY 3.0 | ✓ | — | 1043 | game |
| 220 | Mega Man Zero 1 Soundfont (1/4) (UPDATE 8/16/2026) | VideoGameKid | musical-artifacts | CC BY 3.0 | ✓ | — | 1033 | game |
| 221 | Sonic Battle (USA) Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 1008 | game |
| 222 | Sonic 2 + Knuckles Chaotix Buzzer Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 971 | game |
| 223 | Kapi SoundFont Pack | — | polyphone | CC BY | ✓ | — | 947 | game |
| 224 | Mega Man 10 Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 938 | game |
| 225 | Sonic 1,2,3,CD Soundfont | — | polyphone | CC BY | ✓ | — | 895 | game |
| 226 | Super Mario World/All-stars Instruments | — | polyphone | CC BY | — | — | 858 | game |
| 227 | Sonic Eraser Frying Pan Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 845 | game |
| 228 | Sega Genesis Soundfont (More Complete, I Guess) | VladTheFatman | musical-artifacts | CC BY 3.0 | ✓ | — | 839 | game |
| 229 | Thunder Force IV Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 836 | game |
| 230 | Olympic Summer Games: Atlanta '96 (SNES) Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 823 | game |
| 231 | Roxie&#039;s Nintendo 64 General MIDI Soundfont | — | polyphone | CC BY | ✓ | — | 823 | game |
| 232 | F-Zero GP Legend & Climax Soundfont (UPDATE 8/16/26) | VideoGameKid | musical-artifacts | CC BY 3.0 | ✓ | — | 791 | game |
| 233 | Sonic ERaZor (ROM hack) Soundfont | Mildanner, Selbi, Amphobius an | musical-artifacts | CC BY 3.0 | ✓ | — | 778 | game |
| 234 | The Complete Sonic Advance 1/2/3 Soundfont Combined | Bouncy Glow's Music Room, robt | musical-artifacts | CC BY 3.0 | ✓ | — | 767 | game |
| 235 | Izzy's Quest for the Olympic Rings (SNES) | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 744 | game |
| 236 | Pinball Tycoon | MLP DJ Gamer Appledash FIM | musical-artifacts | CC BY 3.0 | ✓ | — | 740 | game |
| 237 | NEW Fist of the North Star DS Soundfont (UPDATE 5/17/2026) | VideoGameKid | musical-artifacts | CC BY 3.0 | ✓ | — | 678 | game |
| 238 | Pucca Power Up (DS) Soundfont | Athosworld | musical-artifacts | CC BY 3.0 | ✓ | — | 673 | game |
| 239 | Top Gear (SNES) Soundfont | Mildanner, Gremlin | musical-artifacts | CC BY 3.0 | ✓ | — | 654 | game |
| 240 | Simpsons, The - Bart's Nightmare (SNES) Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 642 | game |
| 241 | Genesis Sonic HQ Bass Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 620 | game |
| 242 | Dangerous Seed (Genesis) Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 619 | game |
| 243 | Ristar FM Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 597 | game |
| 244 | Sesame Street Counting Cafe Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 593 | game |
| 245 | Sonic Mania Soundfont : Sf2 fixed [Updated] | — | polyphone | CC BY | ✓ | — | 583 | game |
| 246 | Sonic 1 Definitive - SHC 2021 Drum Soundfont | Mildanner, Inferno, RadiantNex | musical-artifacts | CC BY 3.0 | ✓ | — | 574 | game |
| 247 | SNES FM Pick Bass DWP (Hooded Edge) | Mildanner, Hooded Edge | musical-artifacts | CC BY 3.0 | — | — | 555 | game |
| 248 | Sonic 2 ARZ Piano HQ Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 551 | game |
| 249 | Socket Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 540 | game |
| 250 | GAX Sound Engine Soundfont | Novo Lubub Music/Shin'en Multi | musical-artifacts | CC BY | ✓ | — | 534 | game |
| 251 | Battle Mania Daiginjou (Genesis) Soundfont | Mildanner, SEGA | musical-artifacts | CC BY 3.0 | ✓ | — | 517 | game |
| 252 | Top Gear 2 (Genesis) Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 472 | game |
| 253 | Nintendo Famicon Soundfont | Bernardo Jose | musical-artifacts | CC BY 3.0 | ✓ | — | 453 | game |
| 254 | The Flintstones (SNES) Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 452 | game |
| 255 | XBOX GM Soundfont | Microsoft, XXtherobloxx21 | musical-artifacts | CC BY 3.0 | ✓ | — | 440 | game |
| 256 | Sonic ERaZor - Drum Soundfont | Mildanner, Selbi, Eduardo Knuc | musical-artifacts | CC BY 3.0 | ✓ | — | 434 | game |
| 257 | Shin Megami Tensei II (SNES) soundfont | Vènatus aka YaBoiVen on youtub | musical-artifacts | CC BY 3.0 | ✓ | — | 411 | game |
| 258 | Casino Night Zone Soundfont | Sonicluver1, SEGA | musical-artifacts | CC BY 3.0 | ✓ | — | 383 | game |
| 259 | Care Bears - Care Quest (Game Boy Advance) Soundfont | Novo Lubub Music/Mildanner/The | musical-artifacts | CC BY | ✓ | — | 374 | game |
| 260 | Ristar Drum Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 373 | game |
| 261 | VAdaPEGA Logo YM2612 Horn Soundfont | Mildanner, VAdaPEGA | musical-artifacts | CC BY 3.0 | ✓ | — | 368 | game |
| 262 | Nineko Vibraphone YM2612 Soundfont | Mildanner, Nineko | musical-artifacts | CC BY 3.0 | ✓ | — | 365 | game |
| 263 | Time Trax (SNES) Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 364 | game |
| 264 | Sonic the Reborn 2025 - PCM Soundfont | Mildanner, HipSnake | musical-artifacts | CC BY 3.0 | ✓ | — | 357 | game |
| 265 | Tricky SoundFont (Friday Night Funkin&#039; Vs. Tricky) | — | polyphone | CC BY | ✓ | — | 342 | game |
| 266 | Zero the Kamikaze Sequel SNES Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 326 | game |
| 267 | The Jetzons Mini Instrument Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 323 | game |
| 268 | Tabi (Friday Night Funkin&#039; Vs. Tabi EX) | — | polyphone | CC BY | ✓ | — | 291 | game |
| 269 | Iridion 3D (Game Boy Advance) GM Soundfont | Majesco Entertainment/Shin'en  | musical-artifacts | CC BY | ✓ | — | 290 | game |
| 270 | Kirby's Dream Land Soundfont Rework! | ArtifactedSonicMusical | musical-artifacts | CC BY 3.0 | ✓ | — | 270 | game |
| 271 | Baldi SoundFont (Friday Night Funkin&#039; Vs. Baldi) | — | polyphone | CC BY | ✓ | — | 262 | game |
| 272 | The original Joytunes soundfont! | — | polyphone | CC BY | ✓ | — | 229 | game |
| 273 | Fixed Rude buster soundfont v2 | — | polyphone | CC BY | ✓ | — | 215 | game |
| 274 | Fixed Mega Man X3 Soundfont | — | polyphone | CC BY | ✓ | — | 213 | game |
| 275 | Best Friends (PC Game) | — | polyphone | CC BY | ✓ | — | 196 | game |
| 276 | Fixed Chrono Trigger Soundfont | — | polyphone | CC BY | ✓ | — | 192 | game |
| 277 | Super Mario All-Stars Instrument Set Soundfont | — | polyphone | CC BY | ✓ | — | 164 | game |
| 278 | Sonic 1/2/3/K Instruments Drumkits | — | polyphone | CC BY | ✓ | — | 162 | game |
| 279 | Coronation Day/'the Soundfont | owerkadower | musical-artifacts | CC BY 3.0 | ✓ | — | 154 | game |
| 280 | Fixed Mario Paint 2.0 Soundfont | — | polyphone | CC BY | ✓ | — | 146 | game |
| 281 | Fixed Sega Genesis (ym2612) electric guitars SUPER DUPER pack Soundfon | — | polyphone | CC BY | ✓ | — | 140 | game |
| 282 | The Fixed Complete Sonic Advance 1,2,&amp; 3 Soundfont | — | polyphone | CC BY | ✓ | — | 139 | game |
| 283 | Socket (Time Dominator) - TFI Instrument Pack | Mildanner | musical-artifacts | CC BY 3.0 | — | — | 138 | game |
| 284 | Fixed Plok Soundfont | — | polyphone | CC BY | ✓ | — | 135 | game |
| 285 | Best of Board Games DS SoundFont | — | polyphone | CC BY | ✓ | — | 130 | game |
| 286 | Fixed Kirby Super Star Soundfont | — | polyphone | CC BY | ✓ | — | 126 | game |
| 287 | SNES Core Soundfont Updated V2 | — | polyphone | CC BY | ✓ | — | 117 | game |
| 288 | Fixed Kirby&#039;s Dreamland 3 Soundfont | — | polyphone | CC BY | ✓ | — | 99 | game |
| 289 | Fixed Mr.Sanic&#039;s NES Soundfont | — | polyphone | CC BY | ✓ | — | 95 | game |
| 290 | Sega&#039;s FM: Orchestra Hit Collection | — | polyphone | CC BY | ✓ | — | 93 | game |
| 291 | Fixed Teenage Mutant Ninja Turtles IV Turtles in Time Soundfont Update | — | polyphone | CC BY | ✓ | — | 89 | game |
| 292 | Sonic Mania Drum | — | polyphone | CC BY | ✓ | — | 87 | game |
| 293 | All of Random SNES Distorted Guitars, Overdrive Guitars, Slap Basses,  | — | polyphone | CC BY | ✓ | — | 83 | game |
| 294 | Fixed Donkey Kong Country Soundfont | — | polyphone | CC BY | ✓ | — | 83 | game |
| 295 | Fixed PCM/Sega AM2 Soundfont | — | polyphone | CC BY | ✓ | — | 81 | game |
| 296 | Fixed Super Game Boy Soundfont | — | polyphone | CC BY | ✓ | — | 78 | game |
| 297 | Fixed Mega Man X3 Revised | — | polyphone | CC BY | ✓ | — | 77 | game |
| 298 | New! Sega Genesis Chiptune Drum | — | polyphone | CC BY | ✓ | — | 77 | game |
| 299 | Fixed Mega Man X2 Soundfont | — | polyphone | CC BY | ✓ | — | 76 | game |
| 300 | Math Play | MrPropper | musical-artifacts | CC BY 3.0 | ✓ | — | 75 | game |
| 301 | Fixed Pizza Tower SNES Instrumentals Soundfont | — | polyphone | CC BY | ✓ | — | 73 | game |
| 302 | Super Mario World Instrument set | — | polyphone | CC BY | ✓ | — | 72 | game |
| 303 | Fixed WIP Sonic Mania Soundfont | — | polyphone | CC BY | ✓ | — | 71 | game |
| 304 | BS The Legend of Zelda Instrument set Soundfont | — | polyphone | CC BY | ✓ | — | 69 | game |
| 305 | Fixed Donkey Kong Country 2 Soundfont | — | polyphone | CC BY | ✓ | — | 65 | game |
| 306 | SNES-Like Soundfont | — | polyphone | CC BY | ✓ | — | 65 | game |
| 307 | My Version of Sonic Genesis Drumkits | — | polyphone | CC BY | ✓ | — | 61 | game |
| 308 | Snoopy Concert v2 Soundfont | — | polyphone | CC BY | ✓ | — | 61 | game |
| 309 | Fixed Street Fighter 2 World Warrior Soundfont | — | polyphone | CC BY | ✓ | — | 59 | game |
| 310 | Fixed Super Metroid Soundfont | — | polyphone | CC BY | ✓ | — | 59 | game |
| 311 | My Fixed Super Mario Kart Soundfont | — | polyphone | CC BY | ✓ | — | 57 | game |
| 312 | My Version of Mario Paint Soundfont | — | polyphone | CC BY | ✓ | — | 56 | game |
| 313 | Donkey Kong Country 3 Instrument sets | — | polyphone | CC BY | ✓ | — | 55 | game |
| 314 | Fixed Complete Mega Man X1 SF | — | polyphone | CC BY | ✓ | — | 55 | game |
| 315 | Fixed YM2612 Basses Soundfont Updated | — | polyphone | CC BY | ✓ | — | 52 | game |
| 316 | SNES Samples Soundfont | — | polyphone | CC BY | ✓ | — | 52 | game |
| 317 | Clock Tower SNES Soundfont | — | polyphone | CC BY | ✓ | — | 51 | game |
| 318 | Mighty Morphin Power Rangers The Fighting Edition V2 Soundfont | — | polyphone | CC BY | ✓ | — | 51 | game |
| 319 | SMW Drumkit | — | polyphone | CC BY | ✓ | — | 51 | game |
| 320 | Fixed Mega Man 7 Soundfont | — | polyphone | CC BY | ✓ | — | 50 | game |
| 321 | My Version of Yoshi&#039;s Island Soundfont | — | polyphone | CC BY | ✓ | — | 50 | game |
| 322 | Super Mario RPG Instrument set | — | polyphone | CC BY | ✓ | — | 50 | game |
| 323 | Mario Paint Instrument Set | — | polyphone | CC BY | ✓ | — | 49 | game |
| 324 | Streets Of Rage Drumkit Trilogy | — | polyphone | CC BY | ✓ | — | 49 | game |
| 325 | All of Random SNES Distorted Guitars, Overdrive Guitars, Slap Basses,  | — | polyphone | CC BY | ✓ | — | 48 | game |
| 326 | Fixed Sonic Audio Gems Collection Updated | — | polyphone | CC BY | ✓ | — | 48 | game |
| 327 | MJ MoonWalker Drumkits | — | polyphone | CC BY | ✓ | — | 48 | game |
| 328 | Chrono Trigger Drumkit | — | polyphone | CC BY | ✓ | — | 47 | game |
| 329 | Fixed Kirby&#039;s Dream Course Soundfont | — | polyphone | CC BY | ✓ | — | 47 | game |
| 330 | Fixed Secret of Mana SNES Soundfont | — | polyphone | CC BY | ✓ | — | 47 | game |
| 331 | Decap Attack Soundfont | — | polyphone | CC BY | ✓ | — | 46 | game |
| 332 | Fixed CPS-2 Mega Man Soundfont | — | polyphone | CC BY | ✓ | — | 46 | game |
| 333 | Tokimeki Memorial Instrument set Soundfont | — | polyphone | CC BY | ✓ | — | 46 | game |
| 334 | Donkey Kong Country Instrument set | — | polyphone | CC BY | ✓ | — | 45 | game |
| 335 | Fixed Bomberman 5 Soundfont | — | polyphone | CC BY | ✓ | — | 45 | game |
| 336 | Sega Master System Drumkit | — | polyphone | CC BY | ✓ | — | 45 | game |
| 337 | Ren &amp; Stimpy Fire Dogs midi files and a Randon SNES soundfont from | — | polyphone | CC BY | ✓ | — | 44 | game |
| 338 | My Version of Super Mario World Soundfont | — | polyphone | CC BY | ✓ | — | 43 | game |
| 339 | Samuri Shodown Instrument set Soundfont | — | polyphone | CC BY | ✓ | — | 43 | game |
| 340 | Yoshi&#039;s Island SNES Instrument set | — | polyphone | CC BY | ✓ | — | 43 | game |
| 341 | Another SMW Soundfont | — | polyphone | CC BY | ✓ | — | 42 | game |
| 342 | Fixed Secret Of Evermore Soundfont | — | polyphone | CC BY | ✓ | — | 42 | game |
| 343 | TMNT Tournament Fighters v2 | — | polyphone | CC BY | ✓ | — | 42 | game |
| 344 | Axelay v4 Soundfont | — | polyphone | CC BY | ✓ | — | 41 | game |
| 345 | Fixed Super Street Fighter 2  - The New Challengers SNES Soundfont | — | polyphone | CC BY | ✓ | — | 41 | game |
| 346 | Pac-Man 2 V2 Soundfont | — | polyphone | CC BY | ✓ | — | 41 | game |
| 347 | Super Adventure Island 2 SNES Soundfont | — | polyphone | CC BY | ✓ | — | 41 | game |
| 348 | Twinbee: Rainbow Bell Adventures V2 Soundfont | — | polyphone | CC BY | ✓ | — | 41 | game |
| 349 | My Version Super Mario Kart Soundfont | — | polyphone | CC BY | ✓ | — | 40 | game |
| 350 | Super Mario Kart Instrument set | — | polyphone | CC BY | ✓ | — | 40 | game |
| 351 | Super Mario SNES Soundfont 2 Drumkits | — | polyphone | CC BY | ✓ | — | 40 | game |
| 352 | Teenage Mutant Ninja Turtles IV: Turtles in Time Soundfont | — | polyphone | CC BY | ✓ | — | 40 | game |
| 353 | Fixed 31 Minutos SNES Soundfont (Fanmade) Soundfont | — | polyphone | CC BY | ✓ | — | 38 | game |
| 354 | Fixed CPS2 V1.0 Soundfont | — | polyphone | CC BY | ✓ | — | 38 | game |
| 355 | Fixed Kirby Soundfont Supplements | — | polyphone | CC BY | ✓ | — | 38 | game |
| 356 | Sonic 1 SNES Soundfont | — | polyphone | CC BY | ✓ | — | 38 | game |
| 357 | Super Castlevania 4 Soundfont | — | polyphone | CC BY | ✓ | — | 38 | game |
| 358 | Axelay Soundfont | — | polyphone | CC BY | ✓ | — | 37 | game |
| 359 | Fixed Sonic Battle Soundfont | — | polyphone | CC BY | ✓ | — | 37 | game |
| 360 | My Version of Donkey Kong Country 2 Soundfont | — | polyphone | CC BY | ✓ | — | 37 | game |
| 361 | TMNT Tournament Fighters V5 Soundfont Updated | — | polyphone | CC BY | ✓ | — | 37 | game |
| 362 | 31 Minutes Drumkits | — | polyphone | CC BY | ✓ | — | 36 | game |
| 363 | Donkey Kong Country 2 Instrument set | — | polyphone | CC BY | ✓ | — | 36 | game |
| 364 | Fixed Yoshi&#039;s Island Instruments | — | polyphone | CC BY | ✓ | — | 36 | game |
| 365 | Kirby&#039;s Avalanche Instrument set Soundfont | — | polyphone | CC BY | ✓ | — | 36 | game |
| 366 | UNDAKE 30 Same Game Mario Version Soundfont | — | polyphone | CC BY | ✓ | — | 36 | game |
| 367 | Battletoads Battlemanics Fixed Soundfont | — | polyphone | CC BY | ✓ | — | 35 | game |
| 368 | My Version of Donkey Kong Country Soundfont | — | polyphone | CC BY | ✓ | — | 35 | game |
| 369 | Sega&#039;s FM: Alt 32X Drums | — | polyphone | CC BY | ✓ | — | 35 | game |
| 370 | Fixed Mickey Mania (Sega CD) Soundfont | — | polyphone | CC BY | ✓ | — | 34 | game |
| 371 | Pocky &amp; Rocky 1&amp;2 Instrument sets Soundfont | — | polyphone | CC BY | ✓ | — | 34 | game |
| 372 | Seifuku Densetu Pretty Fighter Instrument set Soundfont | — | polyphone | CC BY | ✓ | — | 34 | game |
| 373 | All of Random SNES Distorted Guitars, Overdrive Guitars, Slap Basses,  | — | polyphone | CC BY | ✓ | — | 33 | game |
| 374 | Biker Mice From Mars Soundfont | — | polyphone | CC BY | ✓ | — | 33 | game |
| 375 | goofy troop | — | polyphone | CC BY | ✓ | — | 33 | game |
| 376 | Sega&#039;s FM: Billie Jean DAC | — | polyphone | CC BY | ✓ | — | 33 | game |
| 377 | Speedy Gonzales SNES soundfont | — | polyphone | CC BY | ✓ | — | 33 | game |
| 378 | Twinbee: Rainbow Bell Adventures Instrument set Soundfont | — | polyphone | CC BY | ✓ | — | 33 | game |
| 379 | Dragon Ball Z Super Butouden 2 V2 Soundfont | — | polyphone | CC BY | ✓ | — | 32 | game |
| 380 | Fatal Fury Soundfont | — | polyphone | CC BY | ✓ | — | 32 | game |
| 381 | Fixed Data East Soundfont | — | polyphone | CC BY | ✓ | — | 32 | game |
| 382 | Fixed Lion King SNES Soundfont With Drumkit | — | polyphone | CC BY | ✓ | — | 32 | game |
| 383 | My Version Sonic Advance 3 Soundfont | — | polyphone | CC BY | ✓ | — | 32 | game |
| 384 | Snoopy&#039;s Concert Drumkit | — | polyphone | CC BY | ✓ | — | 32 | game |
| 385 | The Adventures of Batman and Robin Instrument set Soundfont | — | polyphone | CC BY | ✓ | — | 32 | game |
| 386 | Animaniacs V2 Soundfont | — | polyphone | CC BY | ✓ | — | 31 | game |
| 387 | Fixed MX. K&#039;s Super Nintendo Soundfont | — | polyphone | CC BY | ✓ | — | 31 | game |
| 388 | Fixed Rock n&#039; Roll Racing Soundfont | — | polyphone | CC BY | ✓ | — | 31 | game |
| 389 | Fixed Beavis &amp;  Butt-Head Soundfont Updated | — | polyphone | CC BY | ✓ | — | 30 | game |
| 390 | Fixed Porky Pig&#039;s Haunted Holiday Soundfont | — | polyphone | CC BY | ✓ | — | 30 | game |
| 391 | Fixed The Magical Quest Starring Mickey Mouse SNES Soundfont | — | polyphone | CC BY | ✓ | — | 30 | game |
| 392 | HOME ALONE 2 SNES | — | polyphone | CC BY | ✓ | — | 30 | game |
| 393 | My Version of Sonic Advance 2 Soundfont | — | polyphone | CC BY | ✓ | — | 30 | game |
| 394 | My Version of Super Mario All-Stars Soundfont | — | polyphone | CC BY | ✓ | — | 30 | game |
| 395 | Sonic Gems Drumkits{Updated} Add Instruments | — | polyphone | CC BY | ✓ | — | 30 | game |
| 396 | Super Famicon Box Instrument Set Soundfont | — | polyphone | CC BY | ✓ | — | 30 | game |
| 397 | ActRaiser V2 Soundfont | — | polyphone | CC BY | ✓ | — | 29 | game |
| 398 | Castlevania  Dracula X Drumkit | — | polyphone | CC BY | ✓ | — | 29 | game |
| 399 | Fixed Drum The Absolute Sega FM Soundfont V2 32X Drum | — | polyphone | CC BY | ✓ | — | 29 | game |
| 400 | Fixed Final Fight Soundfont | — | polyphone | CC BY | ✓ | — | 29 | game |
| 401 | Fixed Jeopardy SNES Soundfont | — | polyphone | CC BY | ✓ | — | 29 | game |
| 402 | Fixed Mega Man And Bass Soundfont | — | polyphone | CC BY | ✓ | — | 29 | game |
| 403 | Fixed Bubsy 2 SNES Soundfont | — | polyphone | CC BY | ✓ | — | 28 | game |
| 404 | Fixed Ed Edd n Eddy Jawbreakers Soundfont | — | polyphone | CC BY | ✓ | — | 28 | game |
| 405 | Fixed Rockman X(UNCOMPRESSED SOUNDPAK) | — | polyphone | CC BY | ✓ | — | 28 | game |
| 406 | Saturday Night Slam Masters V2 Soundfont | — | polyphone | CC BY | ✓ | — | 28 | game |
| 407 | SEGA!!!! Jingle | — | polyphone | CC BY | ✓ | — | 28 | game |
| 408 | Sonic 1 DSK Edition Drum | — | polyphone | CC BY | ✓ | — | 28 | game |
| 409 | Super Adventure Island Instrument set | — | polyphone | CC BY | ✓ | — | 28 | game |
| 410 | Twinbee: Rainbow Bell Adventures Drumkit | — | polyphone | CC BY | ✓ | — | 28 | game |
| 411 | X-Zone V3 Soundfont | — | polyphone | CC BY | ✓ | — | 28 | game |
| 412 | After Burner 32X Soundfont | — | polyphone | CC BY | ✓ | — | 27 | game |
| 413 | Fixed Mario &amp; Wario Soundfont | — | polyphone | CC BY | ✓ | — | 27 | game |
| 414 | Fixed Psycho Dream SNES Soundfont | — | polyphone | CC BY | ✓ | — | 27 | game |
| 415 | Fixed Scooby Doo SNES | — | polyphone | CC BY | ✓ | — | 27 | game |
| 416 | Mighty Morphin Power Rangers Fighting Edition Drumkit | — | polyphone | CC BY | ✓ | — | 27 | game |
| 417 | SatellaView Satella Walker: Sate Bou wo Sukuidasu! | — | polyphone | CC BY | ✓ | — | 27 | game |
| 418 | SatellaView SatesupuDX 4 | — | polyphone | CC BY | ✓ | — | 27 | game |
| 419 | Snoopy&#039;s Concert V3 Soundfont | — | polyphone | CC BY | ✓ | — | 27 | game |
| 420 | Tetris 2 Drumkit | — | polyphone | CC BY | ✓ | — | 27 | game |
| 421 | Barkley Shut Up and Jam! Soundfont | — | polyphone | CC BY | ✓ | — | 26 | game |
| 422 | Dragon Ball Z: Super Butouden 2 Instrument set Soundfont | — | polyphone | CC BY | ✓ | — | 26 | game |
| 423 | Fixed Alcahest Soundfont | — | polyphone | CC BY | ✓ | — | 26 | game |
| 424 | Fixed Tetris 2 SNES Soundfont V2 | — | polyphone | CC BY | ✓ | — | 26 | game |
| 425 | Jikkyou Oshaberi Parodius Forever with Me Instrument set Soundfont | — | polyphone | CC BY | ✓ | — | 26 | game |
| 426 | Street Fighter 2 MD Drumkit | — | polyphone | CC BY | ✓ | — | 26 | game |
| 427 | Tetris &amp; Dr.Mario Soundfont | — | polyphone | CC BY | ✓ | — | 26 | game |
| 428 | X-Men Mutant Apocalypse Instrument Set Soundfont | — | polyphone | CC BY | ✓ | — | 26 | game |
| 429 | Yoshi&#039;s Safari Instrument set Soundfont | — | polyphone | CC BY | ✓ | — | 26 | game |
| 430 | Art of Fighting V2 Soundfont | — | polyphone | CC BY | ✓ | — | 25 | game |
| 431 | Fatal Fury Special Instrument sets Soundfont | — | polyphone | CC BY | ✓ | — | 25 | game |
| 432 | Fixed Mega Man 7 SNES Soundfont V2 | — | polyphone | CC BY | ✓ | — | 25 | game |
| 433 | Fixed Rushing Beat Shura/The Peace Keepers Soundfont | — | polyphone | CC BY | ✓ | — | 25 | game |
| 434 | Fixed Spider-Man and X-Men in Arcade&#039;s Revenge Soundfont | — | polyphone | CC BY | ✓ | — | 25 | game |
| 435 | Knight of the Round Instrument set Soundfont | — | polyphone | CC BY | ✓ | — | 25 | game |
| 436 | Megaman The Wily Wars Drumkits | — | polyphone | CC BY | ✓ | — | 25 | game |
| 437 | Street Fighter Arcade Drumkit | — | polyphone | CC BY | ✓ | — | 25 | game |
| 438 | Stunt FX Drumkit | — | polyphone | CC BY | ✓ | — | 25 | game |
| 439 | Super Adventure Island Drumkit | — | polyphone | CC BY | ✓ | — | 25 | game |
| 440 | The Ninja Warriors V2 Soundfont | — | polyphone | CC BY | ✓ | — | 25 | game |
| 441 | Fixed Cool Spot Soundfont | — | polyphone | CC BY | ✓ | — | 24 | game |
| 442 | Fixed Mega Man &amp; Bass SNES Soundfont V2 | — | polyphone | CC BY | ✓ | — | 24 | game |
| 443 | Fixed Mega Man Battle Network 1 Soundfont | — | polyphone | CC BY | ✓ | — | 24 | game |
| 444 | Fixed Mortal Kombat 3 SNES Soundfont | — | polyphone | CC BY | ✓ | — | 24 | game |
| 445 | Fixed SuperNintendoEntertainmentSystemV1.2 | — | polyphone | CC BY | ✓ | — | 24 | game |
| 446 | Mega Man 7 Instrument set Soundfont | — | polyphone | CC BY | ✓ | — | 24 | game |
| 447 | My Version of Contra Soundfont | — | polyphone | CC BY | ✓ | — | 24 | game |
| 448 | Pac-Attack V2 Soundfont | — | polyphone | CC BY | ✓ | — | 24 | game |
| 449 | The Ninja Warriors Drumkit | — | polyphone | CC BY | ✓ | — | 24 | game |
| 450 | Fixed 31 Minutes Soundfont V2 | — | polyphone | CC BY | ✓ | — | 23 | game |
| 451 | Fixed Empire Interactive SNES Soundfont | — | polyphone | CC BY | ✓ | — | 23 | game |
| 452 | Fixed Equinox Soundfont | — | polyphone | CC BY | ✓ | — | 23 | game |
| 453 | Fixed F-Zero SNES Soundfont | — | polyphone | CC BY | ✓ | — | 23 | game |
| 454 | Fixed F91 Soundfont | — | polyphone | CC BY | ✓ | — | 23 | game |
| 455 | Fixed Marvel Super Heroes War of The Gems Soundfont | — | polyphone | CC BY | ✓ | — | 23 | game |
| 456 | Fixed MMX6 PSX/PS1 Soundfont | — | polyphone | CC BY | ✓ | — | 23 | game |
| 457 | Fixed Mortal Kombat 2 SNES Soundfont | — | polyphone | CC BY | ✓ | — | 23 | game |
| 458 | Fixed Sparkster Soundfont | — | polyphone | CC BY | ✓ | — | 23 | game |
| 459 | Fixed Super Back To The Future SNES Soundfont | — | polyphone | CC BY | ✓ | — | 23 | game |
| 460 | Fixed WaterWorld Soundfont | — | polyphone | CC BY | ✓ | — | 23 | game |
| 461 | Mark Davis&#039;s The Fishing Master Instrument set Soundfont | — | polyphone | CC BY | ✓ | — | 23 | game |
| 462 | My Version of DKC 3 Soundfont | — | polyphone | CC BY | ✓ | — | 23 | game |
| 463 | Pac-Attack Instrument set Soundfont | — | polyphone | CC BY | ✓ | — | 23 | game |
| 464 | Pac-Man 2 Drumkit | — | polyphone | CC BY | ✓ | — | 23 | game |
| 465 | SimCity Instrument set | — | polyphone | CC BY | ✓ | — | 23 | game |
| 466 | Super Fantasy Zone drumkit | — | polyphone | CC BY | ✓ | — | 23 | game |
| 467 | Tetris 2 Instrument set Soundfont | — | polyphone | CC BY | ✓ | — | 23 | game |
| 468 | TMNT Tournament Fighters V2 [Updated] | — | polyphone | CC BY | ✓ | — | 23 | game |
| 469 | X-Zone Drumkit | — | polyphone | CC BY | ✓ | — | 23 | game |
| 470 | Fixed Bubsy in Claws Encounters of the furred kind Soundfont | — | polyphone | CC BY | ✓ | — | 22 | game |
| 471 | Fixed Daze Before Christmas Soundfont | — | polyphone | CC BY | ✓ | — | 22 | game |
| 472 | Fixed Mega Man Chip Challenge Soundfont | — | polyphone | CC BY | ✓ | — | 22 | game |
| 473 | Fixed Mickey Mania Soundfont | — | polyphone | CC BY | ✓ | — | 22 | game |
| 474 | Fixed MixEYE SDSk02 Soundfont V2 | — | polyphone | CC BY | ✓ | — | 22 | game |
| 475 | Fixed Puggsy Edited Version Soundfont | — | polyphone | CC BY | ✓ | — | 22 | game |
| 476 | Fixed Super Bomberman 3 SNES Soundfont | — | polyphone | CC BY | ✓ | — | 22 | game |
| 477 | John Madden&#039;s Football Drumkit | — | polyphone | CC BY | ✓ | — | 22 | game |
| 478 | Kirby&#039;s Avalanche Drumkit | — | polyphone | CC BY | ✓ | — | 22 | game |
| 479 | Lethal Enforcers | — | polyphone | CC BY | ✓ | — | 22 | game |
| 480 | Lethal Enforcers 2 Genesis Drumkit and Orchestra Hit | — | polyphone | CC BY | ✓ | — | 22 | game |
| 481 | Mega Man Soccer Soundfont | — | polyphone | CC BY | ✓ | — | 22 | game |
| 482 | Pac-Man 2 Instrument set | — | polyphone | CC BY | ✓ | — | 22 | game |
| 483 | Power Rangers The Movie Instrument set Soundfont | — | polyphone | CC BY | ✓ | — | 22 | game |
| 484 | Super Adventure Island V2 Soundfont | — | polyphone | CC BY | ✓ | — | 22 | game |
| 485 | Temco Super Bowl Instrument Set Soundfont | — | polyphone | CC BY | ✓ | — | 22 | game |
| 486 | Tiny Toons Wacky Sports Challenge Instrument Set | — | polyphone | CC BY | ✓ | — | 22 | game |
| 487 | Yoshi&#039;s Cookie Instrument set Soundfont | — | polyphone | CC BY | ✓ | — | 22 | game |
| 488 | a bugs life snes | — | polyphone | CC BY | ✓ | — | 21 | game |
| 489 | All of Random SNES Distorted Guitars, Overdrive Guitars, Slap Basses,  | — | polyphone | CC BY | ✓ | — | 21 | game |
| 490 | Animaniacs Instrument sets | — | polyphone | CC BY | ✓ | — | 21 | game |
| 491 | Arkanoid Doh It Again V2 Soundfont | — | polyphone | CC BY | ✓ | — | 21 | game |
| 492 | Art of Fighting Instrument set Soundfont | — | polyphone | CC BY | ✓ | — | 21 | game |
| 493 | Contra 3 Instrument set | — | polyphone | CC BY | ✓ | — | 21 | game |
| 494 | F-Zero Instrument set | — | polyphone | CC BY | ✓ | — | 21 | game |
| 495 | Final Fight Drumkit | — | polyphone | CC BY | ✓ | — | 21 | game |
| 496 | Fixed Dragon Ball Z Hyper Dimension | — | polyphone | CC BY | ✓ | — | 21 | game |
| 497 | Fixed Madden NFL 97 (SNES) Soundfont | — | polyphone | CC BY | ✓ | — | 21 | game |
| 498 | Fixed Super Mario Allstars &amp; Super Mario World SNES Soundfont | — | polyphone | CC BY | ✓ | — | 21 | game |
| 499 | Fixed Toy Story SNES Soundfont | — | polyphone | CC BY | ✓ | — | 21 | game |
| 500 | Harvest Moon Soundfont Updated | — | polyphone | CC BY | ✓ | — | 21 | game |
| 501 | Lethal Enforcers V3 Soundfont | — | polyphone | CC BY | ✓ | — | 21 | game |
| 502 | My Version of Sonic Advance Soundfont | — | polyphone | CC BY | ✓ | — | 21 | game |
| 503 | Pac-Attack Drumkit | — | polyphone | CC BY | ✓ | — | 21 | game |
| 504 | Sega&#039;s FM: Biker Drums | — | polyphone | CC BY | ✓ | — | 21 | game |
| 505 | TAZ Mania Drumkit | — | polyphone | CC BY | ✓ | — | 21 | game |
| 506 | X-Men Mutant Apocalypse V2 Soundfont | — | polyphone | CC BY | ✓ | — | 21 | game |
| 507 | Yoshi&#039;s Cookie V2 Soundfont | — | polyphone | CC BY | ✓ | — | 21 | game |
| 508 | Battletoads and Double Dragon Drumkit | — | polyphone | CC BY | ✓ | — | 20 | game |
| 509 | BSX Broadcast Instrument sets Soundfont | — | polyphone | CC BY | ✓ | — | 20 | game |
| 510 | EVO: Search of Eden Instrument set Soundfont | — | polyphone | CC BY | ✓ | — | 20 | game |
| 511 | Fixed ClayFighter Soundfont | — | polyphone | CC BY | ✓ | — | 20 | game |
| 512 | Fixed Cool World SNES | — | polyphone | CC BY | ✓ | — | 20 | game |
| 513 | Fixed Dragon Ball Z Super Butoden 2 Soundfont | — | polyphone | CC BY | ✓ | — | 20 | game |
| 514 | Fixed Ed Edd N Eddy Jawbreakers V2 Soundfont | — | polyphone | CC BY | ✓ | — | 20 | game |
| 515 | Fixed Equinox SNES Soundfont | — | polyphone | CC BY | ✓ | — | 20 | game |
| 516 | Fixed Jurassic Park (SNES) | — | polyphone | CC BY | ✓ | — | 20 | game |
| 517 | Fixed Magical Drop Soundfont | — | polyphone | CC BY | ✓ | — | 20 | game |
| 518 | Fixed Power Rangers Zeo: Battle Racers SNES Soundfont | — | polyphone | CC BY | ✓ | — | 20 | game |
| 519 | Fixed RPG Maker-Super Dante Soundfont | — | polyphone | CC BY | ✓ | — | 20 | game |
| 520 | Fixed Tetris Attack/ Panel de Pon Soundfont | — | polyphone | CC BY | ✓ | — | 20 | game |
| 521 | Ganbare Goemon 4 SNES Soundfont | — | polyphone | CC BY | ✓ | — | 20 | game |
| 522 | Gokujou Parodius Drumkit | — | polyphone | CC BY | ✓ | — | 20 | game |
| 523 | John Madden Football Instrument set Soundfont | — | polyphone | CC BY | ✓ | — | 20 | game |
| 524 | Sega&#039;s FM: Alt OPL-Drum | — | polyphone | CC BY | ✓ | — | 20 | game |
| 525 | Sega&#039;s FM: Alt Standard Drum | — | polyphone | CC BY | ✓ | — | 20 | game |
| 526 | SMAS V2 Drumkit | — | polyphone | CC BY | ✓ | — | 20 | game |
| 527 | SMRPG Drumkit 1,2&amp;3 | — | polyphone | CC BY | ✓ | — | 20 | game |
| 528 | SNES FM Pick Bass Soundfont | — | polyphone | CC BY | ✓ | — | 20 | game |
| 529 | Soul Blazer Instrument set Soundfont | — | polyphone | CC BY | ✓ | — | 20 | game |
| 530 | Tiny Toons Wacky Sports Challenge V2 Soundfont | — | polyphone | CC BY | ✓ | — | 20 | game |
| 531 | X-Zone Instrument set Soundfont | — | polyphone | CC BY | ✓ | — | 20 | game |
| 532 | ActRaiser 1&amp;2 Instrument set Soundfont | — | polyphone | CC BY | ✓ | — | 19 | game |
| 533 | Animaniacs Drumkit | — | polyphone | CC BY | ✓ | — | 19 | game |
| 534 | BSX Broadcast Drumkit | — | polyphone | CC BY | ✓ | — | 19 | game |
| 535 | Dragon Ball Z: Super Butouden Instrument set Soundfont | — | polyphone | CC BY | ✓ | — | 19 | game |
| 536 | EVO Search for Eden V2 Soundfont | — | polyphone | CC BY | ✓ | — | 19 | game |
| 537 | Fatal Fury V2 Soundfont | — | polyphone | CC BY | ✓ | — | 19 | game |
| 538 | Fixed Bubsy SNES Soundfont V2 | — | polyphone | CC BY | ✓ | — | 19 | game |
| 539 | Fixed Daze Before Christmas (SNES) Soundfont V2 | — | polyphone | CC BY | ✓ | — | 19 | game |
| 540 | Fixed Funaki-Kunio SNES | — | polyphone | CC BY | ✓ | — | 19 | game |
| 541 | Fixed Jurassic Park 2 SNES Soundfont | — | polyphone | CC BY | ✓ | — | 19 | game |
| 542 | Fixed Marko&#039;s Magic Football Soundfont 2.0 | — | polyphone | CC BY | ✓ | — | 19 | game |
| 543 | Fixed Mega Man Soccer Soundfont | — | polyphone | CC BY | ✓ | — | 19 | game |
| 544 | Fixed Mr. K&#039;s Super Nintendo Entertainment Soundfont V2 | — | polyphone | CC BY | ✓ | — | 19 | game |
| 545 | Fixed Skitchin&#039; Soundfont | — | polyphone | CC BY | ✓ | — | 19 | game |
| 546 | Fixed Super Punch-Out SNES Soundfont | — | polyphone | CC BY | ✓ | — | 19 | game |
| 547 | Fixed Tetsuwan Atom SNES Soundfont | — | polyphone | CC BY | ✓ | — | 19 | game |
| 548 | Fixed The Flintstones (SNES) - Soundfont | — | polyphone | CC BY | ✓ | — | 19 | game |
| 549 | Fixed Yoshi&#039;s Safari SNES Soundfont V2 | — | polyphone | CC BY | ✓ | — | 19 | game |
| 550 | Ganbare Goemon 2,3, &amp;4 Instrument sets Soundfonts | — | polyphone | CC BY | ✓ | — | 19 | game |
| 551 | Gokujou Parodius V2 Soundfont | — | polyphone | CC BY | ✓ | — | 19 | game |
| 552 | Home Alone 1991 SNES Drumkit | — | polyphone | CC BY | ✓ | — | 19 | game |
| 553 | Kirby&#039;s Avalanche V2 Soundfont | — | polyphone | CC BY | ✓ | — | 19 | game |
| 554 | Maerchen Adventure Cotton 100% Soundfont Updated Toms | — | polyphone | CC BY | ✓ | — | 19 | game |
| 555 | My Version of SimCity Soundfont | — | polyphone | CC BY | ✓ | — | 19 | game |
| 556 | Parodius-Non-Sense Fantasy Soundfont | — | polyphone | CC BY | ✓ | — | 19 | game |
| 557 | Saturday Night Slam Masters Drumkit | — | polyphone | CC BY | ✓ | — | 19 | game |
| 558 | Saturday Night Slam Masters Instrument set Soundfont | — | polyphone | CC BY | ✓ | — | 19 | game |
| 559 | Sega&#039;s FM Standard DAC | — | polyphone | CC BY | ✓ | — | 19 | game |
| 560 | Sega&#039;s FM: Not Hydro City DAC | — | polyphone | CC BY | ✓ | — | 19 | game |
| 561 | Terranigma Drumkit | — | polyphone | CC BY | ✓ | — | 19 | game |
| 562 | Battletoads and Double Dragon Fixed Soundfont | — | polyphone | CC BY | ✓ | — | 18 | game |
| 563 | BSX Broadcast and Every BSX game Soundfont | — | polyphone | CC BY | ✓ | — | 18 | game |
| 564 | Dragon&#039;s Lair Instrument set Soundfont | — | polyphone | CC BY | ✓ | — | 18 | game |
| 565 | Fixed Batman Forever SNES | — | polyphone | CC BY | ✓ | — | 18 | game |
| 566 | Fixed ClayFighter Drumkit | — | polyphone | CC BY | ✓ | — | 18 | game |
| 567 | Fixed Demon&#039;s Crest SNES Soundfont | — | polyphone | CC BY | ✓ | — | 18 | game |
| 568 | Fixed Drumkit SMAS Extended Ver. 1.1 Soundfont | — | polyphone | CC BY | ✓ | — | 18 | game |
| 569 | Fixed MMX2 *Improved ver* | — | polyphone | CC BY | ✓ | — | 18 | game |
| 570 | Fixed Pac in Time Soundfont | — | polyphone | CC BY | ✓ | — | 18 | game |
| 571 | Fixed Sunset Riders SNES Soundfont | — | polyphone | CC BY | ✓ | — | 18 | game |
| 572 | Ganbare Goemon 2 SNES Soundfont | — | polyphone | CC BY | ✓ | — | 18 | game |
| 573 | Gradius 3 Drumkit | — | polyphone | CC BY | ✓ | — | 18 | game |
| 574 | My Version of F-Zero Soundfont | — | polyphone | CC BY | ✓ | — | 18 | game |
| 575 | My Version of Pilotwings Soundfont | — | polyphone | CC BY | ✓ | — | 18 | game |
| 576 | Mystic Ark Instrument set Soundfont | — | polyphone | CC BY | ✓ | — | 18 | game |
| 577 | NBA Give &#039;N Go! Instrument Set Soundfont | — | polyphone | CC BY | ✓ | — | 18 | game |
| 578 | Parodius-Non-Sense Fantasy Drumkit | — | polyphone | CC BY | ✓ | — | 18 | game |
| 579 | Power Rangers The Fighting Edition Instrument set Soundfont | — | polyphone | CC BY | ✓ | — | 18 | game |
| 580 | Sega FM: Furnace Drum | — | polyphone | CC BY | ✓ | — | 18 | game |
| 581 | Sega&#039;s FM: Alt Virtua Racing Drums | — | polyphone | CC BY | ✓ | — | 18 | game |
| 582 | Sega&#039;s FM: Not Marble Zone DAC | — | polyphone | CC BY | ✓ | — | 18 | game |
| 583 | Stunt Race FX V2 Soundfont | — | polyphone | CC BY | ✓ | — | 18 | game |
| 584 | Sunset Riders Drumkit Soundfont SNES | — | polyphone | CC BY | ✓ | — | 18 | game |
| 585 | Super Buster Bros instrument set Soundfont | — | polyphone | CC BY | ✓ | — | 18 | game |
| 586 | Super Famicon Wars Instrument set Soundfont | — | polyphone | CC BY | ✓ | — | 18 | game |
| 587 | Tetris 2 V2 Soundfont | — | polyphone | CC BY | ✓ | — | 18 | game |
| 588 | Wonder Project J Kikai no Shounen Pino | — | polyphone | CC BY | ✓ | — | 18 | game |
| 589 | American Gladiators V2 Soundfont | — | polyphone | CC BY | ✓ | — | 17 | game |
| 590 | Battle Mania Daiginjou Drumkit | — | polyphone | CC BY | ✓ | — | 17 | game |
| 591 | Battlemanics Alt Drumkit | — | polyphone | CC BY | ✓ | — | 17 | game |
| 592 | Biker Mice From Mars Drumkit | — | polyphone | CC BY | ✓ | — | 17 | game |
| 593 | Final Fight 2 V2 Soundfont | — | polyphone | CC BY | ✓ | — | 17 | game |
| 594 | Fixed Aladdin SNES Soundfont | — | polyphone | CC BY | ✓ | — | 17 | game |
| 595 | Fixed Boogerman Soundfont | — | polyphone | CC BY | ✓ | — | 17 | game |
| 596 | Fixed Dragon Ball Z - Super Butouden 3 SNES Soundfont | — | polyphone | CC BY | ✓ | — | 17 | game |
| 597 | Fixed Madden NFL 98 (SNES) Soundfont | — | polyphone | CC BY | ✓ | — | 17 | game |
| 598 | Fixed The Adams Family SNES Soundfont | — | polyphone | CC BY | ✓ | — | 17 | game |
| 599 | Inspector Gadget SNES Instrument set | — | polyphone | CC BY | ✓ | — | 17 | game |
| 600 | My Version of Lil SNESS Drumkits | — | polyphone | CC BY | ✓ | — | 17 | game |
| 601 | My Version of Sunset Riders Soundfont | — | polyphone | CC BY | ✓ | — | 17 | game |
| 602 | NBA Give N&#039; Go Drumkit | — | polyphone | CC BY | ✓ | — | 17 | game |
| 603 | Pilotwings Instrument sets | — | polyphone | CC BY | ✓ | — | 17 | game |
| 604 | Robotrek Instrument set Soundfont | — | polyphone | CC BY | ✓ | — | 17 | game |
| 605 | Sega&#039;s FM: Alt Cool Drums | — | polyphone | CC BY | ✓ | — | 17 | game |
| 606 | SimCity SNES Drumkit | — | polyphone | CC BY | ✓ | — | 17 | game |
| 607 | Slap Fight MD Drumkit | — | polyphone | CC BY | ✓ | — | 17 | game |
| 608 | The Ninja Warriors Instrument set Soundfont | — | polyphone | CC BY | ✓ | — | 17 | game |
| 609 | ActRaiser 2 V2 Soundfont | — | polyphone | CC BY | ✓ | — | 16 | game |
| 610 | Biker Mice from Mars v2 Soundfont | — | polyphone | CC BY | ✓ | — | 16 | game |
| 611 | Capcom&#039;s MVP Football Drumkit | — | polyphone | CC BY | ✓ | — | 16 | game |
| 612 | Fixed Animaniacs SNES Soundfont V2 | — | polyphone | CC BY | ✓ | — | 16 | game |
| 613 | Fixed College Basketball Soundfont | — | polyphone | CC BY | ✓ | — | 16 | game |
| 614 | Fixed Donald Duck Mahou No Boushi | — | polyphone | CC BY | ✓ | — | 16 | game |
| 615 | Fixed Lupin 3 SNES | — | polyphone | CC BY | ✓ | — | 16 | game |
| 616 | Fixed PilotWings Soundfont | — | polyphone | CC BY | ✓ | — | 16 | game |
| 617 | Fixed Ranna 1/2: Hard Battle Soundfont | — | polyphone | CC BY | ✓ | — | 16 | game |
| 618 | Fixed Road Runner SNES | — | polyphone | CC BY | ✓ | — | 16 | game |
| 619 | Fixed Simcity Soundfont | — | polyphone | CC BY | ✓ | — | 16 | game |
| 620 | Fixed Super Off Road SNES Restored Soundfont | — | polyphone | CC BY | ✓ | — | 16 | game |
| 621 | Fixed Wayne&#039;s World Soundfont | — | polyphone | CC BY | ✓ | — | 16 | game |
| 622 | Gradius 3 Soundfont | — | polyphone | CC BY | ✓ | — | 16 | game |
| 623 | Inspector Gadget SNES Soundfont | — | polyphone | CC BY | ✓ | — | 16 | game |
| 624 | KAME RAIDER | — | polyphone | CC BY | ✓ | — | 16 | game |
| 625 | Lufia II - Rise of the Sinistrals | — | polyphone | CC BY | ✓ | — | 16 | game |
| 626 | Mean Bean Machine Drumkit | — | polyphone | CC BY | ✓ | — | 16 | game |
| 627 | PilotWings Drumkit Soundfont | — | polyphone | CC BY | ✓ | — | 16 | game |
| 628 | Sega&#039;s FM: Cool DAC | — | polyphone | CC BY | ✓ | — | 16 | game |
| 629 | Sega&#039;s FM: OPL DAC | — | polyphone | CC BY | ✓ | — | 16 | game |
| 630 | Sega&#039;s FM: Virtua Racing Drum | — | polyphone | CC BY | ✓ | — | 16 | game |
| 631 | Soul Blazer V2 Soundfont | — | polyphone | CC BY | ✓ | — | 16 | game |
| 632 | Sunset Riders SNES Instrument set | — | polyphone | CC BY | ✓ | — | 16 | game |
| 633 | TMNT Tournament Fighter Drumkit SNES | — | polyphone | CC BY | ✓ | — | 16 | game |
| 634 | Uniracers Fixed Soundfont | — | polyphone | CC BY | ✓ | — | 16 | game |
| 635 | Yoshi&#039;s Cookie Drumkit | — | polyphone | CC BY | ✓ | — | 16 | game |
| 636 | Yoshi&#039;s Safari Drumkit | — | polyphone | CC BY | ✓ | — | 16 | game |
| 637 | Yoshi&#039;s Safari V2 Soundfont | — | polyphone | CC BY | ✓ | — | 16 | game |
| 638 | Arkanoid Doh It Again Drumkit | — | polyphone | CC BY | ✓ | — | 15 | game |
| 639 | Battle Grand Prix Soundfont | — | polyphone | CC BY | ✓ | — | 15 | game |
| 640 | Busters On The Loose SNES Soundfont | — | polyphone | CC BY | ✓ | — | 15 | game |
| 641 | Capcom&#039;s MVP Football Instrument Set Soundfont | — | polyphone | CC BY | ✓ | — | 15 | game |
| 642 | Fixed Bebe Kids SNES | — | polyphone | CC BY | ✓ | — | 15 | game |
| 643 | Fixed Joe &amp; Mac 2 Soundfont | — | polyphone | CC BY | ✓ | — | 15 | game |
| 644 | Fixed Pink Panther: Pink Goes to Hollywood SNES Soundfont | — | polyphone | CC BY | ✓ | — | 15 | game |
| 645 | Fixed Side Pocket SNES | — | polyphone | CC BY | ✓ | — | 15 | game |
| 646 | Fixed Super Mario Advance 4 GBA Soundfont | — | polyphone | CC BY | ✓ | — | 15 | game |
| 647 | Fixed The Smurfs (SNES) Soundfont | — | polyphone | CC BY | ✓ | — | 15 | game |
| 648 | Ganbare Goemon 3 SNES Soundfont | — | polyphone | CC BY | ✓ | — | 15 | game |
| 649 | Jyutei Senki Instrument set Soundfont | — | polyphone | CC BY | ✓ | — | 15 | game |
| 650 | Knights of the Round V2 Soundfont | — | polyphone | CC BY | ✓ | — | 15 | game |
| 651 | Lethal Enforcers Drumkit | — | polyphone | CC BY | ✓ | — | 15 | game |
| 652 | Mega Man &amp; Bass GBA Soundfont | — | polyphone | CC BY | ✓ | — | 15 | game |
| 653 | Stunt Race FX Instrument set Soundfont | — | polyphone | CC BY | ✓ | — | 15 | game |
| 654 | TAZ MANIA V2 | — | polyphone | CC BY | ✓ | — | 15 | game |
| 655 | The Ninja Warriors Instrument set Soundfont | — | polyphone | CC BY | ✓ | — | 15 | game |
| 656 | Tiny Toons Wacky Sports Challenge Drumkit | — | polyphone | CC BY | ✓ | — | 15 | game |
| 657 | Vapor Trail Drumkit | — | polyphone | CC BY | ✓ | — | 15 | game |
| 658 | Wappers Souryu Hen Instrument set Soundfont | — | polyphone | CC BY | ✓ | — | 15 | game |
| 659 | World Heroes 2 Instrument set Soundfont | — | polyphone | CC BY | ✓ | — | 15 | game |
| 660 | Capcoms MVP Football V2 Soundfont | — | polyphone | CC BY | ✓ | — | 14 | game |
| 661 | Captain Commando Drumkit | — | polyphone | CC BY | ✓ | — | 14 | game |
| 662 | Captain Commando Instrument set Soundfont | — | polyphone | CC BY | ✓ | — | 14 | game |
| 663 | Fixed Battle Cars Soundfont | — | polyphone | CC BY | ✓ | — | 14 | game |
| 664 | Fixed Daze Before Christmas SNES | — | polyphone | CC BY | ✓ | — | 14 | game |
| 665 | Fixed Kirby: Nightmare in Dream Land GBA Soundfont | — | polyphone | CC BY | ✓ | — | 14 | game |
| 666 | Fixed Lester the Unlikely Soundfont | — | polyphone | CC BY | ✓ | — | 14 | game |
| 667 | Fixed Mortal Kombat SNES Soundfont | — | polyphone | CC BY | ✓ | — | 14 | game |
| 668 | Fixed Power Piggs of the Dark Age Soundfont | — | polyphone | CC BY | ✓ | — | 14 | game |
| 669 | Fixed Power Piggs of the Dark Age Soundfont | — | polyphone | CC BY | ✓ | — | 14 | game |
| 670 | Fixed Spirou Soundfont | — | polyphone | CC BY | ✓ | — | 14 | game |
| 671 | Fixed Super Putty Soundfont | — | polyphone | CC BY | ✓ | — | 14 | game |
| 672 | Fixed Unofficial Super Nintendo Entertainment System Soundfont | — | polyphone | CC BY | ✓ | — | 14 | game |
| 673 | Gun Force Instrument set Soundfont | — | polyphone | CC BY | ✓ | — | 14 | game |
| 674 | John Madden Football V2 Soundfont | — | polyphone | CC BY | ✓ | — | 14 | game |
| 675 | Sega&#039;s FM: Vapor Trail DAC | — | polyphone | CC BY | ✓ | — | 14 | game |
| 676 | Sousa Sentai Wappers 1 Instrument set Soundfont | — | polyphone | CC BY | ✓ | — | 14 | game |
| 677 | Tecmo Super Bowl Drumkit | — | polyphone | CC BY | ✓ | — | 14 | game |
| 678 | World Heroes 2 Drumkit | — | polyphone | CC BY | ✓ | — | 14 | game |
| 679 | Arkaniod Doh It Again Instrument set Soundfont | — | polyphone | CC BY | ✓ | — | 13 | game |
| 680 | Captain Commando V2 Soundfont | — | polyphone | CC BY | ✓ | — | 13 | game |
| 681 | Final Fight 2 Instrument Set Soundfont | — | polyphone | CC BY | ✓ | — | 13 | game |
| 682 | Fixed Bugs Bunny SNES Soundfont | — | polyphone | CC BY | ✓ | — | 13 | game |
| 683 | Fixed John Madden Football &#039;93 (SNES) GM Soundfont | — | polyphone | CC BY | ✓ | — | 13 | game |
| 684 | Fixed PowerRangerSNESV2 | — | polyphone | CC BY | ✓ | — | 13 | game |
| 685 | Fixed U.N. Squadron Soundfont | — | polyphone | CC BY | ✓ | — | 13 | game |
| 686 | Fixed Yoshi&#039;s Cookie SNES Soundfont V2 | — | polyphone | CC BY | ✓ | — | 13 | game |
| 687 | Gokujou Parodius Instrument set Soundfont | — | polyphone | CC BY | ✓ | — | 13 | game |
| 688 | Lethal Enforcers 1 Genesis Version Drumkit with Orchestra Hits | — | polyphone | CC BY | ✓ | — | 13 | game |
| 689 | Panorama Cotton Drumkit | — | polyphone | CC BY | ✓ | — | 13 | game |
| 690 | Sega&#039;s FM: Not Star Light Zone DAC | — | polyphone | CC BY | ✓ | — | 13 | game |
| 691 | Super Tennis Instrument set Soundfont | — | polyphone | CC BY | ✓ | — | 13 | game |
| 692 | Tecmo Secret of The Stars Instrument set Soundfont | — | polyphone | CC BY | ✓ | — | 13 | game |
| 693 | Temco Super Bowl V2 Soundfont | — | polyphone | CC BY | ✓ | — | 13 | game |
| 694 | American Gladiators Instrument set | — | polyphone | CC BY | ✓ | — | 12 | game |
| 695 | Dragon Ball Z SuperSonic Warriors GBA Soundfont | — | polyphone | CC BY | ✓ | — | 12 | game |
| 696 | Final Fantasy IV GBA Soundfont | — | polyphone | CC BY | ✓ | — | 12 | game |
| 697 | Fixed Asterix &amp; Obelix (SNES) Soundfont | — | polyphone | CC BY | ✓ | — | 12 | game |
| 698 | Fixed Gundam Wing - Endless Duel SNES Soundfont | — | polyphone | CC BY | ✓ | — | 12 | game |
| 699 | Fixed Lubub&#039;s SattellaView BS-X WIP SNES Restored Soundfont | — | polyphone | CC BY | ✓ | — | 12 | game |
| 700 | Fixed Mickey no Tokyo Disneyland Daibouken | — | polyphone | CC BY | ✓ | — | 12 | game |
| 701 | Fixed Monopoly SNES Soundfont | — | polyphone | CC BY | ✓ | — | 12 | game |
| 702 | Fixed NHL &#039;94 (SNES) Soundfont | — | polyphone | CC BY | ✓ | — | 12 | game |
| 703 | Fixed Pinocchio SNES Soundfont V2 | — | polyphone | CC BY | ✓ | — | 12 | game |
| 704 | Fixed Star Fox SNES Soundfont | — | polyphone | CC BY | ✓ | — | 12 | game |
| 705 | Fixed Super Bomberman SNES Soundfont | — | polyphone | CC BY | ✓ | — | 12 | game |
| 706 | Fixed Super Castlevania IV SNES Soundfont | — | polyphone | CC BY | ✓ | — | 12 | game |
| 707 | rei leao | — | polyphone | CC BY | ✓ | — | 12 | game |
| 708 | Sega&#039;s FM: Alt Furnace Drums | — | polyphone | CC BY | ✓ | — | 12 | game |
| 709 | SimTunes GM/Internal MIDI Version Mario Paint Template | — | polyphone | CC BY | ✓ | — | 12 | game |
| 710 | Super Play Action Football Instrument set Soundfont | — | polyphone | CC BY | ✓ | — | 12 | game |
| 711 | EEK! The Cat SNES Soundfont | — | polyphone | CC BY | ✓ | — | 11 | game |
| 712 | Fixed Aero the Acro-Bat SNES Soundfont | — | polyphone | CC BY | ✓ | — | 11 | game |
| 713 | Fixed Arkanoid-Doh it Again SNES Soundfont | — | polyphone | CC BY | ✓ | — | 11 | game |
| 714 | Fixed Home Alone SNES Soundfont | — | polyphone | CC BY | ✓ | — | 11 | game |
| 715 | Fixed John Madden Football (SNES) GM Soundfont | — | polyphone | CC BY | ✓ | — | 11 | game |
| 716 | Fixed Lufia and The Fortress of Doom SNES Soundfont | — | polyphone | CC BY | ✓ | — | 11 | game |
| 717 | Fixed Super Bomberman 2 SNES Soundfont | — | polyphone | CC BY | ✓ | — | 11 | game |
| 718 | mulan snes | — | polyphone | CC BY | ✓ | — | 11 | game |
| 719 | World Heroes 2 V2 Soundfont | — | polyphone | CC BY | ✓ | — | 11 | game |
| 720 | Battle Grand Prix Instrument set | — | polyphone | CC BY | ✓ | — | 10 | game |
| 721 | Final Fight 2 Drumkit | — | polyphone | CC BY | ✓ | — | 10 | game |
| 722 | Fixed Faceball 2000 SNES Soundfont | — | polyphone | CC BY | ✓ | — | 10 | game |
| 723 | Fixed Goof Troop SNES Soundfont | — | polyphone | CC BY | ✓ | — | 10 | game |
| 724 | Fixed Kirby &amp; The Amazing Mirror GBA Soundfont | — | polyphone | CC BY | ✓ | — | 10 | game |
| 725 | Fixed Lion King HQ SNES Soundfont | — | polyphone | CC BY | ✓ | — | 10 | game |
| 726 | Fixed Race Drivin SNES Soundfont | — | polyphone | CC BY | ✓ | — | 10 | game |
| 727 | My Version of Super Mario Advance GBA Soundfont | — | polyphone | CC BY | ✓ | — | 10 | game |
| 728 | Double Dragon V SNES Drumkit | — | polyphone | CC BY | ✓ | — | 9 | game |
| 729 | Fixed Bill Walsh College Football (SNES) Soundfont | — | polyphone | CC BY | ✓ | — | 9 | game |
| 730 | Fixed Bobby&#039;s World SNES Soundfont | — | polyphone | CC BY | ✓ | — | 9 | game |
| 731 | Fixed Mighty Morphin Power Rangers - MK. I SNES Soundfont | — | polyphone | CC BY | ✓ | — | 9 | game |
| 732 | Fixed Super Game Boy SNES Soundfont V2 | — | polyphone | CC BY | ✓ | — | 9 | game |
| 733 | Fixed The Mask SNES Soundfont | — | polyphone | CC BY | ✓ | — | 9 | game |
| 734 | Jaleco Rally Big Run The Supreme 4WD Challenge instrument set | — | polyphone | CC BY | ✓ | — | 9 | game |
| 735 | Fixed Batman Returns SNES Soundfont | — | polyphone | CC BY | ✓ | — | 8 | game |
| 736 | Fixed Battletoads &amp; Double Dragon SNES Drumkit | — | polyphone | CC BY | ✓ | — | 8 | game |
| 737 | Fixed Demolition Man SNES Soundfont | — | polyphone | CC BY | ✓ | — | 8 | game |
| 738 | Fixed Home Alone 2 SNES Soundfont | — | polyphone | CC BY | ✓ | — | 8 | game |
| 739 | Fixed Kamen Rider SNES Soundfont | — | polyphone | CC BY | ✓ | — | 8 | game |
| 740 | Fixed Last Action Hero SNES Soundfont | — | polyphone | CC BY | ✓ | — | 8 | game |
| 741 | Fixed Mighty Morphin Power Rangers (and Zeo) - MK II. SNES Soundfont | — | polyphone | CC BY | ✓ | — | 8 | game |
| 742 | Fixed Rocko&#039;s Modern Life - Spunky&#039;s Dangerous Day SNES Soun | — | polyphone | CC BY | ✓ | — | 8 | game |
| 743 | Fixed Super Vails 4 Soundfont | — | polyphone | CC BY | ✓ | — | 8 | game |
| 744 | Justice League Task Force | — | polyphone | CC BY | ✓ | — | 8 | game |
| 745 | Another Soundfont Series: Sonic Advance 3 | — | polyphone | CC BY | ✓ | — | 7 | game |
| 746 | Fixed American Tail SNES Soundfont | — | polyphone | CC BY | ✓ | — | 7 | game |
| 747 | Fixed Bishoujo Janshi Suchie-Pai SNES Soundfont | — | polyphone | CC BY | ✓ | — | 7 | game |
| 748 | Fixed Bonkers SNES Soundfont | — | polyphone | CC BY | ✓ | — | 7 | game |
| 749 | Fixed Looney Tunes B-Ball SNES Soundfont | — | polyphone | CC BY | ✓ | — | 7 | game |
| 750 | Fixed Mario &amp; Wario Soundfont V1 | — | polyphone | CC BY | ✓ | — | 7 | game |
| 751 | Fixed NBA All-Star Challenge SNES Soundfont | — | polyphone | CC BY | ✓ | — | 7 | game |
| 752 | Fixed Sonic Pinball Party GBA Soundfont | — | polyphone | CC BY | ✓ | — | 7 | game |
| 753 | Fixed Super Star Wars 2 - The Empire Strikes Back SNES Soundfont | — | polyphone | CC BY | ✓ | — | 7 | game |
| 754 | Jaleco Rally Big Run The Supreme 4WD Challenge Soundfont | — | polyphone | CC BY | ✓ | — | 7 | game |
| 755 | Fixed Beethoven - The Ultimate Canine Caper SNES Soundfont | — | polyphone | CC BY | ✓ | — | 6 | game |
| 756 | Fixed Car Rager SNES Soundfont V2 | — | polyphone | CC BY | ✓ | — | 6 | game |
| 757 | Fixed Casper SNES Soundfont | — | polyphone | CC BY | ✓ | — | 6 | game |
| 758 | Fixed Dennis the Menace SNES Soundfont | — | polyphone | CC BY | ✓ | — | 6 | game |
| 759 | Fixed Dragon Ball Advanced Adventure GBA Soundfont | — | polyphone | CC BY | ✓ | — | 6 | game |
| 760 | Fixed Final Fantasy Tactics GBA Soundfont | — | polyphone | CC BY | ✓ | — | 6 | game |
| 761 | Fixed Justice League Task Force SNES Soundfont | — | polyphone | CC BY | ✓ | — | 6 | game |
| 762 | Fixed Kawasaki Superbike Challenge SNES Soundfont | — | polyphone | CC BY | ✓ | — | 6 | game |
| 763 | Fixed Lethal Weapon SNES Soundfont | — | polyphone | CC BY | ✓ | — | 6 | game |
| 764 | Fixed Nickelodeon GUTS SNES Soundfont | — | polyphone | CC BY | ✓ | — | 6 | game |
| 765 | Fixed Operation Logic Bomb SNES Soundfont | — | polyphone | CC BY | ✓ | — | 6 | game |
| 766 | Fixed RoboCop 3 SNES Soundfont | — | polyphone | CC BY | ✓ | — | 6 | game |
| 767 | Fixed Street Racer SNES Soundfont | — | polyphone | CC BY | ✓ | — | 6 | game |
| 768 | Fixed Super Star Wars SNES Soundfont | — | polyphone | CC BY | ✓ | — | 6 | game |
| 769 | Fixed Wizard of OZ SNES Soundfont | — | polyphone | CC BY | ✓ | — | 6 | game |
| 770 | My Favorite Sonic GBA instruments | — | polyphone | CC BY | ✓ | — | 6 | game |
| 771 | Double Dragon Advance GBA Soundfont | — | polyphone | CC BY | ✓ | — | 5 | game |
| 772 | eak the cat snes | — | polyphone | CC BY | ✓ | — | 5 | game |
| 773 | Fixed Batman Revenge of the Joker SNES Soundfont | — | polyphone | CC BY | ✓ | — | 5 | game |
| 774 | Fixed Chuck Rock SNES Soundfont | — | polyphone | CC BY | ✓ | — | 5 | game |
| 775 | Fixed Family Feud SNES Soundfont | — | polyphone | CC BY | ✓ | — | 5 | game |
| 776 | Fixed Final Fantasy VI GBA Soundfont | — | polyphone | CC BY | ✓ | — | 5 | game |
| 777 | Fixed Super R-Type SNES Soundfont | — | polyphone | CC BY | ✓ | — | 5 | game |
| 778 | Fixed The Blues Brothers SNES Soundfont | — | polyphone | CC BY | ✓ | — | 5 | game |
| 779 | Fixed The Itchy &amp; Scratchy Game SNES Soundfont | — | polyphone | CC BY | ✓ | — | 5 | game |
| 780 | AHHHH! Real Monsters SNES Soundfont | — | polyphone | CC BY | ✓ | — | 4 | game |
| 781 | Fixed ACME Animation SNES Soundfont | — | polyphone | CC BY | ✓ | — | 4 | game |
| 782 | Fixed Adventures of Yogi Bear  [Yogi Bear&#039;s Cartoon Capers] SNES  | — | polyphone | CC BY | ✓ | — | 4 | game |
| 783 | Fixed Captain America and The Avengers SNES Soundfont | — | polyphone | CC BY | ✓ | — | 4 | game |
| 784 | Fixed Death and Return of Superman SNES Soundfont | — | polyphone | CC BY | ✓ | — | 4 | game |
| 785 | Fixed Spider-Man - Lethal Foes SNES Soundfont | — | polyphone | CC BY | ✓ | — | 4 | game |
| 786 | Fixed Tintin in Tibet (SNES) Soundfont | — | polyphone | CC BY | ✓ | — | 4 | game |
| 787 | Fixed Hanna Barbera&#039;s Turbo Toons SNES Soundfont | — | polyphone | CC BY | ✓ | — | 3 | game |
| 788 | Fixed Lufia The Ruins of Lore GBA Soundfont | — | polyphone | CC BY | ✓ | — | 3 | game |
| 789 | Fixed Mickey&#039;s Ultimate Challenge SNES Soundfont | — | polyphone | CC BY | ✓ | — | 3 | game |
| 790 | Fixed Super Smash TV SNES Soundfont | — | polyphone | CC BY | ✓ | — | 3 | game |
| 791 | Fixed The Addams Family- Pugsley&#039;s Scavenger Hunt SNES Soundfont | — | polyphone | CC BY | ✓ | — | 3 | game |
| 792 | Fixed Advance Wars 2 GBA Soundfont | — | polyphone | CC BY | ✓ | — | 2 | game |
| 793 | Fixed Advance Wars GBA Soundfont | — | polyphone | CC BY | ✓ | — | 2 | game |
| 794 | Fixed Beauty and the Beast SNES Soundfont | — | polyphone | CC BY | ✓ | — | 2 | game |
| 795 | Fixed Donald Duck - Mahou no Boushi SNES Soundfont V2 | — | polyphone | CC BY | ✓ | — | 2 | game |
| 796 | Fixed Final Fantasy V GBA Soundfont | — | polyphone | CC BY | ✓ | — | 2 | game |
| 797 | Fixed The Jetsons SNES Soundfont | — | polyphone | CC BY | ✓ | — | 2 | game |
| 798 | Lethal Weapon snes | — | polyphone | CC BY | ✓ | — | 2 | game |
| 799 | BaritoneSax | sinshu | github | MIT | — | — | — | game |
| 800 | Brightness | sinshu | github | MIT | — | — | — | game |
| 801 | Plants vs. Zombies 2 Complete Soundfont Pack | Peter McConnell, sampled by Ga | musical-artifacts | CC BY 3.0 | ✓ | — | 0 | game |
| 802 | RetroNoises | TheHartCorei5 | musical-artifacts | CC BY 3.0 | — | — | 0 | game |
| 803 | Super Mario 3D Land SF2 (2025/GM Compatible!) | MasonMasterMusic | musical-artifacts | CC BY 3.0 | ✓ | — | 0 | game |
| 804 | touhou | Tseku210 | github | MIT | ✓ | — | — | game |
| 805 | Touhou Phantom Bullet | 白いチャンネル | musical-artifacts | CC BY 3.0 | ✓ | — | 0 | game |
| 806 | Undertale Mettaton plays Eleanor Rigby [The Beatles] | KENNETH UDUT | archive | CC BY 3.0 | — | — | — | game |
| 807 | XXtherobloxx21s Soundfont | XXtherobloxx21 | musical-artifacts | CC BY 3.0 | ✓ | — | 0 | game |
| 808 | MuseScore_General（.sf3 压缩版） | S. Christian Collins | MuseScore | MIT | — | 38.1 MB | — | gm |
| 809 | The Ultimate Roblox Soundfont V1.7 | NotRoblox, SurelyNotRoblox, ro | musical-artifacts | CC BY 3.0 | ✓ | 79.3 MB | 3645 | gm |
| 810 | FluidR3_GM（tar.gz 同内容） | Frank Wen | MuseScore | MIT | ✓ | 124.3 MB | — | gm |
| 811 | SGM Soundfont | SonicLover 19 | musical-artifacts | CC BY 3.0 | ✓ | — | 289628 | gm |
| 812 | The Ultimate Roblox Soundfont Pack V1.8 | NotRoblox | musical-artifacts | CC BY | ✓ | — | 57041 | gm |
| 813 | Nokia S40 3rd Edition (2.04 WIP) | Zenxia | musical-artifacts | CC BY | ✓ | — | 6420 | gm |
| 814 | SGM v2.01 | Shan | polyphone | CC BY | — | — | 5641 | gm |
| 815 | The Ultimate Megadrive Soundfont | The Eighth Bit | polyphone | CC BY | ✓ | — | 3614 | gm |
| 816 | 3D Maze Man (1998) Soundfont | tahutoa | musical-artifacts | CC BY 3.0 | ✓ | — | 1201 | gm |
| 817 | Android Soundfont (Sonivox EAS) | — | polyphone | CC BY | ✓ | — | 1069 | gm |
| 818 | FluidR3 GM | Frank Wen | polyphone | CC BY | ✓ | — | 1067 | gm |
| 819 | Super Mario World (2026 Edition) | — | polyphone | CC BY | ✓ | — | 658 | gm |
| 820 | Samsung Ch@t 222 (GT-E2220) Soundfont | — | polyphone | CC BY | — | — | 653 | gm |
| 821 | Piconica Soundfont | — | polyphone | CC BY | ✓ | — | 578 | gm |
| 822 | LG C365 (MTK6235) Soundfont | — | polyphone | CC BY | — | — | 506 | gm |
| 823 | LG Wink Style T310/Motorola EM28 Soundfont | — | polyphone | CC BY | ✓ | — | 477 | gm |
| 824 | CASIO SK-200 (general midi) | — | polyphone | CC BY | ✓ | — | 445 | gm |
| 825 | Motorola EX115 (Motokey China) Soundfont | — | polyphone | CC BY | ✓ | — | 439 | gm |
| 826 | Blue Picked Bass | — | polyphone | CC BY | ✓ | — | 403 | gm |
| 827 | SuperSponge Soundfont (PS1) Alpha v0.4 | — | polyphone | CC BY | ✓ | — | 327 | gm |
| 828 | KEmulator Soundfont | — | polyphone | CC BY | ✓ | — | 320 | gm |
| 829 | Nokia 3510 MIDI Port + Vibra | — | polyphone | CC BY | ✓ | — | 291 | gm |
| 830 | Mediatek MTK6276 MIDI Port | — | polyphone | CC BY | ✓ | — | 283 | gm |
| 831 | Sonic The Hedgehog (GM Standard) | — | polyphone | CC BY | — | — | 267 | gm |
| 832 | Motorola MotoGO! EX430/EX440 Soundfont | — | polyphone | CC BY | ✓ | — | 201 | gm |
| 833 | RIM Blackberry Pearl 8100 MIDI Port | — | polyphone | CC BY | ✓ | — | 192 | gm |
| 834 | My instruments use in music | — | polyphone | CC BY | — | — | 115 | gm |
| 835 | My Singing Monsters  mobile | — | polyphone | CC BY | ✓ | — | 110 | gm |
| 836 | mario 64 hq | — | polyphone | CC BY | ✓ | — | 107 | gm |
| 837 | Smash Remix | — | polyphone | CC BY | ✓ | — | 107 | gm |
| 838 | sonic generetions ps3 xbox 360 | — | polyphone | CC BY | ✓ | — | 72 | gm |
| 839 | sonic generations | — | polyphone | CC BY | ✓ | — | 52 | gm |
| 840 | homer voice | — | polyphone | CC BY | ✓ | — | 47 | gm |
| 841 | beethoven | — | polyphone | CC BY | ✓ | — | 45 | gm |
| 842 | toy story sega | — | polyphone | CC BY | ✓ | — | 41 | gm |
| 843 | SNESv1.3 Soundfont | — | polyphone | CC BY | ✓ | — | 38 | gm |
| 844 | samples snes | — | polyphone | CC BY | — | — | 36 | gm |
| 845 | disneys toy story snes | — | polyphone | CC BY | ✓ | — | 34 | gm |
| 846 | sonic advence 123 | — | polyphone | CC BY | ✓ | — | 34 | gm |
| 847 | super back to future snes | — | polyphone | CC BY | ✓ | — | 32 | gm |
| 848 | super star wars | — | polyphone | CC BY | ✓ | — | 32 | gm |
| 849 | audio ltd 1 | — | polyphone | CC BY | ✓ | — | 30 | gm |
| 850 | bart&#039;s nightmare snes | — | polyphone | CC BY | ✓ | — | 30 | gm |
| 851 | scooby doo snes | — | polyphone | CC BY | ✓ | — | 29 | gm |
| 852 | The lion king  snes | — | polyphone | CC BY | ✓ | — | 29 | gm |
| 853 | Dragon Ball Z Hyper Dimension | — | polyphone | CC BY | ✓ | — | 28 | gm |
| 854 | the lion king drums | — | polyphone | CC BY | ✓ | — | 28 | gm |
| 855 | demon  crest | — | polyphone | CC BY | ✓ | — | 27 | gm |
| 856 | pinochio 1995 snes | — | polyphone | CC BY | ✓ | — | 26 | gm |
| 857 | HAVEST MOON SNES | — | polyphone | CC BY | ✓ | — | 25 | gm |
| 858 | mortal kombat 1 and mortal kombat 2 | — | polyphone | CC BY | ✓ | — | 25 | gm |
| 859 | Sid Meier&#039;s Civilization | — | polyphone | CC BY | ✓ | — | 25 | gm |
| 860 | the mask | — | polyphone | CC BY | ✓ | — | 25 | gm |
| 861 | tiny toons | — | polyphone | CC BY | ✓ | — | 25 | gm |
| 862 | Prince of persia snes | — | polyphone | CC BY | ✓ | — | 24 | gm |
| 863 | The Flintstones snes | — | polyphone | CC BY | ✓ | — | 24 | gm |
| 864 | sailor moon snes | — | polyphone | CC BY | ✓ | — | 23 | gm |
| 865 | home alone 1991 snes | — | polyphone | CC BY | ✓ | — | 21 | gm |
| 866 | jurassic park 2 snes | — | polyphone | CC BY | ✓ | — | 21 | gm |
| 867 | balls 3d snes | — | polyphone | CC BY | ✓ | — | 20 | gm |
| 868 | Dr._Seuss__The_Cat_in_the_Hat_ gba 2003 | — | polyphone | CC BY | ✓ | — | 20 | gm |
| 869 | home alone 1991 samples snes | — | polyphone | CC BY | — | — | 20 | gm |
| 870 | mine claft 360 | — | polyphone | CC BY | ✓ | — | 20 | gm |
| 871 | Psycho Dream | — | polyphone | CC BY | ✓ | — | 20 | gm |
| 872 | the Wizard of Oz, | — | polyphone | CC BY | ✓ | — | 20 | gm |
| 873 | barbie  super model snes | — | polyphone | CC BY | ✓ | — | 19 | gm |
| 874 | batman forever | — | polyphone | CC BY | ✓ | — | 19 | gm |
| 875 | Dragon Ball Z - Super Butouden 3 | — | polyphone | CC BY | ✓ | — | 19 | gm |
| 876 | lion king | — | polyphone | CC BY | ✓ | — | 19 | gm |
| 877 | magical quest mickey mouse snes | — | polyphone | CC BY | ✓ | — | 19 | gm |
| 878 | Megaman &amp; Bass | — | polyphone | CC BY | ✓ | — | 19 | gm |
| 879 | POWER RANGERS 1994 SNES | — | polyphone | CC BY | ✓ | — | 19 | gm |
| 880 | super man snes | — | polyphone | CC BY | ✓ | — | 19 | gm |
| 881 | dennis the menace | — | polyphone | CC BY | ✓ | — | 18 | gm |
| 882 | Jeopardy | — | polyphone | CC BY | ✓ | — | 18 | gm |
| 883 | jurasic park | — | polyphone | CC BY | ✓ | — | 18 | gm |
| 884 | robots  gba | — | polyphone | CC BY | ✓ | — | 18 | gm |
| 885 | spongebob creature from the krusty krab | — | polyphone | CC BY | ✓ | — | 18 | gm |
| 886 | beauty and beast | — | polyphone | CC BY | ✓ | — | 17 | gm |
| 887 | itchy e scratchy | — | polyphone | CC BY | ✓ | — | 17 | gm |
| 888 | Joe mac 2 | — | polyphone | CC BY | ✓ | — | 17 | gm |
| 889 | lion king hq snes | — | polyphone | CC BY | ✓ | — | 17 | gm |
| 890 | Mickey no Tokyo Disneyland Daibouken (SNES) Soundfont | — | polyphone | CC BY | ✓ | — | 17 | gm |
| 891 | the simpsons gba | — | polyphone | CC BY | ✓ | — | 17 | gm |
| 892 | 102 dalmatas pc | — | polyphone | CC BY | ✓ | — | 16 | gm |
| 893 | animanics snes new version | — | polyphone | CC BY | ✓ | — | 16 | gm |
| 894 | monopoly snes | — | polyphone | CC BY | ✓ | — | 16 | gm |
| 895 | the addams family pugsley&#039;s scavenger hunt | — | polyphone | CC BY | ✓ | — | 16 | gm |
| 896 | Tigger&#039;s Honey Hunt PlayStation | — | polyphone | CC BY | ✓ | — | 16 | gm |
| 897 | Nobunaga&#039;s Ambition | — | polyphone | CC BY | ✓ | — | 15 | gm |
| 898 | power rangers zeo | — | polyphone | CC BY | ✓ | — | 15 | gm |
| 899 | Rocko&#039;s Modern Life - Spunky&#039;s Dangerous Day | — | polyphone | CC BY | ✓ | — | 15 | gm |
| 900 | sony snes 700 | — | polyphone | CC BY | ✓ | — | 15 | gm |
| 901 | the addans family snes | — | polyphone | CC BY | ✓ | — | 15 | gm |
| 902 | the smufs snes | — | polyphone | CC BY | ✓ | — | 15 | gm |
| 903 | FUNAKI_KUNIO | — | polyphone | CC BY | ✓ | — | 14 | gm |
| 904 | lufia the fortress of doom | — | polyphone | CC BY | ✓ | — | 14 | gm |
| 905 | mortal kombat 3 snes | — | polyphone | CC BY | ✓ | — | 14 | gm |
| 906 | road runner | — | polyphone | CC BY | ✓ | — | 14 | gm |
| 907 | super bomberman 3 | — | polyphone | CC BY | ✓ | — | 14 | gm |
| 908 | the adams family values snes | — | polyphone | CC BY | ✓ | — | 14 | gm |
| 909 | CAR RAGER SNES | — | polyphone | CC BY | ✓ | — | 13 | gm |
| 910 | Nicktoons: Globs of Doom | — | polyphone | CC BY | ✓ | — | 13 | gm |
| 911 | Parodius - Non-Sense Fantasy / Parodius Da! - Shinwa kara Owarai he | — | polyphone | CC BY | ✓ | — | 13 | gm |
| 912 | pinochio 1995  samples | — | polyphone | CC BY | — | — | 13 | gm |
| 913 | tom e jerry snes | — | polyphone | CC BY | ✓ | — | 13 | gm |
| 914 | bubsy 2 snes | — | polyphone | CC BY | ✓ | — | 12 | gm |
| 915 | equinox snes | — | polyphone | CC BY | ✓ | — | 12 | gm |
| 916 | flushed away gba | — | polyphone | CC BY | ✓ | — | 12 | gm |
| 917 | home alone 2  lost in new york snes | — | polyphone | CC BY | ✓ | — | 12 | gm |
| 918 | jurasic park snes | — | polyphone | CC BY | ✓ | — | 12 | gm |
| 919 | Ranma 1/2: Treasure of the Red Cat Gang | — | polyphone | CC BY | ✓ | — | 12 | gm |
| 920 | 102 dalmatas psx | — | polyphone | CC BY | ✓ | — | 11 | gm |
| 921 | american tail | — | polyphone | CC BY | ✓ | — | 11 | gm |
| 922 | chuck rock snes | — | polyphone | CC BY | ✓ | — | 11 | gm |
| 923 | mega man 7 hq | — | polyphone | CC BY | ✓ | — | 11 | gm |
| 924 | scooby doo 2 gba | — | polyphone | CC BY | ✓ | — | 11 | gm |
| 925 | sonic adventure | — | polyphone | CC BY | ✓ | — | 11 | gm |
| 926 | Chester Cheetah: Too Cool to Fool | — | polyphone | CC BY | ✓ | — | 10 | gm |
| 927 | drum kit ninja gaden snes | — | polyphone | CC BY | ✓ | — | 10 | gm |
| 928 | fifa soccer 97 | — | polyphone | CC BY | ✓ | — | 10 | gm |
| 929 | Joe and mac 2 | — | polyphone | CC BY | ✓ | — | 10 | gm |
| 930 | ninja gander snes | — | polyphone | CC BY | ✓ | — | 10 | gm |
| 931 | Race Drivin | — | polyphone | CC BY | ✓ | — | 10 | gm |
| 932 | shrek orgers and donkeys | — | polyphone | CC BY | ✓ | — | 10 | gm |
| 933 | the Blues Brothers snes | — | polyphone | CC BY | ✓ | — | 10 | gm |
| 934 | the penguins of madagascar ds | — | polyphone | CC BY | ✓ | — | 10 | gm |
| 935 | wwf | — | polyphone | CC BY | ✓ | — | 10 | gm |
| 936 | barbie super model | — | polyphone | CC BY | ✓ | — | 9 | gm |
| 937 | Bobby&#039;s World | — | polyphone | CC BY | ✓ | — | 9 | gm |
| 938 | madagascar ds | — | polyphone | CC BY | ✓ | — | 9 | gm |
| 939 | shrek carnival | — | polyphone | CC BY | ✓ | — | 9 | gm |
| 940 | Super R-Type snes | — | polyphone | CC BY | ✓ | — | 9 | gm |
| 941 | Tetsuwan Atom  snes | — | polyphone | CC BY | ✓ | — | 9 | gm |
| 942 | Beethoven - The Ultimate Canine Caper | — | polyphone | CC BY | ✓ | — | 8 | gm |
| 943 | Bonkers snes | — | polyphone | CC BY | ✓ | — | 8 | gm |
| 944 | cogumelo | — | polyphone | CC BY | ✓ | — | 8 | gm |
| 945 | power piggs snes | — | polyphone | CC BY | ✓ | — | 8 | gm |
| 946 | shrek forever | — | polyphone | CC BY | ✓ | — | 8 | gm |
| 947 | super bomber man 1  and 2 | — | polyphone | CC BY | — | — | 8 | gm |
| 948 | buggs bunny snes | — | polyphone | CC BY | ✓ | — | 7 | gm |
| 949 | goofy troop snes | — | polyphone | CC BY | ✓ | — | 7 | gm |
| 950 | Gundam Wing - Endless Duel snes | — | polyphone | CC BY | ✓ | — | 7 | gm |
| 951 | madagascar | — | polyphone | CC BY | ✓ | — | 7 | gm |
| 952 | Operation Logic Bomb | — | polyphone | CC BY | ✓ | — | 7 | gm |
| 953 | Pinocchio snes version 2 | — | polyphone | CC BY | ✓ | — | 7 | gm |
| 954 | Scooby doo 2 gba | — | polyphone | CC BY | ✓ | — | 7 | gm |
| 955 | shrek smash | — | polyphone | CC BY | ✓ | — | 7 | gm |
| 956 | shrek thild | — | polyphone | CC BY | ✓ | — | 7 | gm |
| 957 | Sonic GBA Collection | — | polyphone | CC BY | ✓ | — | 7 | gm |
| 958 | super man snes | — | polyphone | CC BY | ✓ | — | 7 | gm |
| 959 | the adams family snes 1991 | — | polyphone | CC BY | ✓ | — | 7 | gm |
| 960 | toy story snes new version | — | polyphone | CC BY | ✓ | — | 7 | gm |
| 961 | yoshi cookie snes | — | polyphone | CC BY | ✓ | — | 7 | gm |
| 962 | ahhhh real monsters snes | — | polyphone | CC BY | ✓ | — | 6 | gm |
| 963 | Bishoujo Janshi Suchie-Pai | — | polyphone | CC BY | ✓ | — | 6 | gm |
| 964 | Dennis the Menace snes | — | polyphone | CC BY | ✓ | — | 6 | gm |
| 965 | looney tunes b ball snes | — | polyphone | CC BY | ✓ | — | 6 | gm |
| 966 | the smurfs | — | polyphone | CC BY | ✓ | — | 6 | gm |
| 967 | Addams Family, The - Pugsley&#039;s Scavenger Hunt snes | — | polyphone | CC BY | ✓ | — | 5 | gm |
| 968 | Aero the Acro-Bat SNES | — | polyphone | CC BY | ✓ | — | 5 | gm |
| 969 | batman returns snes | — | polyphone | CC BY | ✓ | — | 5 | gm |
| 970 | Demolition Man | — | polyphone | CC BY | ✓ | — | 5 | gm |
| 971 | faceball 2000 | — | polyphone | CC BY | ✓ | — | 5 | gm |
| 972 | home alone 1991 | — | polyphone | CC BY | ✓ | — | 5 | gm |
| 973 | street racer snes | — | polyphone | CC BY | ✓ | — | 5 | gm |
| 974 | Super Star Wars 2 - The Empire Strikes Back | — | polyphone | CC BY | ✓ | — | 5 | gm |
| 975 | yoshi safari | — | polyphone | CC BY | ✓ | — | 5 | gm |
| 976 | kawasaki superbike challeng snes | — | polyphone | CC BY | ✓ | — | 4 | gm |
| 977 | popeye snes | — | polyphone | CC BY | ✓ | — | 4 | gm |
| 978 | super smash tv snes | — | polyphone | CC BY | ✓ | — | 4 | gm |
| 979 | super star wars  snes | — | polyphone | CC BY | ✓ | — | 4 | gm |
| 980 | the mask snes 1994 | — | polyphone | CC BY | ✓ | — | 4 | gm |
| 981 | ACME Animation Factory snes | — | polyphone | CC BY | ✓ | — | 3 | gm |
| 982 | Adventures of Yogi Bear  [Yogi Bear&#039;s Cartoon Capers snes | — | polyphone | CC BY | ✓ | — | 3 | gm |
| 983 | casper snes 1996 | — | polyphone | CC BY | ✓ | — | 3 | gm |
| 984 | donald duck no mahou no boushi v2 | — | polyphone | CC BY | ✓ | — | 3 | gm |
| 985 | family feud snes | — | polyphone | CC BY | ✓ | — | 3 | gm |
| 986 | Jungle Book, snes | — | polyphone | CC BY | ✓ | — | 3 | gm |
| 987 | Mickey&#039;s Ultimate Challenge snes | — | polyphone | CC BY | ✓ | — | 3 | gm |
| 988 | Nickelodeon GUTS snes | — | polyphone | CC BY | ✓ | — | 3 | gm |
| 989 | robocop 3 | — | polyphone | CC BY | ✓ | — | 3 | gm |
| 990 | Spider-Man - Lethal Foes snes | — | polyphone | CC BY | ✓ | — | 3 | gm |
| 991 | the jetsons snes | — | polyphone | CC BY | ✓ | — | 3 | gm |
| 992 | american tail snes | — | polyphone | CC BY | ✓ | — | 2 | gm |
| 993 | batman revenge of the joker snes | — | polyphone | CC BY | ✓ | — | 2 | gm |
| 994 | car rager new version | — | polyphone | CC BY | ✓ | — | 2 | gm |
| 995 | Hanna Barbera&#039;s Turbo Toons snes | — | polyphone | CC BY | ✓ | — | 2 | gm |
| 996 | kamen rider snes | — | polyphone | CC BY | ✓ | — | 2 | gm |
| 997 | Last Action Hero snes | — | polyphone | CC BY | ✓ | — | 2 | gm |
| 998 | NBA All-Star Challenge  snes | — | polyphone | CC BY | ✓ | — | 2 | gm |
| 999 | Aladdin gba | — | polyphone | CC BY | — | — | 1 | gm |
| 1000 | captain america and the avengers | — | polyphone | CC BY | ✓ | — | 1 | gm |
| 1001 | Death and Return of Superman,  snes | — | polyphone | CC BY | ✓ | — | 1 | gm |
| 1002 | Tintin in Tibet (SNES) | — | polyphone | CC BY | ✓ | — | 1 | gm |
| 1003 | Hpcarl Jupiter 2 | Hpcarl | musical-artifacts | CC BY | ✓ | — | 0 | gm |
| 1004 | Bass | gregogiudici | github | MIT | ✓ | 2.3 MB | — | guitar |
| 1005 | FDL Bass | FDLBricks | musical-artifacts | CC BY | ✓ | 3.8 MB | 576 | guitar |
| 1006 | Deep Bass (based on pasta bass) | j_e_f_f_g | musical-artifacts | CC BY | — | 9.8 MB | 3411 | guitar |
| 1007 | Fender Squire Bass | Bill Brown | musical-artifacts | CC BY | ✓ | — | 6209 | guitar |
| 1008 | Fender Knockoff Strat | Bill Brown | musical-artifacts | CC BY | ✓ | — | 5423 | guitar |
| 1009 | Studio FG460s II Pro Guitar Pack | Mitrofanis George Gemitros | polyphone | CC BY | ✓ | — | 4039 | guitar |
| 1010 | Buddy Holly Riff | XXtherobloxx21 | musical-artifacts | CC BY 3.0 | ✓ | — | 2324 | guitar |
| 1011 | Custom Classical Guitar | — | polyphone | CC BY | ✓ | — | 1008 | guitar |
| 1012 | Blue Acoustic Bass | — | polyphone | CC BY | ✓ | — | 741 | guitar |
| 1013 | Primeira Soundfont de violão básico | — | polyphone | CC BY | ✓ | — | 652 | guitar |
| 1014 | OverDrived Guitar | — | polyphone | CC BY | ✓ | — | 622 | guitar |
| 1015 | Emperador 12 String Gtr Demo | — | polyphone | CC BY | ✓ | — | 363 | guitar |
| 1016 | Flight bass | Breity | polyphone | CC BY | ✓ | — | 326 | guitar |
| 1017 | Baton Harmonics | — | polyphone | CC BY | — | — | 297 | guitar |
| 1018 | Ghost Strumming | — | polyphone | CC BY | ✓ | — | 265 | guitar |
| 1019 | Tremolo bass | Breity | polyphone | CC BY | ✓ | — | 223 | guitar |
| 1020 | Blue Jeans And Moonbeams | Malaclypse the Younger | sfzinstruments | MIT | — | — | — | guitar |
| 1021 | Kalimbass | Malaclypse the Younger | sfzinstruments | MIT | — | — | — | guitar |
| 1022 | Slap Bass | gregogiudici | github | MIT | ✓ | — | — | guitar |
| 1023 | RolandNicePiano | bradhowes | github | MIT | ✓ | 6.2 MB | — | hist |
| 1024 | RolandNicePiano | bradhowes | github | MIT | ✓ | 6.2 MB | — | hist |
| 1025 | Casio Privia PX-860 Concert Grand Piano | Casio, sampled by Caed | musical-artifacts | CC BY 3.0 | ✓ | 32.3 MB | 7846 | hist |
| 1026 | The 90-2000's Famous House Kit | Aleksandr Bykov, other | musical-artifacts | CC BY 3.0 | — | 157.0 MB | 3836 | hist |
| 1027 | Classic Dream House, Trance Kit | Aleksandr Bykov, other | musical-artifacts | CC BY 3.0 | — | 175.3 MB | 2556 | hist |
| 1028 | Kurzweil K2000 Stereo Grand (Soundfont) | The GP | musical-artifacts | CC BY 3.0 | ✓ | — | 22903 | hist |
| 1029 | Kurzweil K2000 Acous 12 Strings (Soundfont) | The GP | musical-artifacts | CC BY 3.0 | ✓ | — | 14717 | hist |
| 1030 | Yamaha C3 Grand Piano | Ctech2021 | musical-artifacts | CC BY 3.0 | ✓ | — | 13227 | hist |
| 1031 | Live HQ Natural SoundFont GM V3.0 | UnderxPipe1985 | musical-artifacts | CC BY | — | — | 12693 | hist |
| 1032 | St. GIGA's HQ FM General MIDI Set | stgiga/stgiga | musical-artifacts | CC BY | ✓ | — | 12031 | hist |
| 1033 | Kurzweil K2000 Steel String Guitar (Soundfont) | The GP | musical-artifacts | CC BY 3.0 | ✓ | — | 12020 | hist |
| 1034 | Roland MV-30 (SC-55 Version) | MAG2001 | musical-artifacts | CC BY 3.0 | ✓ | — | 9291 | hist |
| 1035 | YAMAHA SHS-10 + YM2413 (GM mapped) | stgiga, NESMaster96, little-sc | musical-artifacts | CC BY 3.0 | ✓ | — | 8663 | hist |
| 1036 | E3Kay's Roland Juno-60 Soundfont v2.0 | E3Kay | musical-artifacts | CC BY 3.0 | ✓ | — | 8556 | hist |
| 1037 | Kurzweil K2000 Brite Piano (Soundfont) | The GP | musical-artifacts | CC BY 3.0 | ✓ | — | 8432 | hist |
| 1038 | FPD98 | Dekyo Ongen | musical-artifacts | CC BY | ✓ | — | 7686 | hist |
| 1039 | Chaos V20 Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 6327 | hist |
| 1040 | Kurzweil K2000 Tine Elec Piano (673Mb Soundfont) | The GP | musical-artifacts | CC BY 3.0 | ✓ | — | 5885 | hist |
| 1041 | Proteus 2 - orchestral | E-mu Sound Central | polyphone | CC BY | ✓ | — | 5072 | hist |
| 1042 | Yamaha MA2 fm soundfont | Yamaha | musical-artifacts | CC BY 3.0 | ✓ | — | 4926 | hist |
| 1043 | Reality GM/GS FalcoMod | FalcoMod | musical-artifacts | CC BY 3.0 | ✓ | — | 4732 | hist |
| 1044 | Kurzweil K2000 All In The Fader (704Mb Soundfont) | The GP | musical-artifacts | CC BY 3.0 | — | — | 4530 | hist |
| 1045 | Caed’s Trash GMGS Version 1.1 | Caed | musical-artifacts | CC BY 3.0 | ✓ | — | 4440 | hist |
| 1046 | Kurzweil K2000 Dual Elec Piano (Rhodes 680Mb Soundfont) | The GP | musical-artifacts | CC BY 3.0 | — | — | 4360 | hist |
| 1047 | Yamaha YM2612 GM Standard Soundfont | — | polyphone | CC BY | — | — | 3689 | hist |
| 1048 | - | eeeeeeee | musical-artifacts | CC BY 3.0 | ✓ | — | 3458 | hist |
| 1049 | YAMAHA SHS-10 + YM2413 (GM mapped Redesigned) | stgiga, NESMaster96, little-sc | musical-artifacts | CC BY 3.0 | ✓ | — | 3264 | hist |
| 1050 | YM2612 SMPS Brass Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 3044 | hist |
| 1051 | Yamaha CFX Grand Piano | — | polyphone | CC BY | — | — | 2405 | hist |
| 1052 | 91 Slow Chorus Guitar | Username_Tony | musical-artifacts | CC BY 3.0 | ✓ | — | 2351 | hist |
| 1053 | Proteus 1 - pop/rock | E-mu Sound Central | polyphone | CC BY | ✓ | — | 2130 | hist |
| 1054 | E3Kay's Roland Juno-60 Soundfont | E3Kay | musical-artifacts | CC BY 3.0 | ✓ | — | 1962 | hist |
| 1055 | Ensoniq ESQ-1 Fantabell | Ensoniq | musical-artifacts | CC BY | ✓ | — | 1874 | hist |
| 1056 | Industrial set | E-mu Sound Central | polyphone | CC BY | ✓ | — | 1852 | hist |
| 1057 | Jazz kit | E-mu Sound Central | polyphone | CC BY | ✓ | — | 1782 | hist |
| 1058 | Metal Drums | E-mu Sound Central | polyphone | CC BY | ✓ | — | 1653 | hist |
| 1059 | Proteus 3 - world | E-mu Sound Central | polyphone | CC BY | ✓ | — | 1512 | hist |
| 1060 | Vintage Keys | E-mu Sound Central | polyphone | CC BY | ✓ | — | 1413 | hist |
| 1061 | Acoustic guitars | E-mu Sound Central | polyphone | CC BY | ✓ | — | 1411 | hist |
| 1062 | Orchestral Battery | E-mu Sound Central | polyphone | CC BY | ✓ | — | 1411 | hist |
| 1063 | Korg M1 HipHop Bass Soundfont | Mildanner, KORG | musical-artifacts | CC BY 3.0 | ✓ | — | 1353 | hist |
| 1064 | Indian ensemble | E-mu Sound Central | polyphone | CC BY | ✓ | — | 1299 | hist |
| 1065 | Korg Triton Sax Ensemble Soundfont | Mildanner, KORG | musical-artifacts | CC BY 3.0 | ✓ | — | 1260 | hist |
| 1066 | Korg Triton 30303 Mega Bass Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 1242 | hist |
| 1067 | Korg Triton Acoustic Piano Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 1232 | hist |
| 1068 | Caed’s Trash GMGS Version 1 | Caed | musical-artifacts | CC BY 3.0 | — | — | 1165 | hist |
| 1069 | Latin Hand Percussion | E-mu Sound Central | polyphone | CC BY | ✓ | — | 1147 | hist |
| 1070 | Woodwinds | E-mu Sound Central | polyphone | CC BY | ✓ | — | 1114 | hist |
| 1071 | Windows MIDI Converted to SF2 | — | polyphone | CC BY | ✓ | — | 1092 | hist |
| 1072 | Vox &amp; Voice | E-mu Sound Central | polyphone | CC BY | ✓ | — | 1079 | hist |
| 1073 | Korg Triton Strings Ensemble Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 1070 | hist |
| 1074 | Korg Triton Euro 8va Bass Soundfont | Mildanner, KORG | musical-artifacts | CC BY 3.0 | ✓ | — | 1001 | hist |
| 1075 | Emu funky guitars | E-mu Sound Central | polyphone | CC BY | ✓ | — | 989 | hist |
| 1076 | Worldvox | E-mu Sound Central | polyphone | CC BY | ✓ | — | 886 | hist |
| 1077 | Latin Drums Large | E-mu Sound Central | polyphone | CC BY | ✓ | — | 825 | hist |
| 1078 | World combo | E-mu Sound Central | polyphone | CC BY | ✓ | — | 803 | hist |
| 1079 | Gtr Chords &amp; Licks | E-mu Sound Central | polyphone | CC BY | ✓ | — | 797 | hist |
| 1080 | Dance organs | E-mu Sound Central | polyphone | CC BY | ✓ | — | 781 | hist |
| 1081 | Arco Strings | E-mu Sound Central | polyphone | CC BY | ✓ | — | 745 | hist |
| 1082 | Clavinet | E-mu Sound Central | polyphone | CC BY | ✓ | — | 709 | hist |
| 1083 | NitroShoe&#039;s lightweight Roland SC-55 soundfont | — | polyphone | CC BY | ✓ | — | 643 | hist |
| 1084 | Acoustic kits 1-4 | E-mu Sound Central | polyphone | CC BY | ✓ | — | 619 | hist |
| 1085 | Fire - World Instruments | E-mu Sound Central | polyphone | CC BY | ✓ | — | 609 | hist |
| 1086 | Korg Triton Spiky & Tight Instrument Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 601 | hist |
| 1087 | Marcato strings | E-mu Sound Central | polyphone | CC BY | ✓ | — | 561 | hist |
| 1088 | Phatt kit | E-mu Sound Central | polyphone | CC BY | ✓ | — | 555 | hist |
| 1089 | Phatt Beats 113-123bpm | E-mu Sound Central | polyphone | CC BY | ✓ | — | 549 | hist |
| 1090 | Orchestral | E-mu Sound Central | polyphone | CC BY | ✓ | — | 541 | hist |
| 1091 | Bowed psaltery | E-mu Sound Central | polyphone | CC BY | ✓ | — | 508 | hist |
| 1092 | Church combo | E-mu Sound Central | polyphone | CC BY | ✓ | — | 505 | hist |
| 1093 | Exotic harp | E-mu Sound Central | polyphone | CC BY | ✓ | — | 505 | hist |
| 1094 | Musical Effects | E-mu Sound Central | polyphone | CC BY | ✓ | — | 478 | hist |
| 1095 | Vinyl | E-mu Sound Central | polyphone | CC BY | ✓ | — | 466 | hist |
| 1096 | Techno combo | E-mu Sound Central | polyphone | CC BY | ✓ | — | 444 | hist |
| 1097 | Realms | E-mu Sound Central | polyphone | CC BY | ✓ | — | 441 | hist |
| 1098 | Robotnik's theme (AoSTH) synth soundfont | CloudyJolt | musical-artifacts | CC BY 3.0 | ✓ | — | 439 | hist |
| 1099 | Hip hop combo | E-mu Sound Central | polyphone | CC BY | ✓ | — | 435 | hist |
| 1100 | E-mu bass | E-mu Sound Central | polyphone | CC BY | ✓ | — | 431 | hist |
| 1101 | Techno Kit | E-mu Sound Central | polyphone | CC BY | ✓ | — | 415 | hist |
| 1102 | FluidR CC mod | — | polyphone | CC BY | — | — | 409 | hist |
| 1103 | Korg Triton Rock Organ Soundfont | Mildanner, KORG | musical-artifacts | CC BY 3.0 | ✓ | — | 402 | hist |
| 1104 | Guitar effects | E-mu Sound Central | polyphone | CC BY | ✓ | — | 397 | hist |
| 1105 | BFDI GMGS Soundfont | — | polyphone | CC BY | ✓ | — | 389 | hist |
| 1106 | Snares 2 | E-mu Sound Central | polyphone | CC BY | ✓ | — | 344 | hist |
| 1107 | Blade runner | E-mu Sound Central | polyphone | CC BY | ✓ | — | 341 | hist |
| 1108 | Planet Phatt Examples | E-mu Sound Central | polyphone | CC BY | ✓ | — | 335 | hist |
| 1109 | Toms 2 | E-mu Sound Central | polyphone | CC BY | ✓ | — | 333 | hist |
| 1110 | Trance | E-mu Sound Central | polyphone | CC BY | ✓ | — | 316 | hist |
| 1111 | Kit 07-10 | E-mu Sound Central | polyphone | CC BY | ✓ | — | 249 | hist |
| 1112 | Evolver | E-mu Sound Central | polyphone | CC BY | ✓ | — | 248 | hist |
| 1113 | Out Back | E-mu Sound Central | polyphone | CC BY | ✓ | — | 245 | hist |
| 1114 | Wicked Hits | E-mu Sound Central | polyphone | CC BY | ✓ | — | 225 | hist |
| 1115 | Passing Jet | E-mu Sound Central | polyphone | CC BY | ✓ | — | 209 | hist |
| 1116 | XXtherob-malik-dan GM 2.0 | XXtherobloxx21, CupheadKrasueH | musical-artifacts | CC BY | ✓ | — | 179 | hist |
| 1117 | Tinpots Piano V3 | — | polyphone | CC BY | — | — | 163 | hist |
| 1118 | Skids Away | E-mu Sound Central | polyphone | CC BY | ✓ | — | 155 | hist |
| 1119 | Playersounds Compiled &#039;23 | — | polyphone | CC BY | — | — | 143 | hist |
| 1120 | toy story | — | polyphone | CC BY | ✓ | — | 51 | hist |
| 1121 | Arkanoid - Doh It Again | — | polyphone | CC BY | ✓ | — | 9 | hist |
| 1122 | Roland Disney Soundfont | XXtherobloxx21, Disney | musical-artifacts | CC BY 3.0 | — | — | 0 | hist |
| 1123 | The 90's Dreams II (599Mb Soundfont Collection) | Aleksandr Bykov, The GP and ot | musical-artifacts | CC BY 3.0 | — | — | 0 | hist |
| 1124 | harmonium | ledlaux | github | MIT | ✓ | 6.3 MB | — | orch |
| 1125 | Ixox Flute | Xavier Hosxe | sfzinstruments | CC BY 4.0 | — | 10.7 MB | — | orch |
| 1126 | MTG Solo Sax | Music Technology Group (MTG) | sfzinstruments | CC BY 4.0 | — | 110.0 MB | — | orch |
| 1127 | Musescore General HQ Soundfont (.sf2 Converted) | Frank Wen, Michael Cowgill, S. | musical-artifacts | CC BY 3.0 | ✓ | — | 21853 | orch |
| 1128 | Tin Whistle | misc | musical-artifacts | CC BY | ✓ | — | 3599 | orch |
| 1129 | Westgate Studios - Trumpets | Timothy Smith | polyphone | CC BY | ✓ | — | 2582 | orch |
| 1130 | Papelmedia Final SF2 XXL - Strings | Simon Tristan Papel | polyphone | CC BY | ✓ | — | 2371 | orch |
| 1131 | Papelmedia Final SF2 XXL - Trumpet | Simon Tristan Papel | polyphone | CC BY | ✓ | — | 1945 | orch |
| 1132 | Hades strings | Hades | polyphone | CC BY | — | — | 1771 | orch |
| 1133 | Papelmedia Flute | Simon Tristan Papel | polyphone | CC BY | ✓ | — | 1738 | orch |
| 1134 | Mellotron 02 Soundfont | Mildanner, Image-Line | musical-artifacts | CC BY 3.0 | ✓ | — | 1391 | orch |
| 1135 | Celtic harp | Jason Sommerlad | polyphone | CC BY | — | — | 1236 | orch |
| 1136 | Papelmedia Final SF2 XXL - Trombone | Simon Tristan Papel | polyphone | CC BY | ✓ | — | 1197 | orch |
| 1137 | Cello solo | Ethan Winer | polyphone | CC BY | ✓ | — | 1191 | orch |
| 1138 | E-MU Proteus 2000: T-Sax | — | polyphone | CC BY | ✓ | — | 995 | orch |
| 1139 | Celtic Harp [Haug Harp] SoundFont | — | polyphone | CC BY | ✓ | — | 828 | orch |
| 1140 | Strings DXS Super Orchestra | Xiaosu Du | polyphone | CC BY | ✓ | — | 799 | orch |
| 1141 | String EFX | Mick Gordon | polyphone | CC BY | ✓ | — | 780 | orch |
| 1142 | Orchestral brass effects | Project SAM | polyphone | CC BY | ✓ | — | 754 | orch |
| 1143 | Piccolo | Yuri Smolyakov | polyphone | CC BY | ✓ | — | 671 | orch |
| 1144 | Darro 2017 Duduk | — | polyphone | CC BY | — | — | 659 | orch |
| 1145 | Papelmedia String Ensemble | Simon Tristan Papel | polyphone | CC BY | ✓ | — | 659 | orch |
| 1146 | Ensemble Pad - Econo | J. Talbert | polyphone | CC BY | ✓ | — | 627 | orch |
| 1147 | Bamboo alto flute | — | polyphone | CC BY | ✓ | — | 593 | orch |
| 1148 | Strings Legato Korg Triton | Mazurov Roman | polyphone | CC BY | ✓ | — | 592 | orch |
| 1149 | Suspense strings | Mark Semple | polyphone | CC BY | ✓ | — | 581 | orch |
| 1150 | Harp Strings | — | polyphone | CC BY | ✓ | — | 565 | orch |
| 1151 | Papelmedia Trombone Stac | Simon Tristan Papel | polyphone | CC BY | ✓ | — | 562 | orch |
| 1152 | HS Strings | Thomas Hammer | polyphone | CC BY | ✓ | — | 540 | orch |
| 1153 | Cello Karoryfer | — | polyphone | CC BY | ✓ | — | 496 | orch |
| 1154 | Zither eco | ? | polyphone | CC BY | ✓ | — | 464 | orch |
| 1155 | Beakman Orchestral Hit Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 444 | orch |
| 1156 | Kalimba | — | polyphone | CC BY | ✓ | — | 397 | orch |
| 1157 | 056 Florestan Trumpet metallic | Nando Florestan | polyphone | CC BY | ✓ | — | 330 | orch |
| 1158 | Strings DXS Super Pizz | Xiaosu Du | polyphone | CC BY | ✓ | — | 329 | orch |
| 1159 | Tarka | — | polyphone | CC BY | ✓ | — | 262 | orch |
| 1160 | DoubleBassSmolken | — | polyphone | CC BY | — | — | 244 | orch |
| 1161 | Zither - Anton Kiendl | — | polyphone | CC BY | ✓ | — | 188 | orch |
| 1162 | Kuiisi / Flauta  de la etnia Kogi | — | polyphone | CC BY | ✓ | — | 181 | orch |
| 1163 | Rave Mbyá | — | polyphone | CC BY | ✓ | — | 169 | orch |
| 1164 | Damon&#039;s Hits | — | polyphone | CC BY | ✓ | — | 166 | orch |
| 1165 | Early Woodwinds (Demo) | — | polyphone | CC BY | ✓ | — | 146 | orch |
| 1166 | Recorder Stereo | — | polyphone | CC BY | ✓ | — | 109 | orch |
| 1167 | Moxeño | — | polyphone | CC BY | — | — | 106 | orch |
| 1168 | Siebenhüner&#039;s Konzertzither | — | polyphone | CC BY | ✓ | — | 105 | orch |
| 1169 | Lethal Enforcers Drum and Orchestra Hit 1 &amp; 2 | — | polyphone | CC BY | ✓ | — | 30 | orch |
| 1170 | Brass1 | sinshu | github | MIT | — | — | — | orch |
| 1171 | Cello | sinshu | github | MIT | — | — | — | orch |
| 1172 | EnglishHorn | sinshu | github | MIT | — | — | — | orch |
| 1173 | Flute | sinshu | github | MIT | — | — | — | orch |
| 1174 | FrenchHorns | sinshu | github | MIT | — | — | — | orch |
| 1175 | MuteTrumpet | sinshu | github | MIT | — | — | — | orch |
| 1176 | Oboe | sinshu | github | MIT | — | — | — | orch |
| 1177 | Orchestra | sinshu | github | MIT | — | — | — | orch |
| 1178 | OrchestraHit | sinshu | github | MIT | — | — | — | orch |
| 1179 | PanFlute | sinshu | github | MIT | — | — | — | orch |
| 1180 | Party Pipes | Malaclypse the Younger | sfzinstruments | MIT | — | — | — | orch |
| 1181 | SlowStrings | sinshu | github | MIT | — | — | — | orch |
| 1182 | Strings | sinshu | github | MIT | — | — | — | orch |
| 1183 | Sunset Brassh | Hsjszu | archive | CC BY 4.0 | — | — | — | orch |
| 1184 | SynthBrass1 | sinshu | github | MIT | — | — | — | orch |
| 1185 | SynthBrass2 | sinshu | github | MIT | — | — | — | orch |
| 1186 | SynthStrings1 | sinshu | github | MIT | — | — | — | orch |
| 1187 | SynthStrings2 | sinshu | github | MIT | — | — | — | orch |
| 1188 | Trumpet | sinshu | github | MIT | — | — | — | orch |
| 1189 | Violin | sinshu | github | MIT | — | — | — | orch |
| 1190 | &#039;Decrescendo&#039; Pump Organ | — | polyphone | CC BY | ✓ | — | 678 | organ |
| 1191 | Magnificent Gothic 2 | Eisenstoeck / Kranjec | polyphone | CC BY | ✓ | — | 575 | organ |
| 1192 | The dutch electric | — | polyphone | CC BY | ✓ | — | 439 | organ |
| 1193 | Acordeón Diatónico del 1900 | — | polyphone | CC BY | ✓ | — | 371 | organ |
| 1194 | Gordon’s Whistle | Gabriel Ferrante | musical-artifacts | CC BY 3.0 | — | 0.3 MB | 329 | other |
| 1195 | Beatnik Mobile Banks (SF2) | Beatnik Inc. | musical-artifacts | CC BY 3.0 | ✓ | 0.6 MB | 4070 | other |
| 1196 | Rhodes | gregogiudici | github | MIT | ✓ | 0.8 MB | — | other |
| 1197 | Square | gregogiudici | github | MIT | ✓ | 0.8 MB | — | other |
| 1198 | Dull Duco Dances | Digi Hartatak | archive | CC BY 3.0 | ✓ | 1.7 MB | — | other |
| 1199 | CTK 230 Sound Font | Melissa Gilbert-yakoub | archive | CC BY 4.0 | ✓ | 3.1 MB | — | other |
| 1200 | FreeFont | bradhowes | github | MIT | ✓ | 3.1 MB | — | other |
| 1201 | FreeFont | bradhowes | github | MIT | ✓ | 3.1 MB | — | other |
| 1202 | scc1t2 | misterhat | github | MIT | ✓ | 3.1 MB | — | other |
| 1203 | Saw | gregogiudici | github | MIT | ✓ | 3.2 MB | — | other |
| 1204 | default | yakari | github | MIT | ✓ | 5.7 MB | — | other |
| 1205 | Pulse | gregogiudici | github | MIT | ✓ | 7.4 MB | — | other |
| 1206 | SuperSponge (PSX) Soundfont | tahutoa | musical-artifacts | CC BY 3.0 | — | 9.5 MB | 1908 | other |
| 1207 | The King of Fighters 2002: Challenge to Ultimate Battle Soundfont (UPD | VideoGameKid (Originally rippe | musical-artifacts | CC BY 3.0 | ✓ | 13.8 MB | 1303 | other |
| 1208 | SONiVOX EAS GM Wavetable 12 Variants | Sonic Network Inc. | musical-artifacts | CC BY 3.0 | ✓ | 17.8 MB | 6361 | other |
| 1209 | H G F Sounds U C 1 S D P01 | HGFortune, Paule Amca | archive | CC BY 3.0 | — | 20.8 MB | — | other |
| 1210 | GeneralUser GS MuseScore v1.442 | bradhowes | github | MIT | ✓ | 29.8 MB | — | other |
| 1211 | Proteus | Proteus | musical-artifacts | CC BY | ✓ | 34.8 MB | 20017 | other |
| 1212 | H G F Sounds Uc Lp inst 01 | HGFortune, Paule Amca | archive | CC BY 3.0 | — | 35.0 MB | — | other |
| 1213 | Pizza Tower Soundfont | XXtherobloxx21, PeterGriffin10 | musical-artifacts | CC BY | — | 37.3 MB | 4734 | other |
| 1214 | WOTJA X | Intermorphic | musical-artifacts | CC BY | ✓ | 37.4 MB | 1639 | other |
| 1215 | H G F Sounds Uc 1 S InstrFx01 | HGFortune, Paule Amca | archive | CC BY 3.0 | — | 49.7 MB | — | other |
| 1216 | Synth Pack 1 | Joshua R (Soundfont Collector) | musical-artifacts | CC BY | ✓ | 51.8 MB | 7510 | other |
| 1217 | Sci-Fi & Supernatural | Joshua R (Soundfont Collector) | musical-artifacts | CC BY | ✓ | 60.1 MB | 9815 | other |
| 1218 | loopool's Visible Spectrum Scale Project | loopool / Jean-Paul Garnier | archive | CC BY 3.0 | ✓ | 65.6 MB | — | other |
| 1219 | H G F Sounds Uc 1 S AthmoFx01 | HGFortune, Paule Amca | archive | CC BY 3.0 | — | 80.1 MB | — | other |
| 1220 | H G F Sounds Uc 1 S Txt Phrases 01 | HGFortune, Paule Amca | archive | CC BY 3.0 | — | 86.9 MB | — | other |
| 1221 | PerfectPiano Soundfont Instrument Package | Mildanner, Revontulet Soft | musical-artifacts | CC BY 3.0 | — | 98.1 MB | 2576 | other |
| 1222 | H G F Sounds Uc Lp Athm Fx 01 | HGFortune, Paule Amca | archive | CC BY 3.0 | — | 115.7 MB | — | other |
| 1223 | H G F Sounds Uc Lp X A 01 | HGFortune, Paule Amca | archive | CC BY 3.0 | — | 119.3 MB | — | other |
| 1224 | Synth Pack 2 | Joshua R (Soundfont Collector) | musical-artifacts | CC BY | ✓ | 122.5 MB | 7178 | other |
| 1225 | H G F Sounds Uc StereoSF2 | HGFortune, Paule Amca | archive | CC BY 3.0 | — | 151.6 MB | — | other |
| 1226 | OnuteFont | OnuteWORLD Server Ltd. | musical-artifacts | CC BY 3.0 | ✓ | 164.4 MB | 7896 | other |
| 1227 | Beats CodeNameHippie Collection | Motionwave (MW) | musical-artifacts | CC BY 3.0 | ✓ | 209.1 MB | 1348 | other |
| 1228 | Amen Break Soundfont | ASmolBoy, VEXST | musical-artifacts | CC BY 3.0 | ✓ | — | 22647 | other |
| 1229 | Samsung Ch@t 222 (GT-E2220) Soundfont (122MB + 120KB) | Sonic Network Inc. | musical-artifacts | CC BY 3.0 | ✓ | — | 9923 | other |
| 1230 | Concert Harp Soundfont (from Sonatina sfz) | Fernando A. Martin | musical-artifacts | CC BY | ✓ | — | 9178 | other |
| 1231 | Metal Slug (Direct Sampling) | Josh R. | musical-artifacts | CC BY | ✓ | — | 7225 | other |
| 1232 | E3Kay's Fairlight CMI Collection v2.0 | E3Kay, stgiga | musical-artifacts | CC BY 3.0 | ✓ | — | 6253 | other |
| 1233 | General User GS! | SpessaSus and XXtherobloxx21 | musical-artifacts | CC BY 3.0 | ✓ | — | 6117 | other |
| 1234 | Styx Soundfont v1.1 | Arsi | musical-artifacts | CC BY | ✓ | — | 5543 | other |
| 1235 | Sinfon36Plus.sf2 | Anugrah Pratama | musical-artifacts | CC BY 3.0 | ✓ | — | 4823 | other |
| 1236 | LG G5400 SoundFont (aka Casio Mobile, OKI ML2870) | © OKI, Casio, 2003; | musical-artifacts | CC BY 3.0 | ✓ | — | 4205 | other |
| 1237 | Damn daniel soundfont (sf2) | weggyisawesome | musical-artifacts | CC BY 3.0 | ✓ | — | 3772 | other |
| 1238 | GeneralUser GS Live-Audigy v1.44_custom Soundfont | Unknown | musical-artifacts | CC BY 3.0 | ✓ | — | 3595 | other |
| 1239 | Super Smash Flash 2 - Mr. Saturn SFX Soundfont | Mildanner, McLeodGaming | musical-artifacts | CC BY 3.0 | ✓ | — | 3485 | other |
| 1240 | Leapster | iusmaker777 | musical-artifacts | CC BY 3.0 | ✓ | — | 3424 | other |
| 1241 | Female Vocalizer | Bubby293 | musical-artifacts | CC BY 3.0 | ✓ | — | 3365 | other |
| 1242 | Amiga 5S - SF2 | ThatOneWiiMattFan | musical-artifacts | CC BY 3.0 | ✓ | — | 3114 | other |
| 1243 | Just Shapes and Beats Inspired Soundfont | XXtherobloxx21, Berzerk Studio | musical-artifacts | CC BY 3.0 | ✓ | — | 3069 | other |
| 1244 | SONiVOX EAS GM Wavetable | Anugrah Pratama | musical-artifacts | CC BY 3.0 | ✓ | — | 2963 | other |
| 1245 | Yee Soundfonts | M. Reza Khadafi | musical-artifacts | CC BY | ✓ | — | 2783 | other |
| 1246 | LG B2000 SoundFont (aka Casio Mobile, OKI ML2871) | © OKI, Casio, 2003; | musical-artifacts | CC BY 3.0 | ✓ | — | 2681 | other |
| 1247 | WalkBand Default Instruments Soundfont | Mildanner, Revontulet Soft, Ma | musical-artifacts | CC BY 3.0 | ✓ | — | 2680 | other |
| 1248 | &#039;Decrescendo&#039; Accordion | — | polyphone | CC BY | ✓ | — | 2655 | other |
| 1249 | Maestro clarinet | Mats Helgesson | polyphone | CC BY | ✓ | — | 2647 | other |
| 1250 | Sonatina Symphonic Orchestra | Mattias Westlund | polyphone | CC BY | — | — | 2623 | other |
| 1251 | Macintosh Startup Soundfont | Polter | musical-artifacts | CC BY 3.0 | ✓ | — | 2355 | other |
| 1252 | E3Kay's Fairlight CMI Collection | E3Kay | musical-artifacts | CC BY 3.0 | ✓ | — | 2135 | other |
| 1253 | PhoeniXG v2.1 | Jexu | musical-artifacts | CC BY 3.0 | ✓ | — | 2103 | other |
| 1254 | yamaha combo organ soundfont | TheSoundfontMaker | musical-artifacts | CC BY 3.0 | — | — | 2102 | other |
| 1255 | Saint James Orchestra | Simon JL | polyphone | CC BY | — | — | 1896 | other |
| 1256 | Scratch 2.0 Alpha Soundfont (2010-2011) | OnuteWORLD Server Ltd. | musical-artifacts | CC BY 3.0 | ✓ | — | 1837 | other |
| 1257 | bell soundfont | TheSoundfontMaker | musical-artifacts | CC BY 3.0 | — | — | 1742 | other |
| 1258 | Macintosh Startup Soundfont 2.0 | N.Z | musical-artifacts | CC BY 3.0 | ✓ | — | 1697 | other |
| 1259 | Ba Soundfont 2017 | M. Reza Khadafi | musical-artifacts | CC BY | ✓ | — | 1469 | other |
| 1260 | The Ultimate Earthbound Soundfont | — | polyphone | CC BY | — | — | 1372 | other |
| 1261 | SuperSponge Soundfont (PS1) | — | polyphone | CC BY | ✓ | — | 1257 | other |
| 1262 | 42 All-Time Classics/Clubhouse Games (DS) Soundfont | tahutoa | musical-artifacts | CC BY 3.0 | ✓ | — | 1160 | other |
| 1263 | LG G5400 SoundFont Samples | © OKI, Casio, 2003; | musical-artifacts | CC BY 3.0 | — | — | 1134 | other |
| 1264 | Mega Man 8-bit &amp; Wily Wars Soundfont(s) | — | polyphone | CC BY | ✓ | — | 1128 | other |
| 1265 | Discord Stage Music Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 1125 | other |
| 1266 | Aria Math Hand Pan Soundfont | Bryson Lemere | musical-artifacts | CC BY 3.0 | ✓ | — | 1119 | other |
| 1267 | The Wav Soundfont | Bubby293 | musical-artifacts | CC BY 3.0 | ✓ | — | 1111 | other |
| 1268 | The Ultimate (american) DTMF Soundfont | sylavenn | musical-artifacts | CC BY 3.0 | ✓ | — | 1107 | other |
| 1269 | Caed's Small Trash GM v1.06 | Caed | musical-artifacts | CC BY 3.0 | ✓ | — | 1103 | other |
| 1270 | Discord Keyboard Combo Soundfont | Mildanner, Discord | musical-artifacts | CC BY 3.0 | ✓ | — | 1094 | other |
| 1271 | New Face Trumpet (PSY) Soundfont | Mason (2022) | musical-artifacts | CC BY | ✓ | — | 1040 | other |
| 1272 | Dystopian Terra | Brandon Clark | polyphone | CC BY | ✓ | — | 975 | other |
| 1273 | Voxatron SF2 | BarOS | musical-artifacts | CC BY 3.0 | ✓ | — | 914 | other |
| 1274 | Instagram Piano Ringtone Soundfont | Mildanner, Meta | musical-artifacts | CC BY 3.0 | ✓ | — | 895 | other |
| 1275 | Scratch Video Game Loop Soundfont | Mildanner, Scratch Team | musical-artifacts | CC BY 3.0 | ✓ | — | 884 | other |
| 1276 | Buh bah dahdah Sounfont | Bubby293 | musical-artifacts | CC BY 3.0 | ✓ | — | 866 | other |
| 1277 | Boeing 737 Soundfont | a human | musical-artifacts | CC BY 3.0 | ✓ | — | 840 | other |
| 1278 | Fire Emblem 4 Soundfont Concept | Mahmoud Ehab | musical-artifacts | CC BY 3.0 | ✓ | — | 805 | other |
| 1279 | YouTube Microphone Search Soundfont | Mildanner, Google LLC | musical-artifacts | CC BY 3.0 | ✓ | — | 768 | other |
| 1280 | Jeffersonbi's chromatics scale | Bubby293 | musical-artifacts | CC BY 3.0 | ✓ | — | 762 | other |
| 1281 | Anomaly 1 | ? | polyphone | CC BY | — | — | 759 | other |
| 1282 | Bassoon | Ethan Winer | polyphone | CC BY | ✓ | — | 696 | other |
| 1283 | Discord Snake 404 Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 695 | other |
| 1284 | Roland U220 Winds (clarinet) | Roland | polyphone | CC BY | ✓ | — | 680 | other |
| 1285 | RAW Buzzer SB2 Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 672 | other |
| 1286 | Doodle Suno Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 628 | other |
| 1287 | Discord Main Synths (FIXED) Soundfont | Mildanner, Tarty9810 | musical-artifacts | CC BY 3.0 | ✓ | — | 619 | other |
| 1288 | Insaniquarium! Deluxe | — | polyphone | CC BY | ✓ | — | 608 | other |
| 1289 | EMU Proteus 2000: Platinum Pads Vol.2 | — | polyphone | CC BY | — | — | 607 | other |
| 1290 | Xpand!2 Basic Square Lead Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 524 | other |
| 1291 | Madagascar (2005) DS/GBA HD Soundfont (Incomplete) | Nicolas Soliz-12 | musical-artifacts | CC BY 3.0 | ✓ | — | 441 | other |
| 1292 | Africa | Herb Jimmerson | polyphone | CC BY | ✓ | — | 430 | other |
| 1293 | Game Creator Soundfont | PikaNoob | musical-artifacts | CC BY 3.0 | ✓ | — | 406 | other |
| 1294 | LMMS TripleOscillator Mini Custom Instrument Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 392 | other |
| 1295 | Opera GX Ad Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 384 | other |
| 1296 | MidiTrail iOS Soundfont lookalike (Wasteyarded) | MidiTrail, XXtherobloxx21 | musical-artifacts | CC BY 3.0 | ✓ | — | 361 | other |
| 1297 | Choir Bell | Sonido media | polyphone | CC BY | ✓ | — | 355 | other |
| 1298 | Discord Halloween 2022 Soundfont | Mildanner, Discord | musical-artifacts | CC BY 3.0 | ✓ | — | 355 | other |
| 1299 | symbian series 60 3rd edition (needs fixed) | — | polyphone | CC BY | ✓ | — | 355 | other |
| 1300 | 99 Food Ad Soundfont | Mildanner, 99 | musical-artifacts | CC BY 3.0 | ✓ | — | 353 | other |
| 1301 | Harry Styles - As It Was Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 335 | other |
| 1302 | OPL-3 FM 128M | Zandro Reveille | polyphone | CC BY | — | — | 329 | other |
| 1303 | Concon Soundfont | — | polyphone | CC BY | ✓ | — | 326 | other |
| 1304 | Mega Man 8 Soundfont - (PS1 &amp; Saturn) | — | polyphone | CC BY | ✓ | — | 323 | other |
| 1305 | Mario Kart Wii | — | polyphone | CC BY | ✓ | — | 299 | other |
| 1306 | Amazon Ad Promotion Soundfont | Mildanner, Amazon | musical-artifacts | CC BY 3.0 | ✓ | — | 287 | other |
| 1307 | Krypton | Sonido media | polyphone | CC BY | ✓ | — | 284 | other |
| 1308 | Death of a princess | Shane Marsh | polyphone | CC BY | ✓ | — | 281 | other |
| 1309 | Lost boys | Sonido media | polyphone | CC BY | ✓ | — | 278 | other |
| 1310 | MagicSF (Soundfont) Jampea | Jampea | musical-artifacts | CC BY 3.0 | ✓ | — | 259 | other |
| 1311 | Golan | Sonido media | polyphone | CC BY | ✓ | — | 245 | other |
| 1312 | Electric company | J. Talbert | polyphone | CC BY | ✓ | — | 241 | other |
| 1313 | Super Mario World Modded SF2 | — | polyphone | CC BY | ✓ | — | 238 | other |
| 1314 | Keeta Ad Soundfont | Mildanner, Keeta | musical-artifacts | CC BY 3.0 | ✓ | — | 235 | other |
| 1315 | Bell wavescape | Sonido media | polyphone | CC BY | ✓ | — | 234 | other |
| 1316 | Centrifuge | Sonido media | polyphone | CC BY | ✓ | — | 223 | other |
| 1317 | Millenium | Shane Marsh | polyphone | CC BY | ✓ | — | 208 | other |
| 1318 | Bloodwar | Skov-Nielsen Jess Donovan | polyphone | CC BY | ✓ | — | 207 | other |
| 1319 | Bradbury | Sonido media | polyphone | CC BY | ✓ | — | 200 | other |
| 1320 | Stoat Notification Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 196 | other |
| 1321 | (Unfinished) Waveworld Soundfont | Linksab | musical-artifacts | CC BY 3.0 | — | — | 188 | other |
| 1322 | Roblox Bass(Trowel) | — | polyphone | CC BY | ✓ | — | 166 | other |
| 1323 | Quag | J. Talbert | polyphone | CC BY | ✓ | — | 161 | other |
| 1324 | Vintage 1930-1970 Soundfont | — | polyphone | CC BY | — | — | 153 | other |
| 1325 | NitroShoe&#039;s Super Small &#039;Font | — | polyphone | CC BY | ✓ | — | 149 | other |
| 1326 | 80s | — | polyphone | CC BY | ✓ | — | 131 | other |
| 1327 | SuperSponge (PSX) Beta | — | polyphone | CC BY | ✓ | — | 123 | other |
| 1328 | 80s drums version 2 | — | polyphone | CC BY | ✓ | — | 114 | other |
| 1329 | Chrome Music Lab | — | polyphone | CC BY | ✓ | — | 112 | other |
| 1330 | Fixed SONY SPC700 SNES Soundfont | — | polyphone | CC BY | ✓ | — | 102 | other |
| 1331 | Jug Band | — | polyphone | CC BY | ✓ | — | 93 | other |
| 1332 | Sound Blaster: Restoration Project | — | polyphone | CC BY | ✓ | — | 73 | other |
| 1333 | Bell&#039;s &amp; Whistles Arcade V2 Soundfont | — | polyphone | CC BY | ✓ | — | 59 | other |
| 1334 | Dragon Quest VI (SNES) | — | polyphone | CC BY | ✓ | — | 46 | other |
| 1335 | mortal kombat 3 snes | — | polyphone | CC BY | ✓ | — | 46 | other |
| 1336 | Dragon Quest V (SNES) | — | polyphone | CC BY | ✓ | — | 45 | other |
| 1337 | drums 80s | — | polyphone | CC BY | ✓ | — | 45 | other |
| 1338 | Bells and Whistles Arcade instrument set Soundfont | — | polyphone | CC BY | ✓ | — | 44 | other |
| 1339 | Make 10: A Journey of Numbers - DS Soundfont | — | polyphone | CC BY | ✓ | — | 44 | other |
| 1340 | secret of mana snes | — | polyphone | CC BY | ✓ | — | 38 | other |
| 1341 | Touhou Soundfont | — | polyphone | CC BY | — | — | 38 | other |
| 1342 | Sunset Riders (Arcade version) Instrument Set Soundfont | — | polyphone | CC BY | ✓ | — | 34 | other |
| 1343 | Fixed Simpsons Arcade Soundfont | — | polyphone | CC BY | ✓ | — | 31 | other |
| 1344 | Late 90s Mashup | — | polyphone | CC BY | ✓ | — | 31 | other |
| 1345 | Salamander 2 Drumkit | — | polyphone | CC BY | ✓ | — | 31 | other |
| 1346 | TOY STROY SNES | — | polyphone | CC BY | ✓ | — | 30 | other |
| 1347 | Fatal Fury Instrument Set Soundfont | — | polyphone | CC BY | ✓ | — | 27 | other |
| 1348 | lufia 2 snes | — | polyphone | CC BY | ✓ | — | 27 | other |
| 1349 | Salamander 2 Arcade Soundfont | — | polyphone | CC BY | ✓ | — | 25 | other |
| 1350 | the simpsons arcade 1991 konami | — | polyphone | CC BY | ✓ | — | 25 | other |
| 1351 | Sexy Parodius Arcade Soundfont | — | polyphone | CC BY | ✓ | — | 23 | other |
| 1352 | Sunset Riders Arcade V2 Soundfont | — | polyphone | CC BY | ✓ | — | 23 | other |
| 1353 | Fixed TAITO-F3System | — | polyphone | CC BY | ✓ | — | 22 | other |
| 1354 | MAXIMUM CARNAGE snes | — | polyphone | CC BY | ✓ | — | 21 | other |
| 1355 | Lethal Enforcers 2 Arcade Soundfont | — | polyphone | CC BY | ✓ | — | 20 | other |
| 1356 | bubsy snes | — | polyphone | CC BY | ✓ | — | 19 | other |
| 1357 | daze before christmans | — | polyphone | CC BY | ✓ | — | 19 | other |
| 1358 | donald duck maui malad | — | polyphone | CC BY | ✓ | — | 19 | other |
| 1359 | Gokujyou Parodius Arcade Soundfont | — | polyphone | CC BY | ✓ | — | 19 | other |
| 1360 | lupin snes | — | polyphone | CC BY | ✓ | — | 19 | other |
| 1361 | Mystic Warriors Arcade Soundfont | — | polyphone | CC BY | ✓ | — | 19 | other |
| 1362 | Fixed Taito Aqua Jack Soundfont | — | polyphone | CC BY | ✓ | — | 18 | other |
| 1363 | Racin&#039; Force Konami Instrument set | — | polyphone | CC BY | ✓ | — | 18 | other |
| 1364 | the lion king snes drums | — | polyphone | CC BY | ✓ | — | 18 | other |
| 1365 | Fixed Gradius [Taito System] Soundfont | — | polyphone | CC BY | ✓ | — | 17 | other |
| 1366 | the lion king snes 2026 | — | polyphone | CC BY | ✓ | — | 17 | other |
| 1367 | Cadillacs and Dinosaurs Arcade Soundfont | — | polyphone | CC BY | ✓ | — | 15 | other |
| 1368 | Golfing Greats 2 (Japan) / Konami&#039;s Open Golf Championship (US) S | — | polyphone | CC BY | ✓ | — | 15 | other |
| 1369 | Lethal Enforcers 2: Gun Fighters Arcade Soundfont | — | polyphone | CC BY | ✓ | — | 15 | other |
| 1370 | Mystic Warriors Arcade Soundfont | — | polyphone | CC BY | ✓ | — | 15 | other |
| 1371 | Mystic Warriors: Wrath of The Ninjas Konami Instrument set | — | polyphone | CC BY | ✓ | — | 15 | other |
| 1372 | Saturday Night Slam Masters Arcade Soundfont | — | polyphone | CC BY | ✓ | — | 15 | other |
| 1373 | Fixed Taito Enforce Soundfont | — | polyphone | CC BY | ✓ | — | 14 | other |
| 1374 | fzero snes | — | polyphone | CC BY | ✓ | — | 14 | other |
| 1375 | tetris 2 snes | — | polyphone | CC BY | ✓ | — | 14 | other |
| 1376 | Fixed Air Inferno (Arcade) Soundfont | — | polyphone | CC BY | ✓ | — | 13 | other |
| 1377 | Racin&#039; Force Arcade Soundfont | — | polyphone | CC BY | ✓ | — | 13 | other |
| 1378 | Salamander 2 Konami Instrument set | — | polyphone | CC BY | ✓ | — | 13 | other |
| 1379 | Fixed Taito Top Landing Soundfont | — | polyphone | CC BY | ✓ | — | 12 | other |
| 1380 | Rushing Heroes Arcade Soundfont | — | polyphone | CC BY | ✓ | — | 12 | other |
| 1381 | Fixed Taito Final Blow Drumkit | — | polyphone | CC BY | ✓ | — | 11 | other |
| 1382 | Saturday Night Slam Masters Arcade Instrument set | — | polyphone | CC BY | ✓ | — | 11 | other |
| 1383 | Fixed Taito MEGA BLAST Soundfont | — | polyphone | CC BY | ✓ | — | 10 | other |
| 1384 | Blitz Lunar/William Kage SMW Soundfont [FIXED] | — | polyphone | CC BY | ✓ | — | 9 | other |
| 1385 | Fixed TAITO Superman Soundfont | — | polyphone | CC BY | ✓ | — | 9 | other |
| 1386 | acordeon gabanelli 5 registros | — | polyphone | CC BY | ✓ | — | 1 | other |
| 1387 | Beeper | gregogiudici | github | MIT | ✓ | — | — | other |
| 1388 | Fanon Park Soundfont ~ DIRECTOR'S CUT – demo files | — | archive | CC BY 4.0 | — | — | — | other |
| 1389 | PACK of SOUNDFONTS | PHJ Piano Solos | archive | CC BY 4.0 | — | — | — | other |
| 1390 | Pocoyo Soundfont | MasonMasterMusic | musical-artifacts | CC BY 3.0 | ✓ | — | 0 | other |
| 1391 | Scrimblo Bimblo's Scrunky Adventure Soundfont | Aquacycle | musical-artifacts | CC BY 3.0 | ✓ | — | 0 | other |
| 1392 | soundfont | markus tornow | archive | CC BY 4.0 | — | — | — | other |
| 1393 | Soundfont collection | — | archive | CC BY 4.0 | — | — | — | other |
| 1394 | Theremin | gregogiudici | github | MIT | ✓ | — | — | other |
| 1395 | Trombone | gregogiudici | github | MIT | ✓ | — | — | other |
| 1396 | what a mario world Overworld (Super Mario Advance Soundfont) | Yodel Boi | archive | CC BY 4.0 | — | — | — | other |
| 1397 | ZZZ1 | bradhowes | github | MIT | ✓ | — | — | other |
| 1398 | ZZZ2 | bradhowes | github | MIT | ✓ | — | — | other |
| 1399 | nylon_guitar | constcut | github | MIT | ✓ | 0.1 MB | — | piano |
| 1400 | guitar | constcut | github | MIT | ✓ | 0.2 MB | — | piano |
| 1401 | eguitar | constcut | github | MIT | ✓ | 0.4 MB | — | piano |
| 1402 | piano | constcut | github | MIT | ✓ | 0.6 MB | — | piano |
| 1403 | drums | constcut | github | MIT | ✓ | 0.7 MB | — | piano |
| 1404 | Tiny piano (ogg version) | Signal Experiments | musical-artifacts | CC BY | — | 2.1 MB | 2448 | piano |
| 1405 | fullset | constcut | github | MIT | ✓ | 5.7 MB | — | piano |
| 1406 | Tiny Piano 00 (SFZ) | Signal Experiments | musical-artifacts | CC BY | — | 7.2 MB | 1765 | piano |
| 1407 | UprightPianoKW-small-20190703 | AnonN10 | github | MIT | ✓ | 9.0 MB | — | piano |
| 1408 | Greg Sullivan E-Pianos | Greg Sullivan | sfzinstruments | CC BY 3.0 | — | 21.5 MB | — | piano |
| 1409 | Piano | gregogiudici | github | MIT | ✓ | 22.0 MB | — | piano |
| 1410 | GeneralUser-GS | patakuti | github | MIT | ✓ | 30.8 MB | — | piano |
| 1411 | GeneralUserGS | isssifre-arch | github | MIT | ✓ | 30.8 MB | — | piano |
| 1412 | floppy disk soundfont V2 | TheSoundfontMaker | musical-artifacts | CC BY 3.0 | — | 33.6 MB | 1541 | piano |
| 1413 | YDP Grand Piano | FreePats project | FreePats | CC BY 3.0 | ✓ | 36.0 MB | — | piano |
| 1414 | Equinox_Grand_Pianos | SpaceShaman | github | MIT | ✓ | 91.7 MB | — | piano |
| 1415 | FluidR3_GM | Frank Wen | MuseScore | MIT | ✓ | 125.7 MB | — | piano |
| 1416 | Headroom Piano | Bengt Nilsson | sfzinstruments | CC BY 4.0 | — | 156.2 MB | — | piano |
| 1417 | MuseScore_General | S. Christian Collins（改编自 Fluid | MuseScore | MIT | ✓ | 205.6 MB | — | piano |
| 1418 | Salamander Grand Piano | FreePats project | FreePats | CC BY 3.0 | ✓ | 296.0 MB | — | piano |
| 1419 | Salamander Grand Piano | Alexander Holm | sfzinstruments | CC BY 3.0 | — | 394.0 MB | — | piano |
| 1420 | Accurate-Salamander Project | Chisato Yamauchi | sfzinstruments | CC BY | — | 1638.4 MB | — | piano |
| 1421 | Alex's gm soundfont version 1.3 | High quality sfs | musical-artifacts | CC BY 3.0 | ✓ | — | 69780 | piano |
| 1422 | S90ES | Henrique Gogó | musical-artifacts | CC BY 3.0 | ✓ | — | 27220 | piano |
| 1423 | Real Honky tonk piano by Milton Paredes | Milton Paredes, mpj factory st | musical-artifacts | CC BY | ✓ | — | 10965 | piano |
| 1424 | [DEPRECATED] NeoVST Piano One (sf2 version) | Exthayan | musical-artifacts | CC BY 3.0 | ✓ | — | 7128 | piano |
| 1425 | Yamaha YPT 220 soundfont studio version | TheSoundfontMaker | musical-artifacts | CC BY 3.0 | ✓ | — | 6287 | piano |
| 1426 | Yamaha CFX Studio Grand V2 | — | polyphone | CC BY | — | — | 3136 | piano |
| 1427 | Akai-Steinway III | Denis | polyphone | CC BY | ✓ | — | 3023 | piano |
| 1428 | Piano Sample Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 2050 | piano |
| 1429 | WalkBand Complete Drum Soundfont | Mildanner, WalkBand, Revontule | musical-artifacts | CC BY 3.0 | ✓ | — | 1890 | piano |
| 1430 | Nord Stage GP Grand Piano | — | polyphone | CC BY | — | — | 1873 | piano |
| 1431 | GPO Concert Steinway Piano | David Shan | polyphone | CC BY | ✓ | — | 1686 | piano |
| 1432 | Motif ES6 Concert Piano v2 | Mitrofanis George (GeMitro@) | polyphone | CC BY | ✓ | — | 1429 | piano |
| 1433 | White Grand Piano Collection | — | polyphone | CC BY | — | — | 1382 | piano |
| 1434 | Nord Imperial Grand | — | polyphone | CC BY | ✓ | — | 1207 | piano |
| 1435 | SC55 Piano V2 | Xiaosu Du | polyphone | CC BY | ✓ | — | 1008 | piano |
| 1436 | Nord Romantic Grand | — | polyphone | CC BY | ✓ | — | 970 | piano |
| 1437 | Steinway B - 1956 | — | polyphone | CC BY | ✓ | — | 887 | piano |
| 1438 | Yamaha S90 ES Natural Grand | — | polyphone | CC BY | ✓ | — | 803 | piano |
| 1439 | JV1080 Nice Piano | Xiaosu Du | polyphone | CC BY | ✓ | — | 658 | piano |
| 1440 | Sad Piano | — | polyphone | CC BY | ✓ | — | 606 | piano |
| 1441 | Piano Icons Vol.1 | — | polyphone | CC BY | ✓ | — | 593 | piano |
| 1442 | Steinway B-211 Lite | — | polyphone | CC BY | ✓ | — | 466 | piano |
| 1443 | My Wurlitzer Piano | — | polyphone | CC BY | — | — | 399 | piano |
| 1444 | Piano | — | polyphone | CC BY | ✓ | — | 215 | piano |
| 1445 | Rowans Soundfont Pack | — | polyphone | CC BY | ✓ | — | 212 | piano |
| 1446 | BJDNielKalimba | — | polyphone | CC BY | ✓ | — | 170 | piano |
| 1447 | Digo Piano | — | polyphone | CC BY | ✓ | — | 168 | piano |
| 1448 | Cesar Fever | — | polyphone | CC BY | — | — | 163 | piano |
| 1449 | MidiAnimated | — | polyphone | CC BY | ✓ | — | 139 | piano |
| 1450 | Shiroi Lite Grand I | — | polyphone | CC BY | ✓ | — | 134 | piano |
| 1451 | Tinpots Piano Collection | — | polyphone | CC BY | ✓ | — | 120 | piano |
| 1452 | Honky-Tonk | — | polyphone | CC BY | ✓ | — | 111 | piano |
| 1453 | Earrape piano | — | polyphone | CC BY | ✓ | — | 102 | piano |
| 1454 | Tinpots Piano. | — | polyphone | CC BY | ✓ | — | 39 | piano |
| 1455 | Clav | sinshu | github | MIT | — | — | — | piano |
| 1456 | Electric Piano | gregogiudici | github | MIT | ✓ | — | — | piano |
| 1457 | ElectricPiano1 | sinshu | github | MIT | — | — | — | piano |
| 1458 | ElectricPiano2 | sinshu | github | MIT | — | — | — | piano |
| 1459 | epiano | constcut | github | MIT | ✓ | — | — | piano |
| 1460 | Piano1 | sinshu | github | MIT | — | — | — | piano |
| 1461 | Piano2 | sinshu | github | MIT | — | — | — | piano |
| 1462 | Piano3 | sinshu | github | MIT | — | — | — | piano |
| 1463 | TX Brass | AudioKit | github | MIT | — | — | — | piano |
| 1464 | TX LoTine81z | AudioKit | github | MIT | — | — | — | piano |
| 1465 | TX Metalimba | AudioKit | github | MIT | — | — | — | piano |
| 1466 | TX Pluck Bass | AudioKit | github | MIT | — | — | — | piano |
| 1467 | unbolted_min | io7m-com | github | ISC | ✓ | 0.3 MB | — | sfx |
| 1468 | Árvore Leitor SFX Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 557 | sfx |
| 1469 | Slide whistle | Ethan Winer | polyphone | CC BY | ✓ | — | 545 | sfx |
| 1470 | Bangs and effects | Project SAM | polyphone | CC BY | ✓ | — | 424 | sfx |
| 1471 | Electro Friend | — | polyphone | CC BY | ✓ | — | 180 | sfx |
| 1472 | lourd of the rings | — | polyphone | CC BY | ✓ | — | 31 | sfx |
| 1473 | Twinbee Yahho! Arcade Soundfont | — | polyphone | CC BY | ✓ | — | 23 | sfx |
| 1474 | StaticSinesta | — | polyphone | CC BY | ✓ | — | 21 | sfx |
| 1475 | Beauty and the Beast  snes | — | polyphone | CC BY | ✓ | — | 1 | sfx |
| 1476 | complex0 | io7m-com | github | ISC | ✓ | — | — | sfx |
| 1477 | empty | io7m-com | github | ISC | ✓ | — | — | sfx |
| 1478 | inst1 | io7m-com | github | ISC | ✓ | — | — | sfx |
| 1479 | inst1_with_modulator | io7m-com | github | ISC | ✓ | — | — | sfx |
| 1480 | preset1 | io7m-com | github | ISC | ✓ | — | — | sfx |
| 1481 | preset1_with_modulator | io7m-com | github | ISC | ✓ | — | — | sfx |
| 1482 | sample0 | io7m-com | github | ISC | ✓ | — | — | sfx |
| 1483 | Classic House Organ 2 Bass | Aleksandr Bykov | musical-artifacts | CC BY 3.0 | ✓ | 0.3 MB | 4862 | synth |
| 1484 | florestan-subset | schellingb | github | MIT | ✓ | 0.5 MB | — | synth |
| 1485 | Synth | gregogiudici | github | MIT | ✓ | 0.6 MB | — | synth |
| 1486 | 2MBGMGS | copych | github | MIT | ✓ | 2.0 MB | — | synth |
| 1487 | Various synths | SpaceShaman | github | MIT | ✓ | 2.2 MB | — | synth |
| 1488 | Papelmedia_Irina_Brochin | SpaceShaman | github | MIT | ✓ | 4.8 MB | — | synth |
| 1489 | loopool - Synthesis Tools .SF2 Soundfont Bundle | loopool / Jean-Paul Garnier | archive | CC BY 3.0 | — | 12.7 MB | — | synth |
| 1490 | Electric Keys | SpaceShaman | github | MIT | ✓ | 14.2 MB | — | synth |
| 1491 | FluidR3Mono_GM | atsushieno | github | MIT | — | 22.5 MB | — | synth |
| 1492 | RCKTNEO SND316X soundfont (version 3.0, GM compatible, feel free to re | RCKTNEO | musical-artifacts | CC BY | ✓ | — | 7700 | synth |
| 1493 | GM Soundtrack Pad Recreation | Darko747 | musical-artifacts | CC BY 3.0 | ✓ | — | 3296 | synth |
| 1494 | Mauifm | N/A | musical-artifacts | CC BY 3.0 | ✓ | — | 2887 | synth |
| 1495 | MediaTek GM Synth [Nokia 108 Profile] "BASS" | DERFJECK | musical-artifacts | CC BY | ✓ | — | 2422 | synth |
| 1496 | Bass Meme Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 2163 | synth |
| 1497 | MEGALOVANIA ACCURATE SHREDDAGE X SOUNDFONT (WITH PRE AMP) - That1Rand0 | — | polyphone | CC BY | ✓ | — | 2083 | synth |
| 1498 | Warm pad | Alessandro Cardinale | polyphone | CC BY | ✓ | — | 1252 | synth |
| 1499 | Casio CZ-5000: Electric Keys | — | polyphone | CC BY | ✓ | — | 930 | synth |
| 1500 | EMU Proteus 2000: Platinum Pads Vol.1 | — | polyphone | CC BY | — | — | 909 | synth |
| 1501 | Roland Alpha Juno-2: Saturn | — | polyphone | CC BY | ✓ | — | 861 | synth |
| 1502 | Heavy | E-mu Sound Central | polyphone | CC BY | ✓ | — | 752 | synth |
| 1503 | NitroFont / flagship HQ soundfont (DISCONTINUED) | — | polyphone | CC BY | — | — | 685 | synth |
| 1504 | Roland Alpha Juno-2: Axel-F | — | polyphone | CC BY | ✓ | — | 673 | synth |
| 1505 | Korg DW-8000: Digital Wire | — | polyphone | CC BY | ✓ | — | 668 | synth |
| 1506 | Elf&#039;s Ultimate Synth Pad pack | — | polyphone | CC BY | ✓ | — | 663 | synth |
| 1507 | Roland Alpha Juno-2: Jump | — | polyphone | CC BY | ✓ | — | 595 | synth |
| 1508 | Roland Alpha Juno-2: A-String | — | polyphone | CC BY | ✓ | — | 532 | synth |
| 1509 | SNES FM Pick Bass Soundfont (Hooded Edge) | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 498 | synth |
| 1510 | E-MU Proteus 2000: Carlos | — | polyphone | CC BY | ✓ | — | 493 | synth |
| 1511 | FM Slap Bass | — | polyphone | CC BY | ✓ | — | 483 | synth |
| 1512 | Sonic the Hedgehog 1/2/3K Soundfont Extension | — | polyphone | CC BY | ✓ | — | 449 | synth |
| 1513 | Namco Arcade Sound Generator/Emulator 2 | — | polyphone | CC BY | ✓ | — | 441 | synth |
| 1514 | Stylophone S-1  (2021 Analogue Sound version) | — | polyphone | CC BY | ✓ | — | 441 | synth |
| 1515 | Cheap Toys | — | polyphone | CC BY | ✓ | — | 435 | synth |
| 1516 | Namco Arcade Recreated WSG - &quot;My Wave Sound Generator&quot; offic | — | polyphone | CC BY | ✓ | — | 429 | synth |
| 1517 | HyperSound Classic / version 3.0 (HyperSound SF2) | — | polyphone | CC BY | ✓ | — | 425 | synth |
| 1518 | Synth Icons Vol.2 | — | polyphone | CC BY | ✓ | — | 414 | synth |
| 1519 | Octave- Neutral Organ (432 Hz A) | — | polyphone | CC BY | ✓ | — | 351 | synth |
| 1520 | 8BitSf Fixed Soundfont | — | polyphone | CC BY | ✓ | — | 331 | synth |
| 1521 | Hardy-Boy | — | polyphone | CC BY | ✓ | — | 291 | synth |
| 1522 | PureSynth - JavaScript Waveforms | — | polyphone | CC BY | ✓ | — | 289 | synth |
| 1523 | Lyle Mays Lead | — | polyphone | CC BY | ✓ | — | 246 | synth |
| 1524 | Doodle Lead | — | polyphone | CC BY | ✓ | — | 220 | synth |
| 1525 | Carnivalesque | — | polyphone | CC BY | ✓ | — | 213 | synth |
| 1526 | HyperSound Rebooted | — | polyphone | CC BY | ✓ | — | 193 | synth |
| 1527 | SoniFont / The ultimate SONiVOX experience | — | polyphone | CC BY | ✓ | — | 188 | synth |
| 1528 | Jackenstein (beta) | — | polyphone | CC BY | ✓ | — | 169 | synth |
| 1529 | Wind orchestra of variable stars | — | polyphone | CC BY | — | — | 163 | synth |
| 1530 | The Michael Rosen Soundfont | — | polyphone | CC BY | — | — | 161 | synth |
| 1531 | Pokemon emerald | — | polyphone | CC BY | ✓ | — | 156 | synth |
| 1532 | ZingPlay SF2! (New) | — | polyphone | CC BY | ✓ | — | 132 | synth |
| 1533 | Pokemon red gb | — | polyphone | CC BY | ✓ | — | 88 | synth |
| 1534 | NitroFont Rebooted | — | polyphone | CC BY | ✓ | — | 86 | synth |
| 1535 | Ande-site GS | — | polyphone | CC BY | ✓ | — | 83 | synth |
| 1536 | Future Bass - cute/electronic | — | polyphone | CC BY | ✓ | — | 80 | synth |
| 1537 | Pokemon gold | — | polyphone | CC BY | ✓ | — | 79 | synth |
| 1538 | Pokemon heart gold | — | polyphone | CC BY | ✓ | — | 78 | synth |
| 1539 | Super Bomberman 2 | — | polyphone | CC BY | ✓ | — | 71 | synth |
| 1540 | Ds | — | polyphone | CC BY | ✓ | — | 69 | synth |
| 1541 | mortal kombat | — | polyphone | CC BY | ✓ | — | 68 | synth |
| 1542 | Earthbound &amp; Chrono Trigger  Soundfont | — | polyphone | CC BY | ✓ | — | 66 | synth |
| 1543 | Pokemon yellow | — | polyphone | CC BY | ✓ | — | 64 | synth |
| 1544 | beepbox square | — | polyphone | CC BY | ✓ | — | 63 | synth |
| 1545 | Golden Sun - Lost Age (gba) | — | polyphone | CC BY | ✓ | — | 60 | synth |
| 1546 | Dragon Quest: The Erdrick Trilogy (SNES) | — | polyphone | CC BY | ✓ | — | 52 | synth |
| 1547 | Pokemon platinun | — | polyphone | CC BY | ✓ | — | 47 | synth |
| 1548 | Gb gbc | — | polyphone | CC BY | ✓ | — | 42 | synth |
| 1549 | Pokemon ruby safire | — | polyphone | CC BY | ✓ | — | 42 | synth |
| 1550 | beepbox snyth bass | — | polyphone | CC BY | ✓ | — | 41 | synth |
| 1551 | Miniitea Studio&#039;s Synth Collection Issue 0-16 | — | polyphone | CC BY | ✓ | — | 37 | synth |
| 1552 | Pokemon cristal | — | polyphone | CC BY | ✓ | — | 34 | synth |
| 1553 | bandlab chip organ | — | polyphone | CC BY | ✓ | — | 30 | synth |
| 1554 | Danny Phantom GBA SoundFont | — | polyphone | CC BY | ✓ | — | 25 | synth |
| 1555 | FM-Synth Fantasy | — | polyphone | CC BY | ✓ | — | 25 | synth |
| 1556 | Gba 1 version | — | polyphone | CC BY | ✓ | — | 25 | synth |
| 1557 | Gba 2 version | — | polyphone | CC BY | ✓ | — | 25 | synth |
| 1558 | Pokemon blue and green | — | polyphone | CC BY | ✓ | — | 25 | synth |
| 1559 | Pokemon silver | — | polyphone | CC BY | ✓ | — | 25 | synth |
| 1560 | sprunki simon soundfont | — | polyphone | CC BY | ✓ | — | 20 | synth |
| 1561 | Pokemon Fire red versão 2 | — | polyphone | CC BY | ✓ | — | 19 | synth |
| 1562 | ahhhh real monsters | — | polyphone | CC BY | ✓ | — | 17 | synth |
| 1563 | N-Siffer Sounder | — | polyphone | CC BY | ✓ | — | 16 | synth |
| 1564 | sim city | — | polyphone | CC BY | ✓ | — | 16 | synth |
| 1565 | Xmen | — | polyphone | CC BY | ✓ | — | 14 | synth |
| 1566 | Pokemon Firefox red 1 | — | polyphone | CC BY | ✓ | — | 11 | synth |
| 1567 | viacom 1976 logo soundfont | — | polyphone | CC BY | ✓ | — | 9 | synth |
| 1568 | 5thSawWave | sinshu | github | MIT | — | — | — | synth |
| 1569 | Accordion | sinshu | github | MIT | — | — | — | synth |
| 1570 | AcousticBass | sinshu | github | MIT | — | — | — | synth |
| 1571 | Agogo | sinshu | github | MIT | — | — | — | synth |
| 1572 | AltoSax | sinshu | github | MIT | — | — | — | synth |
| 1573 | Applause | sinshu | github | MIT | — | — | — | synth |
| 1574 | Atmosphere | sinshu | github | MIT | — | — | — | synth |
| 1575 | Bandoneon | sinshu | github | MIT | — | — | — | synth |
| 1576 | BassLead | sinshu | github | MIT | — | — | — | synth |
| 1577 | Bassoon | sinshu | github | MIT | — | — | — | synth |
| 1578 | Bird | sinshu | github | MIT | — | — | — | synth |
| 1579 | BottleBlow | sinshu | github | MIT | — | — | — | synth |
| 1580 | BowedGlass | sinshu | github | MIT | — | — | — | synth |
| 1581 | BreathNoise | sinshu | github | MIT | — | — | — | synth |
| 1582 | Brush | sinshu | github | MIT | — | — | — | synth |
| 1583 | Celesta | sinshu | github | MIT | — | — | — | synth |
| 1584 | Charang | sinshu | github | MIT | — | — | — | synth |
| 1585 | ChifferLead | sinshu | github | MIT | — | — | — | synth |
| 1586 | ChoirAahs | sinshu | github | MIT | — | — | — | synth |
| 1587 | ChurchOrgan1 | sinshu | github | MIT | — | — | — | synth |
| 1588 | Clarinet | sinshu | github | MIT | — | — | — | synth |
| 1589 | CleanGtr | sinshu | github | MIT | — | — | — | synth |
| 1590 | Contrabass | sinshu | github | MIT | — | — | — | synth |
| 1591 | Crystal | sinshu | github | MIT | — | — | — | synth |
| 1592 | DistortionGtr | sinshu | github | MIT | — | — | — | synth |
| 1593 | EchoDrops | sinshu | github | MIT | — | — | — | synth |
| 1594 | Electronic | sinshu | github | MIT | — | — | — | synth |
| 1595 | Fantasia | sinshu | github | MIT | — | — | — | synth |
| 1596 | Fiddle | sinshu | github | MIT | — | — | — | synth |
| 1597 | FingerBass | sinshu | github | MIT | — | — | — | synth |
| 1598 | FretlessBass | sinshu | github | MIT | — | — | — | synth |
| 1599 | Glockenspiel | sinshu | github | MIT | — | — | — | synth |
| 1600 | Goblin | sinshu | github | MIT | — | — | — | synth |
| 1601 | GtFretNoise | sinshu | github | MIT | — | — | — | synth |
| 1602 | Gunshot | sinshu | github | MIT | — | — | — | synth |
| 1603 | HaloPad | sinshu | github | MIT | — | — | — | synth |
| 1604 | Harmonica | sinshu | github | MIT | — | — | — | synth |
| 1605 | HarmonicGtr | sinshu | github | MIT | — | — | — | synth |
| 1606 | Harp | sinshu | github | MIT | — | — | — | synth |
| 1607 | Harpsichord | sinshu | github | MIT | — | — | — | synth |
| 1608 | Helicopter | sinshu | github | MIT | — | — | — | synth |
| 1609 | Honkytonk | sinshu | github | MIT | — | — | — | synth |
| 1610 | IceRain | sinshu | github | MIT | — | — | — | synth |
| 1611 | Jazz | sinshu | github | MIT | — | — | — | synth |
| 1612 | JazzGtr | sinshu | github | MIT | — | — | — | synth |
| 1613 | Marimba | sinshu | github | MIT | — | — | — | synth |
| 1614 | Mellopad | gregogiudici | github | MIT | ✓ | — | — | synth |
| 1615 | MeloTom1 | sinshu | github | MIT | — | — | — | synth |
| 1616 | MetalPad | sinshu | github | MIT | — | — | — | synth |
| 1617 | MusicBox | sinshu | github | MIT | — | — | — | synth |
| 1618 | MuteGtr | sinshu | github | MIT | — | — | — | synth |
| 1619 | NylonGtr | sinshu | github | MIT | — | — | — | synth |
| 1620 | Ocarina | sinshu | github | MIT | — | — | — | synth |
| 1621 | Organ1 | sinshu | github | MIT | — | — | — | synth |
| 1622 | Organ2 | sinshu | github | MIT | — | — | — | synth |
| 1623 | Organ3 | sinshu | github | MIT | — | — | — | synth |
| 1624 | OverdriveGtr | sinshu | github | MIT | — | — | — | synth |
| 1625 | Piccolo | sinshu | github | MIT | — | — | — | synth |
| 1626 | PickedBass | sinshu | github | MIT | — | — | — | synth |
| 1627 | PizzicatoStr | sinshu | github | MIT | — | — | — | synth |
| 1628 | Polysynth | sinshu | github | MIT | — | — | — | synth |
| 1629 | Power | sinshu | github | MIT | — | — | — | synth |
| 1630 | Recorder | sinshu | github | MIT | — | — | — | synth |
| 1631 | ReedOrgan | sinshu | github | MIT | — | — | — | synth |
| 1632 | ReverseCym | sinshu | github | MIT | — | — | — | synth |
| 1633 | Room | sinshu | github | MIT | — | — | — | synth |
| 1634 | Santur | sinshu | github | MIT | — | — | — | synth |
| 1635 | Sawtooth Pad | gregogiudici | github | MIT | ✓ | — | — | synth |
| 1636 | SawWave | sinshu | github | MIT | — | — | — | synth |
| 1637 | Seashore | sinshu | github | MIT | — | — | — | synth |
| 1638 | SFX | sinshu | github | MIT | — | — | — | synth |
| 1639 | Shanai | sinshu | github | MIT | — | — | — | synth |
| 1640 | SlapBass1 | sinshu | github | MIT | — | — | — | synth |
| 1641 | SlapBass2 | sinshu | github | MIT | — | — | — | synth |
| 1642 | SoloVox | sinshu | github | MIT | — | — | — | synth |
| 1643 | SopranoSax | sinshu | github | MIT | — | — | — | synth |
| 1644 | Soundfont - FluidR3 GM (20011225) | newzik | github | MIT | ✓ | — | — | synth |
| 1645 | Soundtrack | sinshu | github | MIT | — | — | — | synth |
| 1646 | SpaceVoice | sinshu | github | MIT | — | — | — | synth |
| 1647 | SquareWave | sinshu | github | MIT | — | — | — | synth |
| 1648 | Standard | sinshu | github | MIT | — | — | — | synth |
| 1649 | StarTheme | sinshu | github | MIT | — | — | — | synth |
| 1650 | SteelGtr | sinshu | github | MIT | — | — | — | synth |
| 1651 | SuperSmallFont | Wh1teDuke | github | MIT | ✓ | — | — | synth |
| 1652 | SweepPad | sinshu | github | MIT | — | — | — | synth |
| 1653 | SynthBass1 | sinshu | github | MIT | — | — | — | synth |
| 1654 | SynthBass2 | sinshu | github | MIT | — | — | — | synth |
| 1655 | SynthCalliope | sinshu | github | MIT | — | — | — | synth |
| 1656 | SynthVox | sinshu | github | MIT | — | — | — | synth |
| 1657 | Taiko | sinshu | github | MIT | — | — | — | synth |
| 1658 | Telephone1 | sinshu | github | MIT | — | — | — | synth |
| 1659 | TenorSax | sinshu | github | MIT | — | — | — | synth |
| 1660 | Timpani | sinshu | github | MIT | — | — | — | synth |
| 1661 | TinkleBell | sinshu | github | MIT | — | — | — | synth |
| 1662 | Tofurkey | Malaclypse the Younger | sfzinstruments | MIT | — | — | — | synth |
| 1663 | TR-808 | sinshu | github | MIT | — | — | — | synth |
| 1664 | TremoloStr | sinshu | github | MIT | — | — | — | synth |
| 1665 | Trombone | sinshu | github | MIT | — | — | — | synth |
| 1666 | Tuba | sinshu | github | MIT | — | — | — | synth |
| 1667 | TubularBell | sinshu | github | MIT | — | — | — | synth |
| 1668 | Vibraphone | sinshu | github | MIT | — | — | — | synth |
| 1669 | Viola | sinshu | github | MIT | — | — | — | synth |
| 1670 | VoiceOohs | sinshu | github | MIT | — | — | — | synth |
| 1671 | WarmPad | sinshu | github | MIT | — | — | — | synth |
| 1672 | Whistle | sinshu | github | MIT | — | — | — | synth |
| 1673 | Woodblock | sinshu | github | MIT | — | — | — | synth |
| 1674 | Xylophone | sinshu | github | MIT | — | — | — | synth |
| 1675 | Oohs | gregogiudici | github | MIT | ✓ | 0.1 MB | — | vocal |
| 1676 | KBH Real and Swelling Choirs | lfz | musical-artifacts | CC BY | ✓ | — | 37872 | vocal |
| 1677 | Papelmedia Final SF2 XXL - Irina Brochin | Simon Tristan Papel | polyphone | CC BY | ✓ | — | 3376 | vocal |
| 1678 | Discord Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 3140 | vocal |
| 1679 | Sampled Choir Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — | 1540 | vocal |
| 1680 | Korg Choir Ahhs | Quodlibet | polyphone | CC BY | ✓ | — | 1248 | vocal |
| 1681 | Papelmedia Final SF2 XXL - Aaa-Choir | Simon Tristan Papel | polyphone | CC BY | ✓ | — | 959 | vocal |
| 1682 | Choir MMMH Female | Xiaosu Du | polyphone | CC BY | ✓ | — | 782 | vocal |
| 1683 | Hallelujah | — | polyphone | CC BY | — | — | 648 | vocal |
| 1684 | Boy choir | Phil Camp | polyphone | CC BY | ✓ | — | 623 | vocal |
| 1685 | DT Kawkaw soundfont | — | polyphone | CC BY | ✓ | — | 341 | vocal |
| 1686 | HQ Bruh Soundfont | — | polyphone | CC BY | ✓ | — | 195 | vocal |
| 1687 | The Choral Soundfont Pack Freemium | Rick Blues from RE MEDIA PRODU | musical-artifacts | CC BY 3.0 | ✓ | — | 0 | vocal |
| 1688 | Clarinet | gregogiudici | github | MIT | ✓ | 0.1 MB | — | wind |
| 1689 | Tenor Saxophone | gregogiudici | github | MIT | ✓ | 0.3 MB | — | wind |
| 1690 | harmonica soundfont | TheSoundfontMaker | musical-artifacts | CC BY 3.0 | — | — | 4936 | wind |
| 1691 | Harmonica | gregogiudici | github | MIT | ✓ | — | — | wind |

## 六、F3 · 相同方式共享（有传染性：CC BY-SA / GPL） · 全量 60 条

> 本档**逐条列明**：名称 / 作者 / 来源 / 许可 / 是否 `.sf2` / 体积 / 下载量 / 分类。

| # | 名称 | 作者 | 来源 | 许可 | .sf2 | 体积 | 下载 | 分类 |
|---:|---|---|---|---|---:|---|---:|---|
| 1 | BJDNielPercussions | Yi Yunseok | sfzinstruments | CC BY-SA 4.0 | — | 4.2 MB | — | drum |
| 2 | Salamander Drumkit | Alexander Holm | sfzinstruments | CC BY-SA 3.0 | — | 7.0 MB | — | drum |
| 3 | Brazilian Bateria Percussion | JasperCodes | github | GPL v3 | ✓ | 10.3 MB | — | drum |
| 4 | Melodic Cuica Soundfont | Sizz Tuna | musical-artifacts | CC BY-SA | ✓ | — | 3447 | drum |
| 5 | Musyng Kite | SynthFont Viena | archive | CC BY-SA 3.0 | — | — | — | drum |
| 6 | Sam's Sonor | Sam Greene | sfzinstruments | CC BY-SA 4.0 | — | — | — | drum |
| 7 | Kay 5-String Banjo | FlameStudios | sfzinstruments | GPL v3 | — | 425.0 MB | — | ethnic |
| 8 | Kalimba Soundfont | Sizz Tuna | musical-artifacts | CC BY-SA | ✓ | — | 3002 | ethnic |
| 9 | OPL-3 FM 128M Soundfont | Zandro Reveille | musical-artifacts | CC BY-SA | ✓ | 113.2 MB | 49476 | game |
| 10 | Hedsound's MT32 Soundfont (CM64-L / LAPC-1) [GM remap fix with MSB127  | stgiga, hakerg, Ziya Mete Demi | musical-artifacts | CC BY-SA | ✓ | — | 37765 | game |
| 11 | RetroHybrid! | strixSF2 | musical-artifacts | GPL v3 | ✓ | — | 14863 | game |
| 12 | Sonic 4 Episode 2 Soundfont | Mildanner | musical-artifacts | GPL v2 | ✓ | — | 1665 | game |
| 13 | CMI Orchestra Hit SOUNDFONT | Max Gianelli | musical-artifacts | GPL | ✓ | — | 871 | game |
| 14 | Megaman Zero GM Soundfont | 0P | musical-artifacts | GPL v3 | ✓ | — | 850 | game |
| 15 | F-Zero GM Soundfont | 0P | musical-artifacts | GPL v3 | ✓ | — | 820 | game |
| 16 | Final Fantasy VI Advance GM Soundfont | 0P | musical-artifacts | GPL v3 | ✓ | — | 474 | game |
| 17 | FreePats General MIDI percussion set | FreePats project | FreePats | GPL v3 | ✓ | 15.0 MB | — | gm |
| 18 | FreePats General MIDI set | FreePats project | FreePats | GPL v3 | ✓ | 227.0 MB | — | gm |
| 19 | BalancedGM 1 | sleaf | musical-artifacts | GPL v3 | ✓ | — | 9168 | gm |
| 20 | NanoGM | SG studio | musical-artifacts | CC BY-SA | ✓ | — | 149 | gm |
| 21 | ColomboGMGS2 SoundFont v15.0 | W. Duwindu Tharinda Perera | archive | CC BY-SA 4.0 | — | — | — | gm |
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
| 43 | lesserdevil Soundfonts 1/3 | JSDay | archive | CC BY-SA 3.0 | — | — | — | other |
| 44 | lsrdvl_Soundfonts-2 | JSDay | archive | CC BY-SA 3.0 | — | — | — | other |
| 45 | Realistic Soundfont V2: Libre Edition | SonicLover 19, sleaf | musical-artifacts | CC BY-SA | — | — | 0 | other |
| 46 | SoundFont Collection for Linux | — | archive | CC BY-SA 4.0 | — | — | — | other |
| 47 | ULTIMATE CAUSTIC PRESETS COLLECTION 7 GB MIRROR | Caustic3Archive | archive | CC BY-SA 4.0 | — | — | — | other |
| 48 | piano | ThomasKiljanczykDev | github | GPL v3 | — | 2.4 MB | — | piano |
| 49 | LivingRoom Upright - Micro SFZ | KeyPleezer | sfzinstruments | CC BY-SA 4.0 | — | 107.0 MB | — | piano |
| 50 | Keppy's Steinway Piano (Version 5.2) | KaleidonKep99 & Frozen Snow Pr | musical-artifacts | CC BY-SA | — | — | 32674 | piano |
| 51 | Freepats Rhodes | Unknown | musical-artifacts | GPL | ✓ | — | 6488 | piano |
| 52 | sine | ssankko | github | GPL v3 | ✓ | — | — | piano |
| 53 | GeneralUser GS 1.35 | Piskocis | github | GPL v3 | ✓ | 25.4 MB | — | synth |
| 54 | GeneralUser-GS | ItalianJoker | github | GPL v3 | ✓ | 30.8 MB | — | synth |
| 55 | Supersaw Collection 2 | Strix SF2 | musical-artifacts | GPL v3 | ✓ | — | 11017 | synth |
| 56 | ReVintage World | Elf of Happy and Love, mirrore | musical-artifacts | GPL v3 | ✓ | — | 3584 | synth |
| 57 | Mpj  vocal collection, my voice | Milton Paredes, mpj factory st | musical-artifacts | CC BY-SA | ✓ | — | 7745 | vocal |
| 58 | STYVELL ORCHESTRA SOUNDFONT SAXO-ALTO-VIB-FF | olof | musical-artifacts | CC BY-SA | ✓ | — | 13764 | wind |
| 59 | STYVELL ORCHESTRA SOUNDFONT SAXO-SOPRANO-FF | olof | musical-artifacts | CC BY-SA | ✓ | — | 8120 | wind |
| 60 | STYVELL ORCHESTRA SOUNDFONT SAXO-SOPRANO-VIB-FF | olof | musical-artifacts | CC BY-SA | ✓ | — | 8051 | wind |

## 七、F4 · **不收录** · 全量 1050 条（**逐条写明为什么不收录**）

| # | 名称 | 作者 | 来源 | 许可 | 分类 | 不收录原因 |
|---:|---|---|---|---|---|---|
| 1 | Terkelsen's Marimba | Lars Terkelsen, S Christia | sfzinstruments | 未标注 | drum | **未标注许可** → 许可不明即不收录 |
| 2 | E-MU Classic Series Vol. 6 - World Percussion/Ensembles (WAV | E-mu | archive | 未标注 | drum | **未标注许可** → 许可不明即不收录 |
| 3 | Ultimate Guitar Kit V2 | Gregjazz | archive | 未标注 | drum | **未标注许可** → 许可不明即不收录 |
| 4 | Upward Movement Drums | — | archive | 未标注 | drum | **未标注许可** → 许可不明即不收录 |
| 5 | florestan-subset | paladin-t | github | 未标注 | game | **未标注许可** → 许可不明即不收录 |
| 6 | ins | paladin-t | github | 未标注 | game | **未标注许可** → 许可不明即不收录 |
| 7 | Game Boy Drum Kit | Bedroom Producers Blog | sfzinstruments | 未标注 | game | **未标注许可** → 许可不明即不收录 |
| 8 | 8bit | paladin-t | github | 未标注 | game | **未标注许可** → 许可不明即不收录 |
| 9 | MFB Tanzbar Drum Samples | Wave Alchemy | sfzinstruments | 未标注 | game | **未标注许可** → 许可不明即不收录 |
| 10 | GeneralUser | ad-si | github | 未标注 | game | **未标注许可** → 许可不明即不收录 |
| 11 | Anti-Piracy Measures In Fire Emblem: The Sacred Stones (FE8) | Epholo8 | archive | 未标注 | game | **未标注许可** → 许可不明即不收录 |
| 12 | Apotos Daytime / Windmill Isle ( Touhou Soundfont) | SEGA | archive | 未标注 | game | **未标注许可** → 许可不明即不收录 |
| 13 | Bonetrousle SNES Remix - Undertale (EarthBound 16 Bit Soundf | Bulby | archive | 未标注 | game | **未标注许可** → 许可不明即不收录 |
| 14 | Deltarune Rude Buster ( Pokemon B 2 W 2 Soundfont) | — | archive | 未标注 | game | **未标注许可** → 许可不明即不收录 |
| 15 | Doom Snes | — | archive | 未标注 | game | **未标注许可** → 许可不明即不收录 |
| 16 | Fallen by Evanescence but it's in the SM64 soundfont | KannaBis420 | archive | 未标注 | game | **未标注许可** → 许可不明即不收录 |
| 17 | FNF: Vs. CatNap- DogDay's SF (Original!!!!) | BrenTheCat, Austin The Dal | archive | 未标注 | game | **未标注许可** → 许可不明即不收录 |
| 18 | Killing Mood ( BOSS 2) [ SEGAudio] 144bpm Dm | — | archive | 未标注 | game | **未标注许可** → 许可不明即不收录 |
| 19 | Little Einsteins - Theme Song (Super Mario SNES Soundfont) | Billy Straus | archive | 未标注 | game | **未标注许可** → 许可不明即不收录 |
| 20 | Mediatek Startup and Shutdown Tones in Spreadtrum Soundfont | New Some Phonez Videos | archive | 未标注 | game | **未标注许可** → 许可不明即不收录 |
| 21 | minimal_gs | libraz | github | 未标注 | game | **未标注许可** → 许可不明即不收录 |
| 22 | MX Deltarune - Chaos King (Touhou Style Arrange) | Soundfont Arranger | archive | 未标注 | game | **未标注许可** → 许可不明即不收录 |
| 23 | My Aquarium - WiiWare - MIDI and Soundfont Rip | Hudson Soft | archive | 未标注 | game | **未标注许可** → 许可不明即不收录 |
| 24 | Nintendo Wii Channel Soundfont | idk | archive | 未标注 | game | **未标注许可** → 许可不明即不收录 |
| 25 | Over The River And Through The Wood (Super Mario SNES Soundf | Lydia Marie Child, Nintend | archive | 未标注 | game | **未标注许可** → 许可不明即不收录 |
| 26 | Pokemon Mystery Dungeon Explorers Of Sky Full Soundfont | — | archive | 未标注 | game | **未标注许可** → 许可不明即不收录 |
| 27 | Realistic Soundfont V 2 Libre V 1 ( 16bit) Sub 2 Gi B.sf 2.7 | — | archive | 未标注 | game | **未标注许可** → 许可不明即不收录 |
| 28 | Roland D-70 Tones and Waveforms SoundFont | — | archive | 未标注 | game | **未标注许可** → 许可不明即不收录 |
| 29 | Samsung SGH-A437 tones (Samsung Soundfont demo) | Floomsy Tech | archive | 未标注 | game | **未标注许可** → 许可不明即不收录 |
| 30 | Sega Genesis | — | archive | 未标注 | game | **未标注许可** → 许可不明即不收录 |
| 31 | Sonic Pinball Party Midi + SoundFont Rip | Sonic Team | archive | 未标注 | game | **未标注许可** → 许可不明即不收录 |
| 32 | Soundfonts for VGM | — | archive | 未标注 | game | **未标注许可** → 许可不明即不收录 |
| 33 | South Park's Parents: Magic Alliance (Nintendo DS) soundfont | Parker-stone Interactive S | archive | 未标注 | game | **未标注许可** → 许可不明即不收录 |
| 34 | South Park: Read and Play (2008 Nintendo DS release) Soundfo | Parker-stone Interactive S | archive | 未标注 | game | **未标注许可** → 许可不明即不收录 |
| 35 | Southern Park's Parents (2001, Gameboy Advance/PlayStation 2 | Parker-stone Interactive S | archive | 未标注 | game | **未标注许可** → 许可不明即不收录 |
| 36 | Super Mario SNES Soundfont | Erika Furudo, Koji Kondo | archive | 未标注 | game | **未标注许可** → 许可不明即不收录 |
| 37 | The Definitive FNF Soundfont (ALL CHARACTERS + EXTRAS) | SuperStamps | archive | 未标注 | game | **未标注许可** → 许可不明即不收录 |
| 38 | The DELTARUNE Music Sample List | — | archive | 未标注 | game | **未标注许可** → 许可不明即不收录 |
| 39 | The Ultimate LG Mobile Ringtones Archive - Software and Soun | LG | archive | 未标注 | game | **未标注许可** → 许可不明即不收录 |
| 40 | The Wellington March - Doraemon: Nobita And The 3 Fairy Spir | Stephanie Kim, Wilhelm Zeh | archive | 未标注 | game | **未标注许可** → 许可不明即不收录 |
| 41 | tiny | not-hanjo-mei | github | 未标注 | game | **未标注许可** → 许可不明即不收录 |
| 42 | Touhou | — | archive | 未标注 | game | **未标注许可** → 许可不明即不收录 |
| 43 | Touhou soundfonts | — | archive | 未标注 | game | **未标注许可** → 许可不明即不收录 |
| 44 | TurboGrafx-16/PC Engine + Extras (NES And SMS) | — | archive | 未标注 | game | **未标注许可** → 许可不明即不收录 |
| 45 | tv room - sonic spinball soundfont 👀 | tv room | archive | 未标注 | game | **未标注许可** → 许可不明即不收录 |
| 46 | ファノンパーク GO GO! 真夜中の逃走 (GBA) Soundfont ~ Demos + Resources | Parker-Stone Interactive S | archive | 未标注 | game | **未标注许可** → 许可不明即不收录 |
| 47 | TimGM6mb | — | fluidsynth | 未标注 | gm | **未标注许可** → 许可不明即不收录 |
| 48 | SGM Soundfont Archive | Shan | archive | 未标注 | gm | **未标注许可** → 许可不明即不收录 |
| 49 | Shan SGM Pro / X64 / X28 / ES8 Soundfont | Shan | archive | 未标注 | gm | **未标注许可** → 许可不明即不收录 |
| 50 | E-MU Classic Series Vol. 17 – Heavy Guitars (WAV, Soundfont) | E-mu | archive | 未标注 | guitar | **未标注许可** → 许可不明即不收录 |
| 51 | Guitar sound font pack | — | archive | 未标注 | guitar | **未标注许可** → 许可不明即不收录 |
| 52 | I found the full sample of Megalovania's/Earthbound's guitar | ASmolBoy | archive | 未标注 | guitar | **未标注许可** → 许可不明即不收录 |
| 53 | Jackson Distortion Guitar Soundfont | Jack Butler | archive | 未标注 | guitar | **未标注许可** → 许可不明即不收录 |
| 54 | RESOLUTE SYMPHONY | StanleyTremblayMusic | archive | 未标注 | guitar | **未标注许可** → 许可不明即不收录 |
| 55 | Steinberg Virtual Guitarist + VG Electric Edition VST x86 Wi | Steinberg | archive | 未标注 | guitar | **未标注许可** → 许可不明即不收录 |
| 56 | Xploshi - The actual strumming sound added to a virtual guit | Xploshi | archive | 未标注 | guitar | **未标注许可** → 许可不明即不收录 |
| 57 | [Various Mirrors] SF2 and/or SFZ (and a few NKI) conversions | Ensoniq, Various users | archive | 未标注 | hist | **未标注许可** → 许可不明即不收录 |
| 58 | Creative Labs / EMU - Soundfont CD II | Creative Labs | archive | 未标注 | hist | **未标注许可** → 许可不明即不收录 |
| 59 | E-MU Classic Series Vol. 2 - More Emulator Standards (WAV, S | E-mu | archive | 未标注 | hist | **未标注许可** → 许可不明即不收录 |
| 60 | KORG M1 Waveforms Soundfont | KORG | archive | 未标注 | hist | **未标注许可** → 许可不明即不收录 |
| 61 | Roland SC-55 Soundfont | — | archive | 未标注 | hist | **未标注许可** → 许可不明即不收录 |
| 62 | Roland SC-55 Soundfont by EmperorGrieferus | EmperorGrieferus | archive | 未标注 | hist | **未标注许可** → 许可不明即不收录 |
| 63 | Roland SC-55 Soundfonts | I created these soundfonts | archive | 未标注 | hist | **未标注许可** → 许可不明即不收录 |
| 64 | Roland Sound Canvas SC-55 Soundfont | EmperorGrieferus | archive | 未标注 | hist | **未标注许可** → 许可不明即不收录 |
| 65 | Roland Sound Canvas SoundFont ( 24 Bit XGD Edition) | W. Duwindu Tharinda Perera | archive | 未标注 | hist | **未标注许可** → 许可不明即不收录 |
| 66 | Roland U-110 (SL-01 Pipe Organ And Harpsicord) | Roland | archive | 未标注 | hist | **未标注许可** → 许可不明即不收录 |
| 67 | Roland U-110 (SL-02 Latin And FX Percussions) | Roland | archive | 未标注 | hist | **未标注许可** → 许可不明即不收录 |
| 68 | Roland U-110 (SL-04 Electric Grand and Clavi) | Roland | archive | 未标注 | hist | **未标注许可** → 许可不明即不收录 |
| 69 | Roland U-110 (SL-05 Orchestral Strings) | Roland | archive | 未标注 | hist | **未标注许可** → 许可不明即不收录 |
| 70 | Roland U-110 (SL-09 Guitar and Keyboards) | Roland | archive | 未标注 | hist | **未标注许可** → 许可不明即不收录 |
| 71 | Roland U-110 (SL-10 Rock Drums) | Roland | archive | 未标注 | hist | **未标注许可** → 许可不明即不收录 |
| 72 | Roland U-110 (SL-11 Sound Effects) | Roland | archive | 未标注 | hist | **未标注许可** → 许可不明即不收录 |
| 73 | Roland U-110 Internal | Roland | archive | 未标注 | hist | **未标注许可** → 许可不明即不收录 |
| 74 | Roland U-220 (SL-01 Pipe Organ and Harpsicord) | Roland | archive | 未标注 | hist | **未标注许可** → 许可不明即不收录 |
| 75 | Roland U-220 (SL-03 Ethnic) | Roland | archive | 未标注 | hist | **未标注许可** → 许可不明即不收录 |
| 76 | Roland U-220 (SL-04 Electric Grand and Clavi) | Roland | archive | 未标注 | hist | **未标注许可** → 许可不明即不收录 |
| 77 | Roland U-220 (SL-06 Orchestral Winds) | Roland | archive | 未标注 | hist | **未标注许可** → 许可不明即不收录 |
| 78 | Roland U-220 (SL-07 Electric Guitar) | Roland | archive | 未标注 | hist | **未标注许可** → 许可不明即不收录 |
| 79 | S90ES Soundfont | Henrique Gogó | archive | 未标注 | hist | **未标注许可** → 许可不明即不收录 |
| 80 | Virtual Playing Orchestra | Paul Battersby | sfzinstruments | 未标注 | orch | **未标注许可** → 许可不明即不收录 |
| 81 | Aegean Symphonic Orchestra v2.5 universal | — | fluidsynth | 未标注 | orch | **未标注许可** → 许可不明即不收录 |
| 82 | Sonatina Symphonic Orchestra | — | fluidsynth | 未标注 | orch | **未标注许可** → 许可不明即不收录 |
| 83 | 1 HQ Orchestral Soundfont Collection V 2.0 | — | archive | 未标注 | orch | **未标注许可** → 许可不明即不收录 |
| 84 | Best Service - Orchestral Colours (1994) With Unused Sounds! | Best Service | archive | 未标注 | orch | **未标注许可** → 许可不明即不收录 |
| 85 | Digidesign Sample Cell Factory Brass | Digidesign | archive | 未标注 | orch | **未标注许可** → 许可不明即不收录 |
| 86 | Digidesign Sample Cell Factory Strings Soundfont | Digidesign | archive | 未标注 | orch | **未标注许可** → 许可不明即不收录 |
| 87 | E-MU Classic Series Vol. 3 - Orchestral (WAV, Soundfont) | E-mu | archive | 未标注 | orch | **未标注许可** → 许可不明即不收录 |
| 88 | E-MU Classic Series Vol. 9 - Psychic Horns (WAV, Soundfont) | E-mu | archive | 未标注 | orch | **未标注许可** → 许可不明即不收录 |
| 89 | CFaz Keys IV (3s Release, No-Pan) | mbms0 | github | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 90 | CFaz Keys IV (No-Pan) | mbms0 | github | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 91 | CFaz Keys IV (Old Tuned, 3s Release, No-Pan) | mbms0 | github | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 92 | CFaz Keys IV (Old Tuned, No-Pan) | mbms0 | github | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 93 | CFaz Keys IV (Random Offset) | mbms0 | github | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 94 | CFaz Keys IV (Random Offset, 3s Release) | mbms0 | github | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 95 | CFaz Keys IV (Random Offset, 3s Release, No-Pan) | mbms0 | github | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 96 | CFaz Keys IV (Random Offset, No-Pan) | mbms0 | github | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 97 | GB | kmatze | github | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 98 | CFaz Keys IV | mbms0 | github | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 99 | CFaz Keys IV (3s Release) | mbms0 | github | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 100 | CFaz Keys IV (Old Tuned) | mbms0 | github | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 101 | CFaz Keys IV (Old Tuned, 3s Release) | mbms0 | github | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 102 | FluidR3_GS | Jacalz | github | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 103 | soundbank | 59de44955ebd | github | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 104 | FluidR3 | Jacalz | github | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 105 | Salamander C5 Light | — | fluidsynth | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 106 | S. Christian Collins GeneralUser GS | — | fluidsynth | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 107 | 233_poprockbank | Rezonality | github | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 108 | Magic Sound Font, version 2.0 | — | fluidsynth | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 109 | Fluid (R3) General MIDI SoundFont (GM) | — | fluidsynth | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 110 | Arachno SoundFont, version 1.0 | — | fluidsynth | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 111 | "Lost" SoundFonts | stgiga, et. al. | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 112 | "WST 25 FStein 00 Sep 22" Soundfont | Warren Trachtman | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 113 | (REUPLOAD) SC 55 Sound Font V 1.2b | The SF2 file was created b | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 114 | 0x 39 D 5 F Mii Maker ( CTR N HEDE) ( U) Midi & Soundfont. 7 | 0x 39 D 5 F Mii Maker ( CT | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 115 | 1930 1970 Music Soundfont | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 116 | 4Kids TV Soundfont (UNOFFICIAL AND INSPIRED) | Ralph Dion Shuckett, John  | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 117 | 500 Soundfonts Collection - Full GM Sets, SF2 Pack | Musicially-inclined indivi | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 118 | 541-soundfonts-full-gm-sets | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 119 | 909 Day! Mystery Soundfont Demo with TR-909 | David "SgtPepperArc360" Eg | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 120 | A Soundfont Spectacular Christmas | Stephanie Kim | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 121 | Ace Attorney J 4 All Psyche Locks | Seba 20 90 | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 122 | Aladdin And The Adventure Of All-Time (Movie Based Un-Offici | Ferris Ellen Gluck, Mary E | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 123 | ALL IN ONE Android App Soundfont Collection | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 124 | Almost Paradise: Benevolence | Digital Jockey | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 125 | alphabet soundfont | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 126 | alpineairplane | 👁👁👁 | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 127 | Andy Hopper Soundfont MIDI Collection | Frank Gari And Let's Go Lu | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 128 | ASI_Symlink_All_In_One | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 129 | Baby Einstein Soundfont (Version 3) | Baby Einstein, The Baby Ei | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 130 | Bad Mii Theme Soundfont | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 131 | BARCHboi_OS (mini sample pack) | BARCHboi | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 132 | Beach House - Space Song (Super Mario 64 Soundfont) | on4word | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 133 | BEETLEJUICE MAIN TITLES But In The PVZ Soundfont | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 134 | Ben 10: Protector of Earth (DS) SoundFont | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 135 | Best General MIDI soundfonts collection | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 136 | Bittercold (Phase 2) - Pokémon Mystery Dungeon: Gates to Inf | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 137 | Black And White Soundfonts V 3 | hnturs12 | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 138 | Bloons DSiWare Soundfont | MarioW | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 139 | boards of canada - kid for today (animal crossing soundfont) | psych | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 140 | Boop (Roblox Animal Hospital) | TGaming03 | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 141 | Bruh Soundfont | me | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 142 | Bubble's Hotel - Soundfont (V1, FIXED) | Bubble's Hotel, Tiny Pop | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 143 | Canon Lexus 185 Soundfont | Canon | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 144 | Captain Claw (1997) - Full OST (CLAW4.SF2 Soundfont) | Virgin Snake | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 145 | Cassette Girl Soundfont | charlesmb | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 146 | CFaz Keys IV (Extended Layers) | mbms0 | github | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 147 | CFaz Keys IV (Extended Layers, 3s Release) | mbms0 | github | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 148 | CFaz Keys IV (Extended Layers, 3s Release, No-Pan) | mbms0 | github | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 149 | CFaz Keys IV (Extended Layers, No-Pan) | mbms0 | github | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 150 | CFaz Keys IV (No Layers) | mbms0 | github | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 151 | CFaz Keys IV (No Layers, 3s Release) | mbms0 | github | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 152 | CFaz Keys IV (No Layers, 3s Release, No-Pan) | mbms0 | github | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 153 | CFaz Keys IV (No Layers, No-Pan) | mbms0 | github | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 154 | Complete Sound Canvas SC-88 Pro Soundfont Collection | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 155 | Cookie Run: OvenBreak MIDIs (Pre-Season 6) | Devsisters | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 156 | Cope Land — Spyro Custom Tracks & Remakes Archive | Cope Land | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 157 | Cradle Of Filth Mannequin! ( With Pokémon Ruby And Sapphire  | Midian-P | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 158 | Crash Bandicoot Midi & Soundfont [by Crash Zone] | Crash Bandicoot Zone | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 159 | Crash Bandicoot PS1 Sounds and MIDIs Collection | OxidizedResult | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 160 | Crash Twinsanity 3D Java Game OST - Full Soundtrack (Nokia S | Sonic 25 | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 161 | Creative Labs SoundBlaster Live!5.1 Driver CD | Creative Technologies Ltd. | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 162 | Creative Sound Blaster AWE 64 Plug And Play | Creative Labs | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 163 | Creative Sound Blaster AWE64 Gold - Complete CD Set (Install | Creative Labs | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 164 | Cumbia Soundfont SF2 | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 165 | Daft Punk - Get Lucky ft. Pharrell but with the SM64 soundfo | verymilkee | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 166 | Death Grips - I've Seen Footage (DK Rap / DK64 Soundfont) | on4word | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 167 | DOOM E1M1 (OSRS Soundfont) | Brian Espinoza / ICFreeze | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 168 | Dope Soundfonts | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 169 | Dora the Explorer: Soundfont Collection (WIP) | Steve Sandberg | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 170 | Dream Sam 2133b | Karaoke Player Soundfont | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 171 | E-MU Classic Series Vol. 10 – Elements of Sound 1MB (WAV, So | E-mu | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 172 | E-MU Classic Series Vol. 12 – ESI 32 150 MB Production Sound | E-mu | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 173 | E-MU Classic Series Vol. 8 - Vintage (WAV, Soundfont) | E-mu | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 174 | EAPCI8M soundfont converted to SF2 | Borg Number One | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 175 | Ed Harrison - 'Nimbus' Stems/Samples | Ed Harrison | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 176 | Essential Keys Sforzando V 9.6 | unsure. | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 177 | Fairlight CMI Series IIx Factory Disks. 7z | Fairlight Instruments, Pty | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 178 | Falcosoft MIDI Player v5.8 Stable | Falcosoft | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 179 | Fanon Park Nostalgia Soundfont ~ PREMIUM EDITION – Demo File | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 180 | Fanon Park Nostalgia Soundfonts ~ Demo Files | PROJECT FANON PARK | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 181 | Fanon Park SoundFonts ~ demo files | PROJECT FANON PARK | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 182 | Fat Boy GM/GS SoundFont v0.790 | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 183 | Fatalize RSE Soundfont | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 184 | FatBoy SoundFont (.sf2) v0.790 | Unknown | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 185 | Finding Nemo: Escape To The Big Blue (DS) Soundfont | Disney, Pixar | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 186 | Fluid R3 Mobile GM Soundfont | Frank Wen | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 187 | FluidR3 GM+GS Soundfont | Frank Wen | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 188 | FluidR3_GM | Jacalz | github | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 189 | Free Soundfonts (2019 - 2026) [HD, HQ] | Owen Deane, Shylin Deane,  | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 190 | free soundfonts sf2 2019-04 | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 191 | free-soundfonts | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 192 | free-soundfonts-sf2 | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 193 | Friggin Mouse SF2 Pack | datonerylsguy | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 194 | Funky Karts Official Soundfont | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 195 | Gangsta Rap - Ni**a Ni**a Ni**a (SMA2 Soundfont) | yodel boi | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 196 | General MIDI SoundFonts for the Sound Blaster Family startin | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 197 | General Montage Soundfont | Daindune | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 198 | generalmanual 000010765 | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 199 | generalmanual 000021094 | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 200 | generalmanual 000021196 | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 201 | Gigapack 1 & 2 (Soundfont) | Best Service | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 202 | God Bless America! (Imagine: Figure Skater And Ice Champions | Irving Berlin, Stephanie K | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 203 | Gravis Ultrasound Classic Pach Set V 1.6 (SF2) | ArekR | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 204 | H G F Sounds Uc Seq Loops01 | HGFortune, Paule Amca | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 205 | Home - We're Finally Landing (Super Mario 64 Soundfont) | on4word | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 206 | Hotel Mario Soundfont | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 207 | I'd Like To Teach The World To Sing (Super Mario 64 Soundfon | Billy Davis, Billy Backer, | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 208 | It's Green (SC-55) | Lee Jackson | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 209 | iteachvader-01-02-2023 | iteachvader | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 210 | Itsy's List of Soundfonts and Samples | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 211 | Kid Pix Undo Guy SoundFont & .wav Samples | Behelit | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 212 | Kingdom Hearts Soundfont & MIDI Archive | Exabyte U, not me, Musical | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 213 | Laugh and Learn - The ("Un-Official") Soundfont | Timothy Steven Clarke, Nic | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 214 | Leap-Font SYNs and MIDIs | LeapFrog Enterprises, Inc. | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 215 | Live HQ Natural Sound Font GM | UnderxPipe1985 | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 216 | Londonderry Air/Danny Boy ( M&L: PiT Soundfont) | Fred Weatherly, Stephanie  | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 217 | Manuel Xavier - Divina CreaciÃ³n Humana | Manuel Xavier | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 218 | Mario Kart Super Circuit - Snow Land (LeapFrog Leap-font) | Minako Hamano | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 219 | Mario Paint - Gnat Attack Boss (LeapFrog Leap-fomt) | Hirokazu Tanaka | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 220 | Mario Party 3 - Music Selection (LeapFrog Leap-font) | Ichiro Shimakura, Jeanne P | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 221 | Mega Man Zero 1 4 Soundfont ( VER 1) | Jordan Moore | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 222 | MIDI and Soundfont Archive Favorites | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 223 | Midi Editor 3.3.0 Setup | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 224 | MIDI SF2 Soundfonts (Mys1, Mys2, Mys3) | Unknown | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 225 | MIDNIGHT HORROR SCHOOL Soundfont ~ demo files | MILKY CARTOON ltd. | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 226 | Miko Soundfont! | Kn1ghtNight uPic | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 227 | misc remix .flp archive | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 228 | Music for The New CER Two | Kaylor Blakley | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 229 | My Downloaded MIDI's & Soundfonts File Collection | Lando Johnson | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 230 | My Soundfont Collection | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 231 | Mystery dungeon Fanmade Ost | Franson Langinbelik | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 232 | Mystery Soundfont - you won't guess! | David "SgtPepperArc360" Eg | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 233 | Mystic Island Soundfont ~ SPECIAL EDITION (demos and resourc | Village Roadshow, Imagine  | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 234 | Neonight Soundfont | charlesmb | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 235 | New Super Mario Bros. Music (LeapFrog Leap-font) | Koji Kondo, Brad Fuller | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 236 | New Super Mario Bros. U (2012 Soundfont) | Koji Kondo, Nintendo | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 237 | Nirvana In Utero SM 64 Soundfont | @somethingisreal on YouTub | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 238 | Nirvana Nevermind SM64 soundfont | @somethingisreal on YouTub | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 239 | Nirvana's Nevermind but with the SM64 soundfont (flac) | Something is real | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 240 | Nokia 3110c (Lloyd Bank) Soundfont | Nokia | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 241 | Not bad. Finally found the #soundfont I like. Arachno. I kno | Kenneth Udut | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 242 | Nuero Fantasy | Barchboi | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 243 | OHAGI Official Soundfont | Enoki_1997 | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 244 | OKeys | Henrique Gogó | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 245 | Online Sequencer - Soundfont V1.0 | Online Sequencer | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 246 | OnpuFONT 2026 Edition (Demos and resources) | MILKY CARTOON Ltd. | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 247 | Original Kids Soundfonts | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 248 | OST - SimCity 2000 (Mac OS Soundfont) | Maxis | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 249 | Paper Mario 64 Soundfont | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 250 | Passport.mid - PC Audacious - Arachno SoundFont Version 1.0 | Petr Mach | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 251 | Patch93's SC-55 Soundfont | Patch93 | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 252 | Paul Speer & David Lanz - Behind The Waterfall (SM64 Soundfo | Unknown | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 253 | Perfect Nothing (SMRPG SoundFont Remix) ://: Cutila-Mun | Florageist / Hyacinth Orch | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 254 | Phoenix Soundfont | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 255 | Pkmn XY Spundfont | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 256 | plugins for old video games | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 257 | PMD Explorers Of Sky Full Soundfont | u/RatelRaichu | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 258 | Pocoyo Soundfont V 1 | MasonMasterMusic | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 259 | Pokémon Emerald Soundfont | Game Freak | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 260 | Professor Layton and the Big Dog (ProZD Animated) | DearestHershel | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 261 | Pudata in the Big City soundfont (SF2) | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 262 | Quadratic Rainbow | scarecrow_ | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 263 | Rayman: Band Land - Super Mario 64 DS Soundfont | Biker Wolf Chip | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 264 | Recursos Soundfonts CDROM | Pulsesar | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 265 | Remixes | Me | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 266 | Reviews SHENMUE | NOMOIDA | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 267 | Roarsputin (Rasputin / SM64 Soundfont) | Deadz64 | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 268 | Robrin Soundfont Examples | Robrin Sound | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 269 | Sammy Soundfont | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 270 | Sapphire S 274.7z | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 271 | SC 55 | Roland | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 272 | Serial Experiments Lain PS 1 Soundfont Ver. 0.1 | kju, Tsuruoka Yota, Kasama | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 273 | SF2 Collection | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 274 | Sforzatron | Plogue | sfzinstruments | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 275 | SFPack v1.0.0.4 | Megota Software | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 276 | sfz | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 277 | SFZ Pack. 7z | 白いチャンネル | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 278 | Small Friends, Big Tales: Suzy's Music Box Soumdfonts ~ demo | UrChinchillaElcie | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 279 | Smash Bandicoot's Random Chromatics | Smash Bandicoot | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 280 | Soccer Shootout Soundfont | TheJosh347 | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 281 | Sound Blaster Live! MP3+ 5.1 CD-ROMs | Creative | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 282 | Sound Font / Sf 2 | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 283 | Sound Fonts The Collection. 7z | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 284 | soundfont and MIDI collection | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 285 | Soundfont collection 2 | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 286 | Soundfont collection 3 | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 287 | Soundfont Collection Download | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 288 | Soundfont Spectacular Presents: The Classics | Stephanie Kim | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 289 | soundfont.sf2 | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 290 | SoundFonts | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 291 | Soundfonts Collection | DJJMB1 | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 292 | Soundfonts-collection-anapan.ca-2024-misc | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 293 | Southern Park: Read and Play (2001 PC release) Soundfonts ~  | Parker-Stone Interactive S | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 294 | Spreadtrum Mocor 12C Soundfonts | UNISOC | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 295 | Strawberry Shortcake Soundfont Collection | Andy Street | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 296 | Super Black Parade 64 - My Chemical Romance / Super Mario So | Microplastic Brain | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 297 | Super Mario 64 Midis And Soundfont | Pablo's Corner + Unknown M | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 298 | Super Mario 64 Midis And Soundfont | Pablo's Corner | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 299 | Super Mario 64 Resources | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 300 | Super Mario 64 Soundfont by sm64pie | sm64pie | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 301 | Super Mario Bros. 2 - Soundtrack (Leap-font/LeapFrog Toys So | Koji Kondo, Brad Fuller | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 302 | SVM7570 Generator V10B | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 303 | TADC - Your New Home - SM64 Soundfont ❨V2❩-[aO8q2iP5XoM] | Garfield, VeeDoesStuff1 | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 304 | TCF And Star Wars Theme Soundfont Footage Part 3 | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 305 | TCF And Star Wars Theme Soundfont Footage Part 3 | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 306 | TCF And Star Wars Theme Soundfont Footage Part 3 V 2 | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 307 | Terratec Audio System EWS 64 L XL Drivers, Applications, Ed! | Terratec | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 308 | The Amazing Digital Circus : Your New Home - SM64 Soundfont  | Garfield, VeeDoesStuff1 | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 309 | The Art Of SoundFont Creation | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 310 | The Athletic (Eek!) - [SMW Athletic Theme in Eek's Soundfont | Lou | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 311 | The Beatles' Magical Mystery Tour (LeapFrog Leap-font Soundf | The Beatles, Brad Fuller,  | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 312 | The Gods of Windows 2000 RnJesus0 | Rn_Jesus0 | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 313 | The Kingston & Atounku Movie - Inspired Soundfont (PUBLIC BE | Cosmodra, ZyntraBox Media | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 314 | The New Original Kids + Douglas and Company Soundfont (Ver.  | Original Kids Productions, | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 315 | The Southern Park High School Survival Guide Instruments ~ S | Parker-stone Interactive S | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 316 | The Ultimate Earthbound Soundfont | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 317 | The ULTIMATE LeapFrog Leap-font ( 4 Instrument Packs) | LeapFrog Enterprises | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 318 | Thomas and Friends 1984 Classic Series theme (with PBS Kids  | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 319 | Timidity++ Soundfont [for Opentouch] | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 320 | Toy Xylophone V2 Low Octave Preset With Split Points | TheSoundfontMaker | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 321 | toy_xylophone_V2_soundfont_fixed | TheSoundfontMaker | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 322 | Trevor0402's SC-55 Soundfont | Trevor0402 | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 323 | TurboGrafx-16 Soundfont (PC-Engine Soundfont) | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 324 | TURKISH-ARAB3 (.sf2) soundfont | [unknown] | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 325 | tv room - good soundfont names | tv room | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 326 | Ultimate Midnight Animal Show Soundfonts (Ver. 2.0!) ~ demo  | MILKY CARTOON Ltd. | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 327 | Utopia Soundfont Collection | Utopia Sound Division | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 328 | Video Game Mashups - NSMB: Desert Theme (4 Soundfont Mashup) | Asuka Ota, Hajime Wakai, K | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 329 | Viena SoundFont Editor 0.800 | SynthFont | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 330 | Viena SoundFont Editor 0.992 | SynthFont | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 331 | Vintage Celesta Soundfont (SFZ) - Michael Pitcher Music | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 332 | Vintage Dream Waves 2.0.1 Restored | Ian Wilson | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 333 | Visions of the MIDI Beyond | The MIDIvishnu Orchestra | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 334 | Welson Symphony SFZ | Flipperwaldt | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 335 | whatever soundfonts | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 336 | wind96 - Plume Valley | Windows96 | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 337 | Windows MIDI Demos: OPL-3_FM_128M soundfont | Microsoft Corporation | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 338 | XMplayer. 7z | — | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 339 | XP50HOUZ | jdm7dv | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 340 | Yoshi Story 64 Soundfont | Reza Khadafi | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 341 | 『恋愛サーキュレーション』を Newスーパーマリオブラザーズ 風にアレンジ | にす | archive | 未标注 | other | **未标注许可** → 许可不明即不收录 |
| 342 | Arataki's Great and Glorious Drum | StarryCosmosPiano | github | 未标注 | piano | **未标注许可** → 许可不明即不收录 |
| 343 | Djem Djem Drum | StarryCosmosPiano | github | 未标注 | piano | **未标注许可** → 许可不明即不收录 |
| 344 | Ukulele | StarryCosmosPiano | github | 未标注 | piano | **未标注许可** → 许可不明即不收录 |
| 345 | GeneralUserGS | pinkpixel-dev | github | 未标注 | piano | **未标注许可** → 许可不明即不收录 |
| 346 | Lingering Euphonia | StarryCosmosPiano | github | 未标注 | piano | **未标注许可** → 许可不明即不收录 |
| 347 | Lingering Euphonia (Original with Chords) | StarryCosmosPiano | github | 未标注 | piano | **未标注许可** → 许可不明即不收录 |
| 348 | Ukulele (Original with Chords) | StarryCosmosPiano | github | 未标注 | piano | **未标注许可** → 许可不明即不收录 |
| 349 | Windsong Lyre | StarryCosmosPiano | github | 未标注 | piano | **未标注许可** → 许可不明即不收录 |
| 350 | Leaping Spirit Piano | StarryCosmosPiano | github | 未标注 | piano | **未标注许可** → 许可不明即不收录 |
| 351 | Vodyanitsa | StarryCosmosPiano | github | 未标注 | piano | **未标注许可** → 许可不明即不收录 |
| 352 | Harmonic Keys | StarryCosmosPiano | github | 未标注 | piano | **未标注许可** → 许可不明即不收录 |
| 353 | Floral Zither | StarryCosmosPiano | github | 未标注 | piano | **未标注许可** → 许可不明即不收录 |
| 354 | Nightwind Horn | StarryCosmosPiano | github | 未标注 | piano | **未标注许可** → 许可不明即不收录 |
| 355 | Vintage Lyre | StarryCosmosPiano | github | 未标注 | piano | **未标注许可** → 许可不明即不收录 |
| 356 | Nice-Steinway-Lite-v3.0 | ales-tsurko | github | 未标注 | piano | **未标注许可** → 许可不明即不收录 |
| 357 | Church Steinway | Pianobook | sfzinstruments | 未标注 | piano | **未标注许可** → 许可不明即不收录 |
| 358 | Estate Grand LE | Production Voices | sfzinstruments | 未标注 | piano | **未标注许可** → 许可不明即不收录 |
| 359 | Piano in 162 | Ivy Audio | sfzinstruments | 未标注 | piano | **未标注许可** → 许可不明即不收录 |
| 360 | Amethyst Imperial Grand - Imperial Hall | mbms0 | github | 未标注 | piano | **未标注许可** → 许可不明即不收录 |
| 361 | Amethyst Imperial Grand - Imperial Hall - Strings Accompanim | mbms0 | github | 未标注 | piano | **未标注许可** → 许可不明即不收录 |
| 362 | Amethyst Imperial Grand - Studio | mbms0 | github | 未标注 | piano | **未标注许可** → 许可不明即不收录 |
| 363 | Amethyst Imperial Grand - Studio - Strings Accompaniment | mbms0 | github | 未标注 | piano | **未标注许可** → 许可不明即不收录 |
| 364 | Cathan Concert Grand | mbms0 | github | 未标注 | piano | **未标注许可** → 许可不明即不收录 |
| 365 | Cathan Concert Grand (Long Release) | mbms0 | github | 未标注 | piano | **未标注许可** → 许可不明即不收录 |
| 366 | Cathan Concert Grand (Long Release, No Pan) | mbms0 | github | 未标注 | piano | **未标注许可** → 许可不明即不收录 |
| 367 | Cathan Concert Grand (No Pan) | mbms0 | github | 未标注 | piano | **未标注许可** → 许可不明即不收录 |
| 368 | Cathan Concert Grand - Detuned | mbms0 | github | 未标注 | piano | **未标注许可** → 许可不明即不收录 |
| 369 | Cathan Concert Grand - Detuned (Long Release) | mbms0 | github | 未标注 | piano | **未标注许可** → 许可不明即不收录 |
| 370 | Cathan Concert Grand - Detuned (Long Release, No Pan) | mbms0 | github | 未标注 | piano | **未标注许可** → 许可不明即不收录 |
| 371 | Cathan Concert Grand - Detuned (No Pan) | mbms0 | github | 未标注 | piano | **未标注许可** → 许可不明即不收录 |
| 372 | Cathan Concert Grand - Random Offset | mbms0 | github | 未标注 | piano | **未标注许可** → 许可不明即不收录 |
| 373 | Cathan Concert Grand - Random Offset (Long Release) | mbms0 | github | 未标注 | piano | **未标注许可** → 许可不明即不收录 |
| 374 | Cathan Concert Grand - Random Offset (Long Release, No Pan) | mbms0 | github | 未标注 | piano | **未标注许可** → 许可不明即不收录 |
| 375 | Cathan Concert Grand - Random Offset (No Pan) | mbms0 | github | 未标注 | piano | **未标注许可** → 许可不明即不收录 |
| 376 | SGM V 2.01 Compact Grand Guit Bass V 2.7 | — | archive | 未标注 | piano | **未标注许可** → 许可不明即不收录 |
| 377 | Southerncafe24's Toy Piano + Lyre Soundfont ~ demo files | The Southerncafe24 Project | archive | 未标注 | piano | **未标注许可** → 许可不明即不收录 |
| 378 | The Super Mario Bros 2 Piano | The Super Mario Bros 2 | archive | 未标注 | piano | **未标注许可** → 许可不明即不收录 |
| 379 | Warren S. Trachtman - Steinway Model-C Soundfont | Warren S. Trachtman | archive | 未标注 | piano | **未标注许可** → 许可不明即不收录 |
| 380 | Timbres Of Heaven GM_GS_XG_SFX V 3.4 | — | fluidsynth | 未标注 | sfx | **未标注许可** → 许可不明即不收录 |
| 381 | VintageDreams | fcarvajalbrown | github | 未标注 | synth | **未标注许可** → 许可不明即不收录 |
| 382 | florestan-subset | fynv | github | 未标注 | synth | **未标注许可** → 许可不明即不收录 |
| 383 | florestan-subset | fynv | github | 未标注 | synth | **未标注许可** → 许可不明即不收录 |
| 384 | florestan-subset | Wally869 | github | 未标注 | synth | **未标注许可** → 许可不明即不收录 |
| 385 | TimGM6mbEdit | chipweinberger | github | 未标注 | synth | **未标注许可** → 许可不明即不收录 |
| 386 | soundfont | Electric-ray | github | 未标注 | synth | **未标注许可** → 许可不明即不收录 |
| 387 | GeneralUserGS | spessasus | github | 未标注 | synth | **未标注许可** → 许可不明即不收录 |
| 388 | GeneralUser GS v1.471 | arkark2010arkark | github | 未标注 | synth | **未标注许可** → 许可不明即不收录 |
| 389 | GeneralUser_GS_SoftSynth_v1.44 | arkark2010arkark | github | 未标注 | synth | **未标注许可** → 许可不明即不收录 |
| 390 | GeneralUser-GS | Misterscan | github | 未标注 | synth | **未标注许可** → 许可不明即不收录 |
| 391 | GeneralUser_GS | fcarvajalbrown | github | 未标注 | synth | **未标注许可** → 许可不明即不收录 |
| 392 | Amazound DXJD Synths Vol 1 Huge Pads (SOUNDFONTS) | Amazound, Roland | archive | 未标注 | synth | **未标注许可** → 许可不明即不收录 |
| 393 | Custom instrumental variant of Dragon Tales theme with leapf | — | archive | 未标注 | synth | **未标注许可** → 许可不明即不收录 |
| 394 | dummy | sinshu | github | 未标注 | synth | **未标注许可** → 许可不明即不收录 |
| 395 | GS For HTF ( Redmi Oct) Soundfont | — | archive | 未标注 | synth | **未标注许可** → 许可不明即不收录 |
| 396 | test_empty_samples | sinshu | github | 未标注 | synth | **未标注许可** → 许可不明即不收录 |
| 397 | GeneralUserGS | birkeeper | github | 未标注 | vocal | **未标注许可** → 许可不明即不收录 |
| 398 | Choir_practice | birkeeper | github | 未标注 | vocal | **未标注许可** → 许可不明即不收录 |
| 399 | Radiohead - Follow Me Around From The Lost Woods (Ocarina of | on4word | archive | 未标注 | wind | **未标注许可** → 许可不明即不收录 |
| 400 | Crisis General Midi v3.01 | Christophe MARICOURT | polyphone | CC BY-NC | gm | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 401 | Timbres Of Heaven v3.4 Final | Don Allen | polyphone | CC BY-NC | gm | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 402 | Steinway Grand Piano | Soeren Bovbjerg | polyphone | CC BY-NC | piano | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 403 | Titanic 200 GM-GS v1.2 | Luke Sena - Titanic Soundf | polyphone | CC BY-NC | gm | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 404 | Jeux 1.4 | John W. McCoy | polyphone | CC BY-NC | organ | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 405 | Wario Land 4 | — | polyphone | CC BY-NC | other | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 406 | Musyng Kite | Sarcyan | polyphone | CC BY-NC | gm | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 407 | Yamaha PSR-F50 Piano | — | polyphone | CC BY-NC | piano | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 408 | Sonic the Hedgehog (Prototype) Soundfont | Mildanner, ProjectFM, Sega | musical-artifacts | CC BY-NC | game | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 409 | Korg WAVESTATION Vektor Organ Soundfont | Mildanner, KORG | musical-artifacts | CC BY-NC | hist | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 410 | G-Town church organ | Tobias Margerber | polyphone | CC BY-NC | organ | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 411 | MSM Soundfonts volume 5 | — | polyphone | CC BY-NC | ethnic | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 412 | Arachno soundfont | Maxime Abbey | polyphone | CC BY-NC | gm | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 413 | ROLAND SC - 55 | — | polyphone | CC BY-NC | other | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 414 | Banjo | — | polyphone | CC BY-NC | orch | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 415 | RJV Grand Piano.sf2 | — | polyphone | CC BY-NC | piano | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 416 | AnttuBrass v2 | Andreas Åkesson | polyphone | CC BY-NC | orch | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 417 | Sub Bass | — | polyphone | CC BY-NC | synth | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 418 | N-Grand piano | — | polyphone | CC BY-NC | piano | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 419 | Lute collections | — | polyphone | CC BY-NC | orch | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 420 | Penny Whistles and Recorders | — | polyphone | CC BY-NC | orch | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 421 | UoI Trumpet NV4 looped | Cmdratz | polyphone | CC BY-NC | orch | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 422 | pads | — | polyphone | CC BY-NC | piano | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 423 | MSM Percussion | — | polyphone | CC BY-NC | ethnic | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 424 | Modern EP1 Technics sx-KN7000 (SF2) [V. I. Music / iKorgPa / | — | polyphone | CC BY-NC | piano | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 425 | Green positive | — | polyphone | CC BY-NC | organ | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 426 | G-Town church Stomps | Tobias Margerber | polyphone | CC BY-NC | sfx | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 427 | 60´s EP | — | polyphone | CC BY-NC | piano | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 428 | Rubber Band Bass | — | polyphone | CC BY-NC | guitar | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 429 | yabeep.1.1.sf2 (Yet another beep sound font) | — | polyphone | CC BY-NC | synth | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 430 | BUBSY in: Claws Encounters of the Furred Kind (GS) | — | polyphone | CC BY-NC | hist | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 431 | Coral sitar | — | polyphone | CC BY-NC | orch | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 432 | CMX.3.1 | — | polyphone | CC BY-NC | hist | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 433 | Xyster | — | polyphone | CC BY-NC | orch | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 434 | SNES LookALike SF2. | — | polyphone | CC BY-NC | synth | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 435 | Grand So Fi Piano | — | polyphone | CC BY-NC | hist | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 436 | Gold | Jens Walther Jacobsen | polyphone | CC BY-NC | other | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 437 | Lycaoe&#039;s Soundfont I (Mono) | — | polyphone | CC BY-NC | piano | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 438 | G-Town church bass drum | Tobias Margerber | polyphone | CC BY-NC | drum | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 439 | Nexus - PanFlute | — | polyphone | CC BY-NC | orch | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 440 | G-Town church cymbals | Tobias Margerber | polyphone | CC BY-NC | drum | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 441 | My piano | — | polyphone | CC BY-NC | piano | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 442 | my soundfonts collection | — | polyphone | CC BY-NC | ethnic | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 443 | G-Town church ensemble snare | Tobias Margerber | polyphone | CC BY-NC | drum | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 444 | 3D Maze Man (1997 PC Game) | — | polyphone | CC BY-NC | hist | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 445 | MeMeMe | — | polyphone | CC BY-NC | piano | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 446 | cps2 | — | polyphone | CC BY-NC | synth | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 447 | BIONICLE Heroes (GBA) | — | polyphone | CC BY-NC | synth | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 448 | 2023 Recreation of 8-Bit Soundfont Project | — | polyphone | CC BY-NC | other | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 449 | The Legend of Zelda: A Link to the Past | — | polyphone | CC BY-NC | game | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 450 | Maltigi Scream | — | polyphone | CC BY-NC | piano | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 451 | YOU BITCH | — | polyphone | CC BY-NC | vocal | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 452 | Random ahh soundfont | — | polyphone | CC BY-NC | piano | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 453 | Cutie Mew Mew Magic - Hatsune Miku | — | polyphone | CC BY-NC | game | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 454 | homework | — | polyphone | CC BY-NC | guitar | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 455 | Benjo | — | polyphone | CC BY-NC | synth | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 456 | Sitar | — | polyphone | CC BY-NC | orch | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 457 | Freaking bell | — | polyphone | CC BY-NC | drum | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 458 | SpongeBob SquarePants: The Yellow Avenger | — | polyphone | CC BY-NC | other | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 459 | FoxOG / Fennec PC Soundfont | — | polyphone | CC BY-NC | synth | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 460 | Body Percussion | — | polyphone | CC BY-NC | drum | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 461 | spongebob the movie gba | — | polyphone | CC BY-NC | gm | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 462 | K | — | polyphone | CC BY-NC | hist | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 463 | El chavo the elephant never forgets  song | — | polyphone | CC BY-NC | gm | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 464 | side pocket snes | — | polyphone | CC BY-NC | sfx | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 465 | Lilo &amp;amp; Stitch gba | — | polyphone | CC BY-NC | gm | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 466 | LloydHigh | — | polyphone | CC BY-NC | synth | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 467 | super bomber man 4 e 5 samples | — | polyphone | CC BY-NC | gm | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 468 | madagascar 2 | — | polyphone | CC BY-NC | gm | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 469 | F | — | polyphone | CC BY-NC | sfx | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 470 | Aegean Symphonic Orchestra sf2 | Ziya Mete Demircan | musical-artifacts | CC BY-NC | gm | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 471 | LEGO Racers Soundfont | T1G3R | archive | CC BY-NC | other | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 472 | The Soul Hackers Soundfont | ATLUS | archive | CC BY-NC | other | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 473 | jRhodes3d | Jeff Learman | sfzinstruments | CC BY-NC | piano | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 474 | Salamander C5 Light sf2 | Ziya Mete Demircan | musical-artifacts | CC BY-NC | piano | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 475 | Equinox Grand Pianos | Shan | polyphone | 未识别码 by-nc-nd | piano | 许可不允许再分发 |
| 476 | Emperador Classic Concert Grand Piano | — | polyphone | 未识别码 by-nc-nd | piano | 许可不允许再分发 |
| 477 | vieuxmac.early.musical.instrument.v2.3.4.sf2 (circa A=430 Hz | — | polyphone | 未识别码 by-nc-nd | synth | 许可不允许再分发 |
| 478 | Maganda piano | Robert C. Allen | polyphone | 未识别码 by-nc-nd | piano | 许可不允许再分发 |
| 479 | grand E piano | — | polyphone | 未识别码 by-nc-nd | piano | 许可不允许再分发 |
| 480 | Diamond Man Soundfont | — | polyphone | 未识别码 by-nc-nd | vocal | 许可不允许再分发 |
| 481 | Tinpots Piano V2 | — | polyphone | 未识别码 by-nc-nd | hist | 许可不允许再分发 |
| 482 | animaniacs snes | — | polyphone | 未识别码 by-nc-nd | piano | 许可不允许再分发 |
| 483 | phineas and ferb ds | — | polyphone | 未识别码 by-nc-nd | other | 许可不允许再分发 |
| 484 | phineas and ferb 2d dimension ds | — | polyphone | 未识别码 by-nc-nd | other | 许可不允许再分发 |
| 485 | The DEFINITIVE MEGALOVANIA Soundfont! V1.19 | Willie Aton | musical-artifacts | CC BY-NC-ND 3.0 | game | NC-ND：禁商用且禁改作 → 我们不代管、不直链 |
| 486 | Christian Zell Harpsichord 1737 (Equal temperament) | Pere Casulleras | musical-artifacts | CC BY-NC-ND 3.0 | other | NC-ND：禁商用且禁改作 → 我们不代管、不直链 |
| 487 | Christian Zell Harpsichord 1737 (Original fifth-comma meanto | Pere Casulleras | musical-artifacts | CC BY-NC-ND 3.0 | other | NC-ND：禁商用且禁改作 → 我们不代管、不直链 |
| 488 | Dr. Mario 64 Soundfont | Mildanner, Nintendo | musical-artifacts | CC BY-NC-ND 3.0 | game | NC-ND：禁商用且禁改作 → 我们不代管、不直链 |
| 489 | chiptunes | Saynal | archive | CC BY-NC-ND 3.0 | game | NC-ND：禁商用且禁改作 → 我们不代管、不直链 |
| 490 | Sonic 3 (Prototype) Credits (Touhou Soundfont Remix) | Eternal Archivist 17 | archive | CC BY-NC-ND 3.0 | game | NC-ND：禁商用且禁改作 → 我们不代管、不直链 |
| 491 | Sonic 3 Credits Theme (Touhou Soundfont Remix) | Eternal Archivist 17 | archive | CC BY-NC-ND 3.0 | game | NC-ND：禁商用且禁改作 → 我们不代管、不直链 |
| 492 | DREAM FRANCE SOUND MODULE SOUNDFONTS BLASTER | Dream France | archive | CC BY-NC-ND 3.0 | other | NC-ND：禁商用且禁改作 → 我们不代管、不直链 |
| 493 | Limit Sound Field Expand | Various Artists | archive | CC BY-NC-ND 3.0 | other | NC-ND：禁商用且禁改作 → 我们不代管、不直链 |
| 494 | loopool soundfont collection | loopool / Jean-Paul Garnie | archive | CC BY-NC-ND 3.0 | other | NC-ND：禁商用且禁改作 → 我们不代管、不直链 |
| 495 | old 1904 door bell soundfont V2 | TheSoundfontMaker | archive | CC BY-NC-ND 3.0 | other | NC-ND：禁商用且禁改作 → 我们不代管、不直链 |
| 496 | on4word - Selected Aphex Works N64 | on4word | archive | CC BY-NC-ND 3.0 | other | NC-ND：禁商用且禁改作 → 我们不代管、不直链 |
| 497 | The Mega Musical Soundfont | SandisBergvalds2008 | archive | CC BY-NC-ND 3.0 | other | NC-ND：禁商用且禁改作 → 我们不代管、不直链 |
| 498 | Unicom 62172 Door Chime soundfont V4 [UPDATED] | Unicom | archive | CC BY-NC-ND 3.0 | other | NC-ND：禁商用且禁改作 → 我们不代管、不直链 |
| 499 | Saxophone (PKMN BW) | — | archive | CC BY-NC-ND 3.0 | wind | NC-ND：禁商用且禁改作 → 我们不代管、不直链 |
| 500 | Titanic 200 GM-GS v1.2 | Luke Sena - Titanic Soundf | musical-artifacts | CC BY-NC-SA | other | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 501 | VirtuOrgan Soundfont | Fernando A. Martin | musical-artifacts | CC BY-NC-SA | organ | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 502 | Caed's Ultimate Adequate GM Version 1.00 (3.97 GB GM Soundfo | Caed | musical-artifacts | CC BY-NC-SA | gm | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 503 | Falcosoft Midi Player 5.7 | Falcosoft | archive | CC BY-NC-SA | other | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 504 | jRhodes3c | Jeff Learman | sfzinstruments | CC BY-NC-SA | piano | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 505 | Sonic 4 Ep. 1 & 2 Accurate Drum (Soundfont Port) | Mildanner, Speedy the Dog | musical-artifacts | CC BY-NC-SA 3.0 | game | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 506 | MF Tin Whistle | Markus Fiedler | sfzinstruments | CC BY-NC-SA 3.0 | ethnic | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 507 | Rickenbacker 4001 | Project 16 | sfzinstruments | CC BY-NC-SA 3.0 | guitar | NC 系列：禁止商业使用 → 我们不代管、不直链 |
| 508 | Orpheus GM V1.047e | Virtuon | musical-artifacts | CC BY-ND（禁改作） | orch | **ND 禁改作**：音色的主要用途就是衍生（用采样做音乐/改编）→ 收录会误导使用者 |
| 509 | Emperador House Organ 1 | — | polyphone | CC BY-ND（禁改作） | organ | **ND 禁改作**：音色的主要用途就是衍生（用采样做音乐/改编）→ 收录会误导使用者 |
| 510 | Violin Old Serrano | Jason Serrano | polyphone | CC BY-ND（禁改作） | orch | **ND 禁改作**：音色的主要用途就是衍生（用采样做音乐/改编）→ 收录会误导使用者 |
| 511 | Note Blocks - A Minecraft Soundfont | — | polyphone | CC BY-ND（禁改作） | other | **ND 禁改作**：音色的主要用途就是衍生（用采样做音乐/改编）→ 收录会误导使用者 |
| 512 | Spongebob fratic sf2 and Some midis | — | polyphone | CC BY-ND（禁改作） | gm | **ND 禁改作**：音色的主要用途就是衍生（用采样做音乐/改编）→ 收录会误导使用者 |
| 513 | Spongebob the yellow avengers | — | polyphone | CC BY-ND（禁改作） | synth | **ND 禁改作**：音色的主要用途就是衍生（用采样做音乐/改编）→ 收录会误导使用者 |
| 514 | My Singing Monsters Shimmer / Ceng-Ceng | — | polyphone | CC BY-ND（禁改作） | sfx | **ND 禁改作**：音色的主要用途就是衍生（用采样做音乐/改编）→ 收录会误导使用者 |
| 515 | Casio PT-82/PT-87 Tone Pack | — | polyphone | CC BY-ND（禁改作） | other | **ND 禁改作**：音色的主要用途就是衍生（用采样做音乐/改编）→ 收录会误导使用者 |
| 516 | Baritone Saxophone | — | polyphone | CC BY-ND（禁改作） | orch | **ND 禁改作**：音色的主要用途就是衍生（用采样做音乐/改编）→ 收录会误导使用者 |
| 517 | Just t4, yamaha tyros 4 gm soundfont | Milton Paredes, MP factory | musical-artifacts | CC Sampling（整包分发受限） | hist | CC Sampling 系列：整包原样再分发受限（仅非商业）→ 只给来源 |
| 518 | Sonatina Symphonic Orchestra (Full SF2) | SonicLover 19 | musical-artifacts | CC Sampling（整包分发受限） | orch | CC Sampling 系列：整包原样再分发受限（仅非商业）→ 只给来源 |
| 519 | Sonatina Symphonic Orchestra | Mattias Westlund | musical-artifacts | CC Sampling（整包分发受限） | orch | CC Sampling 系列：整包原样再分发受限（仅非商业）→ 只给来源 |
| 520 | G-Town Church Sampling Project (kontakt) | Tobias Marberger | musical-artifacts | CC Sampling（整包分发受限） | drum | CC Sampling 系列：整包原样再分发受限（仅非商业）→ 只给来源 |
| 521 | MrSanic's (me) NES Soundfont | MrSanic | musical-artifacts | CC Sampling（整包分发受限） | game | CC Sampling 系列：整包原样再分发受限（仅非商业）→ 只给来源 |
| 522 | Mellowtron | j_e_f_f_g | musical-artifacts | CC Sampling（整包分发受限） | other | CC Sampling 系列：整包原样再分发受限（仅非商业）→ 只给来源 |
| 523 | Sonic Adventure Soundfont | Redhotsupermario, SEGA for | musical-artifacts | CC Sampling（整包分发受限） | other | CC Sampling 系列：整包原样再分发受限（仅非商业）→ 只给来源 |
| 524 | Sonatina Symphonic Orchestra | Mattias Westlund, Peter Ea | sfzinstruments | CC Sampling Plus 1.0 | orch | CC Sampling Plus 1.0：整包原样再分发仅限非商业 → 只给来源 |
| 525 | G-Town Church Sampling Project | Tobias Marberger | sfzinstruments | CC Sampling Plus 1.0 | other | CC Sampling Plus 1.0：整包原样再分发仅限非商业 → 只给来源 |
| 526 | Ghana Drums | Karoryfer Samples | sfzinstruments | 商业授权 / 付费产品 | drum | 商业授权 / 需付费购买 |
| 527 | Tubular Bells II | Versilian Studios LLC | sfzinstruments | 商业授权 / 付费产品 | drum | 商业授权 / 需付费购买 |
| 528 | Castanets | TKDrums | sfzinstruments | 商业授权 / 付费产品 | drum | 商业授权 / 需付费购买 |
| 529 | RawCowbell | TKDrums | sfzinstruments | 商业授权 / 付费产品 | drum | 商业授权 / 需付费购买 |
| 530 | Simple Tamb | TKDrums | sfzinstruments | 商业授权 / 付费产品 | drum | 商业授权 / 需付费购买 |
| 531 | Turkish Rebab | Karoryfer Samples | sfzinstruments | 商业授权 / 付费产品 | ethnic | 商业授权 / 需付费购买 |
| 532 | Fourth Tagelharpa | Karoryfer Samples | sfzinstruments | 商业授权 / 付费产品 | ethnic | 商业授权 / 需付费购买 |
| 533 | Kemençe Of The Black Sea | Karoryfer Samples | sfzinstruments | 商业授权 / 付费产品 | ethnic | 商业授权 / 需付费购买 |
| 534 | Nanfo | Karoryfer Samples | sfzinstruments | 商业授权 / 付费产品 | ethnic | 商业授权 / 需付费购买 |
| 535 | Three Tagelharpas | Karoryfer Samples | sfzinstruments | 商业授权 / 付费产品 | ethnic | 商业授权 / 需付费购买 |
| 536 | World Instruments | Garritan | sfzinstruments | 商业授权 / 付费产品 | ethnic | 商业授权 / 需付费购买 |
| 537 | (various) | Wave Alchemy | sfzinstruments | 商业授权 / 付费产品 | game | 商业授权 / 需付费购买 |
| 538 | (various) | Samples From Mars | sfzinstruments | 商业授权 / 付费产品 | game | 商业授权 / 需付费购买 |
| 539 | Beefowulf Bass | Karoryfer Samples | sfzinstruments | 商业授权 / 付费产品 | guitar | 商业授权 / 需付费购买 |
| 540 | Karniszbass | Karoryfer Samples | sfzinstruments | 商业授权 / 付费产品 | guitar | 商业授权 / 需付费购买 |
| 541 | Glockenskull Guitar | Karoryfer Samples | sfzinstruments | 商业授权 / 付费产品 | guitar | 商业授权 / 需付费购买 |
| 542 | Secret Agent Guitar | Karoryfer Samples | sfzinstruments | 商业授权 / 付费产品 | guitar | 商业授权 / 需付费购买 |
| 543 | Surfkiss | Karoryfer Samples | sfzinstruments | 商业授权 / 付费产品 | guitar | 商业授权 / 需付费购买 |
| 544 | Baconwulf | Karoryfer Samples | sfzinstruments | 商业授权 / 付费产品 | guitar | 商业授权 / 需付费购买 |
| 545 | Secret Agent Bass | Karoryfer Samples | sfzinstruments | 商业授权 / 付费产品 | guitar | 商业授权 / 需付费购买 |
| 546 | Snowkiss Guitar | Karoryfer Samples | sfzinstruments | 商业授权 / 付费产品 | guitar | 商业授权 / 需付费购买 |
| 547 | VG Soul Trumpet | VGTrumpet | sfzinstruments | 商业授权 / 付费产品 | orch | 商业授权 / 需付费购买 |
| 548 | VG Trumpet Harmon muted | VGTrumpet | sfzinstruments | 商业授权 / 付费产品 | orch | 商业授权 / 需付费购买 |
| 549 | VG Trombone | VGTrumpet | sfzinstruments | 商业授权 / 付费产品 | orch | 商业授权 / 需付费购买 |
| 550 | VG Soprano Saxophone | VGTrumpet | sfzinstruments | 商业授权 / 付费产品 | orch | 商业授权 / 需付费购买 |
| 551 | VG Tenor Saxophone | VGTrumpet | sfzinstruments | 商业授权 / 付费产品 | orch | 商业授权 / 需付费购买 |
| 552 | VG Clarinet | VGTrumpet | sfzinstruments | 商业授权 / 付费产品 | orch | 商业授权 / 需付费购买 |
| 553 | VG Flugelhorn | VGTrumpet | sfzinstruments | 商业授权 / 付费产品 | orch | 商业授权 / 需付费购买 |
| 554 | VG Alto Saxophone | VGTrumpet | sfzinstruments | 商业授权 / 付费产品 | orch | 商业授权 / 需付费购买 |
| 555 | Vengeful Viola | Karoryfer Samples | sfzinstruments | 商业授权 / 付费产品 | orch | 商业授权 / 需付费购买 |
| 556 | Vengeful Violin | Karoryfer Samples | sfzinstruments | 商业授权 / 付费产品 | orch | 商业授权 / 需付费购买 |
| 557 | Merciful Cello | Karoryfer Samples | sfzinstruments | 商业授权 / 付费产品 | orch | 商业授权 / 需付费购买 |
| 558 | Strange String Summer | Karoryfer Samples | sfzinstruments | 商业授权 / 付费产品 | orch | 商业授权 / 需付费购买 |
| 559 | Vengeful Cello | Karoryfer Samples | sfzinstruments | 商业授权 / 付费产品 | orch | 商业授权 / 需付费购买 |
| 560 | Vengeful Bass | Karoryfer Samples | sfzinstruments | 商业授权 / 付费产品 | orch | 商业授权 / 需付费购买 |
| 561 | All SFZ Bundle | VGTrumpet | sfzinstruments | 商业授权 / 付费产品 | orch | 商业授权 / 需付费购买 |
| 562 | Harps | Garritan | sfzinstruments | 商业授权 / 付费产品 | orch | 商业授权 / 需付费购买 |
| 563 | Instant Orchestra | Garritan | sfzinstruments | 商业授权 / 付费产品 | orch | 商业授权 / 需付费购买 |
| 564 | Personal Orchestra 5 | Garritan | sfzinstruments | 商业授权 / 付费产品 | orch | 商业授权 / 需付费购买 |
| 565 | Concert and Marching Band 2 | Garritan | sfzinstruments | 商业授权 / 付费产品 | other | 商业授权 / 需付费购买 |
| 566 | Classic Series Collection | Versilian Studios LLC | sfzinstruments | 商业授权 / 付费产品 | other | 商业授权 / 需付费购买 |
| 567 | Orcophony | Karoryfer Samples | sfzinstruments | 商业授权 / 付费产品 | other | 商业授权 / 需付费购买 |
| 568 | Classic Pipe Organs | Garritan | sfzinstruments | 商业授权 / 付费产品 | other | 商业授权 / 需付费购买 |
| 569 | Jazz and Big Band 3 | Garritan | sfzinstruments | 商业授权 / 付费产品 | other | 商业授权 / 需付费购买 |
| 570 | The Halfling | Production Voices | sfzinstruments | 商业授权 / 付费产品 | other | 商业授权 / 需付费购买 |
| 571 | PiAnnette | fisound | sfzinstruments | 商业授权 / 付费产品 | piano | 商业授权 / 需付费购买 |
| 572 | Estate Grand | Production Voices | sfzinstruments | 商业授权 / 付费产品 | piano | 商业授权 / 需付费购买 |
| 573 | CFX Concert Grand | Garritan | sfzinstruments | 商业授权 / 付费产品 | piano | 商业授权 / 需付费购买 |
| 574 | CFX Lite | Garritan | sfzinstruments | 商业授权 / 付费产品 | piano | 商业授权 / 需付费购买 |
| 575 | Concert Grand Compact | Production Voices | sfzinstruments | 商业授权 / 付费产品 | piano | 商业授权 / 需付费购买 |
| 576 | Death Piano | Production Voices | sfzinstruments | 商业授权 / 付费产品 | piano | 商业授权 / 需付费购买 |
| 577 | Electric V | Production Voices | sfzinstruments | 商业授权 / 付费产品 | piano | 商业授权 / 需付费购买 |
| 578 | Production Grand Compact | Production Voices | sfzinstruments | 商业授权 / 付费产品 | piano | 商业授权 / 需付费购买 |
| 579 | Dandelion Witch | Karoryfer Samples | sfzinstruments | 商业授权 / 付费产品 | vocal | 商业授权 / 需付费购买 |
| 580 | Hadziha | Karoryfer Samples | sfzinstruments | 商业授权 / 付费产品 | vocal | 商业授权 / 需付费购买 |
| 581 | Hster | Karoryfer Samples | sfzinstruments | 商业授权 / 付费产品 | vocal | 商业授权 / 需付费购买 |
| 582 | Torgbe | Karoryfer Samples | sfzinstruments | 商业授权 / 付费产品 | vocal | 商业授权 / 需付费购买 |
| 583 | Hadzi-Hevi | Karoryfer Samples | sfzinstruments | 商业授权 / 付费产品 | vocal | 商业授权 / 需付费购买 |
| 584 | Hadzi-Fia | Karoryfer Samples | sfzinstruments | 商业授权 / 付费产品 | vocal | 商业授权 / 需付费购买 |
| 585 | The Megalovania Library V2 (FL Studio Mobile Compatible) | Micasddsa | musical-artifacts | 版权受限 | other | 版权受限（原权利人保留全部权利） |
| 586 | CT-7000 (Retro Synth) [Free Version] | Michael Picher | musical-artifacts | 版权受限 | game | 版权受限（原权利人保留全部权利） |
| 587 | Among Us Soundfont | Inky Nic | musical-artifacts | 版权受限 | game | 版权受限（原权利人保留全部权利） |
| 588 | Vintage Dreams Waves v 2.0 Soundfont | Ian Wilson | musical-artifacts | 版权受限 | synth | 版权受限（原权利人保留全部权利） |
| 589 | Cave Story Soundfont | Pixel | musical-artifacts | 版权受限 | game | 版权受限（原权利人保留全部权利） |
| 590 | Wurlitzer Soundfont | John R. Tay | musical-artifacts | 版权受限 | other | 版权受限（原权利人保留全部权利） |
| 591 | Wii Grand Piano (Sampled) | Created and ripped by MrSa | musical-artifacts | 版权受限 | game | 版权受限（原权利人保留全部权利） |
| 592 | Binaural Upright Piano | Michael Picher | musical-artifacts | 版权受限 | piano | 版权受限（原权利人保留全部权利） |
| 593 | Casio SA-76 (+GM Soundfont) | Casio Computer Co., Underx | musical-artifacts | 版权受限 | hist | 版权受限（原权利人保留全部权利） |
| 594 | SF2 Comp "GM" | Unknown | musical-artifacts | 版权受限 | other | 版权受限（原权利人保留全部权利） |
| 595 | Shreddage Zero | Unknown Creator For Soundf | musical-artifacts | 版权受限 | guitar | 版权受限（原权利人保留全部权利） |
| 596 | HS Synthetic Electronic v1.0 Soundfont | Thomas Hammer | musical-artifacts | 版权受限 | hist | 版权受限（原权利人保留全部权利） |
| 597 | HS Synth Collection I Soundfont | Thomas Hammer | musical-artifacts | 版权受限 | hist | 版权受限（原权利人保留全部权利） |
| 598 | TR-808 Drums Soundfont | Thomas Hammer | musical-artifacts | 版权受限 | drum | 版权受限（原权利人保留全部权利） |
| 599 | Ana gaby voice, Soundfont version. | Milton  Paredes, mpj facto | musical-artifacts | 版权受限 | vocal | 版权受限（原权利人保留全部权利） |
| 600 | HS TB-303 Soundfont | Thomas Hammer | musical-artifacts | 版权受限 | hist | 版权受限（原权利人保留全部权利） |
| 601 | Shreddage Soundfont Beta | Unknown Creator For Soundf | musical-artifacts | 版权受限 | guitar | 版权受限（原权利人保留全部权利） |
| 602 | amiga st20 lite soundfont | respective autorhts, and m | musical-artifacts | 版权受限 | game | 版权受限（原权利人保留全部权利） |
| 603 | HS Strings Soundfont | Thomas Hammer | musical-artifacts | 版权受限 | hist | 版权受限（原权利人保留全部权利） |
| 604 | Xhomie3 - Drums For Dubstep And HardStyle (SoundFonts) with  | Xhomie3 | musical-artifacts | 版权受限 | drum | 版权受限（原权利人保留全部权利） |
| 605 | HS M1 Drums Soundfont | Thomas Hammer | musical-artifacts | 版权受限 | drum | 版权受限（原权利人保留全部权利） |
| 606 | HS Pads and Textures II Soundfont | Thomas Hammer | musical-artifacts | 版权受限 | synth | 版权受限（原权利人保留全部权利） |
| 607 | HS Linn Drums Soundfont | Thomas Hammer | musical-artifacts | 版权受限 | drum | 版权受限（原权利人保留全部权利） |
| 608 | Kururin Paradise Soundfont | Nintendo/Eighting, ripped  | musical-artifacts | 版权受限 | gm | 版权受限（原权利人保留全部权利） |
| 609 | Cuckoo's Taped Piano SFZ (wav version) | Cuckoo Music | musical-artifacts | 版权受限 | piano | 版权受限（原权利人保留全部权利） |
| 610 | HS Boss DR-550 Drums Soundfont | Thomas Hammer | musical-artifacts | 版权受限 | drum | 版权受限（原权利人保留全部权利） |
| 611 | HS Acoustic Percussion Soundfont | Thomas Hammer | musical-artifacts | 版权受限 | drum | 版权受限（原权利人保留全部权利） |
| 612 | HS R8 Drums Soundfont | Thomas Hammer | musical-artifacts | 版权受限 | drum | 版权受限（原权利人保留全部权利） |
| 613 | Nena, gm soundfont set | Milton Paredes, mpj factor | musical-artifacts | 版权受限 | ethnic | 版权受限（原权利人保留全部权利） |
| 614 | Magic Techno Drums Soundfont | Thomas Hammer | musical-artifacts | 版权受限 | drum | 版权受限（原权利人保留全部权利） |
| 615 | HS African Percussion Soundfont | Thomas Hammer | musical-artifacts | 版权受限 | drum | 版权受限（原权利人保留全部权利） |
| 616 | Bassoon Ethan Nando | Ethan Winer | musical-artifacts | 版权受限 | guitar | 版权受限（原权利人保留全部权利） |
| 617 | HS Pads and Textures I Soundfont | Thomas Hammer | musical-artifacts | 版权受限 | synth | 版权受限（原权利人保留全部权利） |
| 618 | Bejeweled 3 Samples (Soundfont) | Peter Hajba & Alexander Br | musical-artifacts | 版权受限 | orch | 版权受限（原权利人保留全部权利） |
| 619 | HS Vox Soundfont | Thomas Hammer | musical-artifacts | 版权受限 | vocal | 版权受限（原权利人保留全部权利） |
| 620 | Bejeweled 3 Percussions (Soundfont) | Peter Hajba & Alexander Br | musical-artifacts | 版权受限 | drum | 版权受限（原权利人保留全部权利） |
| 621 | Cuckoo's Taped Piano SFZ (flac version) | Cuckoo Music | musical-artifacts | 版权受限 | piano | 版权受限（原权利人保留全部权利） |
| 622 | HS StarTrekFX Soundfont | Thomas Hammer | musical-artifacts | 版权受限 | sfx | 版权受限（原权利人保留全部权利） |
| 623 | Tonewheel Organ and MORE!! | Michael Picher | musical-artifacts | 版权受限 | piano | 版权受限（原权利人保留全部权利） |
| 624 | RCKTNEO SND316X soundfont (beta version, read description fo | RCKTNEO | musical-artifacts | 版权受限 | synth | 版权受限（原权利人保留全部权利） |
| 625 | Famicom Detective Club | Nintendo | musical-artifacts | 版权受限 | game | 版权受限（原权利人保留全部权利） |
| 626 | RE Library Manager 1.0 | Rick Blues from RE MEDIA P | musical-artifacts | 版权受限 | other | 版权受限（原权利人保留全部权利） |
| 627 | Native Instruments - Brass ensemble And Strings ensemble Sou | Xhomie3 or XNX team | musical-artifacts | 版权受限 | other | 版权受限（原权利人保留全部权利） |
| 628 | WTBleep | Sampled by Shiru 08'2019 | musical-artifacts | 版权受限 | game | 版权受限（原权利人保留全部权利） |
| 629 | SME Sequencer 2.0 | Rick Blues from RE MEDIA P | musical-artifacts | 版权受限 | other | 版权受限（原权利人保留全部权利） |
| 630 | SME Studio 1.0 | Rick Blues from RE MEDIA P | musical-artifacts | 版权受限 | other | 版权受限（原权利人保留全部权利） |
| 631 | Anaconda (Genesis) Soundfont | Mildanner, DevWorks Game T | musical-artifacts | 版权受限 | game | 版权受限（原权利人保留全部权利） |
| 632 | Korg TRITON Techno Rock Organ Soundfont | Mildanner, KORG | musical-artifacts | 版权受限 | hist | 版权受限（原权利人保留全部权利） |
| 633 | A LOT OF NEW INSTRUMENTS HERE! | Rick Blues from RE MEDIA P | musical-artifacts | 版权受限 | other | 版权受限（原权利人保留全部权利） |
| 634 | MPJ sound escentials for kontakt | Milton paredes, Mpj factor | musical-artifacts | 版权受限 | other | 版权受限（原权利人保留全部权利） |
| 635 | Our FIRST DAW--SME(Soundfont MIDI Editor) SEQUENCER EDITION! | Rick Blues from RE MEDIA P | musical-artifacts | 版权受限 | other | 版权受限（原权利人保留全部权利） |
| 636 | House Piano's soundfont version | Xhomie3 | musical-artifacts | 版权受限 | piano | 版权受限（原权利人保留全部权利） |
| 637 | Epic Tom | Unreal Instruments | sfzinstruments | 自定义许可（未明） | drum | 自定义许可，条款未明 → **许可不明即不收录** |
| 638 | Kitchen X | Unreal Instruments | sfzinstruments | 自定义许可（未明） | drum | 自定义许可，条款未明 → **许可不明即不收录** |
| 639 | Wind Chime | Unreal Instruments | sfzinstruments | 自定义许可（未明） | drum | 自定义许可，条款未明 → **许可不明即不收录** |
| 640 | Koto | Unreal Instruments | sfzinstruments | 自定义许可（未明） | ethnic | 自定义许可，条款未明 → **许可不明即不收录** |
| 641 | 1912 | Unreal Instruments | sfzinstruments | 自定义许可（未明） | ethnic | 自定义许可，条款未明 → **许可不明即不收录** |
| 642 | Standard Bass | Unreal Instruments | sfzinstruments | 自定义许可（未明） | guitar | 自定义许可，条款未明 → **许可不明即不收录** |
| 643 | Standard Guitar | Unreal Instruments | sfzinstruments | 自定义许可（未明） | guitar | 自定义许可，条款未明 → **许可不明即不收录** |
| 644 | The Slapper | Unreal Instruments | sfzinstruments | 自定义许可（未明） | guitar | 自定义许可，条款未明 → **许可不明即不收录** |
| 645 | Metal GTX | Unreal Instruments | sfzinstruments | 自定义许可（未明） | guitar | 自定义许可，条款未明 → **许可不明即不收录** |
| 646 | Sonatina Symphonic Orchestra | Mattias Westlund | MuseScore | 自定义许可（未明） | orch | 自定义许可，条款未明 → **许可不明即不收录** |
| 647 | Maestro Concert Grand Piano | Mats Helgesson | sfzinstruments | 自定义许可（未明） | piano | 自定义许可，条款未明 → **许可不明即不收录** |
| 648 | Pablemo 2020 | Pablemo | musical-artifacts | 未识别许可码 falv13 | game | **许可码未识别**（`falv13`）→ 不猜、不收录 |
| 649 | Alesis Drum Module 4 SoundFont | VentusArranger | musical-artifacts | 未识别许可码 falv13 | drum | **许可码未识别**（`falv13`）→ 不猜、不收录 |
| 650 | Clay Fighter 63 1/3 NOW HAVE A SOUNDFONT!!! | JJ MH | musical-artifacts | 未识别许可码 falv13 | game | **许可码未识别**（`falv13`）→ 不猜、不收录 |
| 651 | Custom Drums by JJ MH | JJ MH | musical-artifacts | 未识别许可码 falv13 | game | **许可码未识别**（`falv13`）→ 不猜、不收录 |
| 652 | Northern Trumpets | VGTrumpet | sfzinstruments | 标注 Free 但未指明许可 | orch | 标注 Free 但未指明具体许可 → 视为许可不明 |
| 653 | G1 | TKDrums | sfzinstruments | Freemium（免费增值） | drum | 免费增值（免费版许可不明） |
| 654 | L1 | TKDrums | sfzinstruments | Freemium（免费增值） | drum | 免费增值（免费版许可不明） |
| 655 | The Ultimate Megadrive Soundfont | TheEighthBit | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 656 | [REUPLOAD] The DEFINITIVE MEGALOVANIA Soundfont! V1.17 | DannieloCQ Music! | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 657 | 8bitSF ( The Nes Soundfont ) | TheEighthBit | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 658 | Default Windows MIDI Soundfont | Roland / Microsoft Corpora | musical-artifacts | 站点自标「存疑」 | other | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 659 | Super Nintendo Entertainment System General MIDI Soundfont | dotsarecool | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 660 | Edirol SD-90 Pack I (Complete) | rosntdoxot, DrKoupop, Spoo | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 661 | Earthbound Soundfont | SleepyTimeJesse | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 662 | NEW! Mother 3 Soundfont 2023 Update (1.0) | Shigisato Itoi & Nintendo | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 663 | KORG M1 GM soundfont Second Beta | Various artists | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 664 | Super Mario World (Full version) | MrSanic | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 665 | New Super Mario Bros DS Soundfont | M. Reza Khadafi | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 666 | The Ultimate Wii Soundfont | Mr.Sanic | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 667 | MOTHER 3 Soundfont | fluidvolt | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 668 | MEGALOVANIA (Shreddage) Bass Guitar Soundfont [Bigger range] | ASmolBoy | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 669 | SNES Mario Paint Soundfont 2.0 | ASmolBoy | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 670 | THE WORLD REVOLVING Soundfont (From DELTARUNE) | ASmolBoy | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 671 | HQ Orchestral Soundfont Collection | Unknown | musical-artifacts | 站点自标「存疑」 | orch | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 672 | Crisis 3.51 GM Soundfont [UNOFFICIAL UPDATE FROM CrisisGener | SonicLover 19 | musical-artifacts | 站点自标「存疑」 | gm | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 673 | KEYGEN / CHIPTUNE Soundfont | ASmolBoy | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 674 | Mother 1+2 (Game Boy Advance) Soundfont (1.0) | Wrapped | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 675 | Earthbound/Megalovania restored Overdrive Guitar | The guy2 | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 676 | Legend of Zelda: Majora's Mask Soundfont | exciter | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 677 | -Sonic The Hedgehog 2- | Mr.Sanic | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 678 | Mario Kart 64 Soundfont | M. Reza Khadafi | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 679 | Super Smash Bros 64 Soundfont | M. Reza Khadafi | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 680 | Chrono Trigger Soundfont | Mathew Valente [TSSF] | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 681 | jRhodes 1977 Mark | Learjeff | musical-artifacts | 站点自标「存疑」 | piano | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 682 | EarthBound Soundfont (2012) (Unused Instruments) | ASmolBoy, SleepyTimeJesse | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 683 | Kirby Super Star soundfont | fluidvolt | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 684 | The Beepbox Soundfont | Micasddsa4000 | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 685 | (OUTDATED) Roxie's Nintendo 64 General MIDI Soundfont | IkaMusumeYiyaRoxie | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 686 | Super Mario World Soundfont | Blitz Lunar | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 687 | SNES Plok Soundfont (V1.02) | ASmolBoy | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 688 | SEGA Samples | Zackie | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 689 | Kirby Super Star Ultra DS Soundfont | M. Reza Khadafi | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 690 | Mega Man X Soundfont | Blitzlunar | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 691 | WarioWare D.I.Y. Soundfont | M. Reza Khadafi | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 692 | Kiarchive (Soundfont Version) | Sodichi | musical-artifacts | 站点自标「存疑」 | other | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 693 | Bomberman Hero soundfont | HandlebarOrionX | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 694 | Banjo Kazooie Donkey Kong 64 Banjo Tooie Diddy Kong Racing S | M. Reza Khadafi | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 695 | Mario Kart Wii Soundfont | Mr.Sanic | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 696 | Mario & Luigi: Superstar Saga | Nintendo | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 697 | Cave Story Soundfont (OrgMaker) | ASmolBoy | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 698 | Famicom Soundfont | Kitt | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 699 | Sonic Spinball (Soundfont) | Mr.Sanic | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 700 | Pokemon Emerald XQ++ SC-88Pro Soundfont (read description) | stgiga, Zandro Reville, GA | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 701 | Android System Synth | Yamaha Corporation (1998) | musical-artifacts | 站点自标「存疑」 | other | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 702 | TrianGMGS Soundfont | Thomas K. | musical-artifacts | 站点自标「存疑」 | orch | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 703 | Yamaha TX16w GM compatible soundfont | McCheeseBob | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 704 | Kirby 64 Soundfont | fluidvolt | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 705 | Wii System Menu SoundFont | MrSanic | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 706 | Donkey Kong Country Soundfont Collection | William Kage | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 707 | SeinFont (The Seinfeld Soundfont) | ASmolBoy | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 708 | SNES Kirby's Dream Course Soundfont (V1.1) | ASmolBoy | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 709 | Mega Man Soundfont | Capcom | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 710 | Kirby 64 The Crystal Shards Soundfont | M. Reza Khadafi | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 711 | SILENT HILL (PS1) Midis + Soundfonts | Nolann59860 | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 712 | The Legend of Zelda Spirit Tracks DS Soundfont | M. Reza Khadafi | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 713 | Teenage Mutant Ninja Turtles 4: Turtles in Time Soundfont | Ehehe~ | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 714 | Super Mario World HD soundfont (UPDATED: v1.1) | justsomegal | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 715 | Realistic SF V2 | SonicLover 19 | musical-artifacts | 站点自标「存疑」 | other | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 716 | Sonic the Hedgehog 4: Episode 1 Soundfont + midis | Nolann59860 | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 717 | Super Mario Advance 4 | Dekyo Ongen | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 718 | Wii U Soundfont | Mr.Sanic | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 719 | ebhalloween002 | Toby Fox and Nintendo | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 720 | Bass Legends (Spectrasonics) | shrodedokaedro | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 721 | Glover 64 Soundfont | fluidvolt | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 722 | Mario Party DS Soundfont | M. Reza Khadafi | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 723 | Animal Crossing Nintendo 64/GameCube Soundfont Demo W.I.P. | IkaMusumeYiyaRoxie | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 724 | The Ultimate Piano Collection (East West) | shrodedokaedro | musical-artifacts | 站点自标「存疑」 | piano | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 725 | Sonic Jam Soundfont | type_a | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 726 | (sf2) Kontakt Factory Library - Pop Drums | Kontakt 6 Player / Native  | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 727 | Super Metroid Soundfont | Brian Crawford | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 728 | (OUTDATED, See Desc.) SNES Mario Paint Soundfont | Lil'Alien | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 729 | Super Mario Kart Soundfont | Blitz Lunar | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 730 | Splendid piano (136 MB) | High quality sfs | musical-artifacts | 站点自标「存疑」 | piano | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 731 | Yoshi's Island Soundfont | William Kage | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 732 | Roland JV-1010 GM Soundfont | Thomas K. | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 733 | SILENT HILL 2 (PS2) Midis + Soundfonts | Nolann59860 | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 734 | Star Fox 64 Soundfont | M. Reza Khadafi | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 735 | NES Sunsoft DPCM Bass Soundfont | ASmolBoy | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 736 | Super Mario RPG Soundfont | Mike Crain | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 737 | Mario & Luigi Partners in Time Soundfont | M. Reza Khadafi | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 738 | Pokemon: Ruby/Sapphire/Emerald [GBA] | Exabyte U | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 739 | Retro Synth PC | SONiVOX | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 740 | Nintendo Medley Soundfont | hakerg | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 741 | Rugrats Search For Reptar (Playstation 1) Soundfont | Wrapped | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 742 | Rock Bass | Edirol | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 743 | Groove Agent 3 Pack | Steinberg | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 744 | Roland EDIROL SD-90 Intim8String | Hayde | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 745 | TLoZ: A Link To The Past | Mr.Sanic | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 746 | Korg AG-10 GM Soundfont | Thomas K. | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 747 | Proteus GM soundfont | SonicLover 19 | musical-artifacts | 站点自标「存疑」 | gm | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 748 | Twilight Princess | Anonymous | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 749 | GoldenEye 64 Soundfont (N64Vault.com Versión) | JJ MH (RePost ir N64Vault. | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 750 | Kirby Mass Attack DS Soundfont | M. Reza Khadafi | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 751 | Nine Hours, Nine Persons, Nine Doors - Soundfonts + MIDIs | Ed_IT | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 752 | Sonic 3 Credits Soundfont and Samples | ElPavo613 | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 753 | Square Soundfont | Steven Rhodes | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 754 | Rockman & Forte Soundfont | fluidvolt | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 755 | Rock Man X/X2 Soundfont | Harumi Makoto | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 756 | Final Fantasy 6 Soundfont | Vienna Master | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 757 | Kirby's Dream Land 3 Soundfont | Blitz Lunar | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 758 | Diddy Kong Racing Nintendo 64 Soundfont | M. Reza Khadafi | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 759 | Minecraft GM Soundfont 1.1.1 | HYWT | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 760 | Jazz Bass | Edirol | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 761 | Mega Man Battle Network 5 DS Soundfont | M. Reza Khadafi | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 762 | The Legend of Zelda Phantom Hourglass DS Soundfont | M. Reza Khadafi | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 763 | South Park N64 Sountfont | IkaMusumeYiyaRoxie | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 764 | The Kawasaki Sax-A-Boom Soundfont (Jack Black) | Wrapped | musical-artifacts | 站点自标「存疑」 | wind | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 765 | Doom SNES Soundfont | Patricio Herrera | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 766 | Steve Stevens Guitar Samples Collection (East West) | shrodedokaedro | musical-artifacts | 站点自标「存疑」 | guitar | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 767 | Zelda A Link to The Past Soundfont | Blitz Lunar | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 768 | Ephesus GM v1.00 [WIP] | Simone Piervergili | musical-artifacts | 站点自标「存疑」 | gm | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 769 | Fire Emblem 8: The Sacred Stones Soundfont | circleseverywhere | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 770 | Diddy Kong Racing Nintendo DS Soundfont | M. Reza Khadafi | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 771 | WCW/NWO Revenge soundfont | HandlebarOrionX | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 772 | Pokemon: Firered/Leafgreen [GBA] | Exabyte U | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 773 | Earthworm Jim DSi Soundfont 2017 | M. Reza Khadafi | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 774 | F-Zero X (N64) Percussion Soundfont | Stephen Bereznicki | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 775 | Kirby Squeak Squad Soundfont | M. Reza Khadafi | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 776 | FatBoy-v0.786 | Simone Piervergili, Chris  | musical-artifacts | 站点自标「存疑」 | other | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 777 | Wario Ware: Smooth Moves Soundfont (W.I.P) | Mr.Sanic | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 778 | Nokia 30 Soundfont | Bryan Bilocura | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 779 | (OUTDATED, See Desc.) Seinfeld (Korg M1) Slap Bass Soundfont | Lil'Alien | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 780 | Setzer's SPC Soundfont Soundfont | Setzer | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 781 | Street Fighter 2 CPS1 Drum/Percussion Kit | Stephen Bereznicki | musical-artifacts | 站点自标「存疑」 | drum | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 782 | Secret of Mana Soundfont | Blitz Lunar | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 783 | Yoshi Island DS Soundfont | M. Reza Khadafi | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 784 | Samsung One UI 5.0 sounds | Samsung | musical-artifacts | 站点自标「存疑」 | piano | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 785 | Cookie Run: Ovenbreak Soundfont (.zip, includes SF2 & DLS) | luna (+squib, unknown - og | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 786 | F-Zero Soundfont | Blitz Lunar | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 787 | Zelda The Minish Cap Soundfont | Mathew Valente [TSSF] | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 788 | nylon guitar V3 soundfont | TheSoundfontMaker | musical-artifacts | 站点自标「存疑」 | other | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 789 | Yamaha YPT 220 piano V4 - fixed | TheSoundfontMaker | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 790 | Mario Hoops 3 on 3 DS Soundfont | M. Reza Khadafi | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 791 | Ghost Trick: Phantom Detective DS Soundfont Rip | Ed_IT | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 792 | Illusion of Gaia Soundfont | Felix Flywheel | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 793 | Mario VS Donkey Kong Mini Land Mayhem DS Soundfont | M. Reza Khadafi | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 794 | Pootis Soundfont | IkaMusumeYiyaRoxie | musical-artifacts | 站点自标「存疑」 | other | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 795 | The Legend Zelda Four Swords Anniversary Edition DSi Soundfo | M. Reza Khadafi | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 796 | CP80 (Yamaha PSR-SX700) | Simone Piervergili | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 797 | NES Soundfont V1.0 | iand255 | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 798 | Mystical Ninja Starring Goemon Soundfont | Blitz Lunar | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 799 | Fairlight CMI IIx GM compatible soundfont | McCheeseBob | musical-artifacts | 站点自标「存疑」 | gm | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 800 | Mario Paint Composer Nes Soundfont | Awpwr | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 801 | Kirby Canvas Curse DS Soundfont | M. Reza Khadafi | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 802 | Mii Channel Soundfont | Kazumi Totaka, Ripped By B | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 803 | Castlevania - Harmony of Dissonance Soundfont | Teuthida | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 804 | Yoshi Touch And Go DS Soundfont | M. Reza Khadafi | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 805 | Super Bomberman 2, 3, 4 , 5 Soundfont | Dont / YFU | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 806 | Fat-Man OPL-2 v2 Soundfont | George "The Fat Man" Sange | musical-artifacts | 站点自标「存疑」 | other | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 807 | Bomberman 64 The Second Attack soundfont | HandlebarOrionX | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 808 | Industrial Dance PC | SONiVOX | musical-artifacts | 站点自标「存疑」 | other | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 809 | Diddy Kong Racing Nintendo DS Soundfonts 2017 | M. Reza Khadafi | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 810 | Star Fox Soundfont | iteachvader | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 811 | SNES Rock n' Roll Racing Soundfont (and WAV pack) | ASmolBoy | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 812 | SD-90 SP1 004 Atomstrings | Hayde | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 813 | Samsung 2020 soundfont | TheSoundfontMaker | musical-artifacts | 站点自标「存疑」 | piano | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 814 | Cooking Mama Series Nintendo DS Official Soundfont | M. Reza Khadafi | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 815 | St.Concert | Edirol | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 816 | Puyo Puyo ~ n Soundfont [v 0.1] | Nintedo [ripped by Sozuke] | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 817 | Rugrats: Scavenger Hunt (Nintendo 64) Soundfont | Wrapped | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 818 | Hip-Hop | Steinberg | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 819 | Mario VS Donkey Kong 2 March of the Minis DS Soundfont | M. Reza Khadafi | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 820 | SD-90 SP1 005 Noo Tongs | Hayde | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 821 | The ULTIMATE LeapFrog Leap-font (4 Instrument Packs in 1 fil | Richard Marriott, Brad Ful | musical-artifacts | 站点自标「存疑」 | other | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 822 | Rushing Beat Shura (SFC) SoundFont | Dekyo Ongen | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 823 | SNES Alcahest Soundfont (and WAV pack) | ASmolBoy | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 824 | Rugrats in Paris: The Movie (Nintendo 64) Soundfont 1.0. 1 | Wrapped | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 825 | Kirby Dreamland 3 SNES GM Soundfont | M. Reza Khadafi | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 826 | Mario Kart 64 DLS Soundfont | M. Reza Khadafi | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 827 | Pingas Soundfont | IkaMusumeYiyaRoxie | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 828 | LiLVintage Soundfont | Thomas K. | musical-artifacts | 站点自标「存疑」 | other | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 829 | Battletoads: Battlemaniacs Soundfont | fluidvolt | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 830 | SD-90 SP1 001 D.L.A.Pad | Hayde | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 831 | Drill Dozer Soundfont | fluidvolt | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 832 | Conker Soundfont Collection | SonicLover 19 | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 833 | The Grand 3 Model D Close | Unknown | musical-artifacts | 站点自标「存疑」 | other | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 834 | SNES Bubsy in Claws Encounters of the Furred Kind Soundfont | ASmolBoy | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 835 | Blast Corps Nintendo 64 Soundfont | M. Reza Khadafi | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 836 | Final Fantasy: Mystic Quest Soundfont | Zetshiro | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 837 | Chrome Song Maker Soundfont | I don't know. | musical-artifacts | 站点自标「存疑」 | other | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 838 | Groove Agent 4/5 - Elementic | Unknown | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 839 | Doraemon - Nobita to Mittsu no Seireiseki Soundfont W.I.P | IkaMusumeYiyaRoxie | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 840 | WCW/NWO World Tour/Virtual Pro Wrestling 64  soundfont | HandlebarOrionX | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 841 | Final Fantasy 5 Soundfont | Mathew Valente [TSSF] | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 842 | Style Savvy Soundfont (Updated) | Atsuhiro Motoyama | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 843 | Burning Grooves (Spectrasonics) FIXED Cutoff | shrodedokaedro | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 844 | Triebwerk - Drum Kit 6 | Unknown | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 845 | 64 Trump Collection Soundfont | M. Reza Khadafi | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 846 | Groove Agent 4/5 - 8Bit | Unknown | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 847 | Buck Bumble soundfont | HandlebarOrionX | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 848 | LeapFrog Leap-font Complete Instrument Bundle (1999-2007) | LuckyPrincess (under LeapF | musical-artifacts | 站点自标「存疑」 | other | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 849 | TerrariaInstrumentPackV1 | Eternal Wonder | musical-artifacts | 站点自标「存疑」 | other | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 850 | SD-90 SP1 003 Xtremities | Hayde | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 851 | HALion Sonic - Beauty Pop Bell | Unknown | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 852 | Castlevania: Dracula X Soundfont | Patricio Herrera | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 853 | Super Castlevania 4 Soundfont | Mike Crain | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 854 | Final Fantasy 4 Soundfont | Mathew Valente [TSSF] | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 855 | Wonder Project J2: Cloro no Mori no Josette | IkaMusumeYiyaRoxie | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 856 | Rugrats: I Gotta Go Party (Game Boy Advance) Soundfont 1.0 | Wrapped | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 857 | Star Fox SNES GM Soundfont | M. Reza Khadafi | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 858 | Groove Agent ONE - Elecktro Kit | Steinberg | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 859 | SD-90 SP1 002 BrushingSaw | Hayde | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 860 | Hebereke's Popoon Soundfont v1.2 | LucianoTheWindowsFan | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 861 | Final Fantasy 8 Demo Disc Soundfont | Mathew Valente [TSSF] | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 862 | Romancing SaGa 3 | _Scribbly | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 863 | Magic Castle (PS1) Soundfont | Sodichi | musical-artifacts | 站点自标「存疑」 | other | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 864 | Groove Agent 4/5 - Dam Hard | Unknown | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 865 | Jurassic Park (SNES) Soundfont | deinolite | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 866 | SILENT HILL 3 (PS2) MIDIs and SF2s | Nolann59860 | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 867 | Yoshi's Island Small samples Collection | Mr.Sanic | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 868 | Groove Agent 4/5 - Ambiences | Unknown | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 869 | NONNTUTTI SoundFont | Simone Piervergili | musical-artifacts | 站点自标「存疑」 | gm | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 870 | SNES U.N. Squadron Soundfont (and WAV pack) | ASmolBoy | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 871 | Pilotwings Soundfont | fluidvolt | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 872 | SILENT HILL 4 THE ROOM (Windows) Soundfonts | Nolann59860 | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 873 | Kirby & The Amazing Mirror [GBA] | Exabyte U | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 874 | Cooking Mama DS Sound Rip SFX Collection | M. Reza Khadafi | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 875 | EMU Liveware ESC SoundFont Library | E-MU Systems | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 876 | Fire Emblem: Genealogy of the Holy War Soundfont | Mahmoud Ehab, EpitaphEpito | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 877 | Harvest Moon Soundfont | fluidvolt | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 878 | Battletoads and Double Dragon Soundfont | fluidvolt | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 879 | Magical Drop Soundfont | fluidvolt | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 880 | Secret of Evermore Soundfont | William Kage | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 881 | Kirby: Nightmare in Dreamland [GBA] | Exabyte U | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 882 | GenieVoice GM64Pro 2.0 - All Sets | Simone Piervergili, Studio | musical-artifacts | 站点自标「存疑」 | other | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 883 | Diddy Kong Racing DS Sound Rip SFX Collection | M. Reza Khadafi | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 884 | Mighty Morphin Power Rangers Soundfont | Patricio Herrera | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 885 | Carnival Games DS Soundfont | Salutanis Orkonus | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 886 | (outdated) PrismSynth | Vini (2) | musical-artifacts | 站点自标「存疑」 | synth | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 887 | LIT (Wiiware) Soundfont + Midis | Nolann59860 | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 888 | Sounds of the Learning Screen and Fridge DJ (Learning Screen | Richard Marriott, Brad Ful | musical-artifacts | 站点自标「存疑」 | other | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 889 | Piano Tiles Soundfont | Cab | musical-artifacts | 站点自标「存疑」 | piano | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 890 | Mario Kart DS Credits Soundfont | Shinobu Nagata, Makarthenu | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 891 | Contra 3: The Alien Wars Soundfont | Patricio Herrera | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 892 | Game Watch DSi Collection Soundfont | M. Reza Khadafi | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 893 | Music MonStars (DS) Soundfont | JappaWakka | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 894 | Kingdom Hearts: Chain of Memories [GBA] | Exabyte U | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 895 | Scooby Doo 2: Monsters Unleashed [GBA] SoundFont | nickboy6 | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 896 | Giana Sisters DS / 2D Soundfonts | Poké-Brother | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 897 | Sim City Soundfont | Mike Crain | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 898 | Tales of Phantasia Soundfont | Christian Esquivel | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 899 | Super Bomberman Soundfont | Blitz Lunar | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 900 | Final Fantasy I & II : Dawn of Souls [GBA] | Exabyte U | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 901 | AliceGM v1.1 | Alice "Radiomicrowave" S.S | musical-artifacts | 站点自标「存疑」 | gm | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 902 | X-Men: Mutant Apocalypse Soundfont | Patricio Herrera | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 903 | NEW! Mother 1+2 Soundfont (1.01) | Shigesato Itoi & Nintendo | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 904 | Ninja Gaiden Trilogy Soundfont | Patricio Herrera | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 905 | Final Fantasy VI: Advance [GBA] | Exabyte U | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 906 | Zhu Zhu Pets DS soundfont | That Animatronic Person | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 907 | Romancing Saga Soundfont | Zetshiro | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 908 | Prince of Persia Soundfont Soundfont | Patricio Herrera | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 909 | Samsung TV 2015 nostalgia TV sound test sound effect | Samsung | musical-artifacts | 站点自标「存疑」 | piano | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 910 | Final Fantasy IV: Advance [GBA] | Exabyte U | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 911 | Marvel Super Heroes War of The Gems Soundfont | Patricio Herrera | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 912 | Sunset Riders Soundfont | Mike Crain | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 913 | Final Fantasy V: Advance [GBA] | Exabyte U | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 914 | Legend of Zelda: Four Swords [GBA] | Exabyte U | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 915 | Chamberlin Marimba Soundfont | sleepnsound | musical-artifacts | 站点自标「存疑」 | other | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 916 | College Slam Basketball Soundfont | fluidvolt | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 917 | Mario Kart 8 Campaign Software MIDI and Soundfont | Landon & Emma | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 918 | Alcahest Soundfont | William Kage | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 919 | Lufia Soundfont | Felix Flywheel | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 920 | WWF Raw Soundfont | Patricio Herrera | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 921 | Megaman & Bass [GBA] | Exabyte U | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 922 | Dry Snap [Native Instruments DrumLab] | kitty-cat-satellite | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 923 | The Legend Zelda Four Swords Anniversary Edition DSi Sound R | M. Reza Khadafi | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 924 | Advanced Wars+ [GBA] | Exabyte U | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 925 | Nokia E71 TMobile sounds V2 | TheSoundfontMaker | musical-artifacts | 站点自标「存疑」 | other | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 926 | Final Fantasy Tactics Advance [GBA] | Exabyte U | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 927 | 7th Dragon - Soundfonts and Midis | flamentnagel | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 928 | Spider-Man 2 (NDS) Midis + SoundFonts | Nolann59860 | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 929 | Bird & Beans & Paper Airplane Chase (NDS) MIDIs + SoundFonts | Tailx | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 930 | Breath of Fire 2 Soundfont | Felix Flywheel | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 931 | Final Fight Soundfont | Mike Crain | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 932 | Ellen Whitaker's Horse Life 2 DS soundfont | @IzzBloxian on YouTube (*I | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 933 | Growth Or Devolution SNES 2.0 Soundfont | Witch's Cadence | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 934 | Failed Distorted Rip Soundfont | Salutanis Orkonus | musical-artifacts | 站点自标「存疑」 | other | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 935 | Breath of Fire Soundfont | Felix Flywheel | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 936 | Tekken Advanced [GBA] | Exabyte U | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 937 | Clay Fighter Soundfont | Mike Crain | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 938 | Metal Slug: Advance 2.0 [GBA] | Exabyte U | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 939 | Old Phone Tones | onj3.andrelouis.com | musical-artifacts | 站点自标「存疑」 | other | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 940 | Drill Dozer [GBA] | Exabyte U | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 941 | GAX Engine (GBA) Sample Pack | Shin'en Multimedia | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 942 | Style Savvy Soundfont | Atsuhiro Motoyama | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 943 | Nokia E71 TMobile version sound assets | TheSoundfontMaker | musical-artifacts | 站点自标「存疑」 | other | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 944 | Gemfire Soundfont | Mike Crain | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 945 | F-Zero: GP Legend [GBA] | Exabyte U | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 946 | Planning Permission soundfont V2 | TheSoundfontMaker | musical-artifacts | 站点自标「存疑」 | other | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 947 | Ensoniq ESQ-1 "SAX 1" synth soundfont | unknown | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 948 | Cello Cocoto | @IzzBloxian on YouTube (*I | musical-artifacts | 站点自标「存疑」 | orch | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 949 | Ensoniq ESQ-1 "PIANO2" synth soundfont | unknown | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 950 | Ensoniq ESQ-1 "ORGAN1" synth soundfont | unknown | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 951 | Ensoniq ESQ-1 "WAVBEL" synth soundfont | unknown | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 952 | Ensoniq ESQ-1 "HI-RES" synth soundfont | unknown | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 953 | Ensoniq ESQ-1 "SINPAD" synth soundfont | unknown | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 954 | Ensoniq ESQ-1 "PIANO1" synth soundfont | unknown | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 955 | Aladdin [GBA] | Exabyte U | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 956 | King of Fighters EX2: Howling Blood [GBA] | Exabyte U | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 957 | Ensoniq ESQ-1 "VELBAS" synth soundfont | unknown | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 958 | Ensoniq ESQ-1 "SHAKER" synth soundfont | unknown | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 959 | Ensoniq ESQ-1 "SYNBAZ" synth soundfont | unknown | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 960 | Lufia: Ruins of Lore [GBA] | Exabyte U | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 961 | Ensoniq ESQ-1 "SLOSTR" synth soundfont | unknown | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 962 | Lunar Legend [GBA] | Exabyte U | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 963 | Ensoniq ESQ-1 "MIXED" synth soundfont | unknown | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 964 | Airforce Delta Storm: Deadly Skies [GBA] | Exabyte U | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 965 | Ensoniq ESQ-1 "MOODS" synth soundfont | unknown | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 966 | Ensoniq ESQ-1 "PLKMTL" synth soundfont | unknown | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 967 | Ensoniq ESQ-1 "NOISTR" synth soundfont | unknown | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 968 | Ensoniq ESQ-1 "MINI M" synth soundfont | unknown | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 969 | Ensoniq ESQ-1 "TRIBEL" synth soundfont | unknown | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 970 | Ensoniq ESQ-1 +KOTO2 Soundfont | unknown | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 971 | Ensoniq ESQ-1 "PLKBRS" synth soundfont | unknown | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 972 | Ensoniq ESQ-1 "SNAPS1" synth soundfont | unknown | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 973 | Britney's Dance Beat [GBA] | Exabyte U | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 974 | Ensoniq ESQ-1 "BL PNO" synth soundfont | unknown | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 975 | Ensoniq ESQ-1 "CLAV 1" synth soundfont | unknown | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 976 | Ensoniq ESQ-1 "HARP2" synth soundfont | unknown | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 977 | Ensoniq ESQ-1 "DIGPNO" synth soundfont | unknown | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 978 | Ensoniq ESQ-1 "SLDRUM" synth soundfont | unknown | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 979 | Ensoniq ESQ-1 "BRASTR" synth soundfont | unknown | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 980 | Ensoniq ESQ-1 "BOTTLS" synth soundfont | unknown | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 981 | Ensoniq ESQ-1 "ICYORG" synth soundfont | unknown | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 982 | Ensoniq ESQ-1 "ECHO1" synth soundfont | unknown | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 983 | Ensoniq ESQ-1 "ANABRS" synth soundfont | unknown | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 984 | Ensoniq ESQ-1 "KLUNKS" synth soundfont | unknown | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 985 | Ensoniq ESQ-1 "3TRUMS" synth soundfont | unknown | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 986 | Yu Yu Hakasho: Tournament Tactics [GBA] | Exabyte U | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 987 | Ensoniq ESQ-1 "4XFADE" synth soundfont | unknown | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 988 | Ensoniq ESQ-1 "HEVBRS" synth soundfont | unknown | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 989 | Atomic Betty [GBA] | Exabyte U | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 990 | Hamtaro: Ham-Ham Heartbreak Soundfont | Datasette Trax | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 991 | Ensoniq ESQ-1 "KICK" synth soundfont | unknown | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 992 | Ensoniq ESQ-1 "MRIMBA" synth soundfont | unknown | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 993 | Ensoniq ESQ-1 "2 COOL" synth soundfont | unknown | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 994 | Sarukh's Nintendo DS General MIDI Soundfont | Sarukh_Animates | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 995 | Altered Beasts: Guardian of the Realms [GBA] | Exabyte U | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 996 | Ensoniq ESQ-1 "ISLAND" synth soundfont | unknown | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 997 | Hot Wheels: Burning Rubber [GBA] | Exabyte U | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 998 | Strike Force Hydra [GBA] | Exabyte U | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 999 | Ace Combat: Advance 2.5 [GBA] | Exabyte U | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 1000 | Ensoniq ESQ-1 "KALMBA" synth soundfont | unknown | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 1001 | Boscombe pier vibraphone soundfont | TheSoundfontMaker | musical-artifacts | 站点自标「存疑」 | other | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 1002 | Ensoniq ESQ-1 "K+SIMS" synth soundfont | unknown | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 1003 | Super Bust-A-Move [GBA] | Exabyte U | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 1004 | ILIO Sinclavier Essential Percussion (Soundfont/.sf2 Convers | supermumbo | musical-artifacts | 站点自标「存疑」 | piano | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 1005 | Spider-Man and the X-Men in Arcade's Revenge Soundfont | KiwiFlare | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 1006 | Edirol SD-90 Pack II | rosntdoxot, DrKoupop, Spoo | musical-artifacts | 站点自标「存疑」 | game | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 1007 | Stolen Soundfont (Update V2.03) | ME! | musical-artifacts | 站点自标「存疑」 | gm | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 1008 | Stolen Soundfont v2.05 | ME! | musical-artifacts | 站点自标「存疑」 | gm | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 1009 | Stolen Soundfont v2.07 | ME! | musical-artifacts | 站点自标「存疑」 | gm | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 1010 | Apollo GMGS v1.051 (3.89 GiB GM+GS soundfont) | Caed | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 1011 | Edirol SD-20 ~ Contemporary Soundfont | Thomas K. | musical-artifacts | 站点自标「存疑」 | hist | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 1012 | Kingdom Hearts - Soundfont Bundle 2024 | not me | musical-artifacts | 站点自标「存疑」 | other | **站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权 |
| 1013 | DSOUNDFONT Ultimate | Strix Soundfont Team | musical-artifacts | 混合 / 不明 | gm | 混合 / 不明（同一包内多种来源，无法逐项确认） |
| 1014 | "Ultimate" Roblox Soundfont (Old) | AquaDoesStuff | musical-artifacts | 混合 / 不明 | game | 混合 / 不明（同一包内多种来源，无法逐项确认） |
| 1015 | DSoundFont Gaming Edition | Strix SoundFont Team | musical-artifacts | 混合 / 不明 | gm | 混合 / 不明（同一包内多种来源，无法逐项确认） |
| 1016 | Taiko Drum Collection | Jason Champion, S. Christi | musical-artifacts | 混合 / 不明 | game | 混合 / 不明（同一包内多种来源，无法逐项确认） |
| 1017 | Monalisa GM v2.06 | Simone Piervergili | musical-artifacts | 混合 / 不明 | gm | 混合 / 不明（同一包内多种来源，无法逐项确认） |
| 1018 | Ephesus GM v1.00 (WIP) | Simone Piervergili | musical-artifacts | 混合 / 不明 | gm | 混合 / 不明（同一包内多种来源，无法逐项确认） |
| 1019 | Arachno SoundFont | Arachnosoft - Maxime Abbey | musical-artifacts | 混合 / 不明 | game | 混合 / 不明（同一包内多种来源，无法逐项确认） |
| 1020 | Monalisa GM v2.105 (14th June, 2025!!!) | Simone Piervergili | musical-artifacts | 混合 / 不明 | gm | 混合 / 不明（同一包内多种来源，无法逐项确认） |
| 1021 | Cocoto Platform Jumper WiiWare Soundfont | @IzzBloxian("IsHungry" on  | musical-artifacts | 混合 / 不明 | game | 混合 / 不明（同一包内多种来源，无法逐项确认） |
| 1022 | ROCCHETTA PLIN PLIN SoundFont V1 (probably a Beta version) | Simone Piervergili | musical-artifacts | 混合 / 不明 | game | 混合 / 不明（同一包内多种来源，无法逐项确认） |
| 1023 | Hight HD SoundFont SynthFont | Simone Piervergili | musical-artifacts | 混合 / 不明 | gm | 混合 / 不明（同一包内多种来源，无法逐项确认） |
| 1024 | mpj minibox demo | MPJ factory studios | musical-artifacts | 混合 / 不明 | game | 混合 / 不明（同一包内多种来源，无法逐项确认） |
| 1025 | Unleash The Beast SoundFont v1.2 (Not complete) | Simone Piervergili | musical-artifacts | 混合 / 不明 | other | 混合 / 不明（同一包内多种来源，无法逐项确认） |
| 1026 | Orchestra HQ Traditional Realistic SoundFont (2024 Edition) | Simone Piervergili | musical-artifacts | 混合 / 不明 | other | 混合 / 不明（同一包内多种来源，无法逐项确认） |
| 1027 | An old version of Rocchetta Plin Plin SoundFont | Simone Piervergili | musical-artifacts | 混合 / 不明 | other | 混合 / 不明（同一包内多种来源，无法逐项确认） |
| 1028 | Antares SoundFont | Simone Piervergili | musical-artifacts | 混合 / 不明 | gm | 混合 / 不明（同一包内多种来源，无法逐项确认） |
| 1029 | Unleash The Beast SoundFont | Simone Piervergili | musical-artifacts | 混合 / 不明 | other | 混合 / 不明（同一包内多种来源，无法逐项确认） |
| 1030 | Unleash The Beast SoundFont v1.1 | Simone Piervergili | musical-artifacts | 混合 / 不明 | other | 混合 / 不明（同一包内多种来源，无法逐项确认） |
| 1031 | Monalisa GM v1.0 (WIP) | Simone Piervergili | musical-artifacts | 混合 / 不明 | gm | 混合 / 不明（同一包内多种来源，无法逐项确认） |
| 1032 | MelloSFZotron | Nathan Ingelbrecht | musical-artifacts | 混合 / 不明 | game | 混合 / 不明（同一包内多种来源，无法逐项确认） |
| 1033 | Linnoleum SFZ-1 v2 | Nathan Ingelbrecht | musical-artifacts | 混合 / 不明 | drum | 混合 / 不明（同一包内多种来源，无法逐项确认） |
| 1034 | ECHECAZ SoundFont | Simone Piervergili | musical-artifacts | 混合 / 不明 | other | 混合 / 不明（同一包内多种来源，无法逐项确认） |
| 1035 | Phoenix GM-10 | Jexu | musical-artifacts | 混合 / 不明 | gm | 混合 / 不明（同一包内多种来源，无法逐项确认） |
| 1036 | Cirnomiji Soundfont Archive | Cirnomiji (formerly known  | musical-artifacts | 混合 / 不明 | other | 混合 / 不明（同一包内多种来源，无法逐项确认） |
| 1037 | Linnoleum SFZ-1 v1 | Nathan Ingelbrecht | musical-artifacts | 混合 / 不明 | drum | 混合 / 不明（同一包内多种来源，无法逐项确认） |
| 1038 | The Fox and The Crow General MIDI SoundFont Ultimate | Simone Piervergili | musical-artifacts | 混合 / 不明 | other | 混合 / 不明（同一包内多种来源，无法逐项确认） |
| 1039 | RetroFont2026 (WIP) | Simone Piervergili | musical-artifacts | 混合 / 不明 | game | 混合 / 不明（同一包内多种来源，无法逐项确认） |
| 1040 | Sonic GBA Sound Collection [V1]: Advance 1, Advance 2, Pinba | AsalTheBunMoth/Reverie, Ne | musical-artifacts | 混合 / 不明 | game | 混合 / 不明（同一包内多种来源，无法逐项确认） |
| 1041 | The Ultimate SoundFont Pack | IvyWolf and a lot of other | musical-artifacts | 混合 / 不明 | game | 混合 / 不明（同一包内多种来源，无法逐项确认） |
| 1042 | Monalisa GM SoundFont v2.06.5 | Simone Piervergili | musical-artifacts | 混合 / 不明 | gm | 混合 / 不明（同一包内多种来源，无法逐项确认） |
| 1043 | Monalisa GM v2.10 | Simone Piervergili | musical-artifacts | 混合 / 不明 | gm | 混合 / 不明（同一包内多种来源，无法逐项确认） |
| 1044 | Monalisa GM v2.109 [Download new v2.109.5!!!] | Simone Piervergili | musical-artifacts | 混合 / 不明 | gm | 混合 / 不明（同一包内多种来源，无法逐项确认） |
| 1045 | Caed's Ultimate Adequate GM version 1.04 (3.96GiB/4.26GB) | Caed, with some material b | musical-artifacts | 混合 / 不明 | hist | 混合 / 不明（同一包内多种来源，无法逐项确认） |
| 1046 | Old Version of ROCCHETTA PLIN PLIN SoundFont | Simone Piervergili | musical-artifacts | 混合 / 不明 | hist | 混合 / 不明（同一包内多种来源，无法逐项确认） |
| 1047 | Rocchetta Plin Plin SoundFont V2.022 | Simone Piervergili | musical-artifacts | 混合 / 不明 | hist | 混合 / 不明（同一包内多种来源，无法逐项确认） |
| 1048 | Monalisa GM v2.109.5 (rev. 1) (6th September, 2026) | Simone Piervergili | musical-artifacts | 混合 / 不明 | other | 混合 / 不明（同一包内多种来源，无法逐项确认） |
| 1049 | Unleash The Beast SoundFont v1.2 | Simone Piervergili | musical-artifacts | 混合 / 不明 | other | 混合 / 不明（同一包内多种来源，无法逐项确认） |
| 1050 | GS for The Spy Teen (PUBLIC BETA) | Bento Media, Velzaic Studi | musical-artifacts | 混合 / 不明 | piano | 混合 / 不明（同一包内多种来源，无法逐项确认） |

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
| 全部条目 | 四来源抓到的全部记录 | **3542** |
| 可分发候选 | F1 + F2 + F3 | **2492** |
| 可自由分发（F1） | CC0 / PD / WTFPL / Unlicense | **741** |
| F1 且 `.sf2` | 可直接站内分发 | **627** |
| **F1 且 `.sf2` 且 ≤50 MB** | **首批托管候选** | **69** |

**许可分布（全部 3542 条）**：

| 许可 | 数量 | 占比 | 档位 | 可再分发 |
|---|---:|---:|---|---|
| CC BY | 1140 | 32.2% | F2 | ✅ |
| 公有领域 | 426 | 12.0% | F1 | ✅ |
| 未标注 | 399 | 11.3% | F4 | ❌ |
| 站点自标「存疑」 | 358 | 10.1% | F4 | ❌ |
| CC BY 3.0 | 323 | 9.1% | F2 | ✅ |
| MIT | 205 | 5.8% | F2 | ✅ |
| CC0 | 115 | 3.2% | F1 | ✅ |
| WTFPL（等同公有领域） | 107 | 3.0% | F1 | ✅ |
| 公有领域（站点标注） | 93 | 2.6% | F1 | ✅ |
| CC BY-NC | 75 | 2.1% | F4 | ❌ |
| 商业授权 / 付费产品 | 59 | 1.7% | F4 | ❌ |
| 版权受限 | 52 | 1.5% | F4 | ❌ |
| 混合 / 不明 | 38 | 1.1% | F4 | ❌ |
| GPL v3 | 29 | 0.8% | F3 | ✅ |
| CC BY-SA | 17 | 0.5% | F3 | ✅ |
| CC BY 4.0 | 15 | 0.4% | F2 | ✅ |
| CC BY-NC-ND 3.0 | 15 | 0.4% | F4 | ❌ |
| 自定义许可（未明） | 11 | 0.3% | F4 | ❌ |
| 未识别码 by-nc-nd | 10 | 0.3% | F4 | ❌ |
| CC BY-ND（禁改作） | 9 | 0.3% | F4 | ❌ |
| ISC | 8 | 0.2% | F2 | ✅ |
| CC Sampling（整包分发受限） | 7 | 0.2% | F4 | ❌ |
| CC BY-SA 4.0 | 6 | 0.2% | F3 | ✅ |
| CC BY-NC-SA | 5 | 0.1% | F4 | ❌ |
| CC BY-SA 3.0 | 4 | 0.1% | F3 | ✅ |
| 未识别许可码 falv13 | 4 | 0.1% | F4 | ❌ |
| CC BY-NC-SA 3.0 | 3 | 0.1% | F4 | ❌ |
| GPL v2 | 2 | 0.1% | F3 | ✅ |
| GPL | 2 | 0.1% | F3 | ✅ |
| Freemium（免费增值） | 2 | 0.1% | F4 | ❌ |
| CC Sampling Plus 1.0 | 2 | 0.1% | F4 | ❌ |
| 标注 Free 但未指明许可 | 1 | 0.0% | F4 | ❌ |

## 十、对音色站的意义（三层的实际条数）

| 层 | 内容 | 条数 |
|---|---|---:|
| 第 1 层 · 目录 | 可分发候选（台账驱动、静态生成） | **2492** |
| 第 2 层 · 托管 | F1 · `.sf2` · ≤50 MB（站内直下） | **69** |
| 第 3 层 · 指引 | F4（只写来源地址，**不托管、不直链**） | **1050** |

### 10.1 首批托管候选（F1 · `.sf2` · ≤50 MB，按体积升序）

| # | 名称 | 作者 | 来源 | 许可 | 体积 | 分类 |
|---:|---|---|---|---|---:|---|
| 1 | Rhythmfont | Charlie | musical-artifacts | 公有领域（站点标注） | 0.1 MB | 游戏音源 |
| 2 | roland cr-78 general midi soundfont (+ rhythm midi files | barrelhead | musical-artifacts | WTFPL（等同公有领域） | 0.3 MB | 历史合成器/硬件音源 |
| 3 | DTS Soundfont | Swarm | archive | 公有领域 | 0.3 MB | 其他 / 未归类 |
| 4 | Milo Murphy's Law Soundfont | RunTheCoins | archive | CC0 | 0.4 MB | 其他 / 未归类 |
| 5 | dirtyyy | NikkyHika | archive | CC0 | 0.6 MB | 其他 / 未归类 |
| 6 | RemyMarshal's worlds smallest soundfont (electric piano) | RemyMarshal | musical-artifacts | WTFPL（等同公有领域） | 0.7 MB | 其他 / 未归类 |
| 7 | Minecraft Noteblock Soundfont v4.00 | happy_mimimix | archive | 公有领域 | 0.7 MB | 其他 / 未归类 |
| 8 | FreePats synthesizer percussion | FreePats project | FreePats | CC0 | 1.0 MB | 打击乐 / 鼓组 |
| 9 | Module'90 (free retro synth module) | Vini (2) | musical-artifacts | 公有领域（站点标注） | 1.2 MB | 游戏音源 |
| 10 | Module'89 (free retro synth module) | Vini (2) | musical-artifacts | 公有领域（站点标注） | 1.2 MB | 游戏音源 |
| 11 | Ukulele | FreePats project | FreePats | CC0 | 1.5 MB | 吉他 / 贝斯 / 拨弦 |
| 12 | Xylophone | Versilian Studios LLC | FreePats | CC0 | 1.7 MB | 打击乐 / 鼓组 |
| 13 | new super mario bros world 1 soundfont | nintendo ( ripped by me  | archive | CC0 | 1.7 MB | 其他 / 未归类 |
| 14 | Synth Bass #2 | FreePats project | FreePats | CC0 | 1.7 MB | 电子 / 合成 |
| 15 | Jaw Harp | FreePats project | FreePats | CC0 | 1.8 MB | 民族 / 世界 |
| 16 | Lately Bass | FreePats project | FreePats | CC0 | 2.0 MB | 电子 / 合成 |
| 17 | Bass Guitar YR | Andrea Biasior | FreePats | CC0 | 2.2 MB | 吉他 / 贝斯 / 拨弦 |
| 18 | Ocarina | FreePats project | FreePats | CC0 | 3.0 MB | 管弦 / 古典 |
| 19 | Roland GS Wavetable Synth | Roland Corporation | archive | 公有领域 | 3.1 MB | 历史合成器/硬件音源 |
| 20 | Synth Bass #1 | FreePats project | FreePats | CC0 | 3.2 MB | 电子 / 合成 |
| 21 | jd_rockkit1.sf2 | no idea | musical-artifacts | WTFPL（等同公有领域） | 3.3 MB | 打击乐 / 鼓组 |
| 22 | Synth Brass #2 | FreePats project | FreePats | CC0 | 3.4 MB | 电子 / 合成 |
| 23 | Kalimba | FreePats project | FreePats | CC0 | 3.7 MB | 民族 / 世界 |
| 24 | small-balafon-from-Burkina-Faso-sf2 | Isis999 | musical-artifacts | WTFPL（等同公有领域） | 3.9 MB | 民族 / 世界 |
| 25 | Synth Strings #1 | FreePats project | FreePats | CC0 | 4.2 MB | 电子 / 合成 |
| 26 | Tubular Bells | Versilian Studios LLC | FreePats | CC0 | 4.3 MB | 打击乐 / 鼓组 |
| 27 | Synth Crystal | FreePats project | FreePats | CC0 | 4.4 MB | 电子 / 合成 |
| 28 | Timpani | Versilian Studios LLC | FreePats | CC0 | 4.5 MB | 打击乐 / 鼓组 |
| 29 | SM64 SF | JackJamesMacdonald5 | archive | CC0 | 4.5 MB | 其他 / 未归类 |
| 30 | FM Synthesized Piano #2 | FreePats project | FreePats | CC0 | 4.6 MB | 钢琴 |
| 31 | World percussion | Versilian Studios LLC | FreePats | CC0 | 4.9 MB | 打击乐 / 鼓组 |
| 32 | Concert Harp | Versilian Studios LLC | FreePats | CC0 | 4.9 MB | 管弦 / 古典 |
| 33 | FSBS Electric Guitar Clean #2 (Jazz) | FreePats project | FreePats | CC0 | 5.0 MB | 吉他 / 贝斯 / 拨弦 |
| 34 | Synth Brass #1 | FreePats project | FreePats | CC0 | 5.2 MB | 电子 / 合成 |
| 35 | LX Space Piano - Soundfont sf2 | LexSound | archive | 公有领域 | 5.4 MB | 钢琴 |
| 36 | Drawbar organ emulation | Roberto | FreePats | CC0 | 5.8 MB | 风琴 / 键盘乐器 |
| 37 | Upright Piano KW | Gonzalo | FreePats | CC0 | 5.8 MB | 钢琴 |
| 38 | Synth Bass & Lead | FreePats project | FreePats | CC0 | 6.1 MB | 电子 / 合成 |
| 39 | FSBS Electric Guitar Clean #1 | FreePats project | FreePats | CC0 | 6.3 MB | 吉他 / 贝斯 / 拨弦 |
| 40 | Tenor Saxophone | Versilian Studios LLC | FreePats | CC0 | 6.5 MB | 管弦 / 古典 |
| 41 | Bagpipe | FreePats project | FreePats | CC0 | 6.7 MB | 民族 / 世界 |
| 42 | Clarinet | FreePats project | FreePats | CC0 | 6.7 MB | 管弦 / 古典 |
| 43 | Sweep Pad | FreePats project | FreePats | CC0 | 7.2 MB | 电子 / 合成 |
| 44 | New Age | FreePats project | FreePats | CC0 | 7.4 MB | 电子 / 合成 |
| 45 | Synth Strings #2 | FreePats project | FreePats | CC0 | 7.4 MB | 电子 / 合成 |
| 46 | Synth Lead Calliope | FreePats project | FreePats | CC0 | 7.5 MB | 电子 / 合成 |
| 47 | Wooden Recorder | Eugene Vlaskin | FreePats | CC0 | 7.9 MB | 管弦 / 古典 |
| 48 | (Wii U) Super Mario 3D World Soundfont (2019) | Mr.Sanic | musical-artifacts | 公有领域（站点标注） | 8.6 MB | 游戏音源 |
| 49 | Old Piano FB | FreePats project | FreePats | CC0 | 8.8 MB | 钢琴 |
| 50 | Synth Lead Square | FreePats project | FreePats | CC0 | 9.0 MB | 电子 / 合成 |
| 51 | Ravers & Gabbers 2 | ZwamTek Music | archive | 公有领域 | 9.2 MB | 其他 / 未归类 |
| 52 | Spanish classical guitar | FreePats project | FreePats | CC0 | 9.5 MB | 吉他 / 贝斯 / 拨弦 |
| 53 | Glasses of water | FreePats project | FreePats | CC0 | 9.8 MB | 打击乐 / 鼓组 |
| 54 | Hang tuned in D minor | FreePats project | FreePats | CC0 | 11.0 MB | 打击乐 / 鼓组 |
| 55 | Percussive organ emulation | FreePats project | FreePats | CC0 | 12.0 MB | 风琴 / 键盘乐器 |
| 56 | Rock organ emulation | FreePats project | FreePats | CC0 | 12.0 MB | 风琴 / 键盘乐器 |
| 57 | Synth Fifths | FreePats project | FreePats | CC0 | 12.0 MB | 电子 / 合成 |
| 58 | Synth Pad Choir | FreePats project | FreePats | CC0 | 12.0 MB | 电子 / 合成 |
| 59 | Gamer’s Tracker-MIDI(nSF2) Extracted Collection | Gamer45, technically als | musical-artifacts | WTFPL（等同公有领域） | 12.5 MB | 其他 / 未归类 |
| 60 | Church Organ Emulation | Fons Adriaensen | FreePats | CC0 | 13.0 MB | 风琴 / 键盘乐器 |
| 61 | FM Synthesized Piano #1 | FreePats project | FreePats | CC0 | 13.0 MB | 钢琴 |
| 62 | Synth Soundtrack | FreePats project | FreePats | CC0 | 17.0 MB | 电子 / 合成 |
| 63 | Synth Goblins | FreePats project | FreePats | CC0 | 19.0 MB | 电子 / 合成 |
| 64 | Soundfonts | rabid47 | archive | CC0 | 21.0 MB | 其他 / 未归类 |
| 65 | Synth Pad Bowed | FreePats project | FreePats | CC0 | 21.0 MB | 电子 / 合成 |
| 66 | Media Tek MT 6235 Soundfont | MediaTek | archive | CC0 | 21.1 MB | 其他 / 未归类 |
| 67 | Synth Sci-Fi | FreePats project | FreePats | CC0 | 22.0 MB | 电子 / 合成 |
| 68 | Zappa Kit.sf2 | rabid47 | archive | CC0 | 23.7 MB | 打击乐 / 鼓组 |
| 69 | PrismCorp's Soundfonts | Creative Technology, NTO | archive | 公有领域 | 30.9 MB | 其他 / 未归类 |

### 10.2 民族 / 世界音色（原本只有 2 个，S0 后的实际改善）

可分发候选里的民族 / 世界音色 **35 条**：

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
| Early European Instruments | — | polyphone | 公有领域 | ✓ | — |
| Seagull Acoustic Guitar | ? | polyphone | 公有领域 | ✓ | — |
| Lao Khaen | — | polyphone | 公有领域 | ✓ | — |
| Spirit of Hope gamelan balungan pelog | — | polyphone | 公有领域 | ✓ | — |
| Makala Ukulele Plucked | SuP3r_P1ckL3 | musical-artifacts | WTFPL（等同公有领域） | ✓ | — |
| 022 Florestan Harmonica | Nando Florestan | polyphone | 公有领域 | ✓ | — |
| Out of Africa | ? | polyphone | 公有领域 | ✓ | — |
| Vhamp | — | polyphone | 公有领域 | ✓ | — |
| Recorder 1.4 | — | polyphone | 公有领域 | ✓ | — |
| Ancient Instruments Of The World | — | polyphone | CC BY | ✓ | — |
| Multi Kalimba | A1219 | musical-artifacts | CC BY | ✓ | — |
| Metal Pipe Soundfont | Mildanner | musical-artifacts | CC BY 3.0 | ✓ | — |
| World percussion | Project SAM | polyphone | CC BY | — | — |
| Africa 1 | Joe Ortiz | polyphone | CC BY | ✓ | — |
| Woodblocks | Andreas Sumerauer | polyphone | CC BY | ✓ | — |
| Krumhorn Alt | ? | polyphone | CC BY | ✓ | — |
| Rindik | — | polyphone | CC BY | ✓ | — |
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
