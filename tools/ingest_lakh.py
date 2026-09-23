#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Lakh MIDI 接入器（过滤 + 入库 C3=study）

合规依据：Lakh MIDI Dataset 声明 CC-BY 4.0（允许再分发）；
但作者明言「未转录任何 MIDI、均从公开来源抓取」→ 内容层需严格过滤：
  1. 剔除所有**含版权声明**的曲目（读 MIDI 的 Copyright meta-event）
  2. 剔除**路径含流行/摇滚/游戏/影视关键词**的曲目（内容性质风险）
  3. 仅保留**明确提出为古典/传统/宗教/学术**的曲目 → 定级 C3（仅供研究/学习）

用法（须带 mido + 托管 venv）：
  python tools/ingest_lakh.py [--limit N] [--dry-run]
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import tarfile
import tempfile
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARBALL = ROOT / "sources" / "lakh" / "lmd_full.tar.gz"
OUT_JSONL = ROOT / "midi_db" / "tracks" / "lakh.jsonl"
STATE = ROOT / "tools" / "state" / "lakh-progress.json"

SOURCE_ID = "lakh"
LICENSE = "CC-BY-4.0"
ZONE = "study"          # C3 · 仅供研究/学习
BUCKET = 1000

# 保留：明确的古典/传统/宗教/学术类路径
# ⚠ 2026-09-23 修正：**不得再用 christmas|carol 当"公有领域"代理**。
#   「圣诞」≠「无版权」——LAKH 的 christmas/carol 路径混入大量 20 世纪商业音乐
#   （White Christmas / Frosty / Rudolph / Last Christmas / 各类流行圣诞歌），
#   这条规则实际放进了 356 首仍在保护期内的作品（真实侵权入口）。
#   已由 tools/exclude_lakh_modern.py 全部剔除（台账 docs/internal/lakh-review-2026-09-23.md）。
#   真正的传统颂歌另带 traditional / hymn / church 标记，仍会经这些词保留。
KEEP_PAT = re.compile(
    r"classical|klassik|baroque|renaissance|medieval|"
    r"bach|mozart|beethoven|chopin|liszt|schubert|brahms|handel|vivaldi|haydn|"
    r"hymn|church|choral|organ|sacred|gospel|"
    r"traditional|trad[_ ]|folk|celtic|irish|scottish|"
    r"etude|sonata|symphony|concerto|nocturne|prelude|fugue|waltz|mazurka",
    re.I)

# 剔除：流行/摇滚/影视/游戏/现代商业音乐
DROP_PAT = re.compile(
    r"\bpop\b|top.?40|hits|charts?|"
    r"rock|metal|punk|grunge|hard.?rock|"
    r"tv.?theme|movie|soundtrack|film|"
    r"nintendo|sega|playstation|final fantasy|zelda|mario|game|"
    r"samba|pagode|forro|mpb|axé|"
    r"rap|hip.?hop|techno|trance|house|dance|"
    r"disco|reggae|kpop|jpop|anime",
    re.I)

# ── 版权剔除：与 tools/lakh_denylist.py 同源（单一真源，勿两处各写一份）──────
# DROP 判定先于 KEEP，所以这里命中的现代作品**不会**再被 classical/hymn 等救回。
# 词表缺失时必须直接失败，而不是静默放行（否则等于悄悄放弃版权防线）。
sys.path.insert(0, str(Path(__file__).resolve().parent))
try:
    from lakh_denylist import ARTIST_RE as _MODERN_ARTIST_RE
    from lakh_denylist import LATE_COMPOSER_RE as _LATE_NAME_RE
    from lakh_denylist import MODERN_DIRS as _MODERN_DIRS
    from lakh_denylist import dir_hit as _dir_hit
    from lakh_denylist import MODERN_RE as _MODERN_WORK_RE
except Exception as _exc:  # pragma: no cover
    raise SystemExit(f"[lakh] 缺少版权词表 tools/lakh_denylist.py：{_exc}")

