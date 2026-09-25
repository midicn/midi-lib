#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""由四个抓取结果生成**音色库台账**（人可读 Markdown + 机器可读 JSON）。

与 MIDI 侧的做法一致（见 `SOURCE-CATALOG.md` / `provenance.json`）：
**单一真源**是 `internal/` 下的四份抓取原始数据（未入 git），
本工具派生出两份台账：`SOUNDFONT-CATALOG.md`（人读）与 `soundfonts.json`（机读）。

四份原始数据（`sf_crawl.py` 产出，统一中间 schema）
--------------------------------------------------
| 文件 | 来源 | 抓法 |
|---|---|---|
| `internal/soundfonts-raw.json` | musical-artifacts.com | artifacts.json API |
| `internal/sf-freepats.json` | freepats.zenvoid.org | 36 个乐器页 |
| `internal/sf-sfzinstruments.json` | sfzinstruments.github.io | data/sfz/instruments.yml |
| `internal/sf-musescore.json` | MuseScore 官方分发目录 | Apache 索引 + HEAD |

**档位判定与分类只在本文件实现一次** —— 抓取器只陈述事实（许可原文 / 标签 / 体积 / 下载地址）。

产出
----
    docs/SOUNDFONT-CATALOG.md     源清单与许可对照全表（全量逐条）
    docs/soundfonts.json          机器可读台账（音色站的数据源）

用法
----
    python sf_ledger.py --build
    python sf_ledger.py --report   # 只看统计
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

DOCS = Path(__file__).resolve().parents[1] / "docs"
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))                      # 复用 sf_crawl 的字段映射（单一实现）
INTERNAL = DOCS / "internal"
RAW_MA = INTERNAL / "soundfonts-raw.json"
RAW_FP = INTERNAL / "sf-freepats.json"
RAW_SFZ = INTERNAL / "sf-sfzinstruments.json"
RAW_MS = INTERNAL / "sf-musescore.json"
RAW_FS = INTERNAL / "sf-fluidsynth.json"
RAW_GH = INTERNAL / "sf-github.json"
RAW_IA = INTERNAL / "sf-archive.json"

OUT_MD = DOCS / "SOUNDFONT-CATALOG.md"
OUT_JSON = DOCS / "soundfonts.json"

# ══════════════════════════════════════════════════════════════════════
# 许可短码 → (可读名, 是否允许自由再分发, 档位)
# ══════════════════════════════════════════════════════════════════════
# 档位与 MIDI 侧 C1/C2/C3 是**两套独立分级**：
#   前者判「这个音色文件能不能再分发」，后者判「这首曲子能不能商用」。
#   F1 = 可自由分发（CC0/PD/WTFPL/Unlicense）· F2 = 署名后可分发（CC BY / MIT / BSD / ISC）
#   F3 = 相同方式共享/传染（CC BY-SA / GPL）· F4 = 不可分发（NC / 存疑 / 版权 / 未标注）
LIC = {
    "cc0":            ("CC0",                       True,  "F1"),
    "public":         ("公有领域（站点标注）",          True,  "F1"),
    "pd":             ("公有领域",                   True,  "F1"),
    "wtfpl":          ("WTFPL（等同公有领域）",        True,  "F1"),
    "unlicense":      ("Unlicense",                 True,  "F1"),
    "by":             ("CC BY",                     True,  "F2"),
    "by-3":           ("CC BY 3.0",                 True,  "F2"),
    "by-4":           ("CC BY 4.0",                 True,  "F2"),
    "mit":            ("MIT",                       True,  "F2"),
    "apache-2.0":     ("Apache 2.0",                 True,  "F2"),
    "zlib":           ("Zlib",                       True,  "F2"),
    "mpl":            ("MPL 2.0",                    True,  "F3"),
    "agpl-v3":        ("AGPL v3",                    True,  "F3"),
    "bsd":            ("BSD",                       True,  "F2"),
    "isc":            ("ISC",                       True,  "F2"),
    "by-sa":          ("CC BY-SA",                  True,  "F3"),
    "by-sa-3":        ("CC BY-SA 3.0",              True,  "F3"),
    "by-sa-4":        ("CC BY-SA 4.0",              True,  "F3"),
    "gpl":            ("GPL",                       True,  "F3"),
    "gpl-v2":         ("GPL v2",                    True,  "F3"),
    "gpl-v3":         ("GPL v3",                    True,  "F3"),
    "lgpl":           ("LGPL",                      True,  "F3"),
    "by-nc":          ("CC BY-NC",                  False, "F4"),
    "by-nc-sa":       ("CC BY-NC-SA",               False, "F4"),
    "by-nc-sa-3":     ("CC BY-NC-SA 3.0",           False, "F4"),
    "by-nc-nd-3":     ("CC BY-NC-ND 3.0",           False, "F4"),
    "by-nd":          ("CC BY-ND（禁改作）",           False, "F4"),
    "cc-sample":      ("CC Sampling（整包分发受限）",    False, "F4"),
    "cc-sampling-plus": ("CC Sampling Plus 1.0",    False, "F4"),
    "falv13":         ("未识别许可码 falv13",          False, "F4"),
    "gray":           ("站点自标「存疑」",              False, "F4"),
    "copyright":      ("版权受限",                   False, "F4"),
    "commercial":     ("商业授权 / 付费产品",           False, "F4"),
    "freemium":       ("Freemium（免费增值）",         False, "F4"),
    "custom":         ("自定义许可（未明）",            False, "F4"),
    "free-unclear":   ("标注 Free 但未指明许可",        False, "F4"),
    "various":        ("混合 / 不明",                 False, "F4"),
    "":               ("未标注",                     False, "F4"),
}

