#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# atm10-zh-cn — All the Mods 10 简体中文汉化补丁「绿油油版」
# Copyright (C) 2026 星野夢華 (Hoshino Yumeka)
# SPDX-License-Identifier: GPL-3.0-or-later
"""闸的反例测试：造一批**故意违规**的样本，验每道闸真的会红。

## 为什么需要它

「写了闸」不等于「有闸」。2026-07-28 的对抗审计一次抓到三种假象：

- `check_gui_maps.py` / `check_dynamic_substrings.py` 写完了**从没接进任何流水线**；
- `vp-config-ui-no-single-word` 只查一个模块文件，另一份完全没保护；
- 好几个检查器在 glob 命中 0 个文件时**静默通过**，源文件被挪走闸就悄悄消失。

三种假象的共同点：跑一遍全绿，看起来一切正常。**只有拿反例去撞，才知道闸是不是实心的。**

## 反例长什么样

每条反例都复刻一次**真实事故**，而且都是「在游戏里绝不会生效」的假翻译——
它们只存在于临时目录里的夹具，跑完即弃：

| 反例 | 复刻的事故 |
|---|---|
| 模块里塞 `top horizontal` | 译了 blockui 的对齐标志串，整个 MineColonies/建筑棒对齐失效 |
| 配置模块塞单词键 `Sound` | 单词可能同时是枚举值，译了会被反查/写回配置 |
| 两条 `@` 子串键互为子串 | `String.replace` 顺序不定，长的那条被啃掉，翻出半中半英 |
| `class_patch: true` | 数据目录变成代码执行入口 |
| `vaultpatcher/patch/` 下留 `.class` | 旧补丁复活 → ClassFormatError 闪退 |
| 标识符样式的键 | 被拿去构造 ResourceLocation → 注册崩 |
| 以 `/` 开头的键 | 译了建筑棒的类别路径，查表落空 → NPE 闪退（issue #3） |

## 为什么不会进出货包

夹具全部在**临时目录**里现造现删，仓库里一个假翻译文件都不留；
`assemble.py` 只摊 `src/`，`scripts/` 与临时目录都不进出货树。
出货侧另有 `vp-no-stray-class-patch` 等闸兜底。

用法:
    python3 scripts/compliance/test_gates.py
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
CHECK = ROOT / 'scripts' / 'check.py'

# (名字, 怎么把违规注入到一棵临时出货树 / 临时模块目录, 期望报出的规则 id)
CASES = []


def case(name, rule_id):
    def deco(fn):
        CASES.append((name, fn, rule_id))
        return fn
    return deco


@case('译了 blockui 的对齐标志串', 'vp-blockui-alignment-tags')
def _c1(mods):
    p = mods / 'blockui.json'
    d = json.loads(p.read_text(encoding='utf-8'))
    d[1]['pairs'].append({'key': 'top horizontal', 'value': '顶部水平'})
    p.write_text(json.dumps(d, ensure_ascii=False), encoding='utf-8')


@case('配置界面模块出现单词键', 'vp-config-ui-no-single-word')
def _c2(mods):
    p = mods / 'catnip_config_ui.json'
    d = json.loads(p.read_text(encoding='utf-8'))
    d[1]['pairs'].append({'key': 'Sound', 'value': '音效'})
    p.write_text(json.dumps(d, ensure_ascii=False), encoding='utf-8')


@case('标识符样式的键被译', 'vp-identifier-not-translated')
def _c3(mods):
    p = mods / 'blockui.json'
    d = json.loads(p.read_text(encoding='utf-8'))
    d[1]['pairs'].append({'key': 'open_upgrade_screen', 'value': '打开升级界面'})
    p.write_text(json.dumps(d, ensure_ascii=False), encoding='utf-8')


@case('两条 @ 子串键互为子串', 'DYNSUB')
def _c4(mods):
    p = mods / 'minecolonies_styles.json'
    d = json.loads(p.read_text(encoding='utf-8'))
    d[1]['pairs'] += [{'key': 'Frontier', 'value': '@边疆'},
                      {'key': 'Farthest Frontier', 'value': '@最远边疆'}]
    p.write_text(json.dumps(d, ensure_ascii=False), encoding='utf-8')


@case('class_patch 被留开', 'vp-class-patch-off')
def _c5(mods):
    p = mods.parent.parent / 'config' / 'vaultpatcher_asm' / 'config.json'
    if not p.is_file():
        return
    d = json.loads(p.read_text(encoding='utf-8'))
    d['class_patch'] = True
    p.write_text(json.dumps(d, ensure_ascii=False), encoding='utf-8')


@case('路径片段被当界面文字译', 'vp-no-path-prefix-keys')
def _c7(mods):
    p = mods / 'minecolonies_styles.json'
    d = json.loads(p.read_text(encoding='utf-8'))
    d[1]['pairs'].append({'key': '/luxury', 'value': '@/豪华'})
    p.write_text(json.dumps(d, ensure_ascii=False), encoding='utf-8')


@case('出货树残留字节码补丁', 'vp-no-stray-class-patch')
def _c6(mods):
    f = mods.parent / 'patch' / 'com' / 'ldtteam' / 'blockui' / 'controls' / 'Button.class'
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_bytes(b'\xca\xfe\xba\xbe\x00\x00\x00\x41')


def run_case(name, inject, rule_id):
    """把 src/ 复制一份到临时目录，注入违规，跑 check.py，看有没有报出那条规则。"""
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        shutil.copytree(ROOT / 'src', tmp / 'src')
        shutil.copytree(ROOT / 'scripts', tmp / 'scripts')
        tree = tmp / 'build' / 'common'
        (tree / 'vaultpatcher').mkdir(parents=True)
        shutil.copytree(ROOT / 'src' / 'vaultpatcher' / 'modules',
                        tree / 'vaultpatcher' / 'modules')
        for d in ('config', 'resourcepacks', 'kubejs'):
            if (ROOT / 'build' / 'common' / d).is_dir():
                shutil.copytree(ROOT / 'build' / 'common' / d, tree / d, symlinks=True)
        inject(tmp / 'src' / 'vaultpatcher' / 'modules')
        inject(tree / 'vaultpatcher' / 'modules')
        if rule_id == 'DYNSUB':      # 这条由独立脚本查，不在 check.py 的规则里
            r = subprocess.run([sys.executable,
                                str(tmp / 'scripts' / 'compliance' / 'check_dynamic_substrings.py')],
                               capture_output=True, text=True, cwd=tmp)
            ok = r.returncode != 0
            print(('✅' if ok else '❌') + ' %-28s 期望 %-32s 退出码 %d'
                  % (name, 'check_dynamic_substrings', r.returncode))
            return ok
        r = subprocess.run([sys.executable, str(tmp / 'scripts' / 'check.py'), str(tree)],
                           capture_output=True, text=True, cwd=tmp)
        out = r.stdout + r.stderr
        ok = r.returncode != 0 and rule_id in out
        print(('✅' if ok else '❌') + ' %-28s 期望 %-32s 退出码 %d'
              % (name, rule_id, r.returncode))
        if not ok:
            line = [x for x in out.splitlines() if rule_id in x or '❌' in x]
            print('     实际输出：%s' % (line[0][:120] if line else out.strip()[:160]))
        return ok


def main():
    print('闸的反例测试：每条都复刻一次真实事故，验它真的会红\n')
    ok = sum(run_case(*c) for c in CASES)
    print('\n%d/%d 条闸经反例验证确实会红' % (ok, len(CASES)))
    if ok != len(CASES):
        print('有闸没拦住反例——它现在是假闸，修好之前不许发版。')
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
