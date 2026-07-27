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
CLIENT_MIN = {
    'lang_files':   500,    # 实测 604 个 lang/*.json
    'lang_keys': 150000,    # 实测 21 万余条
    'banners':      190,    # 实测 200 张
    'buttons':       14,    # 14 张主菜单按钮
    'vp_modules':   140,    # 151 个 VaultPatcher 模块
    'quest_delta':   30,    # 34 个任务书 delta
    'gui_files':     20,    # 24 个 RFTools .gui
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

    # 安装器里的占位符必须已被打包脚本填掉
    for n in names:
        if n.endswith(('install.sh', 'install.ps1')):
            if '@@' in z.read(n).decode('utf-8', 'replace'):
                bad.append('%s 里还有未替换的 @@占位符@@' % n)

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
