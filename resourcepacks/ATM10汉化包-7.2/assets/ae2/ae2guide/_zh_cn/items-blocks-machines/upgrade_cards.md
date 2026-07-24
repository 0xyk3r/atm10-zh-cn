---
navigation:
  parent: items-blocks-machines/items-blocks-machines-index.md
  title: 升级卡
  icon: speed_card
  position: 410
categories:
- tools
item_ids:
- ae2:basic_card
- ae2:advanced_card
- ae2:redstone_card
- ae2:capacity_card
- ae2:void_card
- ae2:fuzzy_card
- ae2:speed_card
- ae2:inverter_card
- ae2:crafting_card
- ae2:equal_distribution_card
- ae2:energy_card
---

# 升级卡

<Row>
  <ItemImage id="redstone_card" scale="2" />

  <ItemImage id="capacity_card" scale="2" />

  <ItemImage id="void_card" scale="2" />

  <ItemImage id="fuzzy_card" scale="2" />

  <ItemImage id="speed_card" scale="2" />

  <ItemImage id="inverter_card" scale="2" />

  <ItemImage id="crafting_card" scale="2" />

  <ItemImage id="equal_distribution_card" scale="2" />

  <ItemImage id="energy_card" scale="2" />
</Row>

升级卡会改变应用能源 [ME设备](../ae2-mechanics/devices.md) 和机器的行为，提高它们的速度、改善其筛选容量、启用红石控制等。

## 卡片组件

<Row>
  <ItemImage id="basic_card" scale="2" />

  <ItemImage id="advanced_card" scale="2" />
</Row>

卡片由基础或高级卡片基底制作而成

<Row>
  <RecipeFor id="basic_card" />

  <RecipeFor id="advanced_card" />
</Row>

## 红石卡

<ItemImage id="redstone_card" scale="2" />

红石卡会添加红石控制，在设备界面中加入一个切换按钮，用于在各种红石条件判断之间切换。

<RecipeFor id="redstone_card" />

## 容量卡

<ItemImage id="capacity_card" scale="2" />

容量卡可增加输入总线、输出总线、存储总线和成型面板中的过滤槽数量。

<RecipeFor id="capacity_card" />

## 溢出销毁卡

<ItemImage id="void_card" scale="2" />

溢出销毁卡可应用于 <ItemLink id="cell_workbench" /> 中的[存储元](storage_cells.md)，
并会在存储元已满时删除输入的物品。（请务必先对你的存储元进行[分区](cell_workbench.md)！）与均分卡配合使用时，如果该物品在存储元中对应的分区已满，物品就会被清除，即使其他物品的分区仍是空的。

<RecipeFor id="void_card" />

## 模糊卡

<ItemImage id="fuzzy_card" scale="2" />

模糊卡可让带有过滤名单的 ME设备 和工具按耐久损耗程度进行过滤和/或忽略物品NBT，从而让你可以导出所有铁斧，无论其已消耗耐久和附魔如何；或者只导出受损的钻石剑，而不导出那些已完全修复的。

下面是一个关于模糊耐久比较强化如何工作的示例：左侧是总线配置，上方是被比较的物品。

| 25%                    | 10%受损的镐 | 30%受损的镐 | 80%受损的镐 | 完全修复的镐 |
| ---------------------- | ----------- | ----------- | ----------- | ------------ |
| 濒临损坏的镐           | ✅          | \*\*\*\*    | \*\*\*\*    | \*\*\*\*     |
| 完全修复的镐           | \*\*\*\*    | ✅          | ✅          | ✅           |

| 50%                    | 10% 损坏的镐 | 30% 损坏的镐 | 80% 损坏的镐 | 完全修复的镐 |
| ---------------------- | ------------------- | ------------------- | ------------------- | ------------------- |
| 濒临损坏的镐  | ✅                   | ✅                   | \*\*\*\*            | \*\*\*\*            |
| 完全修复的镐 | \*\*\*\*            | \*\*\*\*            | ✅                   | ✅                   |

| 75%                    | 10% 损坏的镐 | 30% 损坏的镐 | 80% 损坏的镐 | 完全修复的镐 |
| ---------------------- | ------------ | ------------ | ------------ | ------------ |
| 近乎损坏的镐           | ✅            | ✅            | \*\*\*\*     | \*\*\*\*     |
| 完全修复的镐           | \*\*\*\*     |              | ✅            | ✅            |

| 99%                    | 损坏了 10% 的镐 | 损坏了 30% 的镐 | 损坏了 80% 的镐 | 完全修复的镐 |
| ---------------------- | ---------------- | ---------------- | ---------------- | ------------ |
| 几乎损坏的镐           | ✅                | ✅                | ✅                | \*\*\*\*     |
| 完全修复的镐           | \*\*\*\*         | \*\*\*\*         | \*\*\*\*         | ✅           |

| 忽略 | 10% 损坏的镐 | 30% 损坏的镐 | 80% 损坏的镐 | 完全修复的镐 |
| ---------------------- | ------------------- | ------------------- | ------------------- | ------------------- |
| 几乎损坏的镐 | ✅ | ✅ | ✅ | **✅** |
| 完全修复的镐 | **✅** | **✅** | **✅** | ✅ |

<RecipeFor id="fuzzy_card" />

## 加速卡

<ItemImage id="speed_card" scale="2" />

加速卡能让各种设备运转得更快，使输入/输出总线每次操作搬运更多物品，也让压印器
和组装机工作得更快。

<RecipeFor id="speed_card" />

## 反相卡

<ItemImage id="inverter_card" scale="2" />

反相卡会将设备和工具中的过滤模式从白名单切换为黑名单。

<RecipeFor id="inverter_card" />

## 合成卡

<ItemImage id="crafting_card" scale="2" />

合成卡片可让设备向你的[自动合成](../ae2-mechanics/autocrafting.md)
系统发送合成请求，以获取它所需的物品。

<RecipeFor id="crafting_card" />

## 均分卡

<ItemImage id="equal_distribution_card" scale="2" />

均分卡可应用于 <ItemLink id="cell_workbench" /> 中的[存储单元](storage_cells.md)，并根据该卡[分区至](cell_workbench.md)的内容，将存储单元划分为大小相等的区域。这样可以防止某一种物品完全填满整个存储单元。

<RecipeFor id="equal_distribution_card" />

## 能量卡

<ItemImage id="energy_card" scale="2" />

能量卡可为某些工具提供更多能量存储，例如便携式存储终端，并让 <ItemLink id="vibration_chamber" /> 更高效。

<RecipeFor id="energy_card" />