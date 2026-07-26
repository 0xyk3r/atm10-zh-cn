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

1. **描边色 / 内部像素的划分**：先用最小值滤波把不透明区**整体腐蚀掉描边的厚度**
   （原图描边普遍有 3~4 像素厚，只排除紧贴透明的那一圈远远不够——剩下几层黑描边
   会被当成材质采进去，中文笔画上就是一块块黑斑）。腐蚀掉的外圈取中位色作描边色，
   腐蚀后活下来的才算内部像素；
2. **填充用原图的材质，不是单一颜色**：ATM 的标题字大多不是纯色——APOTHIC 是裂纹石头、
   UNDERGARDEN 是长苔石、EXTENDED AND ADVANCED AE 干脆是用方块贴图拼出来的立体字。
   只取一个颜色或一条竖向渐变，纹理和方块效果就全没了（"抠烂了"）。
   做法是按行提取原字内部（非描边）的像素序列，横向平铺成一张与画布同大的材质板，
   再用中文字形当遮罩去取色——中文看起来就像用同一种材料刻出来的。
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

## 字形：逐图判定，不是全套一种字

原图 154 张的字体各不相同——有 MC 那种方块像素字（CHAPTER 2 / Mekanism / Powah）、
有粗衬线（The Aether / Bumblezone / Nature's Aura）、有粗黑无衬线（Create / Artifacts）、
也有细体（Deeper and Darker / Integrated Dynamics）。全用同一种字既不像原作也不好看。

判定是机械的，不靠人眼逐张点名：

- **是不是像素字**：把不透明遮罩按 k×k 方格对齐检查（k 从大到小试），
  若某个 k≥2 能让每个格子内部要么全实要么全空，说明原图是 1 倍点阵放大 k 倍来的，
  即像素字体 → 用 Minecraft 自己的 Unifont 点阵渲染，放大倍率对齐原图的 k。
- **笔画粗细**：量平均笔画宽度占字高的比例，据此在细黑 / 粗黑 / 粗宋之间选。
- 少数明显是衬线体的（天境 / 嗡嗡领域 / 自然灵气 / 遗物 / 神秘学 等）在 SERIF 表里点名，
  走宋体 Black。

## 点阵渲染细节

早期版本用系统黑体渲染，字形是平滑矢量，跟原图的像素英文完全不搭。
正解是用 **Minecraft 渲染中文时用的那套字**——GNU Unifont，16×16 点阵，
整合包 assets 里就有（`minecraft/font/unifont.zip`，随资源索引下载，无需外部字体）。

流程：按 Unifont 的 `.hex` 位图在 **1 倍尺度**拼出文字 → 按整数倍**最近邻**放大到目标框。
这样笔画边缘是硬像素块，和原图的像素英文同一套观感；描边也在 1 倍尺度做膨胀再一起放大，
所以描边同样是方块状，不会出现矢量字那种圆滑边。

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

MARGIN = 4    # 原图四周的透明边
LINE_GAP = 2  # 多行时的行距（1 倍尺度像素）

# 矢量字备选：(路径, 索引)
FACE = {
    'thin':  ('/System/Library/Fonts/Hiragino Sans GB.ttc', 0),   # 冬青黑 W3
    'bold':  ('/System/Library/Fonts/Hiragino Sans GB.ttc', 2),   # 冬青黑 W6
    'serif': ('/System/Library/Fonts/Songti.ttc', 0),             # 宋体 SC Black
}
# 原图明显是衬线/装饰体的，点名走宋体
SERIF = {
    'aether/aether_title.png', 'bumblezone/bumble_title.png',
    'natures_aura/natures_aura_title.png', 'occultism/occultism_title.png',
    'draconic/draconic_title.png', 'apothic/gear_sigils.png', 'apothic/gear_tiers.png',
    'chap3/creative_items.png', 'chap3/creative_star.png',
    'undergarden/undergarden_title.png', 'relics/relics_title.png',
    'iron_spells/spells_title.png',
}


