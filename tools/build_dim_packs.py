#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""维度包生成器（v1.23）· **blob 加速版**

把发布目录按 **8 个维度**切成子集包，供 `zip.midicn.com` 单独下载：
  来源 source · 风格 genre · 时期 period · 乐器 instrument ·
  授权档位 zone · 曲式 form · 地域 region · 作曲家 composer

为什么要有 blob
--------------
朴素做法是「每个维度包各自遍历它的曲目、逐个 `z.write(路径)`」——8 个维度 × 13.4 万曲
= **107 万次零散文件打开**。在 Windows（Defender 实时扫描 + 小文件目录项开销）下实测
降到约 **67 文件/秒**，全量要 4 小时以上，不可接受。

本版改为：
  ① 先把全库 MIDI **顺序拼成一个 `_blob.bin`**（每个文件只读一次，13.4 万次）；
  ② 各维度包用 `mmap` 从 blob 按字节范围取数据、`writestr` 进 zip —— **零额外文件打开**。
把 4 小时压到约半小时。

产出
  release/packs/<dim>/<slug>.zip        每包：子集 MIDI + 子集 catalog.json + LICENSE.md + README.txt
  release/packs/packs-manifest.json     包清单（供 zip 站生成索引；也提交到数据仓 meta/）
  release/packs/_blob.bin / _blob.json  中间缓存（`--clean-blob` 可删）

关键约定
  · **子集 catalog 用精简六字段**（id/t/c/cn/z/l/f）——用全字段时 aria 单包会多 ~13 MB（N2）
  · **zip 顶层带 `midicn-lib-<ver>/` 前缀**，解压不散落
  · 每包内附 `LICENSE.md` 与 `README.txt`，**可独立分发**

用法
  python tools/build_dim_packs.py                  # 生成（自动建/复用 blob）
  python tools/build_dim_packs.py --verify         # 生成后校验条数/前缀/文件数自洽
  python tools/build_dim_packs.py --only source    # 只生成某维度（调试）
  python tools/build_dim_packs.py --rebuild-blob   # 强制重建 blob
  python tools/build_dim_packs.py --clean-blob     # 只删 blob 缓存
