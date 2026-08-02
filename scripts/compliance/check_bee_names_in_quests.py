#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# atm10-zh-cn — All the Mods 10 简体中文汉化补丁「绿油油版」
# Copyright (C) 2026 星野夢華 (Hoshino Yumeka)
# SPDX-License-Identifier: GPL-3.0-or-later
"""任务书里提到某只蜜蜂时，用的必须是玩家在 JEI 里搜得到的那个名字。

## 为什么要这道闸

2026-08-02 玩家截图：任务正文写「倒在**幽灵蜜蜂**蛋上」，而 JEI 里那个物品叫
**恶魂蜜蜂**。照着任务书搜是搜不到的——这比漏翻难受得多，漏翻至少能拿英文去搜。

顺着同一条线索机械地扫了一遍，同类的还有：正文里直接留着 `BeeBee`、`KamikazBee`
两个英文原名（物品名是「蜂蜂」「“神风特攻队”蜜蜂」），以及英文的
`Ghostly Bee or Shroombees` 在中文里把 Shroombees 整个漏掉了。
**一次报告 = 一个表面，剩下三个是扫出来的。** 所以这件事不能靠人眼。

## 判定

对每个任务条目：英文原文里出现某只蜜蜂的英文名 → 我们的中文里必须出现它的中文名。

英文名取自 productivebees 的 `en_us.json`，中文名取自本包资源包的 `zh_cn.json`
（同一个键，所以是一一对应，不靠猜）。

**最长匹配优先**：`Dragonsteel Bee` 会带着词边界落在 `Lightning Dragonsteel Bee`
里边，不排掉就会误报——第一版扫描器就是这么多报了一条，而「龙霆钢蜜蜂」本来是对的。
所以某条英文名命中时，若同一段文字里还命中了包含它的更长的名字，这条不算。

## fail-closed

拿不到 jar、读不到两张表、上游英文任务书目录不在、一个任务条目都没对上——全部当红。
这道闸最没用的失败形态就是「没扫到东西所以通过」。

用法:
    python3 scripts/compliance/check_bee_names_in_quests.py <mods 目录> <上游树> <出货树>
"""
import json
import re
import sys
import zipfile
from pathlib import Path

EN_LANG = 'assets/productivebees/lang/en_us.json'
ZH_LANG = 'resourcepacks/ATM10汉化包/assets/productivebees/lang/zh_cn.json'
EN_QUESTS = 'config/ftbquests/quests/lang/en_us'
ZH_QUESTS = 'config/ftbquests/quests/lang/zh_cn'
KEY = re.compile(r'^[\t ]+([A-Za-z0-9_.]+):\s*(.*)$')
# 太短的英文名（Bee、Egg 之类）拿去全文搜必然满地假阳性，判不了就不判。
MIN_LEN = 6


def die(msg):
    print('❌ %s' % msg)
    sys.exit(1)


def bee_names(mods, tree):
    jars = sorted(Path(mods).glob('productivebees*.jar'))
    if not jars:
        die('%s 里没有 productivebees 的 jar —— 英文名表取不到，这道闸等于没跑' % mods)
    try:
        with zipfile.ZipFile(jars[-1]) as z:
            en = json.loads(z.read(EN_LANG))
    except Exception as e:
        die('%s 里读不出 %s：%s' % (jars[-1].name, EN_LANG, e))
    zp = Path(tree) / ZH_LANG
    if not zp.is_file():
        die('%s 不在 —— 资源包没摊出来' % zp)
    try:
        zh = json.loads(zp.read_text(encoding='utf-8'))
    except Exception as e:
        die('%s 解析失败：%s' % (zp, e))

    pairs = [(en[k], zh[k]) for k in en
             if k.startswith('entity.productivebees.') and k in zh
             and isinstance(en[k], str) and len(en[k]) >= MIN_LEN
             and isinstance(zh[k], str) and zh[k].strip()]
    if not pairs:
        die('一对「英文名→中文名」都没配上 —— 两张表对不上，判不了')
    return pairs


def quest_text(root):
    """把一棵任务书语言树读成 键 -> 全文（多行数组拼成一串，只为查词）。"""
    out = {}
    for p in sorted(Path(root).rglob('*.snbt*')):
        cur = None
        for line in p.read_text(encoding='utf-8', errors='replace').split('\n'):
            m = KEY.match(line)
            if m:
                cur = m.group(1)
                out[cur] = out.get(cur, '') + m.group(2)
            elif cur:
                out[cur] = out.get(cur, '') + line
    return out


def main(argv):
    if len(argv) != 4:
        die('用法: check_bee_names_in_quests.py <mods 目录> <上游树> <出货树>')
    mods, uproot, tree = argv[1], Path(argv[2]), Path(argv[3])
    pairs = bee_names(mods, tree)

    if not (uproot / EN_QUESTS).is_dir():
        die('上游树里没有 %s —— 英文原文取不到，无从判断译名对不对（树: %s）'
            % (EN_QUESTS, uproot))
    up = quest_text(uproot / EN_QUESTS)
    ours = quest_text(tree / ZH_QUESTS)
    if not up:
        die('%s 里一条任务文本都没读到' % (uproot / EN_QUESTS))
    if not ours:
        die('%s 里一条任务文本都没读到 —— 出货树没摊好' % (tree / ZH_QUESTS))

    common = [k for k in up if k in ours]
    if not common:
        die('英文与中文一个键都对不上 —— 两棵树不是同一版，判了也没意义')

    hits = []
    for k in common:
        text, mine = up[k], ours[k]
        found = [(e, c) for e, c in pairs
                 if re.search(r'\b' + re.escape(e) + r'\b', text, re.I)]
        for e, c in found:
            # 最长匹配优先：短名落在长名里不算命中
            if any(len(e2) > len(e) and e.lower() in e2.lower() for e2, _ in found):
                continue
            if c not in mine:
                hits.append((k, e, c))

    if hits:
        print('❌ 任务书里的蜜蜂名跟物品名对不上（玩家照任务书去 JEI 搜会搜不到）：')
        for k, e, c in sorted(hits):
            print('   %-42s 英文 %-24s 中文应出现 %s' % (k, e, c))
        return 1
    print('✅ %s：%d 条任务文本对过 %d 个蜜蜂名，全部与物品名一致'
          % (tree, len(common), len(pairs)))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
