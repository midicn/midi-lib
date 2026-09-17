# midicn-lib v1.0 · MIDI 音乐库（二次整理版）

> 94,740 条记录 · 17 个来源数据集 · 统一 21 字段 Schema · 五级质量标记 · 全程可溯源
>
> 本库是对 17 个公开 MIDI 数据集的**系统性二次整理**：统一字段、质量验证、许可分区、索引构建。
> 我们发布的不只是音频文件，还有**完整的整理过程与审计档案**——每一步都可复现、可追溯、可质疑。

## 📦 包结构

| 目录 | 内容 | 数量 | 许可 |
|---|---|---:|---|
| `main/` | 可商用主库：爱尔兰民谣、世界民谣、英美民谣、克莱兹梅尔/巴尔干、古典开放许可、游戏音乐、鼓点 | ~48,140 | CC BY / CC BY-SA / PD 等 |
| `piano-special/` | 古典钢琴特区（自动转录） | 32,522 | CC BY-NC-SA（**非商用**） |
| `meta/` | 全量目录 `catalog.json` + 4 轴索引 + MD5 校验 | — | CC0 |
| `research/` | 研究用（不随本发布分发） | — | — |

**未包含**：
- 中国民歌集成（10,473 首）——许可待确认，确认后将作为独立包发布
- 损坏文件（102 首，解析失败/零音符）——验证后排除
- 重复文件（322 首，MD5/指纹检测）——验证后排除

## 🗂️ main/ 分类明细

| 子目录 | 内容 | 数量 | 主要来源 |
|---|---|---:|---|
| `folk-ireland/` | 爱尔兰传统舞曲与歌谣 | 26,689 | TheSession, Norbeck |
| `folk-world/` | 世界民谣（含中国、德国、北欧等） | 10,818 | Essen, Wikifonia(PD) |
| `klezmer-balkan/` | 克莱兹梅尔与巴尔干曲调 | 1,487 | ABCMisc |
| `folk-british/` | 英美民谣 | 1,033 | Nottingham |
| `classical-open/` | 古典开放许可（文艺复兴-浪漫） | 6,624 | Mutopia, OpenScore, music21, MusicNet |
| `game/` | 游戏原创音乐 | 340 | OpenGameArt |
| `drum/` | 鼓点节奏型 | 1,149 | Groove MIDI |

## 🚀 快速使用

```python
import json
catalog = json.load(open("meta/catalog.json"))["tracks"]

main_only = [t for t in catalog if t["z"] == "main"]            # 只要可商用
bach     = [t for t in catalog if t["c"] == "bach"]             # 按作曲家
romantic = [t for t in catalog if t["p"] == "romantic"]         # 按时期
china    = [t for t in catalog if t["r"] and "中国" in t["r"]]   # 按地域
games    = [t for t in catalog if t["g"] == "game"]             # 按流派
clean    = [t for t in catalog if not t["v"]]                   # 只要全验证通过的
```

`meta/` 下的 4 个索引文件（`index-by-composer.json` / `index-by-region.json` / `index-by-period.json` / `index-by-source.json`）为「键 → 曲目 id 列表」的映射，可直接用于网站前端导航，无需加载全量目录。

## 🏷️ 字段说明（完整定义见 [schema.md](schema.md)）

每首曲目 21 个字段（19 必需 + 2 可选），核心字段：

| 字段 | 含义 |
|---|---|
| `c` / `cn` | 作曲家 slug / 显示名（传统曲调统一为 `traditional`） |
| `t` | 标题（中国曲目保留中文名） |
| `g` / `p` / `r` / `i` | 流派 / 音乐时期 / 地域 / 乐器 |
| `z` | 分区：`main` 可商用 · `piano-special` 非商用 |
| `l` | 许可（逐曲标注） |
| `v` | 质量标记：`broken` 已排除 · `suspect` 特征异常建议核查 · `verified-short` 真实短曲 · `extreme-range` 音域极值 |
| `f` | 文件路径（`{id}.mid` 统一命名） |
| `duplicate_of` | 若为重复文件，指向保留者（本发布已排除这些记录） |

## ✅ 质量承诺（详见 [DATA-QUALITY-STATEMENT.md](DATA-QUALITY-STATEMENT.md)）

以下每一项都经过程序化穷尽核验，审计报告随包公开：

1. **文件完整性**：94,740 条记录逐一核验，缺失 0
2. **路径唯一性**：同源路径零冲突
3. **MIDI 可解析性**：抽样 300 首事件级解析，0 失败
4. **音乐内容统计级验证**（全量 94,740 首）：调性相关系数中位 **0.826**、动机重复率中位 **0.485**——真实音乐强证据；损坏/乱码文件已排除
5. **重复控制**：MD5 + 音高指纹两阶段检测，高置信重复 322 条已标记排除
6. **许可审计**：17 源逐源审计，雷区零收录（受版权保护的流行/游戏转录 0 首入库）
7. **作曲家字段**：归并映射经人工逐条审查，零误伤

**诚实披露的信任边界**（详见质量声明第二节）：与原乐谱的逐音符比对未执行；元数据信任原始数据集；链式许可无法穿透验证。

## 📜 许可

各源许可不同，**使用前务必查阅** [LICENSE-AUDIT.md](docs/LICENSE-AUDIT.md)：

- `main/`：逐曲标注许可（`l` 字段），以 CC BY / CC BY-SA / 公有领域为主
- `piano-special/`：**CC BY-NC-SA 4.0——禁止商用**，署名后可非商用使用
- 全库整体引用请使用下方 BibTeX

## 📖 引用格式（BibTeX）

```bibtex
@dataset{midicn_lib_2026,
  title     = {midicn-lib: A Curated Multi-Source MIDI Library},
  author    = {midicn.com},
  year      = {2026},
  version   = {v1.0},
  url       = {https://github.com/midicn/midi-lib},
  note      = {94,740 tracks from 17 public datasets, unified schema,
               quality-verified and license-zoned}
}
```

## 🙏 来源数据集（17 个）

ariamidi · TheSession · 中国民歌集成 · Essenfolkdance · Norbeck · Mutopia · ABCMisc · OpenScore Lieder Corpus · MAESTRO · Groove MIDI · EMOPIA · Nottingham · MuseData · OpenGameArt · MusicNet · Wikifonia(PD 子集) · music21 corpus

完整来源与许可审计见 [LICENSE-AUDIT.md](docs/LICENSE-AUDIT.md)，各源曲目数见 [DATASET-CARD.md](DATASET-CARD.md)。

## 🛠️ 整理工具链（全部开源，可复现）

清洗、验证、去重、审计的全部脚本随仓库发布（`tools/`）：
`quality_pipeline.py`（质量管线）· `music_verify.py`（音乐内容验证）· `dedup.py`（去重）· `clean_v1.py`（作曲家归并）· `infer_period.py`（时期推断）· `audit.py` / `audit2.py`（终审）

任何人可在原始数据集上重跑整个流程，得到与本库一致的产物。
