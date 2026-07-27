---
navigation:
  parent: items-blocks-machines/items-blocks-machines-index.md
  title: 等级发射器
  icon: level_emitter
  position: 220
categories:
- devices
item_ids:
- ae2:level_emitter
- ae2:energy_level_emitter
---

# 存储状态发信器

<GameScene zoom="8" background="transparent">
  <ImportStructure src="../assets/blocks/level_emitter.snbt" />
</GameScene>

存储状态发信器会根据[存储网络](../ae2-mechanics/import-export-storage.md)中某种物品的数量发出红石信号。

还有一个版本，会根据你的网络中存储的[能量](../ae2-mechanics/energy.md)发出红石信号。

即使你实际上并没有任何对应的物品或流体，也可以从 JEI/REI 将物品和流体拖入该槽位。

使用流体容器（如桶或储罐）右击，即可将其中的流体设为过滤器，而不是将桶或储罐物品本身设为过滤器。

它们是[线缆部件](../ae2-mechanics/cable-subparts.md)。

与其他[设备](../ae2-mechanics/devices.md)不同，存储状态发信器*不*需要[频道](../ae2-mechanics/channels.md)。

## 设置

*   存储状态发信器可设置为“大于等于”或“小于”模式
*   插入 <ItemLink id="crafting_card" /> 后，它可设置为“在物品合成期间发出红石信号”或
    “发出红石信号以合成物品”

## 升级

电平发射器支持以下[升级](upgrade_cards.md):

*   <ItemLink id="fuzzy_card" /> 允许发射端按耐久值筛选和/或忽略物品NBT
*   <ItemLink id="crafting_card" /> 启用合成功能

## 合成功能

如果插入了 <ItemLink id="crafting_card" />，发射器将切换到合成模式。

这会启用两个选项：

第一个选项“在物品合成时发出红石信号”会让发射器在你的[自动合成](../ae2-mechanics/autocrafting.md)
通过 <ItemLink id="pattern_provider" /> 合成某个特定物品时发出红石信号。这样就能只在实际使用时
启用特定的高耗能自动化装置。

第二个选项“发出红石以合成物品”在某些特定场景下极其有用，例如无限农场以及
那种只有概率产出、而非保证产出的自动化装置。
这个设置会为自动合成](../ae2-mechanics/autocrafting.md)创建一个虚拟的[样板](patterns.md)，供其使用，
对应发射器筛选槽中的任意物品。
（为了正确运作，你的 <ItemLink id="pattern_provider" /> 中**不应存在**同一物品的真实样板）

这种“样板”并不定义，甚至根本不关心材料。

它表达的只有一件事：“如果你让这个等级发信器发出红石信号，那么 ME 系统将在不久或遥远的将来某个时刻收到这个物品。” 这通常用于启用或停用不需要输入材料的无限农场，或者用于启用[处理循环配方的系统](../example-setups/recursive-crafting-setup.md)（这是标准自动合成无法理解的），例如，如果你有一台能复制圆石的机器，那么“1 个圆石 = 2 个圆石”。

## 配方

<RecipeFor id="level_emitter" />

<RecipeFor id="energy_level_emitter" />