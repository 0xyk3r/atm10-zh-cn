---
navigation:
  parent: items-blocks-machines/items-blocks-machines-index.md
  title: ME箱子
  icon: chest
  position: 210
categories:
- devices
item_ids:
- ae2:chest
---

# ME箱子

<GameScene zoom="8" background="transparent">
<ImportStructure src="../assets/blocks/chest.snbt" />
</GameScene>

ME箱子的作用类似于一个微型网络，带有 <ItemLink id="terminal" />、<ItemLink id="drive" /> 和 <ItemLink id="energy_acceptor" />。
虽然它可以作为一个微型存储网络使用，但它只能容纳一个[存储元](../items-blocks-machines/storage_cells.md)，因此在这方面用途有限。

相反，它的作用在于与安装在其中的存储元进行交互。它的集成终端只能查看并访问已安装驱动器中的物品，而通用网络上的 [ME设备](../ae2-mechanics/devices.md) 则可以访问任何[网络存储](../ae2-mechanics/import-export-storage.md)中的物品，
包括 ME箱子。

它有 2 个不同的 GUI，并且在物品运输方面区分面。与顶部终端交互会打开集成终端。物品可以通过这一面插入已安装的存储单元，
但不能从中取出。与其他任意一面交互会打开带有存储单元插槽
和优先级设置的 GUI。只有带有存储单元插槽的那一面才能通过物品物流插入和移除该存储单元。

它可以用<ItemLink id="certus_quartz_wrench" />旋转。

它有一个小型 AE能量存储缓冲，因此如果未连接到带有[能量单元](../items-blocks-machines/energy_cells.md)的网络，
一次插入或提取过多物品可能会导致它掉电。

终端可以使用 <ItemLink id="color_applicator" /> 染色。

<GameScene zoom="6" background="transparent">
<ImportStructure src="../assets/assemblies/chest_color.snbt" />
<IsometricCamera yaw="195" pitch="30" />
</GameScene>

## 设置

ME箱子与 <ItemLink id="terminal" /> 或 <ItemLink id="crafting_terminal" /> 拥有完全相同的设置。
但是，它不支持 <ItemLink id="view_cell" />s。

## 存储元状态 LED

箱子中的存储元上有一个LED，可显示其状态：

| 颜色  | 状态 |
| :----- | :------------------------------------------------------------------------------- |
| 绿色  | 空 |
| 蓝色   | 有一些内容 |
| 橙色 | [类型已满](../ae2-mechanics/bytes-and-types.md)，无法添加新类型     |
| 红色    | [字节已满](../ae2-mechanics/bytes-and-types.md)，无法再插入物品 |
| 黑色  | 没有电力，或磁盘没有[channel](../ae2-mechanics/channels.md)                 |

## 优先级

可以通过点击单元槽 GUI 右上角的扳手来设置优先级。

进入网络的物品会首先以前往优先级最高的存储为目标。如果两个存储或单元拥有相同的优先级，而其中一个已经包含该物品，则会优先选择该存储而不是其他存储。任何 [已分区的](cell_workbench.md) 单元在与其他存储处于同一优先级组时，都会被视为已经包含该物品。从存储中取出物品时，将会从优先级最低的存储中移除。这个优先级系统意味着，当物品被插入和移出网络存储时，高优先级存储会被逐渐填满，而低优先级存储会被逐渐清空。

## 配方

<RecipeFor id="chest" />