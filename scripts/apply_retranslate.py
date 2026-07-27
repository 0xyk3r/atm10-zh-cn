#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# All the Mods 10 简体中文汉化补丁 · 绿油油版
# Copyright (C) 2026 星野夢華 (Hoshino Yumeka)
# SPDX-License-Identifier: GPL-3.0-or-later
"""把重译的结果核过再回填。

重译是分批外包出去的，产出不能直接信——回填前逐条过闸：

1. **下标对得上**：结果里的 `i` 必须与工作包里的条目一一对应，不许漏、不许多；
2. **占位符一致**：`%s` `%d` `%1$s` `%%`、`$(l:…)$(/l)`、`§`/`&` 颜色码、`\\n`
   的**种类与个数**必须与英文原文相同。多一个少一个，游戏运行到那句就抛异常；
3. **确实换掉了**：译文与旧译文相同的，必须显式标了 `same_ok`——那是「这句话
   只有这一种译法」的声明，不是忘了改；
4. **确实是中文**：英文原文里有单词、译文却一个汉字都没有，判为没译。

过不了的条目**整条不回填**，列出来等人处理。宁可留着旧的，也不能填个会崩的。

用法:
    python3 scripts/apply_retranslate.py --batches <目录> [--write]
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOKENS = re.compile(r'%(?:\d+\$)?[a-zA-Z%]|\$\(l:[^)]*\)|\$\(/l\)|\$\(br2?\)|[§&][0-9a-fk-orA-FK-OR]|\\n')
CJK = re.compile(r'[一-鿿]')
WORD = re.compile(r'[A-Za-z]{2,}')


def tokens(s):
    return Counter(TOKENS.findall(s or ''))


def check(item, zh, same_ok):
    en, old = item.get('en'), item.get('old')
    if zh is None:
        return None                                    # 交白卷，保持原样
    if tokens(zh) != tokens(en):
        return '占位符对不上：原文 %s / 译文 %s' % (dict(tokens(en)), dict(tokens(zh)))
    if zh == old and not same_ok:
        return '与旧译文相同却没标 same_ok'
    if en and WORD.search(en) and not CJK.search(zh):
        return '译文里一个汉字都没有'
    return ''


def apply_lang(items, write):
    n = 0
    by_ns = {}
    for it, zh in items:
        by_ns.setdefault(it['ns'], []).append((it['key'], zh))
    for ns, kv in by_ns.items():
        p = ROOT / 'src' / 'pack' / 'assets' / ns / 'lang' / 'zh_cn.json'
        if not p.is_file():
            continue
        cur = json.loads(p.read_text(encoding='utf-8-sig'))
        for k, zh in kv:
            if cur.get(k) != zh:
                cur[k] = zh
                n += 1
        if write:
            p.write_text(json.dumps(cur, ensure_ascii=False, indent=2) + '\n',
                         encoding='utf-8')
    return n


def apply_vp(items, write):
    n = 0
    by_file = {}
    for it, zh in items:
        by_file.setdefault(it['file'], []).append((it['key'], zh))
    for f, kv in by_file.items():
        p = ROOT / 'src' / 'vaultpatcher' / 'modules' / f
        if not p.is_file():
            continue
        d = json.loads(p.read_text(encoding='utf-8-sig'))
        want = dict(kv)
        for blk in d if isinstance(d, list) else []:
            for pr in (blk.get('pairs') or []):
                if isinstance(pr, dict) and pr.get('key') in want:
                    zh = want[pr['key']]
                    if pr.get('value') != zh:
                        pr['value'] = zh
                        n += 1
        if write:
            p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n',
                         encoding='utf-8')
    return n


def apply_quest(items, write):
    n = 0
    by_file = {}
    for it, zh in items:
        by_file.setdefault(it['file'], []).append((it['key'], zh))
    for f, kv in by_file.items():
        p = ROOT / f
        if not p.is_file():
            continue
        lines = p.read_text(encoding='utf-8').split('\n')
        want = dict(kv)
        out = []
        for line in lines:
            m = re.match(r'^(\s*)([\w.\-]+):\s*"(.*)"\s*$', line)
            if m and m.group(2) in want:
                zh = want[m.group(2)].replace('"', '\\"')
                if m.group(3) != zh:
                    n += 1
                line = '%s%s: "%s"' % (m.group(1), m.group(2), zh)
            out.append(line)
        if write:
            p.write_text('\n'.join(out), encoding='utf-8')
    return n


def main(d, write=False):
    d = Path(d)
    ok, bad, blank = [], [], 0
    for bp in sorted(d.glob('batch-*.json')):
        op = d / bp.name.replace('batch-', 'out-')
        if not op.is_file():
            print('  ⚠️ %s 还没有结果，跳过' % bp.name)
            continue
        items = json.loads(bp.read_text(encoding='utf-8'))['items']
        res = json.loads(op.read_text(encoding='utf-8'))['results']
        seen = {r['i'] for r in res}
        if seen != set(range(len(items))):
            print('  ❌ %s 下标对不上：期望 0..%d，实得 %d 个'
                  % (op.name, len(items) - 1, len(seen)))
            continue
        for r in res:
            it = items[r['i']]
            zh = r.get('zh')
            if zh is None:
                blank += 1
                continue
            why = check(it, zh, r.get('same_ok'))
            (bad if why else ok).append((it, zh, why))
    print('通过 %d 条 / 交白卷 %d 条 / 不合格 %d 条' % (len(ok), blank, len(bad)))
    for it, zh, why in bad[:15]:
        print('   ❌ %-46s %s' % (str(it.get('key'))[:46], why))
        print('      原文 %r\n      译文 %r' % ((it.get('en') or '')[:70], zh[:70]))

    good = [(it, zh) for it, zh, _ in ok]
    kinds = Counter(it['kind'] for it, _ in good)
    n = 0
    n += apply_lang([x for x in good if x[0]['kind'] == 'lang'], write)
    n += apply_vp([x for x in good if x[0]['kind'] == 'vaultpatcher'], write)
    n += apply_quest([x for x in good if x[0]['kind'] == 'quest'], write)
    print('%s %d 条（%s）' % ('已回填' if write else '可回填', n, dict(kinds)))
    return len(bad)


if __name__ == '__main__':
    a = sys.argv[1:]
    if '--batches' not in a:
        sys.exit(__doc__)
    sys.exit(1 if main(a[a.index('--batches') + 1], '--write' in a) else 0)