# F4 的**具体原因**（台账 §七 要逐条写明「为什么不收录」）
F4_REASON = {
    "by-nc":          "NC 系列：禁止商业使用 → 我们不代管、不直链",
    "by-nc-sa":       "NC 系列：禁止商业使用 → 我们不代管、不直链",
    "by-nc-sa-3":     "NC 系列：禁止商业使用 → 我们不代管、不直链",
    "by-nc-nd-3":     "NC-ND：禁商用且禁改作 → 我们不代管、不直链",
    "by-nd":          "**ND 禁改作**：音色的主要用途就是衍生（用采样做音乐/改编）→ 收录会误导使用者",
    "cc-sample":      "CC Sampling 系列：整包原样再分发受限（仅非商业）→ 只给来源",
    "cc-sampling-plus": "CC Sampling Plus 1.0：整包原样再分发仅限非商业 → 只给来源",
    "falv13":         "**许可码未识别**（`falv13`）→ 不猜、不收录",
    "gray":           "**站点自标「存疑」** —— 多为商业游戏 ROM 提取，再分发几乎必然侵权",
    "copyright":      "版权受限（原权利人保留全部权利）",
    "commercial":     "商业授权 / 需付费购买",
    "freemium":       "免费增值（免费版许可不明）",
    "custom":         "自定义许可，条款未明 → **许可不明即不收录**",
    "free-unclear":   "标注 Free 但未指明具体许可 → 视为许可不明",
    "various":        "混合 / 不明（同一包内多种来源，无法逐项确认）",
    "":               "**未标注许可** → 许可不明即不收录",
}

# ══════════════════════════════════════════════════════════════════════
# 分类：按标签关键词判定（**顺序即优先级**）
# 结构：(键, 中文名, 英文名, 关键词)
# ══════════════════════════════════════════════════════════════════════
# ⚠️ 新增分类**只能追加在本表末尾** —— 这样任何「已分类」条目都不会被重新归类，
#    只有原先落在 other 的条目会被吸收进来。改前必看这条注释。
CATS = [
    # ⚠️ `game` 的**平台名**（wii / switch / 3ds…）是「这是游戏提取」的明确信号，
    #    必须放在最前 —— 否则「Super Mario 3D World」会因为名字里的 "world" 落进民族类。
    ("game",    "游戏音源", "Game rips", ("video game", "gba", "nintendo", "snes", "sega", "sonic", "vgm",
                                 "mega drive", "nes", "game boy", "touhou", "playstation", "genesis",
                                 "chiptune", "8bit", "16bit", "retro",
                                 "wii", "switch", "gamecube", "3ds", "xbox", "steam", "ps2", "ps3",
                                 "super mario", "pokemon", "zelda", "kirby", "metroid", "undertale",
                                 "deltarune", "friday night funkin", "fnf")),
    ("hist",    "历史合成器/硬件音源", "Vintage hardware", ("korg", "roland", "yamaha", "kurzweil", "ensoniq", "emu",
                                 "e-mu", "akai", "casio", "kawai", "triton", "s90", "jv-", "srj",
                                 "sc-55", "mt-32", "dx7", "ym2612", "mu-", "s-YXG")),
    ("piano",   "钢琴", "Piano", ("piano", "grand", "upright", "steinway", "yamaha c", "clav")),
    ("orch",    "管弦 / 古典", "Orchestral", ("orchestral", "orchestra", "strings", "violin", "cello", "brass",
                                 "woodwind", "flute", "oboe", "trumpet", "horn", "classical", "symphonic")),
    ("ethnic",  "民族 / 世界", "Ethnic / World", ("ethnic", "world music", "asian", "chinese", "japanese", "koto", "shakuhachi",
                                 "sitar", "folk", "celtic", "bagpipe", "kalimba", "jaw harp", "ukulele",
                                 "banjo", "re bab", "kemence", "tagelharpa", "nanfo", "djembe",
                                 # 具体民族乐器（点名比「world」这种泛词可靠）
                                 "balafon", "kora", "gamelan", "shamisen", "erhu", "guqin", "pipa",
                                 "guzheng", "dizi", "suona", "yangqin", "oud", "bouzouki", "hurdy")),
    ("drum",    "打击乐 / 鼓组", "Drums & percussion", ("drum", "percussion", "kit", "tabla")),
    ("synth",   "电子 / 合成", "Synth", ("synth", "fm", "analog", "pad", "lead", "bass synth", "edm", "trance")),
    ("sfx",     "音效 / 其他", "Sound effects", ("sfx", "sound effect", "effect", "noise")),
    ("gm",      "通用 GM 音色库", "General MIDI", ("gm", "general midi", "soundfont pack", "all-in-one")),
    # ── 以下为 2026-09-25 S0 新增（只吸收原先落进 other 的条目）──
    ("guitar",  "吉他 / 贝斯 / 拨弦", "Guitars & basses", ("guitar", "bass", "ukulele", "banjo", "mandolin", "lute")),
    ("organ",   "风琴 / 键盘乐器", "Organs & keys", ("organ", "hammond", "tonewheel", "drawbar", "accordion")),
    ("vocal",   "人声 / 合唱", "Voices & choirs", ("voice", "vocal", "choir", "choral", "oohs", "aahs")),
    ("wind",    "管乐独奏", "Solo wind", ("sax", "saxophone", "clarinet", "harmonica", "recorder",
                                 "ocarina", "pan flute", "tin whistle", "melodica", "bassoon")),
]


