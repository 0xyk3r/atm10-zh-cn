#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# atm10-zh-cn — All the Mods 10 简体中文汉化补丁「绿油油版」
# Copyright (C) 2026 星野夢華 (Hoshino Yumeka)
# SPDX-License-Identifier: GPL-3.0-or-later
"""任务书章节横幅上的文字（烤进 PNG，语言文件够不着）。

ATM 的任务书章节顶上挂的是图片（`images:` 字段），文字直接画在 PNG 里。
原图在 `kubejs/assets/atm/textures/questpics/`，是整合包自带的散装文件；
资源包的加载顺序排在 KubeJS 之后（见 ReloadableResourceManager 日志），
所以本包放同路径的 `assets/atm/textures/questpics/...` 就能覆盖它们。

## 只翻这 6 张

带文字的横幅共 35 张，其中：
- **25 张是模组自己的品牌 logo**（Mekanism / Create / Twilight Forest / Occultism…），
  按「品牌名不硬翻」的口径保持英文；
- 4 张压根不是文字（木框、末影人图标、五芒星、气动工艺图标）；
- 剩下 6 张是通用词，翻了才有意义，就是下面这张表。

## 画法

原图是「纯文字 + 透明底」，所以整张重画即可，不需要抠。
每张的填充色取原图最多的实心像素、描边色照原图目测配对；
字号按 `min(可用宽/文字宽, 可用高/文字高)` 等比放到最大，居中。
渲染走 4 倍超采样再缩回，边缘和原图一样顺滑。

字体是 macOS 自带的，Linux CI 上没有，故不做 CI 漂移检查；改完本机重跑即可。

用法:
    python3 scripts/gen_quest_banners.py            # 重新生成 6 张
    python3 scripts/gen_quest_banners.py --check    # 只算尺寸不写文件
"""
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    sys.exit('需要 Pillow：python3 -m pip install Pillow')

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'resourcepacks' / 'ATM10汉化包-7.2' / 'assets' / 'atm' / 'textures' / 'questpics'
SRC = Path('/Users/yumeka/Documents/minecraft/.minecraft/versions/All the Mods 10'
           '/kubejs/assets/atm/textures/questpics')

FONT_CANDIDATES = [
    ('/System/Library/Fonts/Hiragino Sans GB.ttc', 2),   # 冬青黑体简体中文 W6
    ('/System/Library/Fonts/STHeiti Medium.ttc', 1),     # 黑体-简 Medium
    ('/System/Library/Fonts/PingFang.ttc', 4),           # 苹方-简 Medium
]
FONT, FONT_INDEX = next(((f, i) for f, i in FONT_CANDIDATES if Path(f).exists()), (None, 0))
if FONT is None:
    sys.exit('找不到可用的中文字体，候选：%s' % [f for f, _ in FONT_CANDIDATES])

SS = 4        # 超采样倍数
MARGIN = 4    # 原图四周留的透明边，照抄

# 相对路径 → (中文, 填充色, 描边色, 描边宽(原图像素))
BANNERS = {
    'allthemodium/all_title.png':        ('第二章',   (233, 233, 233), (0, 0, 0), 5),
    'basicarmor/armor_title.png':        ('基础护甲', (157, 209, 255), (23, 22, 22), 4),
    'powah/text/generation_text.png':    ('发电',     (26, 173, 255), (255, 255, 255), 4),
    'powah/text/storage_text.png':       ('储能',     (26, 173, 255), (255, 255, 255), 4),
    'powah/text/transfer_text.png':      ('传输',     (26, 173, 255), (255, 255, 255), 4),
    'powah/text/useful_items_text.png':  ('实用物品', (26, 173, 255), (255, 255, 255), 4),
}


def render(text, w, h, fill, stroke, sw):
    """在 w×h 画布上把 text 等比放到最大并居中"""
    aw, ah = w - 2 * MARGIN, h - 2 * MARGIN
    size = ah                                   # 初值：按高度猜
    for _ in range(12):                         # 迭代逼近
        f = ImageFont.truetype(FONT, max(1, size) * SS, index=FONT_INDEX)
        probe = Image.new('RGBA', (w * SS * 3, h * SS * 3), (0, 0, 0, 0))
        ImageDraw.Draw(probe).text((w * SS, h * SS), text, font=f, fill=fill,
                                   stroke_width=sw * SS, stroke_fill=stroke)
        bb = probe.getbbox()
        tw, th = (bb[2] - bb[0]) / SS, (bb[3] - bb[1]) / SS
        k = min(aw / tw, ah / th)
        if abs(k - 1) < 0.01:
            break
        size = max(1, size * k)
    glyph = probe.crop(bb)
    gw = max(1, round(glyph.width / SS))
    gh = max(1, round(glyph.height / SS))
    glyph = glyph.resize((gw, gh), Image.LANCZOS)
    canvas = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    canvas.alpha_composite(glyph, ((w - gw) // 2, (h - gh) // 2))
    return canvas, gw, gh


def main(check_only=False):
    n = 0
    for rel, (text, fill, stroke, sw) in sorted(BANNERS.items()):
        src = SRC / rel
        if not src.exists():
            sys.exit('❌ 找不到原图 %s（本脚本要对着整合包实例跑）' % src)
        w, h = Image.open(src).size
        img, gw, gh = render(text, w, h, fill + (255,), stroke + (255,), sw)
        if not check_only:
            dst = OUT / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            img.save(dst)
        print('  %-34s %-6s 画布 %dx%d → 字 %dx%d' % (rel, text, w, h, gw, gh))
        n += 1
    print(('校验通过' if check_only else '已生成') + ' %d 张 -> %s'
          % (n, OUT.relative_to(ROOT)))


if __name__ == '__main__':
    main(check_only='--check' in sys.argv)
