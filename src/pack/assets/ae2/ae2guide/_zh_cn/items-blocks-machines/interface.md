---
navigation:
  parent: items-blocks-machines/items-blocks-machines-index.md
  title: 接口
  icon: interface
  position: 210
categories:
- devices
item_ids:
- ae2:interface
- ae2:cable_interface
---

# 接口

<Row gap="20">
<BlockImage id="interface" scale="8" />
<GameScene zoom="8" background="transparent">
  <ImportStructure src="../assets/blocks/cable_interface.snbt" />
</GameScene>
</Row>

接口的作用类似于一个小箱子和储罐，会根据你在其槽位中设置要保持库存的物品，从[network storage](../ae2-mechanics/import-export-storage.md)中自动填充或向其中排出内容。它会尝试在单个游戏刻内完成这一过程，因此每个游戏刻最多可向自身填充或从自身排出 9 组物品，如果你有高速的物品管道，这会是一种快速导入或导出的方法。

另一个实用特性是：虽然大多数流体储罐只能储存 1 种流体，但接口最多可以储存 9 种流体，以及物品。

它们本质上就是带有一些额外功能的箱子/多流体储罐，而只要让它们不连接到任何网络，
你就可以阻止这些额外功能生效。

因此，在某些你想少量存放许多不同物品的特殊情况下，它们会很有用。

## 接口在内部是如何工作的

如前所述，接口本质上就是一个箱子/储罐，附带一些超级厉害的 <ItemLink id="import_bus" /> 和 <ItemLink id="export_bus" />，以及一大堆 <ItemLink id="level_emitter" />。

<GameScene zoom="3" interactive={true}>
  <ImportStructure src="../assets/assemblies/interface_internals.snbt" />

<BoxAnnotation color="#dddddd" min="1.3 0.3 1.3" max="9.7 1 1.7">
        一组用于控制所请求库存数量的等级发信器
        <GameScene zoom="4" background="transparent">
        <ImportStructure src="../assets/blocks/level_emitter.snbt" />
        </GameScene>
  </BoxAnnotation>

<BoxAnnotation color="#dddddd" min="1.3 4 1.3" max="9.7 4.7 1.7">
        一组用于控制所请求库存数量的等级发信器
        <GameScene zoom="4" background="transparent">
        <ImportStructure src="../assets/blocks/level_emitter.snbt" />
        </GameScene>
  </BoxAnnotation>

<BoxAnnotation color="#dddddd" min="1.3 1.3 1.3" max="9.7 2 1.7">
        一堆超级无敌的输入总线，每游戏刻可传输 1 组物品
        <GameScene zoom="4" background="transparent">
        <ImportStructure src="../assets/blocks/import_bus.snbt" />
        </GameScene>
  </BoxAnnotation>

<BoxAnnotation color="#dddddd" min="1.3 3 1.3" max="9.7 3.7 1.7">
        一堆超级无敌的输出总线，每游戏刻可传输 1 组物品
        <GameScene zoom="4" background="transparent">
        <ImportStructure src="../assets/blocks/export_bus.snbt" />
        </GameScene>
  </BoxAnnotation>

  <BoxAnnotation color="#dddddd" min="1 2 1" max="10 3 2">
        9个独立的内部槽位
  </BoxAnnotation>

  <IsometricCamera yaw="195" pitch="15" />
</GameScene>

## 特殊交互

接口还具备一些与其他 AE2 [设备](../ae2-mechanics/devices.md) 交互的特殊功能：

将 <ItemLink id="storage_bus" /> 放在未配置的接口上时，会将其网络中的全部[网络存储](../ae2-mechanics/import-export-storage.md)
提供给存储总线所在的网络，就好像接口的网络是一个巨型箱子，而存储总线就放在这个箱子上一样。
在接口的过滤槽中设置要库存的物品后，此功能将被禁用。

<GameScene zoom="6" interactive={true}>
  <ImportStructure src="../assets/assemblies/interface_storage.snbt" />
  <IsometricCamera yaw="195" pitch="30" />
</GameScene>

样板供应器与[subnets](../ae2-mechanics/subnetworks.md)上的接口有一种特殊的交互方式：如果该接口未配置，
供应器将完全跳过该接口，并直接推送到该子网的[storage](../ae2-mechanics/import-export-storage.md)中，
跳过接口且不会用配方批次将其填满，更重要的是，在存储中有空间之前，不会插入下一批。

<GameScene zoom="6" background="transparent">
<ImportStructure src="../assets/assemblies/provider_interface_storage.snbt" />

<BoxAnnotation color="#dddddd" min="2.7 0 1" max="3 1 2">
        接口（必须是平的，不能是完整方块）
  </BoxAnnotation>

<BoxAnnotation color="#dddddd" min="1 0 0" max="1.3 1 4">
        存储总线
  </BoxAnnotation>

<BoxAnnotation color="#dddddd" min="0 0 0" max="1 1 4">
        你想要进行样板供应的位置（多台机器，或 1 台机器的多个面）
  </BoxAnnotation>

<IsometricCamera yaw="185" pitch="30" />
</GameScene>

## 变种

接口有 2 种不同的变体：普通和平面/[subpart](../ae2-mechanics/cable-subparts.md)。这会影响它们的容器可从哪些特定侧面访问，以及它们会向哪些侧面提供网络连接。

*   普通网络接口允许其他设备从任意一侧向其插入、从中抽取，并访问其容器；并且像大多数应用能源机器一样，会像数据线一样向所有侧面提供网络连接。

*   平面接口是[线缆子部件](../ae2-mechanics/cable-subparts.md)，因此可在同一根线缆上放置多个，从而实现紧凑的布局。
    它们允许从其正面向容器中推入、从容器中拉出，以及访问其容器，但不会在其正面提供网络连接。

接口可以在合成网格中于普通与扁平两种形态之间切换。

## 设置

界面上方的槽位决定了该界面会在自身内部储备什么物品。当有物品被放入这些槽位，或从 JEI/REI 中拖入时，会出现一个扳手，让你设置数量。

使用流体容器（如桶或储罐）右击，即可将其中的流体设为过滤器，而不是将桶或储罐物品本身设为过滤器。

当你将某个槽位设置为补货模式时，它还会阻止外部机器向该槽位插入任何其他物品。

## 升级

接口支持以下[升级](upgrade_cards.md):

*   <ItemLink id="fuzzy_card" /> 可让总线按损伤值筛选和/或忽略物品 NBT
*   <ItemLink id="crafting_card" /> 可让接口向你的[自动合成](../ae2-mechanics/autocrafting.md)
    系统发送合成请求，以获取它所需的物品。如果可能，它会先从存储中提取物品，然后再请求合成新物品

## 优先级

可以通过点击 GUI 右上角的扳手来设置优先级。优先级较高的接口会比优先级较低的接口更先获得其物品，

## 配方

<Recipe id="network/blocks/interfaces_interface" />

<RecipeFor id="cable_interface" />