#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""用 IMSLP 作品目录反查 aria 曲目标题

IMSLP 作品页标题 → 目录编号映射，例：
  "Aufforderung zum Tanze, Op.65 (Weber, Carl Maria von)"     → (Op., 65)  → Aufforderung zum Tanze
  "Goldberg Variations, BWV 988 (Bach, Johann Sebastian)"     → (BWV, 988) → Goldberg Variations
  "Piano Sonata No.11, K.331 (Mozart, Wolfgang Amadeus)"      → (K., 331)  → Piano Sonata No.11
aria 的 opus 字段即该作曲家体系下的编号（Bach=BWV / Mozart=K. / Schubert=D. / Haydn=Hob. / 多数=Op.）。

用法：python tools/enrich_aria_titles.py [--dry-run]
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARIA = ROOT / "midi_db/tracks/aria.jsonl"
IMSLP = ROOT / "sources/imslp"
BACKUP = ROOT / "midi_db/tracks_backup"

PREFIX_ORDER = {
    "bach": ["BWV"], "mozart": ["K."], "scarlatti": ["K.", "L."], "schubert": ["D."],
    "haydn": ["HOBXVI", "HOB"], "liszt": ["S."], "chopin": ["Op.", "B.", "KK"],
    "rachmaninoff": ["Op.", "TN"], "handel": ["HWV"], "vivaldi": ["RV"], "giuliani": ["Op."], "sor": ["Op."], "carcassi": ["Op."],
    "carulli": ["Op."], "aguado": ["Op."], "coste": ["Op."], "mertz": ["Op."], "tarrega": ["Op."],
    "bizet": ["WD"], "albeniz": ["Op.", "T."], "granados": ["Op.", "D."],
}
# 严格体系（只用指定前缀，不做任意前缀兜底）——防止把钢琴奏鸣曲错标成弦乐四重奏
STRICT = {"bach", "mozart", "scarlatti", "schubert", "haydn", "liszt", "handel", "vivaldi"}
DEFAULT_ORDER = ["Op.", "WoO", "Anh.", "H."]
# 同一作曲家的不同拼写 → 规范 slug（用已抓到的目录）
ALIAS_SLUG = {
    "skriabin": "scriabin", "rakhmaninov": "rachmaninoff", "glier": "gliere",
    "liadov": "lyadov", "gedike": "goedicke", "gretchaninoff": "grechaninov",
    "gretchaninow": "grechaninov", "moshkovsky": "moszkowski", "loeschhorn": "loschhorn",
    "burgmueller": "burgmuller", "meraux": "mereaux", "cherny": "czerny",
    "saint-saens": "saint-saens", "sains-saens": "saint-saens",
}
NUM_RE = re.compile(
    r"\b(BWV|Op\.?|K\.|KV\.?|D\.|Hob\.|S\.|J\.|HWV|RV|WoO|Anh\.|L\.|B\.|Sz\.|BB|TN|KK|H\.|Wq|G\.|EH|WD|T\.)\s*"
    r"([0-9]+(?:[:/][0-9]+)?)",
    re.I)


HOB_RE = re.compile(r"\bHob\.\s*([IVXab]+)\s*[:/.]\s*(\d+)", re.I)


def parse_work(title: str):
    """标题 → (名字, [(前缀, 主体编号)])"""
    name = re.split(r",\s*(?:BWV|Op\.?|K\.|KV|D\.|Hob\.|S\.|J\.|HWV|RV|WoO|Anh\.|L\.|B\.|Sz\.|BB|TN|KK|H\.|Wq|G\.|EH|WD|T\.)\s*[0-9]", title)[0]
    name = name.strip().rstrip(",").strip()
    pairs = []
    for m in NUM_RE.finditer(title):
        pre = m.group(1).rstrip(".").upper() if m.group(1).upper() != "OP" else "OP"
        num = m.group(2)
        pairs.append((pre, num))
    # Hob. 体系（Haydn）：Hob.XVI:20 → 钢琴奏鸣曲；Hob. 后的罗马数字是类别
    for m in HOB_RE.finditer(title):
        roman, num = m.group(1).upper(), m.group(2)
        pairs.append(("HOB", f"{roman}:{num}"))
        if roman.startswith("XVI"):
            pairs.append(("HOBXVI", num))
    return name or None, pairs


def norm_pre(pre: str):
    p = pre.upper().rstrip(".")
    if p.startswith("HOB"):
        return p
    return {"OP": "OP", "KV": "K", "K": "K"}.get(p, p)


