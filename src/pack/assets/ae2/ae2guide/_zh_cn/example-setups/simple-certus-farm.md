---
navigation:
  parent: example-setups/example-setups-index.md
  title: 简单赛特斯农场
  icon: certus_quartz_crystal
  position: 110
---

# 简易赛特斯农场

如 [赛特斯生长](../ae2-mechanics/certus-growth.md)] 中所述，<ItemLink id="certus_quartz_crystal" /> 的自动收获需要用到 <ItemLink id="annihilation_plane" /> 和 <ItemLink id="storage_bus" />。  
<ItemLink id="growth_accelerator" /> 可用于大幅加快赛特斯石英芽的生长，随后平面会破坏已经完全成熟的 <ItemLink id="quartz_cluster" />。它们之所以能够被筛选出来，是利用了一个好得过头的特性：未成熟的赛特斯石英芽会掉落 <ItemLink id="certus_quartz_dust" />，而不是没有掉落物。

这个农场在使用 <ItemLink id="flawless_budding_quartz" /> 时可完全自动运行，但如果使用的是有瑕的、开裂的或损坏的赛特斯石英母岩，你就必须手动更换母岩。或者，如 [半自动赛特斯农场](semiauto-certus-farm.md)
和 [高级赛特斯农场](advanced-certus-farm.md) 中所述，也可以实现自动更换。

速度估算请参见 [赛特斯生长](../ae2-mechanics/certus-growth.md)。

<GameScene zoom="6" interactive={true}>
  <ImportStructure src="../assets/assemblies/simple_certus_farm.snbt" />

  <BoxAnnotation color="#dddddd" min="3.7 1 1" max="4 2 2">
        (1) ME破坏面板：没有可配置的 GUI，但可以附魔时运。
  </BoxAnnotation>

  <BoxAnnotation color="#dddddd" min="3 1 1" max="3.3 2 2">
        (2) 存储总线 #1：过滤为赛特斯石英水晶。
        <ItemImage id="certus_quartz_crystal" scale="2" />
  </BoxAnnotation>

<BoxAnnotation color="#dddddd" min="3 1 .7" max="2 2 1">
        （3）存储总线 #2：已过滤为赛特斯石英水晶。其优先级设置得高于主存储。
        <ItemImage id="certus_quartz_crystal" scale="2" />
  </BoxAnnotation>

<DiamondAnnotation pos="1 0.5 0.5" color="#00ff00">
        连接到主网络
    </DiamondAnnotation>

  <IsometricCamera yaw="195" pitch="30" />
</GameScene>

## 配置

* 第一个 <ItemLink id="annihilation_plane" /> (1) 没有 GUI，也无法配置，但可以附魔时运。
* 第一个 <ItemLink id="storage_bus" /> (2) 被筛选为 <ItemLink id="certus_quartz_crystal" />。
* 第二个 <ItemLink id="storage_bus" /> (3) 被筛选为 <ItemLink id="certus_quartz_crystal" />，并且其
  [优先级](../ae2-mechanics/import-export-storage.md#storage-priority) 被设置得高于主存储。

## 工作原理

1. <ItemLink id="annihilation_plane" /> 会尝试破坏其前方的方块，但只能破坏 <ItemLink id="quartz_cluster" />
   因为该子网络上唯一的存储设备是 <ItemLink id="storage_bus" />，并被筛选为 <ItemLink id="certus_quartz_crystal" />。
4. 第一个 <ItemLink id="storage_bus" /> 会将赛特斯石英水晶存入木桶中。
5. 第二个 <ItemLink id="storage_bus" /> 会让主网络能够访问木桶中的所有赛特斯石英水晶。它被设置为
   高 [priority](../ae2-mechanics/import-export-storage.md#storage-priority)，这样赛特斯石英水晶会被优先
   放回木桶中，而不是放进你的主存储里。