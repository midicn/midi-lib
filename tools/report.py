#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""全库统计报告生成器 → midi_db/stats/library-report.md

用法：python tools/report.py
"""
from __future__ import annotations

import json
from collections import Counter
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACKS = ROOT / "midi_db" / "tracks"
OUT = ROOT / "midi_db" / "stats" / "library-report.md"


def main() -> int:
    per_source, all_rows = [], []
    for f in sorted(TRACKS.glob("*.jsonl")):
        rows = [json.loads(l) for l in f.open(encoding="utf-8")]
        ok = sum(1 for r in rows if (ROOT / r["midi"]["file"]).exists())
        per_source.append({"source": f.stem, "n": len(rows), "ok": ok,
                           "zone": rows[0]["zone"] if rows else "?",
                           "license": rows[0]["license"] if rows else "?"})
        all_rows.extend(rows)

    total = len(all_rows)
    zones = Counter(r["zone"] for r in all_rows)
    licenses = Counter(r["license"] for r in all_rows)
    genres = Counter(r["genre"] for r in all_rows if r["genre"])
    forms = Counter(r["form"] for r in all_rows if r["form"])
    regions = Counter(r["region"] for r in all_rows if r["region"])
    periods = Counter(r["period"] for r in all_rows if r["period"])
    composers = Counter(r["composer_slug"] for r in all_rows if r["composer_slug"])
    with_title = sum(1 for r in all_rows if r["title"])

    cov_fields = ["composer_slug", "composer_name", "title", "opus", "genre",
                  "form", "key", "period", "region", "instrument", "license", "zone"]
    cov = {}
    for fld in cov_fields:
        cov[fld] = sum(1 for r in all_rows if r.get(fld) not in (None, "")) / total * 100

    lines = [
        "# midicn-lib 全库统计报告",
        "",
        f"> 生成：{datetime.now().isoformat(timespec='seconds')} · 源数 **{len(per_source)}** · 曲目 **{total:,}**",
        "",
        "## 一、分源汇总",
        "",
        "| 源 | 曲目数 | 落盘 | 分区 | 许可 |",
        "|---|---:|---|---|---|",
    ]
    for s in sorted(per_source, key=lambda x: -x["n"]):
        flag = "✓" if s["ok"] == s["n"] else f"⚠ {s['ok']}"
        lines.append(f"| `{s['source']}` | {s['n']:,} | {flag} | {s['zone']} | {s['license']} |")
    lines += [f"| **合计** | **{total:,}** | | | |", ""]

    lines += ["## 二、分区与许可", "", "| 分区 | 曲目数 | 占比 |", "|---|---:|---:|"]
    for z, n in zones.most_common():
        lines.append(f"| {z} | {n:,} | {n/total*100:.1f}% |")
    lines += ["", "| 许可 | 曲目数 |", "|---|---:|"]
    for l_, n in licenses.most_common(15):
        lines.append(f"| `{l_}` | {n:,} |")

    lines += ["", "## 三、字段覆盖率", "", "| 字段 | 覆盖率 |", "|---|---:|"]
    for fld, v in cov.items():
        lines.append(f"| `{fld}` | {v:.1f}% |")

    lines += ["", "## 四、内容分布", "",
              f"- **作曲家**：{len(composers):,} 位（Top 15："
              + "、".join(f"{k}({v:,})" for k, v in composers.most_common(15)) + "）",
              f"- **流派**：{len(genres)} 类（" + "、".join(f"{k} {v:,}" for k, v in genres.most_common(12)) + "）",
              f"- **曲式/类型**：{len(forms)} 类（" + "、".join(f"{k} {v:,}" for k, v in forms.most_common(12)) + "）",
              f"- **地域**：{len(regions)} 个（" + "、".join(f"{k} {v:,}" for k, v in regions.most_common(12)) + "）",
              f"- **时期**：{len(periods)} 个（" + "、".join(f"{k} {v:,}" for k, v in periods.most_common(8)) + "）",
              f"- **带曲名**：{with_title:,} / {total:,}（{with_title/total*100:.1f}%）",
              ""]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"[report] {total:,} tracks · {len(per_source)} sources -> {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
