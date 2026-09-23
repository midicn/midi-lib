#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""OpenGameArt.org MIDI 抓取器

遍历搜索页（keys=midi）→ 逐个 asset 页 → 抓 .mid/.midi 文件 + 许可标签 → sources/oga/
许可：逐 asset（CC0 / CC-BY / CC-BY-SA 等）→ 记录在 state，入库时按 asset 标注。

用法：
  python tools/fetch_oga.py [--max-pages 25]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "sources" / "oga"
STATE = ROOT / "tools" / "state" / "oga-progress.json"
UA = {"User-Agent": "Mozilla/5.0 (compatible; midicn-lib/0.1)"}
HREF = re.compile(r'href="([^"]+)"')
MID_LINK = re.compile(r'href="(https?://[^"]+\.midi?)"', re.I)
LICENSE = re.compile(r'(CC0|CC-BY-SA\s*[\d.]*|CC-BY\s*[\d.]*|GPL\s*[\d.]*|OGA-BY\s*[\d.]*)', re.I)


def get(url: str) -> str:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=40) as r:
        return r.read().decode("utf-8", "replace")


def load_state() -> dict:
    if STATE.exists():
        return json.loads(STATE.read_text(encoding="utf-8"))
    return {"assets": [], "files": {}, "failed": []}


def save_state(st: dict) -> None:
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(st, ensure_ascii=False), encoding="utf-8")


def collect_assets(max_pages: int) -> list[str]:
    assets = set()
    for page in range(0, max_pages):
        url = f"https://opengameart.org/art-search?keys=midi&page={page}"
        try:
            h = get(url)
        except Exception as e:
            print(f"[warn] page {page}: {e}", flush=True)
            continue
        found = {m for m in re.findall(r'href="(/content/[^"?#]+)"', h)}
        if not found:
            print(f"[collect] page {page} 无结果，停止", flush=True)
            break
        assets |= found
        print(f"[collect] page {page}: +{len(found)} (累计 {len(assets)})", flush=True)
        time.sleep(0.3)
    return sorted(assets)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-pages", type=int, default=25)
    ap.add_argument("--collect-only", action="store_true")
    args = ap.parse_args(argv[1:])

    st = load_state()
    if not st["assets"]:
        st["assets"] = collect_assets(args.max_pages)
        save_state(st)
    print(f"[assets] {len(st['assets'])}", flush=True)
    if args.collect_only:
        return 0

    DEST.mkdir(parents=True, exist_ok=True)
    n_new = 0
    for i, a in enumerate(st["assets"], 1):
        if a in st["files"]:
            continue
        url = "https://opengameart.org" + a
        try:
            h = get(url)
        except Exception as e:
            st["failed"].append({"asset": a, "err": str(e)[:100]})
            continue
        mids = MID_LINK.findall(h)
        lic = LICENSE.findall(h)
        lic = lic[0][0] if lic else "UNKNOWN"
        for mu in mids:
            name = mu.rsplit("/", 1)[-1]
            target = DEST / a.strip("/").replace("/", "_") / name
            if target.exists():
                continue
            try:
                req = urllib.request.Request(mu, headers=UA)
                with urllib.request.urlopen(req, timeout=60) as r:
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(r.read())
                st["files"][f"{a}/{name}"] = {"url": mu, "license": lic, "asset": a}
                n_new += 1
            except Exception as e:
                st["failed"].append({"file": mu, "err": str(e)[:100]})
            time.sleep(0.2)
        if i % 25 == 0:
            save_state(st)
            print(f"  ... {i}/{len(st['assets'])} assets, {n_new} new files", flush=True)
    save_state(st)
    print(f"[done] {len(st['files'])} files total ({n_new} new) -> {DEST}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
