#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# atm10-zh-cn — All the Mods 10 简体中文汉化补丁「绿油油版」
# Copyright (C) 2026 星野夢華 (Hoshino Yumeka)
# SPDX-License-Identifier: GPL-3.0-or-later
"""把某个模组的汉化单独摘出来，发成**任何整合包都能用**的一份。

起因：资源蜜蜂的汉化本来只是这个补丁的一部分，但装了这个模组的整合包多得很，
不少人只想要这一块。

两个死规矩：

1. **不另抄一份**。内容来自同一份真源（`src/pack` 的 lang + `src/books` 的导览书
   映射），跟整合包版走同一条生成链。抄一份出来必然漂移，最后变成两个版本的译名。
2. **出包前对着目标 jar 点名**。`en_us` 的每个键、导览书的每个文件，都得有对应的
   中文；够不到 `coverage_floor` 就不出包。「装上去只翻了一半」比没翻还糟——
   玩家不会来报，只会觉得这包很烂。

产出两种形态，同样的内容：

- **资源包 zip**：丢进 `resourcepacks/`，手动启用。任何加载器、任何启动器都吃。
- **资源模组 jar**：丢进 `mods/`，自动生效，不用管资源包顺序。里面**没有一行
  Java**，用的是 NeoForge 的 `lowcodefml` 加载器（就是给纯资源/数据模组用的）。

用法:
    python3 scripts/gen_standalone.py productivebees <含该模组jar的目录> <版本号>
"""
import hashlib
import json
import shutil
import sys
import zipfile
from pathlib import Path

import gen_books
from paths import BUILD, PACK, ROOT, SRC

MANIFESTS = SRC / 'standalone'
OUT = ROOT / 'dist'


def find_jar(mods_dir, modid, want_name):
    """在目录里认出这个模组的 jar：先按记录的文件名，再按 modid 前缀。"""
    d = Path(mods_dir)
    p = d / want_name
    if p.is_file():
        return p
    cand = sorted(x for x in d.glob('*.jar') if x.name.lower().startswith(modid.lower()))
    if not cand:
        sys.exit('❌ %s 里找不到 %s 的 jar（想找 %s）' % (d, modid, want_name))
    return cand[-1]


def coverage(jar, ns, pack_root, floor):
    """对着 jar 里的 en_us 与导览书逐个点名，返回 (覆盖率字典, 问题清单)。"""
    bad = {}
    z = zipfile.ZipFile(jar)
    en_path = 'assets/%s/lang/en_us.json' % ns
    zh_file = pack_root / 'assets' / ns / 'lang' / 'zh_cn.json'
    rate = {}
    if en_path in z.namelist():
        en = json.loads(z.read(en_path))
        zh = json.loads(zh_file.read_text(encoding='utf-8')) if zh_file.is_file() else {}
        miss = sorted(set(en) - set(zh))
        rate['lang_keys'] = (len(en) - len(miss)) / max(1, len(en))
        if miss:
            bad['lang_keys'] = miss
    # 导览书：jar 里每个 en_us 页都得有一个 zh_cn 页
    books_en = [n for n in z.namelist()
                if n.startswith('assets/%s/patchouli_books/' % ns)
                and '/en_us/' in n and n.endswith('.json')]
    if books_en:
        miss = [n for n in books_en
                if not (pack_root / n.replace('/en_us/', '/zh_cn/')).is_file()]
        rate['book_files'] = (len(books_en) - len(miss)) / len(books_en)
        if miss:
            bad['book_files'] = miss
    fails = []
    for k, need in floor.items():
        if k.startswith('_'):
            continue
        got = rate.get(k)
        if got is None:
            continue
        if got < need:
            fails.append('%s 覆盖率 %.1f%% 低于下限 %.0f%%，缺 %d 项：%s'
                         % (k, got * 100, need * 100, len(bad.get(k, [])),
                            bad.get(k, [])[:5]))
    return rate, fails


def book_name(jar, ns, pack_root):
    """导览书的中文名：上游 book.json 的 name 过一遍我们的 lang。"""
    z = zipfile.ZipFile(jar)
    p = 'data/%s/patchouli_books/guide/book.json' % ns
    if p not in z.namelist():
        return None
    en = json.loads(z.read(p)).get('name')
    lf = pack_root / 'assets' / ns / 'lang' / 'zh_cn.json'
    if not lf.is_file():
        return en
    return json.loads(lf.read_text(encoding='utf-8')).get(en, en)


def readme(man, ver, jar):
    lim = '\n'.join('- %s' % x for x in man.get('known_limitations', []))
    book = man.get('_book_name') or '内置导览书'
    return """{name}（{en_name}）简体中文汉化
================================================

版本 {ver}
适配 Minecraft {mc} / {loader}，对着 {jar} 逐条核过

装法（二选一，别两个都装）
--------------------------
资源包版  {id}-{ver}-resourcepack.zip
    丢进 .minecraft/resourcepacks/，游戏里「选项 → 资源包」启用。
    任何加载器都能用。

资源模组版  {id}-{ver}.jar
    丢进 mods/，自动生效，不用管资源包顺序。仅 NeoForge。
    里面没有一行 Java 代码，只是资源。

翻了什么
--------
- 物品 / 方块 / 蜜蜂 / 界面 / 进度：{n_lang} 条
- 内置导览书《{book}》：{n_book} 个页面文件，全部中文

已知边界
--------
{lim}

来历与授权
----------
摘自 All the Mods 10 简体中文汉化补丁「绿油油版」，与整合包版**同一份真源**，
不是另抄的一份，所以译名不会两边打架。

Copyright (C) 2026 星野夢華 (Hoshino Yumeka)
SPDX-License-Identifier: GPL-3.0-or-later
{home}
""".format(name=man['zh_name'], en_name=man['en_name'], ver=ver,
           mc=man['verified_against']['minecraft'],
           loader=man['verified_against']['loader'],
           jar=jar.name, id=man['id'], lim=lim or '- 无',
           home=man.get('homepage', ''),
           n_lang=man['_n_lang'], n_book=man['_n_book'], book=book)


