#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# atm10-zh-cn — All the Mods 10 简体中文汉化补丁「绿油油版」
# Copyright (C) 2026 星野夢華 (Hoshino Yumeka)
# SPDX-License-Identifier: GPL-3.0-or-later
"""把全历史每一笔删除**按内容**审一遍：到底丢没丢东西。

为什么不能看提交说明：那些说明是删的人自己写的（就是我），
「上游死重」「游戏根本不读」「改由 jar 现生成」都是待证的结论，不是证据。
也不能按路径比对——仓库中途重构过，译文从「一整份文件」改存成
「原文→译文的映射」，路径全变了，按路径看每一笔都像是灾难。

所以按**内容原子**比对：

    中文串   —— 从被删文件里抽出的每一条含汉字的字符串（去掉格式码后归一）
    二进制   —— 图片等按 sha256

对每一笔删除，取它父提交上那些文件的内容，抽出原子，再拿去**今天的整个
src/** 里找。找得到 = 换了个地方存着，没丢；找不到 = 这条中文今天确实
不在仓库里了。给出的是条数，不是形容词。

用法:
    python3 scripts/audit_deletions.py            # 审全历史
    python3 scripts/audit_deletions.py <commit>…  # 只审这几笔
"""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CJK = re.compile(r'[一-鿿]')
# 归一：去掉颜色码、占位符、空白与标点，只留下「这句话说了什么」。
# 不归一的话，同一句译文换了个 §a 前缀就会被算成「丢了」。
NOISE = re.compile(r'[§&][0-9a-fk-orA-FK-OR]|%(?:\d+\$)?[a-zA-Z%]|\$\([^)]*\)|\s+'
                   r'|[　-〿！-～.,:;!?"\'()\[\]{}<>/\\|*_~`#=+-]')
TEXT_EXT = {'.json', '.md', '.mdx', '.snbt', '.txt', '.toml', '.js', '.cfg'}


def norm(s):
    return NOISE.sub('', s)


def git(*a, binary=False):
    r = subprocess.run(['git', '-c', 'safe.directory=*', '-c', 'core.quotepath=false', *a],
                       cwd=ROOT, capture_output=True, check=False)
    if r.returncode != 0:
        return None
    return r.stdout if binary else r.stdout.decode('utf-8', 'replace')


def strings(obj, out):
    """把任意 JSON 结构里的字符串全抠出来。"""
    if isinstance(obj, str):
        out.append(obj)
    elif isinstance(obj, dict):
        for v in obj.values():
            strings(v, out)
    elif isinstance(obj, list):
        for v in obj:
            strings(v, out)


def atoms(path, data):
    """一份文件贡献的内容原子集合。"""
    ext = Path(path).suffix.lower()
    if ext not in TEXT_EXT:
        return {'b:' + hashlib.sha256(data).hexdigest()}          # 图片等按字节
    try:
        text = data.decode('utf-8-sig')
    except UnicodeDecodeError:
        return {'b:' + hashlib.sha256(data).hexdigest()}
    vals = []
    if ext == '.json':
        try:
            strings(json.loads(text), vals)
        except Exception:                                          # noqa: BLE001
            vals = text.split('\n')
    else:
        vals = text.split('\n')
    out = set()
    for v in vals:
        if CJK.search(v):
            n = norm(v)
            if n:
                out.add('t:' + n)
    return out


