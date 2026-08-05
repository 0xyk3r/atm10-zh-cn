#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# atm10-zh-cn — All the Mods 10 简体中文汉化补丁「绿油油版」
# Copyright (C) 2026 星野夢華 (Hoshino Yumeka)
# SPDX-License-Identifier: GPL-3.0-or-later
"""去掉任务书中文里那些从英文原文带过来的半角空格。

## 为什么

FTB Quests **在空格处断行**：MC 的 `StringSplitter` 一旦在本行见过空格，行宽溢出时
就回退到那个空格断开。于是中文段落里任何一个半角空格都是潜在的断行点，而且断出来
的是**半截空行**，比按字符硬断难看得多：

    你开始时有 3 个基本形态          → 断成「你开始时有」/「3 个基本形态」
    这些生物会失去全部 AI，          → 断成「……会失去全部」/「AI，基本就和……」
    护符碎片来自 Reliquary，         → 断成「护符碎片来自」/「Reliquary，可以……」
    每颗发酵蛛眼会让这个数值上下调整 1 → 断成「……上下调整」/「1，最高可到 16。」

issue #10 报了 11 条、issue #11 又报了 9 条，全是同一个成因、几千处。逐条存覆盖的话
delta 会暴涨，上游一改还得重新对齐；所以放在构建时统一处理，上游怎么改都自动跟上。

## 规则只有一条：空格挨着中文就删

    空格左邻或右邻是中日韩字符（含中文标点、全角符号、中文引号/破折号/省略号）→ 删

两侧都是 ASCII 的空格一律不动，所以 `Just Enough Items`、`quest.XXX.quest_desc: [`
这些原样保留；键名、颜色码、`\\n` 转义、SNBT 结构一概碰不到。判定时把颜色码
（`&a` 这类）当透明，因为 `抄写台&r 来为` 里的空格两侧实际上都是中文。

## 「中西之间的空格保留」这条曾经在，是错的

修 issue #10 时这里只删「中文␠中文」和「中文␠数字␠中文」，中西之间的空格
（`AllTheMods 团队`、`失去全部 AI`）作为正常的中英混排排版特意留着。issue #11 的
九条断行反例证明那条线划错了：留下的每一个都是断行点，而排版上的收益只是一个窄
缝。中文 MC 汉化里不加这个空格是常态，断出半截空行不是。

**治不了的那一半**：中文标点落在行首（「……什么颜色」/「、几支纱……」）。MC 的
换行器没有禁则处理，删空格反而会让行填得更满、更容易撞上。这是引擎限制，只能靠
改写句子回避，不在本脚本职责内。

用法:
    python3 scripts/gen_quest_space_fix.py <出货树>
"""
import re
import sys
from pathlib import Path

LANG = 'config/ftbquests/quests/lang/zh_cn'
# 汉字（含扩展 A）+ 中文标点 + 全角符号 + 中文文本里常用的那几个西文区标点
CJK = ('—‘’“”…'
       '　-〿㐀-䶿一-鿿＀-￯')
COL = r'(?:&[0-9a-fk-orA-FK-OR])*'                 # 颜色码，判定时透明

# 左邻是中文 / 右邻是中文，各删一遍，循环到不动为止
P_L = re.compile(r'([%s])(%s) +(%s)' % (CJK, COL, COL))
P_R = re.compile(r'(%s) +(%s)([%s])' % (COL, COL, CJK))


def fix(text):
    n = 0
    while True:
        k = 0
        text, c = P_L.subn(r'\1\2\3', text)
        k += c
        text, c = P_R.subn(r'\1\2\3', text)
        k += c
        n += k
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
    print('✅ 任务书断行：%d 个文件、共去掉 %d 处紧挨中文的半角空格' % (touched, total))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
