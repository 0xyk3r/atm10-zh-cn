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
import zipfile
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


@case('同一个任务键落在两份文件里', 'quest-delta-no-duplicate-keys')
def _c11(mods):
    # gen_quest_lang_patches.py 之后，出货树里一个任务键只许由一份文件持有：
    # splitter 在 chapters/ 里根本不排序（Files.list 直接 forEach），
    # 落在两份文件里就等于「谁生效看 ext4 的哈希序」。
    d = mods.parent.parent / 'config' / 'ftbquests' / 'quests' / 'lang' / 'zh_cn' / 'chapters'
    d.mkdir(parents=True, exist_ok=True)
    key = '\tquest.0000A88BB40B2149.quest_desc: ["闸探针"]\n'
    for n in ('aaa_gate_probe_one.snbt', 'aaa_gate_probe_two.snbt'):
        (d / n).write_text('{\n' + key + '}\n', encoding='utf-8')


@case('两个客户端脚本重名声明', 'client-scripts-no-duplicate-decl')
def _c10(mods):
    # 2026-08-01 实机事故的形状：KubeJS client_scripts 共用一个全局作用域，
    # 第二个 `const $Component` 抛 redeclaration，整批脚本一起加载失败。
    d = mods.parent.parent / 'kubejs' / 'client_scripts'
    d.mkdir(parents=True, exist_ok=True)
    for n in ('aaa_gate_probe_one.js', 'aaa_gate_probe_two.js'):
        (d / n).write_text("const $Component = Java.loadClass('net.minecraft.network.chat.Component')\n",
                           encoding='utf-8')


@case('try 块内部写 const', 'js-no-const-inside-block')
def _c12(mods):
    # 2026-08-01 实机事故的形状：KubeJS 的 Rhino 把块里的 const 提升成函数作用域的
    # var，执行到声明那句抛 redeclaration of var——加载阶段 0 errors，躺在事件回调里
    # 就表现成「进游戏什么都没发生」。前三句是对照：顶格、回调体顶层、块里的赋值，
    # 上游天天在用，一条都不许被拦。
    d = mods.parent.parent / 'kubejs' / 'client_scripts'
    d.mkdir(parents=True, exist_ok=True)
    (d / 'aaa_gate_probe_block.js').write_text(
        "const TopLevelIsFine = Java.loadClass('net.minecraft.network.chat.Component')\n"
        "ClientEvents.loggedIn(event => {\n"
        "  const CallbackTopIsFine = Java.loadClass('java.util.HashSet')\n"
        "  let assignedLater = null\n"
        "  try {\n"
        "    assignedLater = Java.loadClass('java.util.ArrayList')\n"
        "    const InsideTryIsFatal = Java.loadClass('org.apache.http.impl.client.HttpClients')\n"
        "  } catch (err) {}\n"
        "})\n", encoding='utf-8')


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


def _delta(mods, text):
    p = (mods.parent.parent / 'config' / 'ftbquests' / 'quests' / 'lang' / 'zh_cn'
         / 'chapters' / 'zz_hanhua_zzz_gate_fixture.snbt')
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding='utf-8')


@case('delta 里有不属于任何键的游离行', 'quest-delta-blocks-parse')
def _c13(mods):
    # 2026-08-02 的形状：按行 sort 把多行数组打散，留下 513 个孤零零的 `""`。
    # 当时 check.py 只有按行正则，匹配不上就跳过 → 全绿放行。
    _delta(mods, '{\n\ttitle: "测试"\n\t\t""\n}\n')


@case('delta 里的多行数组到文件尾都没闭合', 'quest-delta-blocks-parse')
def _c14(mods):
    _delta(mods, '{\n\tdescription: [\n\t\t"第一行"\n}\n')


@case('delta 是个一条键都没有的空壳', 'quest-delta-blocks-parse')
def _c15(mods):
    # 空文件语法上合法，但「生成器静默产出空覆盖」＝这批译文人间蒸发。
    # 规则里有 allow_empty 名单，夹具用的文件名不在名单上，所以必须红。
    _delta(mods, '{\n}\n')


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


