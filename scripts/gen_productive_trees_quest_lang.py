#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# atm10-zh-cn — All the Mods 10 简体中文汉化补丁「绿油油版」
# Copyright (C) 2026 0xyk3r
# Copyright (C) 2026 星野夢華 (Hoshino Yumeka)
# SPDX-License-Identifier: GPL-3.0-or-later
"""任务书里的资源树育种公式，从 Productive Trees 自己的数据生成。

任务书副标题写的是「甲 + 乙」这种育种公式，而这些名字必须跟 JEI 里的物品名
一模一样，否则玩家照着搜是空的。手写就会漂：改了树名不记得回来改公式。
所以副标题不手写，从模组的授粉配方与 trees.json 现推。

**只管能被数据证明是树木节点的字段**：

- 授粉配方对应任务的 ``quest_subtitle``；
- ``trees.json`` 自突变对应任务的 ``quest_subtitle``；
- 任务英文标题与该树苗官方英文名逐字相等时的 ``title``。

箱子/考古来源、机器双关、说明节点，以及所有 ``quest_desc``，一概不碰——
它们的文案是人写的，不是配方推得出来的。

## 不变量：所有在册版本一致

**每个在册版本都跑一遍，结果必须彼此逐字一致，且等于入库的那份文件。**

原始实现（PR #17）钉的是四个计数 148/8/2/9。那是数字，ATM 一大更就对不上，
而且对不上之后没人知道该填几，最后一定变成「跑一遍看输出多少就填多少」——
闸自己把自己关了。这里钉的是一句不含数字的性质，ATM 更几次都不用改本文件。

真有某版分叉时会红并列出是哪个版本、哪些键，那时候再按仓库已有的
``versions/<版本>/quest_overrides.snbt`` 拆成该版专属覆盖。**现在不预先拆**：
7.0 的 Productive Trees 0.8.1 与其余版本的 1.0.0，148 条授粉配方与 8 条自突变
逐条相同（只是 1.0.0 多一棵树），摆四份一模一样的文件只是徒增维护面。

## 版本要什么都查画像，不写死

jar 名与字节取自 ``versions/db/<版本>/jars.json``，官方章节取自
``build/packsrc/<版本>/``。加一个新版本不用动这个脚本，把该版画像入库即可。
jar 由 ``scripts/fetch_one_jar.py`` 按画像单独取回并核过 sha256——不在这里下载，
生成器不联网，取不到就红。

    python3 scripts/gen_productive_trees_quest_lang.py              # 预览
    python3 scripts/gen_productive_trees_quest_lang.py --write
    python3 scripts/gen_productive_trees_quest_lang.py --check
    python3 scripts/gen_productive_trees_quest_lang.py --only 7.3
    python3 scripts/gen_productive_trees_quest_lang.py --pack-root <本机实例>
"""
import argparse
import json
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ZH_LANG = ROOT / 'src' / 'pack' / 'assets' / 'productivetrees' / 'lang' / 'zh_cn.json'
DELTA_ROOT = ROOT / 'src' / 'config' / 'ftbquests' / 'quests' / 'lang' / 'zh_cn'
OUTPUT = DELTA_ROOT / 'chapters' / 'zz_hanhua_productive_trees_names.snbt'
MANUAL_DELTA = OUTPUT.with_name('zz_hanhua_productive_trees.snbt')
PACKSRC = ROOT / 'build' / 'packsrc'

CHAPTER = Path('config/ftbquests/quests/chapters/productive_trees.snbt')
EN_QUEST = Path('config/ftbquests/quests/lang/en_us/chapters/productive_trees.snbt')
JAR_PREFIX = 'productivetrees'
TREES_JSON = 'data/productivetrees/trees.json'
EN_LANG = 'assets/productivetrees/lang/en_us.json'
POLLINATION = re.compile(r'data/productivetrees/recipe/pollination/[^/]+\.json')
SCALAR = re.compile(r'^[\t ]+([A-Za-z0-9_.]+):\s*(.+)$')
QUEST_ID = re.compile(r'[0-9A-F]{16}')
ITEM_ID = re.compile(r'[a-z0-9_.-]+:[a-z0-9_./-]+')

