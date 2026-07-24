---
navigation:
  parent: items-blocks-machines/items-blocks-machines-index.md
  title: 压印机
  icon: inscriber
  position: 310
categories:
- machines
item_ids:
- ae2:inscriber
---

# 压印机

<BlockImage id="inscriber" scale="8" />

压印器可使用 [presses](presses.md) 来压印电路和[processors](processors.md)，并将各种物品粉碎成尘土。
它既可接受 AE2 的能量 (AE)，也可接受 Fabric/Forge Energy (E/FE)。它支持侧面配置，因此从不同侧面插入物品时，
会将它们放入其容器中的不同槽位。为便于操作，可以使用 <ItemLink id="certus_quartz_wrench" /> 来旋转它。
它还可以设置为将合成结果推送到相邻的容器中。

输入缓存器的大小可以调整。举例来说，如果你想从一个容器向一大片压印器阵列供料，
你会希望将缓存器设得小一些，这样材料就能在各个压印器之间更均匀地分配（而不是第一个
压印器先堆满到 64 个，其余的却还是空的）。

这 4 种电路模板用于制作[处理器](processors.md)

<Row>
  <ItemImage id="silicon_press" scale="4" />

  <ItemImage id="logic_processor_press" scale="4" />

  <ItemImage id="calculation_processor_press" scale="4" />

  <ItemImage id="engineering_processor_press" scale="4" />
</Row>

虽然“press”这个名称也可以用来称呼类似铁砧的方块，但在 <ItemLink id="pattern_access_terminal" /> 中给物品做标记时会很有用。

<ItemImage id="name_press" scale="4" />

## 设置

* 压印器可以设置为分侧（如下所述），也可以允许从任意一侧将输入物品放入任意槽位，并由内部过滤器决定
    物品该进入哪里。处于非分侧模式时，无法从顶部和底部槽位中抽取物品。
* 压印器可以设置为将物品推入邻近的容器中。
* 输入缓存的大小可以调整；大型选项适合需要你手动供料的独立压印器，而
小型选项则能让大型并行化布局更具可行性。

## GUI 与朝向

在分侧模式下，刻印机会根据你从哪一侧插入或抽取来筛选物品的去向。

![Inscriber GUI](../assets/diagrams/inscriber_gui.png) ![Inscriber Sides](../assets/diagrams/inscriber_sides.png)

A. **上输入栏**，可通过压印器的顶部访问（物品既可以被推入此槽位，也可以从此槽位拉出）

B. **中心输入** 可通过压印器的左侧、右侧、前侧和后侧插入（物品只能被推入此槽位，不能从中拉出）

C. **下输入栏** 可通过压印器的底面访问（可将物品推入此槽位，也可从中拉出）

D. **输出槽**可通过压印机的左侧、右侧、前侧和后侧抽取物品（该槽位中的物品只能被抽出，不能被推入）

## 简易自动化

例如，侧面特性和可旋转性意味着你可以像这样半自动化压印机：

<GameScene zoom="4" background="transparent">
  <ImportStructure src="../assets/assemblies/inscriber_hopper_automation.snbt" />
  <IsometricCamera yaw="195" pitch="30" />
</GameScene>

或者在非侧面模式下，直接向压印机输入和输出即可。

## 升级

压印器支持以下[升级](upgrade_cards.md):

*   <ItemLink id="speed_card" />

## 配方

<RecipeFor id="inscriber" />