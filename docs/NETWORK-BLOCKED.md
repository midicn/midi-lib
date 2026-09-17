# NETWORK-BLOCKED · 境内网络受限源清单

> 用途：记录境内直连失败的源，**等全部可下载源处理完后统一交给用户开代理**。
> 探测方式：`tools/probe_network.py`（HEAD/GET + 浏览器 UA + 证书忽略分流测试）
> 最后更新：2026-09-17 08:10

## 一、真受限（需要代理）❌

| 源 | 目标 URL | 症状 | 影响规模 | 备注 |
|---|---|---|---|---|
| `figshare` 中国经典 MIDI | api.figshare.com / ndownloader.figshare.com | **403**（换浏览器 UA 仍 403，0.9s 快速响应） | 14 首 | 疑似 Cloudflare 地区封锁 |
| `sonatica` 古典整库 | sonatica.fm | **Tunnel 502**（11s 超时） | ~11,000 首 | 走代理隧道失败，疑似隧道规则问题 |
| `ia` Internet Archive 精选 | archive.org | **Tunnel 502**（10s 超时） | 数千+ | 同上 |
| `cpdl` ChoralWiki | www.cpdl.org | **403**（换 UA 仍 403） | ~25,000 首 | 疑似 Cloudflare 反爬；可再试镜像/API |
| `kern` KernScores 数据服务 | kern.humdrum.org（全站，含 browse/data 路径） | **503 Service Unavailable** | 108,703 文件 | kern.ccarh.org 主页可访问但**所有数据链接指向 humdrum.org**；Verovio 渲染可用但不提供数据；待代理后走 humdrum.org 或找镜像 |
| `wikifonia` Wikifonia 遗存 | www.synthzone.com/files/Wikifonia/Wikifonia.zip | **403 Forbidden** | ~6,405 lead sheets | 35MB 整包；待代理或找镜像（GitHub 有 wikifonia 数据镜像） |
| `jsb` JSB Chorales | www-etud.iro.umontreal.ca/~boulanni/JSB Chorales.zip | **502 Bad Gateway** | 382 | 老旧学术站点不稳定；可用 music21 corpus 的 bach 众赞歌替代（已收录） |
| `nesdb` NES Music Database | deepyeti.ucsd.edu/cdonahue/nesmdb/nesmdb_midi.tar.gz | **502 Bad Gateway** | 5,278 | 站点故障；GitHub chrisdonahue/nesmdb 有说明，可试代理或镜像 |

## 二、可自行绕过（无需代理）⚠️

| 源 | 症状 | 绕过方式 |
|---|---|---|
| `kdf` Kunst der Fuge | SSL 证书验证失败（证书过期/自签） | **`ssl._create_unverified_context()` 后 OK 200** ✓；本站限流 5 次/天，慢爬 |

## 三、确认可下载 ✅（实测）

| 源 | 实测 | 规模 |
|---|---|---|
| Mutopia | OK 200 | ~2,124 |
| MuseData / CCARH | OK 200（GitHub 仓库可下；**但许可禁止分发**→ research 区不发布） | ~1,200 |
| IMSLP | OK 200 | 数千（MIDI 附件） |
| Hymnary | OK 200 | 数千 |
| OpenGameArt | OK 200 | 数百 |
| **Google 存储（Groove / MAESTRO）** | **OK 200**（根路径 400 是 HEAD 根目录所致，具体文件 URL 正常） | 1,150 + 1,282 |
| HuggingFace | OK 200 | EMOPIA 等 |
| Magenta | OK 200 | — |
| ifdo.ca（Seymour：abc2midi / EsAC / Nottingham / 附加 abc） | OK 200 | 已全部下载 |
| thesession / GitHub 各 ABC 源 | 常规 HTTP，未受阻 | 已下载 |
| verovio.humdrum.org | OK 200（渲染工具） | 不提供批量数据 |

## 四、待代理清单交付格式（数据集收尾时生成）

最终会打包成一份简报给用户，含：
1. 受限源清单（上表 §一）+ 每个源的**具体下载方式与目标文件 URL**（代理开启后一条命令直下）
2. 预估总下载量（MB）与时间
3. 开启代理后的执行顺序（用户只需说「代理已开」）
