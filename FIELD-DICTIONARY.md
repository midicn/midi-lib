# midicn-lib 数据字段字典（v1.23 · 2026-09-23）

> 发布侧：**134,191 首 · 21 源**。字段覆盖率以 `midi_db/FROZEN-STATS-v123.json` 为准。
> 标注规范：**权威**（源数据自带）· **推断**（算法生成，字段带 `*_src` 标记）· **留空**（不猜）

## 一、曲目标识

| 字段 | 类型 | 覆盖率 | 语义 | 来源 |
|---|---|---:|---|---|
| `id` | str | 100% | 唯一标识（`{source}-{6 位序号}`） | 生成 |
| `source` | str | 100% | 来源 id（21 源之一） | 注册表 |
| `version_type` | str | 100% | **版本类型**：`score`（乐谱型）/ `performance`（演奏型，ATEPP） | 新增 v1.23 |
| `fingerprint` | str | 100% | MIDI 内容 MD5（跨源去重依据） | 计算 |

## 二、作品信息

| 字段 | 类型 | 覆盖率 | 语义 | 来源 / 标注 |
|---|---|---:|---|---|
| `title` | str | 90.8% | 曲名（无标题者由作曲家+编号合成保证可分辨） | 各源 / IMSLP 反查 |
| `opus` | str | 27.9% | 作品号（依各作曲家编号体系：Op./BWV/K./D.…） | 源 + IMSLP。**不用次级编号兜底** |
| `no` | str | 27.5% | 编号 / 乐章号 | 源 + 标题提取 |
| `form` | str | **53.5%** | 曲式体裁（213+ 值：sonata/waltz/etude/ballade/xiaodiao/shange…） | 标题提取 + IMSLP + **essen R: 体裁** |
| `topic` / `extra.topics_zh` | list | 3,102（essen） | **题材**（爱情/死亡/宗教/传说…）——与曲式分列 | essen 德文题材 + 中文标签 |
| `extra.cut_title` | str | 8,508（essen） | 源文件原文曲名（.sm 的 CUT） | essen .sm |

## 三、作曲家

| 字段 | 类型 | 覆盖率 | 语义 | 来源 / 标注 |
|---|---|---:|---|---|
| `composer_name` | str | 100% | 显示名（**全库统一**：同 slug 单一规范名，高频者用全名） | 归并 + 清洗 |
| `composer_slug` | str | 100% | 标识（人工确认归并 35 组同人；CPE Bach 等已分流） | 归并表 |
| `cn_zh` | str | 28.1% | **中文名**（136 位有标准译名者：巴赫/莫扎特…赵元任/谭盾/久石让） | 人工表（无标准译名者留空） |
| `birth` / `death` | int | 32.2% | 生卒年（占位值 1500/1600 类已过滤） | giantmidi 官方表 + hymntime |

## 四、音乐属性

| 字段 | 类型 | 覆盖率 | 语义 | 来源 / 标注 |
|---|---|---:|---|---|
| `genre` | str | 95.8% | 风格（classical/folk/hymn/jazz…） | 各源 |
| `period` | str | 88.0% | 时期（medieval/renaissance/baroque/classical/romantic/impressionist/modern/contemporary/traditional） | 源 + 生卒年推导 |
| `key` | str | **73.6%** | 调性（31 标准值：`C`/`Dm`/`C#m`/`Eb`…） | **权威 37.7%** + **`key_src="inferred"` 35.9%**（Krumhansl 算法，留一验证 64-76%，附 `extra.key_corr`） |
| `instrument` | str | 94.5% | 乐器（8 类粗分类：piano/melody/organ/voice/…） | 各源 |
| `instrument_gm` | str | 60.0% | **GM 标准乐器名**（128 级，如 Acoustic Grand Piano / Violin） | MIDI program_change；无 program 且源为钢琴者按 GM 默认 |
| `region` | str | **76.5%** | 地域：国家（中文）/ 中国省级 / 地区（essen 保留原文地区名） | 源 + 作曲家国籍（giantmidi 表/hymntime，`region_src` 标注） |
| `country` | str | — | 国家层（essen 双粒度：region 地区 + country 国家） | essen |

## 五、MIDI 实测属性（从文件内部解析）

| 字段 | 类型 | 覆盖率 | 语义 | 来源 / 标注 |
|---|---|---:|---|---|
| `midi.tempo` | int | 99.5% | 速度 BPM | set_tempo meta（无 meta 留空） |
| `midi.timesig` | str | 75.2% | 拍号 | time_signature meta。（**推断方案已验证 26.8% → 放弃，留空**） |
| `midi.velocity_avg` / `velocity_range` | float/list | **100%** | **演奏力度**均值 / 动态范围（表现力指标） | note_on velocity 统计 |
| `midi.notes_per_sec` | float | 100% | 音符密度（音符数 / 时长） | 计算 |
| `pitch_range` | [int,int] | **100%** | 音域 [最低音, 最高音]（MIDI 音高号）+ `pitch_avg` | note 统计 |
| `midi.duration_sec` / `note_count` | float/int | 100% | 时长 / 音符数 | 解析 |
| `difficulty` | str | 6.5% | **演奏难度**（beginner/intermediate/advanced/virtuoso） | aria 官方元数据 |
| `yr` | int | 21.1% | 年代（语义按源：作品首出版年 / 早期出版年 / 录音年，`extra.yr_semantics` 标注） | IMSLP 首出版年 + 源标注 |

## 六、歌词

| 字段 | 类型 | 覆盖 | 语义 | 存法 |
|---|---|---:|---|---|
| `has_lyrics` | bool | 10,035 | 有歌词标记 | jsonl |
| `midi.lyrics_inline` | str | 2,773 | MIDI 内嵌歌词 | jsonl |
| **歌词库** | — | 10,035 | 中国民歌歌词全文（中位 91 字） | **独立分片** `midi_db/lyrics/chinafolk.jsonl`（不塞 catalog） |

## 七、许可与分区

| 字段 | 说明 |
|---|---|
| `license` | 逐曲许可标识（CC0-1.0 / CC-BY-4.0 / CC-BY-SA-4.0 / CC-BY-NC-SA-4.0 / PD / OPEN / MUTOPIA-MIXED / UNSPECIFIED）。**100%** |
| `zone` | 分包区：`main`（C1 可商用）/ `piano-special`（C2）/ `study`（C3 研究学习） |
| `verify_flag` | 质量标记（`broken` 发布时自动跳过 / `suspect` / `verified-short`） |

## 八、标注原则（贯穿全库）

1. **权威 > 推断 > 留空**：推断字段一律带 `*_src` 标记（`key_src` / `region_src`）并附置信度，可一键筛选
2. **未知留空不猜**：匹配不到就空（13,922 处姓氏级匹配被跳过、拍号推断 26.8% 被弃用）
3. **可分辨 100%**：无标题曲目由作曲家+编号合成
4. **中国台湾 / 中国香港 / 中国澳门** 严格标注
5. 每项改动均备份（`midi_db/tracks_backup/pre-*-20260923.jsonl`）+ 工具可复现（`tools/*.py`）
