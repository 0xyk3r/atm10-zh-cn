---
navigation:
  parent: example-setups/example-setups-index.md
  title: 自动矿石时运机
  icon: minecraft:raw_iron
---

# 矿石时运自动化

<ItemLink id="annihilation_plane" /> 可以附上任何镐类附魔，包括时运，因此一个显而易见的用法是给其中几个附上时运，然后让 <ItemLink id="formation_plane" /> 和 <ItemLink id="annihilation_plane" /> 快速放置并破坏矿石。

请注意，由于 <ItemLink id="import_bus" /> 会“逐渐加速至运转速度”，该装置一开始会比较慢，几秒后才会达到全速。

<GameScene zoom="6" interactive={true}>
  <ImportStructure src="../assets/assemblies/ore_fortuner.snbt" />

  <BoxAnnotation color="#dddddd" min="2.7 0 2" max="3 1 3">
        (1) 输入总线：其中装有几张加速卡。
        <ItemImage id="speed_card" scale="2" />
  </BoxAnnotation>

  <BoxAnnotation color="#dddddd" min="0 0 2" max="2 1 2.3">
        (2) 成型面板：使用默认配置。
  </BoxAnnotation>

  <BoxAnnotation color="#dddddd" min="0 0 0.7" max="2 1 1">
        (3) ME破坏面板：没有可配置的 GUI，但附有时运魔咒。
  </BoxAnnotation>

  <BoxAnnotation color="#dddddd" min="2.7 0 0" max="3 1 1">
        (4) 存储总线：使用默认配置。
  </BoxAnnotation>

<DiamondAnnotation pos="3.5 0.5 2.5" color="#00ff00">
        输入
    </DiamondAnnotation>

<DiamondAnnotation pos="3.5 0.5 0.5" color="#00ff00">
        输出
    </DiamondAnnotation>

<DiamondAnnotation pos="4 0.5 1.5" color="#00ff00">
        连接到主网络
    </DiamondAnnotation>

  <IsometricCamera yaw="195" pitch="30" />
</GameScene>

## 配置

*   <ItemLink id="import_bus" /> (1) 里有几个 <ItemLink id="speed_card" />。阵列中的成型平面越多，所需的数量也就越多，因为它们会让导入总线一次拉取更多物品。
*   <ItemLink id="formation_plane" /> (2) 均处于默认配置。
*   <ItemLink id="annihilation_plane" /> (3) 没有 GUI，且无法配置，但附有时运魔咒。
*   <ItemLink id="storage_bus" /> (4) 处于默认配置。

## 工作原理

1.  绿色子网上的 <ItemLink id="import_bus" /> 会将第一个木桶中的方块导入到[存储网络](../ae2-mechanics/import-export-storage.md)
2.  绿色子网上唯一的存储设备是 <ItemLink id="formation_plane" />，它会放置这些方块。
3.  橙色子网上的 <ItemLink id="annihilation_plane" /> 会破坏这些方块，并对其应用时运效果。
4.  橙色子网上的 <ItemLink id="storage_bus" /> 会将破坏后的结果存入第二个木桶中。