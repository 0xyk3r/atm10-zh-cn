---
navigation:
  parent: items-blocks-machines/items-blocks-machines-index.md
  title: 物质炮
  icon: matter_cannon
  position: 410
categories:
- tools
item_ids:
- ae2:matter_cannon
---

# 物质炮

<ItemImage id="matter_cannon" scale="4" />

物质加农炮是一种便携式超电磁炮，可以将小型物品作为弹射物发射出去，例如 <ItemLink id="matter_ball" /> 和金粒。造成的伤害取决于发射的物品，“较重”的物品（如金粒，造成 10 点伤害）比轻型物品（如物质球，造成 2 点伤害）造成更高的伤害。
每次发射会消耗基础 1600 AE 能量。

当配置选项“matterCannonBlockDamage”为 true 时，大炮会根据方块的硬度和弹药的伤害来破坏方块。

它的能量可以在<ItemLink id="charger" />中充能。

物质炮的工作方式类似于[存储元](storage_cells.md)，而且只需将物质炮放入 <ItemLink id="chest" /> 的存储元槽位中，就能最轻松地填充其弹药弹匣

## 升级

物质炮支持以下[升级](upgrade_cards.md)，通过 <ItemLink id="cell_workbench" /> 插入：

*   <ItemLink id="fuzzy_card" /> 可让存储元件按损伤值进行分区，并且/或者忽略物品 NBT
*   <ItemLink id="inverter_card" /> 可将过滤器从白名单切换为黑名单
*   <ItemLink id="speed_card" /> 会提高每次射击消耗的能量，使其发射时威力更大。
*   <ItemLink id="void_card" /> 会在元件已满时虚空销毁插入的物品。请务必先对其进行分区！
*   <ItemLink id="energy_card" />，以提高电池容量

## 配方

<RecipeFor id="matter_cannon" />