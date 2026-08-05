#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# atm10-zh-cn - All the Mods 10 简体中文汉化补丁「绿油油版」
# Copyright (C) 2026 0xyk3r
# SPDX-License-Identifier: GPL-3.0-or-later
"""从 Productive Trees 的结构化数据生成任务书树名。

这个生成器只管理能够被数据证明为树木节点的字段：

- 授粉配方对应任务的 ``quest_subtitle``；
- ``trees.json`` 自突变对应任务的 ``quest_subtitle``；
- 任务英文标题与目标树苗官方英文名完全相等时的 ``title``。

箱子/考古来源、机器双关、说明节点以及所有 ``quest_desc`` 都不进入输出。生成结果
写到独立的 ``zz_hanhua_productive_trees_names.snbt``，不会覆盖同章节的手写 delta。

默认只把预览写到 stdout。树名定稿后显式使用 ``--write``，或在 CI 中用 ``--check``：

    python3 scripts/gen_productive_trees_quest_lang.py <ATM 实例目录>
    python3 scripts/gen_productive_trees_quest_lang.py <ATM 实例目录> --write
    python3 scripts/gen_productive_trees_quest_lang.py <ATM 实例目录> --check

7.0 使用较旧的 Productive Trees。核过该版本后，可用 ``--expect-*`` 传入该版计数；
默认计数对应本地验证过的 ATM10 7.3（Productive Trees 1.0.0）。
"""
import argparse
import json
import re
import sys
import zipfile
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_ZH = ROOT / 'src' / 'pack' / 'assets' / 'productivetrees' / 'lang' / 'zh_cn.json'
DEFAULT_DELTA_ROOT = (ROOT / 'src' / 'config' / 'ftbquests' / 'quests' / 'lang' / 'zh_cn')
DEFAULT_OUTPUT = (ROOT / 'src' / 'config' / 'ftbquests' / 'quests' / 'lang' / 'zh_cn'
                  / 'chapters' / 'zz_hanhua_productive_trees_names.snbt')
MANUAL_DELTA = DEFAULT_OUTPUT.with_name('zz_hanhua_productive_trees.snbt')

CHAPTER = Path('config/ftbquests/quests/chapters/productive_trees.snbt')
EN_QUEST = Path('config/ftbquests/quests/lang/en_us/chapters/productive_trees.snbt')
TREES_JSON = 'data/productivetrees/trees.json'
EN_LANG = 'assets/productivetrees/lang/en_us.json'
POLLINATION = re.compile(r'data/productivetrees/recipe/pollination/[^/]+\.json')
SCALAR = re.compile(r'^[\t ]+([A-Za-z0-9_.]+):\s*(.+)$')
QUEST_ID = re.compile(r'[0-9A-F]{16}')
ITEM_ID = re.compile(r'[a-z0-9_.-]+:[a-z0-9_./-]+')

# 这些不是 Productive Trees 的译名，本轮不顺带改口径。固定为 ATM 7.3 任务书现有中文，
# 避免树名生成器把“相思木/红树林/开花杜鹃”等人工选择意外改掉。
VANILLA_PARENT_NAMES = {
    'minecraft:acacia_leaves': '相思木',
    'minecraft:birch_leaves': '白桦',
    'minecraft:cherry_leaves': '樱花木',
    'minecraft:dark_oak_leaves': '深色橡木',
    'minecraft:flowering_azalea_leaves': '开花杜鹃',
    'minecraft:jungle_leaves': '丛林木',
    'minecraft:mangrove_leaves': '红树林',
    'minecraft:oak_leaves': '橡木',
    'minecraft:spruce_leaves': '云杉',
}


class DataError(Exception):
    pass


@dataclass(frozen=True)
class Recipe:
    result: str
    left: tuple[str, ...]
    right: tuple[str, ...]


@dataclass(frozen=True)
class Generated:
    values: dict[str, str]
    pollination_count: int
    mutation_count: int
    title_count: int
    manual_subtitles: tuple[str, ...]


def load_json(path):
    try:
        value = json.loads(Path(path).read_text(encoding='utf-8-sig'))
    except Exception as e:
        raise DataError('%s 解析失败：%s' % (path, e)) from e
    if not isinstance(value, dict):
        raise DataError('%s 的根节点不是对象' % path)
    return value


def zip_json(z, name):
    try:
        value = json.loads(z.read(name).decode('utf-8-sig'))
    except Exception as e:
        raise DataError('%s 读取失败：%s' % (name, e)) from e
    if not isinstance(value, dict):
        raise DataError('%s 的根节点不是对象' % name)
    return value


