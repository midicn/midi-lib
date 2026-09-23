# midicn-lib 全库终审报告
> ⏳ **历史快照**：本文件为过程文档，其中的数字反映撰写当时的状态。现行数据（**133,667 首 / 21 源**）以 `DATASET-CARD.md`、`meta/catalog.json` 与 `PROVENANCE.md` 为准。


> 生成：2026-09-18T20:20:17 · 记录 **104,380** · 源 **18**

## 一、核查结果总表

| # | 检查项 | 结果 | 详情 |
|---|---|---|---|
| 1 | 文件完整性 | ✅ | 引用文件全部存在 |
| 2 | 同源路径唯一性 | ✅ | 无覆盖残留 |
| 3 | JSONL 合法性 | ✅ | 非法行 0 |
| 4 | 19 字段结构 | ✅ | 异常 0 条 |
| 5 | 枚举值合法 | ✅ | zone 非法 0 · period 非法 0 |
| 6 | zone-license 自洽 | ✅ | main 区含 NC/未声明 0 条 |
| 7 | duplicate_of 有效 | ✅ | 异常 0 |
| 8 | composer 非空 | ✅ | 空值 0 |
| 9 | region 清洁 | ✅ | 疑似噪声 0 |
| 10 | MIDI 头抽样 | ✅ | 抽样 500 · 异常 0 |

**总计**：记录 104,380 · 标记重复 322 · 唯一内容 104,058 · 待处理问题 0 条

## 二、分源明细

| 源 | 记录 | 落盘 | 路径唯一 | 分区 |
|---|---:|---|---|---|
| `aria` | 32,522 | ✓ | ✓ | piano-special32,522 |
| `thesession` | 23,294 | ✓ | ✓ | main23,294 |
| `chinafolk` | 10,479 | ✓ | ✓ | pending10,479 |
| `essen` | 10,448 | ✓ | ✓ | main10,448 |
| `lakh` | 9,640 | ✓ | ✓ | study9,640 |
| `norbeck` | 3,473 | ✓ | ✓ | main3,473 |
| `m21` | 3,068 | ✓ | ✓ | main3,068 |
| `mutopia` | 1,861 | ✓ | ✓ | main1,861 |
| `abcmisc` | 1,579 | ✓ | ✓ | main1,579 |
| `openscore` | 1,440 | ✓ | ✓ | main1,440 |
| `maestro` | 1,276 | ✓ | ✓ | piano-special1,276 |
| `groove` | 1,150 | ✓ | ✓ | main1,150 |
| `emopia` | 1,071 | ✓ | ✓ | piano-special1,071 |
| `nottingham` | 1,037 | ✓ | ✓ | main1,037 |
| `musedata` | 924 | ✓ | ✓ | research924 |
| `wikifonia` | 446 | ✓ | ✓ | main446 |
| `oga` | 342 | ✓ | ✓ | main342 |
| `musicnet` | 330 | ✓ | ✓ | main330 |

## 三、分区与许可

| 分区 | 记录数 |
|---|---:|
| main | 48,468 |
| piano-special | 34,869 |
| pending | 10,479 |
| study | 9,640 |
| research | 924 |

| 许可 | 记录数 |
|---|---:|
| `CC-BY-NC-SA-4.0` | 34,869 |
| `CC-BY-SA-4.0` | 23,294 |
| `OPEN` | 16,537 |
| `CC-BY-4.0` | 11,120 |
| `UNSPECIFIED` | 10,479 |
| `PD` | 3,514 |
| `MUTOPIA-MIXED` | 1,861 |
| `CC0-1.0` | 1,440 |
| `CCARH-RESTRICTED` | 924 |
| `CC0` | 267 |
| `CC-BY-SA 4.0` | 39 |
| `CC-BY 4.0` | 15 |

## 四、问题清单

**无** —— 10 项全部通过 ✅