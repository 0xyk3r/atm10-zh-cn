---
navigation:
  parent: example-setups/example-setups-index.md
  title: 紫水晶农场
  icon: minecraft:amethyst_shard
---

# 紫水晶种植

虽然 <ItemLink id="growth_accelerator" /> 能作用于紫水晶，但用 <ItemLink id="annihilation_plane" /> 过滤[水晶石英芽](../items-blocks-machines/budding_certus.md)
的常规方法并不适用于紫晶芽。与未成熟的水晶石英芽会掉落
<ItemLink id="certus_quartz_dust" /> 不同，未成熟的紫晶芽不会掉落任何东西，因此破坏面板总是会将其破坏，
因为网络总是能够存储“什么都没有”。

解决办法是给 ME破坏面板附上精准采集。这样一来，未成熟的紫晶芽*确实*会掉落物品
（即紫晶芽方块的各个生长阶段），因此就可以被过滤。

然后，必须由 <ItemLink id="formation_plane" /> 再次放置 <ItemLink id="minecraft:amethyst_cluster" />，再由未附有精准采集的 <ItemLink id="annihilation_plane" /> 将其打破，才能获得 <ItemLink id="minecraft:amethyst_shard" />。

请注意，由于簇具有方向性，形成平面的正对面必须紧贴一个实心方块面。

<GameScene zoom="6" interactive={true}>
  <ImportStructure src="../assets/assemblies/amethyst_farm.snbt" />

  <BoxAnnotation color="#dddddd" min="2.7 1 1" max="3 2 2">
        (1) ME破坏面板 #1：无可配置的 GUI，但附有精准采集魔咒。
  </BoxAnnotation>

  <BoxAnnotation color="#dddddd" min="2 1 1" max="2.3 2 2">
        (2) 成型面板：过滤为紫水晶簇。
        <ItemImage id="minecraft:amethyst_cluster" scale="2" />
  </BoxAnnotation>

<BoxAnnotation color="#dddddd" min="1.3 0.7 1" max="2 1 2">
        (3) ME破坏面板 #2：没有可供配置的 GUI，但可以附魔时运。
  </BoxAnnotation>

  <BoxAnnotation color="#dddddd" min="1 0 1" max="1.3 1 2">
        (4) 存储总线 #1：过滤为紫水晶碎片。
        <ItemImage id="minecraft:amethyst_shard" scale="2" />
  </BoxAnnotation>

<BoxAnnotation color="#dddddd" min="0 0 .7" max="1 1 1">
        （5）存储总线 #2：过滤为紫水晶碎片。其优先级设置得高于你的主存储。
        <ItemImage id="minecraft:amethyst_shard" scale="2" />
  </BoxAnnotation>

<DiamondAnnotation pos="0 0.5 0.5" color="#00ff00">
        连接到主网络
    </DiamondAnnotation>

  <IsometricCamera yaw="195" pitch="30" />
</GameScene>

## 配置

* 第一个 <ItemLink id="annihilation_plane" />（1）没有 GUI，无法配置，但必须附魔精准采集。
* 将 <ItemLink id="formation_plane" />（2）筛选为 <ItemLink id="minecraft:amethyst_cluster" />。
* 第二个 <ItemLink id="annihilation_plane" />（3）没有 GUI，无法配置，但可以附魔时运。
* 将第一个 <ItemLink id="storage_bus" />（4）筛选为 <ItemLink id="minecraft:amethyst_shard" />。
* 将第二个 <ItemLink id="storage_bus" />（5）筛选为 <ItemLink id="minecraft:amethyst_shard" />，并且其
  [priority](../ae2-mechanics/import-export-storage.md#storage-priority) 设置得高于你的主存储。

## 工作原理

1. 第一个 <ItemLink id="annihilation_plane" /> 会尝试破坏它前方的方块，但由于子网中唯一的存储设备是 <ItemLink id="formation_plane" />，且已被筛选为紫水晶簇，因此它只能破坏 <ItemLink id="minecraft:amethyst_cluster" />。这之所以可行，是因为该面板附有精准采集附魔；否则它也能破坏未成熟的晶芽，而那些晶芽不会掉落任何物品。
2. <ItemLink id="formation_plane" /> 会将紫水晶簇放置在与其相对的方块上。
3. 第二个 <ItemLink id="annihilation_plane" /> 会破坏紫水晶簇，产出 <ItemLink id="minecraft:amethyst_shard" />。
4. 第一个 <ItemLink id="storage_bus" /> 会将紫水晶碎片存入木桶中。从技术上来说，这里其实不需要筛选，因为第二个破坏面板理论上只会接触到完全长成的紫水晶簇。
5. 第二个 <ItemLink id="storage_bus" /> 会让主网络能够访问木桶中的所有紫水晶碎片。它被设置为较高的 [优先级](../ae2-mechanics/import-export-storage.md#storage-priority)，这样紫水晶碎片会优先放回木桶中，而不是放进你的主存储里。