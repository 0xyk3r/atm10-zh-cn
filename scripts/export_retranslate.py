#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# All the Mods 10 简体中文汉化补丁 · 绿油油版
# Copyright (C) 2026 星野夢華 (Hoshino Yumeka)
# SPDX-License-Identifier: GPL-3.0-or-later
"""把「要重译的底本残留」导成工作包。

`scripts/audit_base.py` 找出哪些译文与底本一字不差且没有替代来源。这些必须重写。
重写要有英文原文才做得了，所以这里把原文配齐再分批导出：

    lang         原文取自模组 jar 里的 `en_us.json`
    vaultpatcher 原文就是替换对的 key 本身（VaultPatcher 按原文匹配）
    quests       原文取自整合包自己的 `config/ftbquests/quests/lang/en_us.snbt`

每个工作包还带一份**术语提示**：同一命名空间下我们已有的译文里，出现频次最高的
那些词。重译时必须跟着它们走——一致性比单条的文采重要。

用法:
    python3 scripts/export_retranslate.py --out <目录> \\
        --mods <整合包 mods 目录> --pack <整合包根目录> [--size 60]
"""
import json
import re
import sys
import zipfile
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SNBT = re.compile(r'^\s*([\w.\-]+):\s*"(.*)"\s*$')
CJK = re.compile(r'[一-鿿]{2,6}')


def en_of_jars(mods):
    out = {}
    for j in sorted(Path(mods).glob('*.jar')):
        try:
            z = zipfile.ZipFile(j)
        except Exception:                                  # noqa: BLE001
            continue
        for n in z.namelist():
            if n.startswith('assets/') and n.endswith('/lang/en_us.json'):
                try:
                    out.setdefault(n.split('/')[1], {}).update(
                        json.loads(z.read(n).decode('utf-8-sig')))
                except Exception:                          # noqa: BLE001
                    pass
    return out


def glossary(ns):
    """这个命名空间我们已有译文里的高频词，重译时照着用。"""
    p = ROOT / 'src' / 'pack' / 'assets' / ns / 'lang' / 'zh_cn.json'
    if not p.is_file():
        return []
    kv = json.loads(p.read_text(encoding='utf-8-sig'))
    c = Counter()
    for v in kv.values():
        if isinstance(v, str):
            c.update(CJK.findall(v))
    return [w for w, n in c.most_common(40) if n >= 3]


def main(out_dir, mods, pack, size=60):
    res = json.loads((ROOT / 'versions' / 'base_residue.json').read_text(encoding='utf-8'))
    en = en_of_jars(mods)
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    jobs = []

    # 1. 语言条目里的散文（短名交给合成器，不进这里）
    for ns, items in res['lang_selftrans'].items():
        E = en.get(ns, {})
        for k, v in items:
            if not isinstance(v, str) or len(v) <= 12:
                continue
            jobs.append({'kind': 'lang', 'ns': ns, 'key': k,
                         'en': E.get(k), 'old': v})

    # 2. VaultPatcher：key 就是英文原文
    vp = {}
    for p in (ROOT / 'src' / 'vaultpatcher' / 'modules').glob('*.json'):
        try:
            d = json.loads(p.read_text(encoding='utf-8-sig'))
        except Exception:                                  # noqa: BLE001
            continue
        for blk in d if isinstance(d, list) else []:
            for pr in (blk.get('pairs') or []):
                if isinstance(pr, dict) and 'key' in pr:
                    vp[pr['key']] = (p.name, pr.get('value'))
    for k in res['vaultpatcher_same']:
        if k in vp:
            f, v = vp[k]
            jobs.append({'kind': 'vaultpatcher', 'file': f, 'key': k,
                         'en': k, 'old': v})

    # 3. 任务书
    qen = {}
    q = Path(pack) / 'config' / 'ftbquests' / 'quests' / 'lang' / 'en_us.snbt'
    if q.is_file():
        for line in q.read_text(encoding='utf-8', errors='replace').splitlines():
            m = SNBT.match(line)
            if m:
                qen[m.group(1)] = m.group(2)
    qzh = {}
    for p in (ROOT / 'src' / 'config' / 'ftbquests').rglob('*.snbt'):
        for line in p.read_text(encoding='utf-8', errors='replace').splitlines():
            m = SNBT.match(line)
            if m:
                qzh[m.group(1)] = (p.relative_to(ROOT).as_posix(), m.group(2))
    for k in res['quests_same']:
        if k in qzh:
            f, v = qzh[k]
            jobs.append({'kind': 'quest', 'file': f, 'key': k,
                         'en': qen.get(k), 'old': v})

    gl = {}
    for j in jobs:
        ns = j.get('ns')
        if ns and ns not in gl:
            gl[ns] = glossary(ns)

    batches = [jobs[i:i + size] for i in range(0, len(jobs), size)]
    for i, b in enumerate(batches):
        (out / ('batch-%02d.json' % i)).write_text(json.dumps(
            {'items': b,
             'glossary': {j['ns']: gl.get(j['ns'], []) for j in b if j.get('ns')}},
            ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    kinds = Counter(j['kind'] for j in jobs)
    noen = sum(1 for j in jobs if not j['en'])
    print('导出 %d 条待重译，分 %d 个工作包 → %s' % (len(jobs), len(batches), out))
    print('   按类型：%s' % dict(kinds))
    print('   其中 %d 条找不到英文原文（模组已不在这一版整合包里）' % noen)
    return len(jobs)


if __name__ == '__main__':
    a = sys.argv[1:]

    def arg(n, d=None):
        return a[a.index(n) + 1] if n in a else d

    if '--out' not in a:
        sys.exit(__doc__)
    main(arg('--out'), arg('--mods'), arg('--pack'), int(arg('--size', '60')))
