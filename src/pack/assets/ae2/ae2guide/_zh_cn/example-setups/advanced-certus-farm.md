---
navigation:
  parent: example-setups/example-setups-index.md
  title: 高级赛特斯农场
  icon: certus_quartz_crystal
  position: 120
---

# 高级赛特斯农场

这基本上就是[半自动赛特斯农场](semiauto-certus-farm.md)，只不过它已经完全集成到你的 ME 系统中了。

这个装置不需要储备大量晶芽方块，也不用时不时手动刷新它们，
而是利用[充电器自动化](charger-automation.md)和[投水自动化](throw-in-water-automation.md)
来自动完成这一过程。

速度估算请参见 [赛特斯生长](../ae2-mechanics/certus-growth.md)。

**这是一个复杂的搭建结构，有些部分藏在其他部分后面，请拖动视角从各个角度查看**

<GameScene zoom="6" interactive={true}>
  <ImportStructure src="../assets/assemblies/advanced_certus_farm.snbt" />

<BoxAnnotation color="#ddaaaa" min="3.7 2 1" max="4 3 2">
        (1) 破坏面板 #1：没有可配置的 GUI，但可以附魔时运。
  </BoxAnnotation>

  <BoxAnnotation color="#ddaaaa" min="2 2 1.7" max="3 3 2">
        (2) 存储总线 #1：过滤为赛特斯石英水晶。
        <ItemImage id="certus_quartz_crystal" scale="2" />
  </BoxAnnotation>

  <DiamondAnnotation pos="3 2.5 1.5" color="#ff0000">
    晶簇破坏器子网络
  </DiamondAnnotation>

  <BoxAnnotation color="#aaddaa" min="3.7 1 1" max="4 2 2">
        (3) ME破坏面板 #2：无可配置的 GUI，但附有精准采集魔咒。
  </BoxAnnotation>

  <BoxAnnotation color="#aaddaa" min="2 1 1.7" max="3 2 2">
        (4) 存储总线 #2：过滤为赛特斯石英方块。
        <BlockImage id="quartz_block" scale="2" />
  </BoxAnnotation>

  <DiamondAnnotation pos="3 1.5 1.5" color="#00ff00">
    赛特斯方块破坏器子网络
  </DiamondAnnotation>

  <BoxAnnotation color="#ffddaa" min="4 0.7 1" max="5 1 2">
        (5) 成型面板：使用默认配置。
  </BoxAnnotation>

  <BoxAnnotation color="#ffddaa" min="2 0.7 2" max="3 1 3">
        (6) 输入总线：过滤为有瑕的赛特斯石英母岩。
        <BlockImage id="flawed_budding_quartz" scale="2" />
  </BoxAnnotation>

  <DiamondAnnotation pos="3 0.5 1.5" color="#ddcc00">
    晶簇母岩放置器子网络
  </DiamondAnnotation>

<BoxAnnotation color="#aaaadd" min="1.7 2 2" max="2 3 3">
        (7) 存储总线 #3：已过滤为赛特斯石英水晶。其优先级设置得高于你的主存储。
        <ItemImage id="certus_quartz_crystal" scale="2" />
  </BoxAnnotation>

<BoxAnnotation color="#aaaadd" min="2 1 2" max="3 2 3">
        （8）接口：设置为在自身中保留 1 个有瑕的赛特斯石英母岩，并装有合成卡。
        <Row><BlockImage id="flawed_budding_quartz" scale="2" /> <ItemImage id="crafting_card" scale="2" /></Row>
  </BoxAnnotation>

<DiamondAnnotation pos="1.5 0.5 0" color="#00ff00">
        连接到主网络、充能器自动化和投水自动化
        <Row>
        <GameScene zoom="3" background="transparent">
          <ImportStructure src="../assets/assemblies/charger_automation.snbt" />
          <IsometricCamera yaw="195" pitch="30" />
        </GameScene>
        <GameScene zoom="3" background="transparent">
          <ImportStructure src="../assets/assemblies/throw_in_water.snbt" />
          <IsometricCamera yaw="195" pitch="30" />
        </GameScene>
        </Row>
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

* <ItemLink id="formation_plane" /> (5) 处于默认配置。
* <ItemLink id="import_bus" /> (6) 已过滤为 <ItemLink id="flawed_budding_quartz" />。

### 在主网络上：

* 第三个 <ItemLink id="storage_bus" />（7）已过滤为 <ItemLink id="certus_quartz_crystal" />，并且其
  [优先级](../ae2-mechanics/import-export-storage.md#storage-priority)设置得高于你的主存储。
* <ItemLink id="interface" />（8）被设置为在其自身中保留 1 个有瑕的赛特斯石英母岩，并且具有一个 <ItemLink id="crafting_card" />。

## 工作原理

### 簇破坏器：

簇破坏子网的工作方式与[简易赛特斯农场](simple-certus-farm.md)中的子网非常相似。

1. <ItemLink id="annihilation_plane" /> 会尝试破坏它前方的东西，但它只能破坏 <ItemLink id="quartz_cluster" />，
   因为该子网上唯一的存储设备是 <ItemLink id="storage_bus" />，并被过滤为 <ItemLink id="certus_quartz_crystal" />。
2. <ItemLink id="storage_bus" /> 会将赛特斯石英水晶存入桶中。

### 赛特斯方块破坏器

赛特斯方块破坏器子网用于在枯竭的晶种方块变成普通的 <ItemLink id="quartz_block" /> 后将其破坏。
它的工作方式与簇破坏器类似。

1. <ItemLink id="annihilation_plane" /> 会尝试破坏它前方的方块，但它只能破坏 <ItemLink id="quartz_block" />，
   因为该子网络上唯一的存储设备是 <ItemLink id="storage_bus" />，并且被筛选为只存储 <ItemLink id="quartz_block" />。
   这个平面必须具有精准采集，这样母岩在被破坏时就不会退化，因此平面也不会过早将其破坏。
2. <ItemLink id="storage_bus" /> 会将赛特斯石英方块存入 <ItemLink id="interface" /> 中，使
   [投水自动化](throw-in-water-automation.md) 能够用它来制作新的 <ItemLink id="flawed_budding_quartz" />。

### 晶芽方块放置器

晶芽方块放置子网会在破坏子网打碎旧的、已耗尽的方块后，放置一个新的 <ItemLink id="flawed_budding_quartz" />。

1. <ItemLink id="import_bus" /> 将 <ItemLink id="interface" /> 中的母岩导入到[网络存储](../ae2-mechanics/import-export-storage.md)
2. 子网中唯一的存储设备是 <ItemLink id="formation_plane" />，它会放置母岩。

### 在主网络上

* <ItemLink id="storage_bus" /> 让主网络（以及 [充电器自动化](charger-automation.md)）能够访问桶中的所有赛特斯石英晶体。它被设置为
  高[优先级](../ae2-mechanics/import-export-storage.md#storage-priority)，这样赛特斯石英晶体会优先
  放回桶中，而不是进入你的主存储。
* <ItemLink id="interface" /> 让生长晶块放置器子网能够访问 <ItemLink id="flawed_budding_quartz" />，并且
    让赛特斯方块破坏器子网能够将耗尽的方块送回主网络。
    <ItemLink id="crafting_card" /> 使接口能够从主网络的[自动合成](../ae2-mechanics/autocrafting.md)中请求新的生长晶块。