# 原版树的名字不归本生成器管，写死成任务书里现有的中文。
# 不跟着 Productive Trees 的口径走：这几个是 minecraft: 命名空间的东西，
# 顺手改掉等于借育种公式偷改原版译名。
VANILLA_PARENTS = {
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
    """数据不是预期的形状。一律当失败，不许降级继续。"""


# ── 读取 ────────────────────────────────────────────────────────────────────

def parse_quest_tasks(text):
    """返回 ``quest id -> 该任务 tasks 里的 item id``，不读 rewards。

    FTB Quests 的 SNBT 不是 JSON，``tasks: [{`` 还经常挤在同一行，正则读不了。
    这里按字符维护容器路径：只在 ``quests`` 的直接子对象里认任务，只在该任务的
    ``tasks`` 里认物品——奖励里也会出现树苗，认进来就会把「产出」和「奖励」搞混。
    """
    out, stack = {}, []
    pending = current = None
    i, n = 0, len(text)
    while i < n:
        c = text[i]
        if c == '"':
            j = i + 1
            while j < n and not (text[j] == '"' and text[j - 1] != '\\'):
                j += 1
            if j >= n:
                raise DataError('任务章节里有未闭合的字符串（偏移 %d）' % i)
            value, path = text[i + 1:j], [k for _, k in stack]
            if current and pending == 'id' and len(stack) == current[0] \
                    and current[1] is None and QUEST_ID.fullmatch(value):
                current[1] = value
            if current and 'tasks' in path[current[0] - 1:] \
                    and pending in ('item', 'id') and ITEM_ID.fullmatch(value):
                current[2].append(value)
            pending, i = None, j + 1
            continue
        if c in '{[':
            stack.append((c, pending))
            if pending is None and c == '{' and current is None \
                    and len(stack) >= 2 and stack[-2][1] == 'quests':
                current = [len(stack), None, []]
            pending, i = None, i + 1
            continue
        if c in '}]':
            if current and c == '}' and len(stack) == current[0]:
                if current[1]:
                    if current[1] in out:
                        raise DataError('任务章节里重复的 quest id：%s' % current[1])
                    out[current[1]] = tuple(dict.fromkeys(current[2]))
                current = None
            if stack:
                stack.pop()
            pending, i = None, i + 1
            continue
        m = re.match(r'([A-Za-z_][A-Za-z0-9_]*)\s*:', text[i:])
        if m:
            pending, i = m.group(1), i + m.end()
            continue
        i += 1
    if current or stack:
        raise DataError('任务章节的括号没闭合')
    if not out:
        raise DataError('任务章节里一个 quest id 都没读到')
    return out


def scalar_lang(text):
    """任务语言文件里的单行标量。多行数组（描述）有意不读，本生成器不碰描述。"""
    out = {}
    for no, line in enumerate(text.splitlines(), 1):
        m = SCALAR.match(line)
        if not m or not m.group(2).startswith('"'):
            continue
        key, raw = m.groups()
        try:
            value = json.loads(raw)
        except Exception as e:                                   # noqa: BLE001
            raise DataError('任务语言第 %d 行的 %s 不是合法字符串：%s' % (no, key, e)) from e
        if isinstance(value, str):
            if key in out:
                raise DataError('任务语言里重复的键：%s' % key)
            out[key] = value
    if not out:
        raise DataError('任务语言文件里一个标量键都没读到')
    return out


def _items(value, where):
    values = value if isinstance(value, list) else [value]
    if not values:
        raise DataError('%s 是空的配料数组' % where)
    out = []
    for one in values:
        if not isinstance(one, dict) or not ITEM_ID.fullmatch(str(one.get('item', ''))):
            raise DataError('%s 出现不支持的配料结构：%r' % (where, one))
        out.append(one['item'])
    return tuple(dict.fromkeys(out))


def mod_data(jar):
    """从 jar 里取：授粉配方、自突变、官方英文名。三者缺一都当失败。"""
    try:
        z = zipfile.ZipFile(jar)
    except Exception as e:                                       # noqa: BLE001
        raise DataError('%s 不是可读的 jar：%s' % (jar, e)) from e
    with z:
        def load(name):
            try:
                value = json.loads(z.read(name).decode('utf-8-sig'))
            except Exception as e:                               # noqa: BLE001
                raise DataError('%s 里的 %s 读不出来：%s' % (jar, name, e)) from e
            if not isinstance(value, dict):
                raise DataError('%s 里的 %s 根节点不是对象' % (jar, name))
            return value

        recipes = {}
        for name in sorted(n for n in z.namelist() if POLLINATION.fullmatch(n)):
            d = load(name)
            if d.get('type') != 'productivetrees:tree_pollination':
                raise DataError('%s 不是授粉配方' % name)
            result = d.get('result', {}).get('id') if isinstance(d.get('result'), dict) else None
            if not isinstance(result, str) or not result.startswith('productivetrees:') \
                    or not result.endswith('_sapling'):
                raise DataError('%s 的 result 不是树苗：%r' % (name, result))
            if result in recipes:
                raise DataError('多个授粉配方产出同一树苗：%s' % result)
            recipes[result] = (_items(d.get('leafA'), name + '.leafA'),
                               _items(d.get('leafB'), name + '.leafB'))

        mutations = {}
        for source, tree in load(TREES_JSON).items():
            info = tree.get('mutation_info') if isinstance(tree, dict) else None
            if not isinstance(info, dict):
                continue
            raw = info.get('target')
            if not isinstance(raw, str) or ':' not in raw:
                raise DataError('%s 的 mutation_info.target 非法：%r' % (source, raw))
            namespace, path = raw.split(':', 1)
            if namespace != 'productivetrees':
                raise DataError('%s 的突变目标不属于 Productive Trees：%s' % (source, raw))
            target = 'productivetrees:%s' % (path if path.endswith('_sapling')
                                             else path + '_sapling')
            if target in mutations:
                raise DataError('多个自突变来源指向同一树苗：%s' % target)
            mutations[target] = 'productivetrees:%s_sapling' % source

        english = load(EN_LANG)

    if not recipes:
        raise DataError('%s 里一个授粉配方都没读到' % jar)
    if not mutations:
        raise DataError('%s 里一个自突变都没读到' % jar)
    overlap = set(recipes) & set(mutations)
    if overlap:
        raise DataError('这些树苗同时有授粉与自突变来源：%s' % '、'.join(sorted(overlap)))
    return recipes, mutations, english


# ── 生成 ────────────────────────────────────────────────────────────────────

def sapling_key(item_id):
    if not item_id.startswith('productivetrees:') or not item_id.endswith('_sapling'):
        raise DataError('不是 Productive Trees 树苗：%s' % item_id)
    return 'block.productivetrees.%s' % item_id.split(':', 1)[1]


def sapling_name(item_id, zh, bare):
    """取树苗中文名。``bare`` 时去掉「树苗」二字，因为公式里写的是树名不是树苗。"""
    key = sapling_key(item_id)
    value = zh.get(key)
    if not isinstance(value, str) or not value.strip():
        raise DataError('中文语言文件缺少有效的 %s' % key)
    if not bare:
        return value
    if value == '树苗' or not value.endswith('树苗'):
        raise DataError('%s 必须严格以「树苗」结尾，实际是 %r' % (key, value))
    return value[:-2]


def parent_name(item_id, zh):
    if item_id in VANILLA_PARENTS:
        return VANILLA_PARENTS[item_id]
    if item_id.startswith('productivetrees:') and item_id.endswith('_leaves'):
        stem = item_id.split(':', 1)[1][:-len('_leaves')]
        return sapling_name('productivetrees:%s_sapling' % stem, zh, True)
    raise DataError('授粉配方出现未知父本：%s' % item_id)


def generate(chapter_text, quest_lang_text, jar, zh):
    """返回 ``{任务语言键: 中文}``。只放能被数据证明归本生成器管的键。"""
    tasks = parse_quest_tasks(chapter_text)
    lang = scalar_lang(quest_lang_text)
    recipes, mutations, english = mod_data(jar)

    # 一个任务只认一个树苗产出；多个就说明这不是「种出某棵树」的节点。
    by_quest, by_target = {}, {}
    for quest, items in tasks.items():
        targets = tuple(dict.fromkeys(
            i for i in items
            if i.startswith('productivetrees:') and i.endswith('_sapling')))
        if targets:
            by_quest[quest] = targets
            for t in targets:
                by_target.setdefault(t, []).append(quest)

    values, owned = {}, {}
    for target, source in sorted({**recipes, **mutations}.items()):
        quests = by_target.get(target, [])
        if not quests:
            continue
        if len(quests) != 1:
            raise DataError('%s 同时被多个任务作为目标：%s' % (target, '、'.join(quests)))
        quest = quests[0]
        if quest in owned:
            raise DataError('任务 %s 同时对应多个树苗结果' % quest)
        key = 'quest.%s.quest_subtitle' % quest
        if key not in lang:
            raise DataError('该由本生成器管理的树木任务缺英文副标题：%s' % key)

        # 有配方 ≠ ATM 想把这个节点展示成育种公式。作者写成「Ancient City Chests」
        # 这类来源说明时，那条文案归人写，生成器让开。判据是英文副标题的形状。
        if lang[key].count(' + ') != 1:
            continue
        if target in recipes:
            left, right = recipes[target]
            values[key] = '%s + %s' % ('/'.join(parent_name(i, zh) for i in left),
                                       '/'.join(parent_name(i, zh) for i in right))
        else:
            if not lang[key].endswith(' + Luck'):
                continue
            values[key] = '%s + 运气' % sapling_name(source, zh, True)
        owned[quest] = target

    # 标题另判：任何树苗任务都可以同步标题，但只在「英文标题 == 该树苗官方英文名」
    # 时才算。这样 Productive Trees / Stripping / Sawing 这些人起的标题不会被吃掉。
    for quest, targets in sorted(by_quest.items()):
        if len(targets) != 1:
            continue
        key = 'quest.%s.title' % quest
        if key in lang and lang[key] == english.get(sapling_key(targets[0])):
            values[key] = sapling_name(targets[0], zh, False)

    if not any(k.endswith('.quest_subtitle') for k in values):
        raise DataError('一个可生成的树木育种公式都没找到')
    return values


def render(values):
    lines = ['{']
    lines += ['\t%s: %s' % (k, json.dumps(v, ensure_ascii=False))
              for k, v in sorted(values.items())]
    lines.append('}')
    return '\n'.join(lines) + '\n'


# ── 与手写 delta 的边界 ──────────────────────────────────────────────────────

def delta_scalars(path):
    out = {}
    for no, line in enumerate(Path(path).read_text(encoding='utf-8').splitlines(), 1):
        m = SCALAR.match(line)
        if not m or not m.group(2).startswith('"'):
            continue
        key, raw = m.groups()
        try:
            value = json.loads(raw)
        except Exception as e:                                   # noqa: BLE001
            raise DataError('%s 第 %d 行的 %s 解析失败：%s' % (path, no, key, e)) from e
        if isinstance(value, str):
            if key in out:
                raise DataError('%s 内部重复键：%s' % (path, key))
            out[key] = value
    return out


def ownership_issues(values, delta_root=DELTA_ROOT, output=OUTPUT):
    """生成器管的键，不许同时还被某个手写 delta 攥着。

    出过「以为改好了其实改的是另一份」这类事故：两处都定义同一个键，最后靠
    合并顺序决定谁赢。这里不猜谁该赢，直接要求人先移交。
    """
    owners = {}
    skip = Path(output).resolve()
    for path in sorted(Path(delta_root).rglob('zz_hanhua_*.snbt')):
        if path.resolve() == skip:
            continue
        for key in delta_scalars(path):
            if key in owners:
                raise DataError('手写 delta 重复键：%s 同时在 %s 与 %s'
                                % (key, owners[key], path))
            owners[key] = path
    return ['生成键 %s 仍由手写文件 %s 持有，需先移交' % (k, owners[k])
            for k in sorted(set(values) & set(owners))]


def existing_values(path):
    """读回入库的生成物。形状不对就拒绝覆盖——那说明有人手改过它。"""
    lines = Path(path).read_text(encoding='utf-8').splitlines()
    if len(lines) < 2 or lines[0] != '{' or lines[-1] != '}':
        raise DataError('%s 不是预期的纯生成 SNBT' % path)
    out = {}
    for no, line in enumerate(lines[1:-1], 2):
        m = SCALAR.match(line)
        if not m:
            raise DataError('%s 第 %d 行不是单行标量，拒绝覆盖' % (path, no))
        key, raw = m.groups()
        try:
            value = json.loads(raw)
        except Exception as e:                                   # noqa: BLE001
            raise DataError('%s 第 %d 行解析失败：%s' % (path, no, e)) from e
        if not isinstance(value, str) or key in out:
            raise DataError('%s 第 %d 行不是唯一字符串键，拒绝覆盖' % (path, no))
        out[key] = value
    return out


# ── 版本画像 ────────────────────────────────────────────────────────────────

def declared_versions():
    out = sorted(p.name for p in (ROOT / 'versions').iterdir()
                 if p.is_dir() and p.name[:1].isdigit())
    if not out:
        raise DataError('versions/ 下一个整合包版本都没有')
    return out


def jar_for(version, mods_dir):
    """按画像定位该版的 jar，**不按通配符在目录里瞎找**。

    名字来自 versions/db/<版本>/jars.json，取不到就红：宁可红，也不要
    「目录里恰好有个别的版本的 jar」被当成这一版的数据悄悄用上。
    """
    db = ROOT / 'versions' / 'db' / version / 'jars.json'
    if not db.is_file():
        raise DataError('没有 %s——该版本还没入库' % db)
    jars = json.loads(db.read_text(encoding='utf-8')).get('jars')
    if not isinstance(jars, dict):
        raise DataError('%s 里没有 jars 表' % db)
    hit = sorted(n for n in jars if n.lower().startswith(JAR_PREFIX))
    if len(hit) != 1:
        raise DataError('ATM10 %s 的画像里以 %r 开头的 jar 应恰有一个，实际 %d 个'
                        % (version, JAR_PREFIX, len(hit)))
    path = Path(mods_dir) / hit[0]
    if not path.is_file():
        raise DataError('%s 不存在——先跑 scripts/fetch_one_jar.py %s %s %s'
                        % (path, version, JAR_PREFIX, mods_dir))
    return path


def read_pack(root, version=None):
    """从一个包目录读出生成所需的三样输入。"""
    root = Path(root)
    chapter, quest_lang = root / CHAPTER, root / EN_QUEST
    for path, label in ((chapter, '任务章节'), (quest_lang, '英文任务语言')):
        if not path.is_file():
            raise DataError('%s不存在：%s' % (label, path))
    if version:
        jar = jar_for(version, root / 'mods')
    else:
        hit = sorted((root / 'mods').glob(JAR_PREFIX + '*.jar'))
        if len(hit) != 1:
            raise DataError('%s/mods 下以 %r 开头的 jar 应恰有一个，实际 %d 个'
                            % (root, JAR_PREFIX, len(hit)))
        jar = hit[0]
    return (chapter.read_text(encoding='utf-8'),
            quest_lang.read_text(encoding='utf-8'), jar)


def generate_all(versions, pack_root, zh):
    """逐版本生成并要求结果一致。返回 ``(共同结果, {版本: 用的 jar 名})``。"""
    if pack_root:
        chapter, lang, jar = read_pack(pack_root)
        return generate(chapter, lang, jar, zh), {'（本机）': jar.name}

    results, jars = {}, {}
    for v in versions:
        root = PACKSRC / v
        if not root.is_dir():
            raise DataError('%s 不存在——先跑 scripts/fetch_pack.py %s %s --no-jars'
                            % (root, v, root))
        chapter, lang, jar = read_pack(root, v)
        results[v] = generate(chapter, lang, jar, zh)
        jars[v] = jar.name

    base = versions[0]
    for v in versions[1:]:
        if results[v] == results[base]:
            continue
        a, b = results[base], results[v]
        diff = sorted(set(a) ^ set(b)) + sorted(k for k in set(a) & set(b) if a[k] != b[k])
        raise DataError(
            'ATM10 %s 与 %s 生成的育种公式不一致，%d 个键分叉：%s\n'
            '   一份共用的生成物已经描述不了所有版本了。把分叉的那版拆成\n'
            '   versions/<版本>/quest_overrides.snbt 的专属覆盖。'
            % (base, v, len(diff), '、'.join(diff[:12]) + ('…' if len(diff) > 12 else '')))
    return results[base], jars


# ── 入口 ────────────────────────────────────────────────────────────────────

def parse_args(argv):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument('--only', nargs='+', metavar='版本',
                   help='只跑这几个在册版本；默认全部')
    p.add_argument('--pack-root', type=Path,
                   help='改用一个本机 ATM 实例，绕开版本画像（调试用，不做一致性检查）')
    p.add_argument('--lang', type=Path, default=ZH_LANG, help='本包的树名中文 lang')
    p.add_argument('--output', type=Path, default=OUTPUT, help='纯生成 SNBT 的路径')
    mode = p.add_mutually_exclusive_group()
    mode.add_argument('--write', action='store_true', help='写入 --output；默认只预览')
    mode.add_argument('--check', action='store_true', help='检查 --output 与生成结果逐字一致')
    return p.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    try:
        if args.output.resolve() == MANUAL_DELTA.resolve():
            raise DataError('拒绝覆盖手写任务文件 %s；生成物必须自己一个文件'
                            % args.output)
        versions = args.only or declared_versions()
        zh = json.loads(Path(args.lang).read_text(encoding='utf-8-sig'))
        values, jars = generate_all(versions, args.pack_root, zh)
        text = render(values)

        issues = ownership_issues(values, output=args.output)
        if (args.write or args.check) and issues:
            raise DataError('任务键所有权没就绪：\n   ' + '\n   '.join(issues))

        if args.check:
            if not args.output.is_file():
                raise DataError('待检查的生成物不存在：%s' % args.output)
            if args.output.read_text(encoding='utf-8') != text:
                raise DataError('%s 与当前配方／树名对不上，改完树名要重跑 --write'
                                % args.output)
            action = '检查通过'
        elif args.write:
            if args.output.is_file():
                foreign = sorted(set(existing_values(args.output)) - set(values))
                if foreign:
                    raise DataError('%s 里有本生成器不管理的键，拒绝删除：%s'
                                    % (args.output, '、'.join(foreign)))
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(text, encoding='utf-8')
            action = '已写入 %s' % args.output
        else:
            sys.stdout.write(text)
            action = '仅预览'

        subtitles = sum(1 for k in values if k.endswith('.quest_subtitle'))
        print('✅ 资源树育种公式%s：%d 条副标题 + %d 条标题；'
              '%d 个版本结果一致（%s）'
              % (action, subtitles, len(values) - subtitles, len(jars),
                 '、'.join('%s→%s' % kv for kv in jars.items())), file=sys.stderr)
        if issues:
            print('⚠️ 写入前待处理：\n   %s' % '\n   '.join(issues), file=sys.stderr)
        return 0
    except DataError as e:
        print('❌ %s' % e, file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