def _modern_dir_of(origs: list[str]) -> str | None:
    """任一原始路径的目录分量命中 MODERN_DIRS 即返回该目录名。

    lakh 的目录名携带版权身份（`BachmanTurnerOverdrive/Hey You`、`ELVIS/Blue 2`、
    `F/Fire Emblem…`、`C/Castlevania…`），是比标题更可靠的结构性信号。
    **只认具名目录**——单字母桶 c/m/f/j/C/F/J/M 实测是混合桶（含大量古典与赞美诗）。
    复用语料库里的 `dir_hit()`（扫描全部目录分量，兼容带/不带 `sources/lakh/` 前缀）。
    """
    for p in origs:
        parts = p.replace("\\", "/").split("/")[:-1]
        d = _dir_hit(parts)
        if d:
            return d
    return None


def drop_reason(origs: list[str]) -> str | None:
    """统一的路径级剔除判定：返回剔除理由，`None` 表示保留。

    **ingest 主流程与 tools/_ingest_divergence.py 共用本函数**，确保
    「冷重跑口径」与「实际入库口径」永远一致（此前两处各写一份，导致差异检查假警报）。

    四道信号，顺序即优先级：
      ① DROP_PAT              流行/摇滚/影视/游戏/舞曲关键词
      ② MODERN_RE / ARTIST_RE 现代作品名 / 艺人名（与清理器同源词表）
      ③ _modern_dir_of()      一级目录是具名艺人 / 游戏 / 商业包
      ④ _LATE_NAME_RE         卒年晚于 PD 线的作曲家人名
    ①②④ 都在三个**分隔符变体**上判定（路径写 `White-Christmas`，词表按空格写）。
    """
    joined = " | ".join(origs)
    probes = (
        joined,
        re.sub(r"[-_]+", " ", joined),
        re.sub(r"[-_\s]+", "", joined),
    )
    if any(DROP_PAT.search(s) for s in probes):
        return "流行/影视/游戏"
    if any(rx.search(s) for rx in (_MODERN_WORK_RE, _MODERN_ARTIST_RE) for s in probes):
        return "现代作品/艺人"
    d = _modern_dir_of(origs)
    if d:
        return f"现代目录（{d}）"
    if any(_LATE_NAME_RE.search(s) for s in probes):
        return "晚卒作曲家"
    return None

COPYRIGHT_PAT = re.compile(r"©|\(c\)|copyright|all rights reserved|www\.|http", re.I)


def has_copyright_event(path: Path) -> bool:
    """读 MIDI 的 Copyright meta-event（速度优先，只扫前若干事件）。"""
    try:
        import mido
        mid = mido.MidiFile(str(path))
        for track in mid.tracks:
            for msg in track[:60]:
                if msg.type == "copyright" and msg.text and COPYRIGHT_PAT.search(msg.text):
                    return True
        return False
    except Exception:
        return True          # 解析失败的保守剔除


# tar 内文件以 MD5 命名 → 需用原始路径映射做内容判断
PATHS_MAP: dict = {}


def load_paths_map() -> dict:
    global PATHS_MAP
    if PATHS_MAP:
        return PATHS_MAP
    p = ROOT / "sources" / "lakh" / "md5_to_paths.json"
    if p.exists():
        import json as _json
        PATHS_MAP = _json.loads(p.read_text(encoding="utf-8"))
    print(f"[lakh] md5→路径映射: {len(PATHS_MAP):,} 条", flush=True)
    return PATHS_MAP


def orig_paths_of(md5: str) -> list[str]:
    return PATHS_MAP.get(md5, [])


def extract_and_filter(tar_path: Path, tmpdir: Path, limit: int | None) -> list[Path]:
    """解压 + 初筛（用 md5 反查原始路径），返回保留的文件路径列表。"""
    load_paths_map()
    kept = []
    stats = Counter()
    with tarfile.open(tar_path, "r:gz") as tf:
        for i, m in enumerate(tf):
            if not m.isfile() or not m.name.lower().endswith(".mid"):
                continue
            md5 = Path(m.name).stem.lower()
            origs = orig_paths_of(md5)
            if not origs:
                stats["drop_无路径记录"] += 1
                continue
            why = drop_reason(origs)
            if why:
                stats[f"drop_{why}"] += 1
                continue
            if not KEEP_PAT.search(joined):
                stats["drop_无古典传统标记"] += 1
                continue
            if not KEEP_PAT.search(joined):
                stats["drop_无古典传统标记"] += 1
                continue
            stats["路径级保留"] += 1
            f = tf.extractfile(m)
            if f is None:
                continue
            dest = tmpdir / Path(m.name).name
            dest.write_bytes(f.read())
            kept.append(dest)
            if limit and len(kept) >= limit:
                break
            if len(kept) % 1000 == 0:
                print(f"  ... 已提取 {len(kept):,} 首", flush=True)
    print(f"[extract] {dict(stats)}", flush=True)
    return kept


