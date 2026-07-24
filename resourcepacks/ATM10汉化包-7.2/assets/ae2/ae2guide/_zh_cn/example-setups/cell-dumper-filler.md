---
navigation:
  parent: example-setups/example-setups-index.md
  title: 存储元清空器或填充器
  icon: io_port
---

# 存储元清空器或填充器

有人可能会问：“我该如何快速将电芯中的物品清空到箱子、抽屉阵列或背包中，或者反过来，从它们中填充电芯呢？”

答案是使用一个 <ItemLink id="io_port" />，并配合一些子网划分，来限制它可以将物品放到哪里，或从哪里抽取物品。

<GameScene zoom="6" interactive={true}>
  <ImportStructure src="../assets/assemblies/cell_dumper_filler.snbt" />

<BoxAnnotation color="#dddddd" min="1 1 0" max="2 2 1">
        (1) IO 端口：可使用 GUI 中央的箭头按钮将其设置为“将数据传输到网络”或“将数据传输到存储元件”。
        内含 3 张加速卡。
        <ItemImage id="speed_card" scale="2" />
  </BoxAnnotation>

<BoxAnnotation color="#dddddd" min="0 0.7 0" max="1 1 1">
        (2) 存储总线：使用默认配置。
  </BoxAnnotation>

<BoxAnnotation color="#33dd33" min="0 1 0" max="1 2 1">
        将你想要填充或清空的东西放在这里。
  </BoxAnnotation>

<BoxAnnotation color="#dddddd" min="2 0.35 0.35" max="2.3 0.65 0.65">
        石英纤维：仅在能源来自另一个网络时才需要。
  </BoxAnnotation>

<DiamondAnnotation pos="3 0.5 0.5" color="#00ff00">
        连接到某种能量源，例如另一个网络或能源接收器。
    </DiamondAnnotation>

  <IsometricCamera yaw="195" pitch="30" />
</GameScene>

## 配置

* 可使用 GUI 中间的箭头按钮将 <ItemLink id="io_port" />（1）设置为“将数据传输到网络”或“将数据传输到存储元件”。它装有 3 张加速卡，以达到最大速度。
* <ItemLink id="storage_bus" />（2）处于默认配置。

## 工作原理

### 在“传输到网络”模式下

1. <ItemLink id="io_port" /> 会尝试将插入的[存储元](../items-blocks-machines/storage_cells.md).
    中的内容转存到[网络存储](../ae2-mechanics/import-export-storage.md).
2. 子网中唯一的存储设备是 <ItemLink id="storage_bus" />，它会存储你放在其前方的物品、流体等内容。
* <ItemLink id="energy_cell" /> 提供了足够大的[能量](../ae2-mechanics/energy.md)缓冲，使网络不会因每游戏刻传输如此多物品的耗电而断电。

### 在“传输到存储元”模式下

1. <ItemLink id="io_port" /> 会尝试将[网络存储](../ae2-mechanics/import-export-storage.md)中的内容转储到插入的[存储元](../items-blocks-machines/storage_cells.md)中。
2. 该子网中唯一的存储设备是 <ItemLink id="storage_bus" />，它会把你放在它前方的物品、流体等从中抽取出来。
* <ItemLink id="energy_cell" /> 提供了足够大的[能量](../ae2-mechanics/energy.md)缓冲，使网络不会因每游戏刻传输如此大量的物品而耗尽电力。