---
navigation:
  parent: items-blocks-machines/items-blocks-machines-index.md
  title: 成型面板
  icon: formation_plane
  position: 210
categories:
- devices
item_ids:
- ae2:formation_plane
---

# 成型面板

<GameScene zoom="8" background="transparent">
  <ImportStructure src="../assets/blocks/formation_plane.snbt" />
</GameScene>

成型面板会放置方块并丢出物品。它的工作方式类似于仅可插入的 <ItemLink id="storage_bus" />，
当物品被 [ME设备](../ae2-mechanics/devices.md) 插入到 [网络存储](../ae2-mechanics/import-export-storage.md) 中时，就会进行放置/丢出，例如 <ItemLink id="import_bus" />ses 和 <ItemLink id="interface" />s。

<GameScene zoom="8" interactive={true}>
  <ImportStructure src="../assets/assemblies/formation_plane_demonstration.snbt" />
  <IsometricCamera yaw="255" pitch="30" />
</GameScene>

请注意，这些与[管道子网络](../example-setups/pipe-subnet.md)中的“输入总线 -> 存储总线”和“接口 -> 存储总线”管道类似。

<GameScene zoom="6" interactive={true}>
  <ImportStructure src="../assets/assemblies/import_storage_pipe.snbt" />
  <IsometricCamera yaw="195" pitch="30" />
</GameScene>

<GameScene zoom="6" interactive={true}>
  <ImportStructure src="../assets/assemblies/interface_storage_pipe.snbt" />
  <IsometricCamera yaw="195" pitch="30" />
</GameScene>

这个[设备](../ae2-mechanics/devices.md)利用了类似于[管道子网](../example-setups/pipe-subnet.md)这类设置中所使用的存储总线机制，
如果你想要丢弃物品/放置方块而不是运输物品，它就可以在这些设置中替代存储总线。

它们是[线缆部件](../ae2-mechanics/cable-subparts.md)。

**记得在你的区块声明中启用假玩家**

## 过滤

默认情况下，该平面会放置/丢出任何物品。插入其过滤槽的物品会作为白名单，只允许放置那些特定物品。

即使你实际上并没有该物品，仍然可以从 JEI/REI 将物品和流体拖入槽位中。

使用流体容器（如桶或储罐）右击，即可将其中的流体设为过滤器，而不是将桶或储罐物品本身设为过滤器。

## 优先级

可以通过点击 GUI 右上角的扳手来设置优先级。
进入网络的物品会从最高优先级的存储开始放入。

## 设置

*   该面板可设置为在世界中放置方块或掉落物品

## 升级

成型面板支持以下[升级](upgrade_cards.md):

*   <ItemLink id="capacity_card" /> 会增加过滤槽的数量
*   <ItemLink id="fuzzy_card" /> 可让平面按耐久等级进行过滤和/或忽略物品NBT
*   <ItemLink id="inverter_card" /> 会将过滤器从白名单切换为黑名单

## 配方

<RecipeFor id="formation_plane" />