"""
from __future__ import annotations

import argparse
import hashlib
import json
import mmap
import re
import sys
import time
import zipfile
from collections import defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _version() -> str:
    """从 `build_release.py` 读版本号（**单源**，避免发新版时多处漏改）。

    `build_release.py` 是发布链的起点，其 `VERSION` 是唯一真源；
    `pack_release.py` 也是这么读的 —— 这里保持同一口径。
    """
    src = (ROOT / "tools" / "build_release.py").read_text(encoding="utf-8")
    m = re.search(r'^VERSION\s*=\s*"([^"]+)"', src, re.M)
    if not m:
        raise SystemExit("[err] 在 tools/build_release.py 里找不到 VERSION")
    return "v" + m.group(1).lstrip("v")


VERSION = _version()
REL = ROOT.parent / "output" / f"midicn-lib-{VERSION}"
OUT = ROOT.parent / "output" / "packs"
BLOB = OUT / "_blob.bin"
BLOB_IDX = OUT / "_blob.json"
TODAY = date.today().isoformat()

# 维度定义：(键, catalog 字段, top-N（0=全量）, 兜底桶名)
DIMS = [
    ("source",     "src",    0,   None),
    ("genre",      "g",      0,   "unknown"),
    ("period",     "p",      0,   "unknown"),
    ("instrument", "i",      0,   "unknown"),
    ("zone",       "z",      0,   "unknown"),
    ("form",       "form",   30,  "unknown"),
    ("region",     "r",      40,  "unknown"),
    ("composer",   "c",      300, "traditional"),
]
SLIM = ("id", "t", "c", "cn", "z", "l", "f")


try:                                    # 仅用于把中文键转成 ASCII 文件名
    from pypinyin import lazy_pinyin as _lazy_pinyin
except ImportError:                      # pragma: no cover
    _lazy_pinyin = None


def _ascii_ize(s: str) -> str:
    """把任意字符串转成 ASCII（CJK 走拼音，其余非 ASCII 丢弃）。

    为什么必须 ASCII：实测 GitHub 的上传端点对**非 ASCII 文件名**不稳定
    （`region-德国.zip` 等 36 个包反复 504/422，实际都没传上去）。
    文件名 ASCII 化后 URL、下载器、解压工具全兼容；**中文显示名保留在
    manifest 的 `key` 字段里**，前端照常显示中文。
    """
    if _lazy_pinyin is None:
        # ⚠️ **必须硬失败**：缺 pypinyin 时非 ASCII 会被整段丢弃，
        #    所有中文键会塌缩成同一个 `unknown.zip` → **静默丢包**。
        if any(ord(ch) >= 128 for ch in s):
            raise RuntimeError(
                f"键 {s!r} 含非 ASCII，但缺少 pypinyin，无法安全生成 ASCII 文件名。\n"
                "  请用带 pypinyin 的解释器运行（本机："
                "C:/Users/chenhua/.workbuddy/binaries/python/envs/default/Scripts/python.exe），\n"
                "  否则会有多个包同名而互相覆盖。"
            )
        return s
    out = []
    for ch in s:
        if ord(ch) < 128:
            out.append(ch)
        else:
            out.append("".join(_lazy_pinyin(ch)))
    return "".join(out)


def slug(s: str) -> str:
    """文件名安全化：**ASCII 化** + 去掉路径/保留字符。

    ⚠️ 不要用 `/` 替换以外的处理去动 CJK——要整段转拼音，否则文件名里残留中文。
    """
    s = _ascii_ize(str(s or "").strip())
    s = s.replace("/", "-").replace("\\", "-")
    s = re.sub(r"[\s]+", "-", s)
    s = re.sub(r'[:*?"<>|]', "", s)
    s = re.sub(r"-{2,}", "-", s).strip("-").lower()
    return re.sub(r"[^0-9a-z\-]+", "-", s).strip("-") or "unknown"


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


def build_blob(tracks: list[dict], force: bool) -> dict:
    """构建 blob（`{rel_path: [offset, length, date_time]}` + `_blob.bin`）。

    **两种来源，优先前者**：
      ① **已打好的用途包 zip**（`main/piano-special/study` 三个顺序大文件）——
         读 3 个文件即可拿到全库，快得多；
      ② 逐个读发布目录里的 MIDI 文件（13.4 万次零散 open，慢，仅作兜底）。
    实测：① 约 2 分钟，② 约 30 分钟（Windows 杀毒 + 小文件目录项开销）。
    """
    if BLOB.exists() and BLOB_IDX.exists() and not force:
        idx = json.loads(BLOB_IDX.read_text(encoding="utf-8"))
        if idx.get("count") == len(tracks):
            print(f"[blob] 复用已有 blob（{BLOB.stat().st_size/1e9:.2f} GB · "
                  f"{idx['count']:,} 文件）")
            return idx["files"]
        print("[blob] 缓存与当前曲目数不符，重建")

    top = f"midicn-lib-{VERSION}"
    zips = [ROOT.parent / "output" / f"midicn-lib-{VERSION}-{p}.zip"
            for p in ("main", "piano-special", "study")]
    zips = [z for z in zips if z.exists()]

    files: dict[str, list] = {}
    t0 = time.time()

    if zips:
        print(f"[blob] 从 {len(zips)} 个用途包 zip 顺序构建（快路径）…", flush=True)
        with BLOB.open("wb") as out:
            off = 0
            total_members = 0
            for zp in zips:
                print(f"    {zp.name}  {zp.stat().st_size/1e6:.0f} MB", flush=True)
                with zipfile.ZipFile(zp) as zf:
                    for zi in sorted(zf.infolist(), key=lambda x: x.header_offset):
                        if not zi.filename.endswith(".mid"):
                            continue
                        rel = zi.filename[len(top) + 1:] if zi.filename.startswith(top + "/") \
                            else zi.filename
                        data = zf.read(zi)
                        out.write(data)
                        files[rel] = [off, len(data), list(zi.date_time)]
                        off += len(data)
                        total_members += 1
                        if total_members % 40000 == 0:
                            print(f"      … {total_members:,} · {off/1e9:.2f} GB · "
                                  f"{time.time()-t0:.0f}s", flush=True)
        print(f"[blob] 快路径完成 {BLOB.stat().st_size/1e9:.2f} GB · {len(files):,} 文件 · "
              f"耗时 {time.time()-t0:.0f}s")
    else:
        print(f"[blob] 未找到用途包 zip，回退逐个读文件（{len(tracks):,} 次，较慢）…", flush=True)
        order = sorted((t.get("f") or "", t) for t in tracks if t.get("f"))
        with BLOB.open("wb") as fh:
            off = 0
            for i, (rel, t) in enumerate(order, 1):
                src = REL / rel
                if not src.exists():
                    continue
                data = src.read_bytes()
                fh.write(data)
                st = src.stat()
                tm = time.localtime(st.st_mtime)
                files[rel] = [off, len(data), [tm.tm_year, tm.tm_mon, tm.tm_mday,
                                               tm.tm_hour, tm.tm_min, tm.tm_sec]]
                off += len(data)
                if i % 20000 == 0:
                    print(f"    … {i:,}/{len(order):,} · {off/1e9:.2f} GB · "
                          f"{time.time()-t0:.0f}s", flush=True)
        print(f"[blob] 完成 {BLOB.stat().st_size/1e9:.2f} GB · {len(files):,} 文件 · "
              f"耗时 {time.time()-t0:.0f}s")

    BLOB_IDX.write_text(
        json.dumps({"count": len(tracks), "files": files}, ensure_ascii=False,
                   separators=(",", ":")), encoding="utf-8")
    return files


def write_pack_members(z: zipfile.ZipFile, top: str, items: list[dict], tidx: dict,
                       mm, dim: str, k: str, lic: str) -> int:
    """写一包的全部成员：子集 catalog + LICENSE + README + 全部 MIDI（从 blob 取）。"""
    when = (2026, 9, 23, 0, 0, 0)
    slim = [{kk: t.get(kk) for kk in SLIM} for t in items]
    z.writestr(zipfile.ZipInfo(f"{top}/meta/catalog.json", date_time=when),
               json.dumps({"version": VERSION, "dim": dim, "key": k,
                           "count": len(items), "tracks": slim},
                          ensure_ascii=False, separators=(",", ":")))
    z.writestr(zipfile.ZipInfo(f"{top}/LICENSE.md", date_time=when), lic)
    z.writestr(zipfile.ZipInfo(f"{top}/README.txt", date_time=when), (
        f"midicn-lib {VERSION} · 维度包（{dim} = {k}）\n"
        f"曲目 {len(items):,} 首 · 生成于 {TODAY}\n\n"
        f"目录：{top}/{{分类}}/{{id}}.mid\n"
        f"清单：{top}/meta/catalog.json（子集，字段 id/t/c/cn/z/l/f）\n\n"
        f"许可：逐曲以 catalog 的 l（许可）与 z（档位）字段为准。\n"
        f"  C1 main          可商用（CC BY / CC BY-SA / CC0 / 公有领域）\n"
        f"  C2 piano-special 仅非商用（CC BY-NC-SA 4.0）\n"
        f"  C3 study         仅研究/学习（TRADITIONAL-STUDY · Lakh 过滤子集）\n"
        f"署名：midicn-lib（github.com/midicn/midi-library）+ 对应上游来源。\n"
        f"条款全文见包内 LICENSE.md 与 https://lib.midicn.com/licenses.html\n"))

    ordered = []
    for t in items:
        rel = t.get("f") or ""
        e = tidx.get(rel)
        if e:
            ordered.append((e[0], rel, e))
    ordered.sort(key=lambda x: x[0])          # 按 blob 偏移升序 → 顺序访问
    n = 0
    for _o, rel, (offset, length, dt) in ordered:
        zi = zipfile.ZipInfo(f"{top}/{rel}", date_time=tuple(dt))
        zi.compress_type = zipfile.ZIP_DEFLATED
        zi.external_attr = 0o644 << 16
        z.writestr(zi, mm[offset:offset + length])
        n += 1
    return n


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--only", default=None)
    ap.add_argument("--rebuild-blob", action="store_true")
    ap.add_argument("--clean-blob", action="store_true")
    args = ap.parse_args(argv[1:])

    if args.clean_blob:
        for p in (BLOB, BLOB_IDX):
            if p.exists():
                p.unlink(); print(f"  × 已删 {p.name}")
        return 0

    catf = REL / "meta" / "catalog.json"
    if not catf.exists():
        print(f"[err] 未找到 {catf}：请先跑 tools/build_release.py", file=sys.stderr)
        return 1

    t0 = time.time()
    cat = json.loads(catf.read_text(encoding="utf-8"))
    tracks = cat["tracks"]
    print(f"[packs] catalog {len(tracks):,} 首 · 版本 {cat.get('version')}", flush=True)

    OUT.mkdir(parents=True, exist_ok=True)
    tidx = build_blob(tracks, args.rebuild_blob)
    lic = read_license()
    top = f"midicn-lib-{VERSION}"

    dims = [d for d in DIMS if not args.only or d[0] == args.only]
    manifest_packs: list[dict] = []

    with BLOB.open("rb") as bf:
        mm = mmap.mmap(bf.fileno(), 0, access=mmap.ACCESS_READ)
        try:
            for dim, field, topn, fallback in dims:
                buckets: dict[str, list[dict]] = defaultdict(list)
                for t in tracks:
                    buckets[key_of(t, dim, field)].append(t)

                keys = sorted(buckets, key=lambda k: -len(buckets[k]))
                if topn:
                    keep, drop = set(keys[:topn]), keys[topn:]
                    if drop:
                        rest = [t for k in drop for t in buckets[k]
                                if fallback is None or k != fallback]
                        for k in drop:
                            del buckets[k]
                        (buckets[fallback] if fallback else buckets["other-unknown"]).extend(rest)

                d_out = OUT / dim
                d_out.mkdir(parents=True, exist_ok=True)
                print(f"\n[{dim}] {len(buckets)} 包（top-N={topn or '全量'}）", flush=True)
                tdim = time.time()
                done = 0
                for k, items in sorted(buckets.items(), key=lambda kv: -len(kv[1])):
                    zname = f"midicn-lib-{VERSION}-{dim}-{slug(k)}.zip"
                    zpath = d_out / zname
                    if zpath.exists():
                        zpath.unlink()
                    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED, compresslevel=1) as z:
                        n_files = write_pack_members(z, top, items, tidx, mm, dim, k, lic)

                    h = hashlib.md5()
                    with zpath.open("rb") as fh:
                        for chunk in iter(lambda: fh.read(1 << 20), b""):
                            h.update(chunk)
                    manifest_packs.append({
                        "dim": dim, "key": k, "count": len(items), "files": n_files,
                        "bytes": zpath.stat().st_size, "zip": zname, "md5": h.hexdigest(),
                        "srcs": sorted({str(t.get("id", "")).split("-")[0] for t in items})[-6:],
                    })
                    done += 1
                    if done % 25 == 0:
                        print(f"    … {done}/{len(buckets)} · {time.time()-tdim:.0f}s", flush=True)
                print(f"  [{dim}] 完成 {done} 包 · {time.time()-tdim:.0f}s", flush=True)
        finally:
            mm.close()

    manifest = {
        "version": VERSION, "generated": TODAY, "total_tracks": len(tracks),
        "release_tag": f"{VERSION}-packs",
        "base_url": f"https://github.com/midicn/midi-library/releases/download/{VERSION}-packs/",
        "packs": manifest_packs,
    }
    mf = OUT / "packs-manifest.json"
    mf.write_text(json.dumps(manifest, ensure_ascii=False, separators=(",", ":")),
                  encoding="utf-8")

    total_b = sum(p["bytes"] for p in manifest_packs)
    print(f"\n[packs] {len(manifest_packs)} 包 · {total_b/1e9:.2f} GB · 总耗时 {time.time()-t0:.0f}s")
    print(f"[packs] 清单 → {mf.relative_to(ROOT)}")
    if manifest_packs:
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
                if not all(n.startswith(f"{top}/") for n in names):
                    print(f"  ✗ 前缀错误 {p['zip']}"); bad += 1
                mids = sum(1 for n in names if n.endswith(".mid"))
                if mids != p["files"]:
                    print(f"  ✗ 文件数不符 {p['zip']}: {mids} != {p['files']}"); bad += 1
                need = {f"{top}/meta/catalog.json", f"{top}/LICENSE.md"}
                if not need.issubset(set(names)):
                    print(f"  ✗ 缺 catalog/LICENSE {p['zip']}"); bad += 1
        print(f"[verify] {len(manifest_packs)} 包 · 异常 {bad} → "
              f"{'✓ 全部自洽' if bad == 0 else '✗ 有异常'}")
        return 0 if bad == 0 else 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
