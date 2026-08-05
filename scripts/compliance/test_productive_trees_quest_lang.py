#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# atm10-zh-cn — All the Mods 10 简体中文汉化补丁「绿油油版」
# Copyright (C) 2026 0xyk3r
# Copyright (C) 2026 星野夢華 (Hoshino Yumeka)
# SPDX-License-Identifier: GPL-3.0-or-later
"""资源树育种公式生成器的反例测试。

每条复刻一种「本该红却可能悄悄放行」的情形。写了闸不等于有闸——
一道从没被触发过的闸和没有闸是一回事。

全部用合成 jar 与合成包目录，不读真整合包：这套测试要能在 PR 阶段秒跑。

    python3 scripts/compliance/test_productive_trees_quest_lang.py
"""
import json
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))

import gen_productive_trees_quest_lang as g                      # noqa: E402
from gen_productive_trees_quest_lang import (                    # noqa: E402
    DataError, generate, generate_all, ownership_issues, render,
)

POLL, MUTATION, LOOT, MACHINE = (c * 16 for c in 'ABCD')

# 章节结构：四个任务。POLL / MUTATION 各产一棵树苗；LOOT 也产树苗，但它的英文
# 副标题是来源说明；MACHINE 压根不产树苗。
CHAPTER = '{\n\tquests: [\n' + '\n'.join(
    '\t\t{\n\t\t\tid: "%s"\n\t\t\ttasks: [{\n\t\t\t\tid: "%s"\n'
    '\t\t\t\titem: { count: 1, id: "%s" }\n\t\t\t\ttype: "item"\n\t\t\t}]\n\t\t}'
    % (q, str(i) * 16, item) for i, (q, item) in enumerate((
        (POLL, 'productivetrees:hybrid_sapling'),
        (MUTATION, 'productivetrees:mutated_sapling'),
        (LOOT, 'productivetrees:loot_sapling'),
        (MACHINE, 'productivetrees:sawmill'),
    ), 1)) + '\n\t]\n}\n'

QUEST_LANG = (
    '{\n'
    '\tquest.%s.quest_subtitle: "Parent + Oak/Other"\n'
    '\tquest.%s.title: "Hybrid Sapling"\n'
    '\tquest.%s.quest_subtitle: "Source + Luck"\n'
    '\tquest.%s.title: "Mutated Sapling"\n'
    '\tquest.%s.quest_subtitle: "Ancient City Chests"\n'
    '\tquest.%s.quest_subtitle: "I Wood too"\n'
    '\tquest.%s.title: "Sawmill"\n'
    '}\n' % (POLL, POLL, MUTATION, MUTATION, LOOT, MACHINE, MACHINE))

ZH = {
    'block.productivetrees.hybrid_sapling': '杂交树树苗',
    'block.productivetrees.mutated_sapling': '突变树树苗',
    'block.productivetrees.loot_sapling': '战利品树树苗',
    'block.productivetrees.parent_sapling': '亲本树苗',
    'block.productivetrees.other_sapling': '另一树树苗',
    'block.productivetrees.source_sapling': '源树树苗',
}


def make_jar(path, extra_tree=False):
    def pollination(result, a, b):
        return {'type': 'productivetrees:tree_pollination',
                'result': {'id': result},
                'leafA': [{'item': x} for x in a],
                'leafB': [{'item': x} for x in b]}

    trees = {'source': {'mutation_info': {'target': 'productivetrees:mutated',
                                          'chance': 0.05}}}
    if extra_tree:
        trees['newcomer'] = {}
    with zipfile.ZipFile(path, 'w') as z:
        z.writestr('data/productivetrees/recipe/pollination/hybrid.json',
                   json.dumps(pollination('productivetrees:hybrid_sapling',
                                          ['productivetrees:parent_leaves'],
                                          ['minecraft:oak_leaves',
                                           'productivetrees:other_leaves'])))
        z.writestr('data/productivetrees/recipe/pollination/loot.json',
                   json.dumps(pollination('productivetrees:loot_sapling',
                                          ['productivetrees:parent_leaves'],
                                          ['minecraft:birch_leaves'])))
        z.writestr('data/productivetrees/trees.json', json.dumps(trees))
        z.writestr('assets/productivetrees/lang/en_us.json', json.dumps({
            'block.productivetrees.hybrid_sapling': 'Hybrid Sapling',
            'block.productivetrees.mutated_sapling': 'Mutated Sapling',
            'block.productivetrees.loot_sapling': 'Loot Sapling'}))


