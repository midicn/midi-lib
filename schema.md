# midi_db schema v1 · midicn-lib 统一字段规范

> 生效日期：2026-09-17 · 本文件是数据真源的字段宪法：任何接入器产出的 JSONL 必须完全符合本规范。
> 变更须评审（改本文件 → 全量重跑受影响的接入器）。

## 1. 记录结构（19 个顶层字段）

```json
{
  "id": "aria-000004",
  "source": "aria",
  "src_path": "sources/ariamidi/data/aa/4_0.mid",
  "title": null,
  "composer_slug": "weber",
  "composer_name": "Weber",
  "opus": 77,
  "no": 2,
  "genre": "classical",
  "form": "sonata",
  "key": "d",
  "period": "classical",
  "region": null,
  "instrument": "piano",
  "license": "CC-BY-NC-SA-4.0",
  "zone": "piano-special",
  "midi": {
    "file": "data/midi/aria/b000/aria-b000-00001.mid",
    "duration_sec": null,
    "note_count": null,
    "tracks_count": null,
    "bpm": null
  },
  "fingerprint": null,
  "extra": { "audio_score": 0.951, "segment": 0, "name_source": "slug" }
}
```

## 2. 字段字典

| # | 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|---|
| 1 | `id` | str | ✔ | 全局唯一：`<source>-<6位序号>`，如 `aria-000004`。引用稳定，不随文件重命名变化 |
| 2 | `source` | str | ✔ | 源 id 短名（见 §4 表） |
| 3 | `src_path` | str | ✔ | 原始文件相对路径（相对工作区根），永久可追溯 |
| 4 | `title` | str/null | — | 曲名。**无则 null，不臆造**；展示名由 composer+opus/form 生成 |
| 5 | `composer_slug` | str | ✔ | 作曲家标识（保留源原始拼写，不擅自归并） |
| 6 | `composer_name` | str/null | — | 显示名。源自 slug 转换时 `extra.name_source="slug"`；来自权威对照表时 `="ref"` |
| 7 | `opus` | int/null | — | 作品号 |
| 8 | `no` | int/null | — | 作品内编号 |
| 9 | `genre` | str/null | — | 流派：classical / folk / hymn / jazz / game / world … |
| 10 | `form` | str/null | — | 曲式：sonata / etude / prelude / waltz / reel / jig … |
| 11 | `key` | str/null | — | 调性：`c`=C大调 `dm`=D小调 `eb`=E♭大调 `c#m`=C♯小调 |
| 12 | `period` | str/null | — | 时期：medieval / renaissance / baroque / classical / romantic / impressionist / modern / contemporary / **traditional**（民间音乐，不归入西方音乐史分期） |
| 13 | `region` | str/null | — | 地域（民歌/世界音乐必填）：ISO 国家/地区代码或中文地名 |
| 14 | `instrument` | str | ✔ | 主奏乐器：piano / ensemble / choir / erhu / guqin … |
| 15 | `license` | str | ✔ | SPDX 风格：`CC0-1.0` `CC-BY-4.0` `CC-BY-SA-4.0` `CC-BY-NC-SA-4.0` `PD` `OPEN`（源自有开放声明） |
| 16 | `zone` | str | ✔ | 分区：`main`（可商用）/ `piano-special`（NC 特区）/ `research`（学术研究） |
| 17 | `midi` | obj | ✔ | MIDI 规格：`file`（规范化相对路径）/ `duration_sec` / `note_count` / `tracks_count` / `bpm`（后四项 D8 统一解析，暂 null） |
| 18 | `fingerprint` | str/null | — | 音高序列哈希（D8 去重用，暂 null） |
| 19 | `extra` | obj | ✔ | 源特有数据透传（如 ariamidi 的 audio_score / segment；来源页 URL 等） |
| 20 | `duplicate_of` | str/null | 可选 | 若本记录被判定为重复（MD5 或同标题指纹），指向保留者的 id；**发布时按此字段过滤** |
| 21 | `verify_flag` | str/null | 可选 | 音乐内容验证标记：`broken`（解析失败/零音符，**发布时排除**）· `suspect`（调性/动机特征异常，保留但建议核查）· `extreme-range`（音域极值，游戏音效等）· `verified-short`（真实短曲：叫卖调/节奏型，正常收录） |

