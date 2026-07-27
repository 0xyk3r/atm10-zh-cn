#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# atm10-zh-cn — All the Mods 10 简体中文汉化补丁「绿油油版」
# Copyright (C) 2026 星野夢華 (Hoshino Yumeka)
# SPDX-License-Identifier: GPL-3.0-or-later
"""把 src/pack 里的导览书译文反解成映射，存进 src/books/。

## 为什么导览书不能整份提交

Patchouli / AE2 Guide / Modonomicon 这类导览书，译文是**上游 JSON 的整份副本**，
只有里面的字符串换成了中文。结构、页码、配方引用全是上游的。这意味着：

- 模组更新导览书（加一页、改配方、拆章节），我们那份旧副本会把新内容整个盖掉，
  玩家永远看不到，**而且没有任何报错**。
- 已现形的实例（2026-07-27 实测）：
  `pneumaticcraft/…/programming/conditions.json` 上游多出 `pages[8].entries[9]`，
  `pneumaticcraft/…/tools/drone.json` 上游的 `pages[7].title` / `pages[8]` 整段变了
  而我们那份错位——这两页此刻就在吞掉上游内容。

所以仓库里只留「哪个位置、原文是什么、译成什么」，构建时拿**目标版本 jar 里的
那份 JSON** 重新套一遍：上游加的页原样保留（暂时是英文），上游改过的位置会被点名。

## 三种文件、三种存法

| 类型 | 例子 | 存什么 |
|---|---|---|
| 结构型 JSON | patchouli 条目、`_meta.json` | `src/books/<路径>.json`：路径 + 原文 + 译文 |
| 散文 | `.md` / `.mdx` / `.txt` / `.gui` | 译文留在 `src/pack`，`_prose.json` 记英文源指纹 |
| 与上游完全相同 | 没翻的条目副本 | 只记一行路径，构建时从 jar 拷，不入库 |

用法:
    python3 scripts/extract_books.py <该版 mods 目录>
"""
import json
import sys
from collections import Counter
from pathlib import Path

import books
from paths import SRC

PACK = SRC / 'pack'
# 这些前缀下的东西是导览书/手册，归本脚本管；lang/ 与本包独有资源不动
BOOK_DIRS = ('patchouli_books', 'ae2guide', 'modopedia', 'books', 'guides',
             'guidebook', 'guide', 'mi_guidebook', 'mj_guide', 'text',
             'manual', 'gui', '_zh_cn')
PROSE_EXT = {'.md', '.mdx', '.txt', '.gui', '.snbt'}


def is_book(rel):
    parts = rel.split('/')
    return len(parts) > 2 and parts[0] == 'assets' and parts[2] in BOOK_DIRS


def candidates(p):
    out = []
    if '/.translated/zh_cn/' in p:
        out.append(p.replace('/.translated/zh_cn/', '/'))
    if '/_zh_cn/' in p:
        out.append(p.replace('/_zh_cn/', '/', 1))
    if '/zh_cn/' in p:
        out.append(p.replace('/zh_cn/', '/en_us/'))
        out.append(p.replace('/zh_cn/', '/'))
    if p.endswith('-zh_cn.txt'):
        out.append(p[:-len('-zh_cn.txt')] + '.txt')
    out.append(p)
    seen, r = set(), []
    for c in out:
        if c not in seen:
            seen.add(c)
            r.append(c)
    return r


def main(mods_dir):
    jars = books.Jars(mods_dir)
    print('jar 内条目 %d 条' % len(jars.index))
    if books.BOOKS.exists():
        import shutil
        shutil.rmtree(books.BOOKS)

    stat = Counter()
    copies, prose, odd = {}, {}, []
    for f in sorted(PACK.rglob('*')):
        if not f.is_file() or f.name == '.DS_Store':
            continue
        rel = f.relative_to(PACK).as_posix()
        if not is_book(rel):
            continue
        data = f.read_bytes()
        src = next((c for c in candidates(rel) if c in jars.index), None)
        if src is None:
            stat['上游没有（本包独有或模组不在整合包里）'] += 1
            continue
        up = jars.read(src)
        if books.sha1(up) == books.sha1(data):
            copies[rel] = src
            stat['与上游完全相同'] += 1
            continue
        if f.suffix.lower() in PROSE_EXT:
            prose[rel] = {'src': src, 'sha1': books.sha1(up)}
            stat['散文（记指纹）'] += 1
            continue
        if f.suffix.lower() != '.json':
            stat['二进制且与上游不同（本包重绘，原样保留）'] += 1
            continue
        try:
            en = json.loads(up.decode('utf-8-sig'))
            zh = json.loads(data.decode('utf-8-sig'))
        except Exception as e:
            odd.append((rel, 'JSON 解析失败: %r' % e))
            stat['解析失败（原样保留）'] += 1
            continue
        pe = dict(books.walk(en))
        matched = list(books.pair(en, zh))
        t = [[p, a, b] for p, a, b in matched if a != b]
        # 上游有、我们没对上的字符串位置：上游新加的内容，暂时保持英文
        untr = len(pe) - len(matched)
        if untr:
            odd.append((rel, '上游有 %d 处字符串我们没有对应译文（上游新增/改过，保持英文）' % untr))
            stat['上游有新内容（保持英文）'] += 1
        if not t:
            copies[rel] = src           # 结构同、字符串也同 → 等价于纯拷贝
            stat['与上游完全相同'] += 1
            continue
        books.dump(rel, {'src': src, 'sha1': books.sha1(up), 't': t})
        stat['结构型 JSON（转成映射）'] += 1

    books.BOOKS.mkdir(parents=True, exist_ok=True)
    books.MAP_COPIES.write_text(
        json.dumps(copies, ensure_ascii=False, indent=1, sort_keys=True) + '\n',
        encoding='utf-8')
    books.MAP_PROSE.write_text(
        json.dumps(prose, ensure_ascii=False, indent=1, sort_keys=True) + '\n',
        encoding='utf-8')

    print()
    for k, v in stat.most_common():
        print('  %-40s %5d' % (k, v))
    if odd:
        print('\n⚠️ 需要人工看的 %d 个：' % len(odd))
        for rel, why in odd:
            print('   %s\n      %s' % (rel, why))


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
