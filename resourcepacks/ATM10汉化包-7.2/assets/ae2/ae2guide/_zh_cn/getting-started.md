---
navigation:
  title: 入门指南（1.20+）
  position: 10
---

<div class="notification is-info">
  以下信息仅适用于 Minecraft 1.20 及更高版本中的应用能源2。
</div>

# 入门指南

## 获取初始材料）

<GameScene zoom="4" background="transparent">
  <ImportStructure src="assets/assemblies/meteor_interior.snbt" />
</GameScene>

要开始接触应用能源2，首先必须找到一颗[陨石](ae2-mechanics/meteorites.md)。这类东西相当常见，而且往往会在地形上留下巨大的坑洞，所以你大概已经在旅途中遇到过了。
如果还没有，你可以合成一个 <ItemLink id="meteorite_compass" />，它会指向最近的 <ItemLink id="mysterious_cube" />。

找到一块陨石后，向其中心挖掘。你会发现赛特斯石英簇、水晶石英芽、各类[budding certus blocks](items-blocks-machines/budding_certus.md)，以及位于中央的神秘方块。

挖掘赛特斯石英簇，以及你找到的所有赛特斯石英方块。你也可以采集正在生长的赛特斯方块，但如果没有精准采集，它们会降级 1 个阶段。

不要破坏任何无瑕的赛特斯石英母岩，因为即使使用精准采集，它们也会劣化为有瑕的赛特斯石英母岩，而且无法将其修复回无瑕状态。

另外，挖掘陨石中央的神秘方块，可以获得全部 4 个压印模板。

## 生长赛特斯石英

<GameScene zoom="4" background="transparent">
<ImportStructure src="assets/assemblies/budding_certus_1.snbt" />
</GameScene>

水晶石英芽会从[萌发赛特斯石英块](items-blocks-machines/budding_certus.md)上长出，类似于紫水晶。如果你打破一个尚未完全
长成的芽，它会掉落一个<ItemLink id="certus_quartz_dust" />，且不会受到时运影响。如果你打破一个完全长成的晶簇，它会掉落四个
<ItemLink id="certus_quartz_crystal" />，并且时运会提高这个数量。

萌发中的赛特斯方块共有 4 个等级：完美之力、有瑕、破缺和损坏。

<GameScene zoom="4" background="transparent">
<ImportStructure src="assets/assemblies/budding_blocks.snbt" />
<IsometricCamera yaw="195" pitch="30" />
</GameScene>

每当晶芽生长到下一阶段时，母岩都有概率降一级，最终变成普通的赛特斯石英方块。你可以通过将母岩（或赛特斯石英方块）与一个或多个 <ItemLink id="charged_certus_quartz_crystal" /> 一同丢入水中来修复它们（并制造新的母岩）。

<RecipeFor id="damaged_budding_quartz" />

无瑕的赛特斯石英母岩不会退化，并且会无限生成赛特斯石英。不过它们无法被合成，也不能用镐子移动，即使附有精准采集也不行。（不过它们*可以*通过[封闭空间](ae2-mechanics/spatial-io.md)来移动）

仅靠自身，水晶石英芽的生长速度非常缓慢。幸运的是，将 <ItemLink id="growth_accelerator" /> 放置在发芽方块旁边时，可以大幅加快这一过程。你应该优先先建造几个这样的装置。

<GameScene zoom="4" background="transparent">
<ImportStructure src="assets/assemblies/budding_certus_2.snbt" />
<IsometricCamera yaw="195" pitch="30" />
</GameScene>

如果你的石英不够再制作一个 <ItemLink id="energy_acceptor" /> 或 <ItemLink id="vibration_chamber" />，
你可以先做一个 <ItemLink id="crank" />，然后把它接在线圈加速器的末端。

如何自动收获赛特斯晶体已在[此处说明](example-setups/simple-certus-farm.md)。

## 关于福鲁伊克斯的简短补充

你还需要另一种材料：福鲁伊克斯，你在制作生长加速器时应该已经接触过了。它是将带电赛特斯水晶、红石和下界石英扔进水中制成的。至于如何自动完成这件事，“就留给读者自己练习吧”。

需要用到 <ItemLink id="charger" /> 才能产出 <ItemLink id="charged_certus_quartz_crystal" />。如果你还没有做过的话。

## 压印一些处理器

在搜刮陨石时，你会从破坏神秘方块中找到四个“模版”。它们可在 <ItemLink id="inscriber" /> 中用于制作三种类型的处理器。

<ItemGrid>
  <ItemIcon id="silicon_press" />

  <ItemIcon id="logic_processor_press" />

  <ItemIcon id="calculation_processor_press" />

  <ItemIcon id="engineering_processor_press" />
</ItemGrid>

压印机是一台区分面输入输出的机器，很像原版熔炉。从顶部或底部插入会将物品放入上方或下方槽位，从侧面或背面插入则会放入中央槽位。成品可以从侧面或背面取出。