def parse_quest_tasks(text):
    """返回 ``quest id -> tasks 中的 item id``，不读取 rewards。

    FTB Quests 的 SNBT 不是 JSON，而且 ``tasks: [{`` 经常挤在同一行。这里按字符维护
    容器路径，只在 ``quests`` 的直接子对象中认任务、只在该任务的 ``tasks`` 内认物品。
    """
    out = {}
    stack = []
    pending = None
    current = None
    i, n = 0, len(text)
    while i < n:
        c = text[i]
        if c == '"':
            j = i + 1
            while j < n:
                if text[j] == '"' and text[j - 1] != '\\':
                    break
                j += 1
            if j >= n:
                raise DataError('任务章节中有未闭合的字符串（偏移 %d）' % i)
            value = text[i + 1:j]
            path_keys = [key for _, key in stack]
            if current is not None and pending == 'id' and len(stack) == current[0]:
                if QUEST_ID.fullmatch(value) and current[1] is None:
                    current[1] = value
            if current is not None and 'tasks' in path_keys[current[0] - 1:] \
                    and pending in ('item', 'id') and ITEM_ID.fullmatch(value):
                current[2].append(value)
            pending = None
            i = j + 1
            continue
        if c in '{[':
            stack.append((c, pending))
            if pending is None and len(stack) >= 2 and stack[-2][1] == 'quests' \
                    and c == '{' and current is None:
                current = [len(stack), None, []]
            pending = None
            i += 1
            continue
        if c in '}]':
            if current is not None and len(stack) == current[0] and c == '}':
                if current[1]:
                    if current[1] in out:
                        raise DataError('任务章节中重复 id：%s' % current[1])
                    out[current[1]] = tuple(dict.fromkeys(current[2]))
                current = None
            if stack:
                stack.pop()
            pending = None
            i += 1
            continue
        match = re.match(r'([A-Za-z_][A-Za-z0-9_]*)\s*:', text[i:])
        if match:
            pending = match.group(1)
            i += match.end()
            continue
        i += 1
    if current is not None or stack:
        raise DataError('任务章节的括号没有闭合')
    if not out:
        raise DataError('任务章节中一个 quest id 都没读到')
    return out


def scalar_lang(text):
    """读取任务语言文件中的单行标量；description 数组有意忽略。"""
    out = {}
    for line_no, line in enumerate(text.splitlines(), 1):
        match = SCALAR.match(line)
        if not match:
            continue
        key, raw = match.groups()
        if not raw.startswith('"'):
            continue
        try:
            value = json.loads(raw)
        except Exception as e:
            raise DataError('任务语言第 %d 行的 %s 不是合法字符串：%s'
                            % (line_no, key, e)) from e
        if isinstance(value, str):
            if key in out:
                raise DataError('任务语言中重复键：%s' % key)
            out[key] = value
    if not out:
        raise DataError('任务语言文件中一个标量键都没读到')
    return out


def ingredient_items(value, where):
    values = value if isinstance(value, list) else [value]
    if not values:
        raise DataError('%s 是空的配料数组' % where)
    out = []
    for ingredient in values:
        if not isinstance(ingredient, dict) or not ITEM_ID.fullmatch(str(ingredient.get('item', ''))):
            raise DataError('%s 出现不支持的配料结构：%r' % (where, ingredient))
        out.append(ingredient['item'])
    return tuple(dict.fromkeys(out))


