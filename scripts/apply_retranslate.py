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
   例外只有一种：**这个词在中文语境里本来就用英文原名**——判据不是「我觉得它是
   品牌名」，而是**模组自带的中文或 CFPA 译文里也照写英文**（通用机械的官方中文
   就写「MekaSuit能量条」「QIO驱动器阵列」）。拿不出这个证据就不许保留英文：
   玩家认的是习惯译名，不是英文原名。

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
        def bare(x):
            return re.sub(r'[^0-9a-z]', '', re.sub(r'[§&][0-9a-fk-orA-FK-OR]', '', x).lower())
        if bare(zh) != bare(en):
            return '译文里一个汉字都没有，也不是原样保留原文'
        if not kept_in_chinese(en):
            return '保留成英文，但中文来源里查不到同样保留的先例'
    return ''


_TRUSTED_CN = None


def trusted_cn():
    """模组自带中文 + CFPA 的全部译文，用来查「这个词中文语境里是否照写英文」。"""
    global _TRUSTED_CN
    if _TRUSTED_CN is None:
        vals = []
        for p in (ROOT / 'src' / 'pack' / 'assets').glob('*/lang/zh_cn.json'):
            try:
                vals += [v for v in json.loads(p.read_text(encoding='utf-8-sig')).values()
                         if isinstance(v, str)]
            except Exception:                              # noqa: BLE001
                pass
        _TRUSTED_CN = '\n'.join(vals)
    return _TRUSTED_CN


_KEEP = None


def keep_list():
    """明确批准保留英文的词表（src/rules/keep_english.json），每条都写了理由。"""
    global _KEEP
    if _KEEP is None:
        p = ROOT / 'src' / 'keep_english.json'
        d = json.loads(p.read_text(encoding='utf-8')) if p.is_file() else {}
        _KEEP = {k.lower() for k in d if not k.startswith('_')}
    return _KEEP


def kept_in_chinese(en):
    """这个英文词在**中文译文里**是否也照写英文（且那条译文确实是中文）。"""
    # 先剥掉 `&a`/`§c` 这类格式码，否则 `&aMekaSuit` 会被切成 `aMekaSuit`，
    # 拿这个去查当然查不到——闸自己造出假阳性
    clean = re.sub(r'[§&][0-9a-fk-orA-FK-OR]', '', en)
    words = [w for w in re.findall(r"[A-Za-z][A-Za-z0-9'-]{2,}", clean)]
    if not words:
        return True                       # 纯符号/占位符，本来就没什么可译
    keep = keep_list()
    if all(w.lower() in keep for w in words):
        return True
    hay = trusted_cn()
    for w in words:
        for line in hay.split('\n'):
            if w in line and CJK.search(line):
                return True
    return False


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
