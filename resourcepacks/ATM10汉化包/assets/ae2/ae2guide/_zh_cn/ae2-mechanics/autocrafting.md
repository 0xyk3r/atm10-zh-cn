---
navigation:
  parent: ae2-mechanics/ae2-mechanics-index.md
  title: 自动合成
  icon: pattern_provider
---

# 自动合成

### 大家伙

<GameScene zoom="4" interactive={true}>
  <ImportStructure src="../assets/assemblies/autocraft_setup_greebles.snbt" />
  <IsometricCamera yaw="195" pitch="30" />
</GameScene>

自动合成是应用能源的主要功能之一。你不用再手动合成每一种子材料所需的正确数量，
然后像某种*庶民*一样埋头苦干；你可以让你的 ME 系统替你完成这些工作。你也可以自动合成物品并将其导出到其他地方。
或者通过巧妙的涌现行为，自动维持某些物品的库存数量。它同样适用于流体；如果你安装了
某些能支持额外模组材料类型的附属模组，比如通用机械的气体，这些材料也一样适用。真的非常强大。

这是个相当复杂的话题，所以打起精神，我们开始吧。

一套自动合成设置由 3 部分组成：
- 发送合成请求的装置
- 合成器CPU
- <ItemLink id="pattern_provider" />。

其工作流程如下：

1. 某些东西会创建一个请求合成请求。这可以是你在终端中点击某个可合成物品，或者是装有搜索合成卡片的数据总线或接口在请求它们被设置为导出/库存的某种物品。

*   （**重要：**使用你绑定到“选取方块”的按键（通常是鼠标中键）来请求合成你库存中已有的物品，这可能会与物品栏整理模组冲突），

2. ME系统会计算完成该请求所需的材料和前置合成步骤，并将它们存储在所选的合成器CPU中

3. 带有对应[样板](../items-blocks-machines/patterns.md)的 <ItemLink id="pattern_provider" /> 会将样板中指定的材料推送到任意相邻容器中。  
    如果是工作台配方（“合成样板”），那将会是一个 <ItemLink id="molecular_assembler" />。  
    如果是非合成配方（“处理样板”），那将会是其他某种方块、机器，或是复杂的红石控制装置。

4. 合成结果必须以某种方式返回到系统中，无论是通过导入总线、接口，还是将结果推回样板供应器。
    **请注意，必须触发一次“物品进入系统”事件；你不能只是把结果用管道输送到一个带有 <ItemLink id="storage_bus" /> 的箱子里。**

5. 如果该合成是请求中另一项合成的前置步骤，这些物品会存储在该合成器CPU中，然后用于该合成。

## 递归配方

<ItemImage id="minecraft:netherite_upgrade_smithing_template" scale="4" />

自动合成算法*无法*处理的一类情况是递归配方。例如，复制类配方，像是
把红石丢进 Botania 的魔力池后得到“1 个红石粉 = 2 个红石粉”。另一个例子则是原版 Minecraft 中的锻造模板。
不过，[有一种方法可以处理这类配方。](../example-setups/recursive-crafting-setup.md)

# 样式

<ItemImage id="crafting_pattern" scale="4" />

样式是在 <ItemLink id="pattern_encoding_terminal" /> 中由空白样式制成的。

针对不同用途，有几种不同类型的样板：

*   <ItemLink id="crafting_pattern" />可对工作台制作的配方进行编码。它们可以直接放入 <ItemLink id="molecular_assembler" /> 中，使其在获得材料时制作出结果，但它们的主要用途是放在分子装配室旁边的 <ItemLink id="pattern_provider" /> 中。
    在这种情况下，样板供应器具有特殊行为，会将对应的样板连同材料一起发送到相邻的组装机中。
    由于组装机会将合成结果自动弹出到相邻容器中，因此，要自动化合成样板，只需要在样板供应器上放置一台组装机即可。

***

*   <ItemLink id="smithing_table_pattern" />与合成样板非常相似，但它们记录的是锻造台配方。它们同样可以通过样板供应器
    和分子装配室自动化，且工作方式完全相同。实际上，合成、锻造和切石机样板都可以
    在同一套布局中使用。

***

*   <ItemLink id="stonecutting_pattern" /> 与合成样板非常相似，但它们编码的是切石机配方。它们同样可以由样板供应器和分子装配室自动化，且工作方式完全相同。事实上，合成、铁匠和切石机样板可以在同一套布局中使用。

