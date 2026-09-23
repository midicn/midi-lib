#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""维度包生成器（v1.23 新增）。

把发布目录按 **8 个维度**切成子集包，供 `zip.midicn.com` 单独下载：
  来源 source · 风格 genre · 时期 period · 乐器 instrument ·
  授权档位 zone · 曲式 form · 地域 region · 作曲家 composer

产出
  release/packs/<dim>/<slug>.zip      每包：子集 MIDI + 子集 catalog.json + LICENSE.md
  release/packs/packs-manifest.json   包清单（供 zip 站生成索引；也提交到数据仓 meta/）

关键设计
  · **子集 catalog 用精简六字段**（id/t/c/cn/z/l/f）——用完整 28 字段的话 aria 单包就 ~13 MB（N2）
  · **zip 顶层带 `midicn-lib-<ver>/` 前缀**，解压不会散落一地（与主包一致）
  · 每个包内附 `LICENSE.md` 与 `README.txt`，**可独立分发**
  · 长尾维度（曲式/地域/作曲家）用 top-N，其余归入 `unknown`，避免几百个小包

用法
  python tools/build_dim_packs.py                 # 生成
  python tools/build_dim_packs.py --verify        # 生成后校验条数/前缀/文件数自洽
  python tools/build_dim_packs.py --only source   # 只生成某维度（调试用）
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
import time
import zipfile
from collections import defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "v1.23"
REL = ROOT / "release" / f"midicn-lib-{VERSION}"
OUT = ROOT / "release" / "packs"
TODAY = date.today().isoformat()

# 维度定义：(键, catalog 字段, top-N（0=全量）, 兜底桶名)
DIMS = [
    ("source",     "src",    0,   None),        # 由 id 前缀得出
    ("genre",      "g",      0,   "unknown"),
    ("period",     "p",      0,   "unknown"),
    ("instrument", "i",      0,   "unknown"),
    ("zone",       "z",      0,   "unknown"),
    ("form",       "form",   30,  "unknown"),
    ("region",     "r",      40,  "unknown"),
    ("composer",   "c",      300, "traditional"),  # 作曲家：traditional 归入兜底桶
]

# 子集 catalog 的精简字段（N2）
SLIM = ("id", "t", "c", "cn", "z", "l", "f")


def slug(s: str) -> str:
    """文件名安全化：**不替换 `/`**（Windows 路径坑），改写成一个短横。"""
    s = str(s or "").strip().replace("/", "-").replace("\\", "-")
    s = re.sub(r"[\s]+", "-", s)
    s = re.sub(r'[:*?"<>|]', "", s)
    s = re.sub(r"-{2,}", "-", s).strip("-")
    return s or "unknown"


def key_of(t: dict, dim: str, field: str) -> str:
    if dim == "source":
        return str(t.get("id", "")).split("-")[0] or "unknown"
    v = t.get(field)
    return str(v) if v not in (None, "") else "unknown"


