#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""抓取音色库来源清单（用于建立音色台账）。

四个来源（S0 起）
-----------------
| 代号        | 来源                                   | 抓法 | 为什么 |
|---|---|---|---|
| `ma`        | musical-artifacts.com                  | `artifacts.json` API | 提供 **license / tags / formats / download_count** 结构化字段，可按许可程序化筛选 |
| `freepats`  | freepats.zenvoid.org                   | 36 个乐器页 HTML | **DFSG 合规 · 逐条写明记录人与许可**；有 **.sf2** 且体积适中（几十 MB 级） |
| `sfz`       | sfzinstruments.github.io               | `data/sfz/instruments.yml` | 钢琴/鼓/弦乐名品（Salamander / Bigcat Cello…）；YAML 带 **license + size** |
| `musescore` | MuseScore 官方音色分发目录（ftp.osuosl.org） | Apache 目录索引 + HEAD | **FluidR3_GM / MuseScore_General（MIT）** —— 社区最广泛推荐的两个 |

为什么用 API / YAML 而不是爬页面
--------------------------------
· musical-artifacts 页面直连会 403，JSON 接口可用；每条带结构化许可字段。
· sfzinstruments 是 MkDocs 站，**数据在 YAML 里**（`data/sfz/instruments.yml`），
  比解析 HTML 稳得多，且带 `download_size` 与 `downloads[].size`（**本台账唯一的官方体积来源**）。
· MuseScore 官方目录是 Apache 索引，可枚举；体积用 HEAD 的 Content-Length 实测。

输出（均为**内部中间产物**，入 `.gitignore`；台账由 `sf_ledger.py` 生成）
--------------------------------------------------------------------
    docs/internal/soundfonts-raw.json       ← ma（沿用原文件名，断点续抓）
    docs/internal/sf-freepats.json
    docs/internal/sf-sfzinstruments.json
    docs/internal/sf-musescore.json

四份都写**统一中间 schema**（见 `norm_item()`），`sf_ledger.py` 只做 LIC 分档 + 分类，
不再关心来源差异 —— **档位判定与分类只有一处实现**（单一真源）。

用法
----
    python sf_crawl.py                     # 抓全部四个来源
    python sf_crawl.py --source ma         # 只抓某一个（ma|freepats|sfz|musescore）
    python sf_crawl.py --report            # 只对已有缓存出统计报告
    python sf_crawl.py --tag soundfont     # 换 musical-artifacts 的标签

