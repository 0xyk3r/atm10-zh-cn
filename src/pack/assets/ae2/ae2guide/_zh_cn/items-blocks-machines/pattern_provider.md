---
navigation:
  parent: items-blocks-machines/items-blocks-machines-index.md
  title: 样板供应器
  icon: pattern_provider
  position: 210
categories:
- devices
item_ids:
- ae2:pattern_provider
- ae2:cable_pattern_provider
---

# 样板供应器

<Row gap="20">
<BlockImage id="pattern_provider" scale="8" />
<BlockImage id="pattern_provider" p:push_direction="up" scale="8" />
<GameScene zoom="8" background="transparent">
  <ImportStructure src="../assets/blocks/cable_pattern_provider.snbt" />
</GameScene>
</Row>

样板供应器是你的[自动合成](../ae2-mechanics/autocrafting.md)系统与世界交互的主要方式。它们会将其[样板](patterns.md)中的材料推送到相邻的容器中，而物品也可以被插入其中，从而将其插入网络。通常，将机器的输出通过管道送回附近的样板供应器（通常就是推送材料的那个），而不是使用<ItemLink id="import_bus" />将机器的输出拉回网络，这样往往可以节省一个频道。

需要注意的是，由于它们会将材料从合成器CPU中的[crafting storage](crafting_cpu_multiblock.md#crafting-storage)直接推出，因此这些材料实际上从未存在于它们的容器中，所以你无法从它们那里用管道导出物品。你必须让供应器将物品推送到另一个容器（例如木桶）中，然后再从那里用管道导出。

另外需要注意的是，提供器必须一次性推送全部材料，不能分批推送一半。这一点可以加以利用。

样板供应器会与[subnets](../ae2-mechanics/subnetworks.md)上的接口产生一种特殊交互：如果接口未被修改（请求槽中没有任何内容），
样板供应器将完全跳过该接口，并直接推送到该子网的[存储](../ae2-mechanics/import-export-storage.md)中，
跳过接口且不会用配方批次将其填满，更重要的是，在机器中有空位之前，它不会插入下一批。
这与阻挡模式能够正确配合，样板供应器会监控机器中的配料槽，而不是接口中的槽。

例如，这种布局会将待冶炼的物品和燃油直接推入熔炉中对应的槽位。

你可以用它通过样板向一台机器的多个面提供物品，或向多台机器提供物品。

<GameScene zoom="6" background="transparent">
  <ImportStructure src="../assets/assemblies/furnace_automation.snbt" />

<BoxAnnotation color="#dddddd" min="1 0 0" max="2 1 1">
        (1) 样板供应器：可使用赛特斯石英扳手调整朝向的变种，其中放入相应的处理样板。

        ![Iron Pattern](../assets/diagrams/furnace_pattern_small.png)
  </BoxAnnotation>

<BoxAnnotation color="#dddddd" min="1 1 0" max="2 1.3 1">
        (2) 接口：使用默认配置。
  </BoxAnnotation>

<BoxAnnotation color="#dddddd" min="1 1 0" max="1.3 2 1">
        (3) 存储总线 #1：过滤为煤炭。
        <ItemImage id="minecraft:coal" scale="2" />
  </BoxAnnotation>

<BoxAnnotation color="#dddddd" min="0 2 0" max="1 2.3 1">
        (4) 存储总线 #2：我使用反转卡将过滤器设置为将煤炭列入黑名单。
        <Row><ItemImage id="minecraft:coal" scale="2" /><ItemImage id="inverter_card" scale="2" /></Row>
  </BoxAnnotation>

<DiamondAnnotation pos="4 0.5 0.5" color="#00ff00">
        连接到主网络
    </DiamondAnnotation>

  <IsometricCamera yaw="195" pitch="30" />
</GameScene>

这是一个向多台机器提供物品的通用示意图

<GameScene zoom="6" background="transparent">
<ImportStructure src="../assets/assemblies/provider_interface_storage.snbt" />

<BoxAnnotation color="#dddddd" min="2.7 0 1" max="3 1 2">
        接口（必须是平的，不能是完整方块）
  </BoxAnnotation>

<BoxAnnotation color="#dddddd" min="1 0 0" max="1.3 1 4">
        存储总线
  </BoxAnnotation>

<BoxAnnotation color="#dddddd" min="0 0 0" max="1 1 4">
        你想要提供样板的地方
  </BoxAnnotation>

<IsometricCamera yaw="185" pitch="30" />
</GameScene>

支持多个具有相同样式的样式供应器，并且它们会并行工作。

样板供应器会尝试将其批处理按顺序循环分配到它的所有面，从而并行使用所有连接的机器。

## 变种

样板供应器有 3 种不同变体：普通、定向和 flat/[subpart](../ae2-mechanics/cable-subparts.md)。这会影响它们会将材料推送到哪些具体侧面、从哪些侧面接收物品，以及向哪些侧面提供网络连接。

* 普通样板供应器会向所有方向推送材料、从所有方向接收输入，并且像大多数 AE2 机器一样，
    会向所有方向提供[网络连接](../ae2-mechanics/me-network-connections.md)，就像线缆一样。

* 定向样板供应器是通过在普通样板供应器上使用 <ItemLink id="certus_quartz_wrench" /> 来改变其
    朝向制成的。它们只会向选定的一侧推送材料，从所有侧面接收输入，并且特别地，不会在所选侧
  提供[网络连接](../ae2-mechanics/me-network-connections.md)。这样一来，如果你想制作子网，它们就可以向 AE2 机器推送物品而不连接网络。

* 平面样板供应器是[线缆子部件](../ae2-mechanics/cable-subparts.md)，因此多个可以放在同一根线缆上，从而实现紧凑布局。
    它们的行为类似于定向样板供应器的选定一侧：提供样板、接收输入，并且**不会**
    在其正面提供[网络连接](../ae2-mechanics/me-network-connections.md)。

样板供应器可以在合成网格中于普通与扁平两种形态之间切换。

## 设置

样板供应器有多种模式：

*   **阻挡模式** 会在机器中已经有材料时，阻止样板供应器推送新一批材料。
*   **锁定合成** 可以在各种红石条件下锁定样板供应器，或一直锁定到上一次合成的结果被插入该特定的样板供应器中。
*   可以在 <ItemLink id="pattern_access_terminal" /> 上显示或隐藏样板供应器。

## 优先级

可以通过点击 GUI 右上角的扳手来设置优先级。在同一种物品存在多个[样板](patterns.md)
的情况下，会优先使用较高优先级的供应器中的样板，而不是较低优先级供应器中的样板，
除非网络没有较高优先级样板所需的材料。

## 一个常见误解

出于某种原因，人们总是在这么做，我不明白为什么，不过我还是把这段写在这里，希望能帮上忙。（也许
人们搞错了，以为 <ItemLink id="export_bus" /> 是物品离开网络的唯一方式，并不知道
样板供应器也会导出物品）

这不会实现你想要的效果。正如在 [cables](cables.md) 中提到的，线缆不是物品管道，它们没有内部容器，提供方不会将物品推入其中。

<GameScene zoom="8" background="transparent">
  <ImportStructure src="../assets/assemblies/provider_misconception_1.snbt" />

  <BoxAnnotation color="#dddddd" min="1 0 3" max="2 1 4">
        不是高炉
  </BoxAnnotation>

  <IsometricCamera yaw="95" pitch="5" />
</GameScene>

由于提供端没有任何可推送的目标，它将无法正常工作。它在这里所做的，仅仅是像一根线缆一样，将 <ItemLink id="export_bus" /> 连接到网络。

供应器也不会以某种方式告诉 <ItemLink id="export_bus" /> 该导出什么，导出总线只会导出你放入其筛选器中的所有东西。

我们在这里本质上做的是这个：

<GameScene zoom="8" background="transparent">
  <ImportStructure src="../assets/assemblies/provider_misconception_2.snbt" />

  <BoxAnnotation color="#dddddd" min="1 0 3" max="2 1 4">
        不是高炉
  </BoxAnnotation>

  <IsometricCamera yaw="95" pitch="5" />
</GameScene>

你真正可能想要制作的其实是这个，在这里，样板提供器可以将其样板中的内容导出到相邻的机器中：

<GameScene zoom="8" background="transparent">
  <ImportStructure src="../assets/assemblies/provider_misconception_3.snbt" />

  <BoxAnnotation color="#dddddd" min="1 0 3" max="2 1 4">
        不是高炉
  </BoxAnnotation>

  <IsometricCamera yaw="95" pitch="5" />
</GameScene>

## 与分子装配室配合使用

<ItemLink id="molecular_assembler" /> 基本上和其他机器没什么两样。它们都有一个可插入物品的容器，随后会对容器中的物品执行操作，然后像许多机器一样，将结果推送到相邻的容器中。因此，它们应当像其他机器一样与供应器配合使用，但有一点额外区别：

组装机可以从直接插入组装机中的 <ItemLink id="crafting_pattern" />、<ItemLink id="smithing_table_pattern" /> 或 <ItemLink id="stonecutting_pattern" />
获取所需的样板。
这在流水线中很有用，但如果每个合成配方都必须专门配一台组装机会很烦人。

因此，样板供应器与组装机配合时具有一项特殊功能：它们可以连同材料一起发送样板数据。
这样一来，你只需在样板供应器旁边放置一台组装机，供应器随后就可以用这台组装机处理其所有的
合成、锻造和切石样板。

其实就是这么简单，只要把样板放进供应器里：

<GameScene zoom="4" background="transparent">
  <ImportStructure src="../assets/assemblies/assembler_tower.snbt" />
  <IsometricCamera yaw="195" pitch="30" />
</GameScene>

*注意，这里恰好有 8 个提供器，这是单个装配器、提供器或非致密线缆所能路由的最大频道数。*

## 配方

<RecipeFor id="pattern_provider" />

<RecipeFor id="cable_pattern_provider" />