def productive_data(jar_path):
    recipes = {}
    mutations = {}
    try:
        z = zipfile.ZipFile(jar_path)
    except Exception as e:
        raise DataError('%s 不是可读的 jar：%s' % (jar_path, e)) from e
    with z:
        names = z.namelist()
        for name in sorted(n for n in names if POLLINATION.fullmatch(n)):
            data = zip_json(z, name)
            if data.get('type') != 'productivetrees:tree_pollination':
                raise DataError('%s 不是 Productive Trees 授粉配方' % name)
            result = data.get('result', {}).get('id') if isinstance(data.get('result'), dict) else None
            if not isinstance(result, str) or not result.startswith('productivetrees:') \
                    or not result.endswith('_sapling'):
                raise DataError('%s 的 result 不是 Productive Trees 树苗：%r' % (name, result))
            if result in recipes:
                raise DataError('多个授粉配方产出同一树苗：%s' % result)
            recipes[result] = Recipe(
                result=result,
                left=ingredient_items(data.get('leafA'), name + '.leafA'),
                right=ingredient_items(data.get('leafB'), name + '.leafB'),
            )

        trees = zip_json(z, TREES_JSON)
        for source, tree in trees.items():
            if not isinstance(tree, dict) or not isinstance(tree.get('mutation_info'), dict):
                continue
            raw_target = tree['mutation_info'].get('target')
            if not isinstance(raw_target, str) or ':' not in raw_target:
                raise DataError('%s 的 mutation_info.target 非法：%r' % (source, raw_target))
            namespace, target_path = raw_target.split(':', 1)
            if namespace != 'productivetrees':
                raise DataError('%s 的突变目标不属于 Productive Trees：%s'
                                % (source, raw_target))
            if not target_path.endswith('_sapling'):
                target_path += '_sapling'
            target = 'productivetrees:' + target_path
            source_sapling = 'productivetrees:%s_sapling' % source
            if target in mutations:
                raise DataError('多个自突变来源指向同一树苗：%s' % target)
            mutations[target] = source_sapling

        en = zip_json(z, EN_LANG)
    if not recipes:
        raise DataError('%s 中一个授粉配方都没读到' % jar_path)
    if not mutations:
        raise DataError('%s 中一个自突变都没读到' % jar_path)
    return recipes, mutations, en


def sapling_key(item_id):
    if not item_id.startswith('productivetrees:') or not item_id.endswith('_sapling'):
        raise DataError('不是 Productive Trees 树苗：%s' % item_id)
    return 'block.productivetrees.%s' % item_id.split(':', 1)[1]


def sapling_name(item_id, zh, strip_suffix):
    key = sapling_key(item_id)
    value = zh.get(key)
    if not isinstance(value, str) or not value.strip():
        raise DataError('中文语言文件缺少有效的 %s' % key)
    if not strip_suffix:
        return value
    if not value.endswith('树苗') or value == '树苗':
        raise DataError('%s 必须严格以“树苗”结尾，实际为 %r' % (key, value))
    return value[:-2]


def parent_name(item_id, zh):
    if item_id in VANILLA_PARENT_NAMES:
        return VANILLA_PARENT_NAMES[item_id]
    if item_id.startswith('productivetrees:') and item_id.endswith('_leaves'):
        base = item_id.split(':', 1)[1][:-len('_leaves')]
        return sapling_name('productivetrees:%s_sapling' % base, zh, True)
    raise DataError('授粉配方出现未知父本：%s' % item_id)


def one_target_per_quest(tasks):
    by_quest, by_target = {}, {}
    for quest_id, items in tasks.items():
        targets = tuple(dict.fromkeys(
            item for item in items
            if item.startswith('productivetrees:') and item.endswith('_sapling')
        ))
        if targets:
            by_quest[quest_id] = targets
            for target in targets:
                by_target.setdefault(target, []).append(quest_id)
    return by_quest, by_target


def generate(chapter_text, quest_lang_text, jar_path, zh):
    tasks = parse_quest_tasks(chapter_text)
    quest_lang = scalar_lang(quest_lang_text)
    recipes, mutations, mod_en = productive_data(jar_path)
    by_quest, by_target = one_target_per_quest(tasks)

    values = {}
    managed_quest_targets = {}
    pollination_count = mutation_count = 0
    overlap = set(recipes) & set(mutations)
    if overlap:
        raise DataError('这些树苗同时有授粉和自突变来源：%s' % '、'.join(sorted(overlap)))

    for target, source in sorted({**recipes, **mutations}.items()):
        quest_ids = by_target.get(target, [])
        if not quest_ids:
            continue
        if len(quest_ids) != 1:
            raise DataError('%s 同时被多个任务作为目标：%s' % (target, '、'.join(quest_ids)))
        quest_id = quest_ids[0]
        if quest_id in managed_quest_targets:
            raise DataError('任务 %s 同时对应多个树苗结果' % quest_id)
        subtitle_key = 'quest.%s.quest_subtitle' % quest_id
        if subtitle_key not in quest_lang:
            raise DataError('受管理的树木任务缺少英文副标题：%s' % subtitle_key)

        if target in recipes:
            # 配方存在不等于 ATM 想把这个节点展示成育种公式。若作者把它写成
            # “Ancient City Chests”一类来源说明，来源文案拥有该字段，生成器跳过。
            if quest_lang[subtitle_key].count(' + ') != 1:
                continue
            recipe = recipes[target]
            left = '/'.join(parent_name(item, zh) for item in recipe.left)
            right = '/'.join(parent_name(item, zh) for item in recipe.right)
            values[subtitle_key] = '%s + %s' % (left, right)
            pollination_count += 1
        else:
            if quest_lang[subtitle_key].count(' + ') != 1 \
                    or not quest_lang[subtitle_key].endswith(' + Luck'):
                continue
            values[subtitle_key] = '%s + 运气' % sapling_name(source, zh, True)
            mutation_count += 1
        managed_quest_targets[quest_id] = target

    # 标题单独判：任何树苗任务都可以同步标题，但必须是“英文标题 == 官方英文树苗名”。
    # 这会命中两个写死的树苗标题，不会命中 Productive Trees / Stripping / Sawing。
    title_count = 0
    for quest_id, targets in sorted(by_quest.items()):
        if len(targets) != 1:
            continue
        target = targets[0]
        title_key = 'quest.%s.title' % quest_id
        if title_key not in quest_lang:
            continue
        lang_key = sapling_key(target)
        if quest_lang[title_key] != mod_en.get(lang_key):
            continue
        values[title_key] = sapling_name(target, zh, False)
        title_count += 1

    all_subtitles = {key for key in quest_lang if key.endswith('.quest_subtitle')}
    managed_subtitles = {key for key in values if key.endswith('.quest_subtitle')}
    manual_subtitles = tuple(sorted(all_subtitles - managed_subtitles))
    if not managed_subtitles:
        raise DataError('一个可生成的树木任务副标题都没找到')
    return Generated(values, pollination_count, mutation_count, title_count, manual_subtitles)