# ── 第三组反例：KubeJS 类过滤表 ───────────────────────────────────────────
#
# 复刻的事故：`hanhua_update_check.js` 在 vr16-beta4 与 vr16 里发了出去，一次都没工作
# 过。它在事件回调里 `Java.loadClass('java.lang.System')`，而 KubeJS 的过滤表写着
# `- java.lang`——必抛，异常又被 catch 吞掉，于是「进游戏什么都没发生」跟「已经是
# 最新版」长得一样。加载阶段 18/18 全绿，CI 全绿，发出去了也没人看得出来。
#
# 夹具里的过滤表是**现造的最小表**，不抄上游那份：只保留这道闸要判的两条语义
# ——包级前缀拒绝、精确类名放行。
def _kjs_fixture(tmp, loaded, table='- java.lang\n+ java.lang.Integer\n- java.net\n'):
    mods = tmp / 'pack' / 'mods'
    mods.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(mods / 'kubejs-neoforge-2101.7.2-build.368.jar', 'w') as z:
        z.writestr('kubejs.classfilter.txt', '# 夹具\n' + table)
    d = tmp / 'kjstree' / 'kubejs' / 'client_scripts'
    d.mkdir(parents=True, exist_ok=True)
    (d / 'probe.js').write_text(
        '\n'.join("const $C%d = Java.loadClass(%s)" % (i, a) for i, a in enumerate(loaded)) + '\n',
        encoding='utf-8')
    return mods, tmp / 'kjstree'


def _kjs_run(tmp, mods, tree):
    r = subprocess.run([sys.executable,
                        str(tmp / 'scripts' / 'compliance' / 'check_kubejs_classfilter.py'),
                        str(mods), str(tree)],
                       capture_output=True, text=True, cwd=tmp)
    return r.returncode, r.stdout + r.stderr


@missing_case('脚本 loadClass 了 java.net 里的类 → 必须红')
def _m5(tmp, tree):
    mods, kt = _kjs_fixture(tmp, ["'java.net.URI'", "'java.lang.System'"])
    rc, out = _kjs_run(tmp, mods, kt)
    return rc != 0 and 'java.net.URI' in out and 'java.lang.System' in out


@missing_case('包被禁但类被精确放行 → 必须绿（证明这道闸不是一律红）')
def _m6(tmp, tree):
    mods, kt = _kjs_fixture(tmp, ["'java.lang.Integer'", "'org.apache.http.client.methods.HttpGet'"])
    rc, out = _kjs_run(tmp, mods, kt)
    return rc == 0 and '全部放行' in out


@missing_case('loadClass 的参数不是字面量 → 静态判不了，必须红')
def _m7(tmp, tree):
    mods, kt = _kjs_fixture(tmp, ['CLASS_NAME'])
    rc, out = _kjs_run(tmp, mods, kt)
    return rc != 0 and '静态判不了' in out


@missing_case('拿不到 kubejs jar → 类过滤检查必须红')
def _m8(tmp, tree):
    mods, kt = _kjs_fixture(tmp, ["'java.util.HashSet'"])
    for jar in mods.glob('kubejs-*.jar'):
        jar.unlink()
    rc, out = _kjs_run(tmp, mods, kt)
    return rc != 0 and '没跑成' in out


# ── 第四组反例：Iron Jetpacks 的等级名 ────────────────────────────────────
#
# 复刻的事故：游戏里显示「Vibranium能量电池」「Creative喷气背包」。物品名模板在
# lang 里，但 `%s` 来自整合包 config 的 `name` 字段；mod 先查 `jetpack.<name>.name`，
# 查不到就**静默**回退成把 name 首字母大写。回退不报错、不留日志，17 个等级一条
# 没翻，跟全翻好了在任何自动检查里都长得一样，只能靠玩家截图发现。
#
# 档位清单随整合包版本变（ATM 自己加了 allthemodium/vibranium/unobtainium/creative），
# 所以夹具里的上游 config 是现造的，不抄任何一版的真实清单。
def _ijp_fixture(tmp, tiers, keys, make_config=True):
    up = tmp / 'uproot'
    if make_config:
        d = up / 'config' / 'ironjetpacks' / 'jetpacks'
        d.mkdir(parents=True, exist_ok=True)
        for name, disable in tiers:
            (d / ('%s.json' % name)).write_text(
                json.dumps({'name': name, 'disable': disable, 'tier': 1}),
                encoding='utf-8')
    else:
        up.mkdir(parents=True, exist_ok=True)
    lang = (tmp / 'ijptree' / 'resourcepacks' / 'ATM10汉化包'
            / 'assets' / 'ironjetpacks' / 'lang')
    lang.mkdir(parents=True, exist_ok=True)
    (lang / 'zh_cn.json').write_text(
        json.dumps(keys, ensure_ascii=False), encoding='utf-8')
    return up, tmp / 'ijptree'


