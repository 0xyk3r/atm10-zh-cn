#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# atm10-zh-cn — All the Mods 10 简体中文汉化补丁「绿油油版」
# Copyright (C) 2026 星野夢華 (Hoshino Yumeka)
# SPDX-License-Identifier: GPL-3.0-or-later
"""去掉任务书中文里那些从英文原文带过来的半角空格。

## 为什么

FTB Quests **在空格处断行**。中文本身不需要空格，但上游译文里留着大量英文词间
空格，每一个都是潜在的断行点，于是断在了不该断的地方：

    你开始时有 3 个基本形态         → 断成「你开始时有」/「3 个基本形态」
    一个&6抄写台&r 来为你的法术书    → 断成「……抄写台」/「来为你的法术书」
    模组包均受 &e保留所有权利&r 许可  → 断成「模组包均受」/「保留所有权利」

issue #10 里被当成 11 条独立瑕疵报上来，其实是同一个成因、几千处。
逐条存覆盖的话 delta 会暴涨，而且上游一改就得重新对齐；这里改成**构建时统一处理**，
上游怎么改都自动跟上。

## 只删两种空格，其余一律不碰

    中文 ␠ 中文          → 删       「均受 保留」→「均受保留」
    中文 ␠ 数字 ␠ 中文   → 删       「有 3 个」→「有3个」

**中西之间的空格保留**：`AllTheMods 团队`、`&a60 位阶` 是正常的中英混排排版，
删了反而挤在一起。判定时把颜色码（`&a` 这类）当透明，因为
`抄写台&r 来为` 里的空格两侧实际上都是中文。

键名、颜色码、`\\n` 转义、SNBT 结构一概不动——只可能删掉两个中日韩字符之间的空格，
而键名和标识符全是 ASCII，碰不到。

用法:
    python3 scripts/gen_quest_space_fix.py <出货树>
"""
import re
import sys
from pathlib import Path

LANG = 'config/ftbquests/quests/lang/zh_cn'
CJK = r'一-鿿　-〿＀-￯'   # 汉字 + 中文标点 + 全角符号
COL = r'(?:&[0-9a-fk-orA-FK-OR])*'                 # 颜色码，判定时透明

# ① 中文 ␠ 中文
P_CC = re.compile(r'([%s])(%s) +(%s)([%s])' % (CJK, COL, COL, CJK))
# ② 中文 ␠ 数字 ␠ 中文（两侧都有空格的短数字，如「有 3 个」）
P_CNC = re.compile(r'([%s])(%s) +(\d+) +(%s)([%s])' % (CJK, COL, COL, CJK))


def fix(text):
    n = 0
    while True:
        t2, k = P_CNC.subn(r'\1\2\3\4\5', text)
        text, n = t2, n + k
        t2, k = P_CC.subn(r'\1\2\3\4', text)
        text, n = t2, n + k
        if not k:
            break
    return text, n


def main(argv):
    if len(argv) != 2:
        print('❌ 用法: gen_quest_space_fix.py <出货树>')
        return 1
    root = Path(argv[1]) / LANG
    if not root.is_dir():
        print('❌ %s 不在 —— 任务书语言树没摊出来，这一步等于没跑' % root)
        return 1
    files = sorted(p for p in root.rglob('*') if p.is_file())
    if not files:
        print('❌ %s 下一个文件都没有' % root)
        return 1
    total = touched = 0
    for p in files:
        s = p.read_text(encoding='utf-8')
        out, n = fix(s)
        if n:
            p.write_text(out, encoding='utf-8')
            touched += 1
            total += n
    print('✅ 任务书断行：%d 个文件、共去掉 %d 处中文之间的多余空格' % (touched, total))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
