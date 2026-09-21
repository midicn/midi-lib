#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Mutopia Project 抓取器（D3 · 批次 1）

递归遍历 http://www.mutopiaproject.org/ftp/ （作曲家/作品号/作品名/*.mid），
下载全部 .mid 到 sources/mutopia/ 保留原目录结构。
状态（已完成 URL 集合）写入 tools/state/mutopia-progress.json —— 可中断、可续跑。

用法：
  python tools/fetch_mutopia.py            # 增量续跑（跳过已完成）
  python tools/fetch_mutopia.py --limit 200  # 本次最多下载 200 个文件（开机跑批配额）
  python tools/fetch_mutopia.py --crawl-only # 只遍历目录建索引，不下载
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
BASE = "https://www.mutopiaproject.org/ftp/"
DEST = ROOT / "sources" / "mutopia"
STATE = ROOT / "tools" / "state" / "mutopia-progress.json"
UA = {"User-Agent": "Mozilla/5.0 (compatible; midicn-lib/0.1; +https://lib.midicn.com)"}
HREF = re.compile(r'href="([^"]+)"')


def load_state() -> dict:
    if STATE.exists():
        return json.loads(STATE.read_text(encoding="utf-8"))
    return {"done": [], "failed": [], "dirs_walked": [], "midi_urls": []}


def save_state(st: dict) -> None:
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(st, ensure_ascii=False), encoding="utf-8")


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def list_dir(url: str) -> list[str]:
    html = fetch(url).decode("utf-8", "replace")
    out = []
    for h in HREF.findall(html):
        if h.startswith("?") or h in ("/", "/ftp/") or h.startswith("http"):
            continue
        out.append(h)
    return out


def rel_depth(full: str) -> int:
    """BASE 之后的相对目录深度：'Composer/'=1, 'Composer/Work/'=2, 'Composer/Work/Piece/'=3"""
    rel = full[len(BASE):]
    return rel.count("/")


def crawl(st: dict) -> None:
    """递归建立 MIDI URL 索引（幂等：只走未走过的目录）。"""
    frontier = [BASE]
    seen_dirs = set(st.get("dirs_walked", []))
    midi = set(st.get("midi_urls", []))
    while frontier:
        d = frontier.pop(0)
        if d in seen_dirs:
            continue
        try:
            entries = list_dir(d)
        except Exception as e:
            print(f"[crawl][warn] {d}: {e}")
            continue
        seen_dirs.add(d)
        for e in entries:
            full = d + e
            if e.endswith(".mid"):
                midi.add(full)
            elif e.endswith("/") and rel_depth(full) <= 3:
                frontier.append(full)
        if len(seen_dirs) % 50 == 0:
            st["dirs_walked"] = sorted(seen_dirs)
            st["midi_urls"] = sorted(midi)
            save_state(st)
            print(f"[crawl] dirs={len(seen_dirs)} midi_found={len(midi)}")
        time.sleep(0.1)
    st["dirs_walked"] = sorted(seen_dirs)
    st["midi_urls"] = sorted(midi)
    save_state(st)
    print(f"[crawl] done: dirs={len(seen_dirs)} midi={len(midi)}")


def download(st: dict, limit: int | None) -> None:
    urls = st.get("midi_urls", [])
    done = set(st.get("done", []))
    todo = [u for u in urls if u not in done]
    if limit:
        todo = todo[:limit]
    print(f"[download] total={len(urls)} done={len(done)} todo={len(todo)}")
    n = 0
    for u in todo:
        rel = u[len(BASE):]
        target = DEST / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        try:
            data = fetch(u)
            target.write_bytes(data)
            done.add(u)
            n += 1
            if n % 50 == 0:
                st["done"] = sorted(done)
                save_state(st)
                print(f"  ... {n}/{len(todo)}  ({rel})")
        except Exception as e:
            st.setdefault("failed", []).append({"url": u, "err": str(e)})
            print(f"[download][err] {u}: {e}")
        time.sleep(0.15)
    st["done"] = sorted(done)
    save_state(st)
    print(f"[download] finished this run: +{n} files -> {DEST}")


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--crawl-only", action="store_true")
    args = ap.parse_args(argv[1:])

    st = load_state()
    if not st.get("midi_urls"):
        crawl(st)
    if not args.crawl_only:
        download(st, args.limit)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