def norm(v):
    if isinstance(v, list):
        return v
    return re.findall(r"'([^']+)'", v or "") if isinstance(v, str) else []


def classify(tags: list[str]) -> str:
    low = [t.lower() for t in tags]
    for key, _zh, _en, keys in CATS:
        for k in keys:
            if any(k in t for t in low):
                return key
    return "other"


def lic_of(code: str):
    c = (code or "").strip().lower()
    return LIC.get(c, ("未识别码 %s" % (c or "空"), False, "F4"))


def slug(s: str) -> str:
    return re.sub(r'[^a-z0-9]+', '-', (s or "").lower()).strip('-') or "x"


# ══════════════════════════════════════════════════════════════════════
# 载入四份原始数据 → 统一行
# ══════════════════════════════════════════════════════════════════════
def load_json(p: Path):
    if not p.exists():
        print("  ! 缺 %s —— 先跑 sf_crawl.py --source %s" % (p.name, p.name), file=sys.stderr)
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def unify(items: list[dict], source: str) -> list[dict]:
    """把中间 schema 变成台账行（补 tier / 可读许可名 / 分类）。"""
    rows = []
    for it in items:
        code = (it.get("license_code") or "").strip().lower()
        lname, perm, tier = lic_of(code)
        fmts = [str(f).lower() for f in (it.get("formats") or [])]
        # 体积：来源标注优先；来源没给但**我们实测过**（size_head）就用实测值
        sm, ssrc = it.get("size_mb"), (it.get("size_src") or ("page" if it.get("size_mb") else ""))
        if not sm and it.get("size_head"):
            sm, ssrc = round(it["size_head"] / 1048576, 1), "head"
        rows.append(dict(
            id=it.get("uid") or "%s-%s" % (source, slug(it.get("name", ""))),
            source=source, source_name=it.get("source_name") or source,
            name=(it.get("name") or "").strip(),
            author=(it.get("author") or "").strip(),
            url=it.get("url") or "", dl_url=it.get("dl_url") or "",
            license_code=code, license=lname, license_raw=(it.get("license_raw") or "").strip(),
            redistributable=perm, tier=tier,
            # ⭐ 只有 F1/F2 允许「站内直链下载」；F3 只给指引、F4 连链接都不给
            direct_ok=(tier in ("F1", "F2")),
            cat=classify(it.get("tags") or []),
            tags=it.get("tags") or [], formats=fmts,
            sf2=("sf2" in fmts), pack=(it.get("pack") or ""),
            size_mb=sm,
            # 体积**来源可溯**：'head' = 我们实测；'page' = 来源页标注；'' = 未提供
            size_src=ssrc if sm else "",
            # 实测发现直链被对方拒绝 → 页面改走「来源页」，不给打不开的下载按钮
            dl_blocked=bool(it.get("dl_blocked")), note=(it.get("note") or "").strip(),
            downloads=it.get("downloads"),
            group=slug(it.get("name", "")),
        ))
    return rows


def build():
    ma = load_json(RAW_MA) or []
    fp = load_json(RAW_FP) or []
    sfz = load_json(RAW_SFZ) or []
    ms = load_json(RAW_MS) or []
    fs = load_json(RAW_FS) or []
    gh = load_json(RAW_GH) or []
    ia = load_json(RAW_IA) or []

    import sf_crawl as C
    rows = []
    rows += unify(C.norm_ma(ma), "ma") if ma else []
    rows += unify(fp, "freepats")
    rows += unify(sfz, "sfz")
    rows += unify(ms, "musescore")
    rows += unify(fs, "fluidsynth")
    rows += unify(gh, "github")
    rows += unify(ia, "archive")

    # 去重：同一 uid 只留一条（理论上不会出现，落个保险）
    seen, ded = set(), []
    for r in rows:
        if r["id"] in seen:
            continue
        seen.add(r["id"])
        ded.append(r)
    rows = ded

    # 排序：可分发优先 → 档位 → 分类 → 已知体积升序（便于挑 ≤50MB）→ 下载量
    order = {"F1": 0, "F2": 1, "F3": 2, "F4": 3}
    rows.sort(key=lambda r: (not r["redistributable"], order.get(r["tier"], 9), r["cat"],
                             r["size_mb"] if r["size_mb"] else 9e9,
                             -(r["downloads"] or 0), r["name"].lower()))
    return rows


