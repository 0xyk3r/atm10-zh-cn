#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# atm10-zh-cn — All the Mods 10 简体中文汉化补丁「绿油油版」
# Copyright (C) 2026 星野夢華 (Hoshino Yumeka)
# SPDX-License-Identifier: GPL-3.0-or-later
"""把「按键绑定」界面里的**分类标题**逐个扫出来。

分类是 `KeyMapping(name, type, code, category)` 的最后一个参数。它有两种形态，
处理方式完全不同：

- **翻译键**（`key.categories.<模组>`）→ 补 lang 就能翻。
  但注意有一批模组注册了键却**没有任何 lang 定义它**，界面上直接显示原始键
  （实测 `key.categories.industrialization_overdrive` 就这样露在玩家眼前）。
- **硬编码字面量**（`Create`、`Auroras`、`Corail Tombstone`…）→ lang 碰不到，
  只能走 VaultPatcher 改常量池。

在 lang 里按 `key.categor*` 匹配是**数不准的**：既漏掉没人定义的键，也完全看不见
字面量那一类。所以这里直接读字节码——找到 `KeyMapping.<init>` 的调用点，
取调用前最后一个入栈的字符串常量（描述符最后一个参数就是 String）。

用法:
    python3 scripts/scan_keybind_categories.py <mods 目录> [输出.json]
"""
import json
import struct
import sys
import zipfile
from pathlib import Path

# 只带一个操作数、且操作数宽度固定的指令表，用来在字节码里正确前进
# （不需要全量指令语义，只要能准确跳过操作数即可）
WIDTH = {}
for op in range(0x00, 0x0f + 1):
    WIDTH[op] = 0
for op, w in [(0x10, 1), (0x11, 2), (0x12, 1), (0x13, 2), (0x14, 2),
              (0x15, 1), (0x16, 1), (0x17, 1), (0x18, 1), (0x19, 1),
              (0x36, 1), (0x37, 1), (0x38, 1), (0x39, 1), (0x3a, 1),
              (0xa7, 2), (0xa8, 2), (0xa9, 1), (0xbb, 2), (0xbc, 1),
              (0xbd, 2), (0xc0, 2), (0xc1, 2), (0xb2, 2), (0xb3, 2),
              (0xb4, 2), (0xb5, 2), (0xb6, 2), (0xb7, 2), (0xb8, 2),
              (0xb9, 4), (0xba, 4), (0x84, 2), (0xc6, 2), (0xc7, 2),
              (0xc5, 3), (0xc8, 4), (0xc9, 4)]:
    WIDTH[op] = w
for op in range(0x99, 0xa6 + 1):
    WIDTH[op] = 2


def parse_pool(b):
    """返回 (常量池列表, 池结束偏移)。列表元素是 (tag, 原始值)。"""
    n = struct.unpack_from('>H', b, 8)[0]
    pool = [None] * n
    i, off = 1, 10
    while i < n:
        tag = b[off]
        if tag == 1:
            ln = struct.unpack_from('>H', b, off + 1)[0]
            pool[i] = (1, b[off + 3:off + 3 + ln].decode('utf-8', 'replace'))
            off += 3 + ln
        elif tag in (7, 8, 16, 19, 20):
            pool[i] = (tag, struct.unpack_from('>H', b, off + 1)[0])
            off += 3
        elif tag in (15,):
            pool[i] = (tag, None)
            off += 4
        elif tag in (3, 4):
            pool[i] = (tag, None)
            off += 5
        elif tag in (5, 6):
            pool[i] = (tag, None)
            off += 9
            i += 1                       # long/double 占两个槽
        else:                            # 9,10,11,12,17,18
            pool[i] = (tag, struct.unpack_from('>HH', b, off + 1))
            off += 5
        i += 1
    return pool, off


def utf(pool, idx):
    e = pool[idx]
    return e[1] if e and e[0] == 1 else None