def validate_counts(result, pollination, mutation, titles, manual):
    expected = {
        '授粉副标题': (result.pollination_count, pollination),
        '自突变副标题': (result.mutation_count, mutation),
        '树苗显式标题': (result.title_count, titles),
        '保留手写的副标题': (len(result.manual_subtitles), manual),
    }
    bad = ['%s %d（预期 %d）' % (name, actual, wanted)
           for name, (actual, wanted) in expected.items() if actual != wanted]
    if bad:
        raise DataError('生成范围发生变化：' + '；'.join(bad))


def render(values):
    lines = ['{']
    for key, value in sorted(values.items()):
        lines.append('\t%s: %s' % (key, json.dumps(value, ensure_ascii=False)))
    lines.append('}')
    return '\n'.join(lines) + '\n'


def existing_generated_values(path):
    text = Path(path).read_text(encoding='utf-8')
    lines = text.splitlines()
    if len(lines) < 2 or lines[0] != '{' or lines[-1] != '}':
        raise DataError('%s 不是预期的 generated-only SNBT' % path)
    out = {}
    for line_no, line in enumerate(lines[1:-1], 2):
        match = SCALAR.match(line)
        if not match:
            raise DataError('%s 第 %d 行不是单行标量，拒绝覆盖' % (path, line_no))
        key, raw = match.groups()
        try:
            value = json.loads(raw)
        except Exception as e:
            raise DataError('%s 第 %d 行解析失败：%s' % (path, line_no, e)) from e
        if not isinstance(value, str) or key in out:
            raise DataError('%s 第 %d 行不是唯一字符串键，拒绝覆盖' % (path, line_no))
        out[key] = value
    return out


def delta_scalars(path):
    """读取一份手写 delta 的单行字符串，数组原样留给手写层、不参与本检查。"""
    out = {}
    for line_no, line in enumerate(Path(path).read_text(encoding='utf-8').splitlines(), 1):
        match = SCALAR.match(line)
        if not match or not match.group(2).startswith('"'):
            continue
        key, raw = match.groups()
        try:
            value = json.loads(raw)
        except Exception as e:
            raise DataError('%s 第 %d 行的 %s 解析失败：%s'
                            % (path, line_no, key, e)) from e
        if isinstance(value, str):
            if key in out:
                raise DataError('%s 内部重复键：%s' % (path, key))
            out[key] = value
    return out


def ownership_issues(result, delta_root, output):
    """检查 generated-only 键没有继续被其他手写 delta 持有。"""
    owners = {}
    excluded = Path(output).resolve()
    for path in sorted(Path(delta_root).rglob('zz_hanhua_*.snbt')):
        if path.resolve() == excluded:
            continue
        for key, value in delta_scalars(path).items():
            if key in owners:
                raise DataError('手写 delta 重复键：%s 同时在 %s 与 %s'
                                % (key, owners[key], path))
            owners[key] = path

    issues = []
    for key in sorted(set(result.values) & set(owners)):
        issues.append('生成键 %s 仍由手写文件 %s 持有，需先移交'
                      % (key, owners[key]))
    return issues