def _ijp_run(tmp, up, tree):
    r = subprocess.run([sys.executable,
                        str(tmp / 'scripts' / 'compliance' / 'check_jetpack_tiers.py'),
                        str(up), str(tree)],
                       capture_output=True, text=True, cwd=tmp)
    return r.returncode, r.stdout + r.stderr


@missing_case('上游有档位而 lang 里没有对应等级名 → 必须红')
def _m9(tmp, tree):
    up, t = _ijp_fixture(
        tmp,
        [('iron', False), ('vibranium', False)],
        {'jetpack.iron.name': '铁'})
    rc, out = _ijp_run(tmp, up, t)
    return rc != 0 and 'jetpack.vibranium.name' in out


@missing_case('每个档位都有等级名 → 必须绿（证明这道闸不是一律红）')
def _m10(tmp, tree):
    up, t = _ijp_fixture(
        tmp,
        [('iron', False), ('vibranium', False)],
        {'jetpack.iron.name': '铁', 'jetpack.vibranium.name': '振金'})
    rc, out = _ijp_run(tmp, up, t)
    return rc == 0 and '2 个等级名全部有译' in out


@missing_case('等级名是空串 → 必须红（有键不等于有译）')
def _m11(tmp, tree):
    up, t = _ijp_fixture(
        tmp,
        [('iron', False)],
        {'jetpack.iron.name': '   '})
    rc, out = _ijp_run(tmp, up, t)
    return rc != 0 and 'jetpack.iron.name' in out


@missing_case('上游 config 没取到 → 等级名检查必须红，不许「没扫到所以通过」')
def _m12(tmp, tree):
    up, t = _ijp_fixture(tmp, [], {'jetpack.iron.name': '铁'}, make_config=False)
    rc, out = _ijp_run(tmp, up, t)
    return rc != 0 and 'config/ironjetpacks/jetpacks' in out


@missing_case('档位被 disable → mod 不注册它，不要求译名，必须绿')
def _m13(tmp, tree):
    up, t = _ijp_fixture(
        tmp,
        [('iron', False), ('wood', True)],
        {'jetpack.iron.name': '铁'})
    rc, out = _ijp_run(tmp, up, t)
    return rc == 0 and '1 个等级名全部有译' in out


