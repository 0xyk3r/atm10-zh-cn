---
navigation:
  parent: items-blocks-machines/items-blocks-machines-index.md
  title: 切换总线
  icon: toggle_bus
  position: 110
categories:
- network infrastructure
item_ids:
- ae2:toggle_bus
- ae2:inverted_toggle_bus
---

# 切换总线

<GameScene zoom="8" background="transparent">
<ImportStructure src="../assets/assemblies/toggle_bus.snbt" />
<IsometricCamera yaw="195" pitch="30" />
</GameScene>

一种功能与 <ItemLink id="fluix_glass_cable" /> 或其他线缆类似的总线，但它允许通过红石切换其连接状态。这样你就可以切断 [ME网络](../ae2-mechanics/me-network-connections.md) 的一部分。

当部件接收到红石信号时，会启用连接，而 <ItemLink id="inverted_toggle_bus" /> 则提供相反的行为，改为禁用连接。

值得注意的是，切换这些选项可能会导致网络重启，并重新计算已连接的设备。

它们是[线缆部件](../ae2-mechanics/cable-subparts.md)。

## 配方

<RecipeFor id="toggle_bus" />

<RecipeFor id="inverted_toggle_bus" />