# ══════════════════════════════════════════════════════════════════════
def build_json(rows: list[dict]) -> dict:
    redist = [r for r in rows if r["redistributable"]]
    tiers = Counter(r["tier"] for r in rows)
    f1 = [r for r in redist if r["tier"] == "F1"]
    host = [r for r in f1 if r["sf2"] and r["size_mb"] and r["size_mb"] <= 50]
    return dict(
        schema=2,
        project="midicn-sfx",
        sources=[
            dict(id="ma", name="musical-artifacts.com", url="https://musical-artifacts.com/",
                 how="artifacts.json API（tags=soundfont）", fetched="2026-09-25",
                 count=sum(1 for r in rows if r["source"] == "ma")),
            dict(id="freepats", name="FreePats", url="https://freepats.zenvoid.org/",
                 how="36 个乐器页 HTML 解析", fetched="2026-09-25",
                 count=sum(1 for r in rows if r["source"] == "freepats")),
            dict(id="sfz", name="sfzinstruments", url="https://sfzinstruments.github.io/",
                 how="data/sfz/instruments.yml", fetched="2026-09-25",
                 count=sum(1 for r in rows if r["source"] == "sfz")),
            dict(id="musescore", name="MuseScore 官方音色分发", url="https://ftp.osuosl.org/pub/musescore/soundfont/",
                 how="Apache 目录索引 + HEAD 实测体积", fetched="2026-09-25",
                 count=sum(1 for r in rows if r["source"] == "musescore")),
            dict(id="fluidsynth", name="FluidSynth 官方 wiki 清单", url="https://www.fluidsynth.org/wiki/SoundFont/",
                 how="官方 wiki 页（仓库内 doc/wiki/SoundFont.md）", fetched="2026-09-25",
                 count=sum(1 for r in rows if r["source"] == "fluidsynth")),
            dict(id="github", name="GitHub topic:soundfont", url="https://github.com/topics/soundfont",
                 how="搜索 API 取仓 + git/trees 列文件（许可取仓 LICENSE 的 SPDX）",
                 fetched="2026-09-25",
                 count=sum(1 for r in rows if r["source"] == "github")),
            dict(id="archive", name="archive.org", url="https://archive.org/search?query=soundfont",
                 how="搜索 API + 逐条目 metadata（许可 licenseurl 机器可读、文件体积可查）",
                 fetched="2026-09-25",
                 count=sum(1 for r in rows if r["source"] == "archive")),
        ],
        fetched="2026-09-25",
        total=len(rows),
        redistributable=len(redist),
        by_tier=dict(tiers),
        by_license=dict(Counter(r["license"] for r in rows)),
        by_category=dict(Counter(r["cat"] for r in rows)),
        by_source=dict(Counter(r["source"] for r in rows)),
        # 站点展示用的名字表（分类 / 档位）—— 单一真源就在这里
        cat_names=CAT_NAMES,
        tier_names={
            "F1": {"zh": "F1 · 可自由分发", "en": "F1 · Free to redistribute",
                   "desc_zh": "CC0 / 公有领域 / WTFPL / Unlicense —— 零署名负担、零传染",
                   "desc_en": "CC0 / public domain / WTFPL / Unlicense — no attribution, no copyleft"},
            "F2": {"zh": "F2 · 署名后可分发", "en": "F2 · Redistribute with credit",
                   "desc_zh": "CC BY / MIT / BSD / ISC —— 须署名，可商用、可改作",
                   "desc_en": "CC BY / MIT / BSD / ISC — attribution required, commercial use and remixing allowed"},
            "F3": {"zh": "F3 · 相同方式共享", "en": "F3 · Share-alike",
                   "desc_zh": "CC BY-SA / GPL —— 有传染性，衍生作品须同许可；本站只给指引不托管",
                   "desc_en": "CC BY-SA / GPL — copyleft; derivatives must keep the same licence. Pointers only."},
            "F4": {"zh": "F4 · 本站不收录", "en": "F4 · Not listed",
                   "desc_zh": "禁止商用 / 禁止改作 / 存疑 / 版权受限 / 未标注",
                   "desc_en": "Non-commercial, no-derivatives, unclear or restricted — excluded"},
        },
        f1_sf2=sum(1 for r in f1 if r["sf2"]),
        hostable_f1_50mb=len(host),
        entries=[r for r in redist],
        excluded=[dict(id=r["id"], source=r["source"], name=r["name"], author=r["author"],
                       license=r["license"], license_code=r["license_code"],
                       cat=r["cat"], url=r["url"], downloads=r["downloads"],
                       reason=F4_REASON.get(r["license_code"])
                       or ("**许可码未识别**（`%s`）→ 不猜、不收录" % r["license_code"]
                           if r["license_code"] else "**未标注许可** → 许可不明即不收录"))
                  for r in rows if not r["redistributable"]],
    )


# ══════════════════════════════════════════════════════════════════════
# Markdown 台账
# ══════════════════════════════════════════════════════════════════════
CAT_NAME = {k: zh for k, zh, _en, _keys in CATS}
CAT_NAME["other"] = "其他 / 未归类"
# 供站点直接使用的分类名表（**单一真源**：只有本文件定义分类与名字）
CAT_NAMES = {k: {"zh": zh, "en": en} for k, zh, en, _keys in CATS}
CAT_NAMES["other"] = {"zh": "其他 / 未归类", "en": "Other"}
TIER_NAME = {
    "F1": "F1 · 可自由分发（CC0 / 公有领域 / WTFPL / Unlicense）",
    "F2": "F2 · 署名后可分发（CC BY / MIT / BSD / ISC）",
    "F3": "F3 · 相同方式共享（有传染性：CC BY-SA / GPL）",
    "F4": "F4 · 不收录（禁止商用 / 禁止改作 / Sampling 系列 / 存疑 / 版权受限 / 未标注）",
}
SRC_NAME = {"ma": "musical-artifacts", "freepats": "FreePats", "sfz": "sfzinstruments",
            "musescore": "MuseScore"}


def _size(r) -> str:
    s = r["size_mb"]
    return ("%.1f MB" % s) if s else "—"


def _row(r, i: int) -> str:
    nm = r["name"][:70].replace("|", "/")
    au = (r["author"] or "—")[:30].replace("|", "/")
    dl = str(r["downloads"]) if r["downloads"] is not None else "—"
    return "| %d | %s | %s | %s | %s | %s | %s | %s | %s |" % (
        i, nm, au, SRC_NAME.get(r["source"], r["source"]), r["license"],
        "✓" if r["sf2"] else "—", _size(r), dl, r["cat"])


