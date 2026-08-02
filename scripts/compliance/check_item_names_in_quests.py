#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# atm10-zh-cn — All the Mods 10 简体中文汉化补丁「绿油油版」
# Copyright (C) 2026 星野夢華 (Hoshino Yumeka)
# SPDX-License-Identifier: GPL-3.0-or-later
"""任务书里提到某件物品时，用的必须是玩家在 JEI 里搜得到的那个名字。

## 为什么要这道闸

蜜蜂那道闸（check_bee_names_in_quests.py）证明了这个判据是机械的，但它只管
productivebees 一个命名空间。2026-08-03 的反馈说明同一个毛病在别的模组里照样有：

    任务书写「XP 果冻豆」「XP 固化机」  物品名是「经验果冻宝宝」「经验固化器」
    任务书写「空灵魂宝石」              物品名是「灵魂宝石（空）」
    任务书写「挡光玻璃」                物品名是「遮光玻璃」

前两组是反馈报上来的，第三组是这道闸自己扫出来的——**人眼看不全，必须机械化。**

## 判定

对每个任务条目：英文原文里出现某件物品的英文名 → 我们的中文里必须出现它的中文名。

英文名取自模组 jar 的 `en_us.json`，中文名取**出货树里实际生效的那一份**：
我们的资源包盖过模组自带（`resourcepacks/ATM10汉化包/assets/<ns>/lang/zh_cn.json`
优先，没有才回退 jar 自带）。判据必须跟玩家看到的一致，所以不能只读 jar。

**最长匹配优先**：`Soul Gem` 会落在 `Empty Soul Gem` 里，不排掉就会误报。
某条英文名命中时，若同一段文字里还命中了包含它的更长的名字，这条不算。

但只比对本表里的名字是不够的——第一版就这么误报了两条：

    Wither Skeleton Skull   套着 occultism 的 Skeleton Skull（长名是原版的，不在表里）
    Glass Divination Rod    套着 occultism 的 Divination Rod（长名是同模组另一个键，
                            但那个键的中文里本来就含短名的中文，判不出来）

还有一条：**匹配大小写敏感**。Relics 有件遗物叫 `Falling Star`，而任务正文里
`call down a falling star` 是普通名词——不区分大小写就会把它当成提到了那件遗物。
上游偶尔会把物品名写成小写，那样这条就漏判，但漏判好过误报。

所以再加一道守卫：**命中处前面紧跟一个大写词的，不算独立提及**。
`the cheapest Divination Rod` 里 `cheapest` 是小写，照样判；`&8Wither Skeleton Skull`
和 `the Glass Divination Rod` 里前一个词是大写，跳过。一段文字里所有命中位置
都被这条挡掉，才算这条名字没被提及——宁可漏报，不许拿判不了的事去红。

**一名多物，而且跨模组**：同一个英文名可能对应多件东西。静态判不出正文说的是哪一件，
所以命中任意一个中文名就算过——宁可漏报，不许拿判不了的事去红。

这一条必须**跨整包**算，只在单个命名空间里合并是不够的：`Rotten Egg` 在
mob_grinding_utils 和 iceandfire 里各有一件（腐烂鸡蛋 / 烂鸡蛋），而鸡蛇那条任务
说的是冰与火那件。只按 MGU 判，闸会理直气壮地要求把它改成另一个模组的物品名。
所以候选中文名和「更长的名字」都取**全包所有模组**的并集，`NAMESPACES` 只决定
「哪些模组的名字要被强制检查」。

## 为什么按 jar 内容找 jar，而不是取排序最后一个

`occultism*.jar` 在 ATM10 里匹配到两个文件，其中一个根本没有 `assets/` ——
按文件名排序取最后一个会拿到空的那个，于是「0 对名字」静默通过。
这里改成**扫所有 jar、谁真有这个命名空间的 lang 就用谁**，并且一个都没找到就红。

## fail-closed

拿不到 jar、读不到英文表、找不到中文表、上游英文任务书目录不在、某个模组一对名字都
配不上、两棵树一个键都对不上——全部当红。这道闸最没用的失败形态就是「没扫到所以通过」。

用法:
    python3 scripts/compliance/check_item_names_in_quests.py <mods 目录> <上游树> <出货树>
"""
import json
import re
import sys
import zipfile
from pathlib import Path

