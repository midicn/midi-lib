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
    for pat in ('lib/site/.github/workflows/*.y*ml', 'mid/site/.github/workflows/*.y*ml',
                'zip/site/.github/workflows/*.y*ml', '*/.github/workflows/*.y*ml'):
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


def check_meta_versions() -> bool:
    """`meta/` 三件套版本号一致性（**发版强制检查**）。

    为什么需要：2026-09-24 发现 `meta/catalog.json` 落后了 **5 个版本**
    （停在 v1.18 / 124,179 条，而 `version.json` 已是 v1.23 / 133,667 条）——
    根因是发版流程只更新了 `version.json` 与 `packs-manifest.json`，**漏了 catalog**。

    检查：`version.json` · `packs-manifest.json` · `catalog.json`（数据仓 + 站点侧各一份）
    全部归一化后必须等于 `build_release.py` 的 VERSION（唯一真源）。
    注意：三个文件的版本写法不同（有的 `"v1.23"`、有的 `"1.23"`），故**归一化后再比**。
    """
    import json as _json
    import re as _re

    def _norm(v) -> str:
        return _re.sub(r"^v", "", str(v or "").strip())

    src = (ROOT / "tools" / "build_release.py").read_text(encoding="utf-8")
    m = _re.search(r'^VERSION\s*=\s*"([^"]+)"', src, _re.M)
    if not m:
        print("  ✗ build_release.py 里找不到 VERSION")
        return False
    want = _norm(m.group(1))

    targets = [
        ("数据仓 version.json", Path("..") / "library" / "meta" / "version.json"),
        ("数据仓 packs-manifest.json", Path("..") / "library" / "meta" / "packs-manifest.json"),
        ("数据仓 catalog.json", Path("..") / "library" / "meta" / "catalog.json"),
        ("站点侧 catalog.json", Path("..") / "site" / "meta" / "catalog.json"),
    ]
    bad = []
    print(f"  真源 VERSION = {want}（build_release.py）")
    for label, rel in targets:
        f = (ROOT / rel).resolve()
        if not f.exists():
            print(f"    -- {label:28} 不存在（跳过）")
            continue
        try:
            got = _norm(_json.loads(f.read_text(encoding="utf-8")).get("version"))
        except Exception as e:                                     # noqa: BLE001
            bad.append(label); print(f"    ✗ {label:28} 解析失败：{e}"); continue
        ok = got == want
        if not ok:
            bad.append(label)
        print(f"    {'✓' if ok else '✗'} {label:28} {got!r}")
    if bad:
        print(f"  ✗ {len(bad)} 个文件的版本号与真源不一致：{' · '.join(bad)}")
        return False
    print("  ✓ meta/ 三件套版本一致")
    return True


def check_file_sizes() -> bool:
    """单文件体积哨兵（**给 Git 的 100 MiB 硬限留安全边际**）。

    背景：GitHub 对 git 里的文件 —— **>50 MiB 只警告，>100 MiB 直接拒绝推送**；
    Release 资产另算（单文件 2 GB）。`catalog.json` 目前约 53 MiB，
    随曲目增加会缓慢增长，需要在**撞墙之前**得到提醒而不是事后报错。

    阈值：硬限 100 MiB → 提醒线 72 MiB（80%）、拦截线 90 MiB。
    到提醒线时应开始考虑：① 转列式（可省约 37% —— 重复键名开销）
    ② 拆成 `catalog/part-NNN.json` + 索引；**Git LFS 不可行**
    （raw.githubusercontent 会返回指针文件，站点与脚本会全断）。
    """
    LIMIT = 90 * 1024 * 1024          # 拦截线
    WARN = int(72 * 1024 * 1024)      # 提醒线
    watch = [Path("..") / "library" / "meta", Path("..") / "site" / "meta"]
    over, warn, scan = [], [], 0
    for d in watch:
        if not d.exists():
            continue
        for f in sorted(d.iterdir()):
            if not f.is_file() or f.suffix not in (".json", ".txt"):
                continue
            scan += 1
            sz = f.stat().st_size
            tag = f"{d.parent.name}/{d.name}/{f.name}"
            if sz > LIMIT:
                over.append((tag, sz))
            elif sz > WARN:
                warn.append((tag, sz))
    print(f"  扫描 {scan} 个 meta 文件（提醒线 72 MiB · 拦截线 90 MiB）")
    for tag, sz in warn:
        print(f"    ⚠ {sz/2**20:6.2f} MiB  {tag}")
    for tag, sz in over:
        print(f"    ✗ {sz/2**20:6.2f} MiB  {tag}")
    if over:
        print("  ✗ 有文件逼近 Git 的 100 MiB 硬限，需先拆分/转列式再发版")
        return False
    if warn:
        print("  · 有文件已过提醒线（未超限，暂不阻断）—— 建议开始规划拆分方案")
    else:
        print("  ✓ 所有 meta 文件均在安全线内")
    return True


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

    # ①c meta/ 三件套版本一致性（发版强制：catalog 曾落后 5 个版本）
    print('=' * 88)
    print('【1c/4 meta 版本一致性】')
    print('-' * 88)
    results.append(('meta 版本一致性（version / packs / catalog）', check_meta_versions()))

    # ①d 单文件体积哨兵（Git 100 MiB 硬限的安全边际）
    print('=' * 88)
    print('【1d/4 单文件体积】')
    print('-' * 88)
    results.append(('单文件体积（Git 100 MiB 硬限边际）', check_file_sizes()))

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
                    [NODE, E2E, str(ROOT.parent / 'site' / 'index.html')], ROOT.parent / 'site', env=env, keep=8)
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
