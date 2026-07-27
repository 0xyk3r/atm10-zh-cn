#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# atm10-zh-cn — All the Mods 10 简体中文汉化补丁「绿油油版」
# Copyright (C) 2026 星野夢華 (Hoshino Yumeka)
# SPDX-License-Identifier: GPL-3.0-or-later
"""打完包之后，拆开 zip 逐项核内容——**发版前的最后一道闸**。

## 为什么必须有

汉化产物已经不入 git，改由构建时生成。这带来一个新的失败模式：
生成器悄悄少产出了、或者压根没跑，打出来的包**结构完整但里面没有汉化**，
上传、发版、玩家下载，一路没有任何东西报错。

`build_dist.sh` 开头那道守卫只查「文件在不在」。**在 ≠ 对**：
一个 0 字节的 lang 文件、一张纯透明的横幅、一个只剩 3 条键的资源包，
都能通过存在性检查。所以这里查的是**量**：每一项都对着实测值设了下限，
少于下限就说明这一环生成失败了。

阈值取实测值的八成左右，留出上游增删的正常波动，但拦得住「整块没了」。

用法:
    python3 scripts/verify_dist.py dist/atm10-zh_cn-client-r12-atm7.2.zip
    python3 scripts/verify_dist.py dist/*.zip
"""
import io
import json
import re
import sys
import zipfile

# 客户端包的下限（实测值见注释）
# 下限一律取实测值的九成上下：留出上游增删的正常波动，但拦得住「整块没了」。
# 2026-07-27 清掉底本带来的死重后重新校准（那 236 个 lang 对应的模组
# 在 7.0/7.1/7.2 三版 jar 里都不存在，永远加载不到）：
#   lang 598 → 362 个文件、21.2 万 → 17.7 万键；导览书 1709 → 1683 个
CLIENT_MIN = {
    'lang_files':   330,    # 实测 362 个 lang/*.json
    'lang_keys': 160000,    # 实测 17.7 万条
    'banners':      190,    # 实测 200 张
    'buttons':       14,    # 14 张主菜单按钮
    'vp_modules':   140,    # 152 个 VaultPatcher 模块
    'quest_delta':   30,    # 34 个任务书 delta
    'gui_files':     20,    # 24 个 RFTools .gui
    'book_files':  1500,    # 实测 1683 个导览书文件（patchouli / ae2guide / oracle-index）
}
SERVER_MIN = {
    'vp_modules':    10,
    'quest_delta':   30,
}


def inner_pack(z):
    """客户端包里那个资源包 zip"""
    for n in z.namelist():
        if '/resourcepacks/' in n and n.endswith('.zip'):
            return n, zipfile.ZipFile(io.BytesIO(z.read(n)))
    return None, None


def check(path):
    z = zipfile.ZipFile(path)
    names = z.namelist()
    is_client = any('/resourcepacks/' in n for n in names)
    bad = []
    got = {}

    got['vp_modules'] = sum(1 for n in names if '/vaultpatcher/modules/' in n and n.endswith('.json'))
    got['quest_delta'] = sum(1 for n in names
                             if '/quests/lang/zh_cn' in n and n.endswith('.snbt'))

    if is_client:
        pname, pz = inner_pack(z)
        if pz is None:
            return ['没有资源包 zip'], {}, True
        pn = pz.namelist()
        lang = [n for n in pn if re.fullmatch(r'assets/[^/]+/lang/zh_cn\.json', n)]
        got['lang_files'] = len(lang)
        keys = 0
        for n in lang:
            try:
                keys += len(json.loads(pz.read(n).decode('utf-8-sig')))
            except Exception:
                bad.append('%s 不是合法 JSON' % n)
        got['lang_keys'] = keys
        got['banners'] = sum(1 for n in pn if '/questpics/' in n and n.endswith('.png'))
        got['gui_files'] = sum(1 for n in pn if n.endswith('.gui'))
        got['book_files'] = sum(1 for n in pn if 'patchouli_books' in n
                                or 'ae2guide' in n or 'oracle-index' in n)
        got['buttons'] = sum(1 for n in names
                             if '/config/fancymenu/assets/' in n and n.endswith('.png'))
        # 资源包描述里的版本号要和文件名对得上
        try:
            desc = json.loads(pz.read('pack.mcmeta'))['pack']['description']
        except Exception:
            desc = ''
            bad.append('pack.mcmeta 读不出来')
        mc = re.search(r'-atm([0-9.]+)\.zip$', str(path))
        if mc and mc.group(1) not in desc:
            bad.append('pack.mcmeta 描述 %r 与文件名里的 atm%s 对不上' % (desc, mc.group(1)))
        if '@@' in desc:
            bad.append('pack.mcmeta 里的占位符没被替换: %r' % desc)
        if mc and ('汉化包-%s.zip' % mc.group(1)) not in pname:
            bad.append('资源包文件名 %r 与 atm%s 对不上' % (pname, mc.group(1)))

    # 占位符必须已被打包脚本填掉。查**包里全部文本文件**，不只是安装器——
    # 曾经只查 install.sh/ps1，结果 SERVER.md 里那句「适用于 ATM10 7.2 专用服务器」
    # 是写死的，7.0 / 7.1 的包里也印着 7.2，玩家报上来才发现。
    TEXT = ('.sh', '.ps1', '.bat', '.md', '.txt', '.json', '.snbt', '.js', '.mcmeta', '.url')
    # 这几份项目文档是**原样**分发的，不是模板；它们正文里会提到占位符本身
    # （CHANGELOG 就在讲这套机制），不能拿它们当漏填。
    VERBATIM = ('README.md', 'CHANGELOG.md', 'CONTRIBUTING.md', 'LICENSE',
                '致谢与技术说明.md')
    for n in names:
        if not n.endswith(TEXT) or n.rsplit('/', 1)[-1] in VERBATIM:
            continue
        body = z.read(n).decode('utf-8', 'replace')
        m = re.search(r'@@[A-Z_]+@@', body)
        if m:
            bad.append('%s 里还有未替换的占位符 %s' % (n, m.group(0)))

    for k, lo in (CLIENT_MIN if is_client else SERVER_MIN).items():
        v = got.get(k, 0)
        if v < lo:
            bad.append('%s 只有 %d，低于下限 %d —— 这一环多半没生成' % (k, v, lo))
    return bad, got, is_client


def main(paths):
    fail = 0
    for p in paths:
        bad, got, is_client = check(p)
        tag = '客户端' if is_client else '服务端'
        if bad:
            fail += 1
            print('❌ %s [%s]' % (p, tag))
            for b in bad:
                print('     ', b)
        else:
            print('✅ %s [%s]  %s' % (p, tag,
                  '  '.join('%s=%s' % (k, v) for k, v in sorted(got.items()))))
    if fail:
        sys.exit('\n❌ %d 个包没通过内容核验——**不要发布**' % fail)
    print('\n全部通过内容核验')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1:])
