# PROVENANCE · 来源台账（每个原始地址的取得与核验记录）

> 核验日期 **2026-09-21** · 来源 **21** 个 · 合计 **133,667** 首 · 机器可读版 [`provenance.json`](provenance.json)
>
> 本文件回答一个问题：**来源页上写的那个「原始地址」，凭什么说它是我们真正取得数据的地方？**
> 每个来源都给出：地址、取得方式、本地证据文件、整包校验值（有则附上游官方值）、许可档位与核验日期。

## 一、三条规则

1. **地址唯一且真实**：每个来源只登记一个地址，= 我们实际取得数据的位置；
   不写泛泛的站点首页，不写凭印象猜的官网，更不写与数据无关的站点。
2. **档位必须与数据一致**：C1 可商用 / C2 非商用 / C3 学习研究，逐曲写入 catalog 的 `z` 字段；
   来源页标注与 catalog 不一致即视为缺陷（本台账每次复核都会检查）。
3. **可复核**：每条地址都有本地证据（文件自述 / 采集台账 / 校验值），并记录核验日期。

## 二、总表

| 来源 | 档位 | 曲目数 | 原始地址 |
|---|---|---:|---|
| aria | C2 | 32,522 | `https://github.com/loubbrad/aria-midi` |
| thesession | C1 | 23,250 | `https://github.com/adactio/TheSession-data` |
| cyberhymnal | C1 | 10,945 | `https://www.hymntime.com/tch/` |
| chinafolk | C3 | 10,473 | `https://github.com/m-july/Anthology-of-Chinese-Folk-Songs` |
| essen | C1 | 10,373 | `https://www.esac-data.org/` |
| giantmidi | C1 | 10,110 | `https://github.com/bytedance/GiantMIDI-Piano` |
| lakh | C3 | 9,109 | `https://colinraffel.com/projects/lmd/` |
| norbeck | C1 | 3,439 | `https://norbeck.nu/abc/` |
| m21 | C1 | 3,028 | `https://github.com/cuthbertLab/music21` |
| mutopia | C1 | 1,860 | `https://www.mutopiaproject.org/` |
| abcmisc | C1 | 1,487 | `http://trillian.mit.edu/~jc/music/abc/` |
| openscore | C1 | 1,438 | `https://github.com/OpenScore/Lieder` |
| maestro | C2 | 1,276 | `https://magenta.tensorflow.org/datasets/maestro` |
| groove | C1 | 1,149 | `https://magenta.tensorflow.org/datasets/groove` |
| emopia | C2 | 1,071 | `https://zenodo.org/records/5257995` |
| nottingham | C1 | 1,033 | `https://ifdo.ca/~seymour/nottingham/` |
| wikifonia | C1 | 445 | `http://www.synthzone.com/files/Wikifonia/Wikifonia.zip` |
| oga | C1 | 339 | `https://opengameart.org/` |
| musicnet | C1 | 297 | `https://zenodo.org/records/5120004` |
| atepp | C1 | 7,130 | `https://github.com/tangjjbetsy/ATEPP` |
| pdmx | C1 | 2,893 | `https://github.com/pnlong/PDMX` |
| **合计** | | **133,667** | |

## 三、逐源明细

### aria

- **原始地址**：`https://github.com/loubbrad/aria-midi`
- **取得方式**：GitHub 仓库克隆（Unique 子集，32,522 首；仓库 README 自述 ICLR 2025 Bradshaw & Colton）
- **入库脚本**：`tools/ingest_aria.py`
- **本地证据**：`sources/ariamidi/README.md`（含 `github.com/loubbrad/aria-midi`）
- **本地规模**：`sources/ariamidi` 32,578 文件 / 513.5MB
- **许可**：CC BY-NC-SA 4.0（catalog 标识 `CC-BY-NC-SA-4.0`）—— CC BY-NC-SA 4.0（非商用 · 相同方式共享）→ C2
- **取得时点**：2025-04-08（依据：earliest file mtime · sources/ariamidi）
- **复核时间线**：核验于 2026-09-21；下次复核不晚于 2027-03-20

### thesession

