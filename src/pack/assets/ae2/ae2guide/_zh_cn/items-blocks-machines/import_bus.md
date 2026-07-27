---
navigation:
  parent: items-blocks-machines/items-blocks-machines-index.md
  title: ME输入总线
  icon: import_bus
  position: 220
categories:
- devices
item_ids:
- ae2:import_bus
---

# 输入总线

<GameScene zoom="8" background="transparent">
<ImportStructure src="../assets/blocks/import_bus.snbt" />
</GameScene>

导入总线会从它所接触的容器中拉取物品和流体（以及安装附属模组后支持的其他内容），并将它们推入
[网络存储](../ae2-mechanics/import-export-storage.md)。

为了减少卡顿，如果导入总线最近没有导入任何东西，它就会进入一种“睡眠模式”，以较慢的速度运行；当它成功导入某样东西时，就会被唤醒并加速到全速（每秒 4 次操作）。

它们是[线缆部件](../ae2-mechanics/cable-subparts.md)。

## 过滤

默认情况下，总线会导入它能够接触到的任何物品。将物品放入它的过滤槽后，这些物品将作为白名单，只允许导入这些特定物品。

即使你实际上并没有该物品，仍然可以从 JEI/REI 将物品和流体拖入槽位中。

使用流体容器（如桶或储罐）右击，即可将其中的流体设为过滤器，而不是将桶或储罐物品本身设为过滤器。

## 升级

输入总线支持以下[升级](upgrade_cards.md):

*   <ItemLink id="capacity_card" /> 会增加过滤槽位的数量
*   <ItemLink id="speed_card" /> 会增加每次操作移动的物品数量
*   <ItemLink id="fuzzy_card" /> 可让总线按耐久值筛选和/或忽略物品NBT
*   <ItemLink id="inverter_card" /> 可将过滤器从白名单切换为黑名单
*   <ItemLink id="redstone_card" /> 会添加红石控制，可设为在高电平信号、低电平信号时激活，或每次脉冲时激活一次

## 速度

| 加速卡 | 每次操作移动的物品数 |
|:-------------------|:--------------------------|
| 0                  | 1                         |
| 1                  | 8                         |
| 2                  | 32                        |
| 3                  | 64                        |
| 4                  | 96                        |

## 配方

<RecipeFor id="import_bus" />