#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# atm10-zh-cn - All the Mods 10 简体中文汉化补丁「绿油油版」
# Copyright (C) 2026 0xyk3r
# SPDX-License-Identifier: GPL-3.0-or-later
"""Productive Trees 任务树名生成器的边界测试。"""
import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))

from gen_productive_trees_quest_lang import (  # noqa: E402
    DataError,
    generate,
    ownership_issues,
    render,
    validate_counts,
)

POLL = 'AAAAAAAAAAAAAAAA'
MUTATION = 'BBBBBBBBBBBBBBBB'
LOOT = 'CCCCCCCCCCCCCCCC'
MACHINE = 'DDDDDDDDDDDDDDDD'

CHAPTER = '''{
\tquests: [
\t\t{
\t\t\tid: "AAAAAAAAAAAAAAAA"
\t\t\ttasks: [{
\t\t\t\tid: "1111111111111111"
\t\t\t\titem: { count: 1, id: "productivetrees:hybrid_sapling" }
\t\t\t\ttype: "item"
\t\t\t}]
\t\t}
\t\t{
\t\t\tid: "BBBBBBBBBBBBBBBB"
\t\t\ttasks: [{
\t\t\t\tid: "2222222222222222"
\t\t\t\titem: "productivetrees:mutated_sapling"
\t\t\t\ttype: "item"
\t\t\t}]
\t\t}
\t\t{
\t\t\tid: "CCCCCCCCCCCCCCCC"
\t\t\ttasks: [{
\t\t\t\tid: "3333333333333333"
\t\t\t\titem: { count: 1, id: "productivetrees:loot_sapling" }
\t\t\t\ttype: "item"
\t\t\t}]
\t\t}
\t\t{
\t\t\tid: "DDDDDDDDDDDDDDDD"
\t\t\ttasks: [{
\t\t\t\tid: "4444444444444444"
\t\t\t\titem: { count: 1, id: "productivetrees:sawmill" }
\t\t\t\ttype: "item"
\t\t\t}]
\t\t}
\t]
}
'''

QUEST_LANG = '''{
\tquest.AAAAAAAAAAAAAAAA.quest_subtitle: "Parent + Oak/Other"
\tquest.AAAAAAAAAAAAAAAA.title: "Hybrid Sapling"
\tquest.BBBBBBBBBBBBBBBB.quest_subtitle: "Source + Luck"
\tquest.BBBBBBBBBBBBBBBB.title: "Mutated Sapling"
\tquest.CCCCCCCCCCCCCCCC.quest_desc: ["Only found in Ancient City chests."]
\tquest.CCCCCCCCCCCCCCCC.quest_subtitle: "Ancient City Chests"
\tquest.DDDDDDDDDDDDDDDD.quest_desc: ["This is a machine, not a tree recipe."]
\tquest.DDDDDDDDDDDDDDDD.quest_subtitle: "I Wood too"
\tquest.DDDDDDDDDDDDDDDD.title: "Sawmill"
}
'''

ZH = {
    'block.productivetrees.parent_sapling': '亲本树苗',
    'block.productivetrees.other_sapling': '另一树树苗',
    'block.productivetrees.hybrid_sapling': '杂交树树苗',
    'block.productivetrees.source_sapling': '源树树苗',
    'block.productivetrees.mutated_sapling': '突变树树苗',
    'block.productivetrees.loot_sapling': '遗迹树树苗',
}


def make_jar(path):
    recipe = {
        'type': 'productivetrees:tree_pollination',
        'leafA': {'item': 'productivetrees:parent_leaves'},
        'leafB': [
            {'item': 'minecraft:oak_leaves'},
            {'item': 'productivetrees:other_leaves'},
        ],
        'result': {'count': 1, 'id': 'productivetrees:hybrid_sapling'},
    }
    # 即使模组数据里有配方，只要 ATM 把副标题写成来源说明，也必须继续手写。
    loot_recipe = {
        'type': 'productivetrees:tree_pollination',
        'leafA': {'item': 'productivetrees:parent_leaves'},
        'leafB': {'item': 'minecraft:birch_leaves'},
        'result': {'count': 1, 'id': 'productivetrees:loot_sapling'},
    }
    trees = {
        'source': {
            'mutation_info': {
                'target': 'productivetrees:mutated',
                'chance': 0.05,
            },
        },
    }
    en = {
        'block.productivetrees.hybrid_sapling': 'Hybrid Sapling',
        'block.productivetrees.mutated_sapling': 'Mutated Sapling',
        'block.productivetrees.loot_sapling': 'Loot Sapling',
    }
    with zipfile.ZipFile(path, 'w') as z:
        z.writestr('data/productivetrees/recipe/pollination/hybrid.json', json.dumps(recipe))
        z.writestr('data/productivetrees/recipe/pollination/loot.json', json.dumps(loot_recipe))
        z.writestr('data/productivetrees/trees.json', json.dumps(trees))
        z.writestr('assets/productivetrees/lang/en_us.json', json.dumps(en))


class ProductiveTreesQuestLangTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.jar = Path(self.temp.name) / 'productivetrees.jar'
        make_jar(self.jar)

    def tearDown(self):
        self.temp.cleanup()

    def test_only_structurally_owned_fields_are_generated(self):
        result = generate(CHAPTER, QUEST_LANG, self.jar, dict(ZH))

        self.assertEqual(result.pollination_count, 1)
        self.assertEqual(result.mutation_count, 1)
        self.assertEqual(result.title_count, 2)
        self.assertEqual(result.values['quest.%s.quest_subtitle' % POLL],
                         '亲本 + 橡木/另一树')
        self.assertEqual(result.values['quest.%s.quest_subtitle' % MUTATION],
                         '源树 + 运气')
        self.assertEqual(result.values['quest.%s.title' % POLL], '杂交树树苗')
        self.assertEqual(result.values['quest.%s.title' % MUTATION], '突变树树苗')

        # 战利品来源与机器文案继续由上游/手写 delta 持有；生成器不输出任何正文。
        self.assertEqual(result.manual_subtitles, (
            'quest.%s.quest_subtitle' % LOOT,
            'quest.%s.quest_subtitle' % MACHINE,
        ))
        self.assertFalse(any(key.endswith('.quest_desc') for key in result.values))
        self.assertNotIn('quest.%s.quest_subtitle' % LOOT, result.values)
        self.assertNotIn('quest.%s.quest_subtitle' % MACHINE, result.values)
        self.assertNotIn('quest.%s.title' % MACHINE, result.values)

    def test_missing_sapling_suffix_fails_closed(self):
        zh = dict(ZH)
        zh['block.productivetrees.parent_sapling'] = '亲本'
        with self.assertRaisesRegex(DataError, '必须严格以“树苗”结尾'):
            generate(CHAPTER, QUEST_LANG, self.jar, zh)

    def test_scope_count_change_fails_closed(self):
        result = generate(CHAPTER, QUEST_LANG, self.jar, dict(ZH))
        with self.assertRaisesRegex(DataError, '生成范围发生变化'):
            validate_counts(result, pollination=2, mutation=1, titles=2, manual=2)

    def test_render_is_stable_and_contains_only_generated_keys(self):
        result = generate(CHAPTER, QUEST_LANG, self.jar, dict(ZH))
        text = render(result.values)
        self.assertTrue(text.startswith('{\n\tquest.'))
        self.assertTrue(text.endswith('\n}\n'))
        self.assertNotIn('Ancient City', text)
        self.assertNotIn('I Wood too', text)
        self.assertNotIn('quest_desc', text)

    def test_ownership_rejects_all_generated_key_duplicates(self):
        result = generate(CHAPTER, QUEST_LANG, self.jar, dict(ZH))
        root = Path(self.temp.name) / 'delta'
        root.mkdir()
        manual = root / 'zz_hanhua_manual.snbt'
        manual.write_text(
            '{\n'
            '\tquest.%s.title: "杂交树树苗"\n'
            '\tquest.%s.title: "突变树树苗"\n'
            '\tquest.%s.quest_subtitle: "旧配方"\n'
            '}\n' % (POLL, MUTATION, POLL),
            encoding='utf-8',
        )
        issues = ownership_issues(result, root, root / 'zz_hanhua_generated.snbt')
        self.assertEqual(len(issues), 3)
        self.assertTrue(all('仍由手写文件' in issue for issue in issues))


if __name__ == '__main__':
    unittest.main()