- **原始地址**：`https://github.com/adactio/TheSession-data`
- **取得方式**：官方数据转储仓库整包（周更 CSV/JSON，含 tunes.csv / sets.csv / thesession.db），本地 ZIP 归档
- **入库脚本**：`tools/ingest_abc.py`
- **本地证据**：`sources/thesession-data/README.mdown`（含 `The Session`）；`sources/thesession-data/.gitattributes`（含 `lfs`）
- **本地规模**：`sources/thesession-data` 24 文件 / 197.2MB
- **整包校验**：`thesession-data.zip` 50,307,527 字节 · MD5 `e951ebb0faaf49c99e2c252d009bc1a3`（本地快照值，用于完整性复核）
- **许可**：CC BY-SA 4.0（catalog 标识 `CC-BY-SA-4.0`）—— CC BY-SA 4.0 **+ 附加「禁止用于大语言模型」条款**：不得用大模型使用/改编/修改/处理该素材（含训练 LLM、借助 LLM 工具处理、并入 LLM 相关应用），仅无障碍方案有豁免 → C1（但受该附加条款约束）
- **取得时点**：2026-09-17（依据：archive mtime · thesession-data.zip）
- **复核时间线**：核验于 2026-09-21；下次复核不晚于 2027-03-20

### cyberhymnal

- **原始地址**：`https://www.hymntime.com/tch/`
- **取得方式**：hymntime.com/tch 的官方索引与 MIDI 整包（tch-idx / tch-mida 7z + 按字母分卷）
- **入库脚本**：`tools/ingest_cyberhymnal.py`
- **本地证据**：`sources/cyberhymnal/idx/tch-idx.txt`（含 `The Cyber Hymnal`）
- **本地规模**：`sources/cyberhymnal` 13,647 文件 / 38.8MB
- **许可**：Public Domain（catalog 标识 `PD`）—— 公有领域（PD）→ C1
- **取得时点**：2004-02-12（依据：earliest file mtime · sources/cyberhymnal）
- **复核时间线**：核验于 2026-09-21；下次复核不晚于 2027-03-20

### chinafolk

- **原始地址**：`https://github.com/m-july/Anthology-of-Chinese-Folk-Songs`
- **取得方式**：GitHub 公开的《中国民间歌曲集成》OMR 数字化项目整包（14 卷 MIDI，按省份分目录；本地 china-folk.zip 844,201,672 B）
- **入库脚本**：`tools/ingest_chinafolk.py`
- **本地证据**：另有留存（不随包分发）（含 `github.com/m-july/Anthology-of-Chinese-Folk-Songs`）；`sources/china-folk/lyrics-included/beijing`
- **本地规模**：`sources/china-folk` 20,960 文件 / 306.3MB
- **许可**：传统音乐 · 学习研究（catalog 标识 `TRADITIONAL-STUDY`）—— 上游未声明许可 → 定为 TRADITIONAL-STUDY，C3 仅学习研究
- **取得时点**：2026-09-17（依据：earliest file mtime · sources/china-folk）
- **复核时间线**：核验于 2026-09-21；下次复核不晚于 2027-03-20

### essen

- **原始地址**：`https://www.esac-data.org/`
- **取得方式**：esac-data.org 的 EsAC 数据库（原生 .sm 编码与 .abc 转写成对，共 81 文件）
- **入库脚本**：`tools/ingest_abc.py`
- **本地证据**：`sources/essen/esac/dva0.sm`（含 `REG[`）；`sources/essen/esac/HAN1.abc`（含 `O: China`）
- **本地规模**：`sources/essen` 81 文件 / 7.1MB
- **许可**：Public Domain / Open（catalog 标识 `OPEN`）—— 站点开放声明 → C1；含少量受限条目（见来源页备注）
- **取得时点**：2026-09-17（依据：earliest file mtime · sources/essen）
- **复核时间线**：核验于 2026-09-21；下次复核不晚于 2027-03-20

### giantmidi

