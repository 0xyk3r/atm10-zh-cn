#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# atm10-zh-cn — All the Mods 10 简体中文汉化补丁「绿油油版」
# Copyright (C) 2026 星野夢華 (Hoshino Yumeka)
# SPDX-License-Identifier: GPL-3.0-or-later
"""产出某个整合包版本的 VaultPatcher 模块。

模块头部里的 `mods` / `desc` 写的是**带版本号的 jar 文件名**，例如
`OctoLib-NEOFORGE-0.6.2+1.21.jar`。整合包换一个版本，一大半模组的 jar 版本号就变了，
所以这两个字段**不可能有一份通用的**：手写死在仓库里，等于三个包里有两个是错的。
实测把 7.2 那份原样拿去比对：7.1 只有 116/152 对得上，7.0 只有 83/152。

所以仓库里的 `src/vaultpatcher/modules/*.json` 只留人写的那部分
（`name` / `authors` / `dynamic` / `i18n` + `target_class` + `pairs`），
`mods` 与 `desc` 由本脚本按 `versions/db/<版本>/vaultpatcher.json` 现填——
那份数据库是拿**该版真实字节码**逐块解出来的，记着每个目标类实际由哪个 jar 提供。

（`mods` 在 VaultPatcher 里只用于 debug 输出，真正的匹配靠 `target_class` +
常量池里的字符串。但它是发出去给人看的东西，写错就是错。）

用法:
    python3 scripts/gen_vaultpatcher.py <整合包版本> <输出目录>
"""
import json
import sys
from pathlib import Path

from paths import ROOT, SRC

MODULES = SRC / 'vaultpatcher' / 'modules'

# 这些模块留在 src/ 备查，但不随包发行（对应的上游类已改名或该组文本已由别处覆盖，
# 发出去只会增加加载体积与排查噪音）。出货侧另有闸复核包里确实没有它们。
SRC_ONLY = {'blockui_legacy_labels.json'}



def main(ver, out_dir):
    db_path = ROOT / 'versions' / 'db' / ver / 'vaultpatcher.json'
    if not db_path.is_file():
        sys.exit('❌ 没有 %s\n'
                 '   先跑: python3 scripts/build_version_db.py %s <该版 mods 目录>'
                 % (db_path, ver))
    db = json.loads(db_path.read_text(encoding='utf-8'))
    out = Path(out_dir) / 'vaultpatcher' / 'modules'
    out.mkdir(parents=True, exist_ok=True)

    n = 0
    nojar = []
    for p in sorted(MODULES.glob('*.json')):
        if p.name in SRC_ONLY:
            continue
        doc = json.loads(p.read_text(encoding='utf-8'))
        entry = db.get(p.name)
        if entry is None:
            sys.exit('❌ %s 的 %s 在该版数据库里没有记录——数据库过期了，重建它。'
                     % (ver, p.name))
        # 该版里，这个模块的目标类实际由哪些 jar 提供
        jars = []
        for b in entry['blocks']:
            for j in b.get('jars') or []:
                if j not in jars:
                    jars.append(j)
        head = dict(doc[0])
        if jars:
            head['desc'] = '%s 硬编码文本汉化' % '、'.join(jars)
            head['mods'] = ', '.join(jars)
        else:
            # 该版本里一个目标类都找不到：模块留着无害（匹配靠 target_class），
            # 但不能瞎填一个不存在的 jar 名。
            head['desc'] = '硬编码文本汉化（ATM10 %s 里未找到目标类）' % ver
            head['mods'] = ''
            nojar.append(p.name)
        # 字段顺序照 VaultPatcher 自带样例：name, desc, authors, mods, dynamic, i18n
        ordered = {}
        for k in ('name', 'desc', 'authors', 'mods', 'dynamic', 'i18n'):
            if k in head:
                ordered[k] = head[k]
        for k in head:
            ordered.setdefault(k, head[k])
        (out / p.name).write_text(
            json.dumps([ordered] + doc[1:], ensure_ascii=False, indent=2) + '\n',
            encoding='utf-8')
        n += 1
    # VaultPatcher 主配置里的 modules / mods 就是模块清单本身，可推导 → 现填。
    # 手维护的那份此刻已经漏了 6 个（我们自己加的 *_zh 模块全没进去）：
    # `load_all_modules` 为真时无害，一旦有人关掉它，这 6 个模块就静默失效。
    cfg_src = SRC / 'config' / 'vaultpatcher_asm' / 'config.json'
    cfg = json.loads(cfg_src.read_text(encoding='utf-8'))
    names = sorted(p.stem for p in MODULES.glob('*.json') if p.name not in SRC_ONLY)
    cfg_out = {'modules': names, 'mods': names}
    cfg_out.update(cfg)
    cfg_path = Path(out_dir) / 'config' / 'vaultpatcher_asm' / 'config.json'
    cfg_path.parent.mkdir(parents=True, exist_ok=True)
    cfg_path.write_text(json.dumps(cfg_out, ensure_ascii=False, indent=2) + '\n',
                        encoding='utf-8')

    print('VaultPatcher 模块：%d 个（ATM10 %s 的 jar 名现填），主配置清单 %d 条'
          % (n, ver, len(names)))
    if nojar:
        print('  该版本里找不到目标类的 %d 个：%s' % (len(nojar), '、'.join(nojar)))


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