def mods_toml(man, ver):
    return '''modLoader="lowcodefml"
loaderVersion="[1,)"
license="GPL-3.0-or-later"
issueTrackerURL="https://github.com/chiba233/atm10-zh-cn/issues"

[[mods]]
modId="{modid}_zh_cn"
version="{ver}"
displayName="{zh} 汉化"
authors="星野夢華 (Hoshino Yumeka)"
description=\'\'\'
{zh}（{en}）的简体中文汉化：物品、方块、蜜蜂、界面，以及内置导览书全部页面。

摘自 All the Mods 10 汉化补丁「绿油油版」，与整合包版同一份真源。
纯资源，无代码。
\'\'\'

[[dependencies.{modid}_zh_cn]]
modId="{modid}"
type="required"
versionRange="[0,)"
ordering="AFTER"
side="CLIENT"
'''.format(modid=man['modid'], ver=ver, zh=man['zh_name'], en=man['en_name'])


def mcmeta(man):
    return json.dumps({'pack': {
        'pack_format': man['pack_format'],
        'supported_formats': man['supported_formats'],
        'description': '%s 简体中文汉化 · 绿油油版' % man['zh_name'],
    }}, ensure_ascii=False, indent=2) + '\n'


def add_tree(zf, root, arc_prefix=''):
    n = 0
    for p in sorted(root.rglob('*')):
        if p.is_file():
            zf.write(p, arc_prefix + p.relative_to(root).as_posix())
            n += 1
    return n


def main(mid, mods_dir, ver):
    man = json.loads((MANIFESTS / ('%s.json' % mid)).read_text(encoding='utf-8'))
    jar = find_jar(mods_dir, man['modid'], man['verified_against']['jar'])
    got = hashlib.sha256(jar.read_bytes()).hexdigest()
    if got != man['verified_against']['sha256']:
        print('⚠️ %s 与清单里验过的那份不是同一个字节。照样生成，但覆盖率以本次实测为准。'
              % jar.name)
        print('   清单 %s…\n   实得 %s…'
              % (man['verified_against']['sha256'][:16], got[:16]))

    # 导览书要现套：仓库里没有任何一份上游副本，译文是「原文→译文」映射
    print('套导览书映射 …')
    gen_books.main(str(Path(mods_dir)))

    stage = BUILD / 'standalone' / mid
    if stage.exists():
        shutil.rmtree(stage)
    n_lang = n_book = 0
    for ns in man['namespaces']:
        src = PACK / 'assets' / ns
        if not src.is_dir():
            sys.exit('❌ 出货树里没有 assets/%s，先跑 assemble.py' % ns)
        dst = stage / 'assets' / ns
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(src, dst)
        lf = dst / 'lang' / 'zh_cn.json'
        if lf.is_file():
            n_lang += len(json.loads(lf.read_text(encoding='utf-8')))
        n_book += sum(1 for _ in dst.rglob('patchouli_books/**/*.json'))
    man['_n_lang'], man['_n_book'] = n_lang, n_book
    # 书名从 lang 里现取。Patchouli 会把 book.json 的 name 过一遍 I18n，
    # 所以中文书名就是那条 lang 的值——**不许在说明里另写一个**，写了必然对不上。
    man['_book_name'] = book_name(jar, man['namespaces'][0], stage)

    rate, fails = coverage(jar, man['namespaces'][0], stage, man['coverage_floor'])
    for k, v in sorted(rate.items()):
        print('  %s 覆盖率 %.1f%%' % (k, v * 100))
    if fails:
        for f in fails:
            print('  ❌', f)
        sys.exit('❌ 覆盖率不达标，不出包——「只翻了一半」比没翻还糟')

    (stage / 'pack.mcmeta').write_text(mcmeta(man), encoding='utf-8')
    (stage / 'LICENSE').write_bytes((ROOT / 'LICENSE').read_bytes())
    (stage / '说明.txt').write_text(readme(man, ver, jar), encoding='utf-8')

    OUT.mkdir(exist_ok=True)
    rp = OUT / ('%s-%s-resourcepack.zip' % (man['id'], ver))
    with zipfile.ZipFile(rp, 'w', zipfile.ZIP_DEFLATED) as zf:
        n = add_tree(zf, stage)
    print('✅ 资源包 %s（%d 个文件）' % (rp.name, n))

    mj = OUT / ('%s-%s.jar' % (man['id'], ver))
    with zipfile.ZipFile(mj, 'w', zipfile.ZIP_DEFLATED) as zf:
        n = add_tree(zf, stage)
        zf.writestr('META-INF/neoforge.mods.toml', mods_toml(man, ver))
    print('✅ 资源模组 %s（%d 个文件 + mods.toml）' % (mj.name, n + 1))
    print('   lang %d 条，导览书 %d 个文件' % (n_lang, n_book))


if __name__ == '__main__':
    if len(sys.argv) < 4:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2], sys.argv[3])
