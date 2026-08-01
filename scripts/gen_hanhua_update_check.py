#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# atm10-zh-cn — All the Mods 10 简体中文汉化补丁「绿油油版」
# Copyright (C) 2026 星野夢華 (Hoshino Yumeka)
# SPDX-License-Identifier: GPL-3.0-or-later
"""给出货树中的游戏内汉化更新检查器填入补丁版本号。

源码中的 KubeJS 脚本是模板：``@@PATCHVER@@`` 必须在打包每个整合包版本时
替换成这次发布的补丁版本。这个逻辑独立出来，避免 build_dist.sh 混入难测的
内嵌 Python，也让漏复制脚本、占位符数量异常等情况立即失败。

用法:
    python3 scripts/gen_hanhua_update_check.py <补丁版本号> <出货树>
"""
import sys
from pathlib import Path


PLACEHOLDER = '@@PATCHVER@@'
RELATIVE_PATH = Path('kubejs/client_scripts/hanhua_update_check.js')


def main(version, tree):
    target = Path(tree) / RELATIVE_PATH
    if not target.is_file():
        sys.exit('❌ 出货树里缺少 %s：先确认 assemble.py 已复制更新检查脚本。'
                 % target)
    text = target.read_text(encoding='utf-8')
    count = text.count(PLACEHOLDER)
    if count != 1:
        sys.exit('❌ %s 中应恰有一个 %s，实际有 %d 个。'
                 % (target, PLACEHOLDER, count))
    target.write_text(text.replace(PLACEHOLDER, version), encoding='utf-8')
    print('游戏内更新提示：已填入补丁版本 %s' % version)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
