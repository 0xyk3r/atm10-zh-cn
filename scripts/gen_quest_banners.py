#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# atm10-zh-cn — All the Mods 10 简体中文汉化补丁「绿油油版」
# Copyright (C) 2026 星野夢華 (Hoshino Yumeka)
# SPDX-License-Identifier: GPL-3.0-or-later
"""任务书章节横幅上的艺术字（烤进 PNG，语言文件够不着）。

ATM 的任务书每章顶上挂一张标题图，文字直接画在 PNG 里。原图在整合包自带的
`kubejs/assets/atm/textures/questpics/`，资源包的加载顺序排在 KubeJS 之后
（对着 ReloadableResourceManager 日志核过），所以本包放同路径的图即可覆盖。

## 写什么字：单一真源 = 该图所属章节的中文标题

每张标题图都只被一个章节引用（脚本启动时会重新核验），所以直接取那一章
已有的中文标题，不另造词。这样任务书侧边栏、章节标题、横幅三处永远一致。

## 怎么画：从原图采样，而不是逐张手调

这些是带渐变和描边的艺术字，一张张配色调不过来，也不可复现。做法是：

1. **描边色**：取「不透明但四邻里有透明像素」的那一圈的中位色；
2. **填充渐变**：把原图内容区按行切片，每行取非描边实心像素的中位色，
   得到一条竖向渐变，再按相对高度重采样到新字上——原图是金色渐变，
   中文就也是金色渐变。
   **只取最高的那一条文字带**：不少原图是两行且两行异色（APOTHIC 灰 / ENCHANTING 紫、
   DRACONIC / EVOLUTION、INDUSTRIAL FOREGOING 加一行小字副标），
   整块一起采会把「上灰下紫」当成渐变，映到一行中文上就是拦腰一道色带（斑纹）；
3. **描边宽度**：按图高的 4.5% 估，最少 2px；
4. 文字按 `min(可用宽/字宽, 可用高/字高)` 等比放到最大后居中，
   4 倍超采样渲染再缩回，边缘与原图同级顺滑。

**尺寸基准是原图的内容框，不是整块画布** —— 有些图（如 id_title 400×400）文字只占
中间一条，按整块画布铺满会让中文比原文大一圈，贴进任务书的固定框里就撑爆了。

## 带装饰的图：只换文字框

少数图除了文字还有别的东西（神秘学两侧站着两只怪、气动工艺右边有小图标、
暮色森林的字压在一条石砖带上）。整张重画会把这些一起抹掉，所以给它们单独标出
「只有英文字的那个框」（按百分比），只在框内替换；框外原样保留。
暮色森林那条石砖带被文字压着，抹掉会留个洞，所以从文字上方干净的砖行取一条
纹理平铺补上。

字体用系统自带的中粗黑体。找不到像素风中文字体，所以字形风格无法与原图的
像素英文完全一致——这是这类「艺术字汉化」的固有限制（社区通行做法要么就是
重绘、要么干脆保留英文）。本包选择重绘：宁可字体风格不完全一致，
也不要同一本任务书里中英横幅混杂。

## 例外：不动的图

- 4 张压根不是文字（木框、末影人图标、五芒星、气动工艺图标）
- 章节里那些非标题的插图（矿车、生物图鉴等）本来就没字

用法:
    python3 scripts/gen_quest_banners.py            # 重新生成
    python3 scripts/gen_quest_banners.py --check    # 只算尺寸不写文件
"""
import re
import statistics
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    sys.exit('需要 Pillow：python3 -m pip install Pillow')

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'resourcepacks' / 'ATM10汉化包-7.2' / 'assets' / 'atm' / 'textures' / 'questpics'
INST = Path('/Users/yumeka/Documents/minecraft/.minecraft/versions/All the Mods 10')
SRC = INST / 'kubejs' / 'assets' / 'atm' / 'textures' / 'questpics'
QUESTS = INST / 'config' / 'ftbquests' / 'quests'