def read_license() -> str:
    for c in (ROOT / "docs" / "LICENSE.md", ROOT / "LICENSE.md"):
        if c.exists():
            return c.read_text(encoding="utf-8")
    return "(LICENSE.md 未找到)"


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--only", default=None, help="只生成指定维度（调试用）")
    args = ap.parse_args(argv[1:])

    catf = REL / "meta" / "catalog.json"
    if not catf.exists():
        print(f"[err] 未找到 {catf}：请先跑 tools/build_release.py", file=sys.stderr)
        return 1

    t0 = time.time()
    cat = json.loads(catf.read_text(encoding="utf-8"))
    tracks = cat["tracks"]
    print(f"[packs] catalog {len(tracks):,} 首 · 版本 {cat.get('version')}", flush=True)

    lic = read_license()
    OUT.mkdir(parents=True, exist_ok=True)

    dims = [d for d in DIMS if not args.only or d[0] == args.only]
    manifest_packs: list[dict] = []

    for dim, field, topn, fallback in dims:
        # ① 分组
        buckets: dict[str, list[dict]] = defaultdict(list)
        for t in tracks:
            buckets[key_of(t, dim, field)].append(t)

        # ② top-N 截断，其余归入兜底桶
        keys = sorted(buckets, key=lambda k: -len(buckets[k]))
        if topn:
            keep, drop = set(keys[:topn]), keys[topn:]
            if drop:
                # `traditional` 之类的兜底桶不进 unknown（它本身就是"无具名"）
                rest = [t for k in drop for t in buckets[k]
                        if fallback is None or k != fallback]
                for k in drop:
                    del buckets[k]
                if rest and fallback:
                    buckets[fallback].extend(rest)
                elif rest:
                    buckets["other-unknown"].extend(rest)

        d_out = OUT / dim
        d_out.mkdir(parents=True, exist_ok=True)
        print(f"\n[{dim}] {len(buckets)} 包（top-N={topn or '全量'}）", flush=True)

        for k, items in sorted(buckets.items(), key=lambda kv: -len(kv[1])):
            zname = f"midicn-lib-{VERSION}-{dim}-{slug(k)}.zip"
            zpath = d_out / zname
            if zpath.exists():
                zpath.unlink()

            n_files = 0
            with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
                # 子集 catalog（精简字段，N2）
                slim = [{kk: t.get(kk) for kk in SLIM} for t in items]
                z.writestr(f"midicn-lib-{VERSION}/meta/catalog.json",
                           json.dumps({"version": VERSION, "dim": dim, "key": k,
                                       "count": len(items), "tracks": slim},
                                      ensure_ascii=False, separators=(",", ":")))
                z.writestr(f"midicn-lib-{VERSION}/LICENSE.md", lic)
                z.writestr(f"midicn-lib-{VERSION}/README.txt", (
                    f"midicn-lib {VERSION} · 维度包（{dim} = {k}）\n"
                    f"曲目 {len(items):,} 首 · 生成于 {TODAY}\n\n"
                    f"目录：midicn-lib-{VERSION}/{{分类}}/{{id}}.mid\n"
                    f"清单：midicn-lib-{VERSION}/meta/catalog.json（子集，字段 id/t/c/cn/z/l/f）\n\n"
                    f"许可：逐曲以 catalog 的 l（许可）与 z（档位）字段为准。\n"
                    f"  C1 main        可商用（CC BY / CC BY-SA / CC0 / 公有领域）\n"
                    f"  C2 piano-special 仅非商用（CC BY-NC-SA 4.0）\n"
                    f"  C3 study       仅研究/学习（TRADITIONAL-STUDY · Lakh 过滤子集）\n"
                    f"署名：midicn-lib（github.com/midicn/midi-lib）+ 对应上游来源。\n"
                    f"条款全文见包内 LICENSE.md 与 https://lib.midicn.com/licenses.html\n"))
                # MIDI 实体（保持 {分类}/{id}.mid 布局）
                for t in items:
                    f = t.get("f") or ""
                    src = REL / f
                    if not src.exists():
                        continue
                    z.write(src, f"midicn-lib-{VERSION}/{f}")
                    n_files += 1

            packs = len(items)
            if n_files != packs:
                print(f"    ⚠ {zname}: catalog {packs} 首但只写入 {n_files} 个文件", flush=True)

            md5 = hashlib.md5(zpath.read_bytes()).hexdigest()
            srcs = sorted({str(t.get("id", "")).split("-")[0] for t in items})
            manifest_packs.append({
                "dim": dim, "key": k, "count": packs, "files": n_files,
                "bytes": zpath.stat().st_size, "zip": zname, "md5": md5,
                "srcs": srcs[-6:],          # 只留少量来源名做展示
            })
            if len(manifest_packs) % 25 == 0:
                print(f"    … 已出 {len(manifest_packs)} 包", flush=True)

    manifest = {
        "version": VERSION,
        "generated": TODAY,
        "total_tracks": len(tracks),
        "release_tag": f"{VERSION}-packs",
        "base_url": f"https://github.com/midicn/midi-lib/releases/download/{VERSION}-packs/",
        "packs": manifest_packs,
    }
    mf = OUT / "packs-manifest.json"
    mf.write_text(json.dumps(manifest, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")

    total_b = sum(p["bytes"] for p in manifest_packs)
    print(f"\n[packs] {len(manifest_packs)} 包 · {total_b/1e9:.2f} GB · 耗时 {time.time()-t0:.0f}s")
    print(f"[packs] 清单 → {mf.relative_to(ROOT)}")
    mx = max(manifest_packs, key=lambda p: p["bytes"])
    print(f"[packs] 最大包 {mx['zip']} · {mx['bytes']/1e6:.1f} MB · {mx['count']:,} 首")

    if args.verify:
        bad = 0
        for p in manifest_packs:
            z = OUT / p["dim"] / p["zip"]
            if not z.exists():
                print(f"  ✗ 缺包 {z}"); bad += 1; continue
            with zipfile.ZipFile(z) as zf:
                names = zf.namelist()
                if not all(n.startswith(f"midicn-lib-{VERSION}/") for n in names):
                    print(f"  ✗ 前缀错误 {p['zip']}"); bad += 1
                mids = sum(1 for n in names if n.endswith(".mid"))
                if mids != p["files"]:
                    print(f"  ✗ 文件数不符 {p['zip']}: {mids} != {p['files']}"); bad += 1
                need = {f"midicn-lib-{VERSION}/meta/catalog.json", f"midicn-lib-{VERSION}/LICENSE.md"}
                if not need.issubset(set(names)):
                    print(f"  ✗ 缺 catalog/LICENSE {p['zip']}"); bad += 1
        print(f"[verify] {len(manifest_packs)} 包 · 异常 {bad} → {'✓ 全部自洽' if bad==0 else '✗ 有异常'}")
        return 0 if bad == 0 else 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