# 纳入这道闸的命名空间。加一个模组进来之前先本地跑一遍：报出来的必须条条是真错，
# 否则说明该模组的名字表不适合当判据（比如物品名是常用词），不许为了「多扫点」硬加。
NAMESPACES = ('mob_grinding_utils', 'occultism', 'relics')

PACK_ZH = 'resourcepacks/ATM10汉化包/assets/%s/lang/zh_cn.json'
EN_QUESTS = 'config/ftbquests/quests/lang/en_us'
ZH_QUESTS = 'config/ftbquests/quests/lang/zh_cn'
NAME_KEY = ('item.', 'block.', 'fluid.', 'entity.')
KEY = re.compile(r'^[\t ]+([A-Za-z0-9_.]+):\s*(.*)$')
# 太短的英文名（Bee、Jar、Egg 之类）拿去全文搜必然满地假阳性，判不了就不判。
MIN_LEN = 6


def die(msg):
    print('❌ %s' % msg)
    sys.exit(1)


def load_json(z, name):
    try:
        return json.loads(z.read(name), strict=False)   # 少数 mod 的 lang 里有裸控制符
    except Exception:
        return None


def pack_zh(tree):
    """我们资源包里每个命名空间的 zh_cn（盖过模组自带）。"""
    out = {}
    for p in sorted(Path(tree).glob(PACK_ZH % '*')):
        try:
            out[p.parts[-3]] = json.loads(p.read_text(encoding='utf-8'))
        except Exception as e:
            die('%s 解析失败：%s' % (p, e))
    return out


def collect(mods, tree):
    """扫全包：→ (英文名 -> 可接受的中文名集合, 被强制检查的英文名集合)。"""
    ours = pack_zh(tree)
    names, enforced = {}, set()
    seen_ns = set()
    for jar in sorted(Path(mods).glob('*.jar')):
        try:
            z = zipfile.ZipFile(jar)
        except Exception:
            continue
        with z:
            for n in z.namelist():
                if not n.endswith('/lang/en_us.json'):
                    continue
                ns = n.split('/')[1]
                en = load_json(z, n)
                if not isinstance(en, dict):
                    continue
                zh = dict(load_json(z, n.replace('en_us', 'zh_cn')) or {})
                zh.update(ours.get(ns, {}))       # 我们的包盖在模组自带之上
                seen_ns.add(ns)
                for k, e in en.items():
                    # count==2 → 只要 item.<ns>.<id> 这种纯名字键，
                    # 把 .tooltip_1 / .jei.info 这类描述排掉
                    if not (k.startswith(NAME_KEY) and k.count('.') == 2):
                        continue
                    c = zh.get(k)
                    if not (isinstance(e, str) and len(e) >= MIN_LEN):
                        continue
                    if '%' in e or not WORD.match(e):
                        continue          # `%s Spawner` 这类格式串不是名字
                    if not (isinstance(c, str) and c.strip()):
                        continue
                    names.setdefault(e, set()).add(c)
                    if ns in NAMESPACES:
                        enforced.add(e)
    missing = [ns for ns in NAMESPACES if ns not in seen_ns]
    if missing:
        die('%s 里没有任何 jar 含这些命名空间的 en_us.json：%s —— 这道闸对它们等于没跑'
            % (mods, '、'.join(missing)))
    if not enforced:
        die('要检查的命名空间（%s）一对「英文名→中文名」都没配上 —— 判不了'
            % '、'.join(NAMESPACES))
    return names, enforced


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


