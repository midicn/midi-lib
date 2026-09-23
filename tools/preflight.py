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
NODE_MODULES = os.environ.get('MIDICN_NODE_MODULES', '')
E2E = os.environ.get('MIDICN_E2E', '')


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


def check_workflows() -> bool:
    """workflow YAML 方言自检（**不依赖 pyyaml**）。

    本机托管解释器没有 pyyaml，但 Git 不能等到 CI 报错才发现 workflow 是非法 YAML。
    这里做定向检查：**未加引号的标量里出现 `: `（冒号+空格）**是 YAML 最常见的
    静默陷阱——GitHub 会直接拒绝解析整个 workflow。

    真实案例（2026-09-23 发现）：站点 workflow 里
        - name: Resolve release tag (single source: meta/version.json)
    因名字里的 `: ` 使文件成为非法 YAML，**mid 站的部署 workflow 一直是坏的**。
    修法是给该标量加引号。
    """
    print('=' * 88)
    print('【1b/4 workflow YAML 自检】')
    print('-' * 88)
    bad = []
    n = 0
    cands = []
    # 本仓（lib 站的 site-repo 在 release/ 下）+ 全部姊妹站仓（mid / zip …）
    cands += list(ROOT.glob('**/.github/workflows/*.y*ml'))
    for pat in ('*/site-repo/.github/workflows/*.y*ml', '*/.github/workflows/*.y*ml'):
        cands += list(ROOT.parent.glob(pat))
    seen = set()
    for wf in sorted(set(cands)):
        if '.git' in wf.parts or wf in seen:
            continue
        seen.add(wf)
        n += 1
        for i, line in enumerate(wf.read_text(encoding='utf-8').splitlines(), 1):
            s = line.strip()
            if not s.startswith('- name:') and not s.startswith('name:'):
                continue
            val = s.split(':', 1)[1].strip()
            if not val or val[0] in '"\'':
                continue                      # 已加引号 → 安全
            if ': ' in val or val.endswith(':'):
                try:
                    rel = wf.relative_to(ROOT.parent)
                except ValueError:
                    rel = wf.relative_to(ROOT)
                bad.append(f'{rel}:{i}  未加引号的标量含「: 」 → {val[:60]}')
    for b in bad:
        print(f'  ✗ {b}')
    if not bad:
        print(f'  ✓ {n} 个 workflow 未发现「未加引号的 : 」问题')
    print(f'  退出码 {1 if bad else 0}')
    return not bad


def main(argv) -> int:
    ap = argparse.ArgumentParser(description='发布前置检查')
    ap.add_argument('--hash', action='store_true', help='追加整包校验值复核')
    ap.add_argument('--online', action='store_true', help='追加来源地址可达性')
    ap.add_argument('--no-e2e', action='store_true', help='跳过站点回归')
    args = ap.parse_args(argv[1:])

    results = []

    # ① 文档单一真源同步
    results.append(('文档同步（真源 → 副本）',
                    run('1/4 文档同步检查', [PY, 'tools/sync_docs.py', '--check'], ROOT)[0]))

    # ①b workflow YAML 方言自检（不依赖 pyyaml）
    results.append(('workflow YAML 自检', check_workflows()))

    # ② 来源台账复核
    cmd = [PY, 'tools/provenance.py']
    if args.hash:
        cmd.append('--hash')
    if args.online:
        cmd.append('--online')
    results.append(('来源台账复核', run('2/4 来源台账复核', cmd, ROOT, keep=16)[0]))

    # ③ 版权合规：把 F1/F3 的人工复核结论固化为可重复断言
    #    （发布侧 lakh 现代版权作品必须为 0；歌词独立权利层条款必须在位）
    results.append(('版权合规审计（发布侧无现代版权作品）',
                    run('3/4 版权合规审计', [PY, 'tools/audit_license.py', '--quiet'], ROOT, keep=20)[0]))

    # ③b 公开内容卫生：过程痕迹 / 内部路径 / 内部脚本名 / 未完成标记
    #     不得进入公开页面、公开文档与公开工具。规则单一真源即该审计器。
    results.append(('公开内容卫生（无过程痕迹/内部路径/未完成标记）',
                    run('3b/4 公开内容卫生审计', [PY, 'tools/audit_public.py'], ROOT, keep=12)[0]))

    # ④ 站点回归（本地）
    if args.no_e2e:
        print('=' * 88)
        print('【4/4 站点回归】已按 --no-e2e 跳过')
    elif not NODE_MODULES or not E2E or not Path(NODE).exists():
        print('=' * 88)
        print('【4/4 站点回归】本机未配置 MIDICN_NODE_MODULES / MIDICN_E2E，跳过（不视为失败）')
        results.append(('站点回归（本地）', True))
    else:
        env = dict(os.environ)
        env['NODE_PATH'] = NODE_MODULES
        ok, _ = run('4/4 站点回归（本地）',
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
