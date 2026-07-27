#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# atm10-zh-cn — All the Mods 10 简体中文汉化补丁「绿油油版」
# Copyright (C) 2026 星野夢華 (Hoshino Yumeka)
# SPDX-License-Identifier: GPL-3.0-or-later
"""按 `src/mods.lock.json` 把随包分发的第三方 jar 取下来，逐个核 sha256。

仓库里不放二进制。锁文件写死了「哪个项目、哪个版本、什么地址、什么哈希」，
构建时现取——**哈希对不上就退出**，不会把一个来路不明的 jar 打进包里。

下载缓存在 `build/modcache/<sha256>.jar`，重复构建不重复下。

为什么不是全部 jar 都这么办：JEI 拼音搜索（jecharacters）只在 CurseForge 上有，
而 CurseForge 的搜索/项目接口挡机器人（403），拿不到能钉死的地址，
所以那一个仍然入库。哪天它上了 Modrinth 再挪过来。

用法:
    python3 scripts/fetch_mods.py <输出目录>       # 一般是 build/common
"""
import hashlib
import json
import sys
import urllib.request
from pathlib import Path

from paths import BUILD, SRC

LOCK = SRC / 'mods.lock.json'
CACHE = BUILD / 'modcache'
UA = {'User-Agent': 'atm10-zh-cn/1.0 (+https://github.com/chiba233/atm10-zh-cn)'}


def sha256(b):
    return hashlib.sha256(b).hexdigest()


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=180) as r:
        return r.read()


def main(out_dir):
    if not LOCK.is_file():
        sys.exit('❌ 没有 %s' % LOCK)
    lock = json.loads(LOCK.read_text(encoding='utf-8'))
    out = Path(out_dir)
    CACHE.mkdir(parents=True, exist_ok=True)
    for rel, info in sorted(lock.items()):
        want = info['sha256']
        cached = CACHE / (want + '.jar')
        if not cached.exists():
            data = get(info['url'])
            got = sha256(data)
            if got != want:
                sys.exit('❌ %s 哈希对不上——**不要用这个文件**\n'
                         '   期望 %s\n   实得 %s\n   地址 %s\n'
                         '   要么上游把同一个地址的内容换了，要么下载被人动了手脚。'
                         % (rel, want, got, info['url']))
            cached.write_bytes(data)
        else:
            # 缓存也要复核：磁盘上的东西同样可能被改
            if sha256(cached.read_bytes()) != want:
                cached.unlink()
                sys.exit('❌ 缓存 %s 哈希对不上，已删除，请重跑' % cached)
        t = out / rel
        t.parent.mkdir(parents=True, exist_ok=True)
        t.write_bytes(cached.read_bytes())
        print('  %-28s %s %s (%d KB)'
              % (rel, info.get('project', ''), info.get('version', ''),
                 len(cached.read_bytes()) // 1024))
    print('随包 jar：%d 个，sha256 全部核对通过' % len(lock))


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
