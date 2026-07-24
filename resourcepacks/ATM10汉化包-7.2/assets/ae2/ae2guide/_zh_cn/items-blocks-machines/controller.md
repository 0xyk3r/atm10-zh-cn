---
navigation:
  parent: items-blocks-machines/items-blocks-machines-index.md
  title: 控制器
  icon: controller
  position: 110
categories:
- network infrastructure
item_ids:
- ae2:controller
---

# 控制器

<BlockImage id="controller" p:state="online" scale="8" />

控制器是[ME网络](../ae2-mechanics/me-network-connections.md)的路由枢纽。
没有它，网络就是“临时”状态，并且总共最多只能拥有 8 个使用频道的[ME设备](../ae2-mechanics/devices.md)。

一个[ME网络](../ae2-mechanics/me-network-connections.md)中不可能存在 2 个控制器。

控制器每个面提供 32 个[频道](../ae2-mechanics/channels.md)。

控制器每有一个方块控制器，运行时就需要消耗 6 AE/t。
每个方块控制器可存储 8000 AE，因此更大的网络可能需要额外的
能量存储。详见 [energy](../ae2-mechanics/energy.md)。

多方块结构控制器的搭建形式相当自由。

<GameScene zoom="2" background="transparent">
  <ImportStructure src="../assets/assemblies/controllers.snbt" />
  <IsometricCamera yaw="195" pitch="30" />
</GameScene>

不过，有几条规则必须遵守：

1.  [ME网络](../ae2-mechanics/me-network-connections.md)中的所有控制器方块都必须连接在一起；否则这些方块会变红。
2.  控制器的大小必须在 7x7x7 以内；否则它会变红。
3.  控制器最多只能在 1 个轴上拥有 2 个相邻方块；如果某个方块违反了这条规则，它就会被禁用并变红。

<GameScene zoom="2" background="transparent">
  <ImportStructure src="../assets/assemblies/controller_rules.snbt" />
  <IsometricCamera yaw="195" pitch="30" />
</GameScene>

只要遵循所有规则并接通电力，控制器就会发光并
循环变色。

你可以右键点击控制器，以打开与 <ItemLink id="network_tool" /> 相同的 GUI

## 配方

<RecipeFor id="controller" />