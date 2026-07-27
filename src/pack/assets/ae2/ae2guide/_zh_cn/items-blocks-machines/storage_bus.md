---
navigation:
  parent: items-blocks-machines/items-blocks-machines-index.md
  title: ME存储总线
  icon: storage_bus
  position: 220
categories:
- devices
item_ids:
- ae2:storage_bus
---

# 存储总线

<GameScene zoom="8" background="transparent">
<ImportStructure src="../assets/blocks/storage_bus.snbt" />
</GameScene>

想要*保留*你的箱子怪，而不是把它替换成更合理的东西吗？隆重推出存储总线！

存储总线会将它所接触的容器变成[网络存储](../ae2-mechanics/import-export-storage.md)。
它通过让网络能够看到该容器中的内容，并向该
容器推入和从中拉出物品，来满足[ME设备](../ae2-mechanics/devices.md)向网络存储推入和从中拉取物品的需求。

由于应用能源的设计理念是：通过[ME设备](../ae2-mechanics/devices.md)各项功能之间的相互作用产生涌现式机制，因此你不一定*必须*把存储总线用于*存储*。通过使用[子网络](../ae2-mechanics/subnetworks.md)，让存储总线（或少量存储总线）成为一个网络中*唯一*的存储，你就可以把它用作物品传输的来源或目的地。（参见["管道子网"](../example-setups/pipe-subnet.md)）

重要提示：像抽屉这类大型且经过优化的容器没问题，但像
巨型箱子这种拥有大量槽位、却*未*优化的大型容器，在与存储总线一起使用时会严重影响性能。

它们是[线缆部件](../ae2-mechanics/cable-subparts.md)。

## 过滤

默认情况下，总线会存储所有物品。将物品放入它的过滤槽后，这些物品将作为白名单，只允许存储这些特定物品。

即使你实际上并没有该物品，仍然可以从 JEI/REI 将物品和流体拖入槽位中。

使用流体容器（如桶或储罐）右击，即可将其中的流体设为过滤器，而不是将桶或储罐物品本身设为过滤器。

## 优先级

可以通过点击 GUI 右上角的扳手来设置优先级。
进入网络的物品会先以前往最高优先级的存储作为
它们的首个目的地。如果两个存储具有相同的优先级，
而其中一个已经包含该物品，则会优先选择那个存储，
而不是其他存储。任何已过滤的存储都会被视为已经包含该物品，
前提是它与其他存储处于同一优先级组中。从存储中取出物品时，
会从优先级最低的存储中移除。这个优先级系统意味着，当物品被插入和移出
网络存储时，高优先级的存储会被填满，而低优先级的存储会被清空。

## 设置

*   总线可以根据相邻存储空间中当前的内容进行分区（过滤）
*   可以设置网络禁止或允许识别相邻存储空间中总线无法提取的物品
    （例如，存储总线无法从 <ItemLink id="inscriber" /> 的中间输入槽中提取物品）
*   总线可以同时对输入和输出进行过滤，也可以仅对输入进行过滤
*   总线可以是双向、仅存入或仅取出

## 升级

存储总线支持以下[升级](upgrade_cards.md):

*   <ItemLink id="capacity_card" /> 会增加过滤槽的数量
*   <ItemLink id="fuzzy_card" /> 让总线能够按耐久值进行过滤和/或忽略物品NBT
*   <ItemLink id="inverter_card" /> 会将过滤器从白名单切换为黑名单
*   <ItemLink id="void_card" /> 会在所连接的容器已满时清空插入的物品，可用于防止农场堵塞。请务必对其进行分区！

## 配方

<RecipeFor id="storage_bus" />