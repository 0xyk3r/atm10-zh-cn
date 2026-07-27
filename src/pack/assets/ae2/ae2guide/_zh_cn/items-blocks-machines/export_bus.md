---
navigation:
  parent: items-blocks-machines/items-blocks-machines-index.md
  title: ME输出总线
  icon: export_bus
  position: 220
categories:
- devices
item_ids:
- ae2:export_bus
---

# 输出总线

<GameScene zoom="8" background="transparent">
<ImportStructure src="../assets/blocks/export_bus.snbt" />
</GameScene>

输出总线会从[网络存储](../ae2-mechanics/import-export-storage.md)
中拉取物品和流体（以及在安装附加组件后提供的其他任何内容），并将它们推入它所接触的容器中。

为了减少卡顿，如果输出总线最近没有导出任何东西，它就会进入一种“睡眠模式”，以较慢的速度运行；而当它成功导出某样东西时，就会被唤醒并加速到全速（每秒 4 次操作）。

它们是[线缆部件](../ae2-mechanics/cable-subparts.md)。

## 过滤

默认情况下，该总线不会导出任何物品。插入其过滤槽中的物品将作为白名单，只允许导出这些特定物品。

即使你实际上并没有该物品，仍然可以从 JEI/REI 将物品和流体拖入槽位中。

使用流体容器（如桶或储罐）右击，即可将其中的流体设为过滤器，而不是将桶或储罐物品本身设为过滤器。

## 升级

输入总线支持以下[升级](upgrade_cards.md):

*   <ItemLink id="capacity_card" /> 会增加过滤槽位数量，并新增一个设置，用于决定按什么顺序输出已过滤的物品。
*   <ItemLink id="speed_card" /> 会增加每次操作移动的物品数量
*   <ItemLink id="fuzzy_card" /> 可让总线按耐久值筛选和/或忽略物品 NBT
*   <ItemLink id="crafting_card" /> 可让总线向你的[自动合成](../ae2-mechanics/autocrafting.md)
    系统发送合成请求，以获取它所需的物品。可以设置为在可能时从存储中拉取物品，或始终请求合成
    一个新的物品。
*   <ItemLink id="redstone_card" /> 会添加红石控制，可设置为在高信号、低信号时激活，或每次脉冲激活一次

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