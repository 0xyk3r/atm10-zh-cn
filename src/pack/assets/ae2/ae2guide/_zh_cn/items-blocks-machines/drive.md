---
navigation:
  parent: items-blocks-machines/items-blocks-machines-index.md
  title: ME驱动器
  icon: drive
  position: 210
categories:
- devices
item_ids:
- ae2:drive
---

# ME驱动器

<GameScene zoom="8" background="transparent">
  <ImportStructure src="../assets/blocks/drive.snbt" />
</GameScene>

驱动器是你将 [存储元](storage_cells.md) 插入其中以用于
[网络存储](../ae2-mechanics/import-export-storage.md) 的[设备](../ae2-mechanics/devices.md)。它有 10 个槽位，每个都可放入一个存储元。

如果你出于某种原因想这么做，也可以使用漏斗或 ae2 总线等任意物品物流方式从它的容器中插入或取出这些元件。

它可以用<ItemLink id="certus_quartz_wrench" />旋转。

## 存储元状态 LED

驱动器中的存储元上有一个LED，可显示其状态：

| 颜色  | 状态 |
| :----- | :------------------------------------------------------------------------------- |
| 绿色  | 空 |
| 蓝色   | 有一些内容 |
| 橙色 | [类型已满](../ae2-mechanics/bytes-and-types.md)，无法添加新类型     |
| 红色    | [字节已满](../ae2-mechanics/bytes-and-types.md)，无法再插入物品 |
| 黑色  | 没有电力，或磁盘没有[channel](../ae2-mechanics/channels.md)                 |

## 优先级

可以通过点击 GUI 右上角的扳手来设置优先级。

进入网络的物品会先将优先级最高的存储作为它们的首个目标。如果两个存储设备或电芯拥有相同的优先级，而其中一个已经包含该物品，则会优先选择那个存储，而不是其他存储。任何[已分区](cell_workbench.md)电芯在与其他存储处于同一优先级组时，都会被视为已经包含该物品。

从存储中取出物品时，会优先从优先级最低的存储中移除。这个优先级系统意味着，随着物品被插入网络存储并从中移除，高优先级存储会被逐渐填满，而低优先级存储会被逐渐清空。

## 配方

<RecipeFor id="drive" />