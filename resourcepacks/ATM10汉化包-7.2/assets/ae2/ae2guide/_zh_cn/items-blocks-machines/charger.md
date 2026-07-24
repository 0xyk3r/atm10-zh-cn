---
navigation:
  parent: items-blocks-machines/items-blocks-machines-index.md
  title: 充电器
  icon: charger
  position: 310
categories:
- machines
item_ids:
- ae2:charger
---

# 充电器

<BlockImage id="charger" scale="8" />

充电器可用于给
受支持的工具和 <ItemLink id="certus_quartz_crystal" /> 充能。

可通过顶部或底部供能，既可以使用 AE2 的[线缆](cables.md)，也可以使用其他模组的能量线缆。它既可以接受 AE2 的能量（AE），也可以接受 Forge Energy（FE）。物品可从任意一侧插入或取出。只有产物可以被取出，因此无需使用过滤器来防止取出赛特斯石英水晶而不是带电赛特斯石英水晶。可使用 <ItemLink id="certus_quartz_wrench" /> 对其进行旋转，以便于自动化。

可用于由 <ItemLink id="certus_quartz_crystal" /> 制成 <ItemLink id="charged_certus_quartz_crystal" />，以及由 <ItemLink id="minecraft:compass" /> 制成 <ItemLink id="meteorite_compass" />。

要手动为其供能，请在顶部或底部放置一个 <ItemLink id="crank" />，然后不断右键，直到物品充满电。

它同时也是 [福鲁伊克斯研究员](fluix_researcher.md) 的工作站。

## 简易自动化

例如，可旋转性让你可以像这样半自动化充能器：

<GameScene zoom="4" background="transparent">
  <ImportStructure src="../assets/assemblies/charger_hopper.snbt" />
  <IsometricCamera yaw="195" pitch="30" />
</GameScene>

## 配方

<RecipeFor id="charger" />