def convert_one(idx: int, src: Path) -> tuple[str, dict | None, str | None]:
    """内容级过滤（版权声明）→ 入库。"""
    try:
        if has_copyright_event(src):
            return src.name, None, "含版权声明"
        bucket = idx // BUCKET
        rel = f"data/midi/{SOURCE_ID}/b{bucket:03d}/{SOURCE_ID}-b{bucket:03d}-{idx % BUCKET:05d}.mid"
        target = ROOT / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, target)
        return src.name, {"seq": idx, "midi": rel, "orig": src.name,
                          "orig_path": (orig_paths_of(Path(src.name).stem.lower()) or [""])[0]}, None
    except Exception as e:
        return src.name, None, str(e)[:100]


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--workers", type=int, default=8)
    args = ap.parse_args(argv[1:])

    if not TARBALL.exists():
        print(f"[error] 未找到 {TARBALL}", flush=True)
        return 1
    print(f"[lakh] tarball {TARBALL.stat().st_size/1024**3:.2f}GB", flush=True)

    st = json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {"done": {}, "failed": []}
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        kept = extract_and_filter(TARBALL, tmp, args.limit)
        if args.dry_run:
            print(f"[dry-run] 路径级保留 {len(kept):,} 首（未做版权过滤）", flush=True)
            return 0
        print(f"[lakh] 路径级保留 {len(kept):,} 首 → 内容级过滤…", flush=True)
        n_ok = n_bad = 0
        base = len(st["done"])
        with ThreadPoolExecutor(max_workers=args.workers) as ex:
            futs = {ex.submit(convert_one, base + i, p): p for i, p in enumerate(kept)}
            for fut in as_completed(futs):
                name, row, err = fut.result()
                if row:
                    st["done"][name] = row
                    n_ok += 1
                else:
                    st["failed"].append({"f": name, "err": err})
                    n_bad += 1
                if (n_ok + n_bad) % 1000 == 0:
                    STATE.write_text(json.dumps(st, ensure_ascii=False), encoding="utf-8")
                    print(f"  ... {n_ok + n_bad:,}/{len(kept):,}（保留 {n_ok:,}）", flush=True)
    st["failed"] = st["failed"][-300:]
    STATE.write_text(json.dumps(st, ensure_ascii=False), encoding="utf-8")
    print(f"[lakh] 内容过滤：保留 {n_ok:,} · 剔除 {n_bad:,}", flush=True)

    keys = sorted(st["done"].keys())
    with OUT_JSONL.open("w", encoding="utf-8", newline="\n") as fj:
        for seq, k in enumerate(keys):
            r = st["done"][k]
            fj.write(json.dumps({
                "id": f"{SOURCE_ID}-{seq:06d}", "source": SOURCE_ID,
                "src_path": f"sources/lakh/{r.get('orig_path') or r['orig']}",
                "title": Path(r.get("orig_path") or r["orig"]).stem.replace("_", " ")[:80],
                "composer_slug": None, "composer_name": None,
                "opus": None, "no": None, "genre": None, "form": None,
                "key": None, "period": None, "region": None, "instrument": None,
                "license": LICENSE, "zone": ZONE,
                "midi": {"file": r["midi"], "duration_sec": None, "note_count": None,
                         "tracks_count": None, "bpm": None},
                "fingerprint": None,
                "extra": {"source": "Lakh MIDI Dataset",
                          "note": "内容层已过滤版权声明；原数据集许可 CC-BY 4.0"},
            }, ensure_ascii=False, separators=(",", ":")) + "\n")
    print(f"[jsonl] {len(keys):,} rows -> {OUT_JSONL}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
