#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# atm10-zh-cn — All the Mods 10 简体中文汉化补丁「绿油油版」
# Copyright (C) 2026 星野夢華 (Hoshino Yumeka)
# SPDX-License-Identifier: GPL-3.0-or-later
"""把 src/ 里的真源摊成一棵出货树（build/common/）。

仓库里不存在 `resourcepacks/`、`kubejs/`、`config/` 这些目录——它们是**产物**，
每次构建现摊。这样就不可能出现「仓库里躺着一份手改过、和生成器输出对不上的文件」。

摊完之后再跑生成器（横幅、奖杯名、按钮…），它们直接往这棵树里写。
版本专属的上游文件由 gen_upstream_patches.py 单独产到 build/upstream/<版本>/。

用法:
    python3 scripts/assemble.py
"""
import shutil
import sys

from paths import COMMON, PACK, PACK_NAME, SRC

# src 下的目录 → 出货树里的位置
LAYOUT = [
    ('pack', 'resourcepacks/' + PACK_NAME),
    ('config', 'config'),
    ('kubejs', 'kubejs'),
    ('vaultpatcher', 'vaultpatcher'),
    ('mods', 'mods'),
    ('可选mods-拼音搜索', '可选mods-拼音搜索'),
]

# 这些路径是生成器的产物，绝不该出现在 src/ 里。出现了就说明有人把产物提交了。
FORBIDDEN_IN_SRC = [
    'pack/assets/atm/textures/questpics',
    'pack/assets/hanhua_trophies',
    'pack/assets/hanhua_wood_names',
    'kubejs/client_scripts/pb_hanhua_tooltip.js',
    'kubejs/server_scripts/pb_hanhua_cage_migrate.js',
    'config/fancymenu/assets',
]


def main():
    bad = [p for p in FORBIDDEN_IN_SRC if (SRC / p).exists()]
    if bad:
        sys.exit('❌ src/ 里出现了生成物，必须删掉（它们由 generate_all.sh 现产）：\n  '
                 + '\n  '.join('src/' + b for b in bad))

    if COMMON.exists():
        shutil.rmtree(COMMON)
    n = 0
    for name, dest in LAYOUT:
        s = SRC / name
        if not s.is_dir():
            sys.exit('❌ 缺 src/%s' % name)
        d = COMMON / dest
        d.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(s, d, ignore=shutil.ignore_patterns('.DS_Store'))
        n += sum(1 for _ in d.rglob('*') if _.is_file())
    print('已摊出货树: %s（%d 个文件）' % (COMMON, n))
    print('  资源包源目录: %s' % PACK)


if __name__ == '__main__':
    main()
