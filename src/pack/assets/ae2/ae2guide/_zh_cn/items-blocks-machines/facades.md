---
navigation:
  parent: items-blocks-machines/items-blocks-machines-index.md
  title: 伪装块
  icon: facade
  icon_components:
    ae2:facade_item: minecraft:stone
  position: 110
categories:
- network infrastructure
item_ids:
- ae2:facade
---

# 伪装板

伪装板可用于让你的基地看起来更加整洁。它们可以覆盖两种尺寸的数据线，并且可以由许多
种方块制成。

<GameScene zoom="6" background="transparent">
  <ImportStructure src="../assets/assemblies/facades_1.snbt" />
  <IsometricCamera yaw="195" pitch="30" />
</GameScene>

它们可以覆盖数据线的所有侧面，但会让[subparts](../ae2-mechanics/cable-subparts.md)和数据线连接部分突出出来。

<GameScene zoom="6"  interactive={true}>
  <ImportStructure src="../assets/assemblies/facades_2.snbt" />
  <IsometricCamera yaw="195" pitch="30" />
</GameScene>

巧妙运用它们来提升你基地的美观度，或制作每一面都有不同材质的方块。

<GameScene zoom="4" interactive={true}>
  <ImportStructure src="../assets/assemblies/facades_3.snbt" />
  <IsometricCamera yaw="195" pitch="30" />
</GameScene>

## 隐藏伪装板

当任一只手持有 <a href="network_tool.md">网络工具</a> 时，伪装板将会被隐藏。

你可以直接与隐藏伪装板后的方块交互，而无需先移除伪装板。

## 配方

将你想要复制纹理的方块放在 4 个 <ItemLink id="cable_anchor" /> 的中间。

![Facade Recipe](../assets/diagrams/facade_recipe.png)