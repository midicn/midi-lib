#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""通用 ABC → MIDI 接入器（批次 2 核心管线）

支持源（--source）：
  essen        EsAC 数据库（sources/essen/esac/*.abc，含 O: 地域）
  nottingham   Nottingham Music Database（sources/nottingham/nottingham_database/*.abc）
  thesession   thesession.org（sources/thesession-data/csv/tunes.csv，每 tune 取首个 setting）

流程：ABC 拆曲（X:）→ abc2midi 并行转换 → data/midi/<source>/b*/ → midi_db/tracks/<source>.jsonl
断点续传：tools/state/<source>-progress.json

用法：
  python tools/ingest_abc.py --source essen --workers 8
  python tools/ingest_abc.py --source thesession --limit 2000
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ABC2MIDI = ROOT / "tools" / "bin" / "abcmidi" / "abcmidi_win32_mingw64" / "abc2midi.exe"
BUCKET = 1000
XRE = re.compile(r"^X\s*:", re.I)
FIELD = re.compile(r"^([A-Za-z])\s*:\s*(.*)$")

SOURCES = {
    "essen": {
        "dirs": ["sources/essen/esac"],
        "license": "OPEN", "zone": "main", "genre": "folk",
    },
    "nottingham": {
        "dirs": ["sources/nottingham/nottingham_database"],
        "license": "OPEN", "zone": "main", "genre": "folk",
        "default_region": "英国/美国",
    },
    "thesession": {
        "csv": "sources/thesession-data/csv/tunes.csv",
        "license": "CC-BY-SA-4.0", "zone": "main", "genre": "folk",
        "default_region": "爱尔兰",
    },
    "abcmisc": {
        "dirs": ["sources/abc-misc"],
        "license": "OPEN", "zone": "main", "genre": "folk",
        "region_by_file": {"balk1": "巴尔干", "balk2": "巴尔干", "isra": "以色列",
                           "intl": "国际民歌", "allklez": "克莱兹梅尔"},
    },
    "norbeck": {
        "dirs": ["sources/norbeck"],
        "license": "OPEN", "zone": "main", "genre": "folk",
        "default_region": "爱尔兰/瑞士",
    },
}


# ---------- ABC 解析 ----------

def split_abc(text: str) -> list[dict]:
    """含多曲的 ABC → 单曲记录列表（保留字段头与乐体）。"""
    tunes, cur = [], None
    for line in text.splitlines():
        if XRE.match(line):
            if cur:
                tunes.append(cur)
            cur = {"x": line.split(":", 1)[1].strip(), "lines": []}
        elif cur is not None:
            cur["lines"].append(line)
    if cur:
        tunes.append(cur)
    for t in tunes:
        fields, body_start = {}, 0
        for i, l in enumerate(t["lines"]):
            m = FIELD.match(l)
            if m and not l.startswith("%"):
                fields.setdefault(m.group(1).upper(), m.group(2).strip())
                body_start = i + 1
            elif l.strip() and not l.strip().startswith("%"):
                body_start = i
                break
        t["fields"] = fields
        t["body"] = "\n".join(t["lines"][body_start:])
    return tunes


def clean_region(raw: str | None) -> str | None:
    if not raw:
        return None
    parts = [p.strip() for p in raw.split(",") if p.strip()]
    return parts[-1] if parts else None


def region_of(it: dict, cfg: dict) -> str | None:
    """按文件名前缀推断地域（abcmisc 的 balk1/isra/intl/allklez 等）。"""
    mapping = cfg.get("region_by_file")
    if not mapping:
        return None
    stem = ""
    if it.get("abc_path") is not None:
        stem = it["abc_path"].stem
    else:
        stem = str(it.get("key", ""))
    for prefix, region in mapping.items():
        if stem.startswith(prefix):
            return region
    return None


