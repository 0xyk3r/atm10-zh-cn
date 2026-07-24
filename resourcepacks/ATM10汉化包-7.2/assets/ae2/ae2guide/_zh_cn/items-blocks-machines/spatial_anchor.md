---
navigation:
  parent: items-blocks-machines/items-blocks-machines-index.md
  title: 空间锚
  icon: spatial_anchor
  position: 110
categories:
- network infrastructure
item_ids:
- ae2:spatial_anchor
---

# 空间锚

<BlockImage id="spatial_anchor" p:powered="true" scale="8"/>

AE2网络需要保持区块加载，其任意[设备](../ae2-mechanics/devices.md)才能正常运作；如果只有部分区域被加载，
它可能无法正确运行。空间锚可以解决这个问题。它会强制加载其网络所占据的区块。
只需一根线缆跨过区块边界，就足以加载那个新区块。

它会通过[量子桥](quantum_bridge.md)传播其“加载”，但不会跨维度传播，所以如果你
有一座通往下界的量子桥，你就需要在基地中的网络和下界中的网络上各放置一个空间锚。

默认情况下，它还会在其加载的区块中启用随机刻，这可以在 ae2 配置中关闭。

如果你出于某些原因想这么做，可以用 <ItemLink id="certus_quartz_wrench" /> 旋转它。

## 设置

*   空间锚可访问全局设置，以便选择用 AE 或 E/FE 显示能量。
*   可以显示一个世界中的全息图，用于展示正在被加载的区块。

## 能量

空间锚将根据这个公式消耗[能量](../ae2-mechanics/energy.md)：

e = 80 + (x\*(x+1))/2

其中 x 为已加载区块的数量

## 配方

<RecipeFor id="spatial_anchor" />