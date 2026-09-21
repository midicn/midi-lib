#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Lakh MIDI 多线程分段下载器（Range 请求，8 线程）

单线程实测仅 ~0.17MB/s（老学术服务器单连接限速），多连接可显著提速。
支持断点续传（按已下载的分段文件续传）。

用法：python tools/dl_lakh_multipart.py
"""
import os
import sys
import time
import threading
from pathlib import Path

URL = "http://hog.ee.columbia.edu/craffel/lmd/lmd_full.tar.gz"
OUT = Path("lmd_full.tar.gz")
PARTS_DIR = Path("_parts")
NTHREADS = 8
UA = {"User-Agent": "Mozilla/5.0 (compatible; midicn-lib/1.0)"}

import urllib.request


def head_size() -> int:
    req = urllib.request.Request(URL, method="HEAD", headers=UA)
    r = urllib.request.urlopen(req, timeout=60)
    return int(r.headers["Content-Length"])


def download_part(idx: int, start: int, end: int, total: int, progress: dict):
    p = PARTS_DIR / f"part{idx:02d}"
    have = p.stat().st_size if p.exists() else 0
    if have >= (end - start + 1):
        progress[idx] = end - start + 1
        return
    req = urllib.request.Request(URL, headers={**UA, "Range": f"bytes={start + have}-{end}"})
    try:
        r = urllib.request.urlopen(req, timeout=120)
        mode = "ab" if have else "wb"
        with p.open(mode) as f:
            while True:
                chunk = r.read(512 * 1024)
                if not chunk:
                    break
                f.write(chunk)
                progress[idx] = have + f.tell() if mode == "ab" else f.tell()
                if progress[idx] > 1024 * 1024 and progress[idx] % (5 * 1024 * 1024) < 512 * 1024:
                    pass
    except Exception as e:
        print(f"  线程{idx} 出错: {str(e)[:60]}", flush=True)


def main() -> int:
    PARTS_DIR.mkdir(exist_ok=True)
    total = head_size()
    print(f"总大小: {total/1024**3:.2f}GB · {NTHREADS} 线程分段下载", flush=True)
    seg = total // NTHREADS
    ranges = []
    for i in range(NTHREADS):
        s = i * seg
        e = (total - 1) if i == NTHREADS - 1 else ((i + 1) * seg - 1)
        ranges.append((i, s, e))
    progress = {i: 0 for i in range(NTHREADS)}
    t0 = time.time()
    threads = [threading.Thread(target=download_part, args=(i, s, e, total, progress), daemon=True)
               for i, s, e in ranges]
    for t in threads:
        t.start()
    while any(t.is_alive() for t in threads):
        time.sleep(20)
        done = sum(progress.values())
        sp = done / max(1, time.time() - t0) / 1024**2
        eta = (total - done) / max(0.1, done / max(1, time.time() - t0)) / 60
        print(f"  {done/1024**2:7.1f}MB / {total/1024**2:.0f}MB ({done/total*100:5.1f}%) · {sp:.2f}MB/s · 剩余 ~{eta:.0f}分", flush=True)
    for t in threads:
        t.join()
    print("分段完成，合并中…", flush=True)
    with OUT.open("wb") as out:
        for i, s, e in ranges:
            with (PARTS_DIR / f"part{i:02d}").open("rb") as f:
                while True:
                    chunk = f.read(8 * 1024 * 1024)
                    if not chunk:
                        break
                    out.write(chunk)
    print(f"完成: {OUT.stat().st_size/1024**3:.2f}GB · {(time.time()-t0)/60:.1f}分钟", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