def build_abc_text(t: dict | None, head: dict | None = None) -> str:
    if head is not None:  # thesession：csv 组装
        return (f"X:1\nT:{head['name']}\nR:{head.get('type','')}\n"
                f"M:{head.get('meter','4/4')}\nK:{head.get('mode','G')}\nL:1/8\n{head['abc']}\n")
    out = [f"X:{t['x'] or '1'}"]
    for k in ("T", "C", "R", "M", "L", "Q", "K", "O"):
        if k in t["fields"]:
            out.append(f"{k}:{t['fields'][k]}")
    for k, v in (("K", "G"), ("M", "4/4"), ("L", "1/8")):
        if k not in t["fields"]:
            out.append(f"{k}:{v}")
    return "\n".join(out) + "\n" + t["body"] + "\n"


def convert(abc_text: str, tmpdir: Path, tag: str) -> bytes | None:
    src = tmpdir / f"{tag}.abc"
    out = tmpdir / f"{tag}.mid"
    src.write_text(abc_text, encoding="utf-8")
    subprocess.run([str(ABC2MIDI), str(src), "-o", str(out)],
                   capture_output=True, text=True, timeout=60)
    return out.read_bytes() if out.exists() else None


# ---------- 状态 ----------

def state_path(src_id: str) -> Path:
    return ROOT / "tools" / "state" / f"{src_id}-progress.json"


def load_state(src_id: str) -> dict:
    p = state_path(src_id)
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    return {"done": [], "failed": [], "rows": {}}


def save_state(src_id: str, st: dict) -> None:
    p = state_path(src_id)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(st, ensure_ascii=False), encoding="utf-8")


# ---------- 采集 ----------

def collect(src_id: str, cfg: dict) -> list[dict]:
    items: list[dict] = []
    if "csv" in cfg:
        csv_path = ROOT / cfg["csv"]
        seen = set()
        with csv_path.open(encoding="utf-8", errors="replace") as f:
            total = 0
            for r in csv.DictReader(f):
                total += 1
                tid = r["tune_id"]
                if tid in seen:
                    continue
                seen.add(tid)
                items.append({
                    "key": f"ts-{tid}", "abc_path": None, "tune": None, "tune_id": tid,
                    "head": {"name": r["name"], "type": r["type"], "meter": r["meter"],
                             "mode": r["mode"], "abc": r["abc"],
                             "composer": (r.get("composer") or "").strip()},
                })
        print(f"[collect] {src_id}: csv 行 {total} → 去重 tune {len(items)}")
        return items
    for d in cfg["dirs"]:
        for abc in sorted((ROOT / d).rglob("*.abc")):
            text = abc.read_text(encoding="utf-8", errors="replace")
            for t in split_abc(text):
                items.append({"key": f"{abc.stem}#x{t['x']}", "abc_path": abc,
                              "tune": t, "head": None, "tune_id": None})
    print(f"[collect] {src_id}: abc 曲目 {len(items)}")
    return items


# ---------- 转换（并行安全） ----------

def stable_rel(src_id: str, key: str, ext: str = ".mid") -> str:
    """**稳定路径**：基于 key 哈希（与排序/序号无关）——避免 state 累积导致的重分配覆盖。

    data/midi/<source>/b<桶3位>/<source>-<哈希12位>.mid
    """
    h = hashlib.md5(key.encode("utf-8")).hexdigest()
    bucket = int(h[:3], 16) % 256
    return f"data/midi/{src_id}/b{bucket:03d}/{src_id}-{h[:12]}{ext}"


def convert_one(it: dict, seq: int, src_id: str, cfg: dict,
                tmpdir: Path) -> tuple[str, dict | None, str | None]:
    try:
        if it["head"] is not None:
            abc_text = build_abc_text(None, it["head"])
            fields = {"T": it["head"]["name"], "R": it["head"]["type"],
                      "M": it["head"]["meter"], "K": it["head"]["mode"],
                      "C": it["head"]["composer"] or None}
        else:
            abc_text = build_abc_text(it["tune"])
            f = it["tune"]["fields"]
            fields = {"T": f.get("T"), "R": f.get("R"), "M": f.get("M"),
                      "K": f.get("K"), "C": f.get("C"), "O": f.get("O"), "N": f.get("N")}
        data = convert(abc_text, tmpdir, f"t{seq}")
        if data is None:
            return it["key"], None, "abc2midi no output"
        rel = stable_rel(src_id, it["key"])
        target = ROOT / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        row = {
            "src_path": (it["abc_path"].relative_to(ROOT).as_posix()
                         if it["abc_path"] else cfg["csv"]),
            "title": fields.get("T") or (it["head"]["name"] if it["head"] else it["key"]),
            "form": (fields.get("R") or "").split(",")[0].strip().lower() or None,
            "key": fields.get("K"),
            "composer": (fields.get("C") or "").strip() or None,
            "region": (clean_region(fields.get("O"))
                       or region_of(it, cfg)
                       or cfg.get("default_region")),
            "meter": fields.get("M"),
            "midi": rel,
            "tune_id": it.get("tune_id"),
            "native_id": fields.get("N"),
        }
        return it["key"], row, None
    except Exception as e:
        return it["key"], None, str(e)[:150]


