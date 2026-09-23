#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Release 打包：把 build_release.py 产物打成 4 个 zip（meta/main/piano-special/study）

用法：
    python tools/pack_release.py            # 打当前 VERSION 的 4 包
    python tools/pack_release.py --verify   # 打完试解压 meta 抽查

关键约定（三犯坑）：zip 内部必须带顶层目录 midicn-lib-v<VER>/ 前缀——
lib 站 deploy.yml 解压后执行 `mv site/midicn-lib-*/* site/` 依赖该前缀。
"""
from __future__ import annotations
import argparse, hashlib, sys, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REL = ROOT / "release"
PACKS = ("meta", "main", "piano-special", "study")


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser(description="打 release zip（带顶层前缀）")
    ap.add_argument("--verify", action="store_true", help="打完试解压 meta 抽查")
    args = ap.parse_args()

    # 从 build_release.py 读版本号（单源）
    src = (ROOT / "tools" / "build_release.py").read_text(encoding="utf-8")
    import re
    m = re.search(r'VERSION\s*=\s*"([\d.]+)"', src)
    assert m, "build_release.py 里找不到 VERSION"
    ver = m.group(1)
    vdir = REL / f"midicn-lib-v{ver}"
    assert vdir.exists(), f"{vdir} 不存在——先跑 build_release.py"
    top = f"midicn-lib-v{ver}"          # zip 内顶层前缀（deploy 依赖）

    for pack in PACKS:
        src_dir = vdir / pack
        assert src_dir.exists(), f"{src_dir} 不存在"
        out = REL / f"midicn-lib-v{ver}-{pack}.zip"
        if out.exists():
            print(f"[skip] {out.name} 已存在（先删再重打）")
            continue
        n = 0
        with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
            for p in sorted(src_dir.rglob("*")):
                if p.is_file():
                    z.write(p, f"{top}/{pack}/{p.relative_to(src_dir).as_posix()}")
                    n += 1
        size = out.stat().st_size
        print(f"[ok] {out.name}  {n:,} 文件  {size / 2**20:,.1f} MiB  sha256={sha256(out)[:16]}…")

    if args.verify:
        import tempfile, json, os
        with tempfile.TemporaryDirectory() as td:
            with zipfile.ZipFile(REL / f"midicn-lib-v{ver}-meta.zip") as z:
                names = z.namelist()
                assert any(n.startswith(top + "/") for n in names), "顶层前缀缺失！"
                z.extractall(td)
            cat = Path(td) / top / "meta" / "catalog.json"
            d = json.loads(cat.read_text(encoding="utf-8"))
            nf = sum(1 for t in d["tracks"] if t.get("form"))
            print(f"[verify] catalog: count={d['count']:,} · form 有值={nf:,} ({nf/d['count']*100:.1f}%)")
            idx = Path(td) / top / "meta"
            print(f"[verify] meta 目录: {[p.name for p in idx.iterdir()]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