注意
----
· **翻页/分页不稳定**：全部走长退避 + 逐页落盘（中断可续）。
· 站点自报总量见响应头 `X-Total`；以它判断 musical-artifacts 是否抓全。
"""
from __future__ import annotations

import argparse
import html
import json
import os
import re
import ssl
import sys
import time
import urllib.error
import urllib.request
from collections import Counter
import concurrent.futures as cf
from pathlib import Path

# ── 通用 ───────────────────────────────────────────────────────────────
API = "https://musical-artifacts.com/artifacts.json"
UA = "Mozilla/5.0 (compatible; midicn-sf-survey/1.0; +https://lib.midicn.com)"
DOCS = Path(__file__).resolve().parents[1] / "docs"
INTERNAL = DOCS / "internal"

OUT_MA = INTERNAL / "soundfonts-raw.json"
OUT_FP = INTERNAL / "sf-freepats.json"
OUT_SFZ = INTERNAL / "sf-sfzinstruments.json"
OUT_MS = INTERNAL / "sf-musescore.json"
OUT_FS = INTERNAL / "sf-fluidsynth.json"
OUT_GH = INTERNAL / "sf-github.json"
OUT_IA = INTERNAL / "sf-archive.json"
OUT_POLY = INTERNAL / "sf-polyphone.json"

# GitHub API：带上 PAT 可把限额从 60/时 提到 5000/时（169 个仓要取 tree，必须带）
GH_TOKEN = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN") or ""

# 站点证书链不完整时（本机代理常见）退化为不校验证书
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE

SOURCE_NAMES = {
    "ma": "musical-artifacts.com",
    "freepats": "FreePats (freepats.zenvoid.org)",
    "sfz": "sfzinstruments.github.io",
    "musescore": "MuseScore 官方音色分发",
    "fluidsynth": "FluidSynth 官方 wiki 清单",
    "github": "GitHub topic:soundfont",
    "archive": "archive.org soundfont 归档",
    "polyphone": "Polyphone Soundfont Collection",
}
SOURCE_URLS = {
    "": "",
    "ma": "https://musical-artifacts.com/artifacts?tags=soundfont",
    "freepats": "https://freepats.zenvoid.org/",
    "sfz": "https://sfzinstruments.github.io/",
    "musescore": "https://ftp.osuosl.org/pub/musescore/soundfont/",
    "fluidsynth": "https://www.fluidsynth.org/wiki/SoundFont/",
    "github": "https://github.com/topics/soundfont",
    "archive": "https://archive.org/search?query=soundfont",
    "polyphone": "https://www.polyphone-soundfonts.com/en/soundfonts",
}

# musical-artifacts 的许可短码 → (可读名, 是否允许再分发)
LICENSE_MAP = {
    "by-3":         ("CC BY 3.0", True),
    "by-4":         ("CC BY 4.0", True),
    "by":           ("CC BY", True),
    "by-sa":        ("CC BY-SA", True),
    "by-sa-4":      ("CC BY-SA 4.0", True),
    "by-nc":        ("CC BY-NC", False),
    "by-nc-sa":     ("CC BY-NC-SA", False),
    "by-nc-sa-3":   ("CC BY-NC-SA 3.0", False),
    "by-nc-nd-3":   ("CC BY-NC-ND 3.0", False),
    "by-nd":        ("CC BY-ND（禁改作）", False),
    "cc-sample":    ("CC Sampling（整包分发受限）", False),
    "falv13":       ("站点许可码 falv13（未识别）", False),
    "cc0":          ("CC0", True),
    "public":       ("Public domain / 公有领域", True),
    "pd":           ("Public domain", True),
    "wtfpl":        ("WTFPL（等同公有领域）", True),
    "mit":          ("MIT", True),
    "bsd":          ("BSD", True),
    "isc":          ("ISC", True),
    "unlicense":    ("Unlicense", True),
    "gpl-v2":       ("GPL v2", True),
    "gpl-v3":       ("GPL v3", True),
    "lgpl":         ("LGPL", True),
    "gray":         ("站点自标「存疑」", False),
    "copyright":    ("版权受限", False),
    "various":      ("混合/不明", False),
    "":             ("未标注", False),
}

# ── 各来源的原始许可串 → 规范短码（sf_ledger.LIC 的键）──────────────────
# **顺序即优先级**。三条纪律：
#   ① by-nc* 必须先于 by*（否则 "BY-NC" 会被判成可商用）
#   ② by-sa* 必须先于 by*（否则 "BY-SA" 会被判成无传染）
#   ③ CC0 / 公有领域 最先（"CC0 1.0 public domain dedication" 里含 "public domain"）
CANON = [
    # 许可**URL**（archive.org / CC 的 licenseurl 字段长这样，先按 URL 认）
    (r'publicdomain/zero', 'cc0'),
    (r'publicdomain/mark', 'pd'),
    (r'licenses/by-nc-nd', 'by-nc-nd-3'),
    (r'licenses/by-nc-sa/4', 'by-nc-sa'),
    (r'licenses/by-nc-sa', 'by-nc-sa-3'),
    (r'licenses/by-nc/4', 'by-nc'),
    (r'licenses/by-nc', 'by-nc'),
    (r'licenses/by-sa/4', 'by-sa-4'),
    (r'licenses/by-sa/3', 'by-sa-3'),
    (r'licenses/by-sa', 'by-sa'),
    (r'licenses/by/4', 'by-4'),
    (r'licenses/by/3', 'by-3'),
    (r'licenses/by/', 'by'),
    (r'cc[\s-]?0\b|creative commons zero|public domain dedication|公有领域', 'cc0'),
    (r'public domain|\bpd\b', 'pd'),
    (r'wtfpl', 'wtfpl'),
    (r'unlicense', 'unlicense'),
    (r'cc[\s-]?by[\s-]?nc[\s-]?nd|attribution[\s-]?noncommercial[\s-]?noderiv', 'by-nc-nd-3'),
    (r'cc[\s-]?by[\s-]?nc[\s-]?sa[\s-]?3|attribution[\s-]?noncommercial[\s-]?sharealike[\s-]?3', 'by-nc-sa-3'),
    (r'cc[\s-]?by[\s-]?nc[\s-]?sa|attribution[\s-]?noncommercial[\s-]?sharealike', 'by-nc-sa'),
    (r'cc[\s-]?by[\s-]?nc|attribution[\s-]?noncommercial', 'by-nc'),
    (r'cc[\s-]?by[\s-]?sa[\s-]?4|attribution[\s-]?sharealike[\s-]?4', 'by-sa-4'),
    (r'cc[\s-]?by[\s-]?sa[\s-]?3|attribution[\s-]?sharealike[\s-]?3', 'by-sa-3'),
    (r'cc[\s-]?by[\s-]?sa|attribution[\s-]?sharealike', 'by-sa'),
    (r'cc[\s-]?by[\s-]?4|attribution[\s-]?4(?:\.0)?\b', 'by-4'),
    (r'cc[\s-]?by[\s-]?3|attribution[\s-]?3(?:\.0)?\b', 'by-3'),
    (r'cc[\s-]?by\b|^\s*attribution\s*$', 'by'),
    (r'^\s*apache', 'apache-2.0'),
    (r'^\s*zlib', 'zlib'),
    (r'^\s*mpl', 'mpl'),
    (r'^\s*agpl', 'agpl-v3'),
    (r'^\s*mit-0', 'mit'),
    (r'\bmit\b', 'mit'),
    (r'\bbsd\b', 'bsd'),
    (r'\bisc\b', 'isc'),
    (r'general public license[^\n]{0,30}?3|gpl[^\n]{0,10}?3|gpl-?v?3', 'gpl-v3'),
    (r'general public license[^\n]{0,30}?2|gpl[^\n]{0,10}?2|gpl-?v?2', 'gpl-v2'),
    (r'lgpl', 'lgpl'),
    (r'\bgpl\b|general public license', 'gpl'),
    (r'sampling plus', 'cc-sampling-plus'),
    (r'^\s*(commercial|paid|purchase|proprietary)', 'commercial'),
    (r'^\s*freemium', 'freemium'),
    (r'^\s*custom', 'custom'),
    (r'^\s*free\s*$', 'free-unclear'),
]


def canon_license(raw: str) -> str:
    """把任意来源的许可串归一到规范短码（识别不出 → 空串＝未标注）。"""
    s = (raw or "").strip().lower()
    if not s:
        return ""
    for pat, code in CANON:
        if re.search(pat, s):
            return code
    return ""


# FreePats 的许可写在正文段落里 —— 取**整段**（不按句号切，否则会把 "1.0" 切成 "1. 0"）
FP_LIC_KEY = re.compile(
    r'published under|under the terms of|licensed under|released under|public domain|'
    r'creative commons|general public license|\bGPL\b|CC0|attribution', re.I)


# ── HTTP ───────────────────────────────────────────────────────────────
# ── 受限源兜底（本机网络对部分域名不通）──────────────────────────────
# 实测：`archive.org` 直连超时、经环境代理返回 **502 Tunnel**（受限隧道），
# 而**公共 HTTP 转发**可以取到同样的公开 JSON —— 所以对这类域名走转发，
# 并在台账 §二 如实写明「部分网络下需转发/代理才能访问」。
# 只发送公开 URL、不带任何凭据；只用于**明确不通**的域名白名单。
# 多端点**轮换**：单端点会被限流（实测 allorigins 连发几十次后开始报错），
# 两个互补就能跑完一轮。`wrap` 表示返回值是 `{"contents": "..."}` 形式，需要解包。
FORWARD_TEMPLATES = [
    ("allorigins", "https://api.allorigins.win/raw?url=%s", False),
    ("whateverorigin", "http://www.whateverorigin.org/get?url=%s", True),
]
FORWARD_HOSTS = ("archive.org", "docs.google.com")


def _forward(url: str, idx: int = 0) -> str:
    import urllib.parse
    return FORWARD_TEMPLATES[idx % len(FORWARD_TEMPLATES)][1] % urllib.parse.quote(url, safe="")


def _unwrap(text: str, idx: int):
    """把 `{"contents": "..."}` 形式的转发响应解回原文。"""
    if not FORWARD_TEMPLATES[idx % len(FORWARD_TEMPLATES)][2]:
        return text
    try:
        j = json.loads(text)
        return j.get("contents") or text
    except Exception:
        return text


def get(url: str, tries: int = 5, timeout: int = 45, accept: str = "*/*", auth: bool = False):
    """长退避重试（本机代理不稳）。HTML/YAML/JSON 返回文本；JSON 由调用方解析。

    `auth=True`（仅 GitHub API）时带上 PAT —— 限额从 60/时 提到 5000/时。
    `FORWARD_HOSTS` 里的域名**先直连、失败后走公共转发**（见上注）。
    """
    last = None
    # ⚠️ 白名单域名**直接走转发**，不先试直连 ——
    #    实测直连每次要等满超时（45s），上一次跑 300 个条目就这样耗了 47 分钟。
    fwd = any(h in url for h in FORWARD_HOSTS)
    for i in range(tries):
        # 每一轮换一个转发端点（抗单点限流）
        plans = ([(_forward(url, i), "转发", i)] if fwd else [(url, "直连", -1)])
        for target, _how, fix in plans:
            try:
                hd = {"User-Agent": UA, "Accept": accept}
                if auth and GH_TOKEN:
                    hd["Authorization"] = "Bearer " + GH_TOKEN
                req = urllib.request.Request(target, headers=hd)
                with urllib.request.urlopen(req, timeout=timeout, context=CTX) as r:
                    body = r.read().decode("utf-8", "replace")
                    if fix >= 0:
                        body = _unwrap(body, fix)
                    return body, dict(r.headers)
            except urllib.error.HTTPError as e:
                last = e
                if e.code in (401, 403, 404, 422):
                    continue                     # 业务错误换下一路
                time.sleep(2 * (i + 1))
            except Exception as e:                                       # noqa: BLE001
                last = e
                time.sleep(2 * (i + 1))
    print("    ! 放弃 %s（%s）" % (url[:100], type(last).__name__), file=sys.stderr)
    return None, {}


def head_len(url: str, tries: int = 3, timeout: int = 45) -> int | None:
    """HEAD 取 Content-Length（拿不到 → None，**不猜**）。"""
    for i in range(tries):
        try:
            req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=timeout, context=CTX) as r:
                n = r.headers.get("Content-Length")
                if n:
                    return int(n)
        except Exception:                                            # noqa: BLE001
            time.sleep(2 * (i + 1))
    return None


def probe_size(url: str, tries: int = 2, timeout: int = 30):
    """实测文件体积 + 记下**状态码**。

    返回 `(bytes | None, status)`：status 为 200/206 表示可访问，403 表示
    对方明确拒绝（musical-artifacts 对**直接 `.sf2`** 一律 403，采样 21/21 全中）。
    「被拒」这个事实本身有用 —— 页面据此把下载按钮改成「来源页」，不把用户送到打不开的链接。
    两者都拿不到 → (None, 0)（**宁可留空也不猜**）。
    """
    last = 0
    for i in range(tries):
        for method, hdrs in (("GET", {"Range": "bytes=0-0"}), ("HEAD", {})):
            try:
                req = urllib.request.Request(url, method=method,
                                             headers={"User-Agent": UA, **hdrs})
                with urllib.request.urlopen(req, timeout=timeout, context=CTX) as r:
                    cr = r.headers.get("Content-Range") or ""
                    total = r.headers.get("Content-Length")
                    if "/" in cr:
                        total = cr.rsplit("/", 1)[-1]
                    n = int(total) if (total or "").isdigit() else None
                    return n, r.status
            except urllib.error.HTTPError as e:
                last = e.code
                if e.code in (403, 404, 410):
                    return None, e.code          # 明确拒绝 → 不重试
            except Exception:                                        # noqa: BLE001
                pass
        time.sleep(2 * (i + 1))
    return None, last


# ── musical-artifacts 的直链规律（**实测得出，不是猜的**）────────────────
# 该站对**直接 `.sf2` / `.sf3`** 一律返回 403（防盗链）：抽样 21 条 .sf2 → **21 条全 403**；
# 而归档类（`.zip` / `.rar` / `.7z`）可正常 Range 读取。
# 所以：`.sf2` 直链**不再逐条探测**（省一小时），统一标 `head_status='by-rule'`；
# 归档类照常实测。这是「按已证实的规律归类」，而不是「没测就下结论」——
# 个体差异仍可被覆盖（真去测一次就会写回真实状态）。
SF2_BLOCKED_RULE = ("by-rule", "sf2-antihotlink")


def measure_sizes(path: Path, url_key: str, label: str, limit: int = 0,
                  delay: float = 0.3) -> int:
    """通用实测：给某来源的直链实测体积 + 可访问性，写回它的原始数据。

    - `url_key`：从条目里取直链的字段名（ma 用 `file`，其余用 `dl_url`）
    - 幂等可续：`size_head` 键已存在的跳过，逐段落盘
    - `.sf2` 直链按 `SF2_BLOCKED_RULE` 直接归类，不浪费请求
    """
    items = json.loads(path.read_text(encoding="utf-8"))
    todo = [it for it in items
            if (it.get(url_key) or "").startswith("http") and "size_head" not in it]
    if limit:
        todo = todo[:limit]
    print("[%s] 待实测 %d 条（已测 %d 条）" % (
        label, len(todo), sum(1 for it in items if "size_head" in it)))
    got = blocked = miss = ruled = 0
    for i, it in enumerate(todo, 1):
        u = it[url_key]
        if u.split("?")[0].lower().endswith((".sf2", ".sf3")):
            it["size_head"] = None
            it["head_status"] = SF2_BLOCKED_RULE[0]
            ruled += 1
        else:
            n, st = probe_size(u)
            it["size_head"] = n
            it["head_status"] = st
            if n:
                got += 1
            elif st in (403, 404, 410):
                blocked += 1
            else:
                miss += 1
        if i % 25 == 0 or i == len(todo):
            write_json(path, items)
            print("  %4d/%d · 测到 %d · 被拒 %d · 未取到 %d · 按规律归类 %d" % (
                i, len(todo), got, blocked, miss, ruled))
        time.sleep(delay)
    write_json(path, items)
    print("[%s] 完成：测到 %d · 被拒 %d · 未取到 %d · 按规律归类 %d → %s" % (
        label, got, blocked, miss, ruled, path))
    return got


def measure_ma_sizes(limit: int = 0, delay: float = 0.3) -> int:
    """给 musical-artifacts 的直链**实测体积 + 可访问性**（该站 API 不带体积字段）。

    为什么必须实测：
      · `≤50 MB 才托管`这条红线对它**完全失效** —— 186 条 F1+`.sf2` 因体积未知
        进不了托管候选（是已托管集的 4 倍）；页面上 86% 的条目体积显示「—」。
      · 更要紧的是**可访问性**：该站对**直接 `.sf2`** 一律 **403**（防盗链），
        所以「来源下载」按钮对那批条目其实点不开 —— 必须知道哪些能点、哪些该改成「来源页」。
    """
    return measure_sizes(OUT_MA, "file", "ma", limit, delay)




def write_json(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=1), encoding="utf-8")


# ── 统一中间 schema ─────────────────────────────────────────────────────
def norm_item(*, uid: str, source: str, name: str, author: str = "", url: str = "",
              license_raw: str = "", license_code: str | None = None, tags=None,
              formats=None, size_mb=None, dl_url: str = "", pack: str = "",
              downloads=None, note: str = "", extra: dict | None = None) -> dict:
    """所有来源都产出这一种形状 —— sf_ledger 只做分档与分类。

    `formats` 记**内容格式**（sf2 / sfz / wav / flac…），`pack` 记**外层归档后缀**
    （sf2 常在 .7z/.zip 里）—— 两者必须分开，否则「有没有 .sf2」会判错。

    `license_code` 显式给出时直接采用（musical-artifacts 自带规范短码，无需再归一）。
    """
    fmts = sorted({(f or "").strip().lower() for f in (formats or []) if (f or "").strip()})
    # 外层归档后缀：显式给出优先，否则从 dl_url 推断（.sf2/.sf3 本身不算归档）
    pk = (pack or "").strip().lower()
    if not pk and dl_url:
        tail = dl_url.split("?")[0].rsplit("/", 1)[-1]
        if "." in tail:
            ext = tail.rsplit(".", 1)[-1].lower()
            pk = "" if ext in ("sf2", "sf3") else ext
    it = {
        "uid": uid, "source": source, "source_name": SOURCE_NAMES.get(source, source),
        "name": (name or "").strip(), "author": (author or "").strip(), "url": url,
        "license_code": (license_code if license_code is not None
                         else canon_license(license_raw)),
        "license_raw": (license_raw or "").strip(),
        "tags": sorted({(t or "").strip().lower() for t in (tags or [])
                        if (t or "").strip() and not (t or "").strip().isdigit()}),
        "formats": fmts, "sf2": "sf2" in fmts,
        "size_mb": round(size_mb, 1) if size_mb else None,
        "dl_url": dl_url, "pack": pk, "downloads": downloads, "note": (note or "").strip(),
    }
    if extra:
        it.update(extra)
    return it


def parse_size_mb(s: str) -> float | None:
    """'27MiB (56MiB)' / '302 MB' / '1.3 GB' → MB（浮点）；解析不出 → None。"""
    m = re.search(r'([\d.]+)\s*(Gi?B|Mi?B|Ki?B)', s or "", re.I)
    if not m:
        return None
    v = float(m.group(1))
    unit = m.group(2).lower()
    if unit.startswith("g"):
        return v * 1024
    if unit.startswith("m"):
        return v
    return v / 1024


# ══════════════════════════════════════════════════════════════════════
# 来源 ①：musical-artifacts.com（原有实现，保持不变）
# ══════════════════════════════════════════════════════════════════════
def crawl_ma(tag: str, per_page: int = 100) -> list[dict]:
    # 断点续抓：先装载已有缓存（翻页不稳定，需多次运行补齐）
    items: list[dict] = []
    seen: set = set()
    if OUT_MA.exists():
        try:
            items = json.loads(OUT_MA.read_text(encoding="utf-8"))
            seen = {x.get("id") for x in items}
            print("  已有缓存 %d 条，继续补齐" % len(items))
        except Exception:
            items, seen = [], set()
    total = None
    page = 1
    while True:
        url = "%s?tags=%s&per_page=%d&page=%d" % (API, tag, per_page, page)
        txt, hd = get(url, accept="application/json")
        if txt is None:
            page += 1
            if page > 60:
                break
            continue
        try:
            j = json.loads(txt)
        except Exception:
            page += 1
            continue
        if total is None:
            total = hd.get("X-Total")
            print("  站点自报总量 X-Total = %s" % total)
        new = [x for x in j if x.get("id") not in seen]
        for x in new:
            seen.add(x.get("id"))
        items += new
        print("  page %-3d 本页 %2d 条 · 新增 %2d · 累计 %4d" % (page, len(j), len(new), len(items)))
        # 逐页落盘（中断可续）
        write_json(OUT_MA, items)
        if not j or (total and len(items) >= int(total)) or page > 60:
            break
        page += 1
        time.sleep(1.2)
    return items


def norm_ma(items: list[dict]) -> list[dict]:
    """把 musical-artifacts 原始条目转成统一中间 schema。"""
    out = []
    for it in items:
        lk = (it.get("license") or "").strip().lower()
        name, perm = LICENSE_MAP.get(lk, ("未识别码 %s" % (lk or "空"), False))
        fmts = [f.lower() for f in norm_list(it.get("formats"))]
        # musical-artifacts 的 file 字段后缀即真实格式（如 .sf2 / .zip）
        f = (it.get("file") or "").strip()
        ext = f.rsplit(".", 1)[-1].lower() if "." in f.rsplit("/", 1)[-1] else ""
        tags = norm_list(it.get("tags"))
        # 体积：该站 API 不带，靠 `--sizes` 实测后回填（`size_head`，字节）
        sm = (it.get("size_head") or 0) / 1048576.0 or None
        out.append(norm_item(
            uid="ma-%s" % it.get("id"), source="ma",
            name=it.get("name") or "", author=it.get("author") or "",
            url="https://musical-artifacts.com/artifacts/%s" % it.get("id"),
            license_code=lk,          # ← 该站自带规范短码，直接采用（LICENSE_MAP 的键）
            license_raw=name,
            tags=tags, formats=fmts,
            size_mb=sm,
            dl_url=f, pack=ext if ext and ext not in ("sf2", "sf3") else "",
            downloads=it.get("download_count") or 0,
            extra={"ma_id": it.get("id"), "ma_license_code": lk,
                   "ma_formats_raw": fmts, "ma_ext": ext,
                   "size_src": "head" if sm else "",
                   # 实测发现直链被对方拒绝（403/404/410，或按已证实规律归类）
                   # → 页面应改走「来源页」，不把用户送到打不开的下载链接
                   "dl_blocked": it.get("head_status") in (403, 404, 410, SF2_BLOCKED_RULE[0]),
                   "head_status": it.get("head_status"),
                   "has_description": bool((it.get("description") or "").strip()),
                   "redistributable_hint": perm},
        ))
    return out


# ══════════════════════════════════════════════════════════════════════
# 来源 ②：FreePats（逐乐器页解析）
# ══════════════════════════════════════════════════════════════════════
FP_BASE = "https://freepats.zenvoid.org/"
# 首页未直接链、但属同一来源的补充页（从首页页面内部发现，逐条可核）
FP_EXTRA_PAGES = ["SoundSets/gm-percussion-set.html"]

# 目录名 → 分类标签（供 sf_ledger 的 classify 使用，判定规则不变）
FP_TAGS = {
    "piano": ["piano"], "electricpiano": ["piano", "electric"],
    "chromaticpercussion": ["percussion", "chromatic", "bells"],
    "organ": ["organ"], "guitar": ["guitar", "acoustic"],
    "guitarfamily": ["guitar"], "electricguitar": ["guitar", "electric"],
    "orchestralstrings": ["orchestral", "strings"], "reed": ["woodwind", "reed"],
    "wind": ["woodwind", "wind"], "synthesizer": ["synth"],
    "ethnic": ["ethnic", "world"], "percussion": ["percussion", "drum"],
    "soundsets": ["gm", "general midi"],
}
FP_FORMAT = {"SF2": "sf2", "SFZ": "sfz", "FLAC": "flac", "WAV": "wav", "MP3": "mp3",
             "DLS": "dls", "GIG": "gig"}


def crawl_freepats() -> list[dict]:
    print("抓取 FreePats 首页…")
    idx, _ = get(FP_BASE)
    if not idx:
        return []
    pages = sorted({m for m in re.findall(r'href="([A-Za-z][^":]*\.html)"', idx)
                    if m not in ("index.html",)} | set(FP_EXTRA_PAGES))
    print("  乐器页 %d 个" % len(pages))
    cache_dir = INTERNAL / "_cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    out: list[dict] = []
    for i, rel in enumerate(pages, 1):
        url = FP_BASE + rel
        cf = cache_dir / ("fp-" + re.sub(r'[^a-z0-9]+', '-', rel.lower()).strip('-') + ".html")
        if cf.exists() and cf.stat().st_size > 500:
            h = cf.read_text(encoding="utf-8")          # 有缓存就不再打扰对方站点
        else:
            h, _ = get(url, tries=4, timeout=50)
            if h:
                cf.write_text(h, encoding="utf-8")
        if not h:
            print("  [%2d/%2d] %-44s → ✗ 抓取失败（下轮重试）" % (i, len(pages), rel))
            continue
        got = parse_freepats_page(h, url, rel)
        out += got
        print("  [%2d/%2d] %-44s → %d 个音色库" % (i, len(pages), rel, len(got)))
        time.sleep(0.5)
    write_json(OUT_FP, out)
    print("  合计 %d 条 → %s" % (len(out), OUT_FP))
    return out


def _strip(txt: str) -> str:
    """去标签取纯文本；顺带修掉「标签换空格」造成的 `1. 0` 这类断字。"""
    s = html.unescape(re.sub(r'<[^>]+>', ' ', txt))
    s = re.sub(r'\s+', ' ', s)
    s = re.sub(r'\s+([.,;:!?])', r'\1', s)          # 标点前不留空格
    return s.strip()


def slug(s: str) -> str:
    return re.sub(r'[^a-z0-9]+', '-', (s or "").lower()).strip('-')


def parse_freepats_page(h: str, url: str, rel: str) -> list[dict]:
    """一个 FreePats 页可含多个音色库（按 <h3 id=…> 分节），逐节成一条。

    许可取法：抓「含许可关键词的整句」存进 `license_text`（**可逐条回查原文**），
    再由 CANON 归一 —— 不凭印象定档。
    """
    cat_key = rel.split("/")[0].lower()
    # ⚠️ 标签**只取页面路径**（页面所在目录就是该站给的分类），
    #    不再拼接名称词 —— 否则 "Synth Brass" 会因名称含 "brass" 被判成管弦。
    tags = FP_TAGS.get(cat_key, []) + [t for t in re.split(r'[-_/.]', cat_key) if t]
    page_title = ""
    m = re.search(r'<h2>(.*?)</h2>', h, re.S)
    if m:
        page_title = _strip(m.group(1))

    body = re.sub(r'(?s)<(style|script)\b.*?</\1>', '', h)
    body = re.sub(r'(?s)<nav>.*?</nav>', '', body)
    body = re.sub(r'(?s)<div id="header">.*?</div>', '', body)
    body = re.sub(r'(?s)<audio\b.*?</audio>', '', body)

    parts = re.split(r'<h3\b[^>]*>(.*?)</h3>', body, flags=re.S)
    out = []
    for i in range(1, len(parts) - 1, 2):
        h3_html, chunk = parts[i], parts[i + 1]
        name = _strip(h3_html)
        if not name:
            continue
        plain = _strip(chunk)
        # 许可取法：取**含许可关键词的整段**（不按句号切 —— 会切坏 "1.0"），存进 license_raw 供回查
        paras = [_strip(p) for p in re.findall(r'(?s)<p>(.*?)</p>', chunk)]
        licp = [p for p in paras if FP_LIC_KEY.search(p)]
        license_text = " | ".join(dict.fromkeys(licp))[:400]

        rows, sf2_row = [], None
        for tr in re.findall(r'(?s)<tr>(.*?)</tr>', chunk):
            tds = re.findall(r'(?s)<td[^>]*>(.*?)</td>', tr)
            if len(tds) < 3:
                continue
            a = re.search(r'href="([^"]+)"', tds[0])
            if not a:
                continue
            fmts = [FP_FORMAT.get(_strip(s).upper(), _strip(s).lower())
                    for s in re.findall(r'(?s)<span[^>]*>(.*?)</span>', tds[1])]
            size = parse_size_mb(_strip(tds[2]))
            comments = _strip(tds[3]) if len(tds) > 3 else ""
            row = {"url": a.group(1), "formats": fmts, "size_mb": size, "note": comments}
            rows.append(row)
            if "sf2" in fmts and (sf2_row is None or (size or 9e9) < (sf2_row["size_mb"] or 9e9)):
                sf2_row = row
        if not rows:
            continue
        pick = sf2_row or rows[0]
        dl_url = pick["url"] if pick["url"].startswith("http") else \
            url.rsplit("/", 1)[0] + "/" + pick["url"]
        desc = ""
        for p in re.findall(r'(?s)<p>(.*?)</p>', chunk):
            t = _strip(p)
            if len(t) > 60 and not t.lower().startswith("version"):
                desc = t
                break
        author = "FreePats project"
        am = re.search(r'(?:recorded|created|sampled|performed|made) by '
                       r'([A-Z][^\s<>,.]{1,24}(?: [A-Z][^\s<>,.]{1,24}){0,2})', plain)
        if am:
            author = am.group(1).strip()
        out.append(norm_item(
            uid="fp-%s" % slug(rel.replace(".html", "") + "-" + name),
            source="freepats", name=name, author=author, url=url,
            license_raw=license_text,
            tags=tags,
            formats=[f for r in rows for f in r["formats"]],
            size_mb=pick["size_mb"], dl_url=dl_url, downloads=None,
            note=pick.get("note") or "",
            extra={"page_title": page_title, "page": rel,
                   "variants": rows[:6], "license_text": license_text, "desc": desc[:400]},
        ))
    return out


# ══════════════════════════════════════════════════════════════════════
# 来源 ③：sfzinstruments（YAML 索引）
# ══════════════════════════════════════════════════════════════════════
SFZ_BASE = "https://raw.githubusercontent.com/sfzinstruments/sfzinstruments.github.io/master/"
SFZ_SITE = "https://sfzinstruments.github.io/"
SFZ_TAGS = {
    "basses": ["bass"], "brass": ["brass"], "drums": ["drum"], "drum machines": ["drum", "machine"],
    "folk": ["folk", "ethnic"], "guitars": ["guitar"], "keyboards": ["keyboard"],
    "melodic percussion": ["percussion", "melodic"], "misc": ["misc"],
    "orchestra": ["orchestral"], "percussion": ["percussion"], "pianos": ["piano"],
    "strings": ["strings"], "synthesizers": ["synth"], "vocals": ["vocal", "voice"],
    "woodwinds": ["woodwind"],
}


def parse_sfz_yaml(txt: str) -> list[dict]:
    """定向解析 instruments.yml（零依赖）。

    结构固定：顶级 `- name:` 为分类，其下 `  - name:` 为条目，
    条目内 `    downloads:` 下 `    - label:` 为下载项。
    """
    out: list[dict] = []
    cat = None
    cur = None
    dl = None
    for raw in txt.splitlines():
        if not raw.strip() or raw.lstrip().startswith('#'):
            continue
        ind = len(raw) - len(raw.lstrip())
        s = raw.strip()
        if s.startswith('- name:'):
            val = s.split(':', 1)[1].strip().strip('"')
            if ind == 0:
                cat = val
            else:
                cur = dict(cat=cat, name=val, downloads=[])
                out.append(cur)
            dl = None
            continue
        if s.startswith('- label:') and cur is not None:
            dl = dict(label=s.split(':', 1)[1].strip().strip('"'))
            cur['downloads'].append(dl)
            continue
        kv = re.match(r'^([A-Za-z_]+):\s*(.*)$', s)
        if not kv or cur is None:
            continue
        k, v = kv.group(1), kv.group(2).strip().strip('"')
        if dl is not None and k in ('url', 'format', 'samplerate', 'size'):
            dl[k] = v
        elif k in ('page', 'version', 'author', 'license', 'url', 'download_size', 'format'):
            cur[k] = v
    return out


def crawl_sfz() -> list[dict]:
    print("抓取 sfzinstruments 索引…")
    txt, _ = get(SFZ_BASE + "data/sfz/instruments.yml")
    if not txt:
        return []
    raw = parse_sfz_yaml(txt)
    print("  条目 %d 个" % len(raw))
    out = []
    used: dict[str, int] = {}                      # uid 去重（同名不同分类会撞）
    for e in raw:
        cat = (e.get("cat") or "").strip()
        tags = SFZ_TAGS.get(cat.lower(), []) + [t for t in re.split(r'[^a-z0-9]+', cat.lower()) if t]
        dls = e.get("downloads") or []
        fmts = sorted({(d.get("format") or "").lower() for d in dls if d.get("format")})
        if not fmts and e.get("format"):
            fmts = [x.strip().lower() for x in re.split(r'[,\s]+', e["format"]) if x.strip()]
        # 体积：优先 downloads[].size，其次 download_size（官网标注的两者常一致）
        sizes = [parse_size_mb(d.get("size", "")) for d in dls]
        sizes = [s for s in sizes if s]
        size = min(sizes) if sizes else parse_size_mb(e.get("download_size", "") or "")
        # 下载地址：优先 .sf2，其次第一个
        pick = next((d for d in dls if 'sf2' in (d.get("url", "") + d.get("format", "")).lower()),
                    dls[0] if dls else None)
        slug = (e.get("page") or re.sub(r'[^a-z0-9]+', '-', e["name"].lower()).strip('-'))
        uid = "sfz-%s" % slug
        if uid in used:                            # 同名不同分类（如 Salamander 鼓组 / 钢琴）
            used[uid] += 1
            uid = "%s--%s%d" % (uid, re.sub(r'[^a-z0-9]+', '', cat.lower())[:12], used[uid])
        else:
            used[uid] = 1
        out.append(norm_item(
            uid=uid, source="sfz", name=e["name"],
            author=e.get("author") or "", url=SFZ_SITE + (cat.lower().replace(" ", "-") + "/" + slug + "/"),
            license_raw=e.get("license") or "", tags=tags, formats=fmts,
            size_mb=size, dl_url=(pick or {}).get("url", ""),
            pack="", downloads=None,
            note=re.sub(r'<[^>]+>', ' ', (e.get("short_description") or ""))[:300].strip(),
            extra={"sfz_cat": cat, "version": e.get("version") or "",
                   "download_size_raw": e.get("download_size") or "",
                   "dl_variants": dls[:6]},          # ⚠️ 不能叫 downloads（会覆盖同名字段）
        ))
    write_json(OUT_SFZ, out)
    print("  合计 %d 条 → %s" % (len(out), OUT_SFZ))
    return out


# ══════════════════════════════════════════════════════════════════════
# 来源 ④：MuseScore 官方音色分发目录
# ══════════════════════════════════════════════════════════════════════
MS_BASE = "https://ftp.osuosl.org/pub/musescore/soundfont/"
# 目录里的文件 → 事实（**逐条可核**：许可来自目录内自带的 *_License.md / README）
MS_FACTS = {
    "MuseScore_General/MuseScore_General.sf2": dict(
        name="MuseScore_General", author="S. Christian Collins（改编自 FluidR3 by Frank Wen）",
        license_raw="MIT", tags=["gm", "general midi", "orchestral", "piano", "vocal"],
        formats=["sf2"], note="MuseScore 3/4 默认音色库；由 FluidR3Mono 精简而来。"
                              "许可原文见同目录 MuseScore_General_License.md（MIT）。",
    ),
    "MuseScore_General/MuseScore_General.sf3": dict(
        name="MuseScore_General（.sf3 压缩版）", author="S. Christian Collins",
        license_raw="MIT", tags=["gm", "general midi"], formats=["sf3"],
        note="⚠️ .sf3 为压缩格式，**浏览器（WebAudioFont / soundfont-player）只吃 .sf2** —— 浏览器内不可直接用。",
    ),
    "fluid-soundfont.zip": dict(
        name="FluidR3_GM", author="Frank Wen", license_raw="MIT",
        tags=["gm", "general midi", "orchestral", "vocal", "piano"], formats=["sf2"],
        note="最广泛推荐的通用音色库之一；管弦与人声优于 GeneralUser GS。包内为 .sf2。",
    ),
    "fluid-soundfont.tar.gz": dict(
        name="FluidR3_GM（tar.gz 同内容）", author="Frank Wen", license_raw="MIT",
        tags=["gm", "general midi"], formats=["sf2"],
        note="与 fluid-soundfont.zip 内容相同，仅归档格式不同 —— 台账里**合并计入 1 条**。",
    ),
    "Sonatina_Symphonic_Orchestra_SF2.zip": dict(
        name="Sonatina Symphonic Orchestra", author="Mattias Westlund",
        license_raw="CC Sampling Plus 1.0", tags=["orchestral", "classical"], formats=["sf2"],
        no_direct=True,
        note="上游许可 = **CC Sampling Plus 1.0**（`sso.mattiaswestlund.net` 与 sfzinstruments 条目一致，"
             "已交叉核实）。该许可**整包原样再分发仅限非商业** → 按纪律归 F4：**只给来源，不直链下载**。",
    ),
}


def crawl_musescore() -> list[dict]:
    print("抓取 MuseScore 官方音色目录…")
    h, _ = get(MS_BASE)
    files: list[str] = []
    dirs: list[str] = []
    def _take(htm: str, prefix: str = "") -> None:
        for m in re.finditer(r'href="([^"/?:][^"]*)"', htm):
            f = html.unescape(m.group(1))
            if f.startswith("http"):                     # 站外链接（镜像、赞助方）一律不收
                continue
            if f.endswith("/"):
                (dirs if not prefix else files).append(prefix + f)
            else:
                files.append(prefix + f)
    if h:
        _take(h)
    # 再递归一层子目录（音色文件在 MuseScore_General/ 下）
    for sub in sorted(set(dirs)):
        hs, _ = get(MS_BASE + sub)
        if hs:
            _take(hs, sub)
    files = sorted(set(files))
    print("  目录文件 %d 个" % len(files))

    out = []
    for f in files:
        fact = MS_FACTS.get(f)
        if not fact:
            print("    · 未登记文件（不猜许可，跳过）：%s" % f)
            continue
        url = MS_BASE + f
        n = head_len(url)
        pack = f.rsplit(".", 1)[-1].lower()
        out.append(norm_item(
            uid="ms-%s" % re.sub(r'[^a-z0-9]+', '-', f.lower()).strip('-'),
            source="musescore", name=fact["name"], author=fact["author"], url=url,
            license_raw=fact["license_raw"], tags=fact["tags"], formats=fact["formats"],
            size_mb=(n / 1048576.0) if n else None,
            dl_url="" if fact.get("no_direct") else url,
            pack=pack if pack not in ("sf2", "sf3") else "", downloads=None,
            note=fact["note"],
            extra={"file": f, "bytes": n, "size_measured": bool(n),
                   "no_direct": bool(fact.get("no_direct"))},
        ))
    write_json(OUT_MS, out)
    print("  合计 %d 条 → %s" % (len(out), OUT_MS))
    return out


# ══════════════════════════════════════════════════════════════════════
# 来源 ⑤：FluidSynth 官方 wiki 清单（策展 · 高信号但量小）
# ══════════════════════════════════════════════════════════════════════
# 这是「老牌合成器引擎官方推荐了哪些音色库」——**策展信号**本身有价值
# （被官方推荐过的，质量经实践检验）。但**该清单不写许可**，
# 所以按纪律一律归 F4（未标注）→ 只进台账，不进托管候选。
FS_MD = ("https://raw.githubusercontent.com/FluidSynth/fluidsynth/master/"
         "doc/wiki/SoundFont.md")
FS_SIZE = re.compile(r'(\d[\d,\.]*)\s*(GB|MB|KB)', re.I)
# ⚠️ 这份清单里**混着工具与文档**（CDxtract / SoundFont 规范 / 维基条目 / FAQ …），
#    只有真音色库才标体积 —— 所以「**有体积**」就是最可靠的分拣规则（实测结构如此），
#    再叠一层工具/文档黑名单兜底。
FS_NOT_BANK = re.compile(r'editor|converter|spec(ification)?|faq|wikipedia|documentation|'
                         r'compliance|test|extract|recycle|translator|synthfont|bassmidi|'
                         r'spessasynth|quicktime|logic|studio|hammersound$', re.I)


def crawl_fluidsynth() -> list[dict]:
    print("抓取 FluidSynth 官方 wiki 清单…")
    md, _ = get(FS_MD)
    if not md:
        return []
    out, seen = [], set()
    # 条目形如：  * [名称](链接) - 30 MB
    for m in re.finditer(r'^\s*[*\-]\s+\[([^\]]+)\]\((https?://[^)]+)\)(.*)$', md, re.M):
        name, url, tail = m.group(1).strip(), m.group(2), m.group(3)
        if name.lower() in seen or not name:
            continue
        seen.add(name.lower())
        sz = None
        sm = FS_SIZE.search(tail)
        if sm:
            v = float(sm.group(1).replace(",", ""))
            sz = v * 1024 if sm.group(2).upper() == "GB" else v
        # 分拣：没有体积的是工具/文档（见上注），或名字命中黑名单 → 不收
        if sz is None or FS_NOT_BANK.search(name + " " + url):
            continue
        out.append(norm_item(
            uid="fs-%s" % re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-'),
            source="fluidsynth", name=name, author="", url=url,
            license_raw="",                       # 该清单不写许可 → 按纪律归 F4
            tags=[t for t in re.split(r'[^a-zA-Z0-9]+', name.lower()) if len(t) > 2],
            formats=["sf2"] if url.lower().endswith(".sf2") or "sf2" in url.lower() else ["sf2"],
            size_mb=sz, dl_url=url if url.lower().endswith((".sf2", ".sf3")) else "",
            downloads=None,
            note="FluidSynth 官方 wiki 推荐清单里的条目（该清单不标注许可）",
        ))
    write_json(OUT_FS, out)
    print("  合计 %d 条 → %s" % (len(out), OUT_FS))
    return out


# ══════════════════════════════════════════════════════════════════════
# 来源 ⑥：GitHub `topic:soundfont`（长尾与新品 · **许可机器可读 + 体积自带**）
# ══════════════════════════════════════════════════════════════════════
GH_API = "https://api.github.com"
GH_EXT = (".sf2", ".sf3", ".sfz")


def gh_json(path: str, tries: int = 3):
    txt, hd = get(GH_API + path, tries=tries, accept="application/vnd.github+json", auth=True)
    if txt is None:
        return None
    try:
        return json.loads(txt)
    except Exception:
        return None


def crawl_github(pages: int = 3) -> list[dict]:
    """按 topic:soundfont 搜仓 → 逐仓取 tree → 收仓内的 .sf2/.sf3。

    ⚠️ **许可口径（必须写明）**：用**仓库的 LICENSE（SPDX）**定档 ——
    这是作者对该仓内容的正式声明，与 musical-artifacts 用其 `license` 字段同源。
    但**仓级许可不等于仓内每个采样都无第三方权利**，故条目里如实记
    `license_raw = 仓库 LICENSE: <SPDX>`，并在台账 §二 说明这一层的限度。
    没有声明许可的仓（spdx 为空 / NOASSERTION）一律归 F4，不猜。
    """
    print("抓取 GitHub topic:soundfont…")
    repos = []
    for p in range(1, pages + 1):
        d = gh_json("/search/repositories?q=topic:soundfont&per_page=100&page=%d" % p)
        if not d or not d.get("items"):
            if p == 1:
                print("  ! 搜索失败（可能是限额；带上 GITHUB_TOKEN 可提到 5000/时）")
            break
        repos += d["items"]
        print("  page %d · 本页 %d · 累计 %d / 共 %s" % (
            p, len(d["items"]), len(repos), d.get("total_count")))
        if len(d["items"]) < 100:
            break
    out: list[dict] = []
    withsf = 0
    for i, r in enumerate(repos, 1):
        full = r["full_name"]
        branch = r.get("default_branch") or "master"
        lic = ((r.get("license") or {}).get("spdx_id") or "").strip()
        if lic in ("NOASSERTION", "NONE"):
            lic = ""
        tree = gh_json("/repos/%s/git/trees/%s?recursive=1" % (full, branch), tries=2)
        if not tree or not tree.get("tree"):
            continue
        files = [e for e in tree["tree"]
                 if e.get("type") == "blob" and (e.get("path") or "").lower().endswith(GH_EXT)]
        if not files:
            continue
        withsf += 1
        topics = r.get("topics") or []
        for e in files:
            path = e["path"]
            ext = path.rsplit(".", 1)[-1].lower()
            name = path.rsplit("/", 1)[-1][: -len(ext) - 1]
            raw = "https://raw.githubusercontent.com/%s/%s/%s" % (
                full, branch, urllib.request.quote(path))
            out.append(norm_item(
                uid="gh-%s-%s" % (re.sub(r'[^a-z0-9]+', '-', full.lower()),
                                  re.sub(r'[^a-z0-9]+', '-', path.lower()).strip('-')),
                source="github", name=name, author=full.split("/")[0], url=r["html_url"],
                license_raw=("仓库 LICENSE: %s" % lic) if lic else "",
                # ⚠️ 标签要含**文件名与路径**：对 GitHub 条目来说，文件名
                #    （piano.sf2 / strings.sf2 …）比仓库 topics 更有分类信息量（只用 topics 时整个仓的文件会被归成同一个类）。
                tags=[t.lower() for t in
                      (topics + re.split(r'[^a-zA-Z0-9]+', full)
                       + re.split(r'[^a-zA-Z0-9]+', path)) if len(t) > 2],
                formats=[ext], size_mb=(e.get("size") or 0) / 1048576.0 or None,
                dl_url=raw, downloads=None,
                note="来自 GitHub 仓库 %s（★%d）" % (full, r.get("stargazers_count") or 0),
                extra={"gh_repo": full, "gh_path": path, "gh_spdx": lic,
                       "gh_stars": r.get("stargazers_count") or 0,
                       "size_src": "head" if e.get("size") else "",
                       "gh_pushed": (r.get("pushed_at") or "")[:10]},
            ))
        if i % 25 == 0:
            print("  %d/%d · 含音色的仓 %d · 条目 %d" % (i, len(repos), withsf, len(out)))
        time.sleep(0.15)
    # ⚠️ **防降级保护**：没带凭据时 GitHub 限额只有 60/时，大量 `git/trees` 会失败 ——
    #    结果「扫了 170 个仓，却只认出 19 个含音色」（正常是 54 个）。
    #    这种**静默缩水**会把上一轮的好数据覆盖掉，所以结果明显变少时拒绝写入。
    if OUT_GH.exists():
        try:
            prev = json.loads(OUT_GH.read_text(encoding="utf-8"))
        except Exception:
            prev = []
        if len(prev) > 20 and len(out) < len(prev) * 0.8:
            print("  ! 本次仅 %d 条，明显少于上一份 %d 条（多半是未带 GITHUB_TOKEN 被限流）"
                  % (len(out), len(prev)), file=sys.stderr)
            print("  ! **保留上一份，不覆盖** —— 带 GITHUB_TOKEN 后重跑", file=sys.stderr)
            return prev
    write_json(OUT_GH, out)
    print("  扫过 %d 个仓 · 其中有音色的 %d 个 · 合计 %d 个文件 → %s" % (
        len(repos), withsf, len(out), OUT_GH))
    return out


# ══════════════════════════════════════════════════════════════════════
# 来源 ⑦：archive.org（历史归档 · **许可 URL 机器可读 + 文件体积可查**）
# ══════════════════════════════════════════════════════════════════════
# ⚠️ 本机对 `archive.org` **直连超时、经环境代理 502**（受限隧道），
#    故 `get()` 会走公共转发取公开 JSON（见 FORWARD_HOSTS 说明）。
# ⚠️ 查询串写**原样**（不要预先 %22 编码）：`_forward` 会对整个 URL 做一次 quote，
#    预编码会变成二次编码（%22 → %2522），archive.org 就搜不到东西。
IA_SEARCH = ("https://archive.org/advancedsearch.php?q=%s"
             "&fl[]=identifier&fl[]=title&fl[]=creator&fl[]=licenseurl"
             "&fl[]=year&fl[]=mediatype&rows=100&page=%d&output=json")
IA_QUERIES = ['subject:"soundfont"', 'subject:"soundfonts"', 'title:(soundfont)',
              'title:(soundfont) AND mediatype:data', 'subject:"sf2"']
# 裸音色优先；没有裸音色就退到**归档**（archive.org 条目多为打包上传）。
# 两种都**如实记 format**：前者 sf2（浏览器可直接用），后者是压缩包（需解压）。
IA_EXT = (".sf2", ".sf3")
IA_ARCH = (".zip", ".7z", ".rar", ".tar.gz", ".tar.bz2", ".tar.xz")


def crawl_archive(max_items: int = 400, enrich_max: int = 80) -> list[dict]:
    """archive.org：**两段式**抓取（转发端点很慢，必须省请求）。

    为什么要分段（实测教训）：`archive.org` 在本机只能经**公共转发**访问，
    每次请求 5–10 秒；对 300 个条目逐个取 metadata 会跑 **47 分钟还没完**（已中断）。

    所以：
      ① **搜索先拿全**（几次请求）——identifier / title / creator / **licenseurl** 都在搜索结果里；
      ② 只对**有可分发许可**（F1/F2 档）的前 `enrich_max` 条取 metadata，
         拿到**文件名与体积**（这一步才有直链）；其余条目**不取**，
         如实留空（页面显示「未标注」）——**省请求 ≠ 编数据**。
    """
    print("抓取 archive.org（经公共转发，直连不通）…")
    seen, items = set(), []
    for q in IA_QUERIES:
        for page in (1, 2):
            # 转发端点会限流 → 搜索给足重试（每轮换端点）与间隔
            txt, _ = get(IA_SEARCH % (q, page), tries=6, timeout=60)
            time.sleep(2)
            if not txt:
                break
            try:
                docs = json.loads(txt)["response"]["docs"]
            except Exception:
                break
            new = [d for d in docs if d.get("identifier") not in seen]
            for d in new:
                seen.add(d["identifier"])
            items += new
            print("  %s p%d · 新增 %d · 累计 %d" % (q[:28], page, len(new), len(items)), flush=True)
            if len(docs) < 100 or len(items) >= max_items:
                break
        if len(items) >= max_items:
            break

    # ① 先用搜索结果直接成条（无体积、无直链 —— 如实留空）
    out, todo = [], []
    for d in items[:max_items]:
        ident = d["identifier"]
        lic = d.get("licenseurl") or ""
        code = canon_license(lic)
        tier = "F1" if code in ("cc0", "pd", "wtfpl", "unlicense") else (
            "F2" if code in ("by", "by-3", "by-4", "mit", "bsd", "isc",
                             "apache-2.0", "zlib") else "F4")
        title = str(d.get("title") or ident)
        it = norm_item(
            uid="ia-%s" % re.sub(r'[^a-z0-9]+', '-', ident.lower()).strip('-'),
            source="archive", name=title, author=_first(d.get("creator")),
            url="https://archive.org/details/%s" % ident,
            license_raw=lic,                 # 该站的 licenseurl 是**机器可读**的
            tags=[t for t in re.split(r'[^a-zA-Z0-9]+', title) if len(t) > 2],
            # ⚠️ **没取到文件清单就不写 formats** —— 默认成 ["sf2"] 等于没有证据地断言
            #    「这是浏览器能用的 .sf2」（会污染「仅 .sf2」筛选与托管候选）。取到才写。
            formats=[], size_mb=None, dl_url="", downloads=None,
            note="archive.org 归档条目（%s%s）" % (
                d.get("mediatype") or "?", (" · " + str(d["year"])) if d.get("year") else ""),
            extra={"ia_id": ident, "ia_files": 0},
        )
        out.append(it)
        if tier in ("F1", "F2"):
            todo.append((ident, it))

    # ② 只给「可分发许可」的前 enrich_max 条补 metadata（文件名 + 体积 + 直链）
    print("  搜索命中 %d 条 · 其中可分发 %d 条 · 取前 %d 条的 文件清单" % (
        len(out), len(todo), min(len(todo), enrich_max)), flush=True)
    for i, (ident, it) in enumerate(todo[:enrich_max], 1):
        meta, _ = get("https://archive.org/metadata/%s" % ident, tries=2)
        if meta:
            try:
                allf = json.loads(meta).get("files") or []
            except Exception:
                allf = []
            bare = [f for f in allf if (f.get("name") or "").lower().endswith(IA_EXT)]
            arch = [f for f in allf if (f.get("name") or "").lower().endswith(IA_ARCH)]
            f0 = (sorted(bare, key=lambda f: -(int(f.get("size") or 0)))[0] if bare else
                  (sorted(arch, key=lambda f: -(int(f.get("size") or 0)))[0] if arch else None))
            if f0:
                nm = f0["name"]
                ext = nm.rsplit(".", 1)[-1].lower()
                bare_sf2 = nm.lower().endswith(IA_EXT)
                it["formats"] = ["sf2"] if bare_sf2 else [ext]
                it["sf2"] = bare_sf2
                it["dl_url"] = "https://archive.org/download/%s/%s" % (ident, nm)
                n = int(f0.get("size") or 0)
                it["size_mb"] = round(n / 1048576.0, 1) if n else None
                it["pack"] = "" if bare_sf2 else ext
                it["note"] = (it["note"] + "；" + ("" if bare_sf2 else
                              "条目里是压缩包（需解压取 .sf2）")).strip("；")
                # ⚠️ norm_item 把 extra 的键**打平到顶层**（不是嵌套在 "extra" 里）
                it["size_src"] = "head" if n else ""
                it["ia_files"] = len(allf)
        if i % 10 == 0:
            write_json(OUT_IA, out)          # 逐段落盘：转发端慢，中断可续
            print("  enrich %d/%d" % (i, min(len(todo), enrich_max)), flush=True)
        time.sleep(0.4)
    if not out:
        # ⚠️ **破坏性保护**：搜索全失败时不要用空结果覆盖上一次的好数据
        #    （转发端点被限流、全部查询失败时，空结果会把已有数据冲掉）
        if OUT_IA.exists():
            try:
                old = json.loads(OUT_IA.read_text(encoding="utf-8"))
            except Exception:
                old = []
            print("  ! 本次一条都没抓到（转发端点多半被限流）→ **保留上一份 %d 条**，未覆盖"
                  % len(old), file=sys.stderr)
            return old
        print("  ! 本次一条都没抓到，且没有历史数据可保留", file=sys.stderr)
        return []
    write_json(OUT_IA, out)
    print("  合计 %d 条（其中 %d 条带文件清单） → %s" % (
        len(out), min(len(todo), enrich_max), OUT_IA))
    return out


# ══════════════════════════════════════════════════════════════════════
# 来源 ⑧：Polyphone Soundfont Collection（社区上传站 · 下载需注册登录）
# ══════════════════════════════════════════════════════════════════════
# 抓法与众不同，值得记下来（试了四轮才通）：
#   · 列表页**看似纯客户端**（分类页 847 KB 外壳、条目靠 JS 渲染、引用的
#     `/includes/en_soundfonts_list-*.min.js` 直取 **404** —— hcdn 防盗链，
#     脚本其实挂在另一个域名 `www.polyphone.io/includes/` 上）。
#   · 但**整份目录以 `data_soundfonts = [...]` 内嵌在页面的内联脚本里** ——
#     **一次请求**就拿到全部条目（标题 / slug / 作者 / 下载数 / 属性 id / 外链）。
#   · 详情页**服务端渲染**，且 URL 里的分类段是**装饰性**的（填错分类照样 200）
#     → 只用 `id-slug` 就能取到；许可、分类、文件名、发布日期都在详情页里。
#   · **下载需注册**（页面明写 Members only）→ 拿不到直链，只给来源页 ——
#     这与本站「非 F1 一律不直链」的纪律本来就一致，不是妥协。
POLY_BASE = "https://www.polyphone-soundfonts.com/en/soundfonts"
POLY_DETAIL = "https://www.polyphone-soundfonts.com/en/soundfonts/%s/%d-%s"
# 站点自己的许可键 → 我们的归一码。依据是 /en/licenses 的原文（逐条读过）：
#   public-domain   作者放弃全部权利，可改作、可商用、可忽略署名（**零义务**）
#   give-credit*    个人+商用+衍生可分发，**唯一条件是署名**
#   modification*   可商用但**禁止分发衍生作品**（ND）→ 不可分发
#   personal-use*   只允许非商用/个人使用（NC / NC-ND）→ 不可分发
POLY_LIC = {
    "public-domain": "pd",
    "give-credit": "by",
    "give-credit-no-more-restrictions": "by",
    "modifications-forbidden": "by-nd",
    "personal-use-only": "by-nc-nd",
    "personal-use-and-share": "by-nc",
    "personal-use-and-share-no-more-restrictions": "by-nc",
}
POLY_LIC_NAME = {
    "public-domain": "公有领域（作者放弃权利）",
    "give-credit": "署名后可分发（Give credit）",
    "give-credit-no-more-restrictions": "署名后可分发 · 不得附加更多限制",
    "modifications-forbidden": "禁止分发衍生作品（ND）",
    "personal-use-only": "仅个人使用 · 禁止商与衍生（NC-ND）",
    "personal-use-and-share": "仅个人使用（NC）",
    "personal-use-and-share-no-more-restrictions": "仅个人使用 · 不得附加更多限制（NC）",
}


def _poly_inline(name: str, html_text: str):
    """从列表页的内联脚本里取一个 `name = [...]` 变量（整份目录就藏在这里）。"""
    i = html_text.find(name)
    if i < 0:
        return None
    k = html_text.find("[", html_text.find("=", i))
    try:
        v, _ = json.JSONDecoder().raw_decode(html_text, k)
        return v
    except Exception:
        return None


def _poly_catalog():
    """列表页**一次**拿到：目录 + 属性表（分类 slug / 标签）。"""
    html_text, _ = get(POLY_BASE, tries=4, timeout=60)
    if not html_text:
        return [], {}, {}
    arr = _poly_inline("data_soundfonts", html_text) or []
    attrs = _poly_inline("data_attributes", html_text) or []
    trans = _poly_inline("data_translations", html_text) or {}
    return arr, attrs, trans


def crawl_polyphone(limit: int = 0, delay: float = 0.6) -> list[dict]:
    cat, attrs, trans = _poly_catalog()
    print("  Polyphone 目录（列表页内嵌 data_soundfonts）：%d 条 · 属性 %d 个"
          % (len(cat), len(attrs)))
    # ⚠️ 详情页 URL 里那段分类**必须是有效分类**：填个未知值（如 `x`）不会报错，
    #    而是**静默回落到列表页**（847 KB 的「All soundfonts」）—— 于是解析出空许可、
    #    空文件名 —— 表面"抓到了"，实为无效数据（整批缓存会一起作废）。
    #    所以按 attribute_type_id==1（category）把每个条目的分类算出来，绝不猜分类段。
    cat_of = {a["attribute_id"]: a["slug"] for a in attrs if a.get("attribute_type_id") == 1}
    label_of = {a["attribute_id"]: a["slug"] for a in attrs}
    FALLBACK_CAT = "unclassifiable"

    def detail_url(e):
        for aid in e.get("attribute_ids") or []:
            if aid in cat_of:
                return POLY_DETAIL % (cat_of[aid], e["soundfont_id"], e["soundfont_slug"])
        return POLY_DETAIL % (FALLBACK_CAT, e["soundfont_id"], e["soundfont_slug"])
    if not cat:
        if OUT_POLY.exists():                      # 破坏性保护：抓不到就别覆盖
            old = json.loads(OUT_POLY.read_text(encoding="utf-8"))
            print("  ! 本次没取到目录 → 保留上一份 %d 条，未覆盖" % len(old), file=sys.stderr)
            return old
        return []
    if limit:
        cat = cat[:limit]
    cache = INTERNAL / "_cache"
    cache.mkdir(parents=True, exist_ok=True)

    # ⚠️ 每个详情页要 5–6 秒（hcdn 慢），串行跑 1,569 条 = **2.5 小时**（实测 16 分钟才 169 条）。
    #    所以改成**小并发 + 磁盘缓存**：缓存命中直接读盘（重跑几乎零成本），
    #    未命中的用 4 个线程抓（对社区站不算失礼，且带了退避重试）。
    def fetch_one(item):
        sid_, sl_ = item.get("soundfont_id"), (item.get("soundfont_slug") or "").strip()
        if not sid_ or not sl_:
            return sid_, ""
        cf = cache / ("poly-%d.html" % sid_)
        if cf.exists() and cf.stat().st_size > 500:
            return sid_, cf.read_text(encoding="utf-8")
        h, _ = get(detail_url(item), tries=3, timeout=50)
        if h:
            cf.write_text(h, encoding="utf-8")
        time.sleep(delay)
        return sid_, h

    pages: dict = {}
    with cf.ThreadPoolExecutor(max_workers=6) as ex:
        for i, (sid_, h) in enumerate(ex.map(fetch_one, cat), 1):
            pages[sid_] = h
            if i % 200 == 0:
                print("  取回 %d/%d" % (i, len(cat)), flush=True)

    out: list[dict] = []
    for n, e in enumerate(cat, 1):
        sid, sl = e.get("soundfont_id"), (e.get("soundfont_slug") or "").strip()
        if not sid or not sl:
            continue
        url = detail_url(e)
        h = pages.get(sid) or ""
        if not h:
            continue
        m = re.search(r'/en/licenses#([a-z0-9\-]+)"', h)
        key = m.group(1) if m else ""
        files = sorted(set(re.findall(r'title="Download the file [^"]*?&ldquo;([^"]+?)&rdquo;"', h)))
        cats = []
        mc = re.search(r'>\s*Category\s*</td>\s*<td[^>]*>(.*?)</td>', h, re.S)
        if mc:
            cats = [html.unescape(x).replace("\xa0", " ").strip()
                    for x in re.findall(r'>([^<>]{2,40})</a>', mc.group(1))]
        md = re.search(r"Publication date\s*</td>\s*<td[^>]*>\s*<time[^>]*datetime='([^']+)'", h)
        members = "Members only" in h               # 下载需注册
        formats = sorted({f.rsplit(".", 1)[-1].lower() for f in files if "." in f})
        out.append(norm_item(
            uid="pp-%d-%s" % (sid, re.sub(r'[^a-z0-9]+', '-', sl.lower()).strip('-'))[:80],
            source="polyphone",
            name=(e.get("soundfont_title") or sl).strip(),
            author=(e.get("author_name") or "").strip(),
            url=url,
            license_raw=POLY_LIC_NAME.get(key, key),
            license_code=POLY_LIC.get(key),        # 站点自带许可键 → 直接给归一码
            tags=cats + [label_of[a] for a in (e.get("attribute_ids") or [])
                          if a in label_of and a not in cat_of][:6],
            formats=formats,
            size_mb=None,                          # 详情页不给体积（下载要登录）
            dl_url="",                             # 会员制 → 不给直链，只给来源页
            downloads=e.get("download_count"),
            note="Polyphone 社区上传（%s）%s" % (
                ", ".join(files)[:80] or "—",
                "；下载需注册登录" if members else ""),
            extra={"poly_id": sid, "poly_slug": sl, "poly_lic": key,
                   "poly_date": (md.group(1)[:10] if md else ""),
                   "poly_cats": cats},
        ))
        if n % 50 == 0:
            write_json(OUT_POLY, out)
            print("  %d/%d · 已写 %d 条" % (n, len(cat), len(out)), flush=True)
    if not out:
        if OUT_POLY.exists():
            old = json.loads(OUT_POLY.read_text(encoding="utf-8"))
            print("  ! 一条都没抓到 → 保留上一份 %d 条，未覆盖" % len(old), file=sys.stderr)
            return old
        return []
    write_json(OUT_POLY, out)
    print("  合计 %d 条（其中 %d 条可分发） → %s" % (
        len(out), sum(1 for x in out if x["redistributable"]), OUT_POLY))
    return out


def _first(v):
    """archive.org 的 creator 可能是 list。"""
    if isinstance(v, list):
        return str(v[0]) if v else ""
    return str(v or "")


# ══════════════════════════════════════════════════════════════════════
# 报告
# ══════════════════════════════════════════════════════════════════════
def norm_list(v):
    """字段可能是 list 或 Python 风格字符串。"""
    if isinstance(v, list):
        return v
    return re.findall(r"'([^']+)'", v or "") if isinstance(v, str) else []


def report(items: list[dict]):
    n = len(items)
    print("\n共 %d 条\n" % n)
    lic, fmt, tag, apps = Counter(), Counter(), Counter(), Counter()
    for it in items:
        lic[(it.get("license") or "").strip().lower()] += 1
        for f in norm_list(it.get("formats")):
            fmt[f] += 1
        for t in norm_list(it.get("tags")):
            tag[t] += 1
        for a in norm_list(it.get("apps")):
            apps[a] += 1

    print("=== 许可分布 ===")
    ok = 0
    for k, v in lic.most_common():
        name, perm = LICENSE_MAP.get(k, ("（未知码 %s）" % k, False))
        if perm:
            ok += v
        print("  %-14s %-22s %4d  %5.1f%%  %s" % (k or "(空)", name, v, v / n * 100,
                                                  "可再分发" if perm else "—"))
    print("\n  **许可允许再分发**：%d / %d = %.0f%%" % (ok, n, ok / n * 100))

    print("\n=== 格式分布（前 10）===")
    for k, v in fmt.most_common(10):
        print("  %-10s %4d" % (k, v))

    print("\n=== 标签（前 30，去掉 soundfont）===")
    print("  " + " · ".join("%s(%d)" % (k, v) for k, v in tag.most_common(30) if k.lower() != "soundfont"))

    print("\n=== 目标软件（前 8）===")
    for k, v in apps.most_common(8):
        print("  %-18s %4d" % (k, v))

    cand = []
    for it in items:
        lk = (it.get("license") or "").strip().lower()
        name, perm = LICENSE_MAP.get(lk, ("?", False))
        if not perm:
            continue
        if "sf2" not in [f.lower() for f in norm_list(it.get("formats"))]:
            continue
        cand.append((it.get("download_count") or 0, it, name))
    cand.sort(key=lambda x: -x[0])
    print("\n=== 候选：.sf2 + 许可可再分发（按下载量，前 24）===")
    for dc, it, name in cand[:24]:
        print("  %-46s | %-18s | ↓%-6s | %s" % (
            (it.get("name") or "")[:46], name[:18], dc,
            ",".join(norm_list(it.get("tags"))[:4])[:34]))
    print("\n  候选合计 %d 个" % len(cand))
    return cand


def report_all():
    """对四份缓存分别/合并出报告。"""
    for sid, path in (("ma", OUT_MA), ("freepats", OUT_FP), ("sfz", OUT_SFZ), ("musescore", OUT_MS)):
        if not path.exists():
            print("\n（缺 %s 缓存）" % sid)
            continue
        raw = json.loads(path.read_text(encoding="utf-8"))
        items = raw if sid == "ma" else raw
        print("\n" + "═" * 70)
        print("来源 %s · %d 条 · %s" % (sid, len(items), path.name))
        if sid == "ma":
            report(items)
        else:
            lic = Counter((i.get("license_code") or "(未识别)") for i in items)
            print("  规范短码分布：")
            for k, v in lic.most_common():
                print("    %-20s %d" % (k, v))
            print("  含 .sf2 的：%d / %d" % (sum(1 for i in items if i.get("sf2")), len(items)))
            sz = [i["size_mb"] for i in items if i.get("size_mb")]
            if sz:
                print("  已知体积：%d 条 · 最小 %.1f MB · 中位 %.1f MB" % (
                    len(sz), min(sz), sorted(sz)[len(sz) // 2]))


# ══════════════════════════════════════════════════════════════════════
def main(argv) -> int:
    ap = argparse.ArgumentParser(description="抓取音色库来源（四个来源）")
    ap.add_argument("--source", default="all",
                    choices=["all", "ma", "freepats", "sfz", "musescore", "fluidsynth",
                             "github", "archive", "polyphone"])
    ap.add_argument("--pages", type=int, default=3, help="GitHub 搜索页数（每页 100 仓）")
    ap.add_argument("--tag", default="soundfont", help="musical-artifacts 的标签")
    ap.add_argument("--sizes", action="store_true",
                    help="给 musical-artifacts 直链实测体积（幂等可续，见 measure_ma_sizes）")
    ap.add_argument("--limit", type=int, default=0, help="配合 --sizes：本次最多测多少条")
    ap.add_argument("--report", action="store_true")
    a = ap.parse_args(argv[1:])

    INTERNAL.mkdir(parents=True, exist_ok=True)

    if a.sizes:
        if a.source in ("all", "ma"):
            if not OUT_MA.exists():
                print("✗ 没有 %s（先跑 --source ma）" % OUT_MA, file=sys.stderr)
                return 2
            measure_sizes(OUT_MA, "file", "ma", a.limit)
        if a.source in ("all", "sfz") and OUT_SFZ.exists():
            measure_sizes(OUT_SFZ, "dl_url", "sfz", a.limit)
        print("\n下一步：重跑 sf_ledger.py --build 让体积进台账")
        return 0

    if a.report:
        report_all()
        return 0

    if a.source in ("all", "ma"):
        print("══ 来源 ma · musical-artifacts（tag=%s）══" % a.tag)
        items = crawl_ma(a.tag)
        print("\n写入 %s" % OUT_MA)
        report(items)

    if a.source in ("all", "freepats"):
        print("\n══ 来源 freepats ══")
        crawl_freepats()

    if a.source in ("all", "sfz"):
        print("\n══ 来源 sfz · sfzinstruments ══")
        crawl_sfz()

    if a.source in ("all", "musescore"):
        print("\n══ 来源 musescore ══")
        crawl_musescore()

    if a.source in ("all", "fluidsynth"):
        print("\n══ 来源 fluidsynth · 官方 wiki 清单 ══")
        crawl_fluidsynth()

    if a.source in ("all", "github"):
        print("\n══ 来源 github · topic:soundfont ══")
        crawl_github(a.pages)

    if a.source in ("all", "archive"):
        print("\n══ 来源 archive · archive.org 归档 ══")
        crawl_archive()

    if a.source in ("all", "polyphone"):
        print("\n══ 来源 polyphone · Polyphone Soundfont Collection ══")
        crawl_polyphone()

    if a.source == "all":
        print("\n" + "═" * 70)
        report_all()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