def make_pack(root, version, extra_tree=False, quest_lang=QUEST_LANG):
    """摆一个最小 build/packsrc/<版本>/ 与配套的 versions/db/<版本>/jars.json。"""
    jar = 'productivetrees-1.21.1-%s.jar' % ('1.0.0' if extra_tree else '0.8.1')
    pack = root / 'build' / 'packsrc' / version
    (pack / 'mods').mkdir(parents=True, exist_ok=True)
    make_jar(pack / 'mods' / jar, extra_tree)
    for rel, text in ((g.CHAPTER, CHAPTER), (g.EN_QUEST, quest_lang)):
        (pack / rel).parent.mkdir(parents=True, exist_ok=True)
        (pack / rel).write_text(text, encoding='utf-8')
    db = root / 'versions' / 'db' / version
    db.mkdir(parents=True, exist_ok=True)
    (db / 'jars.json').write_text(json.dumps({'jars': {jar: {
        'projectID': 867074, 'fileID': 1, 'sha256': 'x', 'size': 1}}}),
        encoding='utf-8')
    (root / 'versions' / version).mkdir(parents=True, exist_ok=True)
    return pack


def in_sandbox(tmp, fn):
    """把生成器的 ROOT / PACKSRC 临时指进沙盒，跑完还原。"""
    saved = (g.ROOT, g.PACKSRC)
    g.ROOT, g.PACKSRC = tmp, tmp / 'build' / 'packsrc'
    try:
        return fn()
    finally:
        g.ROOT, g.PACKSRC = saved


CASES = []


def case(name):
    def deco(fn):
        CASES.append((name, fn))
        return fn
    return deco


@case('只输出能被数据证明归生成器管的字段')
def t_scope(tmp):
    make_jar(tmp / 'pt.jar')
    v = generate(CHAPTER, QUEST_LANG, tmp / 'pt.jar', dict(ZH))
    return (v.get('quest.%s.quest_subtitle' % POLL) == '亲本 + 橡木/另一树'
            and v.get('quest.%s.quest_subtitle' % MUTATION) == '源树 + 运气'
            and v.get('quest.%s.title' % POLL) == '杂交树树苗'
            and v.get('quest.%s.title' % MUTATION) == '突变树树苗'
            # 来源说明、机器双关、机器标题都归人写，一个都不许被吃掉
            and 'quest.%s.quest_subtitle' % LOOT not in v
            and 'quest.%s.quest_subtitle' % MACHINE not in v
            and 'quest.%s.title' % MACHINE not in v
            and not any(k.endswith('.quest_desc') for k in v))


@case('树苗中文名不以「树苗」结尾 → 必须红')
def t_bad_suffix(tmp):
    make_jar(tmp / 'pt.jar')
    zh = dict(ZH, **{'block.productivetrees.parent_sapling': '亲本'})
    try:
        generate(CHAPTER, QUEST_LANG, tmp / 'pt.jar', zh)
    except DataError as e:
        return '必须严格以「树苗」结尾' in str(e)
    return False


@case('中文 lang 缺了某个父本 → 必须红，不许把它留空混过去')
def t_missing_zh(tmp):
    make_jar(tmp / 'pt.jar')
    zh = {k: v for k, v in ZH.items() if k != 'block.productivetrees.other_sapling'}
    try:
        generate(CHAPTER, QUEST_LANG, tmp / 'pt.jar', zh)
    except DataError as e:
        return '缺少有效的' in str(e)
    return False