- **原始地址**：`https://github.com/bytedance/GiantMIDI-Piano`
- **取得方式**：官方仓库 + disclaimer.md 指明的官方网盘（Google Drive / 百度网盘）下载 MIDI 整包 midis_v1.2.zip 192,678,627 B，与官方 README 所述「stable version (193 MB)」一致
- **入库脚本**：`tools/ingest_giantmidi.py`
- **本地证据**：`sources/giantmidi/extracted/GiantMIDI-PIano/README.md`（含 `github.com/bytedance/GiantMIDI-Piano`）
- **本地规模**：`sources/giantmidi` 10,860 文件 / 959.9MB
- **整包校验**：`GiantMIDI-PIano-20260919T005501Z-1-001.zip` 335,559,541 字节 · MD5 `2743966fa349908fe5bc21503e897acb`（本地快照值，用于完整性复核）
- **整包校验**：`midis_v1.2.zip` 192,678,627 字节 · MD5 `aaece5750b0cfe30b6a3be5c7bb14f83`（本地快照值，用于完整性复核）
- **整包校验**：`surname_checked_midis_v1.2.zip` 135,604,744 字节 · MD5 `0bc634338b156cadababd99f8da03470`（本地快照值，用于完整性复核）
- **上游官方口径**：size:midis_v1.2.zip = `192,678,627 B ≈ 193 MB` —— 来源：GiantMIDI-Piano README「stable version of GiantMIDI-Piano (193 MB)」
- **许可**：CC BY 4.0（catalog 标识 `CC-BY-4.0`）—— CC BY 4.0 → C1
- **取得时点**：2026-09-19（依据：archive mtime · GiantMIDI-PIano-20260919T005501Z-1-001.zip）
- **复核时间线**：核验于 2026-09-21；下次复核不晚于 2027-03-20

### lakh

- **原始地址**：`https://colinraffel.com/projects/lmd/`
- **取得方式**：官方下载主机 hog.ee.columbia.edu/craffel/lmd/lmd_full.tar.gz（1,768,163,879 B）分卷下载后合并；入库前剔除含版权声明的曲目与流行/影视路径
- **入库脚本**：`tools/ingest_lakh.py`
- **本地证据**：`tools/dl_lakh_multipart.py`（含 `hog.ee.columbia.edu/craffel/lmd/lmd_full.tar.gz`）
- **本地规模**：`sources/lakh` 11 文件 / 3562.6MB
- **整包校验**：`lmd_full.tar.gz` 1,768,163,879 字节 · MD5 `2536ce3fd2cede53ddaa264f731859ab`（本地快照值，用于完整性复核）
- **许可**：CC BY 4.0（catalog 标识 `CC-BY-4.0`）—— 数据集 CC BY 4.0，但内容层过滤后定为 C3 学习研究（study）
- **取得时点**：2026-09-18（依据：archive mtime · lmd_full.tar.gz）
- **复核时间线**：核验于 2026-09-21；下次复核不晚于 2027-03-20

### norbeck

- **原始地址**：`https://norbeck.nu/abc/`
- **取得方式**：norbeck.nu/abc 的 ABC 曲集（文件头部即写明站点地址）
- **入库脚本**：`tools/ingest_abc.py`
- **本地证据**：`sources/norbeck/hnair0.abc`（含 `http://www.norbeck.nu/abc/`）
- **本地规模**：`sources/norbeck` 72 文件 / 1.9MB
- **许可**：Open / Free（catalog 标识 `OPEN`）—— 作者无偿开放 → C1（保留署名）
- **取得时点**：2026-09-17（依据：earliest file mtime · sources/norbeck）
- **复核时间线**：核验于 2026-09-21；下次复核不晚于 2027-03-20

### m21

- **原始地址**：`https://github.com/cuthbertLab/music21`
- **取得方式**：随 music21 工具包分发的 CoreCorpus（site-packages/music21/corpus，3,219 文件 / 60.6MB），含 kern 与 MusicXML，由 ingest_music21.py 导出 MIDI
- **入库脚本**：`tools/ingest_music21.py`
- **本地证据**：`tools/ingest_music21.py`（含 `music21`）
- **本地规模**：`(pip) /music21/corpus` 3,219 文件 / 60.6MB
- **许可**：Public Domain（catalog 标识 `PD`）—— 语料内作品多为 PD → C1
- **复核时间线**：核验于 2026-09-21；下次复核不晚于 2027-03-20

### mutopia

- **原始地址**：`https://www.mutopiaproject.org/`
- **取得方式**：fetch_mutopia.py 从 www.mutopiaproject.org/ftp/ 抓取 .ly 源码并转换
- **入库脚本**：`tools/ingest_mutopia.py`
- **本地证据**：`tools/fetch_mutopia.py`（含 `www.mutopiaproject.org/ftp/`）
- **本地规模**：`sources/mutopia` 3,070 文件 / 30.0MB
- **许可**：Public Domain / CC（逐曲）（catalog 标识 `MUTOPIA-MIXED`）—— 逐曲 PD/CC → C1
- **取得时点**：2026-09-17（依据：earliest file mtime · sources/mutopia）
- **复核时间线**：核验于 2026-09-21；下次复核不晚于 2027-03-20

