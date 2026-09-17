#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""通用下载器（不依赖 shell 命令）

用法：
  python tools/fetch.py github <owner>/<repo> <dest_name> [--branch B]
      # 下载 GitHub 仓库 zip 归档 → sources/_downloads/<dest_name>.zip → 解压到 sources/<dest_name>/
  python tools/fetch.py url <url> <dest_rel_path>
      # 通用 URL 下载（保存到工作区相对路径）
  python tools/fetch.py probe <owner>/<repo>
      # 查询仓库默认分支与大小

所有下载记录写入 tools/state/downloads.json，供断点与审计追溯。
"""
from __future__ import annotations

import json
import ssl
import sys
import time
import urllib.request
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DL_DIR = ROOT / "sources" / "_downloads"
SRC_DIR = ROOT / "sources"
STATE = ROOT / "tools" / "state" / "downloads.json"
UA = {"User-Agent": "midicn-lib-fetcher/0.1 (+https://lib.midicn.com)"}


def _ctx() -> ssl.SSLContext:
    return ssl.create_default_context()


def http_get(url: str, timeout: int = 120) -> bytes:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout, context=_ctx()) as r:
        return r.read()


def api_json(url: str) -> dict:
    return json.loads(http_get(url).decode("utf-8"))


def load_state() -> dict:
    if STATE.exists():
        return json.loads(STATE.read_text(encoding="utf-8"))
    return {}


def save_state(state: dict) -> None:
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def record(key: str, info: dict) -> None:
    st = load_state()
    st[key] = {**info, "at": datetime.now(timezone.utc).isoformat(timespec="seconds")}
    save_state(st)


def probe(repo: str) -> dict:
    d = api_json(f"https://api.github.com/repos/{repo}")
    return {"full_name": d.get("full_name"), "default_branch": d.get("default_branch"),
            "size_kb": d.get("size"), "license": (d.get("license") or {}).get("spdx_id"),
            "pushed_at": d.get("pushed_at"), "description": (d.get("description") or "")[:160]}


def github_zip(repo: str, dest_name: str, branch: str | None = None,
               only_exts: set[str] | None = None) -> Path:
    info = probe(repo)
    br = branch or info["default_branch"]
    print(f"[probe] {info['full_name']} · branch={br} · size≈{info['size_kb']/1024:.1f} MB · license={info['license']}")
    print(f"[probe] desc: {info['description']}")
    DL_DIR.mkdir(parents=True, exist_ok=True)
    zip_path = DL_DIR / f"{dest_name}.zip"
    url = f"https://codeload.github.com/{repo}/zip/refs/heads/{br}"
    t0 = time.time()
    data = http_get(url, timeout=1800)
    zip_path.write_bytes(data)
    dt = time.time() - t0
    print(f"[fetch] {url} -> {zip_path.name}  {len(data)/1024/1024:.1f} MB in {dt:.1f}s ({len(data)/1024/dt:.0f} KB/s)")

    out_dir = SRC_DIR / dest_name
    out_dir.mkdir(parents=True, exist_ok=True)
    n = kept = 0
    with zipfile.ZipFile(zip_path) as z:
        names = z.namelist()
        prefix = names[0].split("/")[0] + "/"
        for m in names:
            if m.endswith("/"):
                continue
            n += 1
            ext = m.rsplit(".", 1)[-1].lower() if "." in m.rsplit("/", 1)[-1] else ""
            if only_exts and ext not in only_exts:
                continue
            rel = m[len(prefix):]
            if not rel:
                continue
            target = out_dir / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            with z.open(m) as src, open(target, "wb") as f:
                f.write(src.read())
            kept += 1
    print(f"[unzip] {kept}/{n} files -> {out_dir} (filter={sorted(only_exts) if only_exts else 'all'})")
    record(f"github:{repo}", {"repo": repo, "branch": br, "zip": str(zip_path.relative_to(ROOT)),
                              "files_total": n, "files_kept": kept, "dest": str(out_dir.relative_to(ROOT)),
                              "license_spdx": info["license"], "bytes": len(data)})
    return out_dir


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 1
    cmd = argv[1]
    if cmd == "probe":
        print(json.dumps(probe(argv[2]), ensure_ascii=False, indent=2))
        return 0
    if cmd == "github":
        branch = None
        only = None
        if "--branch" in argv:
            branch = argv[argv.index("--branch") + 1]
        if "--only" in argv:
            only = {e.lower().lstrip(".") for e in argv[argv.index("--only") + 1].split(",")}
        github_zip(argv[2], argv[3], branch, only)
        return 0
    if cmd == "url":
        url, rel = argv[2], argv[3]
        target = ROOT / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        data = http_get(url)
        target.write_bytes(data)
        print(f"[fetch] {url} -> {rel} ({len(data)/1024:.1f} KB)")
        record(f"url:{url}", {"url": url, "dest": rel, "bytes": len(data)})
        return 0
    print(__doc__)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
