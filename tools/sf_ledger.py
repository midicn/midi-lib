#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""由抓取结果生成**音色库台账**（人可读 Markdown + 机器可读 JSON）。

与 MIDI 侧的做法一致（见 `SOURCE-CATALOG.md` / `provenance.json`）：
**单一真源**是 `internal/soundfonts-raw.json`（抓取原始数据，未入 git），
本工具派生出两份台账：`SOUNDFONT-CATALOG.md`（人读）与 `soundfonts.json`（机读）。

产出
----
    docs/SOUNDFONT-CATALOG.md     源清单与许可对照全表
    docs/soundfonts.json          机器可读台账

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
RAW = DOCS / "internal" / "soundfonts-raw.json"
OUT_MD = DOCS / "SOUNDFONT-CATALOG.md"
OUT_JSON = DOCS / "soundfonts.json"

# 许可短码 → (可读名, 是否允许再分发, 档位)
# 档位对应我们 MIDI 侧的 C1/C2/C3 思路：
#   F1 = 可自由分发（CC0/PD/WTFPL）· F2 = 署名后可分发（CC BY / MIT）·
#   F3 = 相同方式共享/传染（CC BY-SA / GPL）· F4 = 不可分发（NC / 存疑 / 版权）
LIC = {
    "cc0":        ("CC0",                     True,  "F1"),
    "public":     ("公有领域（站点标注）",         True,  "F1"),
    "pd":         ("公有领域",                 True,  "F1"),
    "wtfpl":      ("WTFPL（等同公有领域）",      True,  "F1"),
    "unlicense":  ("Unlicense",               True,  "F1"),
    "by":         ("CC BY",                   True,  "F2"),
    "by-3":       ("CC BY 3.0",               True,  "F2"),
    "by-4":       ("CC BY 4.0",               True,  "F2"),
    "mit":        ("MIT",                     True,  "F2"),
    "bsd":        ("BSD",                     True,  "F2"),
    "isc":        ("ISC",                     True,  "F2"),
    "by-sa":      ("CC BY-SA",                True,  "F3"),
    "by-sa-4":    ("CC BY-SA 4.0",            True,  "F3"),
    "gpl":        ("GPL",                     True,  "F3"),
    "gpl-v2":     ("GPL v2",                  True,  "F3"),
    "gpl-v3":     ("GPL v3",                  True,  "F3"),
    "lgpl":       ("LGPL",                    True,  "F3"),
    "by-nc":      ("CC BY-NC",                False, "F4"),
    "by-nc-sa":   ("CC BY-NC-SA",             False, "F4"),
    "by-nc-sa-3": ("CC BY-NC-SA 3.0",         False, "F4"),
    "by-nc-nd-3": ("CC BY-NC-ND 3.0",         False, "F4"),
    "gray":       ("站点自标「存疑」",            False, "F4"),
    "copyright":  ("版权受限",                 False, "F4"),
    "various":    ("混合 / 不明",               False, "F4"),
    "":           ("未标注",                   False, "F4"),
}

# 分类：按标签关键词判定（顺序即优先级）
CATS = [
    ("game",    "游戏音源",     ("video game", "gba", "nintendo", "snes", "sega", "sonic", "vgm",
                                 "mega drive", "nes", "game boy", "touhou", "playstation", "genesis",
                                 "chiptune", "8bit", "16bit", "retro")),
    ("hist",    "历史合成器/硬件音源", ("korg", "roland", "yamaha", "kurzweil", "ensoniq", "emu",
                                 "e-mu", "akai", "casio", "kawai", "triton", "s90", "jv-", "srj",
                                 "sc-55", "mt-32", "dx7", "ym2612", "mu-", "s-YXG")),
    ("piano",   "钢琴",         ("piano", "grand", "upright", "steinway", "yamaha c", "clav")),
    ("orch",    "管弦 / 古典",   ("orchestral", "orchestra", "strings", "violin", "cello", "brass",
                                 "woodwind", "flute", "oboe", "trumpet", "horn", "classical", "symphonic")),
    ("ethnic",  "民族 / 世界",   ("ethnic", "world", "asian", "chinese", "japanese", "koto", "shakuhachi",
                                 "sitar", "folk", "celtic", "bagpipe")),
    ("drum",    "打击乐 / 鼓组",  ("drum", "percussion", "kit", "tabla")),
    ("synth",   "电子 / 合成",   ("synth", "fm", "analog", "pad", "lead", "bass synth", "edm", "trance")),
    ("sfx",     "音效 / 其他",   ("sfx", "sound effect", "effect", "noise", "voice", "vocal")),
    ("gm",      "通用 GM 音色库", ("gm", "general midi", "soundfont pack", "all-in-one")),
]


