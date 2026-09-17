#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""质量管线（幂等）：清洗 → 时期推断 → 字段补全 → 自检

**重要**：任何源重建（ingest）之后必须重跑本管线，因为重建会覆盖此前的清洗成果。
顺序固定，避免时序问题。

用法：
  python tools/quality_pipeline.py [--no-audit]
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACKS = ROOT / "midi_db" / "tracks"
PY = sys.executable

TRAD = re.compile(r"传统|traditional|民歌|trad\.|anon", re.I)


def slugify(s: str) -> str:
    s = (s or "").strip().lower()
    for a, b in (("é", "e"), ("è", "e"), ("ê", "e"), ("á", "a"), ("à", "a"), ("ö", "o"),
                 ("ü", "u"), ("ä", "a"), ("í", "i"), ("ó", "o"), ("ñ", "n"), ("ç", "c"),
                 ("š", "s"), ("ž", "z"), ("ř", "r"), ("ø", "o"), ("å", "a")):
        s = s.replace(a, b)
    s = re.sub(r"[^a-z0-9\-]", "-", s)
    return re.sub(r"-+", "-", s).strip("-")


def run(script: str) -> None:
    print(f"\n===== {script} =====", flush=True)
    r = subprocess.run([PY, str(ROOT / "tools" / script)], capture_output=True, text=True)
    for l in (r.stdout or "").splitlines():
        if "Warning" not in l and "self." not in l:
            print(l, flush=True)
    if r.returncode != 0:
        print(f"[warn] {script} 退出码 {r.returncode}: {(r.stderr or '')[:200]}", flush=True)


def fill_slug() -> int:
    """补 composer_slug（ABC 类源缺失）。"""
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    bdir = ROOT / "midi_trash" / f"pre-slug-{ts}"
    bdir.mkdir(parents=True, exist_ok=True)
    fixed = 0
    for f in sorted(TRACKS.glob("*.jsonl")):
        rows = [json.loads(l) for l in f.open(encoding="utf-8")]
        changed = False
        for r in rows:
            if not (r.get("composer_slug") or "").strip():
                name = r.get("composer_name") or ""
                r["composer_slug"] = ("traditional" if (TRAD.search(name) or not name)
                                      else (slugify(name) or "unknown"))
                r["composer_name"] = name or "Traditional"
                fixed += 1
                changed = True
        if changed:
            shutil.copy2(f, bdir / f.name)
            with f.open("w", encoding="utf-8", newline="\n") as fh:
                for r in rows:
                    fh.write(json.dumps(r, ensure_ascii=False, separators=(",", ":")) + "\n")
    print(f"[slug] 补全 {fixed:,} 条", flush=True)
    return fixed


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-audit", action="store_true")
    args = ap.parse_args(argv[1:])

    t0 = datetime.now()
    run("clean_v1.py")          # 1) 作曲家归并 + region 清洗
    run("infer_period.py")      # 2) 时期推断
    fill_slug()                 # 3) composer_slug 补全
    if not args.no_audit:
        run("audit.py")         # 4) 全库终审

    # 汇总
    rows = []
    for f in sorted(TRACKS.glob("*.jsonl")):
        rows += [json.loads(l) for l in f.open(encoding="utf-8")]
    n = len(rows)
    cov = {k: sum(1 for r in rows if r.get(k) not in (None, "")) / n * 100
           for k in ("composer_slug", "composer_name", "period", "genre",
                     "title", "form", "key", "region", "license", "zone")}
    print(f"\n===== 管线完成（{(datetime.now()-t0).seconds}s）=====", flush=True)
    print(f"记录 {n:,} · 覆盖率:", flush=True)
    for k, v in sorted(cov.items(), key=lambda x: -x[1]):
        print(f"  {k:16s} {v:5.1f}%", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
