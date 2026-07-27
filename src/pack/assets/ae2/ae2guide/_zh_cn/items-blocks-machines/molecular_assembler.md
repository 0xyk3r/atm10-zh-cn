---
navigation:
  parent: items-blocks-machines/items-blocks-machines-index.md
  title: 分子装配室
  icon: molecular_assembler
  position: 310
categories:
- machines
item_ids:
- ae2:molecular_assembler
---

# 分子装配室

<BlockImage id="molecular_assembler" scale="8" />

分子装配室会接收输入到其中的物品，并执行由相邻的 <ItemLink id="pattern_provider" />
或插入的 <ItemLink id="crafting_pattern" />、<ItemLink id="smithing_table_pattern" /> 或 <ItemLink id="stonecutting_pattern" /> 所定义的操作，
然后将结果推送到相邻的容器中。

这台组装机内放有一张指定了 1 个橡木原木 = 4 个橡木木板配方的合成样板。当橡木原木被送入上方的漏斗时，
组装机会进行合成，并将橡木木板弹出到下方的漏斗中。

<GameScene zoom="6" background="transparent">
  <ImportStructure src="../assets/assemblies/standalone_assembler.snbt" />
  <IsometricCamera yaw="195" pitch="30" />
</GameScene>

## 分子装配室的主要用途

不过，它们的主要用途是在 <ItemLink id="pattern_provider" /> 旁边使用。在这种情况下，样板供应器会表现出特殊行为，
会将相关样板的信息连同材料一起发送给相邻的组装机。由于组装机会自动将
合成产物弹出到相邻的容器中（也就是样板供应器的返回槽位中），因此，在样板供应器旁放置一台组装机
就是实现合成样板自动化所需的全部配置。

<GameScene zoom="4" background="transparent">
  <ImportStructure src="../assets/assemblies/assembler_tower.snbt" />
  <IsometricCamera yaw="195" pitch="30" />
</GameScene>

## 升级

分子装配室支持以下[升级](upgrade_cards.md):

*   <ItemLink id="speed_card" />

## 配方

<RecipeFor id="molecular_assembler" />

## 说明

Optifine 会破坏“将物品输出至附近的容器中”的功能，因此大多数组装机自动化合成方案都无法工作。