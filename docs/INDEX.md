# DOCS INDEX · 文档地图与单一真源规则

> 本目录是 midicn-lib 全部文档的**唯一真源**。其它位置（数据仓根目录、数据仓 `docs/`、发布包）都是副本，
> **永不手工编辑副本**。改完文档跑：
>
> ```bash
> python tools/sync_docs.py --check     # 检查副本是否漂移（发布前置检查会调用）
> python tools/sync_docs.py --apply     # 把真源同步到各副本（数据仓 + 发布包）
> ```
>
> 清单定义在 `tools/docs_manifest.json`（哪一组、真源在哪、同步到哪里）。

## 一、public · 对外公开文档（同步到数据仓**根目录**；随发布包**根目录**分发）

| 文件 | 内容 | 维护方式 |
|---|---|---|
| `README.md` / `README.en.md` | 项目总览、快速开始 | 手写 |
| `DATASET-CARD.md` / `DATASET-CARD.en.md` | **数据集卡**：内容 / 来源 / 分包 / 字段 / 许可与限制 | 手写（数字须与 catalog 一致） |
| `LICENSE.md` | 许可与法律条款（8 节 · 中英）：结构 / 使用义务 / **TheSession 附加条款** / 二次分发 / 免责 / 商标 / 归属 / 下架 / 管辖 | 手写 |
| `NOTICE.md` | 第三方归属声明（19 来源逐条） | 手写（与 `PROVENANCE.md` 对齐） |
| `SOURCE-CATALOG.md` | 来源清单与许可对照全表（含**未收录**来源与原因、自取指引） | 手写 |
| `PROVENANCE.md` | **来源台账**：每个地址的取得方式 / 证据文件 / 整包校验值 / 核验日期 | **脚本生成**（`tools/provenance.py --render`） |
| `provenance.json` | 上述台账的机器可读版 | **脚本生成**（同上） |
| `DATA-QUALITY-STATEMENT.md` / `.en.md` | 数据质量声明（验证范围与口径） | 手写 |
| `DATA-STRUCTURE.md` | 数据结构与访问方式 | 手写 |
| `schema.md` | 字段级 Schema 定义 | 手写 |
| `EXPANSION-PLAN-BATCH34.md` | 扩充计划（第 3/4 批）与源考察记录 | 手写 |
| `CITATION.bib` | 引用条目 | 手写 |

## 二、internal · 审计与过程文档（同步到数据仓 `docs/`；随发布包 `docs/` 分发）

| 文件 | 内容 | 维护方式 |
|---|---|---|
| `INDEX.md` | 本文件：文档地图 | 手写 |
| `LICENSE-AUDIT.md` | 逐源许可审计（判定依据与链接） | 手写 |
| `AUDIT-REPORT.md` · `AUDIT-REPORT-V2.md` · `AUDIT-REPORT-V3.md` | 数据审计报告（结构与字段层） | 手写 |
| `music-verify-report.md` | 音乐内容级验证报告 | **脚本生成**（`tools/music_verify.py`） |
| `QUALITY-GATES.md` | 质量门定义 | 手写 |
| `（内部采集台账）` | **采集台账**：受限源的下载目标与结论（也是 `PROVENANCE.md` 的证据来源之一） | 手写 |
| `（内部网络记录）` | 网络受限记录 | 手写 |
| `（内部发布计划）` | 发布计划与前置检查清单（含 `preflight` 与文档同步检查） | 手写 |
| `（内部计划）` | 门户 UI 计划（历史） | 手写 |
| `（内部许可沟通草稿）` | 向中国民歌集成数据集作者请求许可的草稿（未发出） | 手写 |

## 三、数字口径（改任何数字前必读）

- **曲目数 / 分包数 / 许可分布**：一律以发布 catalog
  `release/site-repo/meta/catalog.json` 为准（当前 **124,179** = main 69,197 + piano-special 34,869 + study 20,113）
- **来源地址 / 档位**：以 `assets/archive.js` 的 `SOURCES` 为准，并与 `PROVENANCE.md` 一致
- **改了以上任一处**：跑 `tools/provenance.py`（地址/档位/计数/证据/文档新鲜度）与
  `tools/sync_docs.py --check`（副本漂移），两者都必须 0 失败

## 四、已退休文件（勿再创建）

| 文件 | 原因 |
|---|---|
| `DATASET_CARD.md`（下划线命名） | 与 `DATASET-CARD.md` 重名冲突且为未填写模板 → 已并入 `DATASET-CARD.md` |
| `release-docs/`（子目录） | 曾作为「随包文档」的第三份副本，重复且易漂移 → 真源已上移到本目录 |