FONT_CANDIDATES = [
    ('/System/Library/Fonts/Hiragino Sans GB.ttc', 2),   # 冬青黑体简体中文 W6
    ('/System/Library/Fonts/STHeiti Medium.ttc', 1),     # 黑体-简 Medium
    ('/System/Library/Fonts/PingFang.ttc', 4),           # 苹方-简 Medium
]
FONT, FONT_INDEX = next(((f, i) for f, i in FONT_CANDIDATES if Path(f).exists()), (None, 0))
if FONT is None:
    sys.exit('找不到可用的中文字体，候选：%s' % [f for f, _ in FONT_CANDIDATES])

SS = 4        # 超采样倍数
MARGIN = 4    # 原图四周的透明边

# 图 → 中文。取值来自「引用该图那一章的中文标题」，脚本会核验对得上。
# 少数几条与章节标题不同，原因写在行尾。
# 带装饰的图：(左, 上, 右, 下) 百分比 —— 只有英文字的那个框；框外原样保留。
# inpaint=True 表示框内是有底纹的（不能直接抹成透明），从 patch_from 那几行取纹理平铺。
BOXES = {
    'occultism/occultism_title.png': dict(box=(16, 27, 73, 67)),                 # 左右两只怪要留
    'pneumaticcraft/pnc_title.png':  dict(box=(0, 0, 92, 100)),                  # 右侧小图标要留
    'twilight_forest_title.png':     dict(box=(5, 18, 95, 72), patch_from=(86, 96)),  # 字压在石砖带上
}

# 少数图自动采样会采到底纹/装饰而不是字本身，颜色发灰看不清，这里直接给定
# （描边色, 填充色）。数值取自原图英文字的实际颜色。
STYLE = {
    'twilight_forest_title.png':  ((16, 40, 28), (86, 240, 190)),   # 字压在石砖上，采样会采到砖
    'ars/ars_nouveau_title.png':  ((58, 12, 78), (196, 96, 234)),   # 原字是发光紫，中位色偏暗
    'router/router_title.png':    ((54, 36, 18), (242, 222, 172)),  # 原字是米色，底纹拉灰了
    'occultism/occultism_title.png': ((28, 6, 34), (150, 40, 168)),
    'allthemodium/all_title.png': ((0, 0, 0), (236, 236, 236)),      # 原字自带上下两色调，会成一道横带
    'id_title.png':              ((22, 58, 68), (126, 238, 252)),
}

BANNERS = {
    'aether/aether_title.png':                              '天境',
    'allthemodium/all_title.png':                           '第二章',      # 该图是章节序号，不是章名
    'apothic/logo.png':                                     '神化附魔',
    'apothic/spawners_title.png':                           '神化刷怪笼',
    'ars/ars_nouveau_title.png':                            '新生魔艺',
    'artifacts/artifacts_title.png':                        '奇异饰品',
    'basicarmor/armor_title.png':                           '基础护甲',
    'bumblezone/bumble_title.png':                          '嗡嗡领域',
    'cataclysm/cataclysm_title.png':                        '灾变',
    'create/create_title.png':                              '机械动力',
    'deepndark/dnd_title.png':                              '更深更暗',
    'draconic/draconic_title.png':                          '龙之进化',
    'forbidden/forbidden_title.png':                        '禁忌与奥秘',
    'id_title.png':                                         '动态\n联合',   # 原图两行，画布 400x400，单行会缩得很小
    'immersive/immersive_title.png':                        '沉浸工程',
    'industrialforegoing/industrial_foregoing_title.png':   '工业先锋',
    'iron_spells/spells_title.png':                         '铁魔法',      # 章节标题仍夹英文，横幅用社区通用名
    'mek/mek_title.png':                                    '通用机械',
    'natures_aura/natures_aura_title.png':                  '自然灵气',
    'occultism/occultism_title.png':                        '神秘学',
    'oritech/oritech-logo.png':                             '奥瑞科技',
    'pneumaticcraft/pnc_title.png':                         '气动工艺',
    'powah/text/generation_text.png':                       '发电',        # 章节内的分区标签
    'powah/text/storage_text.png':                          '储能',
    'powah/text/transfer_text.png':                         '传输',
    'powah/text/useful_items_text.png':                     '实用物品',
    'pylons/pylon_title.png':                               '实用塔',
    'relics/relics_title.png':                              '遗物',
    'router/router_title.png':                              '模块化\n路由器',   # 原图就是两行，画布近正方，单行会缩得很小
    'twilight_forest_title.png':                            '暮色森林',
    'undergarden/undergarden_title.png':                    '深暗之园',
}


