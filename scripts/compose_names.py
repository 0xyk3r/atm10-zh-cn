#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# All the Mods 10 简体中文汉化补丁 · 绿油油版
# Copyright (C) 2026 星野夢華 (Hoshino Yumeka)
# SPDX-License-Identifier: GPL-3.0-or-later
"""按词表重新合成方块/物品名，替换掉底本残留的那一批。

那批残留有一万八千多条，但它们不是「一万八千句翻译」，而是同一套词反复排列：

    Black Eternal Starlight Banyin Display Case  →  黑色 + 榕木 + 展示柜
    Black Eternal Starlight Banyin Seat          →  黑色 + 榕木 + 板凳

所以不该逐条重译——逐条译既慢又必然前后不一致（同一个 banyin 这次译榕木、
下次译班音木）。该做的是把词表建起来，再机械地拼。

词表不是手写的，是**从已有的可信译文里学出来的**。可信译文指：模组自带的中文、
CFPA 社区翻译，以及我们自己写过的那部分——总计九万多条「英文名 ↔ 中文名」。
从中学两件事：

    后缀（器物）  英文以 `Display Case` 结尾的那些条目，中文的公共后缀是什么
    前缀（材料）  英文以 `Black Eternal Starlight Banyin` 开头的那些条目，
                  中文的公共前缀是什么

两边都学到、且样本一致，才敢拼；差一样就不拼——宁可留着让人处理，
也不能拼出「黑色Banyin展示柜」这种半截货。

用法:
    python3 scripts/compose_names.py --mods <mods 目录> [--cfpa <CFPA zip>]
        [--terms src/pack/terms.json] [--write]
"""
import json
import sys
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MIN_SAMPLES = 2          # 学一个词至少要几个样本
MAX_LEN = 12             # 只处理短名；长句子不是组合名


def jar_langs(mods):
    en, zh = defaultdict(dict), defaultdict(dict)
    for j in sorted(Path(mods).glob('*.jar')):
        try:
            z = zipfile.ZipFile(j)
        except Exception:                                  # noqa: BLE001
            continue
        for n in z.namelist():
            if not n.startswith('assets/'):
                continue
            tgt = en if n.endswith('/lang/en_us.json') else (
                zh if n.endswith('/lang/zh_cn.json') else None)
            if tgt is None:
                continue
            try:
                tgt[n.split('/')[1]].update(json.loads(z.read(n).decode('utf-8-sig')))
            except Exception:                              # noqa: BLE001
                pass
    return en, zh


def zip_langs(path):
    out = defaultdict(dict)
    if not path:
        return out
    z = zipfile.ZipFile(path)
    for n in z.namelist():
        if n.endswith('/lang/zh_cn.json') and '/assets/' in '/' + n:
            try:
                out[('/' + n).split('/assets/')[1].split('/')[0]].update(
                    json.loads(z.read(n).decode('utf-8-sig')))
            except Exception:                              # noqa: BLE001
                pass
    return out


def our_langs():
    out = {}
    for p in (ROOT / 'src' / 'pack' / 'assets').glob('*/lang/zh_cn.json'):
        out[p.parts[-3]] = json.loads(p.read_text(encoding='utf-8-sig'))
    return out


MAJORITY = 0.7


def major_prefix(strings):
    """取 **多数派**共有的最长前缀，不取全体的公共前缀。

    全体公共前缀太脆：`Blue` 开头的一百条中文里只要混进一条「湛蓝…」，
    公共前缀就被削成一个字甚至空，于是「蓝色」这个词整个学不到。
    改成「至少七成样本都有的最长前缀」，异类不再有一票否决权。
    """
    n = len(strings)
    best = ''
    for cand in strings:
        for ln in range(min(8, len(cand)), 0, -1):
            pre = cand[:ln]
            if len(pre) <= len(best):
                break
            if sum(1 for s in strings if s.startswith(pre)) >= max(2, n * MAJORITY):
                best = pre
                break
    return best


def major_suffix(strings):
    return major_prefix([s[::-1] for s in strings])[::-1]


