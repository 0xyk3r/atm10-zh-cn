#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# atm10-zh-cn — All the Mods 10 简体中文汉化补丁「绿油油版」
# Copyright (C) 2026 星野夢華 (Hoshino Yumeka)
# SPDX-License-Identifier: GPL-3.0-or-later
"""把某个版本的 ATM10 整合包备齐成一个能当 ATM_PACK_ROOT 用的目录。

生成器要读两样东西：`overrides/`（源图、任务书、kubejs）和 **mod jar 里的
`en_us.json` 与注册表**（奖杯名、木头名、蜂名、格式串快照都靠它）。
CurseForge 的整合包 zip 里只有 manifest + overrides，jar 要按 manifest 逐个下。

CI 上跑这个；本机开发直接把 ATM_PACK_ROOT 指向装好的实例即可，不用下。

用法:
    python3 scripts/fetch_pack.py 7.2 pack        # 全量（含 480 个 jar）
    python3 scripts/fetch_pack.py 7.2 pack --no-jars
"""
import concurrent.futures as cf
import json
import sys
import urllib.request
import zipfile
from pathlib import Path

PROJECT = 925200          # CurseForge 上的 All the Mods 10
API = 'https://www.curseforge.com/api/v1/mods/%d' % PROJECT


def get(url, timeout=180):
    for _ in range(3):
        try:
            with urllib.request.urlopen(url, timeout=timeout) as r:
                return r.read()
        except Exception:
            pass
    return None


def find_file_id(ver):
    d = json.loads(get('%s/files?pageSize=50' % API))
    for f in d['data']:
        if f['displayName'].rsplit('-', 1)[-1].strip() == ver:
            return f['id']
    sys.exit('❌ CurseForge 上找不到 ATM10 %s' % ver)


def main(ver, out, jars=True):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    fid = find_file_id(ver)
    print('ATM10 %s → fileID %s' % (ver, fid))
    z = out.parent / ('atm10-%s.zip' % ver)
    if not z.exists():
        z.write_bytes(get('%s/files/%s/download' % (API, fid)))
    with zipfile.ZipFile(z) as zf:
        manifest = json.loads(zf.read('manifest.json'))
        for n in zf.namelist():
            if n.startswith('overrides/') and not n.endswith('/'):
                t = out / n[len('overrides/'):]
                t.parent.mkdir(parents=True, exist_ok=True)
                t.write_bytes(zf.read(n))
    print('  overrides 解出 %d 个文件' % sum(1 for _ in out.rglob('*') if _.is_file()))
    if not jars:
        return
    mods = out / 'mods'
    mods.mkdir(exist_ok=True)

    def one(f):
        meta = get('%s/files/%d' % (API, f['fileID']), timeout=60)
        if not meta:
            return None
        name = json.loads(meta)['data'].get('fileName')
        if not name:
            return None
        p = mods / name
        if p.exists():
            return name
        d = get('%s/files/%d/download' % (API, f['fileID']))
        if d and len(d) > 500:
            p.write_bytes(d)
            return name
        return None

    todo = manifest['files']
    ok = 0
    with cf.ThreadPoolExecutor(8) as ex:
        for i, r in enumerate(ex.map(one, todo), 1):
            ok += bool(r)
            if i % 50 == 0:
                print('  jar %d/%d' % (i, len(todo)), flush=True)
    print('  mod jar %d/%d，目录共 %d 个'
          % (ok, len(todo), len(list(mods.glob('*.jar')))))
    if ok < len(todo) * 0.98:
        sys.exit('❌ jar 下得太少，生成器会漏内容，中止')


if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2], '--no-jars' not in sys.argv)