def crop_box(im, rel):
    """→ (取样/绘制用的子图, 粘回原图的左上角坐标, 该图是否要保留框外内容)"""
    cfg = BOXES.get(rel)
    if cfg:
        x0, y0, x1, y1 = cfg['box']
        r = (round(im.width * x0 / 100), round(im.height * y0 / 100),
             round(im.width * x1 / 100), round(im.height * y1 / 100))
        return im.crop(r), (r[0], r[1]), cfg
    bb = im.getbbox() or (0, 0, im.width, im.height)   # 默认：原图内容框
    return im.crop(bb), (bb[0], bb[1]), None


def sample_style(im):
    """从原图采出（描边色, 竖向渐变色表, 描边宽）"""
    px = im.load()
    W, H = im.size
    solid = [(x, y) for y in range(H) for x in range(W) if px[x, y][3] > 200]
    if not solid:
        return (0, 0, 0), [(255, 255, 255)], 2
    edge, inner = [], {}
    for x, y in solid:
        out = any(not (0 <= x + dx < W and 0 <= y + dy < H) or px[x + dx, y + dy][3] < 64
                  for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
        (edge if out else inner.setdefault(y, [])).append(px[x, y][:3])
    def med(seq):
        return tuple(int(statistics.median(c[i] for c in seq)) for i in range(3))
    outline = med(edge) if edge else (0, 0, 0)
    ys = sorted(inner)
    if not ys:
        return outline, [(255, 255, 255)], max(2, round(H * 0.045))
    # 切成一条条连续的「有墨行」，只留最高的那条 —— 多行异色的原图不能整块当渐变采
    peak = max(len(v) for v in inner.values())
    runs, cur = [], []
    for y in range(ys[0], ys[-1] + 1):
        if len(inner.get(y, ())) >= peak * 0.06:
            cur.append(y)
        elif cur:
            runs.append(cur); cur = []
    if cur:
        runs.append(cur)
    band = max(runs, key=len) if runs else ys
    grad = [med(inner[y]) for y in band if y in inner] or [med([c for v in inner.values() for c in v])]
    # 逐行中位色本身是抖的（像素画一行里深浅块交替），直接拿去拉伸会变成一条条横纹。
    # 先做滑动平均抹平，取样时再线性插值（见 render），两步一起才不出斑纹。
    w = max(1, len(grad) // 6)
    grad = [tuple(sum(g[i] for g in grad[max(0, j - w):j + w + 1])
                  // len(grad[max(0, j - w):j + w + 1]) for i in range(3))
            for j in range(len(grad))]
    return outline, grad, max(2, round(H * 0.045))


def render(text, w, h, outline, grad, sw):
    aw, ah = w - 2 * MARGIN, h - 2 * MARGIN
    size = ah
    for _ in range(12):
        f = ImageFont.truetype(FONT, max(1, int(size)) * SS, index=FONT_INDEX)
        big = (w * SS * 3, h * SS * 3)
        allm = Image.new('L', big, 0)
        ImageDraw.Draw(allm).text((w * SS, h * SS), text, font=f, fill=255,
                                  stroke_width=sw * SS, stroke_fill=255,
                                  align='center', spacing=int(size * SS * 0.12))
        bb = allm.getbbox()
        tw, th = (bb[2] - bb[0]) / SS, (bb[3] - bb[1]) / SS
        k = min(aw / tw, ah / th)
        if abs(k - 1) < 0.01:
            break
        size = max(1, size * k)
    core = Image.new('L', big, 0)
    ImageDraw.Draw(core).text((w * SS, h * SS), text, font=f, fill=255,
                              align='center', spacing=int(size * SS * 0.12))
    allm, core = allm.crop(bb), core.crop(bb)
    gw, gh = max(1, round(allm.width / SS)), max(1, round(allm.height / SS))
    allm = allm.resize((gw, gh), Image.LANCZOS)
    core = core.resize((gw, gh), Image.LANCZOS)

    glyph = Image.new('RGBA', (gw, gh), (0, 0, 0, 0))
    ga, gc, gp = allm.load(), core.load(), glyph.load()
    n = len(grad)
    for y in range(gh):
        # 线性插值，不用最近邻——源色带常比目标字高矮，最近邻会把同一色重复若干行再跳变
        f = y / max(1, gh - 1) * (n - 1)
        i0 = min(n - 1, int(f)); i1 = min(n - 1, i0 + 1); t0 = f - i0
        col = tuple(round(grad[i0][k] + (grad[i1][k] - grad[i0][k]) * t0) for k in range(3))
        for x in range(gw):
            a = ga[x, y]
            if not a:
                continue
            t = gc[x, y] / 255
            gp[x, y] = (round(outline[0] + (col[0] - outline[0]) * t),
                        round(outline[1] + (col[1] - outline[1]) * t),
                        round(outline[2] + (col[2] - outline[2]) * t), a)
    canvas = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    canvas.alpha_composite(glyph, ((w - gw) // 2, (h - gh) // 2))
    return canvas, gw, gh


def chapter_titles():
    """图 → 引用它的章节中文标题（用于核验译名没跑偏）"""
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from check_quest_item_names import parse_lang, strip
    zh = parse_lang(str(QUESTS / 'lang' / 'zh_cn.snbt'))
    delta = ROOT / 'config' / 'ftbquests' / 'quests' / 'lang' / 'zh_cn' / 'chapters'
    for p in sorted(delta.glob('*.snbt')):
        zh.update(parse_lang(str(p)))
    out = {}
    for p in sorted((QUESTS / 'chapters').glob('*.snbt')):
        src = p.read_text(encoding='utf-8')
        m = re.search(r'\bid: "([0-9A-F]{16})"', src)
        if not m:
            continue
        t = strip(zh.get('chapter.%s.title' % m.group(1), ''))
        for img in set(re.findall(r'questpics/([a-z0-9_/-]+)\.png', src)):
            out.setdefault(img + '.png', []).append(t)
    return out


def main(check_only=False):
    titles = chapter_titles()
    n = 0
    for rel, text in sorted(BANNERS.items()):
        src = SRC / rel
        if not src.exists():
            sys.exit('❌ 找不到原图 %s（本脚本要对着整合包实例跑）' % src)
        used = titles.get(rel, [])
        if len(used) > 1:
            sys.exit('❌ %s 被多个章节引用 %s，不能写死一个标题' % (rel, used))
        im = Image.open(src).convert('RGBA')
        sub, at, cfg = crop_box(im, rel)
        outline, grad, sw = sample_style(sub)
        if rel in STYLE:
            outline, grad = STYLE[rel][0], [STYLE[rel][1]]
        img, gw, gh = render(text, sub.width, sub.height, outline, grad, sw)
        if cfg:
            # 保留框外的装饰：在原图上抠掉文字框，再把中文贴回去
            canvas = im.copy()
            if 'patch_from' in cfg:      # 框内有底纹，取干净的几行平铺补上
                a, b = cfg['patch_from']
                ya, yb = round(im.height * a / 100), round(im.height * b / 100)
                strip = im.crop((at[0], ya, at[0] + sub.width, yb))
                for y in range(0, sub.height, max(1, strip.height)):
                    canvas.paste(strip, (at[0], at[1] + y))
            else:
                canvas.paste(Image.new('RGBA', sub.size, (0, 0, 0, 0)), at)
            canvas.alpha_composite(img, at)
            img = canvas
        else:
            canvas = Image.new('RGBA', im.size, (0, 0, 0, 0))
            canvas.alpha_composite(img, at)
            img = canvas
        if not check_only:
            dst = OUT / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            img.save(dst)
        note = '' if (not used or used[0] == text) else '  ← 与章节标题「%s」不同' % used[0]
        print('  %-50s %-7s %dx%d 描边%s宽%d 渐变%d色%s'
              % (rel, text, im.width, im.height, outline, sw, len(grad), note))
        n += 1
    print(('校验通过' if check_only else '已生成') + ' %d 张 -> %s' % (n, OUT.relative_to(ROOT)))


if __name__ == '__main__':
    main(check_only='--check' in sys.argv)