### abcmisc

- **原始地址**：`http://trillian.mit.edu/~jc/music/abc/`
- **取得方式**：trillian.mit.edu/~jc/music/abc/ 的 John Chambers 曲集（5 个 .abc：克莱兹梅尔/巴尔干/国际/以色列）
- **入库脚本**：`tools/ingest_abc.py`
- **本地证据**：`sources/abc-misc/allklez.abc`（含 `trillian.mit.edu`）
- **本地规模**：`sources/abc-misc` 5 文件 / 1.0MB
- **许可**：Open / Free（catalog 标识 `OPEN`）—— 站点开放声明 → C1
- **取得时点**：2026-09-17（依据：earliest file mtime · sources/abc-misc）
- **复核时间线**：核验于 2026-09-21；下次复核不晚于 2027-03-20

### openscore

- **原始地址**：`https://github.com/OpenScore/Lieder`
- **取得方式**：GitHub OpenScore/Lieder 仓库整包（本地 openscore-lieder.zip 191,547,791 B），MuseScore 源转 MIDI
- **入库脚本**：`tools/ingest_openscore.py`
- **本地证据**：`sources/openscore-lieder/scores`
- **本地规模**：`sources/openscore-lieder` 2,814 文件 / 512.3MB
- **整包校验**：`openscore-lieder.zip` 191,547,791 字节 · MD5 `029bb94357740e0ab60556a9d9da97c9`（本地快照值，用于完整性复核）
- **许可**：CC0 1.0（catalog 标识 `CC0-1.0`）—— CC0 1.0 → C1
- **取得时点**：2026-09-17（依据：archive mtime · openscore-lieder.zip）
- **复核时间线**：核验于 2026-09-21；下次复核不晚于 2027-03-20

### maestro

- **原始地址**：`https://magenta.tensorflow.org/datasets/maestro`
- **取得方式**：官方页面发布的 maestro-v3.0.0（MIDI 分卷 + CSV 元数据），本地 1,278 文件 / 84.5MB
- **入库脚本**：`tools/ingest_mididir.py`
- **本地证据**：`tools/ingest_mididir.py`（含 `MAESTRO v3.0.0`）；`sources/maestro/maestro-v3.0.0`
- **本地规模**：`sources/maestro` 1,278 文件 / 84.5MB
- **许可**：CC BY-NC-SA 4.0（catalog 标识 `CC-BY-NC-SA-4.0`）—— CC BY-NC-SA 4.0 → C2 非商用
- **取得时点**：2026-09-17（依据：earliest file mtime · sources/maestro）
- **复核时间线**：核验于 2026-09-21；下次复核不晚于 2027-03-20

### groove

- **原始地址**：`https://magenta.tensorflow.org/datasets/groove`
- **取得方式**：官方页面发布的 Groove MIDI Dataset（含 info.csv 元数据），本地 1,150 文件
- **入库脚本**：`tools/ingest_groove.py`
- **本地证据**：`tools/ingest_groove.py`（含 `Groove MIDI Dataset`）；`sources/groove/groove`
- **本地规模**：`sources/groove` 1,150 文件 / 5.3MB
- **许可**：CC BY 4.0（catalog 标识 `CC-BY-4.0`）—— CC BY 4.0 → C1
- **取得时点**：2026-09-17（依据：earliest file mtime · sources/groove）
- **复核时间线**：核验于 2026-09-21；下次复核不晚于 2027-03-20

### emopia

- **原始地址**：`https://zenodo.org/records/5257995`
- **取得方式**：Zenodo 记录 5257995（版本 2.2）发布的 EMOPIA_2.2 数据包；本地目录名即版本名
- **入库脚本**：`tools/ingest_mididir.py`
- **本地证据**：`tools/ingest_mididir.py`（含 `EMOPIA_2.2`）；`sources/emopia/EMOPIA_2.2`
- **本地规模**：`sources/emopia` 1,084 文件 / 2.1MB
- **许可**：CC BY-NC-SA 4.0（catalog 标识 `CC-BY-NC-SA-4.0`）—— CC BY-NC-SA 4.0 → C2 非商用（原站上曾误标 CC BY 4.0 / main，v11.4 已改正）
- **取得时点**：2026-09-17（依据：earliest file mtime · sources/emopia）
- **复核时间线**：核验于 2026-09-21；下次复核不晚于 2027-03-20

### nottingham

