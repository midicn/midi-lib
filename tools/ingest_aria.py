#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""D2 · ariamidi 接入器（源 id = aria）

读取 sources/ariamidi/{metadata.json, data/aa..dz/*.mid}，产出：
  1) midi_db/tracks/aria.jsonl         —— 32,522 行规范化元数据（schema v1，19 字段）
  2) midi_db/stats/aria-ingest-report.md —— 行数断言 + 字段覆盖率报告
  3) （--copy-files）data/midi/aria/b*/  —— 规范化 MIDI 副本（<源>-<桶>-<序号>.mid）

用法：
  python tools/ingest_aria.py                # 仅元数据（秒级）
  python tools/ingest_aria.py --copy-files   # 追加规范化文件复制
  python tools/ingest_aria.py --verify       # 仅校验已有产出
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]          # lib.midicn.com/
SRC = ROOT / "sources" / "ariamidi"
META_PATH = SRC / "metadata.json"
DATA_DIR = SRC / "data"
OUT_JSONL = ROOT / "midi_db" / "tracks" / "aria.jsonl"
OUT_REPORT = ROOT / "midi_db" / "stats" / "aria-ingest-report.md"
DST_DIR = ROOT.parent / "data" / "midi" / "aria"

SOURCE_ID = "aria"
LICENSE = "CC-BY-NC-SA-4.0"
ZONE = "piano-special"
BUCKET_SIZE = 1000
SEG_RE = re.compile(r"^(\d+)_(\d+)\.mid$")


def scan_midi() -> dict[int, Path]:
    """磁盘全量扫描（README 明示：桶边界有 ±20 漂移，禁止按 id//2000 推算）。"""
    mapping: dict[int, Path] = {}
    dupes = []
    for p in DATA_DIR.rglob("*.mid"):
        m = SEG_RE.match(p.name)
        if not m:
            continue
        fid = int(m.group(1))
        if fid in mapping:
            dupes.append((fid, mapping[fid], p))
        mapping[fid] = p
    if dupes:
        print(f"[warn] {len(dupes)} duplicate file_ids encountered (first 3: {dupes[:3]})")
    return mapping


def norm_rel(p: Path) -> str:
    return p.relative_to(ROOT).as_posix()


def canonical_name(seq_idx: int) -> str:
    """按源内排序序号连续分桶（千首一桶），与 schema.md §5 一致。"""
    bucket = seq_idx // BUCKET_SIZE
    seq = seq_idx % BUCKET_SIZE
    return f"{SOURCE_ID}-b{bucket:03d}-{seq:05d}.mid"


def canonical_rel(seq_idx: int) -> str:
    bucket = seq_idx // BUCKET_SIZE
    return f"data/midi/{SOURCE_ID}/b{bucket:03d}/{canonical_name(seq_idx)}"


def build_rows(meta: dict, mapping: dict[int, Path]) -> list[dict]:
    rows = []
    for seq_idx, fid_str in enumerate(sorted(meta.keys(), key=lambda s: int(s))):
        fid = int(fid_str)
        entry = meta[fid_str]
        md = entry.get("metadata", {}) or {}
        scores = entry.get("audio_scores", {}) or {}
        seg_scores = list(scores.values())
        src = mapping.get(fid)
        rows.append({
            "id": f"{SOURCE_ID}-{fid:06d}",
            "source": SOURCE_ID,
            "src_path": norm_rel(src) if src else None,
            "title": None,
            "composer_slug": md.get("composer"),
            "composer_name": (md.get("composer") or "").strip().title() or None,
            "opus": md.get("opus"),
            "no": md.get("piece_number"),
            "genre": md.get("genre"),
            "form": md.get("form"),
            "key": md.get("key_signature"),
            "period": md.get("music_period"),
            "region": None,
            "instrument": "piano",
            "license": LICENSE,
            "zone": ZONE,
            "midi": {
                "file": canonical_rel(seq_idx),
                "duration_sec": None,
                "note_count": None,
                "tracks_count": None,
                "bpm": None,
            },
            "fingerprint": None,
            "extra": {
                "audio_score": round(max(seg_scores), 4) if seg_scores else None,
                "segment": 0,
                "source_file_id": fid,
                "name_source": "slug",
            },
        })
    return rows


FIELDS = ["composer_slug", "composer_name", "opus", "no", "genre", "form", "key",
          "period", "region", "instrument", "license", "zone"]