***

*   <ItemLink id="processing_pattern" />s 是自动合成拥有高度灵活性的主要来源。它们是最通用的一类，本质上只是
    在说：“如果样板供应器将这些材料推送到相邻的容器中，那么 ME 系统迟早会在某个时候收到这些物品。”
    你会用它们来通过几乎任何模组机器进行自动合成，也可以用于熔炉之类的设备。正因为它们用途如此
    广泛，而且完全不关心从推送材料到收到结果之间发生了什么，你就可以玩出很多非常离谱的花活，比如把
    材料输入到一整套复杂的工厂生产链中，让它自动分拣物品、从无限产出的农场中获取其他材料、打印出整部《三倍大的蜜蜂总动员》剧本——
    只要 ME 系统最终收到了样板所指定的结果，它就根本不在乎。事实上，
    它甚至不在乎这些材料和结果之间是否有任何关系。你完全可以告诉它“1 个樱桃橡木木板 = 1 个下界之星”，然后让
    你的凋灵农场在收到一个樱桃橡木木板后击杀一只凋灵，这样同样也能正常运作。

支持多个具有相同配方的 <ItemLink id="pattern_provider" /> 同时并行工作。此外，你还可以让配方设定为例如 8 个圆石 = 8 个石子，而不是 1 个圆石 = 1 个石子，这样配方提供器每次运行时都会向你的烧炼装置中一次性插入 8 个圆石，而不是每次只插入 1 个。

## “样式”最通用的形式

实际上，还有一种比处理样板更“通用”的“样板”形式。带有合成卡片的 <ItemLink id="level_emitter" /> 可以被设置为发出红石信号，以便合成某些东西。这种“样板”并不定义，甚至根本不关心原料。它所表达的只有：“如果你让这个等级发信器发出红石信号，那么 ME 系统在不久或很久的将来某个时刻会收到这个物品。” 这通常用于启用和停用不需要输入原料的无限农场，或者用于激活处理循环配方的系统（这是标准自动合成无法理解的），例如“1 圆石 = 2 圆石”——前提是你有一台能够复制圆石的机器。

# 合成器CPU

<GameScene zoom="4" background="transparent">
  <ImportStructure src="../assets/assemblies/crafting_cpus.snbt" />
  <IsometricCamera yaw="195" pitch="30" />
</GameScene>

合成CPU用于管理请求合成/任务。在执行具有多个步骤的合成任务时，它们会存储中间材料，并影响任务规模上限，以及在一定程度上影响完成速度。它们是多方块结构，且必须是包含至少 1 个合成存储器的长方体。

合成CPU由以下部件组成：

*   （必需）[合成存储器](../items-blocks-machines/crafting_cpu_multiblock.md)，提供所有标准存储元件容量（1k、4k、16k、64k、256k）。它们用于存放合成过程中涉及的原料和中间产物，因此如果要让 CPU 处理原料更多的合成任务，就需要更大或更多的存储器。
*   （可选）<ItemLink id="crafting_accelerator" />s，它们能让系统更频繁地从样板供应器发出成批的原料。
    这样一来，例如一个被 6 个分子装配室包围的样板供应器，就能同时向这 6 个分子装配室发送原料（也就能同时使用这 6 个），而不只是其中 1 个。
*   （可选）<ItemLink id="crafting_monitor" />s，它们会显示当前 CPU 正在处理的任务。可以通过 <ItemLink id="color_applicator" /> 为它们着色
*   （可选）<ItemLink id="crafting_unit" />s，它们只是用于填充空间，使 CPU 形成一个长方体。

每个合成器CPU只能处理 1 个请求或任务，因此如果你想同时请求一个运算处理器和 256 个平滑石头，你就需要 2 个 CPU 多方块结构。

它们可以被设置为处理来自玩家、自动化（输出总线和接口）或两者的请求。

# 样板供应器

<Row>
<BlockImage id="pattern_provider" scale="4" />

<BlockImage id="pattern_provider" p:push_direction="up" scale="4" />

<GameScene zoom="4" background="transparent">
  <ImportStructure src="../assets/blocks/cable_pattern_provider.snbt" />
</GameScene>
</Row>