# 颜色码和转义换行会把词边界吃掉：`&8Wither` 里 `8` 和 `W` 都是 \w，
# `\bWither` 根本匹配不上 —— 于是长名匹配不到、短名 `Skeleton Skull` 漏出来当误报。
# 匹配前先把它们换成空格。（换完偏移会变，所以下面一律在规范化后的文本上算。）
#
# **非法**颜色码也要剥。ATM 的任务书里真有 `&zRainbow Plating` 这种 —— `&z` 不是
# 合法格式符，只按合法表剥的话 `z` 会紧贴 `Rainbow`，整条静默漏判。
NOISE = re.compile(r'[&§](?:#[0-9A-Fa-f]{6}|[0-9A-Za-z])|\\+n')
# 命中处前面紧跟的大写词 —— 说明正文说的是一件更长名字的东西，不是本条。
LEADING_CAP = re.compile(r'[A-Z][a-zA-Z]*\s+$')


def norm(text):
    return NOISE.sub(' ', text)


WORD = re.compile(r'\w+')
SPACE = re.compile(r'[\s\u00a0]+')


def found_names(text, by_first):
    """正文里**独立**提到的所有名字。

    全包两万条名字 × 八千段任务文本，逐条跑正则是分钟级的。改成按首词建索引：
    只在正文里每个单词的位置上，试那些以这个词开头的名字。

    最长匹配必须**按出现位置**算，不能按整段算。`The cheapest Divination Rod, the
    Glass Divination Rod.` 里两个名字都出现了；按整段排，短名会被长名整条吃掉，
    这条真错就静默漏判了。所以只有**被某个更长匹配的区间盖住的那一次出现**不算。
    """
    spans = []
    for m in WORD.finditer(text):
        for name in by_first.get(m.group(0), ()):
            s = m.start()
            e = s + len(name)
            if not text.startswith(name, s):
                continue
            if e < len(text) and (text[e].isalnum() or text[e] == '_'):
                continue                      # 右边界：Piglin 不算命中 Piglins
            spans.append((s, e, name))
    hits = set()
    for s, e, name in spans:
        if any(s2 <= s and e2 >= e and e2 - s2 > e - s for s2, e2, _ in spans):
            continue                          # 这一次出现嵌在更长的名字里
        if LEADING_CAP.search(text[max(0, s - 40):s]):
            continue                          # 更长的名字不在表里（原版物品等）时的兜底
        hits.add(name)
    return hits


def mismatches(names, enforced, up, ours, common):
    by_first = {}
    for e in names:
        by_first.setdefault(WORD.match(e).group(0), []).append(e)
    bad = []
    for k in common:
        text, mine = norm(up[k]), ours[k]
        # 「更长的名字」要拿全包的名字表来排，只看被检查的那几个模组会漏
        for e in found_names(text, by_first):
            if e not in enforced:
                continue
            cs = names[e]
            # 比较时抹掉空白：物品名「16k 存储元件」与正文里的「16k存储元件」
            # 是同一个东西，不该因为一个空格判红
            if not any(SPACE.sub('', c) in SPACE.sub('', mine) for c in cs):
                bad.append((k, e, '／'.join(sorted(cs))))
    return bad


def main(argv):
    if len(argv) != 4:
        die('用法: check_item_names_in_quests.py <mods 目录> <上游树> <出货树>')
    mods, uproot, tree = argv[1], Path(argv[2]), Path(argv[3])

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

    names, enforced = collect(mods, tree)
    bad = mismatches(names, enforced, up, ours, common)

    if bad:
        print('❌ 任务书里的物品名跟游戏内物品名对不上（玩家照任务书去 JEI 搜会搜不到）：')
        for k, e, c in sorted(bad):
            print('   %-40s 英文 %-24s 中文应出现 %s' % (k, e, c))
        return 1
    print('✅ %s：%d 条任务文本、%d 个物品名当参照，强制检查 %d 个（%s），全部一致'
          % (tree, len(common), len(names), len(enforced), '、'.join(NAMESPACES)))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
