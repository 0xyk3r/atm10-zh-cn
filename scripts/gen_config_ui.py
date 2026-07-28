#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# atm10-zh-cn — All the Mods 10 简体中文汉化补丁「绿油油版」
# Copyright (C) 2026 星野夢華 (Hoshino Yumeka)
# SPDX-License-Identifier: GPL-3.0-or-later
"""配置界面标签汉化：扫全部 config，逐词查词典，能全查到才输出。

## 为什么不能靠翻译键

这类界面（Create/AE2/…用的 catnip ConfigScreen）**没有翻译键**：它把字段名
`maxCellContentShown` 按驼峰拆成 `Max Cell Content Shown` 现拼出来。实测全部 jar
里搜不到这个串，语言文件够不着，只能按最终字符串做 dynamic 替换。

## 为什么不能一条条手写

整合包里 14000+ 个配置项。手挑永远追不上，而且同一个词在不同模组里译法会飘。
所以改成**逐词词典 + 生成器**（src/config_ui_terms.json）：

- 字段名拆成词 → 每个词都在词典里查得到才拼出译文
- **只要有一个词查不到，整条跳过**——不猜，宁可留英文
- 要扩覆盖面就往词典加词，一次加词全整合包受益，译法自动统一

## 目标类限定

替换限定在配置界面那几个类里。不这么做的话，「Sound」「Client」这种通用词
会把别的界面一起改掉。

用法:
    python3 scripts/gen_config_ui.py [<实例目录>]
"""
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'src' / 'vaultpatcher' / 'modules' / 'config_ui_generated.json'
TERMS = ROOT / 'src' / 'config_ui_terms.json'
CLASSES = ['net.createmod.catnip.config.ui.SubMenuConfigScreen',
           'net.createmod.catnip.config.ui.ConfigScreenList',
           'net.createmod.catnip.config.ui.BaseConfigScreen']
SKIP = re.compile(r'^[A-Z0-9_]+$')          # 全大写的多半是枚举值/常量，别碰


def label(key):
    s = re.sub(r'[_-]+', ' ', key)
    s = re.sub(r'(?<=[a-z0-9])(?=[A-Z])', ' ', s)
    return ' '.join(w[0].upper() + w[1:] if w and w[0].islower() else w for w in s.split())


def main(argv):
    inst = Path(argv[0]) if argv else Path(os.environ.get('ATM_PACK_ROOT', ''))
    cfg = inst / 'config'
    if not cfg.is_dir():
        print('ℹ️ 没有 config 目录，跳过（给个实例目录或设 ATM_PACK_ROOT）')
        return 0
    terms = json.loads(TERMS.read_text(encoding='utf-8'))['terms']
    labels = set()
    for f in list(cfg.rglob('*.toml')) + list(cfg.rglob('*.cfg')):
        try:
            txt = f.read_text(encoding='utf-8', errors='replace')
        except Exception:                                          # noqa: BLE001
            continue
        for m in re.finditer(r'^\s*\[?([A-Za-z][A-Za-z0-9_.-]*)\]?\s*[=\]]', txt, re.M):
            for part in m.group(1).split('.'):
                if part and not SKIP.match(part):
                    labels.add(label(part))
    pairs, skipped = [], 0
    for lb in sorted(labels):
        words = lb.split()
        zh = [terms.get(w) for w in words]
        if not words or any(v is None for v in zh):
            skipped += 1
            continue
        pairs.append({'key': lb, 'value': ''.join(zh)})
    doc = [{'name': 'config_ui_generated_zh_cn',
            'desc': ('配置界面标签（由 gen_config_ui.py 按 src/config_ui_terms.json 逐词生成）。'
                     '这些字没有翻译键，是把字段名按驼峰拆开现拼的，只能按最终字符串替换。'
                     '有一个词查不到词典就整条跳过，不猜。'),
            'authors': 'Hoshino Yumeka', 'dynamic': True, 'i18n': False}]
    for c in CLASSES:
        doc.append({'target_class': [c], 'pairs': pairs})
    OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('配置项标签共 %d 个；词典全覆盖的 %d 个已生成，%d 个因缺词跳过（不猜）'
          % (len(labels), len(pairs), skipped))
    print('   → %s' % OUT.relative_to(ROOT))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
