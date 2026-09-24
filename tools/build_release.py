#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""D9 发布构建器：生成发布目录树 + 索引 + 校验

规则（已拍板）：
  - piano-special 公开；research 不发布（仅本地）；pending 不发布
  - broken / duplicate_of 排除
  - 文件统一 {id}.mid 命名
  - 大分类：源 → main/<category>/ 或 piano-special/

产出：
  release/midicn-lib-v1.0/
    ├── meta/catalog.json + index-*.json × 4 + MD5SUMS.txt
    ├── main/<category>/*.mid
    └── piano-special/*.mid
  （文档由 docs/ 提供，另行放入）

用法：python tools/build_release.py [--dry-run]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
import time
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACKS = ROOT / "midi_db" / "tracks"
REL = ROOT / "release" / "midicn-lib-v1.23"
VERSION = "1.23"

CATEGORY = {
    "thesession": ("main", "folk-ireland"),
    "norbeck": ("main", "folk-ireland"),
    "essen": ("main", "folk-world"),
    "nottingham": ("main", "folk-british"),
    "abcmisc": ("main", "klezmer-balkan"),
    "mutopia": ("main", "classical-open"),
    "openscore": ("main", "classical-open"),
    "m21": ("main", "classical-open"),
    "musicnet": ("main", "classical-open"),
    "oga": ("main", "game"),
    "groove": ("main", "drum"),
    "aria": ("piano-special", "piano"),
    "wikifonia": ("main", "folk-world"),
    "lakh": ("study", "classical-traditional"),
    "maestro": ("piano-special", "maestro"),
    "emopia": ("piano-special", "emopia"),
    "chinafolk": ("study", "folk-china"),
    "giantmidi": ("main", "piano-performance"),
    "cyberhymnal": ("main", "hymn"),
    "atepp": ("main", "piano-performance"),
    "pdmx": ("main", "classical-open"),
}

# 许可标识规范化：上游各源的写法不统一（空格 / 简写），发布前统一为规范标识。
# 这些映射均为「同义改写」，不改变任何许可等级或使用条件。
LICENSE_CANON = {
    "CC0": "CC0-1.0",
    "CC-BY 3.0": "CC-BY-3.0",
    "CC-BY 4.0": "CC-BY-4.0",
    "CC-BY-SA 3.0": "CC-BY-SA-3.0",
    "CC-BY-SA 4.0": "CC-BY-SA-4.0",
    "CC-BY-NC 3.0": "CC-BY-NC-3.0",
    "CC-BY-NC 4.0": "CC-BY-NC-4.0",
    "CC-BY-NC-SA 3.0": "CC-BY-NC-SA-3.0",
    "CC-BY-NC-SA 4.0": "CC-BY-NC-SA-4.0",
    "GPL 2.0": "GPL-2.0",
    "GPL 3.0": "GPL-3.0",
}


def canon_license(v: str | None) -> str | None:
    """把上游写法统一为规范许可标识（未登记的写法原样保留，便于审计发现）。"""
    if not v:
        return v
    return LICENSE_CANON.get(v.strip(), v.strip())


# ── 地域名清洗：上游 Essen / Norbeck 等源残留 LaTeX 转义（{\"aa} / \"o 等） ──
_LATEX = (
    ("{\\aa}", "å"), ("{\\AA}", "Å"), ("{\\o}", "ø"), ("{\\O}", "Ø"),
    ("\\\"o", "ö"), ("\\\"a", "ä"), ("\\\"u", "ü"),
    ("\\\"O", "Ö"), ("\\\"A", "Ä"), ("\\\"U", "Ü"),
    ("\\'e", "é"), ("\\'a", "á"), ("\\`e", "è"), ("\\ss", "ß"),
)


def clean_region(v: str | None) -> str | None:
    """Sm{\\aa}land → Småland，H\\"alsingland → Hälsingland。"""
    if not v:
        return v
    s = str(v)
    for a, b in _LATEX:
        s = s.replace(a, b)
    s = s.replace("{", "").replace("}", "").replace("\\", "")
    s = re.sub(r"\s+", " ", s).strip()
    return s or v


SKIP_ZONES = {"pending"}
# musedata：CCARH 许可明文禁止任何分发（含非商业），永久排除
# chinafolk：以 TRADITIONAL-STUDY 发布（传统民歌旋律 + 转录底本受版权保护 → 仅研究/学习，须署名）
SKIP_SOURCES = {"musedata"}

# 按来源覆盖许可标识：上游未声明时，用我们核定的标识（并在 docs / 站点逐条说明依据）
SOURCE_LICENSE = {"chinafolk": "TRADITIONAL-STUDY"}
# 按来源覆盖分区：chinafolk 在 midi_db 里仍标 pending，发布时归入 study（C3 研究/学习）；
# ATEPP 数据源声明 CC BY 4.0（可商用），jsonl 里的 piano-special 会被误判为 C2 非商用 → 覆盖为 main
SOURCE_ZONE = {"chinafolk": "study", "atepp": "main"}


def norm_key(s: str) -> str:
    """归组键规范化：折叠变音符号 → 只留各语种字母数字 → 小写。

    ⚠️ **不能用 `[^0-9a-z]` 白名单**——那会把中文/西里尔等全部删掉，
    导致上万首中国民歌的标题规范化后变成空串、被并进同一个 wk 组
    （实测 `traditional|` 分组吃进 10,444 首）。
    改用 `str.isalnum()`（按 Unicode 判定，保留 CJK 等），只剔除标点与空白。

    ATEPP 同一作品的标题还会因变音符号写法不同而分裂，例如
      「12 Études, Op. 8: No. 10 in D-Flat Major」 vs 「12 Etudes, Op. 8: No. 10 in D-Flat Major」
    故先做 NFKD 折叠。
    """
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    return "".join(c for c in s if c.isalnum()).lower()


def work_key(r: dict) -> str:
    """作品归组键 `wk`（N1）：`composer_slug | opus | no | 规范化标题`。

    用途：详情页「本曲其他演奏版」区块按 `wk` 聚合，ATEPP 的同一作品多演奏版
    因此得以互相发现。

    纳入 `opus`/`no` 是为了**避免泛标题过度合并**——只按「作曲家+标题」时，
    aria 里 111 首不同的「Piano Sonata」会被并成一组；带上作品号后可分开。
    标题缺失或规范化后为空时（如 aria 的纯转录曲目）**用 id 兜底**，
    否则所有无标题曲目会被错误地并成一个大组。
    """
    c = (r.get("composer_slug") or "unknown").strip().lower()
    k = norm_key(r.get("title"))
    if not k:
        return f"{c}|#{r.get('id')}"
    o = norm_key(str(r.get("opus"))) if r.get("opus") is not None else ""
    n = norm_key(str(r.get("no"))) if r.get("no") is not None else ""
    return f"{c}|{o}|{n}|{k}"


def build(args) -> int:
    t0 = time.time()
    catalog = []
    by_comp = defaultdict(list)
    by_region = defaultdict(list)
    by_period = defaultdict(list)
    by_source = defaultdict(list)
    md5_lines = []
    copied = skipped = dupes = 0
    stats = Counter()
    seen_md5 = set()

    for f in sorted(TRACKS.glob("*.jsonl")):
        for line in f.open(encoding="utf-8"):
            r = json.loads(line)
            src = r["source"]
            zone = SOURCE_ZONE.get(src, r.get("zone"))
            if src in SKIP_SOURCES or zone in SKIP_ZONES:
                skipped += 1
                continue
            if r.get("verify_flag") == "broken" or r.get("duplicate_of"):
                skipped += 1
                continue
            pack, cat = CATEGORY.get(src, ("main", "misc"))
            rel = f"{pack}/{cat}/{r['id']}.mid"
            # 新源（ATEPP / PDMX）未规范化到 data/midi，midi.file 为空 → 回退 src_path
            mf = (r.get("midi") or {}).get("file")
            if not mf:
                sp = (r.get("src_path") or "").replace("\\", "/")
                if sp and (ROOT / sp).exists():
                    mf = sp
            if not mf:
                skipped += 1
                continue
            srcf = ROOT / mf
            if not srcf.exists():
                skipped += 1
                continue
            # 同源自重复（指纹缺失时的兜底）：按文件内容 MD5 去重
            md5 = None
            if not args.dry_run:
                md5 = hashlib.md5(srcf.read_bytes()).hexdigest()
                if (src, md5) in seen_md5:
                    dupes += 1
                    continue
                seen_md5.add((src, md5))
            catalog.append({
                "id": r["id"], "t": r.get("title"), "c": r.get("composer_slug"),
                "cn": r.get("composer_name"), "g": r.get("genre"), "p": r.get("period"),
                "r": clean_region(r.get("region")), "i": r.get("instrument"), "z": zone,
                "l": canon_license(SOURCE_LICENSE.get(src, r.get("license"))),
                "v": r.get("verify_flag"), "f": rel,
                "opus": r.get("opus"), "no": r.get("no"),
                "form": r.get("form"), "ctry": r.get("country"), "diff": r.get("diff"),
                "yr": r.get("yr") or (r.get("extra") or {}).get("tune_year") or (r.get("extra") or {}).get("death") or (r.get("extra") or {}).get("birth"),
                "du": (r.get("midi") or {}).get("duration_sec"),
                "nn": (r.get("midi") or {}).get("note_count"),
                # ── v1.23 新增（gen_shards.py 的 KEEP 已同步扩这 5 个键）────────
                "cnzh": r.get("cn_zh"),              # 作曲家中文名（全量 28%）
                "vt": r.get("version_type"),         # score / performance（ATEPP·PDMX）
                "perf": r.get("performer"),          # 演奏者（ATEPP）
                "alb": r.get("album"),               # 专辑/录音出处（ATEPP）
                "wk": work_key(r),                   # 作品归组键（N1，详情页「其他演奏版」）
            })
            by_comp[r.get("composer_slug") or "unknown"].append(r["id"])
            if r.get("region"):
                by_region[r["region"]].append(r["id"])
            if r.get("period"):
                by_period[r["period"]].append(r["id"])
            by_source[src].append(r["id"])

            if not args.dry_run:
                dest = REL / rel
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(srcf, dest)
                md5 = hashlib.md5(dest.read_bytes()).hexdigest()
                md5_lines.append(f"{md5}  {rel}")
            copied += 1
            stats[f"{pack}/{cat}"] += 1

    REL.mkdir(parents=True, exist_ok=True)
    meta = REL / "meta"
    meta.mkdir(parents=True, exist_ok=True)

    if not args.dry_run:
        (meta / "catalog.json").write_text(
            json.dumps({"version": VERSION, "count": len(catalog), "tracks": catalog},
                       ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        for name, idx in (("by-composer", by_comp), ("by-region", by_region),
                          ("by-period", by_period), ("by-source", by_source)):
            (meta / f"index-{name}.json").write_text(
                json.dumps({k: sorted(v) for k, v in sorted(idx.items())},
                           ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        (meta / "MD5SUMS.txt").write_text("\n".join(md5_lines), encoding="utf-8")
        verjson = ROOT.parent / "lib/library" / "meta" / "version.json"
        if verjson.exists():
            (meta / "version.json").write_text(verjson.read_text(encoding="utf-8"), encoding="utf-8")

    print(f"[build] 复制 {copied:,} · 跳过 {skipped:,} · 分类 {dict(stats.most_common())}")
    print(f"[build] 耗时 {time.time()-t0:.0f}s · 输出 {REL}")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    sys.exit(build(ap.parse_args(sys.argv[1:])))
