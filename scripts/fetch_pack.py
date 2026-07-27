#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# atm10-zh-cn — All the Mods 10 简体中文汉化补丁「绿油油版」
# Copyright (C) 2026 星野夢華 (Hoshino Yumeka)
# SPDX-License-Identifier: GPL-3.0-or-later
"""把某个版本的 ATM10 整合包备齐成一个能当 ATM_PACK_ROOT 用的目录。

两种用法，成本差一个数量级：

- `--no-jars`：只解 `overrides/`。**打补丁用的官方文件**（ATM 自己的 kubejs/*.js、
  config/*.json）就在里面，每个目标版本都要来一份，构建时对着它套映射。
- 全量：再按 manifest 把 480 个 mod jar 下齐。只有「读 jar 里的 en_us 与注册表」
  的那几个生成器需要（奖杯名、木头名、蜂名、格式串快照），一次构建取最新那版即可。

CurseForge 的网页 API 没有配额说明但会限速，480 个 jar 逐个查文件名很容易撞 429。
所以：默认 UA 会被挡（必须伪装成浏览器）、并发压到 4、失败按指数退避重试、
拿不到就**明确报错**而不是让 None 往下走炸出个 AttributeError。

用法:
    python3 scripts/fetch_pack.py 7.2 build/packsrc/7.2 --no-jars   # 只要官方文件
    python3 scripts/fetch_pack.py 7.2 pack                          # 含 480 个 jar
"""
import concurrent.futures as cf
import json
import sys
import time
import urllib.error
import urllib.request
import zipfile
from pathlib import Path

PROJECT = 925200          # CurseForge 上的 All the Mods 10
API = 'https://www.curseforge.com/api/v1/mods/%d' % PROJECT
UA = ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/126.0 Safari/537.36')
TRIES = 6


def get(url, timeout=180, required=True):
    """取一个 URL；限速就退避重试。取不到时 required=True 直接终止构建。"""
    last = None
    for i in range(TRIES):
        req = urllib.request.Request(url, headers={'User-Agent': UA})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            last = 'HTTP %s' % e.code
            if e.code in (403, 429, 500, 502, 503, 504):
                wait = float(e.headers.get('Retry-After') or 0) or (2 ** i)
                time.sleep(min(wait, 60))
                continue
            break
        except Exception as e:                       # 超时、连接重置
            last = repr(e)
            time.sleep(2 ** i)
    if required:
        sys.exit('❌ 取不到 %s（重试 %d 次后仍失败：%s）\n'
                 '   多半是 CurseForge 限速。稍后重跑，或先用 --no-jars 只取官方文件。'
                 % (url, TRIES, last))
    return None


def find_file_id(ver):
    d = json.loads(get('%s/files?pageSize=50' % API))
    for f in d['data']:
        if f['displayName'].rsplit('-', 1)[-1].strip() == ver:
            return f['id']
    have = sorted({f['displayName'].rsplit('-', 1)[-1].strip() for f in d['data']})
    sys.exit('❌ CurseForge 上找不到 ATM10 %s\n   最近 50 个文件里有: %s'
             % (ver, ' '.join(have)))


def main(ver, out, jars=True):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    fid = find_file_id(ver)
    print('ATM10 %s → fileID %s' % (ver, fid))
    z = out.parent / ('atm10-%s.zip' % ver)
    if not z.exists():
        z.parent.mkdir(parents=True, exist_ok=True)
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
        # 这里**任何异常都不许抛**：一个文件查不到只该少下一个 jar，
        # 由外层整轮重试兜住；抛出去会顺着 ex.map 把整个构建炸掉
        # （历史事故：限速时 data 是 null，'NoneType' object has no attribute 'get'）。
        try:
            meta = get('%s/files/%d' % (API, f['fileID']), timeout=60, required=False)
            if not meta:
                return None
            name = ((json.loads(meta) or {}).get('data') or {}).get('fileName')
            if not name:
                return None
            p = mods / name
            if p.exists():
                return name
            d = get('%s/files/%d/download' % (API, f['fileID']), required=False)
            if d and len(d) > 500:
                p.write_bytes(d)
                return name
        except Exception as e:
            print('  ⚠️ fileID %s 取失败（本轮跳过）: %r' % (f['fileID'], e), flush=True)
        return None

    todo = manifest['files']
    got = {}
    for rnd in range(3):                      # 整轮重来，专收被限速漏掉的
        left = [f for f in todo if f['fileID'] not in got]
        if not left:
            break
        if rnd:
            print('  第 %d 轮补下 %d 个（上一轮被限速）' % (rnd + 1, len(left)))
            time.sleep(20)
        with cf.ThreadPoolExecutor(4) as ex:
            for i, (f, r) in enumerate(zip(left, ex.map(one, left)), 1):
                if r:
                    got[f['fileID']] = r
                if i % 50 == 0:
                    print('  jar %d/%d' % (i, len(left)), flush=True)
    print('  mod jar %d/%d，目录共 %d 个'
          % (len(got), len(todo), len(list(mods.glob('*.jar')))))
    if len(got) < len(todo) * 0.98:
        sys.exit('❌ jar 下得太少（%d/%d），生成器会漏内容，中止'
                 % (len(got), len(todo)))


if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2], '--no-jars' not in sys.argv)