def norm(v):
    if isinstance(v, list):
        return v
    return re.findall(r"'([^']+)'", v or "") if isinstance(v, str) else []


def classify(tags: list[str]) -> str:
    low = [t.lower() for t in tags]
    for key, _name, keys in CATS:
        for k in keys:
            if any(k in t for t in low):
                return key
    return "other"


def lic_of(code: str):
    c = (code or "").strip().lower()
    return LIC.get(c, ("未识别码 %s" % (c or "空"), False, "F4"))


def load():
    if not RAW.exists():
        print("缺少抓取缓存 %s —— 先跑 sf_crawl.py" % RAW, file=sys.stderr)
        sys.exit(2)
    return json.loads(RAW.read_text(encoding="utf-8"))


def build(items: list[dict]) -> tuple[str, dict]:
    rows = []
    for it in items:
        lk = (it.get("license") or "").strip().lower()
        name, perm, tier = lic_of(lk)
        tags = norm(it.get("tags"))
        fmts = [f.lower() for f in norm(it.get("formats"))]
        rows.append(dict(
            id=it.get("id"), name=(it.get("name") or "").strip(),
            author=(it.get("author") or "").strip(),
            url=it.get("url") or "", license_code=lk, license=name, redistributable=perm,
            tier=tier, cat=classify(tags), tags=tags, formats=fmts,
            sf2=("sf2" in fmts), size_note="", downloads=it.get("download_count") or 0,
        ))
    rows.sort(key=lambda r: (not r["redistributable"], r["cat"], -r["downloads"]))

    # ── JSON 台账 ──
    cnt = Counter(r["license"] for r in rows)
    cats = Counter(r["cat"] for r in rows)
    tiers = Counter(r["tier"] for r in rows)
    doc = dict(
        schema=1, project="midicn-sfx", source="musical-artifacts.com (tags=soundfont)",
        fetched="2026-09-25", total=len(rows),
        redistributable=sum(1 for r in rows if r["redistributable"]),
        by_license=dict(cnt), by_tier=dict(tiers), by_category=dict(cats),
        entries=[r for r in rows if r["redistributable"]],       # 台账只登记可用候选
        excluded=[dict(id=r["id"], name=r["name"], license=r["license"], cat=r["cat"],
                       downloads=r["downloads"])
                  for r in rows if not r["redistributable"]],
    )

    # ── Markdown ──
    L = []
    A = L.append
    A("# SOUNDFONT CATALOG · 音色库台账")
    A("")
    A("> **用途**：为「lib 站固定音色 + 音色站（分站）」两站规划提供依据。")
    A("> **数据来源**：`musical-artifacts.com`（tag `soundfont`）**全量 1,067 条**，2026-09-25 抓取。")
    A("> **可复现**：`tools/sf_crawl.py`（抓取）→ `tools/sf_ledger.py --build`（生成本文件）。")
    A("> **机器可读版**：[`soundfonts.json`](soundfonts.json)。")
    A("")
    A("## 一、总览")
    A("")
    A("| 项 | 值 |")
    A("|---|---|")
    A("| 登记条目 | **%d** |" % len(rows))
    A("| **许可允许再分发** | **%d（%.0f%%）** ← 可进入我们候选池 |" % (doc["redistributable"], doc["redistributable"] / len(rows) * 100))
    A("| **不可再分发（含站点自标存疑）** | **%d（%.0f%%）** |" % (len(rows) - doc["redistributable"], (len(rows) - doc["redistributable"]) / len(rows) * 100))
    A("| 含 `.sf2` 格式的可分发条数 | %d |" % sum(1 for r in rows if r["redistributable"] and r["sf2"]))
    A("")
    A("## 二、许可分布（全部 %d 条）" % len(rows))
    A("")
    A("| 许可 | 数量 | 占比 | 档位 | 可再分发 |")
    A("|---|---:|---:|---|---|")
    for name, n in cnt.most_common():
        t = next((r["tier"] for r in rows if r["license"] == name), "F4")
        p = next((r["redistributable"] for r in rows if r["license"] == name), False)
        A("| %s | %d | %.1f%% | %s | %s |" % (name, n, n / len(rows) * 100, t, "✅" if p else "❌"))
    A("")
    A("**档位说明**（沿用 MIDI 侧思路）：")
    A("- **F1 可自由分发**：CC0 / 公有领域 / WTFPL / Unlicense —— 站内可直接托管")
    A("- **F2 署名后可分发**：CC BY / MIT / BSD —— 站内可托管，须署名")
    A("- **F3 相同方式共享（传染）**：CC BY-SA / GPL —— 站内可托管，但衍生作品须同许可")
    A("- **F4 不可分发**：NC 系列 / 版权受限 / **站点自标存疑** / 未标注 —— **不托管、不推荐**")
    A("")
    A("## 三、按用途分类（可分发候选 %d 个）" % doc["redistributable"])
    A("")
    A("| 分类 | 数量 | 说明 |")
    A("|---|---:|---|")
    for key, name, _keys in CATS + [("other", "其他 / 未归类", ())]:
        n = cats.get(key, 0)
        if n:
            A("| %s | %d | |" % (name, n))
    A("")
    for key, name, _keys in CATS + [("other", "其他 / 未归类", ())]:
        sel = [r for r in rows if r["redistributable"] and r["cat"] == key]
        if not sel:
            continue
        A("### %s（%d 个 · 按下载量前 12）" % (name, len(sel)))
        A("")
        A("| 名称 | 作者 | 许可 | .sf2 | 下载 |")
        A("|---|---|---|---:|---:|")
        for r in sel[:12]:
            A("| %s | %s | %s | %s | %d |" % (
                r["name"][:56].replace("|", "/"), r["author"][:22].replace("|", "/"),
                r["license"], "✓" if r["sf2"] else "—", r["downloads"]))
        A("")
    A("## 四、未收录（%d 个）" % len(doc["excluded"]))
    A("")
    A("> 与 MIDI 侧同一纪律：**许可不清或不许再分发的一律不进候选池**。")
    A("> 其中 **%d 个（%.0f%%）被该站自己标记为「存疑」（`gray`）** ——" % (
        sum(1 for r in rows if r["license_code"] == "gray"),
        sum(1 for r in rows if r["license_code"] == "gray") / len(rows) * 100))
    A("> 多为**从商业游戏 ROM 提取的音色**，站点无法确认其再分发权。")
    A("")
    ex = [r for r in rows if not r["redistributable"]]
    bylic = Counter(r["license"] for r in ex)
    A("| 未收录原因 | 数量 |")
    A("|---|---:|")
    for k, v in bylic.most_common():
        A("| %s | %d |" % (k, v))
    A("")
    A("## 五、对两站规划的含义")
    A("")
    A("1. **lib 站**：固定**一个**音色库（默认 GeneralUser GS），不随曲目增多而增大体积；")
    A("   用户想换音色 → 去音色站。")
    A("2. **音色站**：内容分两层 ——")
    A("   - **可托管层（F1/F2/F3 共 %d 个）**：许可明确，可直接站内分发；" % doc["redistributable"])
    A("     优先做 **F1**（CC0/PD，**%d 个**，零署名负担）。" % sum(1 for r in rows if r["redistributable"] and r["tier"] == "F1"))
    A("   - **指引层（F4）**：只写「来源 + 查询地址」，**不托管、不直链下载**。")
    A("3. **版权纪律**：与数据来源目录一致 —— **许可不明即不收录**；")
    A("   该站自标的 `gray` 一律按不可分发处理。")
    A("")
    A("---")
    A("")
    A("*本台账由 `tools/sf_ledger.py` 生成，勿手改；改动请改抓取数据后重跑。*")
    return "\n".join(L) + "\n", doc


def main(argv) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--report", action="store_true")
    a = ap.parse_args(argv[1:])
    items = load()
    md, doc = build(items)
    print("源 %d 条 · 可再分发 %d · 分类 %d 种" % (
        doc["total"], doc["redistributable"], len(doc["by_category"])))
    if a.build:
        OUT_MD.write_text(md, encoding="utf-8")
        OUT_JSON.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
        print("已生成 %s（%.1f KB）" % (OUT_MD, OUT_MD.stat().st_size / 1024))
        print("已生成 %s（%.1f KB）" % (OUT_JSON, OUT_JSON.stat().st_size / 1024))
    if not a.build and not a.report:
        print(md[:2000])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
