# DATA-STRUCTURE · 数据存放结构说明

> 本文说明 midicn-lib 的数据存放位置与访问方式。**MIDI 文件不在 git 仓库中**（原因见文末），
> 而是存放在 **Releases 数据包** 与 **lib.midicn.com 在线服务**中。

## 一、三层结构总览

| 层 | 位置 | 内容 | 访问方式 |
|---|---|---|---|
| ① 文档层 | 本仓库（git） | 双语 README · 数据卡 · 质量档案 · `meta/` 索引 · 工具链 | 网页浏览 / `git clone` |
| ② 数据层 | **[Releases → v1.0](../../releases/tag/v1.0)** | 三个 zip：`main` (36.8MB) · `piano-special` (247MB) · `meta` (3.9MB) | 点击下载 |
| ③ 服务层 | **[lib.midicn.com](https://lib.midicn.com)** | 80,662 个 MIDI + 索引，在线试听与按需下载 | HTTP 直链 / 在线播放器 |

## 二、数据包内部结构（Releases 中的 zip）

```
midicn-lib-v1.0/
├── meta/
│   ├── catalog.json              全量目录（80,662 条，17.8 MB）
│   ├── index-by-composer.json    作曲家 → 曲目 id 索引
│   ├── index-by-region.json      地域索引
│   ├── index-by-period.json      音乐时期索引
│   ├── index-by-source.json      来源数据集索引
│   └── MD5SUMS.txt               全部文件校验
│
├── main/                         🟢 可商用（48,140 首）
│   ├── folk-ireland/             爱尔兰传统（26,689）TheSession, Norbeck
│   ├── folk-world/               世界民谣（10,818）Essen, Wikifonia(PD)
│   ├── classical-open/           古典开放许可（6,624）Mutopia, OpenScore, music21, MusicNet
│   ├── klezmer-balkan/           克莱兹梅尔/巴尔干（1,487）ABCMisc
│   ├── drum/                     鼓点节奏（1,149）Groove MIDI
│   ├── folk-british/             英美民谣（1,033）Nottingham
│   └── game/                     游戏音乐（340）OpenGameArt
│
└── piano-special/                🟡 非商用（32,522 首，CC BY-NC-SA）
    └── piano/                    古典钢琴（ariamidi）
```

**文件命名规则**：`{id}.mid`（如 `thesession-000000.mid`），与 `catalog.json` 的 `id` 字段一一对应。

## 三、在线访问（无需下载）

所有文件通过 **lib.midicn.com** 可直接访问，路径与上述结构完全一致：

```
https://lib.midicn.com/main/folk-ireland/thesession-000000.mid
https://lib.midicn.com/piano-special/piano/aria-001190.mid
https://lib.midicn.com/meta/catalog.json
https://lib.midicn.com/meta/index-by-composer.json
```

在线播放器：**https://lib.midicn.com**（五维筛选 + 浏览器合成播放）

## 四、为什么 MIDI 不放在 git 仓库里？

8 万个平均 6.5KB 的小文件进入 git 会导致：

1. **提交极慢**：实测 commit 8 万文件在 Windows 上 40 分钟仍未完成（每文件生成 git 对象 + 杀毒扫描）
2. **仓库膨胀**：`.git` 对象体积约为原始文件的 1.5 倍，且每次改动都会新增副本
3. **克隆灾难**：用户 `git clone` 需要拉取全部历史对象

因此采用业界通行做法：**git 仓库只放文档与索引，数据本体走 Releases（单文件上限 2GB）+ 在线服务（CDN 加速）**。

> 参考同类实践：MAESTRO（数据在 Google Cloud Storage）· aria-midi（数据在 figshare）·
> Hugging Face Datasets（数据不在 GitHub 仓库，走 LFS / HF Hub）。

## 五、如何获取数据

| 需求 | 方式 |
|---|---|
| 下载完整数据包 | [Releases → v1.0](../../releases/tag/v1.0) 三个 zip（附 MD5 校验） |
| 网站/应用直接调用 | `https://lib.midicn.com/<path>` 直链（见第三节） |
| 只要目录与索引 | `meta.zip`（3.9 MB）或 `/meta/*.json` 直链 |
| 单个曲目 | 在 [播放器](https://lib.midicn.com) 里搜索后播放，或按命名规则拼路径 |

## 六、更新机制

数据更新通过 **Release + 自动部署**完成：

1. 本地更新数据 → 生成新 Release（如 v1.1）
2. 触发 `midi-lib-site` 仓库的部署流水线（自动从 Release 下载并组装）
3. lib.midicn.com 全站刷新（约 5–10 分钟）

网站仓库（[midi-lib-site](https://github.com/midicn/midi-lib-site)）因此只包含播放器页面与部署脚本——
这是设计，不是缺失。
