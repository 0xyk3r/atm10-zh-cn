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

第二组反例撞的是另一种假象：**前提不在时静默放过**。检查的前提（生成物、入库的
数据文件、mod jar）缺失时打一行 ℹ️ 然后返回成功，退出码跟「查过了没问题」一样。
`protect.py` 就这么把两条闸关了整整一个版本。跑在生成之后的环节一律传
`GATE_STRICT=1`，让「闸没跑成」变成红；`ci.yml` 用 `--no-jars`，那边**不设**。

## 为什么不会进出货包

夹具全部在**临时目录**里现造现删，仓库里一个假翻译文件都不留；
`assemble.py` 只摊 `src/`，`scripts/` 与临时目录都不进出货树。
出货侧另有 `vp-no-stray-class-patch` 等闸兜底。

用法:
    python3 scripts/compliance/test_gates.py
"""
import json
import os
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


@case('停发的配置界面模块漏回出货树', 'vp-never-ship-config-ui')
def _c8(mods):
    # r14 那次事故的形状：模块本该被 PERF_HOLD 排除，却因为脏 build/ 或排除逻辑失效
    # 又回到了包里。它一进包，全局替换表就从 1086 对涨回 3396 对，掉帧照旧。
    (mods / 'config_ui_generated.json').write_text(
        json.dumps([{'name': 'x', 'dynamic': True, 'i18n': False},
                    {'target_class': ['net.createmod.catnip.config.ui.BaseConfigScreen'],
                     'pairs': [{'key': 'Advanced Capacity', 'value': '进阶容量'}]}],
                   ensure_ascii=False), encoding='utf-8')


@case('物品 tooltip 值里留了换行', 'occultism-tooltip-no-newline')
def _c9(mods):
    # issue #8 的形状：`\n` 在 tooltip 里不断行，而是被当成普通字符去查字形，
    # unifont 给控制字符画的是一个写着 LF 的方框。上游 en_us 自己就带这些换行，
    # 升版重导上游译文时会原样带回来，所以要有闸。
    p = (mods.parent.parent / 'resourcepacks' / 'ATM10汉化包' /
         'assets' / 'occultism' / 'lang' / 'zh_cn.json')
    d = json.loads(p.read_text(encoding='utf-8')) if p.is_file() else {}
    d['item.occultism.chalk_rainbow.auto_tooltip'] = '可代替任意粉笔符文。\n它可以呈现出任何彩色符文的外观。'
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(d, ensure_ascii=False), encoding='utf-8')


@case('出货树残留字节码补丁', 'vp-no-stray-class-patch')
def _c6(mods):
    f = mods.parent / 'patch' / 'com' / 'ldtteam' / 'blockui' / 'controls' / 'Button.class'
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_bytes(b'\xca\xfe\xba\xbe\x00\x00\x00\x41')


def fixture(tmp):
    """把 src/ + scripts/ 复制一份到临时目录，搭出一棵出货树，返回树的路径。"""
    shutil.copytree(ROOT / 'src', tmp / 'src')
    shutil.copytree(ROOT / 'scripts', tmp / 'scripts')
    # versions/db 是**入库**的（keybinds.json 等），不是生成物。不带上它，
    # 「按键注册名」那条在夹具里就没有前提、跟着静默消失——夹具本身成了假闸。
    if (ROOT / 'versions' / 'db').is_dir():
        shutil.copytree(ROOT / 'versions' / 'db', tmp / 'versions' / 'db')
    tree = tmp / 'build' / 'common'
    (tree / 'vaultpatcher').mkdir(parents=True)
    shutil.copytree(ROOT / 'src' / 'vaultpatcher' / 'modules',
                    tree / 'vaultpatcher' / 'modules')
    for d in ('config', 'resourcepacks', 'kubejs'):
        if (ROOT / 'build' / 'common' / d).is_dir():
            shutil.copytree(ROOT / 'build' / 'common' / d, tree / d, symlinks=True)
    return tree


def run_case(name, inject, rule_id):
    """把 src/ 复制一份到临时目录，注入违规，跑 check.py，看有没有报出那条规则。"""
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        tree = fixture(tmp)
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


# ── 第二组反例：「前提不在 → 静默放过」这类假闸 ────────────────────────────
#
# 前一组撞的是「翻译内容违规」。这一组撞的是另一种假象：检查的前提（生成物、
# 入库的数据文件、mod jar）不在时打一行 ℹ️ 然后**返回成功**——退出码上跟
# 「查过了没问题」一模一样。protect.py 那次就是这么漏了两条闸整整一个版本。
#
# 这里不断言「基线全绿」：夹具里没有完整出货树（ci.yml 把本脚本排在摊树之前），
# check.py 本来就会因别的原因报错。所以只断言**那句话在不在**。
MISSING = []


def missing_case(name):
    def deco(fn):
        MISSING.append((name, fn))
        return fn
    return deco


def check_out(tmp, tree, strict):
    env = dict(os.environ)
    env.pop('GATE_STRICT', None)
    if strict:
        env['GATE_STRICT'] = '1'
    r = subprocess.run([sys.executable, str(tmp / 'scripts' / 'check.py'), str(tree)],
                       capture_output=True, text=True, cwd=tmp, env=env)
    return r.returncode, r.stdout + r.stderr


@missing_case('GATE_STRICT 下「前提是生成物但没生成」→ 必须红')
def _m1(tmp, tree):
    rc, out = check_out(tmp, tree, strict=True)
    return rc != 0 and '没跑成' in out and 'GATE_STRICT' in out


@missing_case('不设 GATE_STRICT 时同一棵树 → 仍按 ℹ️ 跳过（ci.yml 走这条）')
def _m2(tmp, tree):
    rc, out = check_out(tmp, tree, strict=False)
    return 'ℹ️ 跳过' in out and '没跑成' not in out


@missing_case('入库的 keybinds.json 全没了 → 不看 GATE_STRICT 也必须红')
def _m3(tmp, tree):
    shutil.rmtree(tmp / 'versions' / 'db')
    rc, out = check_out(tmp, tree, strict=False)
    return rc != 0 and '按键注册名检查没跑成' in out


@missing_case('GATE_STRICT 下没有 mods 目录 → check_gui_maps 必须红')
def _m4(tmp, tree):
    env = dict(os.environ)
    env['GATE_STRICT'] = '1'
    env.pop('ATM_PACK_ROOT', None)
    r = subprocess.run([sys.executable,
                        str(tmp / 'scripts' / 'compliance' / 'check_gui_maps.py'),
                        str(tmp / '压根不存在' / 'mods')],
                       capture_output=True, text=True, cwd=tmp, env=env)
    return r.returncode != 0 and '没跑成' in (r.stdout + r.stderr)


def run_missing(name, fn):
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        ok = fn(tmp, fixture(tmp))
    print(('✅' if ok else '❌') + ' %s' % name)
    return ok


def main():
    print('闸的反例测试：每条都复刻一次真实事故，验它真的会红\n')
    ok = sum(run_case(*c) for c in CASES)
    print('\n%d/%d 条闸经反例验证确实会红' % (ok, len(CASES)))
    print('\n前提缺失时不许静默放过：\n')
    ok2 = sum(run_missing(*m) for m in MISSING)
    print('\n%d/%d 条' % (ok2, len(MISSING)))
    if ok != len(CASES) or ok2 != len(MISSING):
        print('有闸没拦住反例——它现在是假闸，修好之前不许发版。')
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
