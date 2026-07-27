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

CurseForge 的网页 API 没有配额说明但会限速。踩过的坑都写进代码里了：
默认 UA 会被挡（必须伪装成浏览器）、并发压到 4、失败按指数退避重试、
整轮重来收漏网的、**不查元数据**直接下载并从跳转后的 CDN 地址取文件名、
下不来时把**真实的 HTTP 错误**打出来（以前吞成 None，只看得到「下得太少」，
分不清是限速还是接口变了，白折腾好几轮）。

用法:
    python3 scripts/fetch_pack.py 7.2 build/packsrc/7.2 --no-jars   # 只要官方文件
    python3 scripts/fetch_pack.py 7.2 pack                          # 含 480 个 jar
"""
import concurrent.futures as cf
import hashlib
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path

PROJECT = 925200          # CurseForge 上的 All the Mods 10
API = 'https://www.curseforge.com/api/v1/mods/%d' % PROJECT
UA = ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/126.0 Safari/537.36')
TRIES = 6


def fetch(url, timeout=180, required=True):
    """取一个 URL，返回 (内容, 最终URL)。限速/抽风就退避重试。

    **失败原因必须留下来**：以前这里把异常吞成 None，CI 上 482 个 jar 全下不来时
    只看得到「jar 下得太少」，看不出到底是限速、403 还是 404，白折腾好几轮。
    """
    last = None
    for i in range(TRIES):
        req = urllib.request.Request(url, headers={'User-Agent': UA})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read(), r.url
        except urllib.error.HTTPError as e:
            last = 'HTTP %s %s' % (e.code, e.reason)
            if e.code in (403, 408, 425, 429, 500, 502, 503, 504):
                wait = float(e.headers.get('Retry-After') or 0) or (2 ** i)
                time.sleep(min(wait, 60))
                continue
            break                                    # 404/400 这类重试也没用
        except Exception as e:                       # 超时、连接重置
            last = repr(e)
            time.sleep(2 ** i)
    if required:
        sys.exit('❌ 取不到 %s\n   重试 %d 次后仍失败：%s' % (url, TRIES, last))
    return None, last


def get(url, timeout=180, required=True):
    return fetch(url, timeout, required)[0]


def tree_digest(root):
    """整棵 overrides 的确定性指纹：路径 + 内容，排序后逐个吃进去。

    ATM10 的某个已发布版本，它的 overrides 内容是**不会变**的。把指纹记进仓库，
    CI 上无论是从缓存拿的还是现下的，都要跟它对得上——CurseForge 哪天换了内容
    （或者下载被人动了手脚），构建当场红，而不是悄悄拿另一份东西去打补丁。
    """
    h = hashlib.sha256()
    for p in sorted(Path(root).rglob('*')):
        if not p.is_file():
            continue
        h.update(p.relative_to(root).as_posix().encode())
        h.update(b'\0')
        h.update(hashlib.sha256(p.read_bytes()).digest())
    return h.hexdigest()


def check_digest(ver, digest):
    """跟 versions/<版本>/overrides.sha256 对照；没记过就打印出来让人记上。"""
    f = Path(__file__).resolve().parent.parent / 'versions' / ver / 'overrides.sha256'
    if not f.is_file():
        print('  ⚠️ versions/%s/overrides.sha256 还没记。确认这份没问题后写进去：' % ver)
        print('     echo %s > versions/%s/overrides.sha256' % (digest, ver))
        return
    want = f.read_text(encoding='utf-8').split()[0]
    if want != digest:
        sys.exit('❌ ATM10 %s 的 overrides 内容与仓库记录的指纹对不上\n'
                 '   记录 %s\n   实得 %s\n'
                 '   已发布版本的内容本不该变。要么 CurseForge 换了东西，要么这份下载不干净。\n'
                 '   人工核对无误后再更新 versions/%s/overrides.sha256。'
                 % (ver, want, digest, ver))
    print('  指纹与 versions/%s/overrides.sha256 一致 ✅' % ver)


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
    n = sum(1 for _ in out.rglob('*') if _.is_file())
    digest = tree_digest(out)
    print('  overrides 解出 %d 个文件，指纹 %s' % (n, digest[:16]))
    check_digest(ver, digest)
    if not jars:
        return
    mods = out / 'mods'
    mods.mkdir(exist_ok=True)

    errors = []

    def one(f):
        """下一个 jar。**不查元数据**——下载接口会跳转到带文件名的 CDN 地址，
        文件名直接从最终 URL 取。少一半请求，也少一个会 404 的接口。

        任何异常都不许抛：一个文件下不来只该少一个 jar，由外层整轮重试兜住；
        抛出去会顺着 ex.map 把整个构建炸掉。"""
        try:
            url = ('https://www.curseforge.com/api/v1/mods/%d/files/%d/download'
                   % (f['projectID'], f['fileID']))
            d, final = fetch(url, required=False)
            if not d or len(d) < 500:
                errors.append('fileID %d: %s' % (f['fileID'], final))
                return None
            name = urllib.parse.unquote(str(final).rsplit('/', 1)[-1].split('?')[0])
            if not name.endswith('.jar'):
                name = '%d.jar' % f['fileID']
            p = mods / name
            if not p.exists():
                p.write_bytes(d)
            return name
        except Exception as e:
            errors.append('fileID %d: %r' % (f['fileID'], e))
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
        for e in errors[:8]:
            print('   %s' % e)
        sys.exit('❌ jar 下得太少（%d/%d），生成器会漏内容，中止\n'
                 '   上面是前几条真实错误。403/429 是限速，稍后重跑；'
                 '404 说明接口变了，得改 fetch_pack.py。'
                 % (len(got), len(todo)))


if __name__ == '__main__':
    # --verify：目录已经在（多半来自 CI 缓存），只核对指纹，一个字节都不下。
    # 缓存命中也必须核——缓存里的东西同样可能是坏的。
    if '--verify' in sys.argv:
        a = [x for x in sys.argv[1:] if x != '--verify']
        if len(a) != 2:
            sys.exit(__doc__)
        check_digest(a[0], tree_digest(a[1]))
        sys.exit(0)
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2], '--no-jars' not in sys.argv)
