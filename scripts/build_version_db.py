#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# atm10-zh-cn — All the Mods 10 简体中文汉化补丁「绿油油版」
# Copyright (C) 2026 星野夢華 (Hoshino Yumeka)
# SPDX-License-Identifier: GPL-3.0-or-later
"""为某个 ATM10 版本建 VaultPatcher 的**专属**数据库。

## 为什么要一版一份

VaultPatcher 靠字符串精确匹配替换硬编码文本，而且失配是**静默**的——对不上就是不替换，
玩家看到英文，日志一个字都没有。模组在整合包版本之间升级会带来两类破坏：

1. **类改名 / 搬家**：整块补丁失效。实测 7.2 里就有 6 处
   （`ToolbarPanel` 变成了内部类、RFTools 的 `GuiTools` 搬进了 mcjtylib……）
2. **文案改写**：单条 key 失效。industrialization_overdrive 1.11.2→1.12.1 就换了措辞。

所以不能拿一份模块文件同时发给 7.0/7.1/7.2 —— 那等于对老版本闭着眼睛发。
这里对着**该版本真实的 jar** 逐条核验，产出这一版专属的：

- 每个 target_class 在这一版的**实际位置**（搬了家就自动找回来）
- 每条 key 在这一版是否存在（exact / substring / missing）
- 每个模块命中的 jar **精确文件名**（带版本号，作为门控与追溯依据）

打包时按这份数据库生成版本专属的模块：搬了家的类改成该版真实位置、
这一版不存在的 key 剔掉，并附覆盖率报告。

## 类搬家了怎么自动找回

先按声明的全限定名找；找不到就在全部 jar 里找**同简单类名**的候选，
取常量池里命中本块 key 最多的那个。命中 0 条的不算数——宁可报「找不到」，
也不要张冠李戴把补丁打到别的类上。

用法:
    python3 scripts/build_version_db.py 7.1 <该版本的mods目录>
"""
import json
import sys
import zipfile
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))
from check_vaultpatcher_strings import utf8_pool          # noqa: E402

MODULES = ROOT / 'vaultpatcher' / 'modules'


def build_index(mods_dir):
    by_path, by_simple = {}, defaultdict(list)
    for j in sorted(Path(mods_dir).glob('*.jar')):
        try:
            with zipfile.ZipFile(j) as z:
                names = [n for n in z.namelist() if n.endswith('.class')]
        except Exception:
            continue
        for n in names:
            by_path.setdefault(n, j)
            by_simple[n.rsplit('/', 1)[-1][:-6]].append(n)
    return by_path, by_simple


def pool_of(by_path, cls_path, cache):
    """该类 + 其内部类的常量池字符串"""
    if cls_path in cache:
        return cache[cls_path]
    jar = by_path.get(cls_path)
    if jar is None:
        cache[cls_path] = (None, [])
        return cache[cls_path]
    base = cls_path[:-6]
    out = []
    with zipfile.ZipFile(jar) as z:
        for n in [cls_path] + [p for p in by_path
                               if p.startswith(base + '$') and by_path[p] == jar]:
            try:
                out += utf8_pool(z.read(n))
            except Exception:
                pass
    cache[cls_path] = (jar.name, out)
    return cache[cls_path]


def resolve(declared, keys, by_path, by_simple, cache):
    """声明的类在这一版的实际位置；搬家了就按 key 命中数找回"""
    p = declared.replace('.', '/') + '.class'
    if p in by_path:
        jar, pool = pool_of(by_path, p, cache)
        return declared, jar, pool, 'declared'
    simple = declared.split('.')[-1].split('$')[-1]
    best = None
    for cand in by_simple.get(simple, []):
        jar, pool = pool_of(by_path, cand, cache)
        blob = '\n'.join(pool)
        hit = sum(1 for k in keys if k in blob)
        if hit and (best is None or hit > best[0]):
            best = (hit, cand[:-6].replace('/', '.'), jar, pool)
    if best:
        return best[1], best[2], best[3], 'moved'
    return None, None, [], 'not_found'


def main(ver, mods_dir):
    by_path, by_simple = build_index(mods_dir)
    cache = {}
    print('%s: 索引 %d 个 class' % (ver, len(by_path)))
    db, stat = {}, defaultdict(int)
    for f in sorted(MODULES.glob('*.json')):
        try:
            blocks = json.loads(f.read_text(encoding='utf-8'))
        except Exception as e:
            sys.exit('❌ %s 解析失败: %s' % (f.name, e))
        rec = {'blocks': []}
        for bi, blk in enumerate(blocks):
            if not isinstance(blk, dict) or 'pairs' not in blk:
                continue
            keys = [p['key'] for p in blk['pairs'] if p.get('key')]
            tcs = blk.get('target_class') or []
            if not tcs:
                stat['global_block'] += 1
                rec['blocks'].append({'i': bi, 'global': True})
                continue
            classes, jars, pool = {}, [], []
            for tc in tcs:
                actual, jar, pl, how = resolve(tc, keys, by_path, by_simple, cache)
                classes[tc] = {'actual': actual, 'jar': jar, 'how': how}
                stat['class_' + how] += 1
                if jar and jar not in jars:
                    jars.append(jar)
                pool += pl
            ps, blob = set(pool), '\n'.join(pool)
            kv = {}
            for k in keys:
                s = 'exact' if k in ps else ('substring' if k in blob else 'missing')
                kv[k] = s
                stat['key_' + s] += 1
            rec['blocks'].append({'i': bi, 'classes': classes, 'jars': jars, 'keys': kv})
        if rec['blocks']:
            db[f.name] = rec
    out = ROOT / 'versions' / 'db' / ver
    out.mkdir(parents=True, exist_ok=True)
    (out / 'vaultpatcher.json').write_text(
        json.dumps(db, ensure_ascii=False, indent=1, sort_keys=True) + '\n', encoding='utf-8')
    (out / 'jars.json').write_text(
        json.dumps(sorted(p.name for p in Path(mods_dir).glob('*.jar')),
                   ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    tot = stat['key_exact'] + stat['key_substring'] + stat['key_missing']
    print('  target_class: 原位 %d / 搬家已找回 %d / 找不到 %d'
          % (stat['class_declared'], stat['class_moved'], stat['class_not_found']))
    print('  key: 命中 %d + 子串 %d = %d，缺 %d  → 覆盖率 %.1f%%'
          % (stat['key_exact'], stat['key_substring'],
             stat['key_exact'] + stat['key_substring'], stat['key_missing'],
             100 * (tot - stat['key_missing']) / max(1, tot)))
    print('  写入 versions/db/%s/' % ver)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
