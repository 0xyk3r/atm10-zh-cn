---
navigation:
  parent: items-blocks-machines/items-blocks-machines-index.md
  title: 破坏面板
  icon: annihilation_plane
  position: 210
categories:
- devices
item_ids:
- ae2:annihilation_plane
---

# ME破坏面板

<GameScene zoom="8" background="transparent">
<ImportStructure src="../assets/blocks/annihilation_plane.snbt" />
</GameScene>

破坏面板会破坏方块并拾取物品。它的工作方式与 <ItemLink id="import_bus" /> 类似，会将物品推入[网络存储](../ae2-mechanics/import-export-storage.md)。要让物品被拾取，它们必须与面板的正面碰撞；它不会拾取一片区域内的物品。

破坏面板可以附魔任何镐类附魔，所以没错，如果你的整合包允许，你可以给其中几个附上高得离谱的时运等级，并
[自动化矿石处理](../example-setups/ore-fortuner.md)。此外，精准采集会产生你所预期的效果，效率会降低破坏方块的能量消耗，而耐久则有几率不消耗任何能量。

它们是[线缆部件](../ae2-mechanics/cable-subparts.md)。

**记得在你的区块声明中启用假玩家**

## 过滤

只有在能够将产出的掉落物/物品存入其所属网络时，破坏面板才会破坏方块或拾取物品。
这意味着要过滤它，*你必须限制其网络中可存储的内容*，最常见的做法就是将它放在一个
[子网](../ae2-mechanics/subnetworks.md)上。可以通过对 <ItemLink id="storage_bus" /> 或[存储元](../items-blocks-machines/storage_cells.md)
进行[分区](cell_workbench.md)来实现。

<GameScene zoom="6" interactive={true}>
  <ImportStructure src="../assets/assemblies/annihilation_filtering.snbt" />

  <DiamondAnnotation pos="1 0.5 0.5" color="#00ff00">
        过滤为你想要破坏的东西掉落的任何物品。
  </DiamondAnnotation>

  <DiamondAnnotation pos=".5 0.5 2.5" color="#00ff00">
        分区设置为你想要破坏的东西掉落的任何物品。
  </DiamondAnnotation>

  <IsometricCamera yaw="195" pitch="30" />
</GameScene>

再次强调，它是*按物品掉落物*来筛选的，所以举例来说，如果你想筛选破坏 <ItemLink id="minecraft:amethyst_cluster" />，
你就需要一个附有精准采集的平面，否则之前的每个生长阶段都不会掉落任何东西，因此无论如何平面都会将它们破坏掉，
因为网络始终可以存储“无”。

## 配方

<RecipeFor id="annihilation_plane" />