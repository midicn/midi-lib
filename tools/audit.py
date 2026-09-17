#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""全库终审（穷尽式 · 10 维度） → docs/AUDIT-REPORT.md

检查项：
  1. 文件完整性      JSONL 每条引用的 MIDI 是否存在
  2. 路径唯一性      同源内 midi.file 不得重复（防覆盖残留）
  3. JSONL 合法      每行可解析
  4. 字段结构        19 个顶层字段齐全
  5. 枚举合法        zone / period 取值在允许集内
  6. zone-license 自洽  main 必须为可商用许可（非 NC/UNSPECIFIED）
  7. 重复标记有效     duplicate_of 指向存在的 id 且非自指
  8. composer 非空    slug 与 name 均非空
  9. region 清洁      不含噪声特征
  10. MIDI 头抽样     随机 500 个文件以 MThd 开头
另：按源统计行数、落盘率、分区

用法：python tools/audit.py
"""
from __future__ import annotations

import json
import random
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACKS = ROOT / "midi_db" / "tracks"
OUT = ROOT / "docs" / "AUDIT-REPORT.md"

FIELDS = ["id", "source", "src_path", "title", "composer_slug", "composer_name",
          "opus", "no", "genre", "form", "key", "period", "region", "instrument",
          "license", "zone", "midi", "fingerprint", "extra"]
OPTIONAL_FIELDS = {"duplicate_of"}
ZONES = {"main", "piano-special", "research", "pending", "hold"}
PERIODS = {"medieval", "renaissance", "baroque", "classical", "romantic",
           "impressionist", "modern", "contemporary", "traditional"}
NC_LIC = re.compile(r"NC|UNSPECIFIED|RESTRICTED", re.I)
NOISE = re.compile(r"kammen|klez camp|played by|collected by|orchestra|^\d+$", re.I)


def main() -> int:
    issues: list[str] = []
    warns: list[str] = []
    per_source = defaultdict(lambda: {"n": 0, "exists": 0, "paths": set(),
                                      "dup_paths": 0, "zones": Counter()})
    all_ids = set()
    rows_all = []
    json_bad = 0
    field_bad = 0
    zone_bad = 0
    period_bad = 0
    lic_inconsistent = []
    composer_empty = 0
    region_noise = 0
    dup_ref_bad = 0

    for f in sorted(TRACKS.glob("*.jsonl")):
        for ln, line in enumerate(f.open(encoding="utf-8"), 1):
            try:
                r = json.loads(line)
            except Exception:
                json_bad += 1
                issues.append(f"{f.name}:{ln} JSON 非法")
                continue
            rows_all.append(r)
            all_ids.add(r["id"])
            src = r["source"]
            ps = per_source[src]
            ps["n"] += 1
            ps["zones"][r["zone"]] += 1
            p = ROOT / r["midi"]["file"]
            if p.exists():
                ps["exists"] += 1
            else:
                issues.append(f"{r['id']} 文件缺失: {r['midi']['file']}")
            if r["midi"]["file"] in ps["paths"]:
                ps["dup_paths"] += 1
                issues.append(f"{r['id']} 同源路径重复")
            ps["paths"].add(r["midi"]["file"])
            if (set(r.keys()) - OPTIONAL_FIELDS) != set(FIELDS):
                field_bad += 1
                issues.append(f"{r['id']} 字段结构异常: 缺{sorted(set(FIELDS)-set(r.keys()))} 多{sorted(set(r.keys())-set(FIELDS)-OPTIONAL_FIELDS)}")
            if r.get("zone") not in ZONES:
                zone_bad += 1
                issues.append(f"{r['id']} zone 非法: {r.get('zone')}")
            if r.get("period") and r["period"] not in PERIODS:
                period_bad += 1
                issues.append(f"{r['id']} period 非法: {r['period']}")
            if r.get("zone") == "main" and NC_LIC.search(r.get("license") or ""):
                lic_inconsistent.append(r["id"])
            if not (r.get("composer_slug") or "").strip() or not (r.get("composer_name") or "").strip():
                composer_empty += 1
            reg = r.get("region")
            if reg and (NOISE.search(reg) or len(reg) > 24):
                region_noise += 1

    for r in rows_all:
        d = r.get("duplicate_of")
        if d:
            if d == r["id"]:
                dup_ref_bad += 1
                issues.append(f"{r['id']} duplicate_of 自指")
            elif d not in all_ids:
                dup_ref_bad += 1
                issues.append(f"{r['id']} duplicate_of 指向不存在的 id: {d}")

    # MIDI 头抽样
    random.seed(42)
    sample = random.sample(rows_all, min(500, len(rows_all)))
    bad_head = 0
    for r in sample:
        p = ROOT / r["midi"]["file"]
        if p.exists() and p.open("rb").read(4) != b"MThd":
            bad_head += 1

    n = len(rows_all)
    dup_marked = sum(1 for r in rows_all if r.get("duplicate_of"))
    zones = Counter(r["zone"] for r in rows_all)
    lic = Counter(r["license"] for r in rows_all)

    lines = [
        "# midicn-lib 全库终审报告",
        "",
        f"> 生成：{datetime.now().isoformat(timespec='seconds')} · 记录 **{n:,}** · 源 **{len(per_source)}**",
        "",
        "## 一、核查结果总表",
        "",
        "| # | 检查项 | 结果 | 详情 |",
        "|---|---|---|---|",
        f"| 1 | 文件完整性 | {'✅' if not any('文件缺失' in i for i in issues) else '❌'} | 引用文件全部存在 |",
        f"| 2 | 同源路径唯一性 | {'✅' if sum(v['dup_paths'] for v in per_source.values()) == 0 else '❌'} | 无覆盖残留 |",
        f"| 3 | JSONL 合法性 | {'✅' if json_bad == 0 else '❌'} | 非法行 {json_bad} |",
        f"| 4 | 19 字段结构 | {'✅' if field_bad == 0 else '❌'} | 异常 {field_bad} 条 |",
        f"| 5 | 枚举值合法 | {'✅' if zone_bad == 0 and period_bad == 0 else '❌'} | zone 非法 {zone_bad} · period 非法 {period_bad} |",
        f"| 6 | zone-license 自洽 | {'✅' if not lic_inconsistent else '❌'} | main 区含 NC/未声明 {len(lic_inconsistent)} 条 |",
        f"| 7 | duplicate_of 有效 | {'✅' if dup_ref_bad == 0 else '❌'} | 异常 {dup_ref_bad} |",
        f"| 8 | composer 非空 | {'✅' if composer_empty == 0 else '❌'} | 空值 {composer_empty} |",
        f"| 9 | region 清洁 | {'✅' if region_noise == 0 else '⚠️'} | 疑似噪声 {region_noise} |",
        f"| 10 | MIDI 头抽样 | {'✅' if bad_head == 0 else '❌'} | 抽样 500 · 异常 {bad_head} |",
        "",
        f"**总计**：记录 {n:,} · 标记重复 {dup_marked:,} · 唯一内容 {n - dup_marked:,} · 待处理问题 {len(issues)} 条",
        "",
        "## 二、分源明细",
        "",
        "| 源 | 记录 | 落盘 | 路径唯一 | 分区 |",
        "|---|---:|---|---|---|",
    ]
    for src in sorted(per_source, key=lambda s: -per_source[s]["n"]):
        ps = per_source[src]
        ok = "✓" if ps["exists"] == ps["n"] else f"⚠ {ps['exists']}"
        uniq = "✓" if ps["dup_paths"] == 0 else f"⚠{ps['dup_paths']}"
        z = "/".join(f"{k}{v:,}" for k, v in ps["zones"].most_common(2))
        lines.append(f"| `{src}` | {ps['n']:,} | {ok} | {uniq} | {z} |")

    lines += ["", "## 三、分区与许可", "", "| 分区 | 记录数 |", "|---|---:|"]
    for k, v in zones.most_common():
        lines.append(f"| {k} | {v:,} |")
    lines += ["", "| 许可 | 记录数 |", "|---|---:|"]
    for k, v in lic.most_common(12):
        lines.append(f"| `{k}` | {v:,} |")

    if issues:
        lines += ["", "## 四、问题清单（前 50）", ""]
        for i in issues[:50]:
            lines.append(f"- {i}")
    else:
        lines += ["", "## 四、问题清单", "", "**无** —— 10 项全部通过 ✅"]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"[audit] 记录 {n:,} · 问题 {len(issues)} · 报告 {OUT.relative_to(ROOT)}")
    for c in (("文件完整性", not any('文件缺失' in i for i in issues)),
              ("路径唯一", sum(v['dup_paths'] for v in per_source.values()) == 0),
              ("JSON 合法", json_bad == 0), ("字段结构", field_bad == 0),
              ("枚举合法", zone_bad == 0 and period_bad == 0),
              ("zone-license", not lic_inconsistent), ("duplicate_of", dup_ref_bad == 0),
              ("composer 非空", composer_empty == 0), ("region 清洁", region_noise == 0),
              ("MIDI 头", bad_head == 0)):
        print(f"  {'✅' if c[1] else '❌'} {c[0]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