def write_jsonl(src_id: str, cfg: dict, st: dict) -> int:
    keys = sorted(st.get("rows", {}).keys())
    out = ROOT / "midi_db" / "tracks" / f"{src_id}.jsonl"
    with out.open("w", encoding="utf-8", newline="\n") as f:
        for seq, k in enumerate(keys):
            r = st["rows"][k]
            row = {
                "id": f"{src_id}-{seq:06d}", "source": src_id, "src_path": r["src_path"],
                "title": r["title"], "composer_slug": None,
                "composer_name": r.get("composer") or "传统曲调 Traditional",
                "opus": None, "no": None, "genre": cfg["genre"], "form": r["form"],
                "key": r["key"], "period": None, "region": r["region"],
                "instrument": "melody", "license": cfg["license"], "zone": cfg["zone"],
                "midi": {"file": r["midi"], "duration_sec": None, "note_count": None,
                         "tracks_count": None, "bpm": None},
                "fingerprint": None,
                "extra": {"meter": r["meter"], "tune_id": r.get("tune_id"),
                          "native_id": r.get("native_id"), "key_in_dataset": k},
            }
            f.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")
    print(f"[jsonl] {len(keys)} rows -> {out}")
    return len(keys)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True, choices=list(SOURCES))
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--jsonl-only", action="store_true")
    args = ap.parse_args(argv[1:])

    src_id, cfg = args.source, SOURCES[args.source]
    items = collect(src_id, cfg)
    seq_map = {it["key"]: i for i, it in enumerate(sorted(items, key=lambda x: x["key"]))}
    st = load_state(src_id)
    done = set(st.get("done", []))
    todo = [it for it in items if it["key"] not in done]
    if args.limit:
        todo = todo[:args.limit]
    print(f"[convert] total={len(items)} done={len(done)} todo={len(todo)} workers={args.workers}")

    if not args.jsonl_only and todo:
        if not ABC2MIDI.exists():
            print(f"[fatal] abc2midi 不存在: {ABC2MIDI}")
            return 1
        rows = st.setdefault("rows", {})
        failed = st.setdefault("failed", [])
        t0 = time.time()
        n_ok = n_err = 0
        with tempfile.TemporaryDirectory() as td, \
                ThreadPoolExecutor(max_workers=args.workers) as ex:
            tmp = Path(td)
            futs = {ex.submit(convert_one, it, seq_map[it["key"]], src_id, cfg, tmp): it
                    for it in todo}
            for fut in as_completed(futs):
                key, row, err = fut.result()
                if row:
                    rows[key] = row
                    done.add(key)
                    n_ok += 1
                else:
                    failed.append({"key": key, "err": err})
                    n_err += 1
                if (n_ok + n_err) % 500 == 0:
                    st["done"] = sorted(done)
                    save_state(src_id, st)
                    el = time.time() - t0
                    rate = (n_ok + n_err) / max(el, 0.01)
                    eta = (len(todo) - n_ok - n_err) / max(rate, 0.01)
                    print(f"  ... {n_ok + n_err}/{len(todo)} {rate:.1f}/s "
                          f"ok={n_ok} err={n_err} ETA {eta/60:.0f}min", flush=True)
        st["done"] = sorted(done)
        save_state(src_id, st)
        print(f"[convert] run done: +{n_ok} ok · {n_err} failed")

    write_jsonl(src_id, cfg, st)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
