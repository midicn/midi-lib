# DATASET-CARD · midicn-lib v1.0 数据卡

> 104,380 条记录 · 18 个来源数据集 · 统一 21 字段 Schema · 五级质量标记 · 全程可溯源
>
> 本数据卡描述 midicn-lib 的内容、来源、质量验证与使用限制。

## 一、数据集概述

midicn-lib 是对 17 个公开 MIDI 数据集的系统性二次整理：

- **统一 Schema**：全部记录转换为 21 字段结构（19 必需 + 2 可选），跨源字段语义一致
- **质量验证**：结构层 10 项 + 深度层 12 项终审全通过；音乐内容统计级验证全量执行
- **许可分区**：按可商用性将数据分为 main / piano-special / pending / research 四区
- **可溯源**：每条记录保留原始数据集路径（`src_path`），17 源许可审计公开

## 二、规模与来源明细

| 源 id | 来源数据集 | 曲目数 | 内容 | 许可 | 分区 |
|---|---|---:|---|---|---|
| `aria` | ariamidi | 32,522 | 古典钢琴（自动转录） | CC BY-NC-SA-4.0 | piano-special |
| `thesession` | TheSession.org | 23,294 | 爱尔兰传统舞曲/歌谣 | CC BY-SA-4.0 | main |
| `chinafolk` | 中国民歌集成 | 10,479 | 中国各省民歌 | UNSPECIFIED（待确认） | pending |
| `essen` | Essenfolkdance (EsAC) | 10,448 | 世界民谣（欧洲/中国为主） | 开放声明 | main |
| `norbeck` | Norbeck Abby | 3,473 | 爱尔兰/瑞典传统曲调 | 开放声明 | main |
| `mutopia` | Mutopia Project | 1,861 | 古典器乐（PD 乐谱生成） | 各曲不同（PD 为主） | main |
| `abcmisc` | ABC 标准曲集 | 1,579 | 克莱兹梅尔/巴尔干/民谣 | 开放声明 | main |
| `openscore` | OpenScore Lieder Corpus | 1,440 | 艺术歌曲（含女性作曲家） | CC0-1.0 | main |
| `maestro` | MAESTRO v3 | 1,276 | 钢琴演奏对齐转录 | CC BY-NC-SA-4.0 | research |
| `groove` | Groove MIDI Dataset | 1,150 | 专业鼓手节奏型 | CC BY-4.0 | main |
| `emopia` | EMOPIA v2.2 | 1,071 | 流行钢琴+情绪象限 | CC BY-NC-SA-4.0 | research |
| `nottingham` | Nottingham ABC | 1,037 | 英美民谣 | 开放声明 | main |
| `musedata` | MuseData (CCARH) | 924 | 古典器乐 | CCARH 限制 | research |
| `oga` | OpenGameArt.org | 342 | 游戏原创音乐 | CC0/CC-BY 逐曲 | main |
| `musicnet` | MusicNet | 330 | 古典室内乐 | CC BY-4.0 | main |
| `wikifonia` | Wikifonia 遗存（PD 子集） | 446 | 传统/民歌 lead sheets | PD | main |
| `m21` | music21 CoreCorpus | 3,068 | 古典/民谣混合 | PD | main |

## 三、分区说明（zone）

| 分区 | 数量 | 使用权限 |
|---|---:|---|
| `main` | 48,140 | ✅ 可商用（许可已逐曲标注） |
| `piano-special` | 32,522 | ⚠️ 仅非商用（CC BY-NC-SA） |
| `pending` | 10,473 | ❌ 未随本版发布（中国集成，待许可确认） |
| `research` | 3,269 | ❌ 未随本版发布（NC 学术用途） |

## 四、质量验证摘要

| 层 | 检查 | 结果 |
|---|---|---|
| 结构层 v1（10 项） | 文件完整性 / 路径唯一 / JSON / 字段 / 枚举 / 区划 / 去重标记 / 作曲家 / region / MIDI 头 | ✅ 全通过 |
| 深度层 v2（12 项） | MIDI 事件级 / 音高 / id / 溯源 / name-slug / 重复保留 / 跨区优先 / period 锚点 / 值域 / 同义 / title / license 语义 | ✅ 全通过 |
| **音乐内容层**（全量） | 调性相关（中位 0.826）· 动机重复（0.485）· 密度/音域/时长 | broken 102 已排除 · suspect 1,394 已标记 |

详细报告：`docs/AUDIT-REPORT.md`（v1）、`docs/AUDIT-REPORT-V2.md`（v2）、`midi_db/stats/music-verify-report.md`。

## 五、字段说明

见 [schema.md](schema.md)。核心：`c/cn` 作曲家 · `t` 标题 · `g` 流派 · `p` 时期 · `r` 地域 · `z` 分区 · `l` 许可 · `v` 质量标记 · `f` 文件路径。

## 六、局限（诚实披露）

1. **转录准确性**：MIDI 来自原始数据集的既有转录，本库完成统计级验证（可发现损坏/乱码），但**逐音符与原乐谱比对**未执行
2. **元数据**：信任原始数据集；ariamidi 无曲名（title 覆盖率 65.7% 的主因）
3. **链式许可**：核实了各数据集自身的许可声明，但无法穿透验证上游转录者的授权链
4. **中国集成**：10,473 首许可未确认，未包含在本版
5. **长尾署名**：2,094 个仅出现 1–2 次的作曲家署名未逐一考证

## 七、引用（BibTeX）

```bibtex
@dataset{midicn_lib_2026,
  title     = {midicn-lib: A Curated Multi-Source MIDI Library},
  author    = {midicn.com},
  year      = {2026},
  version   = {v1.0},
  url       = {https://github.com/midicn/midi-lib},
  note      = {104,380 tracks from 18 public datasets, unified schema,
               quality-verified and license-zoned}
}
```

同时请引用你实际使用的来源数据集（第二节表格）。

## 八、维护

- 项目主页：midicn.com
- 问题反馈：GitHub Issues
- 数据更新：按「审计→修复→重审计」流程，所有变更保留审计轨迹
