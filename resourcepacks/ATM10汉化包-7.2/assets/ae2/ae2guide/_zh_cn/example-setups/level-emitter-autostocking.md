---
navigation:
  parent: example-setups/example-setups-index.md
  title: 存储状态发信器自动补货
  icon: level_emitter
---

# 存储状态发信器自动补货

你可能会问：“我该如何让某种物品始终保持一定库存，并在需要时自动补充合成更多呢？”

一种解决方案是使用 <ItemLink id="export_bus" />、<ItemLink id="level_emitter" /> 和 <ItemLink id="crafting_card" />，从你的网络的[自动合成](../ae2-mechanics/autocrafting.md)中自动请求新物品。此设置用于维持单种物品的大量储备。

当然，你也可以省略等级发信器和红石卡，让你的网络持续进行合成。

<GameScene zoom="6" interactive={true}>
  <ImportStructure src="../assets/assemblies/level_emitter_autostocking.snbt" />

<BoxAnnotation color="#dddddd" min="1 1 0" max="2 1.3 1">
        (1) 输出总线：已过滤为所需物品。装有红石卡和合成卡。红石模式设置为
        "有信号时激活"，合成行为设置为"不使用已存储物品"。
        <Row><ItemImage id="redstone_card" scale="2" /> <ItemImage id="crafting_card" scale="2" /></Row>
  </BoxAnnotation>

<BoxAnnotation color="#dddddd" min="0.7 1 0" max="1 2 1">
        (2) 存量发信器：配置好所需的物品和数量，并设置为“当存量低于限制时发出信号”。
  </BoxAnnotation>

  <BoxAnnotation color="#dddddd" min="1 0 0" max="2 1 1">
        (3) 接口：使用默认配置。
  </BoxAnnotation>

<DiamondAnnotation pos="4 0.5 0.5" color="#00ff00">
        连接到主网络
    </DiamondAnnotation>

  <IsometricCamera yaw="195" pitch="30" />
</GameScene>

## 配置

* 将 <ItemLink id="export_bus" />（1）筛选为所需物品。它有一个 <ItemLink id="redstone_card" /> 和 <ItemLink id="crafting_card" />。
  “红石模式”设为“有信号时激活”，“合成行为”设为“不使用已储备的物品”。
* 将 <ItemLink id="level_emitter" />（2）配置为所需的物品和数量，并设为“当存量低于限制时发出信号”。
* <ItemLink id="interface" />（3）保持默认配置。

## 工作原理

1. 如果[存储网络](../ae2-mechanics/import-export-storage.md)中目标物品的数量低于 <ItemLink id="level_emitter" /> 中指定的数量，它就会发出红石信号。
2. 在收到红石信号后（并且由于 <ItemLink id="crafting_card" /> 且被设置为不使用库存物品），<ItemLink id="export_bus" /> 会请求该网络的[自动合成](../ae2-mechanics/autocrafting.md)制作更多目标物品，然后将其导出。
3. 当有物品被推入其中时（并且未被配置为在其内部容器中保留任何物品），<ItemLink id="interface" /> 会将该物品推入存储网络。