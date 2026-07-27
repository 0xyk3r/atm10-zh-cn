#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# atm10-zh-cn — All the Mods 10 简体中文汉化补丁「绿油油版」
# Copyright (C) 2026 星野夢華 (Hoshino Yumeka)
# SPDX-License-Identifier: GPL-3.0-or-later
"""把 src/books/ 的映射套到**模组 jar 里那份导览书**上，产出资源包里的中文版。

仓库里没有任何一份导览书副本（原因见 extract_books.py）。这里现取上游 JSON、
逐条套译文：上游新加的页原样保留（暂时英文），上游改过的位置会被点名。

## 判定是「漂移」还是「换了版本」

每条映射都记着提取时那份上游文件的 sha1：

- **sha1 对得上** → 上游文件跟提取时一模一样，那么每一条译文都必须落位。
  落不下就是本脚本自己有 bug，**硬失败**。
- **sha1 对不上** → 上游改过了（或者这是另一个整合包版本、模组版本不同）。
  尽力套，落不下的逐条计数；整体命中率跌破下限就失败，避免「悄悄少翻一半」。

用法:
    python3 scripts/gen_books.py <mods 目录>
    # 不给参数就用 ATM_PACK_ROOT/mods
"""
import json
import os
import sys
from pathlib import Path

import books
from paths import PACK

# 命中率下限：低于这个数说明不是零星漂移，而是整块对不上了
MIN_HIT = 0.90


def apply_one(doc, entries, rel, strict, miss):
    """把 [路径, 英文原文, 中文] 逐条套到 doc 上。返回落位条数。"""
    ok = 0
    for path, en, zh in entries:
        path = tuple(path)
        cur = books.get_at(doc, path)
        if cur == en:
            books.set_at(doc, path, zh)
            ok += 1
            continue
        # 位置漂了（上游插了一页之类）：全文找这段原文，唯一命中就照样翻
        where = [p for p, v in books.walk(doc) if v == en]
        if len(where) == 1:
            books.set_at(doc, where[0], zh)
            ok += 1
            continue
        if strict:
            sys.exit('❌ %s 的 %s 套不上，但上游文件与提取时逐字节相同——\n'
                     '   这是 gen_books.py 自己的 bug，不是上游漂移。\n'
                     '   原文: %r' % (rel, list(path), en[:80]))
        miss.append((rel, path, en[:60]))
    return ok


def main(mods_dir):
    jars = books.Jars(mods_dir)
    if not books.BOOKS.is_dir():
        sys.exit('❌ 没有 %s' % books.BOOKS)

    n_copy = n_skip = 0
    copies = json.loads(books.MAP_COPIES.read_text(encoding='utf-8'))
    for rel, src in copies.items():
        data = jars.read(src)
        if data is None:
            n_skip += 1                     # 该版本没这个模组/这个文件
            continue
        t = PACK / rel
        t.parent.mkdir(parents=True, exist_ok=True)
        t.write_bytes(data)
        n_copy += 1

    drift = []
    prose = json.loads(books.MAP_PROSE.read_text(encoding='utf-8'))
    for rel, info in prose.items():
        data = jars.read(info['src'])
        if data is None:
            n_skip += 1
            continue
        if books.sha1(data) != info['sha1']:
            drift.append(rel)

    total = ok = n_json = 0
    miss = []
    for mp in sorted(books.BOOKS.rglob('*.json')):
        if mp.parent == books.BOOKS and mp.name.startswith('_'):
            continue
        rel = mp.relative_to(books.BOOKS).as_posix()[:-len('.json')]
        doc = json.loads(mp.read_text(encoding='utf-8'))
        up = jars.read(doc['src'])
        if up is None:
            n_skip += 1
            continue
        obj = json.loads(up.decode('utf-8-sig'))
        strict = books.sha1(up) == doc['sha1']
        total += len(doc['t'])
        ok += apply_one(obj, doc['t'], rel, strict, miss)
        t = PACK / rel
        t.parent.mkdir(parents=True, exist_ok=True)
        t.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        n_json += 1

    rate = (ok / total) if total else 1.0
    print('导览书：结构型 %d 个文件、%d/%d 条译文落位（%.1f%%）；'
          '照搬 %d 个；该版本没有的跳过 %d 个'
          % (n_json, ok, total, rate * 100, n_copy, n_skip))
    if drift:
        print('  ⚠️ %d 个散文页的英文原稿与提取时不同（上游改过，译文可能已过时）：' % len(drift))
        for r in drift[:15]:
            print('       ' + r)
        if len(drift) > 15:
            print('       …另外 %d 个' % (len(drift) - 15))
    if miss:
        print('  ⚠️ %d 条译文没落位（上游改了那一段）：' % len(miss))
        for r, p, e in miss[:15]:
            print('       %s %s  %r' % (r, list(p), e))
        if len(miss) > 15:
            print('       …另外 %d 条' % (len(miss) - 15))
    if rate < MIN_HIT:
        sys.exit('❌ 导览书译文命中率 %.1f%% 低于下限 %.0f%%——不是零星漂移，是整块对不上了'
                 % (rate * 100, MIN_HIT * 100))


if __name__ == '__main__':
    d = sys.argv[1] if len(sys.argv) > 1 else (
        os.path.join(os.environ.get('ATM_PACK_ROOT', ''), 'mods'))
    if not d or not Path(d).is_dir():
        sys.exit(__doc__)
    main(d)