def learn(trusted):
    """从可信的「英文名 → 中文名」里学后缀词与前缀词。"""
    by_suf, by_pre = defaultdict(list), defaultdict(list)
    for e, z in trusted.items():
        w = e.split()
        if not (1 <= len(w) <= 8):
            continue
        for i in range(1, len(w)):
            by_suf[' '.join(w[i:])].append(z)
            by_pre[' '.join(w[:i])].append(z)
    suf = {}
    for k, vs in by_suf.items():
        if len(vs) < MIN_SAMPLES:
            continue
        c = major_suffix(vs)
        if c:
            suf[k] = c
    pre = {}
    for k, vs in by_pre.items():
        if len(vs) < MIN_SAMPLES:
            continue
        c = major_prefix(vs)
        if c:
            pre[k] = c
    return suf, pre


def segments(suf, pre, whole):
    """把学到的前缀、后缀、整名合成一张「英文片段 → 中文」的表。

    片段之所以可信，是因为它是从一堆共享这个片段的条目里取的**公共前/后缀**：
    `Display Case` 结尾的十几条中文都以「展示柜」收尾，那这三个字就是它。
    """
    seg = {}
    for d in (suf, pre):
        for k, v in d.items():
            if v and (k not in seg or len(seg[k]) < len(v)):
                seg[k] = v
    for k, v in whole.items():
        seg.setdefault(k, v)
    return seg


def greedy(e, seg):
    """从左往右每次取能查到的最长片段。与最少段数那条路互相独立。"""
    w = e.split()
    out, i = [], 0
    while i < len(w):
        j = len(w)
        while j > i and ' '.join(w[i:j]) not in seg:
            j -= 1
        if j == i:
            return None
        out.append(seg[' '.join(w[i:j])])
        i = j
    return ''.join(out)


ASCII_OK = set(" -_/'()[]%.,:+&")


def sane(e, zh):
    """产物里不许出现英文原文没有的字母数字。

    `Block of Uranium` 拼出「铀-23」就是这么来的：某个片段的中文里混进了别处的
    数字。这条闸挡的正是这类——片段表是从一堆译文里统计出来的，偶尔会带进
    不属于这条的东西。
    """
    for ch in zh:
        if ch.isascii() and ch.isalnum() and ch.lower() not in e.lower():
            return False
    return True


def compose(e, seg, whole, maxseg=5):
    """按词做分段：整名能查到就直接用，否则切成几段各查各的再拼。

    段数越少越可信（`Black Eternal Starlight Banyin | Display Case` 好过
    逐词拼），所以搜索时优先长片段。任何一段查不到就整条放弃。
    """
    if e in whole:
        return whole[e], 'whole'
    w = e.split()
    n = len(w)
    best = {n: ('', 0)}
    for i in range(n - 1, -1, -1):
        for j in range(n, i, -1):
            piece = seg.get(' '.join(w[i:j]))
            if piece is None or j not in best:
                continue
            tail, cnt = best[j]
            if cnt + 1 > maxseg:
                continue
            cand = (piece + tail, cnt + 1)
            if i not in best or cand[1] < best[i][1]:
                best[i] = cand
    if 0 in best:
        return best[0][0], 'compose%d' % best[0][1]
    return None, None


def extra_terms(path):
    """手工补的词表：英文片段 → 中文。

    学习只能索引首尾片段——`Light Blue Couch` 里的 `Blue` 夹在中间，
    既不是前缀也不是后缀，于是「蓝色」这个词学不到。这类词由人（或模型）
    一次性定下来，放进 `src/pack/terms.json`，此后由脚本反复使用。
    """
    p = Path(path) if path else (ROOT / 'src' / 'pack' / 'terms.json')
    if not p.is_file():
        return {}
    d = json.loads(p.read_text(encoding='utf-8'))
    return {k: v for k, v in d.items() if not k.startswith('_') and isinstance(v, str)}