def build_md(rows: list[dict], doc: dict) -> str:
    L: list[str] = []
    A = L.append
    redist = doc["entries"]
    ex = doc["excluded"]
    N = doc["total"]

    A("# SOUNDFONT CATALOG · 音色库台账")
    A("")
    A("> **用途**：音色站（`sf.midicn.com`）的内容真源 —— 目录三层的全部依据。")
    A("> **可复现**：`tools/sf_crawl.py`（抓四个来源）→ `tools/sf_ledger.py --build`（生成本文件）。")
    A("> **机器可读版**：[`soundfonts.json`](soundfonts.json)（音色站直接读它）。")
    A("> **本文件为全量明细** —— 不只是「收录了什么」，还包括**我们审过什么、以及为什么排除**。")
    A("")
    A("## 一、总览")
    A("")
    A("| 项 | 值 |")
    A("|---|---|")
    A("| 登记条目（四来源合计） | **%d** |" % N)
    A("| **许可允许再分发** | **%d（%.0f%%）** ← 进入候选池 |" % (
        doc["redistributable"], doc["redistributable"] / N * 100))
    A("| **不可再分发** | **%d（%.0f%%）** |" % (
        N - doc["redistributable"], (N - doc["redistributable"]) / N * 100))
    A("| 含 `.sf2` 格式的可分发条目 | **%d** |" % sum(1 for r in redist if r["sf2"]))
    A("| **F1 且 `.sf2` 且 ≤50 MB**（可直接托管） | **%d** |" % doc["hostable_f1_50mb"])
    A("")
    A("**四档分布**（判「这个音色文件能不能再分发」）：")
    A("")
    A("| 档位 | 含义 | 数量 | 占比 |")
    A("|---|---|---:|---:|")
    for t in ("F1", "F2", "F3", "F4"):
        n = doc["by_tier"].get(t, 0)
        A("| **%s** | %s | **%d** | %.1f%% |" % (t, TIER_NAME[t].split("·", 1)[1].strip(),
                                                n, n / N * 100))
    A("")
    A("**按来源**：")
    A("")
    A("| 来源 | 抓法 | 条目 | 可分发 |")
    A("|---|---|---:|---:|")
    for s in doc["sources"]:
        n = s["count"]
        rd = sum(1 for r in rows if r["source"] == s["id"] and r["redistributable"])
        A("| **%s** | %s | %d | %d |" % (s["name"], s["how"], n, rd))
    A("")
    A("**按用途分类**（两口径并列 —— 全部条目 / 可分发候选）：")
    A("")
    A("| 分类 | 全部 | 可分发 |")
    A("|---|---:|---:|")
    allc = Counter(r["cat"] for r in rows)
    redc = Counter(r["cat"] for r in redist)
    for key, name, _en, _keys in CATS + [("other", "其他 / 未归类", "Other", ())]:
        a, b = allc.get(key, 0), redc.get(key, 0)
        if a or b:
            A("| %s | %d | %d |" % (name, a, b))
    A("")
    # 体积覆盖率（诚实说明：这一项不是 100%，而且**不能靠猜**）
    _ns = sum(1 for r in rows if r["size_mb"])
    A("**体积已知情况**（共 %d 条）：" % N)
    A("")
    A("| 体积来源 | 条数 | 说明 |")
    A("|---|---:|---|")
    A("| 我们**实测**（Range / HEAD） | %d | musical-artifacts 里可访问的直链 |"
      % sum(1 for r in rows if r["size_src"] == "head"))
    A("| **来源页标注** | %d | FreePats / sfzinstruments / MuseScore 页面自带 |"
      % sum(1 for r in rows if r["size_src"] == "page"))
    A("| **未提供** | %d | 上游不提供、且直链拒绝访问（见 §二）—— **宁缺勿错，不猜** |"
      % (N - _ns))
    A("")
    A("### 1.1 三个口径必须分清（读表前先看这段）")
    A("")
    A("- **全部条目**：四个来源抓到的**全部**记录（含明确不可分发的）。")
    A("- **可分发候选**：许可允许再分发的（F1 + F2 + F3）—— 音色站目录收录这些。")
    A("- **可直接托管**：F1 且是 `.sf2` 且体积 ≤50 MB —— 站内直下只有这一档。")
    A("")
    A("> 历史沿革：早期版本台账只有 musical-artifacts 一个来源（1,067 条 / 595 候选）。")
    A("> S0 补抓 FreePats / sfzinstruments / MuseScore 之后，来源覆盖与条目数均上升。")
    A("")

    # ── §二 数据来源与覆盖度 ──
    A("## 二、⚠️ 数据来源与覆盖度（诚实说明）")
    A("")
    A("**已覆盖（累计 %d 个来源）**：" % len(doc["sources"]))
    A("")
    A("| 来源 | 抓法 | 为什么抓它 |")
    A("|---|---|---|")
    for s in doc["sources"]:
        why = {
            "ma": "唯一的**批量结构化许可字段**来源（可按许可程序化筛选）",
            "freepats": "**DFSG 合规 · 质量经实践检验**；有 `.sf2` 且体积适中；"
                        "**民族/世界乐器的主要来源**（bagpipe / kalimba / jaw harp / ukulele…）",
            "sfz": "钢琴与鼓组名品（Salamander / Bigcat Cello / SM Drums…）；YAML 自带许可与体积",
            "musescore": "**FluidR3_GM / MuseScore_General（MIT）** —— 社区最广泛推荐的两个",
            "fluidsynth": "**引擎官方推荐过的**（策展信号）—— 该清单不写许可，故只进台账作指引",
            "github": "长尾与新品；**许可取自仓库 LICENSE（机器可读）**，且 `git/trees` **自带文件体积**",
            "archive": "历史归档（含公有领域素材）；**licenseurl 与文件体积都可查**；"
                       "⚠️ 本机直连不通，需经转发/代理",
        }.get(s["id"], "")
        A("| %s | %s | %s |" % (s["name"], s["how"], why))
    A("")
    A("**尚未覆盖（诚实列出，不假装已全网）**：")
    A("")
    A("| 优先级 | 来源 | 状态 | 为什么 |")
    A("|---|---|---|---|")
    A("| — | MuseScore 社区策展表格 | ✅ **已核实：不是音色清单** | 抓下来逐列看过：它是 Musescore 的"
      "**乐器分类 / 预设映射表**（Genre / Group / Family / Instrument / Unique ID，656 行），"
      "并不列音色文件 → **不作为台账来源**（不硬凑） |")
    A("| P2 | Polyphone Soundfont Collection | ⏳ 待抓 | 另一处活跃的社区合集，站点结构需先摸 |")
    A("| P3 | 各站点自建的「soundfont 索引页」 | ⏳ 长尾 | 多为一页链接，量小且许可需逐条核 |")
    A("")
    A("> 复现提示：`archive.org` 的搜索与条目接口在部分网络下**不可直接访问**，")
    A("> 此时可用任意可用的 HTTP 转发取同样的公开 JSON；本表的条目即由此得到。")
    A("")
    A("### 2.1 ⚠️ 两个来源的**限度**（必须一起读，否则会误判）")
    A("")
    A("**① GitHub `topic:soundfont` 的许可口径**：许可取自**仓库的 LICENSE（SPDX）**——")
    A("那是作者对该仓内容的正式声明，与 musical-artifacts 用其 `license` 字段同源。")
    A("但**仓级许可不等于仓内每个采样都没有第三方权利**（有的仓是把零散素材打包重发）。")
    A("所以：条目里如实记「仓库 LICENSE: <SPDX>」，**没有声明许可的仓一律归 F4**；")
    A("真要托管时必须逐个再过一遍 —— 本线目前**不托管** GitHub 源的文件。")
    A("")
    A("**② GitHub 源的境内可达性**：它的直链是 `raw.githubusercontent.com`。")
    A("实测**本机可达**（Range 206），但该域名在境内访客侧**不稳** —— ")
    A("所以它只作**目录与来源指引**：`url` 给仓库页，直链照给（能不能下取决于访客网络），")
    A("但我们**不复刻、不托管**该来源的文件（站点直下只做 FreePats 那批稳定可达的）。")
    A("")
    A("> 说明：`sfzinstruments` 绝大多数条目是 **SFZ + WAV/FLAC**（不是 `.sf2`），")
    A("> 浏览器（WebAudioFont / soundfont-player）只吃 `.sf2` —— 故它们进**目录与指引层**，")
    A("> 不进「站内托管」层。这一点在台账里由 `formats` 字段如实体现，不做暗示。")
    A("")
    A("**⚠️ 关于体积：musical-artifacts 这一项拿不到完整数据（实测结论）**")
    A("")
    A("它的 API **不带体积字段**（详情 JSON 18 个字段里没有 size/bytes），")
    A("所以只能对直链**实测**（`Range: bytes=0-0` 读 `Content-Range` 的总长）。实测发现：")
    A("")
    _ma = [r for r in rows if r["source"] == "ma"]
    _blk = [r for r in _ma if r["dl_blocked"]]
    _nodl = [r for r in _ma if not r["dl_url"]]
    _meas = [r for r in _ma if r["dl_url"] and not r["dl_blocked"]]
    A("| 直链类型 | 条数 | 实测结果 |")
    A("|---|---:|---|")
    A("| 可访问（多为归档 `.zip` / `.rar` / `.7z`） | %d | ✅ 体积已回填（本表「我们实测」） |" % len(_meas))
    A("| **被拒绝访问**（直接 `.sf2` 一类，403 防盗链） | %d | ❌ 抽样 21/21 全 403 → 统一按不可直连归类 |" % len(_blk))
    A("| 无直链（只有 `mirrors` 等外链） | %d | — 无法测 |" % len(_nodl))
    A("")
    A("两个后果，都写清楚了：")
    A("")
    A("1. **体积留空**：这些条目的体积在台账与页面上标为「**未提供**」，")
    A("   而不是编一个数字 —— 这也是「≤50 MB 才托管」这条红线对它们不生效的原因。")
    A("2. **下载按钮改走来源页**：既然直链会被 403 拒绝，页面就不再给「来源下载」按钮，")
    A("   改给「**来源页** ↗」——不把用户送到打不开的链接。")
    A("")

    # ── §三 处置规则 ──
    A("## 三、处置规则（每一档怎么处理，以及为什么）")
    A("")
    A("| 档位 | 授权性质 | 本站处置 | 理由 |")
    A("|---|---|---|---|")
    A("| **F1** | CC0 / 公有领域 / WTFPL / Unlicense | ✅ **站内托管 + 直链下载** | 零署名负担、零传染、无合规悬案 |")
    A("| **F2** | CC BY / MIT / BSD / ISC | ✅ 站内托管（**F2 专区**） | 须**逐条附署名与许可原文摘录** |")
    A("| **F3** | CC BY-SA / GPL | ⚠️ **只给指引，不托管** | 有**传染性** —— 衍生作品须同许可，会把义务传给使用者 |")
    A("| **F4** | NC / ND / Sampling 系列 / 存疑 / 版权受限 / 未标注 | ❌ **不托管、不直链** | 见下方逐类说明 |")
    A("")
    A("> **入档规则（两条都要满足）**：① 允许**商用**再分发；② 允许**改作**。")
    A("> 只满足一条的（如 CC BY-ND 允许再分发但禁改作、CC BY-NC 允许改作但禁商用）一律归 F4 —— ")
    A("> 因为音色的**主要用途就是衍生使用**，收了会误导使用者。这条规则让 F4 的含义是「**本站不收录**」，")
    A("> 而不只是「法律上不可分发」—— 台账里逐条写明**具体是哪一条不满足**。")
    A("")
    A("### 3.1 为什么 F4 一律不收（逐类给原因）")
    A("")
    A("| 原因 | 数量 | 说明 |")
    A("|---|---:|---|")
    rc = Counter(x["reason"] for x in ex)
    for k, v in rc.most_common():
        A("| %s | %d | |" % (k, v))
    A("")
    A("### 3.2 ⭐ 曲目的 C1/C2/C3 与音色的 F1–F4 是**两套独立的分级**")
    A("")
    A("> 前者判「**这首曲子**能不能商用」，后者判「**这个音色文件**能不能再分发」。")
    A("> **同一个 F1 音色可以用来演奏 C3 曲目** —— 两者互不推导。")
    A("")
    A("### 3.3 许可优先：同一音色多来源时取哪一条")
    A("")
    A("同一音色可能同时出现在多个来源（例：Salamander Grand Piano 在 FreePats 与 sfzinstruments 都有）。")
    A("台账**两条都留**（各自记明来源与格式），并给出 `group` 字段供站点聚合展示；")
    A("若要**托管控件**，优先取：**① F1 优于 F2 优于 F3** → ② **`.sf2` 优于其余格式** → ③ **体积小者**。")
    A("")

    # ── §四/五/六 逐档全量 ──
    for num, t in (("四", "F1"), ("五", "F2"), ("六", "F3")):
        sel = [r for r in rows if r["tier"] == t]
        A("## %s、%s · 全量 %d 条" % (num, TIER_NAME[t], len(sel)))
        A("")
        A("> 本档**逐条列明**：名称 / 作者 / 来源 / 许可 / 是否 `.sf2` / 体积 / 下载量 / 分类。")
        A("")
        if t == "F1":
            A("**其中可直接托管的（`.sf2` 且 ≤50 MB）**：%d 条 —— 见 §十。"
              % sum(1 for r in sel if r["sf2"] and r["size_mb"] and r["size_mb"] <= 50))
            A("")
        A("| # | 名称 | 作者 | 来源 | 许可 | .sf2 | 体积 | 下载 | 分类 |")
        A("|---:|---|---|---|---|---:|---|---:|---|")
        for i, r in enumerate(sel, 1):
            A(_row(r, i))
        A("")

    # ── §七 F4 全量 ──
    A("## 七、F4 · **不收录** · 全量 %d 条（**逐条写明为什么不收录**）" % len(ex))
    A("")
    A("| # | 名称 | 作者 | 来源 | 许可 | 分类 | 不收录原因 |")
    A("|---:|---|---|---|---|---|---|")
    for i, r in enumerate(
            sorted([r for r in rows if not r["redistributable"]],
                   key=lambda r: (r["license_code"], -int(r["downloads"] or 0))), 1):
        A("| %d | %s | %s | %s | %s | %s | %s |" % (
            i, r["name"][:60].replace("|", "/"), (r["author"] or "—")[:26].replace("|", "/"),
            SRC_NAME.get(r["source"], r["source"]), r["license"], r["cat"],
            F4_REASON.get(r["license_code"], "许可不允许再分发")))
    A("")
    A("> **关于「存疑」那 358 条**：不是我们不知道它们是什么，")
    A("> 而是**该站自己**标记了「来源存疑」—— 绝大多数是从**商业游戏 ROM** 里提取的音色，")
    A("> 原权利人从未授权再分发。**我们不做这种赌。**")
    A("")

    # ── §八 继承自 lib 站 ──
    A("## 八、从 lib 站继承的 5 个音色库（已全部并入本台账）")
    A("")
    A("| 音色库 | 许可（**本次核实**） | 现在在台账里的落点 | 档位 |")
    A("|---|---|---|---|")
    A("| FluidR3_GM | **MIT** | `ms-fluid-soundfont-zip`（MuseScore 官方分发） | F2 |")
    A("| MuseScore_General | **MIT** | `ms-musescore-general-musescore-general-sf2` | F2 |")
    A("| Salamander Grand Piano | **CC BY 3.0**（此前「待核」→ 已核实） | `fp-piano-acoustic-grand-piano-salamander-grand-piano`（FreePats，**含 `.sf2`**）+ sfzinstruments 条目 | F2 |")
    A("| Yamaha Disklavier Pro Grand Piano（YDP） | **CC BY 3.0**（此前「待核」→ 已核实） | `fp-piano-acoustic-grand-piano-ydp-grand-piano` | F2 |")
    A("| The City Piano | **公有领域** | sfzinstruments `pianos/*` | F1 |")
    A("")
    A("> 结论：**5 个全部落进台账**，两个「待核」项的许可靠页面原文核实完毕（不是凭印象）。")
    A("> **但注意**：这 5 个里只有 FreePats 的两个提供 `.sf2`；其余是 SFZ/WAV/FLAC 或 >50 MB，")
    A("> 属目录 + 指引层。")
    A("")

    # ── §九 统计 ──
    A("## 九、统计（三口径并列，**不要混用**）")
    A("")
    A("| 口径 | 定义 | 数量 |")
    A("|---|---|---:|")
    A("| 全部条目 | 四来源抓到的全部记录 | **%d** |" % N)
    A("| 可分发候选 | F1 + F2 + F3 | **%d** |" % doc["redistributable"])
    A("| 可自由分发（F1） | CC0 / PD / WTFPL / Unlicense | **%d** |" % doc["by_tier"].get("F1", 0))
    A("| F1 且 `.sf2` | 可直接站内分发 | **%d** |" % doc["f1_sf2"])
    A("| **F1 且 `.sf2` 且 ≤50 MB** | **首批托管候选** | **%d** |" % doc["hostable_f1_50mb"])
    A("")
    A("**许可分布（全部 %d 条）**：" % N)
    A("")
    A("| 许可 | 数量 | 占比 | 档位 | 可再分发 |")
    A("|---|---:|---:|---|---|")
    for name, n in Counter(r["license"] for r in rows).most_common():
        t = next((r["tier"] for r in rows if r["license"] == name), "F4")
        p = next((r["redistributable"] for r in rows if r["license"] == name), False)
        A("| %s | %d | %.1f%% | %s | %s |" % (name, n, n / N * 100, t, "✅" if p else "❌"))
    A("")

    # ── §十 对音色站的含义 ──
    host = [r for r in redist if r["tier"] == "F1" and r["sf2"] and r["size_mb"]
            and r["size_mb"] <= 50]
    A("## 十、对音色站的意义（三层的实际条数）")
    A("")
    A("| 层 | 内容 | 条数 |")
    A("|---|---|---:|")
    A("| 第 1 层 · 目录 | 可分发候选（台账驱动、静态生成） | **%d** |" % doc["redistributable"])
    A("| 第 2 层 · 托管 | F1 · `.sf2` · ≤50 MB（站内直下） | **%d** |" % len(host))
    A("| 第 3 层 · 指引 | F4（只写来源地址，**不托管、不直链**） | **%d** |" % len(ex))
    A("")
    A("### 10.1 首批托管候选（F1 · `.sf2` · ≤50 MB，按体积升序）")
    A("")
    A("| # | 名称 | 作者 | 来源 | 许可 | 体积 | 分类 |")
    A("|---:|---|---|---|---|---:|---|")
    for i, r in enumerate(sorted(host, key=lambda r: r["size_mb"]), 1):
        A("| %d | %s | %s | %s | %s | %.1f MB | %s |" % (
            i, r["name"][:56].replace("|", "/"), (r["author"] or "—")[:24].replace("|", "/"),
            SRC_NAME.get(r["source"], r["source"]), r["license"], r["size_mb"],
            CAT_NAME.get(r["cat"], r["cat"])))
    A("")
    A("### 10.2 民族 / 世界音色（原本只有 2 个，S0 后的实际改善）")
    A("")
    eth = [r for r in redist if r["cat"] == "ethnic"]
    A("可分发候选里的民族 / 世界音色 **%d 条**：" % len(eth))
    A("")
    if eth:
        A("| 名称 | 作者 | 来源 | 许可 | .sf2 | 体积 |")
        A("|---|---|---|---|---:|---|")
        for r in sorted(eth, key=lambda r: (r["tier"], r["size_mb"] or 9e9)):
            A("| %s | %s | %s | %s | %s | %s |" % (
                r["name"][:52].replace("|", "/"), (r["author"] or "—")[:24].replace("|", "/"),
                SRC_NAME.get(r["source"], r["source"]), r["license"],
                "✓" if r["sf2"] else "—", _size(r)))
    A("")
    A("> FreePats 是民族音色的**主力来源**（bagpipe / jaw harp / kalimba / ukulele /")
    A("> world-and-rare-percussion 等），且多为 **CC0 + `.sf2`** —— 这是 S0 带来的最大改善，")
    A("> 直接回应了规划里「民族音色只有 2 个」的最大缺口。")
    A("")
    A("---")
    A("")
    A("*本台账由 `tools/sf_ledger.py --build` 生成，**勿手改**；改动请改抓取数据后重跑。*")
    return "\n".join(L) + "\n"


# ══════════════════════════════════════════════════════════════════════
def main(argv) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--report", action="store_true")
    a = ap.parse_args(argv[1:])

    rows = build()
    if not rows:
        print("没有数据 —— 先跑 sf_crawl.py", file=sys.stderr)
        return 2
    doc = build_json(rows)

    print("六来源合计 %d 条 · 可分发 %d · F1 %d · F1+sf2 %d · 可托管(≤50MB) %d" % (
        doc["total"], doc["redistributable"], doc["by_tier"].get("F1", 0),
        doc["f1_sf2"], doc["hostable_f1_50mb"]))
    print("  分来源：", dict(Counter(r["source"] for r in rows)))
    print("  分档位：", doc["by_tier"])
    print("  分分类：", dict(Counter(r["cat"] for r in rows).most_common()))

    if a.build:
        md = build_md(rows, doc)
        OUT_MD.write_text(md, encoding="utf-8")
        OUT_JSON.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
        print("已生成 %s（%.1f KB）" % (OUT_MD, OUT_MD.stat().st_size / 1024))
        print("已生成 %s（%.1f KB）" % (OUT_JSON, OUT_JSON.stat().st_size / 1024))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
