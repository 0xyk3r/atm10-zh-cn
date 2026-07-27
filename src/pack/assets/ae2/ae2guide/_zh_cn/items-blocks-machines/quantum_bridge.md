---
navigation:
  parent: items-blocks-machines/items-blocks-machines-index.md
  title: 量子环
  icon: quantum_ring
  position: 110
categories:
- network infrastructure
item_ids:
- ae2:quantum_link
- ae2:quantum_ring
---

# 量子网络桥

![已成形的量子网络桥](../assets/diagrams/quantum_bridge_demonstration.png)

量子环可以将 [网络](../ae2-mechanics/me-network-connections.md) 延伸到无限远的距离，甚至跨维度。
它们总共可以承载 32 个频道（无论线缆如何连接到各个面），本质上
就像一根无线的 [致密线缆](cables.md#dense-cable)。

<GameScene zoom="4" background="transparent">
  <ImportStructure src="../assets/assemblies/quantum_bridge_internal_structure_1.snbt" />
  <IsometricCamera yaw="195" pitch="30" />
</GameScene>

<GameScene zoom="4" background="transparent">
  <ImportStructure src="../assets/assemblies/quantum_bridge_internal_structure_2.snbt" />

  <BoxAnnotation color="#33dd33" min="1 1 1" max="6 2 3">
        两个端点之间的一根假想线缆
  </BoxAnnotation>

  <IsometricCamera yaw="195" pitch="30" />
</GameScene>

需要注意的是，**两侧都必须进行区块加载**，因此如果两侧相距较远，就必须使用 <ItemLink id="spatial_anchor" /> 或其他区块加载机。

# 量子之环

<BlockImage id="quantum_ring" scale="8" />

将这 8 个方块围绕 <ItemLink id="quantum_link" /> 放置即可创建一个量子环。
只有与 <ItemLink id="quantum_link" /> 相邻的 4 个 <ItemLink id="quantum_ring" /> 方块会接受网络连接，
4 个角落方块无法连接线缆。

## 配方

<RecipeFor id="quantum_ring" />

# 量子链接室

<BlockImage id="quantum_link" scale="8" />

这些方块中的任意一个被 <ItemLink id="quantum_ring" /> 包围时，
就会形成一个量子环。该方块不会连接到任何线缆，只有在整个量子环完整建成后，
才会被识别为网络的一部分。

这个方块的容器只能容纳单个 <ItemLink id="quantum_entangled_singularity" />，并且
可被自动化访问。

## 配方

<RecipeFor id="quantum_link" />