@case('生成键还被手写 delta 攥着 → 三条都要报出来')
def t_ownership(tmp):
    make_jar(tmp / 'pt.jar')
    values = generate(CHAPTER, QUEST_LANG, tmp / 'pt.jar', dict(ZH))
    root = tmp / 'delta'
    root.mkdir()
    (root / 'zz_hanhua_manual.snbt').write_text(
        '{\n\tquest.%s.title: "杂交树树苗"\n\tquest.%s.title: "突变树树苗"\n'
        '\tquest.%s.quest_subtitle: "旧公式"\n}\n' % (POLL, MUTATION, POLL),
        encoding='utf-8')
    issues = ownership_issues(values, root, root / 'zz_hanhua_generated.snbt')
    return len(issues) == 3 and all('仍由手写文件' in i for i in issues)


@case('渲染结果形状稳定，且只含生成键')
def t_render(tmp):
    make_jar(tmp / 'pt.jar')
    text = render(generate(CHAPTER, QUEST_LANG, tmp / 'pt.jar', dict(ZH)))
    return (text.startswith('{\n\tquest.') and text.endswith('\n}\n')
            and 'Ancient City' not in text and 'I Wood too' not in text
            and 'quest_desc' not in text)


@case('两版模组版本不同但配方一致 → 应当通过')
def t_versions_agree(tmp):
    make_pack(tmp, '7.0', extra_tree=False)
    make_pack(tmp, '7.9', extra_tree=True)          # 多一棵树，但配方没变
    values, jars = in_sandbox(tmp, lambda: generate_all(['7.0', '7.9'], None, dict(ZH)))
    return bool(values) and len(jars) == 2 and jars['7.0'] != jars['7.9']


@case('某版公式分叉 → 必须红，并点名是哪版哪个键')
def t_versions_diverge(tmp):
    make_pack(tmp, '7.0')
    # 7.9 把那条副标题的 " + " 拆掉：该版不再认它是育种公式，于是分叉
    make_pack(tmp, '7.9', quest_lang=QUEST_LANG.replace('Parent + Oak/Other',
                                                        'Parent and Oak/Other'))
    try:
        in_sandbox(tmp, lambda: generate_all(['7.0', '7.9'], None, dict(ZH)))
    except DataError as e:
        return '7.9' in str(e) and 'quest.%s.quest_subtitle' % POLL in str(e)
    return False


@case('画像里没登记该 mod → 必须红，不许在 mods/ 里瞎找')
def t_portrait_required(tmp):
    pack = make_pack(tmp, '7.0')
    assert list((pack / 'mods').glob('productivetrees*.jar'))   # jar 就在那儿
    (tmp / 'versions' / 'db' / '7.0' / 'jars.json').write_text(
        json.dumps({'jars': {'someotherbee-1.0.jar': {
            'projectID': 1, 'fileID': 1, 'sha256': 'x', 'size': 1}}}),
        encoding='utf-8')
    try:
        in_sandbox(tmp, lambda: generate_all(['7.0'], None, dict(ZH)))
    except DataError as e:
        return '应恰有一个' in str(e)
    return False


@case('画像里有名字但 jar 没取回来 → 必须红，并给出取法')
def t_jar_absent(tmp):
    pack = make_pack(tmp, '7.0')
    next(iter((pack / 'mods').glob('*.jar'))).unlink()
    try:
        in_sandbox(tmp, lambda: generate_all(['7.0'], None, dict(ZH)))
    except DataError as e:
        return 'fetch_one_jar.py' in str(e)
    return False


@case('某版的包目录压根没取 → 必须红，不许当它不存在跳过去')
def t_packsrc_absent(tmp):
    make_pack(tmp, '7.0')
    (tmp / 'versions' / '7.9').mkdir(parents=True)   # 在册，但没取包
    try:
        in_sandbox(tmp, lambda: generate_all(['7.0', '7.9'], None, dict(ZH)))
    except DataError as e:
        return 'fetch_pack.py' in str(e)
    return False


def main():
    fail = 0
    for name, fn in CASES:
        tmp = Path(tempfile.mkdtemp())
        try:
            ok = fn(tmp)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
        print('%s %s' % ('✅' if ok else '❌', name))
        fail += 0 if ok else 1
    print('\n%d/%d 条通过' % (len(CASES) - fail, len(CASES)))
    return 1 if fail else 0


if __name__ == '__main__':
    sys.exit(main())
