# midicn-lib · 开放 MIDI 音乐库（二次整理版）

> **124,179** 首曲目 · **19** 个公开来源 · **14** 个分类 · 逐首标注许可档位 · 全程可溯源
>
> 门户与在线试听：<https://lib.midicn.com> · 数据下载页：<https://lib.midicn.com/download.html>
> 来源台账（每个地址的取得方式与校验值）：<https://lib.midicn.com/provenance.html>

本仓库是 midicn-lib 的**数据发布仓**：目录、索引、字段说明、许可审计与整理工具链。
站点源码在 [midicn/midi-lib-site](https://github.com/midicn/midi-lib-site)。

## 📦 包结构（按「使用方式」分包，而不是按风格）

| 目录 | 含义 | 档位 | 曲目数 | 下载 |
|---|---|---|---:|---|
| `main/` | 许可允许商业使用 | **C1 可商用** | 69,197 | `midicn-lib-<VER>-main.zip` |
| `piano-special/` | 仅限非商业用途 | **C2 非商用** | 34,869 | `midicn-lib-<VER>-piano-special.zip` |
| `study/` | 仅限学习与研究 | **C3 学习研究** | 20,113 | `midicn-lib-<VER>-study.zip` |
| `meta/` | 目录 / 索引 / 字段说明 / 文档 | **CC0-1.0** | — | `midicn-lib-<VER>-meta.zip` |
| **合计** | | | **124,179** | 另附 19 个**按来源**分包（`-source-<id>.zip`） |

> 各版本资产见 [Releases](https://github.com/midicn/midi-lib/releases)。当前版本与下载页一致（以
> <https://lib.midicn.com/download.html> 为准）。

## 🗂️ 分类明细（14 个分类）

**`main/`（C1 · 69,197 首）**

| 分类 | 曲目 | 来源 |
|---|---:|---|
| `folk-ireland/` | 26,689 | thesession 23,250 · norbeck 3,439 |
| `hymn/` | 10,945 | cyberhymnal |
| `folk-world/` | 10,818 | essen |
| `piano-performance/` | 10,112 | giantmidi |
| `classical-open/` | 6,624 | mutopia 1,860 · openscore 1,438 · m21 3,029 · musicnet 297 |
| `klezmer-balkan/` | 1,487 | abcmisc |
| `maestro/` | 1,276 | maestro |
| `drum/` | 1,149 | groove |
| `emopia/` | 1,071 | emopia |
| `folk-british/` | 1,033 | nottingham |
| `game/` | 340 | oga |

**`piano-special/`（C2 · 34,869 首）**

| 分类 | 曲目 | 来源 |
|---|---:|---|
| `piano/` | 32,522 | aria |
| `maestro/` | 1,276 | maestro |
| `emopia/` | 1,071 | emopia |

**`study/`（C3 · 20,113 首）**

| 分类 | 曲目 | 来源 |
|---|---:|---|
| `folk-china/` | 10,473 | chinafolk（中国民间歌曲集成 · OMR） |
| `classical-traditional/` | 9,640 | lakh（已过滤子集） |

## 🚀 快速使用

```python
import json
cat = json.load(open('meta/catalog.json', encoding='utf-8'))
# 每行一条记录，20 个字段（见 schema.md）
# 常用：id / t 标题 / c 作曲家 / z 档位 / l 许可 / f 相对路径 / du 时长(秒) / nn 音符数
piano = [r for r in cat['tracks'] if r['z'] == 'piano-special']
```

配套索引（`meta/`）：`index-by-composer.json` · `index-by-period.json` ·
`index-by-region.json` · `index-by-source.json` · `MD5SUMS.txt`（逐文件校验）。

## 🏷️ 字段说明

20 个字段（`id,t,c,cn,g,p,r,i,z,l,v,f,opus,no,form,ctry,diff,yr,du,nn`），完整定义见
[`schema.md`](schema.md)。覆盖度：作曲家 **100%** · 时长/音符数 **100%** · 标题 90.0% ·
风格/乐器 95.4% · 时期 88.1% · 曲式 46.0% · 作品号 26.0%。
**未知一律留空，不做猜测性填充。**

## ✅ 质量承诺

文件完整性、结构合规、逐文件时长/音符数重算、重复控制、许可分区与雷区排除——
每一项都程序化穷尽核验并有审计报告支撑；同时**诚实列出信任边界**（如未做逐音符人工核听）。
详见 [`DATA-QUALITY-STATEMENT.md`](DATA-QUALITY-STATEMENT.md)。

## 📜 许可

- **逐曲标注**于 `l` 字段；档位（C1 可商用 / C2 非商用 / C3 学习研究）见 `z` 字段
- 完整法律条款（使用义务 / 二次分发 / 免责 / 下架流程）：[`LICENSE.md`](LICENSE.md)
- 逐源归属：[`NOTICE.md`](NOTICE.md) · 许可审计：[`docs/LICENSE-AUDIT.md`](docs/LICENSE-AUDIT.md)
- ⚠️ **`thesession` 附加条款**：在 CC BY-SA 4.0 之外**禁止用于大语言模型**（训练 / LLM 工具处理 /
  并入 LLM 应用均不允许；仅无障碍方案豁免）
- `meta/` 目录、整理文档与工具链以 **CC0-1.0** 释出

## 📖 引用格式（BibTeX）

```bibtex
@misc{midicnlib,
  title     = {midicn-lib: an open MIDI library with per-track licence tagging},
  author    = {midicn project},
  year      = {2026},
  url       = {https://lib.midicn.com},
  note      = {124,179 tracks aggregated from 19 public datasets, unified catalogue,
               per-track licence tiers. Access version: see the Releases page.}
}
```

使用 `piano-special/` 包须同时引用 Aria-MIDI 原文（见 [`DATASET-CARD.md`](DATASET-CARD.md) §七）。

## 🙏 来源数据集（19 个）

**地址均为我们实际取得数据的位置**；取得方式、证据文件与校验值见
[PROVENANCE.md](PROVENANCE.md)（另有站内版 <https://lib.midicn.com/provenance.html>）。

| 源 | 曲目 | 档位 | 原始地址 |
|---|---:|---|---|
| Aria-MIDI（Unique 子集） | 32,522 | C2 | github.com/loubbrad/aria-midi |
| The Session | 23,250 | C1 | github.com/adactio/TheSession-data |
| The Cyber Hymnal | 10,945 | C1 | hymntime.com/tch |
| 中国民间歌曲集成（OMR） | 10,473 | C3 | github.com/m-july/Anthology-of-Chinese-Folk-Songs |
| ESAC 欧洲民歌档案 | 10,373 | C1 | esac-data.org |
| GiantMIDI-Piano | 10,112 | C1 | github.com/bytedance/GiantMIDI-Piano |
| Lakh MIDI Dataset（过滤） | 9,640 | C3 | colinraffel.com/projects/lmd/ |
| Norbeck ABC 曲集 | 3,439 | C1 | norbeck.nu/abc/ |
| music21 CoreCorpus | 3,029 | C1 | github.com/cuthbertLab/music21 |
| Mutopia Project | 1,860 | C1 | mutopiaproject.org |
| ABC Misc（John Chambers） | 1,487 | C1 | trillian.mit.edu/~jc/music/abc/ |
| OpenScore Lieder | 1,438 | C1 | github.com/OpenScore/Lieder |
| MAESTRO v3 | 1,276 | C2 | magenta.tensorflow.org/datasets/maestro |
| Groove MIDI Dataset | 1,149 | C1 | magenta.tensorflow.org/datasets/groove |
| EMOPIA v2.2 | 1,071 | C2 | zenodo.org/records/5257995 |
| Nottingham Music Database（校订版） | 1,033 | C1 | ifdo.ca/~seymour/nottingham/ |
| Wikifonia（PD 子集） | 445 | C1 | synthzone.com/files/Wikifonia/Wikifonia.zip |
| OpenGameArt | 340 | C1 | opengameart.org |
| MusicNet | 297 | C1 | zenodo.org/records/5120004 |

考察但**未收录**的来源（许可不允许再分发等）与原因见
[SOURCE-CATALOG.md](SOURCE-CATALOG.md)。

## 🛠️ 整理工具链（全部开源，可复现）

| 工具 | 作用 |
|---|---|
| `tools/ingest_*.py` | 各来源接入器（19 个，逐一可复现） |
| `tools/build_release.py` | 发布目录树 + `meta/catalog.json` + 四套索引 + MD5SUMS |
| `tools/enrich_*.py` | 元数据富化（IMSLP 作品目录 / Essen 地理 / Lakh 乐器等） |
| `tools/dedup.py` / `dedup_apply.py` | 两阶段去重（MD5 + 音高指纹，保守标记） |
| `tools/music_verify.py` | 音乐内容统计级验证（调性 / 动机 / 密度 / 音域 / 时长） |
| `tools/provenance.py` | **来源台账复核器**（地址 ↔ 站点 ↔ 数据 ↔ 本地证据 ↔ 整包哈希） |
| `tools/sync_docs.py` | 文档单一真源同步器（`docs/` → 各副本） |
| `tools/preflight.py` | **发布前置检查**（文档同步 + 台账复核 + 站点回归，0 失败才可发布） |

---

**English**: see [README.en.md](README.en.md) · Dataset card: [DATASET-CARD.md](DATASET-CARD.md) ·
Provenance ledger: [PROVENANCE.md](PROVENANCE.md) · Licence: [LICENSE.md](LICENSE.md)
