# midicn-lib 深度终审 v2

> 生成：2026-09-17T19:52:05 · 记录 94,740 · 维度 12+

## 一、结果总表

| 维度 | 结果 | 明细 |
|---|---|---|
| 11 MIDI 事件级 | ✅ | 抽样 300 · 解析失败 0 · 零音符 0 |
| 12 音高范围 | ✅ | 越界 0 |
| 13 id 前缀 | ✅ | 0 异常 |
| 14 源文件追溯 | ✅ | 缺失 0（csv/zip 内条目除外） |
| 15 name→slug 一致 | ⚠️ | 不一致 5897（信息级，多数为全名 vs 归并 slug） |
| 16 重复组唯一保留 | ✅ | 异常 0 |
| 17 重复跨区优先级 | ✅ | 0 组保留者分区欠优 |
| 19 period 锚点 | ✅ | 错位 0 |
| 22 license 语义 | ⚠️ | OPEN 16,537 · MUTOPIA-MIXED 1,861（语义模糊值） |

## 二、20 项结构级（v1 已含，复述结果）

v1 十项全部通过 ✅（见 `AUDIT-REPORT.md`）

## 三、维度明细

- **genre 值域**（11）：{'folk': 50777, 'classical': 40183, 'drum': 1150, 'pop': 1071, 'game': 342, 'jazz': 101, 'atonal': 26, 'ragtime': 17, 'soundtrack': 15, 'blues': 8, 'rock': 1}
- **instrument 值域**（6）：{'melody': 40277, 'piano': 34869, 'voice': 10479, 'ensemble': 6525, 'voice_piano': 1440, 'drums': 1150}

## 四、region 同义变体（合并建议）

- **罗马尼亚** ← Romania / Romanian

## 五、period 锚点错位明细


## 五、period 锚点错位明细

无 ✅

## 六、结论

- 结构层 10 项 + 深度层 8 项，**除 license 语义（OPEN/MUTOPIA-MIXED 需在数据卡中明确说明）与 region 中英对照（低优先）外，无阻断项**
- 3 个抽样级提示（零音符 / 解析失败）建议逐一手动核查
