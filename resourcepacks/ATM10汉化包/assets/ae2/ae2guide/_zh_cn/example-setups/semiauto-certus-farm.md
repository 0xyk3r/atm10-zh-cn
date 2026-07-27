---
navigation:
  parent: example-setups/example-setups-index.md
  title: 半自动赛特斯农场
  icon: certus_quartz_crystal
  position: 115
---

# 半自动赛特斯农场

遗憾的是，[简易赛特斯农场](simple-certus-farm.md)需要一个 <ItemLink id="flawless_budding_quartz" /> 才能完全自动运行。
这就需要使用[空间IO](../ae2-mechanics/spatial-io.md)，或者将农场建在[陨石](../ae2-mechanics/meteorites.md)处。

不过，应用能源可以放置和破坏方块，所以也许
可以让你的农场*帮你自动更换赛特斯石英母岩*。（你需要定期将一些
<ItemLink id="flawed_budding_quartz" /> 放入输入桶中，并从用尽的
赛特斯石英母岩桶中取出 <ItemLink id="quartz_block" />）

若要完全自动化地完成此操作，请参见[高级赛特斯农场](advanced-certus-farm.md)。

这个农场比[简单赛特斯农场](simple-certus-farm.md)要复杂一些，因为它实际上是由
3个独立的装置硬塞在一起组成的。

速度估算请参见 [赛特斯生长](../ae2-mechanics/certus-growth.md)。

**这是一个复杂的搭建结构，有些部分藏在其他部分后面，请拖动视角从各个角度查看**

<GameScene zoom="6" interactive={true}>
  <ImportStructure src="../assets/assemblies/semiauto_certus_farm.snbt" />

<BoxAnnotation color="#ddaaaa" min="3.7 2 1" max="4 3 2">
        (1) 破坏面板 #1：没有可配置的 GUI，但可以附魔时运。
  </BoxAnnotation>

  <BoxAnnotation color="#ddaaaa" min="2 2 1" max="2.3 3 2">
        (2) 存储总线 #1：过滤为赛特斯石英水晶。
        <ItemImage id="certus_quartz_crystal" scale="2" />
  </BoxAnnotation>

  <DiamondAnnotation pos="3 2.5 1.5" color="#ff0000">
    晶簇破坏器子网络
  </DiamondAnnotation>

  <BoxAnnotation color="#aaddaa" min="3.7 1 1" max="4 2 2">
        (3) ME破坏面板 #2：无可配置的 GUI，但附有精准采集魔咒。
  </BoxAnnotation>

  <BoxAnnotation color="#aaddaa" min="2 1 1" max="2.3 2 2">
        (4) 存储总线 #2：过滤为赛特斯石英方块。
        <BlockImage id="quartz_block" scale="2" />
  </BoxAnnotation>

  <DiamondAnnotation pos="3 1.5 1.5" color="#00ff00">
    赛特斯方块破坏器子网络
  </DiamondAnnotation>

  <BoxAnnotation color="#ffddaa" min="4 0.7 1" max="5 1 2">
        (5) 成型面板：使用默认配置。
  </BoxAnnotation>

  <BoxAnnotation color="#ffddaa" min="2 0 1" max="2.3 1 2">
        (6) 输入总线：使用默认配置。
  </BoxAnnotation>

  <DiamondAnnotation pos="3 0.5 1.5" color="#ddcc00">
    晶簇母岩放置器子网络
  </DiamondAnnotation>

<BoxAnnotation color="#aaaadd" min="0.7 2 1" max="1 3 2">
        (7) 存储总线 #3：已过滤为赛特斯石英水晶。其优先级设置得高于你的主存储。
        <ItemImage id="certus_quartz_crystal" scale="2" />
  </BoxAnnotation>

    <DiamondAnnotation pos="1.5 0.5 1.5" color="#00ff00">
        手动放入有瑕的赛特斯石英母岩。
        <BlockImage id="flawed_budding_quartz" scale="2" />
    </DiamondAnnotation>

    <DiamondAnnotation pos="1.5 1.5 1.5" color="#00ff00">
        手动取出赛特斯石英方块。
        <BlockImage id="quartz_block" scale="2" />
    </DiamondAnnotation>

<DiamondAnnotation pos="0.5 0.5 0" color="#00ff00">
        连接到主网络
    </DiamondAnnotation>

  <IsometricCamera yaw="165" pitch="5" />
</GameScene>

## 配置

### 簇破坏器：

* 第一个 <ItemLink id="annihilation_plane" /> (1) 没有 GUI，且无法配置，但可以附魔时运。
* 第一个 <ItemLink id="storage_bus" /> (2) 被过滤为 <ItemLink id="certus_quartz_crystal" />。

### 赛特斯方块破坏器：

* 第二个 <ItemLink id="annihilation_plane" />（3）没有 GUI，无法进行配置，但必须附魔精准采集。
* 第二个 <ItemLink id="storage_bus" />（4）会被过滤为 <ItemLink id="quartz_block" />。

### 晶芽方块放置器：

* <ItemLink id="formation_plane" /> (5) 使用默认配置。
* <ItemLink id="import_bus" /> (6) 使用默认配置。

### 在主网络上：

* 第三个 <ItemLink id="storage_bus" />（7）已过滤为 <ItemLink id="certus_quartz_crystal" />，并且其
  [priority](../ae2-mechanics/import-export-storage.md#storage-priority) 设置得高于你的主存储。

## 工作原理

### 簇破坏器：

簇破坏子网的工作方式与[简易赛特斯农场](simple-certus-farm.md)中的子网非常相似。

1. <ItemLink id="annihilation_plane" /> 会尝试破坏它前方的东西，但它只能破坏 <ItemLink id="quartz_cluster" />，
   因为该子网上唯一的存储设备是 <ItemLink id="storage_bus" />，并被过滤为 <ItemLink id="certus_quartz_crystal" />。
2. <ItemLink id="storage_bus" /> 会将赛特斯石英水晶存入桶中。

### 赛特斯方块破坏器

赛特斯方块破坏器子网用于在枯竭的晶种方块变成普通的 <ItemLink id="quartz_block" /> 后将其破坏。
它的工作方式与簇破坏器类似。

1. <ItemLink id="annihilation_plane" /> 会尝试破坏它前方的方块，但由于该子网上唯一的存储是 <ItemLink id="storage_bus" />，并且被过滤为 <ItemLink id="quartz_block" />，所以它只能破坏 <ItemLink id="quartz_block" />。
   该平面需要具有精准采集，这样母岩在被破坏时就不会降级，因此平面也不会过早将其破坏。
2. <ItemLink id="storage_bus" /> 会将赛特斯石英方块存入耗尽的赛特斯母岩桶中，你必须手动将它与 <ItemLink id="charged_certus_quartz_crystal" /> 一起扔进水里来刷新它。

### 晶芽方块放置器

晶芽方块放置子网会在破坏子网打碎旧的、已耗尽的方块后，放置一个新的 <ItemLink id="flawed_budding_quartz" />。

1. <ItemLink id="import_bus" /> 会从输入桶中导入母岩。
2. 子网上唯一的存储设备是 <ItemLink id="formation_plane" />，它会放置母岩。

### 在主网络上

* <ItemLink id="storage_bus" /> 让主网络（以及 [充电器自动化](charger-automation.md)）能够访问木桶中的所有赛特斯石英水晶。它被设置为
  高[优先级](../ae2-mechanics/import-export-storage.md#storage-priority)，这样赛特斯石英水晶会优先
  被放回木桶中，而不是放入你的主存储里。