def build_maps():
    """slug → {(前缀, 编号): 标题}"""
    maps = {}
    for f in sorted(IMSLP.glob("*.json")):
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        slug = d.get("slug")
        works = d.get("works") or []
        m = defaultdict(list)
        for t in works:
            name, pairs = parse_work(t)
            if not name:
                continue
            for pre, num in pairs:
                m[(norm_pre(pre), num)].append(name)
        if m:
            maps[slug] = m
    return maps


def pick(m, slug, num, piece):
    order = [norm_pre(p.rstrip(".")) for p in PREFIX_ORDER.get(slug, DEFAULT_ORDER)]
    for pre in order:
        for key in [(pre, str(num)), (pre, f"{num}")]:
            if key in m:
                cands = m[key]
                if piece:
                    for c in cands:
                        if re.search(rf"No\.?\s*{piece}\b", c) or re.search(rf"/\s*{piece}\b", c):
                            return c
                return cands[0]
    if slug in STRICT:
        return None
    # 兜底：任意前缀
    for (pre, n), cands in m.items():
        if n == str(num):
            return cands[0]
    return None


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--source", default="aria", help="要处理的源（aria / lakh / 逗号分隔）")
    args = ap.parse_args(argv[1:])

    maps = build_maps()
    print(f"[imslp] 载入 {len(maps)} 位作曲家的作品目录索引")
    srcs = [x.strip() for x in args.source.split(",") if x.strip()]
    for src in srcs:
        run_one(src, maps, args.dry_run)
    return 0


def run_one(src: str, maps: dict, dry_run: bool):
    fp = ROOT / f"midi_db/tracks/{src}.jsonl"
    if not fp.exists():
        print(f"[{src}] 文件不存在，跳过")
        return
    rows = [json.loads(l) for l in fp.open(encoding="utf-8")]
    changed = 0
    matched_body = 0
    samples = []
    out = []
    for r in rows:
        ch = None
        slug = r.get("composer_slug") or ""
        m = maps.get(slug) or maps.get(ALIAS_SLUG.get(slug, ""))
        op = r.get("opus")
        if m and op:
            if str(op).strip() in ("0", ""):
                op = None
            title = pick(m, slug, op, r.get("no")) if op else None
            if title:
                cur = str(r.get("title") or "").strip()
                low = cur.lower()
                # 通用：空标题 / 纯编号式
                weak = (not cur
                        or re.match(r"^[0-9a-z]{4,12}$", low)
                        or re.match(r"^(bwv|k|kv|op|d|hob)\.?\s*\d+$", low)
                        or re.match(r"^[a-z ,.]+\s*(bwv|k|kv|op|d|hob)\.?\s*\d*$", low))
                # lakh：只替换 ID 式/纯编号式（描述性文件名本身有信息，覆盖可能退化）
                if src == "lakh":
                    weak = (not cur
                            or re.match(r"^[0-9a-z]{4,12}$", low)
                            or re.match(r"^(bwv|k|kv|op|d|hob)\.?\s*\d+$", low)
                            or re.match(r"^[a-z ,.]+\s*(bwv|k|kv|op|d|hob)\.?\s*0*$", low)
                            or re.match(r"^[a-z]+\s*\d{1,4}$", low))
                if weak:
                    ch = {"title": title}
        if ch:
            changed += 1
            matched_body += 1
            if len(samples) < 12:
                samples.append((r["id"], slug, r.get("opus"), ch["title"]))
            r2 = dict(r); r2.update(ch); out.append(r2)
        else:
            out.append(r)
    print()
    print(f"=== {src} 标题反查报告 ===")
    print(f"  曲目 {len(rows):,} · 可补标题 {changed:,}")
    for s in samples:
        print(f"    {s[0]}  {s[1]:14s} Op.{s[2]:<5} → {s[3][:52]}")
    if dry_run:
        print("\n[dry-run] 未写回")
        return
    ts = time.strftime("%Y%m%d-%H%M%S")
    bdir = BACKUP / f"pre-imslp-{src}-{ts}"
    bdir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(fp, bdir / fp.name)
    with fp.open("w", encoding="utf-8", newline="\n") as fh:
        for r in out:
            fh.write(json.dumps(r, ensure_ascii=False, separators=(",", ":")) + "\n")
    print(f"\n[backup] {bdir}\n[write] {src}.jsonl 已更新")


if __name__ == "__main__":
    sys.exit(main(sys.argv))
