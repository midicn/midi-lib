#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""发布前置检查（midicn-lib）——把「文档同步 / 台账复核 / 站点回归」串成一道门。

用法
  python tools/preflight.py                 # 文档同步 + 台账复核 + 站点本地回归
  python tools/preflight.py --hash          # 追加整包 MD5/字节数复核（读盘约 2.8GB）
  python tools/preflight.py --online        # 追加各来源地址可达性
  python tools/preflight.py --no-e2e        # 跳过站点回归（无 node/jsdom 环境时）

何时跑
  · 每次生成发布包前（build_release → package → release 之前）
  · 改过文档 / 来源台账 / 站点任一文件后

退出码：0 = 全绿；1 = 有失败项（**不要带着失败打包或部署**）
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY = sys.executable
NODE = os.environ.get('MIDICN_NODE', r'C:/Program Files/nodejs/node.exe')
NODE_MODULES = os.environ.get('MIDICN_NODE_MODULES',
                              r'<local>/.workbuddy/binaries/node/workspace/node_modules')
E2E = os.environ.get('MIDICN_E2E',
                     r'<local>/.workbuddy/binaries/node/workspace/diag-e2e.js')


def run(name: str, cmd: list[str], cwd: Path, env: dict | None = None, keep: int = 12) -> tuple[bool, str]:
    print('=' * 88)
    print(f'【{name}】')
    print('$ ' + ' '.join(str(c) for c in cmd))
    print('-' * 88)
    try:
        r = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, timeout=3600, env=env)
    except Exception as e:                                     # noqa: BLE001
        print(f'  执行失败：{type(e).__name__}: {e}')
        return False, f'{type(e).__name__}'
    out = (r.stdout or '') + (r.stderr or '')
    lines = [l for l in out.splitlines() if l.strip()]
    tail = lines[-keep:] if len(lines) > keep else lines
    print('\n'.join(tail))
    if len(lines) > keep:
        print(f'  …（共 {len(lines)} 行，仅显示末尾 {keep} 行）')
    print(f'  退出码 {r.returncode}')
    return r.returncode == 0, out


def main(argv) -> int:
    ap = argparse.ArgumentParser(description='发布前置检查')
    ap.add_argument('--hash', action='store_true', help='追加整包校验值复核')
    ap.add_argument('--online', action='store_true', help='追加来源地址可达性')
    ap.add_argument('--no-e2e', action='store_true', help='跳过站点回归')
    args = ap.parse_args(argv[1:])

    results = []

    # ① 文档单一真源同步
    results.append(('文档同步（真源 → 副本）',
                    run('1/3 文档同步检查', [PY, 'tools/sync_docs.py', '--check'], ROOT)[0]))

    # ② 来源台账复核
    cmd = [PY, 'tools/provenance.py']
    if args.hash:
        cmd.append('--hash')
    if args.online:
        cmd.append('--online')
    results.append(('来源台账复核', run('2/3 来源台账复核', cmd, ROOT, keep=16)[0]))

    # ③ 站点回归（本地）
    if args.no_e2e:
        print('=' * 88)
        print('【3/3 站点回归】已按 --no-e2e 跳过')
    else:
        env = dict(os.environ)
        env['NODE_PATH'] = NODE_MODULES
        ok, _ = run('3/3 站点回归（本地）',
                    [NODE, E2E, str(ROOT / 'release/site-repo/index.html')], ROOT, env=env, keep=8)
        results.append(('站点回归（本地）', ok))

    print('=' * 88)
    print('前置检查汇总')
    print('-' * 88)
    for name, ok in results:
        print(f'  {"✓" if ok else "✗"} {name}')
    bad = [n for n, ok in results if not ok]
    if bad:
        print(f'\n✗ 有 {len(bad)} 项未通过：{" · ".join(bad)}')
        print('  → 不要带着失败打包或部署')
        return 1
    print('\n✓ 全部通过，可进入发布流程')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