def find_jar(mods):
    candidates = []
    for path in sorted(Path(mods).glob('productivetrees*.jar')):
        try:
            with zipfile.ZipFile(path) as z:
                if TREES_JSON in z.namelist() and EN_LANG in z.namelist():
                    candidates.append(path)
        except Exception:
            continue
    if len(candidates) != 1:
        raise DataError('%s 中应恰有一个有效的 Productive Trees jar，实际为：%s'
                        % (mods, '、'.join(p.name for p in candidates) or '0 个'))
    return candidates[0]


def resolve_input(explicit, root, relative, label):
    path = Path(explicit) if explicit else Path(root) / relative
    if not path.is_file():
        raise DataError('%s不存在：%s' % (label, path))
    return path


def parse_args(argv):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('pack_root', type=Path, help='ATM 实例或完整官方包根目录')
    parser.add_argument('--jar', type=Path, help='Productive Trees jar；默认从 <pack_root>/mods 找')
    parser.add_argument('--chapter', type=Path, help='官方 productive_trees.snbt 章节结构')
    parser.add_argument('--quest-lang', type=Path, help='官方英文 productive_trees.snbt')
    parser.add_argument('--lang', type=Path, default=DEFAULT_ZH, help='本包 Productive Trees 中文 lang')
    parser.add_argument('--output', type=Path, default=DEFAULT_OUTPUT, help='generated-only SNBT 路径')
    parser.add_argument('--delta-root', type=Path, default=DEFAULT_DELTA_ROOT,
                        help='手写任务 delta 根目录，用于重键与树苗标题校验')
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--write', action='store_true', help='写入 --output；默认只预览')
    mode.add_argument('--check', action='store_true', help='检查 --output 与生成结果逐字一致')
    parser.add_argument('--expect-pollination', type=int, default=148)
    parser.add_argument('--expect-mutation', type=int, default=8)
    parser.add_argument('--expect-titles', type=int, default=2)
    parser.add_argument('--expect-manual-subtitles', type=int, default=9)
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    try:
        chapter = resolve_input(args.chapter, args.pack_root, CHAPTER, '任务章节')
        quest_lang = resolve_input(args.quest_lang, args.pack_root, EN_QUEST, '英文任务语言')
        jar = args.jar or find_jar(args.pack_root / 'mods')
        if not Path(jar).is_file():
            raise DataError('Productive Trees jar 不存在：%s' % jar)
        zh = load_json(args.lang)
        result = generate(chapter.read_text(encoding='utf-8'),
                          quest_lang.read_text(encoding='utf-8'), jar, zh)
        validate_counts(result, args.expect_pollination, args.expect_mutation,
                        args.expect_titles, args.expect_manual_subtitles)
        output = render(result.values)

        if args.output.resolve() == MANUAL_DELTA.resolve():
            raise DataError('拒绝覆盖手写任务文件：%s；请使用独立的 generated-only 文件' % args.output)
        issues = ownership_issues(result, args.delta_root, args.output)
        if (args.write or args.check) and issues:
            raise DataError('任务键所有权尚未就绪：\n   ' + '\n   '.join(issues))
        if args.check:
            if not args.output.is_file():
                raise DataError('待检查的生成文件不存在：%s' % args.output)
            if args.output.read_text(encoding='utf-8') != output:
                raise DataError('%s 与当前配方/树苗译名不一致，请在译名定稿后重新 --write'
                                % args.output)
        elif args.write:
            if args.output.is_file():
                old = existing_generated_values(args.output)
                foreign = sorted(set(old) - set(result.values))
                if foreign:
                    raise DataError('%s 含有当前生成器不管理的键，拒绝删除：%s'
                                    % (args.output, '、'.join(foreign)))
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(output, encoding='utf-8')
        else:
            sys.stdout.write(output)

        action = '检查通过' if args.check else ('已写入 %s' % args.output if args.write else '仅预览')
        print('✅ Productive Trees 任务树名%s：授粉 %d、自突变 %d、显式树苗标题 %d；'
              '保留手写副标题 %d' % (action, result.pollination_count,
                                  result.mutation_count, result.title_count,
                                  len(result.manual_subtitles)), file=sys.stderr)
        print('   保留手写：%s' % '、'.join(result.manual_subtitles), file=sys.stderr)
        if issues:
            print('⚠️ 写入前待处理：\n   %s' % '\n   '.join(issues), file=sys.stderr)
        return 0
    except DataError as e:
        print('❌ %s' % e, file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