# ── 第五组反例：任务书里的蜜蜂名 ─────────────────────────────────────────
#
# 复刻的事故：任务正文写「倒在幽灵蜜蜂蛋上」，而 JEI 里那个物品叫「恶魂蜜蜂」。
# 照着任务书搜是搜不到的。顺同一条线索机械扫描又找出三处同类（BeeBee /
# KamikazBee 留着英文原名、Shroombees 整个漏译）——一次报告只是一个表面。
#
# 夹具里的两张名字表是现造的最小表，不抄上游那 463 条。
def _bee_fixture(tmp, en_quest, zh_quest, en_names=None, zh_names=None):
    en_names = en_names or {'entity.productivebees.ghostly_bee': 'Ghostly Bee'}
    zh_names = zh_names or {'entity.productivebees.ghostly_bee': '恶魂蜜蜂'}
    mods = tmp / 'beepack' / 'mods'
    mods.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(mods / 'productivebees-1.21.1-fixture.jar', 'w') as z:
        z.writestr('assets/productivebees/lang/en_us.json',
                   json.dumps(en_names, ensure_ascii=False))
    up = tmp / 'beeup' / 'config' / 'ftbquests' / 'quests' / 'lang' / 'en_us' / 'chapters'
    up.mkdir(parents=True, exist_ok=True)
    (up / 'c.snbt').write_text('{\n\tquest.AAA.quest_desc: "%s"\n}\n' % en_quest,
                               encoding='utf-8')
    tree = tmp / 'beetree'
    zq = tree / 'config' / 'ftbquests' / 'quests' / 'lang' / 'zh_cn' / 'chapters'
    zq.mkdir(parents=True, exist_ok=True)
    (zq / 'zz_hanhua_c.snbt').write_text('{\n\tquest.AAA.quest_desc: "%s"\n}\n' % zh_quest,
                                         encoding='utf-8')
    zl = tree / 'resourcepacks' / 'ATM10汉化包' / 'assets' / 'productivebees' / 'lang'
    zl.mkdir(parents=True, exist_ok=True)
    (zl / 'zh_cn.json').write_text(json.dumps(zh_names, ensure_ascii=False),
                                   encoding='utf-8')
    return mods, tmp / 'beeup', tree


def _bee_run(tmp, mods, up, tree):
    r = subprocess.run([sys.executable,
                        str(tmp / 'scripts' / 'compliance' / 'check_bee_names_in_quests.py'),
                        str(mods), str(up), str(tree)],
                       capture_output=True, text=True, cwd=tmp)
    return r.returncode, r.stdout + r.stderr


@missing_case('任务书用了物品名之外的蜜蜂叫法 → 必须红')
def _m14(tmp, tree):
    mods, up, t = _bee_fixture(tmp,
                               'pour it over a Ghostly Bee egg',
                               '倒在幽灵蜜蜂蛋上')
    rc, out = _bee_run(tmp, mods, up, t)
    return rc != 0 and '恶魂蜜蜂' in out


@missing_case('任务书用的就是物品名 → 必须绿（证明这道闸不是一律红）')
def _m15(tmp, tree):
    mods, up, t = _bee_fixture(tmp,
                               'pour it over a Ghostly Bee egg',
                               '倒在恶魂蜜蜂蛋上')
    rc, out = _bee_run(tmp, mods, up, t)
    return rc == 0 and '全部与物品名一致' in out


@missing_case('短名落在长名里 → 不算命中，不许误报')
def _m16(tmp, tree):
    # Dragonsteel Bee 会带词边界落在 Lightning Dragonsteel Bee 里，
    # 第一版扫描器就是这么多报了一条，而「龙霆钢蜜蜂」本来是对的。
    en = {'entity.productivebees.dragonsteel_bee': 'Dragonsteel Bee',
          'entity.productivebees.lightning_dragonsteel_bee': 'Lightning Dragonsteel Bee'}
    zh = {'entity.productivebees.dragonsteel_bee': '龙钢蜜蜂',
          'entity.productivebees.lightning_dragonsteel_bee': '龙霆钢蜜蜂'}
    mods, up, t = _bee_fixture(tmp, 'Lightning Dragonsteel Bee', '龙霆钢蜜蜂', en, zh)
    rc, out = _bee_run(tmp, mods, up, t)
    return rc == 0


@missing_case('上游英文任务书没取到 → 蜜蜂名检查必须红')
def _m17(tmp, tree):
    mods, up, t = _bee_fixture(tmp, 'a Ghostly Bee', '恶魂蜜蜂')
    shutil.rmtree(up / 'config')
    rc, out = _bee_run(tmp, mods, up, t)
    return rc != 0 and 'config/ftbquests/quests/lang/en_us' in out


@missing_case('拿不到 productivebees jar → 蜜蜂名检查必须红')
def _m18(tmp, tree):
    mods, up, t = _bee_fixture(tmp, 'a Ghostly Bee', '恶魂蜜蜂')
    for jar in mods.glob('productivebees*.jar'):
        jar.unlink()
    rc, out = _bee_run(tmp, mods, up, t)
    return rc != 0 and '英文名表取不到' in out


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
