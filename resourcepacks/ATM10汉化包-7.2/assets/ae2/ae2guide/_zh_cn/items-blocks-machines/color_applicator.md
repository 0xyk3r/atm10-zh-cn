---
navigation:
  parent: items-blocks-machines/items-blocks-machines-index.md
  title: 染色器
  icon: color_applicator
  position: 410
categories:
- tools
item_ids:
- ae2:color_applicator
---

# 染色器

<ItemImage id="color_applicator" scale="4" />

染色器用于给可染色的方块上色，例如[线缆](cables.md)、羊毛、陶瓦、玻璃和混凝土。它使用
[染色球](paintballs.md)或染料，而雪球可用于清除线缆上的颜色以及方块上的染色球污渍。

它的能量可以在<ItemLink id="charger" />中充能。

染色器的工作方式类似于[存储元](storage_cells.md)，而且将染色器放入 <ItemLink id="chest" /> 的存储元槽位中，是为其涂料存储补充内容最简单的方法

右键点击目标以应用所选颜色。若要更改颜色，请按住 shift 滚动鼠标滚轮，或在没有目标时右键点击。

## 升级

涂色器支持以下[升级](upgrade_cards.md)，通过 <ItemLink id="cell_workbench" /> 插入：

*   <ItemLink id="equal_distribution_card" /> 会为每种类型分配相同数量的单元字节空间，因此单一类型无法占满整个存储单元
*   如果存储单元已满，<ItemLink id="void_card" /> 会销毁插入的物品（或者在使用均匀分配卡时，销毁插入到该特定类型已分配空间中的物品）。请务必先对此进行分区！
*   <ItemLink id="energy_card" />，以提高它们的电池容量

## 配方

<RecipeFor id="color_applicator" />