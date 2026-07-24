---
navigation:
  parent: items-blocks-machines/items-blocks-machines-index.md
  title: 谐振仓
  icon: vibration_chamber
  position: 110
categories:
- network infrastructure
item_ids:
- ae2:vibration_chamber
---

# 谐振仓

<BlockImage id="vibration_chamber" p:active="true" scale="8" />

虽然为你的网络提供[能量](../ae2-mechanics/energy.md)的主要预期方式是使用 <ItemLink id="energy_acceptor" />，但振动仓也可以直接产生少量到中等数量的 AE。

默认情况下（无[升级](upgrade_cards.md)且配置为默认）它会产生 40 AE/t。

当网络的[energy](../ae2-mechanics/energy.md)存储已满时，谐振仓会降低功率以节省燃料，但无法完全关闭。

## 设置

*   谐振仓可访问全局设置，以 AE 或 E/FE 显示能量。

## 升级

谐振仓支持以下[升级](upgrade_cards.md):

*   <ItemLink id="energy_card" /> 可使该腔室的效率提高 +50%，最高可提高至 +150%，即达到基础效率的 250%。
*   <ItemLink id="speed_card" /> 可使该腔室的燃烧速率提高 +50%，最高可提高至 +150%，即达到基础输出功率的 250%。

## 配置

谐振仓的属性可以在你的 .minecraft\
目录中的 config 文件夹下的 ae2 文件夹里的 common.json 中进行编辑。

*   baseEnergyPerFuelTick 用于设置谐振仓未升级时的基础效率。
*   minEnergyPerGameTick 用于设置最低可能的能量产出（即使网络
    不需要能量，谐振仓也始终会缓慢消耗一些燃料）。
*   maxEnergyPerGameTick 用于设置谐振仓未升级时的最大输出（以及速度）。

## 配方

<RecipeFor id="vibration_chamber" />