def main(mods, cfpa=None, write=False, terms=None):
    res = json.loads((ROOT / 'versions' / 'base_residue.json').read_text(encoding='utf-8'))
    residue = {(ns, k) for ns, items in res['lang_selftrans'].items() for k, _ in items}
    en, off = jar_langs(mods)
    cf = zip_langs(cfpa)
    ours = our_langs()

    votes = defaultdict(Counter)
    for src in (off, cf):
        for ns, kv in src.items():
            E = en.get(ns, {})
            for k, v in kv.items():
                e = E.get(k)
                if isinstance(e, str) and isinstance(v, str) and e.strip():
                    votes[e][v] += 1
    for ns, kv in ours.items():
        E = en.get(ns, {})
        for k, v in kv.items():
            if (ns, k) in residue:
                continue
            e = E.get(k)
            if isinstance(e, str) and isinstance(v, str) and e.strip():
                votes[e][v] += 1
    trusted = {e: c.most_common(1)[0][0] for e, c in votes.items() if len(c) == 1}
    suf, pre = learn(trusted)
    seg = segments(suf, pre, trusted)
    ex = extra_terms(terms)
    seg.update(ex)                    # 手工词表优先级最高
    if ex:
        print('手工词表 %d 条' % len(ex))
    print('可信英中对 %d 条（译法唯一）；学到后缀 %d 个、前缀 %d 个、片段表 %d 条'
          % (len(trusted), len(suf), len(pre), len(seg)))

    # **先验准确率再谈覆盖率**：拿一批已知正确的译名当留出集，把它们从片段表里
    # 摘掉之后重新拼，看拼出来的和真值一不一样。这个数不好看就别谈拼了多少条。
    import random
    rnd = random.Random(20260727)
    hold = [e for e in trusted if 2 <= len(e.split()) <= 6]
    rnd.shuffle(hold)
    hold = hold[:1500]
    ok = bad = skip = 0
    samples = []
    for e in hold:
        w2 = {k: v for k, v in trusted.items() if k != e}
        zh, how = compose(e, seg, w2)
        if zh is not None and how != 'whole' and (
                greedy(e, seg) != zh or not sane(e, zh)):
            zh = None
        if zh is None:
            skip += 1
        elif zh == trusted[e]:
            ok += 1
        else:
            bad += 1
            if len(samples) < 6:
                samples.append((e, trusted[e], zh))
    print('留出集 %d 条：拼对 %d、拼错 %d、拼不出 %d —— 拼得出来的里面正确率 %.1f%%'
          % (len(hold), ok, bad, skip, ok / max(1, ok + bad) * 100))
    for e, t, g in samples:
        print('     错例 %-46s 真值 %-14s 拼出 %s' % (e[:46], t, g))

    made, miss, changed = {}, [], 0
    for ns, items in res['lang_selftrans'].items():
        E = en.get(ns, {})
        for k, old in items:
            if not isinstance(old, str) or len(old) > MAX_LEN:
                continue
            e = E.get(k)
            if not e:
                miss.append((ns, k, old, 'no-en'))
                continue
            zh, how = compose(e, seg, trusted)
            if zh and how != 'whole':
                # 两条独立拼法必须拼出同一个结果，不一致说明这条有歧义
                if greedy(e, seg) != zh:
                    miss.append((ns, k, old, 'ambiguous'))
                    continue
                if not sane(e, zh):
                    miss.append((ns, k, old, 'stray-char'))
                    continue
            if not zh:
                miss.append((ns, k, old, 'no-term'))
                continue
            made.setdefault(ns, {})[k] = zh
            if zh != old:
                changed += 1
    total = sum(len(v) for v in made.values()) + len(miss)
    print('组合名 %d 条：拼出来 %d 条（其中 %d 条与底本不同），拼不出 %d 条'
          % (total, sum(len(v) for v in made.values()), changed, len(miss)))
    why = Counter(m[3] for m in miss)
    print('   拼不出的原因：%s' % dict(why))

    (ROOT / 'versions' / 'composed_names.json').write_text(
        json.dumps({'made': made, 'miss': miss}, ensure_ascii=False, indent=1) + '\n',
        encoding='utf-8')
    if write:
        n = 0
        for ns, kv in made.items():
            p = ROOT / 'src' / 'pack' / 'assets' / ns / 'lang' / 'zh_cn.json'
            if not p.is_file():
                continue
            cur = json.loads(p.read_text(encoding='utf-8-sig'))
            for k, v in kv.items():
                if cur.get(k) != v:
                    cur[k] = v
                    n += 1
            p.write_text(json.dumps(cur, ensure_ascii=False, indent=2) + '\n',
                         encoding='utf-8')
        print('已写入 %d 条' % n)
    return len(miss)


if __name__ == '__main__':
    a = sys.argv[1:]

    def arg(n, d=None):
        return a[a.index(n) + 1] if n in a else d

    if '--mods' not in a:
        sys.exit(__doc__)
    main(arg('--mods'), arg('--cfpa'), '--write' in a, arg('--terms'))
