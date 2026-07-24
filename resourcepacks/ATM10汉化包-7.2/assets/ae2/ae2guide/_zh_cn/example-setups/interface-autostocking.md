---
navigation:
  parent: example-setups/example-setups-index.md
  title: 接口自动补货
  icon: interface
---

# 接口自动补货

你可能会问：“我该如何让各种物品始终保持一定库存，并在需要时自动补充合成更多呢？”

一种解决方案是使用 <ItemLink id="interface" /> 和 <ItemLink id="crafting_card" />，通过你网络的[自动合成](../ae2-mechanics/autocrafting.md)自动请求新物品。这种配置更适合维持多种物品的小批量库存。

这个演示布局做得较短，以免过宽；最理想的做法可能是使用 4 个 <ItemLink id="interface" /> 和 4 个 <ItemLink id="storage_bus" />，
以便在常规的 [cable](../items-blocks-machines/cables.md) 中用满全部 8 个 [channels](../ae2-mechanics/channels.md)。

<GameScene zoom="6" interactive={true}>
  <ImportStructure src="../assets/assemblies/interface_autostocking.snbt" />

<BoxAnnotation color="#dddddd" min="0 0 0" max="2 1 1">
        (1) 接口：设置为将所需物品保留在自身内部。它们带有合成卡。
        <ItemImage id="crafting_card" scale="2" />
  </BoxAnnotation>

<BoxAnnotation color="#dddddd" min="0 1 0" max="2 1.3 1">
        （2）存储总线：“输入/输出模式”设置为“仅提取”。
  </BoxAnnotation>

<DiamondAnnotation pos="4 0.5 0.5" color="#00ff00">
        连接到主网络
    </DiamondAnnotation>

  <IsometricCamera yaw="195" pitch="30" />
</GameScene>

## 配置

* 将 <ItemLink id="interface" />（1）设置为让其自身保留所需物品：点击将目标物品放入其
   顶部槽位，或从 JEI 拖入顶部槽位，然后点击槽位上方的扳手图标来设置数量。它们带有 <ItemLink id="crafting_card" />。
* 将 <ItemLink id="storage_bus" />（2）设置为“输入/输出模式”为“仅提取”。

## 工作原理

1. 如果某个 <ItemLink id="interface" /> 无法从[网络存储](../ae2-mechanics/import-export-storage.md)中取回足够数量的已配置物品，
   （且它有一个 <ItemLink id="crafting_card" />），它就会请求网络的[自动合成](../ae2-mechanics/autocrafting.md)来合成更多该物品。
2. <ItemLink id="storage_bus" />可让网络访问接口中的内容。