def coverage(rows: list[dict]) -> dict[str, float]:
    cov = {}
    for f in FIELDS:
        n = sum(1 for r in rows if r.get(f) not in (None, ""))
        cov[f] = n / len(rows) * 100 if rows else 0.0
    return cov


def write_report(rows: list[dict], meta: dict, mapping: dict[int, Path]) -> None:
    cov = coverage(rows)
    comp = Counter(r["composer_slug"] for r in rows if r["composer_slug"])
    periods = Counter(r["period"] for r in rows if r["period"])
    genres = Counter(r["genre"] for r in rows if r["genre"])
    missing_files = [r["id"] for r in rows if not r["src_path"]]
    lines = [
        "# aria 接入报告（D2）",
        "",
        f"- 生成时间：{__import__('datetime').datetime.now().isoformat(timespec='seconds')}",
        f"- 源 id：`{SOURCE_ID}` · zone：`{ZONE}` · license：`{LICENSE}`",
        "",
        "## 行数断言",
        "",
        "| 项 | 数量 |",
        "|---|---:|",
        f"| metadata.json 条数 | {len(meta):,} |",
        f"| 磁盘 .mid 文件数（扫描到） | {len(mapping):,} |",
        f"| JSONL 行数 | {len(rows):,} |",
        f"| 未匹配到文件的记录 | {len(missing_files):,} |",
        "",
        "## 字段覆盖率",
        "",
        "| 字段 | 覆盖率 |",
        "|---|---:|",
    ]
    for f in FIELDS:
        lines.append(f"| `{f}` | {cov[f]:.1f}% |")
    lines += [
        "",
        f"- 作曲家数：**{len(comp):,}**",
        f"- 时期分布：{', '.join(f'{k} {v:,}' for k, v in periods.most_common(8))}",
        f"- 流派分布：{', '.join(f'{k} {v:,}' for k, v in genres.most_common(8))}",
        "",
        "## 结论",
        "",
        "行数三方一致" + ("✅" if len(rows) == len(meta) == len(mapping) else "❌（需排查）"),
        "",
    ]
    if missing_files[:10]:
        lines.append("缺失文件示例：" + ", ".join(missing_files[:10]))
    OUT_REPORT.parent.mkdir(parents=True, exist_ok=True)
    OUT_REPORT.write_text("\n".join(lines), encoding="utf-8")


def do_copy(rows: list[dict]) -> None:
    total = len(rows)
    copied = skipped = failed = 0
    for i, r in enumerate(rows, 1):
        src = ROOT / r["src_path"] if r["src_path"] else None
        dst = ROOT / r["midi"]["file"]
        if not src or not src.exists():
            failed += 1
            continue
        if dst.exists() and dst.stat().st_size == src.stat().st_size:
            skipped += 1
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        try:
            shutil.copy2(src, dst)
            copied += 1
        except OSError as e:
            failed += 1
            print(f"[error] {src} -> {dst}: {e}")
        if i % 5000 == 0:
            print(f"  ... {i:,}/{total:,} (copied={copied:,} skipped={skipped:,} failed={failed})")
    print(f"[copy] done: copied={copied:,} skipped={skipped:,} failed={failed:,}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--copy-files", action="store_true")
    ap.add_argument("--verify", action="store_true")
    args = ap.parse_args()

    if not META_PATH.exists():
        print(f"[fatal] metadata.json not found: {META_PATH}")
        return 1
    meta = json.loads(META_PATH.read_text(encoding="utf-8"))
    mapping = scan_midi()
    rows = build_rows(meta, mapping)

    OUT_JSONL.parent.mkdir(parents=True, exist_ok=True)
    with OUT_JSONL.open("w", encoding="utf-8", newline="\n") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False, separators=(",", ":")) + "\n")
    write_report(rows, meta, mapping)

    ok = len(rows) == len(meta) == len(mapping)
    print(f"[ingest] metadata={len(meta):,} files={len(mapping):,} rows={len(rows):,} -> {'OK' if ok else 'MISMATCH'}")
    print(f"[ingest] jsonl: {OUT_JSONL}")
    print(f"[ingest] report: {OUT_REPORT}")

    if args.copy_files:
        do_copy(rows)
    if args.verify:
        n_lines = sum(1 for _ in OUT_JSONL.open(encoding="utf-8"))
        print(f"[verify] jsonl lines = {n_lines:,}")
    return 0 if ok else 2


if __name__ == "__main__":
    sys.exit(main())