<ItemLink id="pattern_provider" />是你的自动合成系统与世界交互的主要方式。它们会将其 [patterns](../items-blocks-machines/patterns.md) 中的材料推送到相邻的容器中，并且物品也可以插入其中，以便将它们插入网络。通常，可以将机器的输出通过管道送回附近的样板供应器（通常就是推送材料的那个），而不是使用 <ItemLink id="import_bus" /> 将机器的输出拉入网络，这样往往可以节省一个频道。

需要注意的是，由于它们会将材料从合成器CPU中的[crafting storage](../items-blocks-machines/crafting_cpu_multiblock.md#crafting-storage)直接推出，因此这些材料实际上从未存在于它们的容器中，所以你无法从它们那里用管道导出物品。你必须让供应器将物品推送到另一个容器（例如木桶）中，然后再从那里用管道导出。

另外需要注意的是，提供器必须一次性推送全部材料，不能分批推送一半。这一点可以加以利用。

样板供应器会与[subnets](../ae2-mechanics/subnetworks.md)上的接口发生一种特殊交互：如果该接口未被修改（请求槽中没有任何内容），
样板供应器将完全跳过该接口，并直接推送到该子网的[存储](../ae2-mechanics/import-export-storage.md)中，
跳过接口且不会用配方批次将其填满，更重要的是，在存储中有空间之前，不会插入下一批。

支持多个具有相同样式的样式供应器，并且它们会并行工作。

样板供应器会尝试将其批处理按顺序循环分配到它的所有面，从而并行使用所有连接的机器。

## 变种

样板供应器有 3 种不同的变体：普通、定向和平面。它们会影响其会将材料推送到哪些特定面、从哪些面接收物品，以及向哪些面提供网络连接。

*   普通样板供应器会将材料推送到所有面，从所有面接收输入，并且像大多数应用能源机器一样，充当线缆，为所有面提供网络连接。

*   定向样板供应器是通过对普通样板供应器使用 <ItemLink id="certus_quartz_wrench" /> 来改变其朝向制成的。
    它们只会将材料推送到所选的一侧，会从所有侧面接收输入，并且特意不会在所选侧面提供网络连接。
    如果你想搭建一个子网络，这样它们就可以在不连接网络的情况下向 AE2 机器推送材料。

*   扁平样板供应器是一种[线缆子部件](../ae2-mechanics/cable-subparts.md)，因此可以在同一根线缆上放置多个，从而实现紧凑的布局。
    它们的行为类似于定向样板供应器选中的那一侧：提供样板、接收输入，并且
    不会在其表面提供网络连接。

样板供应器可以在合成网格中于普通与扁平两种形态之间切换。

## 设置

样板供应器有多种模式：

*   **阻挡模式** 会在机器中已经有材料时，阻止样板供应器推送新一批材料。
*   **锁定合成** 可以在各种红石条件下锁定样板供应器，或一直锁定到上一次合成的结果被插入该特定的样板供应器中。
*   可以在 <ItemLink id="pattern_access_terminal" /> 上显示或隐藏样板供应器。

## 优先级

可以通过点击 GUI 右上角的扳手来设置优先级。在同一种物品存在多个[样板](../items-blocks-machines/patterns.md)
的情况下，会优先使用较高优先级的供应器中的样板，而不是较低优先级供应器中的样板，
除非网络没有较高优先级样板所需的材料。

# 分子装配室

<BlockImage id="molecular_assembler" scale="4" />

<ItemLink id="molecular_assembler" /> 会接收输入其中的物品，并执行相邻的 <ItemLink id="pattern_provider" /> 所定义的操作，
或执行插入的 <ItemLink id="crafting_pattern" />、<ItemLink id="smithing_table_pattern" /> 或 <ItemLink id="stonecutting_pattern" /> 所定义的操作，
然后将结果推送到相邻的容器中。

它们的主要用途是在 <ItemLink id="pattern_provider" /> 旁边使用。在这种情况下，样板供应器会有特殊行为，
会将相关样板的信息连同材料一起发送给相邻的组装机。由于组装机会自动将
合成结果弹出到相邻容器中（也就是进入样板供应器的返回槽位），因此，在样板供应器旁放置一台组装机，
就足以将样板合成自动化。

<GameScene zoom="4" background="transparent">
<ImportStructure src="../assets/assemblies/assembler_tower.snbt" />
<IsometricCamera yaw="195" pitch="30" />
</GameScene>