def scan_class(b):
    """产出这个 class 里每个 KeyMapping 构造调用点用的分类字符串。"""
    if b'KeyMapping' not in b:
        return []
    pool, off = parse_pool(b)
    # 找到指向 KeyMapping.<init> 的 Methodref
    targets = set()
    for i, e in enumerate(pool):
        if not e or e[0] != 10:          # Methodref
            continue
        cls_i, nat_i = e[1]
        cls = pool[cls_i]
        nat = pool[nat_i]
        if not cls or cls[0] != 7 or not nat or nat[0] != 12:
            continue
        cname = utf(pool, cls[1]) or ''
        mname = utf(pool, nat[1][0]) or ''
        if mname == '<init>' and cname.endswith('KeyMapping'):
            targets.add(i)
    if not targets:
        return []

    out = []
    # 常量池之后依次是 access_flags(2) this_class(2) super_class(2)
    # interfaces_count(2) interfaces(2n)，然后才是 fields / methods。
    p = off + 6
    ifc = struct.unpack_from('>H', b, p)[0]
    p += 2 + ifc * 2

    def members():
        """走过一段 fields/methods，产出其中 Code 属性的 (偏移, 长度)"""
        nonlocal p
        found = []
        cnt = struct.unpack_from('>H', b, p)[0]
        p += 2
        for _ in range(cnt):
            p += 6
            na = struct.unpack_from('>H', b, p)[0]
            p += 2
            for _ in range(na):
                ln = struct.unpack_from('>I', b, p + 2)[0]
                if utf(pool, struct.unpack_from('>H', b, p)[0]) == 'Code':
                    found.append((p + 6, ln))
                p += 6 + ln
        return found

    members()                                   # fields
    for start, ln in members():                 # methods
        clen = struct.unpack_from('>I', b, start + 4)[0]
        code = b[start + 8:start + 8 + clen]
        last_str = None
        i = 0
        while i < len(code):
            op = code[i]
            if op in (0x12, 0x13):               # ldc / ldc_w
                idx = code[i + 1] if op == 0x12 else struct.unpack_from('>H', code, i + 1)[0]
                e = pool[idx] if idx < len(pool) else None
                if e and e[0] == 8:              # CONSTANT_String
                    s = utf(pool, e[1])
                    if s is not None:
                        last_str = s
            elif op == 0xb7:                     # invokespecial
                idx = struct.unpack_from('>H', code, i + 1)[0]
                if idx in targets and last_str is not None:
                    out.append(last_str)
            elif op == 0xc4:                     # wide
                i += 4 if code[i + 1] != 0x84 else 6
                continue
            elif op in (0xaa, 0xab):             # tableswitch / lookupswitch
                j = i + 1
                while j % 4:
                    j += 1
                if op == 0xaa:
                    lo, hi = struct.unpack_from('>ii', code, j + 4)
                    i = j + 12 + (hi - lo + 1) * 4
                else:
                    npairs = struct.unpack_from('>i', code, j + 4)[0]
                    i = j + 8 + npairs * 8
                continue
            i += 1 + WIDTH.get(op, 0)
    return out


def main(mods_dir, out_path=None):
    cats = {}
    fails = []
    for jar in sorted(Path(mods_dir).glob('*.jar')):
        try:
            z = zipfile.ZipFile(jar)
        except Exception:
            continue
        for n in z.namelist():
            if not n.endswith('.class'):
                continue
            try:
                for c in scan_class(z.read(n)):
                    cats.setdefault(c, set()).add(jar.name)
            except Exception as e:
                # 吞掉解析异常的话，「一个都没扫到」和「全都解析失败」长得一模一样
                fails.append('%s!%s: %r' % (jar.name, n, e))
    keys = sorted(c for c in cats if c.startswith('key.'))
    lits = sorted(c for c in cats if not c.startswith('key.'))
    print('按键分类共 %d 个：翻译键 %d、硬编码字面量 %d'
          % (len(cats), len(keys), len(lits)))
    if fails:
        print('⚠️ %d 个 class 解析失败（前 3 条）:' % len(fails))
        for f in fails[:3]:
            print('   ', f)
    if out_path:
        Path(out_path).write_text(json.dumps(
            {'keys': keys, 'literals': {c: sorted(cats[c]) for c in lits}},
            ensure_ascii=False, indent=1), encoding='utf-8')
        print('已写出 %s' % out_path)
    return keys, lits


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
