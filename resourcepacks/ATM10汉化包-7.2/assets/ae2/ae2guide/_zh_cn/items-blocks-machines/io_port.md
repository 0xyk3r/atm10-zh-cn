---
navigation:
  parent: items-blocks-machines/items-blocks-machines-index.md
  title: ME-IO端口
  icon: io_port
  position: 210
categories:
- devices
item_ids:
- ae2:io_port
---

# ME-IO端口

<BlockImage id="io_port" p:powered="true" scale="8" />

IO端口可以让你快速将[存储单元](../items-blocks-machines/storage_cells.md)填满或清空到
[网络存储](../ae2-mechanics/import-export-storage.md)中。

它可以用<ItemLink id="certus_quartz_wrench" />旋转。

## 设置

*   可以将 IO端口设置为在电芯为空、已满或工作完成时，将电芯移至输出槽。
*   如果插入了 <ItemLink id="redstone_card" />，则会出现各种红石条件的选项
*   在 GUI 的中央，有一个箭头可用于设置物品传输的方向：从电芯到[网络存储](../ae2-mechanics/import-export-storage.md)，
    或从存储到电芯。

## 升级

IO端口支持以下[升级](upgrade_cards.md):

*   <ItemLink id="speed_card" /> 会增加每次操作移动的物品数量
*   <ItemLink id="redstone_card" /> 会添加红石控制，可在高信号、低信号或每次脉冲时激活

## 配方

<RecipeFor id="io_port" />