- **原始地址**：`https://ifdo.ca/~seymour/nottingham/`
- **取得方式**：ifdo.ca/~seymour/nottingham/ 的 ABC 校订版（Seymour Shlien 修正缺失拍与反复）；目录内 nottingham.html 自述「最新版在此下载」
- **入库脚本**：`tools/ingest_abc.py`
- **本地证据**：`sources/nottingham/nottingham_database/nottingham.html`（含 `ifdo.ca/~seymour/nottingham/`）
- **本地规模**：`sources/nottingham` 16 文件 / 0.5MB
- **许可**：Open / Free（catalog 标识 `OPEN`）—— 站点开放声明 → C1（数据库由 Eric Foxley 建立）
- **取得时点**：2026-09-17（依据：earliest file mtime · sources/nottingham）
- **复核时间线**：核验于 2026-09-21；下次复核不晚于 2027-03-20

### wikifonia

- **原始地址**：`http://www.synthzone.com/files/Wikifonia/Wikifonia.zip`
- **取得方式**：公开发布的 Wikifonia 整包 Wikifonia.zip（原站 wikifonia.org 已下线）
- **入库脚本**：`tools/ingest_wikifonia.py`
- **本地证据**：另有留存（不随包分发）（含 `synthzone.com/files/Wikifonia/Wikifonia.zip`）
- **本地规模**：`sources/wikifonia` 1 文件 / 35.7MB
- **整包校验**：`Wikifonia.zip` 35,727,800 字节 · MD5 `d26e22562e67eb7d37535e96cc5eebba`（本地快照值，用于完整性复核）
- **上游官方口径**：md5:Wikifonia.zip = `d26e22562e67eb7d37535e96cc5eebba` —— 来源：muspy 数据集注册表 muspy.datasets.wikifonia
- **许可**：Public Domain（仅传统/民歌子集）（catalog 标识 `PD`）—— 仅保留传统/民歌子集 → PD；C1
- **取得时点**：2026-09-17（依据：archive mtime · Wikifonia.zip）
- **复核时间线**：核验于 2026-09-21；下次复核不晚于 2027-03-20

### oga

- **原始地址**：`https://opengameart.org/`
- **取得方式**：fetch_oga.py 逐素材抓取 opengameart.org（逐 asset 许可记录在 tools/state/oga-progress.json）
- **入库脚本**：`tools/ingest_oga.py`
- **本地证据**：`tools/fetch_oga.py`（含 `opengameart.org`）；`sources/oga`
- **本地规模**：`sources/oga` 342 文件 / 4.2MB
- **许可**：逐曲混合（CC0 / CC BY / CC BY-SA / GPL）（catalog 标识 `GPL-3.0`）—— 逐曲混合（CC0 / CC BY / CC BY-SA / GPL）→ C1，须逐素材署名
- **取得时点**：2026-09-17（依据：earliest file mtime · sources/oga）
- **复核时间线**：核验于 2026-09-21；下次复核不晚于 2027-03-20

### musicnet

- **原始地址**：`https://zenodo.org/records/5120004`
- **取得方式**：Zenodo 记录 5120004 的 musicnet_midis.tar.gz + musicnet_metadata.csv，本地 331 文件
- **入库脚本**：`tools/ingest_mididir.py`
- **本地证据**：`tools/ingest_mididir.py`（含 `sources/musicnet`）；`sources/musicnet/musicnet_metadata.csv`
- **本地规模**：`sources/musicnet` 331 文件 / 10.2MB
- **许可**：CC BY 4.0（catalog 标识 `CC-BY-4.0`）—— CC BY 4.0 → C1
- **取得时点**：2026-09-17（依据：earliest file mtime · sources/musicnet）
- **复核时间线**：核验于 2026-09-21；下次复核不晚于 2027-03-20

### atepp