def pixel_scale(im):
    """原图是不是像素字？是就返回放大倍率 k，不是返回 1。

    判据一（硬）：像素字**没有抗锯齿**——alpha 只有 0 和 255 两种值。
    矢量渲染的标题字边缘一定有半透明过渡，这条一票否决。
    判据二：再找最大的 k，使得按 k×k 方格切开后几乎每格内部纯色。
    """
    a = im.getchannel('A')
    bb = a.getbbox()
    if not bb:
        return 1
    a = a.crop(bb)
    hist = a.histogram()
    tot = sum(hist)
    soft = tot - hist[0] - hist[255]
    if soft / max(1, tot) > 0.02:          # 有抗锯齿 → 矢量字
        return 1
    a = a.point(lambda v: 255 if v > 128 else 0)
    ap = a.load()
    W, H = a.size
    for k in range(8, 1, -1):
        if W // k < 4 or H // k < 4:
            continue
        bad = n = 0
        for by in range(H // k):
            for bx in range(W // k):
                v = {ap[bx * k + dx, by * k + dy] for dy in range(k) for dx in range(k)}
                n += 1
                if len(v) > 1:
                    bad += 1
        if n and bad / n < 0.02:
            return k
    return 1


def ink_density(im):
    """外接框内的着墨比例，用来选字重：粗体密、细体疏"""
    a = im.getchannel('A').point(lambda v: 255 if v > 128 else 0)
    bb = a.getbbox()
    if not bb:
        return 0.0
    a = a.crop(bb)
    return sum(1 for v in a.getdata() if v) / (a.size[0] * a.size[1])


def load_unifont():
    """Minecraft 自己用来渲染中文的 GNU Unifont（16×16 点阵），从游戏 assets 里取"""
    import json as _json, zipfile as _zip
    mc = INST.parent.parent
    ver = _json.loads((INST / (next(INST.glob('*.jar')).stem + '.json')).read_text(encoding='utf-8'))
    idx = _json.loads((mc / 'assets' / 'indexes' / (ver['assetIndex']['id'] + '.json'))
                      .read_text(encoding='utf-8'))['objects']
    h = idx['minecraft/font/unifont.zip']['hash']
    with _zip.ZipFile(mc / 'assets' / 'objects' / h[:2] / h) as z:
        name = next(n for n in z.namelist() if n.endswith('.hex'))
        raw = z.read(name).decode('ascii')
    g = {}
    for line in raw.splitlines():
        cp, bits = line.split(':')
        w = len(bits) // 4                      # 8 或 16 像素宽
        g[int(cp, 16)] = (w, [int(bits[r * (w // 4):(r + 1) * (w // 4)], 16) for r in range(16)])
    return g


UNIFONT = load_unifont()

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
    'extended_advanced_ae/title.png': ((18, 18, 22), (198, 202, 210)),  # 原字是深灰压深灰，采样出来看不清
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
    # ↓ 第二批：章节内的分区标签 / 生物名 / 阶级图等。生物与 Boss 名一律取模组 lang 的官方译名。
    # 纯图标（无文字）的不在此列：apothic/gear_{augment,gem,reforge,salvage,simple,smith}、
    # apothic/enchant_{deep,end,nether,ocean}（是书架插图）、chap3/creative_{crucible4,enchanter5,forge4}、
    # extremereactors/titleimage2；building_tips/building_title_* 是建筑师本人的 ID，属人名，不翻。
    'apothic/enchant_arcana.png': '阿卡那',
    'apothic/enchant_eterna.png': '位阶',
    'apothic/enchant_infusions.png': '灌注',
    'apothic/enchant_quanta.png': '量子化',
    'apothic/gear_sigils.png': '印记',
    'apothic/gear_tiers.png': '世界层级',
    'basicarmor/armor_colors.png': '纹饰颜色',
    'basicarmor/armor_trims.png': '盔甲纹饰',
    'bumblezone/bumble_title_armor.png': '护甲',
    'bumblezone/bumble_title_mobs.png': '生物',
    'bumblezone/bumble_title_progression.png': '进度',
    'bumblezone/bumble_title_special.png': '特殊',
    'bumblezone/bumble_title_structures.png': '结构',
    'bumblezone/bumble_title_tools.png': '工具',
    'cataclysm/cataclysm_title_guardian.png': '末影守卫',
    'cataclysm/cataclysm_title_habinger.png': '先驱者',
    'cataclysm/cataclysm_title_ignis.png': '焰魔',
    'cataclysm/cataclysm_title_items.png': '组合物品',
    'cataclysm/cataclysm_title_leviathan.png': '利维坦',
    'cataclysm/cataclysm_title_maledictus.png': '咒翼灵骸',
    'cataclysm/cataclysm_title_monstrosity.png': '下界合金巨兽',
    'cataclysm/cataclysm_title_remnant.png': '远古遗魂',
    'cataclysm/cataclysm_title_scylla.png': '斯库拉',
    'chap2/atmstar_title1.png': '第三章',
    'chap2/atmstar_title2.png': 'ATM之星',
    'chap3/creative_chap4.png': '第四章',
    'chap3/creative_creative.png': '创造',
    'chap3/creative_items.png': '创造物品',
    'chap3/creative_star.png': '之星自动化',
    'create/create_title_contrapt.png': '装置',
    'create/create_title_fluid.png': '流体物流',
    'create/create_title_item.png': '物品物流',
    'create/create_title_machines.png': '机器',
    'create/create_title_power.png': '旋转\n动力',
    'create/create_title_tool.png': '工具',
    'create/create_title_trains.png': '火车',
    'deepndark/dnd_biome.png': '生物群系',
    'deepndark/dnd_blocks.png': '方块',
    'deepndark/dnd_gear.png': '装备',
    'deepndark/dnd_mobs.png': '生物',
    'deepndark/dnd_plants.png': '植物',
    'eternal/starlight_title1.png': '永恒',
    'eternal/starlight_title2.png': '星光',
    'extended_advanced_ae/title.png': '拓展AE\n与高级AE',
    'extremereactors/title2.png': '极限反应堆',
    'forbidden/forbidden_title_tier1.png': '第一阶',
    'forbidden/forbidden_title_tier2.png': '第二阶',
    'forbidden/forbidden_title_tier3.png': '第三阶',
    'forbidden/forbidden_title_tier4.png': '第四阶',
    'forbidden/forbidden_title_tier5.png': '第五阶',
    'iceandfire/iaf_title_1.png': '冰',
    'iceandfire/iaf_title_2.png': '与',
    'iceandfire/iaf_title_3.png': '火',
    'iceandfire/iaf_title_amphithere.png': '翼蚺',
    'iceandfire/iaf_title_birds.png': '鸟类',
    'iceandfire/iaf_title_cockatrice.png': '鸡蛇',
    'iceandfire/iaf_title_cyclops.png': '独眼巨人',
    'iceandfire/iaf_title_firedragon.png': '火龙',
    'iceandfire/iaf_title_ghosts.png': '幽灵',
    'iceandfire/iaf_title_gorgon.png': '蛇发女妖',
    'iceandfire/iaf_title_hippocampus.png': '海马',
    'iceandfire/iaf_title_hippogryth.png': '骏鹰',
    'iceandfire/iaf_title_hydra.png': '九头蛇',
    'iceandfire/iaf_title_icedragon.png': '冰龙',
    'iceandfire/iaf_title_lightningdragon.png': '电龙',
    'iceandfire/iaf_title_pets.png': '宠物',
    'iceandfire/iaf_title_pixie.png': '小精灵',
    'iceandfire/iaf_title_serpent.png': '海蟒',
    'iceandfire/iaf_title_siren.png': '塞壬',
    'iceandfire/iaf_title_stymphalian.png': '铜羽泽鹗',
    'iceandfire/iaf_title_trolls.png': '食人妖',
    'iceandfire/iaf_title_worm.png': '死亡蠕虫',
    'immersive/immersive_title_log.png': '物流',
    'immersive/immersive_title_mac.png': '机器',
    'immersive/immersive_title_oad.png': '攻防',
    'immersive/immersive_title_sma.png': '小型机器',
    'immersive/immersive_title_tol.png': '工具',
    'immersive/immersive_title_upg.png': '升级',
    'immersive/immersive_title_wir.png': '布线',
    'mahou/mahou_bow.png': '武器投影之弓',
    'mahou/mahou_caliburn.png': '石中剑',
    'mahou/mahou_clarent.png': '克拉伦特',
    'mahou/mahou_disorientation.png': '次元扭曲魔杖',
    'mahou/mahou_emrys.png': '艾米雷斯',
    'mahou/mahou_explosion.png': '爆炸魔杖',
    'mahou/mahou_generation.png': '魔力生成',
    'mahou/mahou_keys.png': '赤之黑键',
    'mahou/mahou_morgan.png': '摩根',
    'mahou/mahou_nobu.png': '诺布',
    'mahou/mahou_replica.png': '暗夜之影',
    'mahou/mahou_tsukai.png': '魔法使',
    'mek/mek_title_1.png': '一级矿物处理',
    'mek/mek_title_2.png': '二级矿物处理',
    'mek/mek_title_3.png': '三级矿物处理',
    'mek/mek_title_4.png': '四级矿物处理',
    'mek/mek_title_advanced.png': '高级',
    'mek/mek_title_antimatter.png': '反物质',
    'mek/mek_title_basic.png': '基础',
    'mek/mek_title_boiler.png': '热电煮沸器',
    'mek/mek_title_elite.png': '精英',
    'mek/mek_title_energy.png': '能量',
    'mek/mek_title_fission.png': '裂变反应堆',
    'mek/mek_title_fusion.png': '聚变反应堆',
    'mek/mek_title_logistics.png': '物流',
    'mek/mek_title_machines.png': '机器',
    'mek/mek_title_matrix.png': '感应矩阵',
    'mek/mek_title_mo.png': '更多机器',
    'mek/mek_title_module.png': '模块',
    'mek/mek_title_qio.png': 'QIO',
    'mek/mek_title_reactor.png': '通用机械反应堆',
    'mek/mek_title_sps.png': 'SPS',
    'mek/mek_title_suit.png': '通用装甲',
    'mek/mek_title_tools.png': '工具',
    'mek/mek_title_turbine.png': '涡轮',
    'mek/mek_title_ultimate.png': '终极',
    'mek/mek_title_upgrades.png': '升级',
    'mystical_agriculture/machines.png': '机器',
    'undergarden/undergarden_biomes.png': '生物群系',
    'undergarden/undergarden_friendly.png': '友好',
    'undergarden/undergarden_hostile.png': '敌对',
    'undergarden/undergarden_neutral.png': '中立',
    'undergarden/undergarden_tools.png': '工具与护甲',
    'undergarden/undergarden_vegetation.png': '植被',
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
    from PIL import ImageFilter
    px = im.load()
    W, H = im.size
    if not im.getbbox():
        return (0, 0, 0), Image.new('RGB', (max(1, W), max(1, H)), (255, 255, 255)), 2, '空'
    # 描边厚度按图高估：原图描边普遍是字高的 4~5%
    ring = max(1, round(H * 0.05))
    a = im.getchannel('A').point(lambda v: 255 if v > 200 else 0)
    er = a.filter(ImageFilter.MinFilter(2 * ring + 1))     # 腐蚀掉描边那几层
    ap, ep = a.load(), er.load()
    edge, inner = [], {}
    for y in range(H):
        for x in range(W):
            if not ap[x, y]:
                continue
            (inner.setdefault(y, []) if ep[x, y] else edge).append(px[x, y][:3])

    def med(seq):
        return tuple(int(statistics.median(c[i] for c in seq)) for i in range(3))

    if not inner:                       # 字太细，腐蚀后什么都不剩，退回不腐蚀
        for y in range(H):
            for x in range(W):
                if ap[x, y]:
                    inner.setdefault(y, []).append(px[x, y][:3])
    # 描边色取腐蚀掉的外圈里**最深**的那一档，避免把渐变亮部当描边
    if edge:
        edge.sort(key=sum)
        outline = med(edge[:max(1, len(edge) // 3)])
    else:
        outline = (0, 0, 0)
    ys = sorted(inner)
    if not ys:
        return outline, Image.new('RGB', (W, H), (255, 255, 255)), max(2, round(H * 0.045)), '空'
    # 切成一条条连续的「有墨行」，只留最高的那条 —— 多行异色的原图（APOTHIC 灰 /
    # ENCHANTING 紫）整块一起用会让中文上下两截色
    peak = max(len(v) for v in inner.values())
    runs, cur = [], []
    for y in range(ys[0], ys[-1] + 1):
        if len(inner.get(y, ())) >= peak * 0.06:
            cur.append(y)
        elif cur:
            runs.append(cur); cur = []
    if cur:
        runs.append(cur)
    band = [y for y in (max(runs, key=len) if runs else ys) if y in inner]
    # 材质板：每一行把该行原字内部的像素序列横向平铺满整宽，再纵向拉伸到画布高。
    # 这样石纹/苔藓/方块贴图都留得住，而不是塌成一个颜色。
    plate = Image.new('RGB', (W, len(band)))
    pp = plate.load()
    for j, y in enumerate(band):
        seq = inner[y]
        for x in range(W):
            pp[x, j] = seq[x % len(seq)]
    # 横向做一次窄窗平滑：平铺会把字母片段反复重复，直接用会看出周期性拖影
    from PIL import ImageFilter
    plate = plate.filter(ImageFilter.GaussianBlur(max(1, W / 240)))
    return outline, plate.resize((W, H), Image.LANCZOS), max(2, round(H * 0.045)), '材质'


def render(text, w, h, outline, plate, sw):
    """用 Unifont 位图排字，整数倍最近邻放大后按材质板上色"""
    lines = text.split('\n')
    rows = []
    for ln in lines:
        gs = [UNIFONT.get(ord(c), (16, [0] * 16)) for c in ln]
        rows.append((sum(g[0] for g in gs), gs))
    W1 = max(r[0] for r in rows)
    H1 = len(rows) * 16 + (len(rows) - 1) * LINE_GAP

    # 1 倍尺度的字形遮罩
    core1 = [[0] * W1 for _ in range(H1)]
    for li, (lw, gs) in enumerate(rows):
        x0 = (W1 - lw) // 2
        y0 = li * (16 + LINE_GAP)
        for gw, bm in gs:
            for r in range(16):
                bits = bm[r]
                for c in range(gw):
                    if bits >> (gw - 1 - c) & 1:
                        core1[y0 + r][x0 + c] = 1
            x0 += gw

    # 描边：1 倍尺度上按切比雪夫距离膨胀 ow 圈，放大后就是方块状的粗描边
    aw, ah = w - 2 * MARGIN, h - 2 * MARGIN
    ow = 1 if sw <= 6 else 2
    k = max(1, min((aw) // (W1 + 2 * ow), (ah) // (H1 + 2 * ow)))
    pad = ow
    AW, AH = W1 + 2 * pad, H1 + 2 * pad
    all1 = [[0] * AW for _ in range(AH)]
    for y in range(H1):
        for x in range(W1):
            if core1[y][x]:
                for dy in range(-ow, ow + 1):
                    for dx in range(-ow, ow + 1):
                        all1[y + pad + dy][x + pad + dx] = 1

    gw, gh = AW * k, AH * k
    tex = plate.resize((max(1, gw), max(1, gh)), Image.LANCZOS).load()
    glyph = Image.new('RGBA', (gw, gh), (0, 0, 0, 0))
    gp = glyph.load()
    for Y in range(gh):
        y1 = Y // k
        for X in range(gw):
            x1 = X // k
            if not all1[y1][x1]:
                continue
            inside = 0 <= y1 - pad < H1 and 0 <= x1 - pad < W1 and core1[y1 - pad][x1 - pad]
            gp[X, Y] = (tex[X, Y] + (255,)) if inside else (outline + (255,))
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
        outline, plate, sw, how = sample_style(sub)
        if rel in STYLE:      # 少数原图字色与底纹太接近，采样出来看不清，直接给定
            outline = STYLE[rel][0]
            plate = Image.new('RGB', plate.size, STYLE[rel][1])
            how = '指定色'
        img, gw, gh = render(text, sub.width, sub.height, outline, plate, sw)
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
        print('  %-50s %-7s %-8s %dx%d%s' % (rel, text, how, im.width, im.height, note))
        n += 1
    print(('校验通过' if check_only else '已生成') + ' %d 张 -> %s' % (n, OUT.relative_to(ROOT)))


if __name__ == '__main__':
    main(check_only='--check' in sys.argv)