为了方便使用漏斗进行自动化（也可能减少管道乱成一团的情况），可以使用 <ItemLink id="certus_quartz_wrench" /> 旋转压印器。

先制作少量各种处理器，为下一步搭建一个最基础的 ME 系统做准备。如何自动化处理器生产“[留给读者自行练习](example-setups/processor-automation.md)”。

## 物质能量技术：ME网络与存储

### 什么是ME存储？

它读作 Emm-Eee，代表质能。

质能是应用能源2的核心组成部分，它就像疯狂科学家版的多方块箱子，
并且能够彻底改变你的存储方式。ME 与 Minecraft 中的其他存储系统截然不同，
你可能需要一点跳出常规的思维方式才能适应；但一旦上手，在极小空间内容纳海量存储、
以及使用多个访问终端，都还只是它所能实现之事的冰山一角。

### 开始之前我需要了解什么？

首先，ME 会将物品存储在其他物品中，称为[存储单元](items-blocks-machines/storage_cells.md); 它们共有 5 个等级，存储容量依次增加。
要使用存储单元，必须将其放入 <ItemLink id="chest" /> 或 <ItemLink id="drive" /> 中。

将 <ItemLink id="chest" /> 放入后，它会立即显示该单元中的内容，而且你可以像操作 <ItemLink id="minecraft:chest" /> 一样向其中添加和取出物品，但其中的物品实际上存储在存储单元中，而不是存储在 <ItemLink id="chest" /> 本身中。

<ItemLink id="chest" /> 的适用场景相当有限，实用性也不高。要真正
发挥 AE2 的优势，你需要搭建一个[ME网络](ae2-mechanics/me-network-connections.md)。

## 你的第一个 ME 系统

现在你已经拥有了应用能源2所需的所有基础材料和机器，可以制作你的第一个 ME（质能转换）系统了。这将是一个非常基础的系统，没有自动合成，没有物流，只有美观、简单且可搜索的存储。

<GameScene zoom="6" interactive={true}>
<ImportStructure src="assets/assemblies/tiny_me_system.snbt" />

</GameScene>

*   你需要准备的材料：
    * 1x <ItemLink id="drive" />
    * 1x <ItemLink id="terminal" /> 或 <ItemLink id="crafting_terminal" />
    * 1x <ItemLink id="energy_acceptor" />
    * 几根 [线缆](items-blocks-machines/cables.md)，可以是玻璃、包层或智能线缆，但不能是致密线缆
    * 几个 [存储元](items-blocks-machines/storage_cells.md)，推荐使用 4k 的，这样能在容量和类型之间取得不错的平衡（如果将 4k 和 1k 混合后再进行[分区](items-blocks-machines/cell_workbench.md)，效率会更高，不过这个就先不展开讲了）
---
1.  先放下驱动器。
2.  能源接收器（以及其他一些 AE2 [设备](ae2-mechanics/devices.md))有两种模式：立方体和平面。它们可以在合成网格中相互切换。如果你的能源接收器是立方体，就把它放在驱动器旁边；如果它是扁平方块，就先在驱动器上接一根线缆，再把接收器放在线缆上。
3.  用你喜欢的发电模组中的线缆/管道/导管，将能量输入到能源接收器中。
4.  在驱动器顶部放一根线缆（或者放在视线高度的其他位置），然后把你的终端或合成终端放上去。
5.  将存储元放入驱动器中
6.  起飞
7.  调整一下终端的设置
8.  沉浸在自己无上的力量与能力之中
9.  然后意识到，这个网络从大局来看其实相当小

### 扩展你的网络

现在你已经有了一些基础存储，并且能够访问这些存储，这是个不错的开始，但你之后很可能会想要将一些处理过程自动化。

一个很好的例子是：在熔炉顶部放置一个 <ItemLink id="export_bus" /> 来
输入矿石，再在熔炉底部放置一个 <ItemLink id="import_bus" />
来提取冶炼后的矿石。

<ItemLink id="export_bus" /> 可让你将物品从网络导出到所连接的
容器中，而 <ItemLink id="import_bus" /> 则会将所连接容器中的物品导入
网络。

### 突破限制

此时你大概已经接近拥有 8 个左右的[ME设备](ae2-mechanics/devices.md)，一旦达到 9 个设备，你就必须开始
管理[频道](ae2-mechanics/channels.md)。许多设备都需要频道才能
运作，但并非全部如此。

默认情况下，一个网络最多可支持 8 个频道，一旦超过这个限制，你就必须在网络中添加一个 <ItemLink id="controller" />。这样可以大幅扩展你的网络。

[智能线缆](items-blocks-machines/cables.md) 可以让你看到频道是如何在网络中进行路由的。刚开始接触时请多加使用，以了解频道的运作方式；或者当你有大量红石和荧石时，也可以使用它们。