- **原始地址**：`https://github.com/tangjjbetsy/ATEPP`
- **取得方式**：用户协助下载官方 ATEPP-1.2.zip（Google Drive，213 MB，11,824 个 MIDI）后本地入库；另有 HuggingFace 镜像 anusfoil/atepp-midi 作为早期来源。筛选链：官方 metadata 匹配 → 有元数据 9,528 演奏 → 官方 quality 标记过滤（排除 2,397）→ 入库 7,131；构建期同源 MD5 去重再剔 1 首 → **发布 7,130**
- **入库脚本**：`tools/ingest_atepp.py`
- **本地证据**：`sources/atepp/ATEPP-metadata-1.2.csv`（含 `track`）；`sources/atepp/ATEPP-metadata-1.2.csv`
- **本地规模**：`sources/atepp` 11,834 文件 / 520.5MB
- **许可**：CC BY 4.0（catalog 标识 `CC-BY-4.0`）—— 数据集声明 CC BY 4.0（可商用、可再分发）。同一作品含多位钢琴家的演奏版本，逐曲以 version_type=performance 标记；演奏录音版权归各演奏者及其唱片方。
- **取得时点**：2026-09-22（依据：用户协助下载（Google Drive 不通，经 HF 镜像 anusfoil/atepp-midi 获取） · sources/atepp/ATEPP-1.2.zip）
- **复核时间线**：核验于 2026-09-22；下次复核不晚于 2027-03-21

### pdmx

- **原始地址**：`https://github.com/pnlong/PDMX`
- **取得方式**：Zenodo mid.tar.gz（254,035 个渲染 MIDI，用户协助下载）+ PDMX v2 CSV 254,077 行（含 license_conflict）+ HF 镜像 JSON/metadata；筛选链：rated_deduplicated → no_license_conflict → 有作曲家 → genre 白名单（classical/folk/world/religious，排除现代类自标 CC0 不可信样本）
- **入库脚本**：`tools/ingest_pdmx.py`
- **本地证据**：`sources/pdmx/PDMX-v2.csv`；`sources/pdmx/PDMX.csv`
- **本地规模**：`sources/pdmx` 7,604 文件 / 2625.7MB
- **许可**：CC0 / Public Domain（catalog 标识 `CC0-1.0`）—— 上游为 CC0 1.0 与公有领域混合；本库仅收录可确证公有领域的乐谱型子集，逐曲以 version_type=score 标记。
- **取得时点**：2026-09-23（依据：用户协助下载（Zenodo 403，经用户放至本地） · sources/pdmx/mid.tar.gz）
- **复核时间线**：核验于 2026-09-23；下次复核不晚于 2027-03-22

## 四、如何自行复核

```bash
# 1) 对照来源页与数据：站点标注 ↔ 发布 catalog ↔ 台账
python tools/provenance.py            # 地址 / 档位 / 计数 / 证据文件
python tools/provenance.py --hash     # 追加整包 MD5 与字节数复核
python tools/provenance.py --online   # 追加各地址当前可达性

# 2) 只用公开信息核验（无需我们的采集目录）
#    - Wikifonia 整包 MD5 可与公开数据集注册表比对：
#      muspy.datasets.wikifonia → md5(Wikifonia.zip) = d26e22562e67eb7d37535e96cc5eebba
#    - GiantMIDI-Piano：官方 README 声明数据集 193 MB，与本台账 midis_v1.2.zip
#      192,678,627 字节一致
```

## 五、复核周期

台账设**180 天复核周期**：`next_review_due` 到期时，`tools/provenance.py` 会给出提醒，
届时重新核验各地址（重跑 `--hash` / `--online`），并把新日期追加进 `reverified`、顺延 `next_review_due`。
「永久可复核」的含义是：**不是核验一次就永远成立，而是永远有一条可复跑的核验路径 + 一个到期提醒。**

## 六、变更纪律

- **改任何来源地址前**：先按本台账的办法取得证据（文件自述 / 采集台账 / 上游官方口径），
  再改 `assets/archive.js` 与本文件，并更新核验日期。**拿不到证据就不要改，也不要写。**
- **改许可档位前**：必须用发布 catalog（`release/site-repo/meta/catalog.json`）重新统计，
  档位与数据不一致会直接影响使用者的合规判断（历史上 lakh 与 emopia 曾各错标一次，已修）。
- 回归：`tools/e2e-test.js` 的【11】段已把 19 个地址、档位与「禁止错误地址复现」写进断言。

---

## English (summary)

Provenance ledger, verified 2026-09-21. 21 sources, 133,667 tracks. Each source records a **single** address — the place we actually obtained the data from — together with how it was obtained, a local evidence file (self-statement or acquisition ledger), package checksums where available (upstream-published values preferred), the licence tier, and the verification date.

Three rules: (1) one true address per source, never a generic homepage or a guessed official site; (2) the tier (C1 commercial / C2 non-commercial / C3 study-only) must match the per-track `z` field in the published catalog; (3) every address must be backed by evidence. Re-verify with `python tools/provenance.py [--hash] [--online]`.

