# RELEASE-PLAN · 发布产物设计（v1.0）

> 目标：二次发布不是搬运，而是**整理增值**。所有包结构、索引、文档都以「使用者拿去就能用、能溯源、能信任」为标准。

## 一、发布包结构（4 包 + 1 元数据包）

```
midicn-lib-v1.0/
│
├── README.md                    # 中文为主 + English 摘要
├── DATASET-CARD.md              # 数据卡（规模/来源/许可/质量/引用）
├── DATA-QUALITY-STATEMENT.md    # 质量声明（已验证/信任边界）
├── schema.md                    # 21 字段说明
├── LICENSE.md                   # 整体许可与各源许可对照
├── docs/
│   ├── LICENSE-AUDIT.md         # 17 源逐源许可审计
│   ├── AUDIT-REPORT.md / -V2.md # 两轮终审
│   ├── QUALITY-GATES.md         # 质量门
│   └── music-verify-report.md   # 音乐内容验证
│
├── meta/                        # ⭐ 元数据包（我们的核心增值）
│   ├── catalog.json             # 全量目录（轻量字段，前端直用）
│   ├── index-by-composer.json   # 作曲家索引
│   ├── index-by-region.json     # 地域索引
│   ├── index-by-period.json     # 时期索引（音乐史时间线直用）
│   ├── index-by-source.json     # 来源索引
│   └── MD5SUMS.txt              # 全部文件校验
│
├── main/                        # 🟢 可商用主库（48,154 → 去重排除后 ~47,850）
│   ├── folk-ireland/            #   爱尔兰传统（thesession + norbeck）
│   ├── folk-world/              #   世界民谣（essen）
│   ├── folk-british/            #   英美民谣（nottingham）
│   ├── klezmer-balkan/          #   克莱兹梅尔/巴尔干（abcmisc）
│   ├── classical-open/          #   古典开放许可（mutopia/openscore/m21/musicnet）
│   ├── game/                    #   游戏原创（oga）
│   └── drum/                    #   鼓点节奏（groove）
│
├── piano-special/               # 🟡 非商用钢琴特区（ariamidi，CC BY-NC-SA 32,522）
│
└── research/                    # ⚪ 研究用（maestro/emopia/musedata——不公开分发，仅本地）
```

**不发布**：`pending-chinafolk`（10,473 首，待许可确认后升 main）；`broken`（102）与 `duplicate_of`（322）在目录中直接排除。

## 二、我们的特色（二次发布的增值点）

| # | 特色 | 说明 |
|---|---|---|
| 1 | **统一 Schema** | 17 个异构源 → 统一 21 字段，一次接入终身受用 |
| 2 | **质量五级标记** | 每首带 `verify_flag`（broken/suspect/verified-short/extreme-range/正常）+ `duplicate_of`——使用者可按质量筛选 |
| 3 | **中文化** | 中国民歌保留**中文标题**（源数据是拼音，我们存了中文）；README/数据卡中文优先 |
| 4 | **三轴索引** | 作曲家 × 地域 × 时期，网站前端直接 `fetch` json 即可导航 |
| 5 | **全程可溯源** | 每首记录 `src_path` 指回原始数据集文件；17 源许可审计公开 |
| 6 | **可复现整理** | 工具链（清洗/验证/去重/审计脚本）全部随包开源，任何人可重跑 |
| 7 | **诚实声明** | 质量声明明确「已验证 11 项 / 信任边界 4 项」——不夸口，有据可查 |
| 8 | **许可墙** | zone 分区让使用者一眼分清「能商用 / 仅非商用 / 待确认」 |

## 三、包大小预估

| 包 | 曲目数 | 体积（估） | 发布渠道 |
|---|---:|---:|---|
| meta | — | ~30 MB | GitHub 仓库直放 |
| main | ~47,850 | ~400 MB | GitHub Release 分卷（或 HF） |
| piano-special | 32,522 | ~250 MB | GitHub Release 分卷（NC 声明） |
| research | 3,269 | ~30 MB | 不公开（本地/合作者） |

## 四、元数据 catalog.json 字段（轻量化）

```json
{
  "id": "thesession-000000",
  "t": "标题",                    // title
  "c": "traditional",             // composer_slug
  "cn": "Traditional",            // composer_name
  "g": "folk",                    // genre
  "p": "traditional",             // period
  "r": "爱尔兰",                   // region
  "i": "melody",                  // instrument
  "z": "main",                    // zone
  "l": "CC-BY-SA-4.0",            // license
  "v": null,                      // verify_flag（null=正常）
  "f": "main/folk-ireland/xxx.mid" // 发布路径
}
```

## 五、执行步骤（D9）

1. [ ] 生成发布目录树（按 zone → 大分类 → 文件，重命名 `{id}.mid`）
2. [ ] 生成 5 个索引 json + MD5SUMS
3. [ ] 撰写 README / DATASET-CARD / LICENSE 终稿
4. [ ] 打包 zip + 校验
5. [ ] 用户自行上传 GitHub（我们只产出本地产物 + 上传清单）

## 六、待确认项

1. `piano-special`（NC 特区）是否随 main 一起发布？（NC 许可需要使用者遵守，公开无妨）
2. `research` 包：确认**不公开**，仅本地保留？
3. `main` 包内是否保留 `duplicate_of` 被标记记录的文件？（默认：排除）
4. 发布文件名用 `{id}.mid`（当前方案）还是保留原文件名？