def blobs(rev, paths):
    """一次性把某个提交上的一批文件内容取出来（git cat-file --batch）。"""
    req = ''.join('%s:%s\n' % (rev, p) for p in paths)
    p = subprocess.Popen(['git', '-c', 'safe.directory=*', 'cat-file', '--batch'],
                         cwd=ROOT, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    out, _ = p.communicate(req.encode())
    res, i, k = {}, 0, 0
    while i < len(out) and k < len(paths):
        nl = out.index(b'\n', i)
        head = out[i:nl].decode('utf-8', 'replace').split()
        if len(head) == 3:
            size = int(head[2])
            res[paths[k]] = out[nl + 1:nl + 1 + size]
            i = nl + 1 + size + 1
        else:                                                      # missing
            i = nl + 1
        k += 1
    return res


def zip_atoms(data, got, depth=0):
    """出货包里的原子。客户端包里还套着一层资源包 zip，得拆两层。"""
    import io
    import zipfile
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        for n in z.namelist():
            if n.endswith('/'):
                continue
            b = z.read(n)
            if n.endswith('.zip') and depth < 2:
                zip_atoms(b, got, depth + 1)
            else:
                got |= atoms(n, b)


def jar_atoms(jars, got):
    """模组 jar 自带的官方中文。

    这一份必须算进来，否则会误判一大批：模组本身就带 zh_cn 的内容，
    我们**不该**再复制一份进补丁（重复覆盖只会跟上游修订打架），
    但玩家在游戏里照样看得到中文。只按「我们的包里有没有」判，
    会把这批全算成「丢了」。
    """
    import zipfile
    for j in sorted(Path(jars).glob('*.jar')):
        try:
            with zipfile.ZipFile(j) as z:
                for n in z.namelist():
                    if 'zh_cn' in n and not n.endswith('/'):
                        got |= atoms(n, z.read(n))
        except Exception:                                          # noqa: BLE001
            pass


def corpus(dist=None, jars=None):
    """今天还找得到这条中文的地方。

    三处，缺一不可：

      src/            —— 仓库里存着的源
      出货包           —— 构建时从 mod jar 现生成的那部分。导览书等内容
                          按设计就**不入库**（只存「原文→译文」映射），
                          光扫 src/ 会把它们全判成「丢了」，那是假阳性
      模组 jar         —— 模组自带的官方中文；这批本来就不该由我们再发一遍

    三处都找不到，才叫真的丢了：玩家在游戏里从此看不到这句中文。
    """
    got = set()
    for p in sorted(ROOT.glob('src/**/*')):
        if p.is_file():
            got |= atoms(p.name, p.read_bytes())
    if dist:
        for z in sorted(Path(dist).glob('*.zip')):
            zip_atoms(z.read_bytes(), got)
    if jars:
        jar_atoms(jars, got)
    return got


def deletions(rev):
    out = git('show', '--name-status', '--format=', rev)
    return [ln[2:] for ln in (out or '').split('\n') if ln.startswith('D\t')]


def main(revs, dist=None, jars=None):
    have = corpus(dist, jars)
    print('今天找得到的内容原子共 %d 个（src/ %s%s）\n'
          % (len(have), '+ 出货包 ' if dist else '', '+ 模组 jar 自带中文' if jars else ''))
    if not revs:
        log = git('log', '--reverse', '--format=%h|%s') or ''
        revs = [ln.split('|', 1) for ln in log.split('\n') if ln]
    else:
        revs = [[r, (git('log', '-1', '--format=%s', r) or '').strip()] for r in revs]

    total_lost = 0
    rows = []
    for h, subject in revs:
        dels = deletions(h)
        if not dels:
            continue
        data = blobs(h + '^', dels)
        want = set()
        for p, b in data.items():
            want |= atoms(p, b)
        lost = sorted(want - have)
        rows.append((h, subject, len(dels), len(want), lost))
        total_lost += len(lost)

    print('%-9s %5s %7s %7s  %s' % ('commit', '删文件', '内容原子', '今天找不到', '标题'))
    for h, s, nd, nw, lost in rows:
        flag = '❌' if lost else '✅'
        print('%s %-9s %5d %7d %7d  %s' % (flag, h, nd, nw, len(lost), s[:40]))

    for h, s, nd, nw, lost in rows:
        if not lost:
            continue
        print('\n' + '=' * 74)
        print('%s  %s' % (h, s))
        print('删了 %d 个文件，其中 %d 条内容在今天的 src/ 里查无此项：' % (nd, len(lost)))
        for a in lost[:40]:
            print('   %s' % (a[2:][:100] if a.startswith('t:') else '(二进制) ' + a[2:14]))
        if len(lost) > 40:
            print('   … 还有 %d 条' % (len(lost) - 40))

    print('\n合计今天找不到的内容原子：%d 条' % total_lost)
    return 0


if __name__ == '__main__':
    a = sys.argv[1:]
    opt = {}
    for k in ('--dist', '--jars'):
        if k in a:
            i = a.index(k)
            opt[k[2:]] = a[i + 1]
            a = a[:i] + a[i + 2:]
    sys.exit(main([x for x in a if not x.startswith('-')],
                  opt.get('dist'), opt.get('jars')))
