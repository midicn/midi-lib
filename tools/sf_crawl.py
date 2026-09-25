#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""抓取 musical-artifacts.com 的音色库清单（用于建立音色台账）。

为什么用 API 而不是爬页面
------------------------
该站提供 `artifacts.json` 接口，每条带 **license / tags / formats / download_count**
等结构化字段 —— 可以**按许可程序化筛选**，比解析网页可靠得多。
（页面直连会 403，JSON 接口可用。）

用法
----
    python sf_crawl.py                 # 抓取并写入 docs/internal/soundfonts-raw.json
    python sf_crawl.py --tag soundfont # 换标签
    python sf_crawl.py --report        # 只对已有缓存出统计报告

注意
----
· **翻页不稳定**：会大量超时/失败，故用长退避 + 逐页落盘（中断可续）。
· 站点自报总量见响应头 `X-Total`；以它判断是否抓全。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.request
from collections import Counter
from pathlib import Path

API = "https://musical-artifacts.com/artifacts.json"
UA = "Mozilla/5.0 (compatible; midicn-sf-survey/1.0; +https://lib.midicn.com)"
OUT = Path(__file__).resolve().parents[1] / "docs" / "internal" / "soundfonts-raw.json"

# 该站的许可短码 → 人的可读名 + 是否允许再分发
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


def get(url: str, tries: int = 5, timeout: int = 45):
    """长退避重试（本机代理不稳）。返回 (json, headers)。"""
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.loads(r.read().decode("utf-8", "replace")), dict(r.headers)
        except Exception as e:                                       # noqa: BLE001
            last = e
            time.sleep(3 * (i + 1))
    print("    ! 放弃 %s（%s）" % (url.split("&page=")[-1], type(last).__name__), file=sys.stderr)
    return None, {}


def crawl(tag: str, per_page: int = 100) -> list[dict]:
    # 断点续抓：先装载已有缓存（翻页不稳定，需多次运行补齐）
    items: list[dict] = []
    seen: set = set()
    if OUT.exists():
        try:
            items = json.loads(OUT.read_text(encoding="utf-8"))
            seen = {x.get("id") for x in items}
            print("  已有缓存 %d 条，继续补齐" % len(items))
        except Exception:
            items, seen = [], set()
    total = None
    page = 1
    while True:
        url = "%s?tags=%s&per_page=%d&page=%d" % (API, tag, per_page, page)
        j, hd = get(url)
        if j is None:
            page += 1
            if page > 60:
                break
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
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps(items, ensure_ascii=False, indent=1), encoding="utf-8")
        if not j or (total and len(items) >= int(total)) or page > 60:
            break
        page += 1
        time.sleep(1.2)
    return items


def norm(v):
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
        for f in norm(it.get("formats")):
            fmt[f] += 1
        for t in norm(it.get("tags")):
            tag[t] += 1
        for a in norm(it.get("apps")):
            apps[a] += 1

    print("=== 许可分布 ===")
    ok = 0
    for k, v in lic.most_common():
        name, perm = LICENSE_MAP.get(k, ("（未知码 %s）" % k, False))
        if perm:
            ok += v
        print("  %-14s %-22s %4d  %5.1f%%  %s" % (k or "(空)", name, v, v / n * 100, "可再分发" if perm else "—"))
    print("\n  **许可允许再分发**：%d / %d = %.0f%%" % (ok, n, ok / n * 100))

    print("\n=== 格式分布（前 10）===")
    for k, v in fmt.most_common(10):
        print("  %-10s %4d" % (k, v))

    print("\n=== 标签（前 30，去掉 soundfont）===")
    print("  " + " · ".join("%s(%d)" % (k, v) for k, v in tag.most_common(30) if k.lower() != "soundfont"))

    print("\n=== 目标软件（前 8）===")
    for k, v in apps.most_common(8):
        print("  %-18s %4d" % (k, v))

    # 可直接用于我们站点的（.sf2 + 可再分发 + 有下载量）
    cand = []
    for it in items:
        lk = (it.get("license") or "").strip().lower()
        name, perm = LICENSE_MAP.get(lk, ("?", False))
        if not perm:
            continue
        if "sf2" not in [f.lower() for f in norm(it.get("formats"))]:
            continue
        cand.append((it.get("download_count") or 0, it, name))
    cand.sort(key=lambda x: -x[0])
    print("\n=== 候选：.sf2 + 许可可再分发（按下载量，前 24）===")
    for dc, it, name in cand[:24]:
        print("  %-46s | %-18s | ↓%-6s | %s" % (
            (it.get("name") or "")[:46], name[:18], dc,
            ",".join(norm(it.get("tags"))[:4])[:34]))
    print("\n  候选合计 %d 个" % len(cand))
    return cand


def main(argv) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", default="soundfont")
    ap.add_argument("--report", action="store_true")
    a = ap.parse_args(argv[1:])

    if a.report:
        if not OUT.exists():
            print("没有缓存：%s" % OUT, file=sys.stderr)
            return 1
        report(json.loads(OUT.read_text(encoding="utf-8")))
        return 0

    print("抓取 musical-artifacts，tag=%s" % a.tag)
    items = crawl(a.tag)
    print("\n写入 %s" % OUT)
    report(items)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