## 3. 分区与许可规则（接入器强制执行）

| zone | 许可范围 | 来源示例 |
|---|---|---|
| `main` | PD / CC0 / CC-BY / CC-BY-SA / 源自有开放声明 | Mutopia、OpenScore、Essen、thesession… |
| `piano-special` | CC BY-NC-SA 4.0 | ariamidi |
| `research` | 学术/NC 类数据集许可 | NES-DB、Weimar Jazz、EMOPIA、MAESTRO |
| `pending` | 许可未声明（**本地收录，不进发布包**） | chinafolk（待作者确认） |

**铁律**：`zone` 与 `license` 必须自洽；受版权保护的流行/游戏转录永不入库。
许可未声明时：`license="UNSPECIFIED"` + `zone="pending"`（文件照收，发布时排除）。

## 4. 源 id 短名表（JSONL 名 / data 子目录 / 文件名前缀 三处一致）

| 源 id | 官方源名 | 预计规模 | zone |
|---|---|---|---|
| `aria` | Aria-MIDI (Unique) | 32,522 | piano-special |
| `mutopia` | Mutopia Project | ~2,124 | main |
| `openscore` | OpenScore Lieder Corpus | ~1,300 | main |
| `musedata` | MuseData (CCARH) | ~800 | main |
| `sonatica` | sonatica.fm | ~11,000 | main |
| `pianomidi` | piano-midi.de | 332 | main |
| `chinafolk` | 中国民间歌曲集成 | 10,479 | main |
| `figshare` | figshare 中国经典 | 14 | main |
| `essen` | Essen Folk Song DB | 9,034 | main |
| `nottingham` | Nottingham Music DB | 1,200 | main |
| `norbeck` | Henrik Norbeck ABC | 2,800 | main |
| `thesession` | thesession.org | ~40,000 | main |
| `gregobase` | Gregobase | ~6,000 | main |
| `josquin` | Josquin RP + CMME | ~1,000 | main |
| `hymnal` | Hymnal Tune Dataset | 1,756 | main |
| `groove` | Groove MIDI | 1,150 | main |
| `musicnet` | MusicNet | 323 | main |
| `jsbach` | JSB Chorales + music21 | ~1,000 | main |
| `weimar` | Weimar Jazz DB | ~2,000 | research |
| `nesdb` | NES Music Database | 5,278 | research |
| `ccmusic` | 复旦 ccmusic | 数百+ | main |
| `cpdl` | CPDL ChoralWiki | ~25,000 | main |
| `kdf` | Kunst der Fuge | ~19,300 | main |
| `imslp` | IMSLP 附件 | 数千 | main |
| `abcn` | abcnotation 各集合 | ~20,000 | main |
| `digtra` | Digital Tradition | 数万 | main |
| `hymnary` | Hymnary.org | 数千 | main |
| `kern` | KernScores | 选择性 | main |
| `oga` | OpenGameArt | 数百 | main |
| `wikifonia` | Wikifonia 遗存 | ~6,405 | main |
| `ia` | Internet Archive 精选 | 数千+ | main |
| `midiworld` | MIDIWorld | 数千 | main |
| `emopia` | EMOPIA | 387 | research |
| `maestro` | MAESTRO | 1,282 | research |
| `lakh` | Lakh MIDI | 174,533 | research（v0.2 议） |
| `ossq` | OpenScore String Quartets | 进行中 | main |

## 5. 文件命名规范

- 规范化路径：`data/midi/<source>/b<桶号3位>/<source>-b<桶号3位>-<5位序号>.mid`
- 千首一桶：`b000` = 该源第 0–999 首，`b001` = 1000–1999，依此类推
- 序号按源内 `id` 排序分配（确定性，可重跑）
- 原始文件永不改动，规范副本由接入器生成
