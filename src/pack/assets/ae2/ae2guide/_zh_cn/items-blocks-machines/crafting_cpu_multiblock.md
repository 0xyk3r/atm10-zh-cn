---
navigation:
  parent: items-blocks-machines/items-blocks-machines-index.md
  title: 合成处理器多方块（存储器、并行处理单元、监控器、单元）
  icon: 1k_crafting_storage
  position: 210
categories:
- devices
item_ids:
- ae2:1k_crafting_storage
- ae2:4k_crafting_storage
- ae2:16k_crafting_storage
- ae2:64k_crafting_storage
- ae2:256k_crafting_storage
- ae2:crafting_accelerator
- ae2:crafting_monitor
- ae2:crafting_unit
---

# 合成器CPU

<GameScene zoom="4" background="transparent">
  <ImportStructure src="../assets/assemblies/crafting_cpus.snbt" />
  <IsometricCamera yaw="195" pitch="30" />
</GameScene>

<Row>
  <BlockImage id="1k_crafting_storage" scale="4" />

  <BlockImage id="crafting_accelerator" scale="4" />

  <BlockImage id="crafting_monitor" scale="4" />

  <BlockImage id="crafting_unit" scale="4" />
</Row>

合成CPU用于管理合成请求/任务。在执行包含多个步骤的合成任务时，它们会存储中间材料，并会影响任务的规模上限，以及在一定程度上影响任务完成的速度。更多详情请参见[自动合成](../ae2-mechanics/autocrafting.md)

每个合成器CPU只能处理 1 个请求或任务，因此如果你想同时请求一个运算处理器和 256 个平滑石头，你就需要 2 个 CPU 多方块结构。

它们可以被设置为处理来自玩家、自动化（输出总线和接口）或两者的请求。

右击其中一个会打开合成状态 UI，你可以在其中查看 CPU 正在处理的合成任务进度。

## 设置

CPU 可设置为仅接受玩家、仅接受自动化（例如带有 <ItemLink id="crafting_card" /> 的 <ItemLink id="export_bus" />），或同时接受两者的请求。

## 建造

合成CPU是多方块结构，必须是没有空隙的实心长方体。它们由多个组件构成。

每个 CPU 都必须至少包含 1 个合成存储器方块（实际上，最小可用的 CPU 其实就只是一个 1k合成存储器）。

# 合成单元

<BlockImage id="crafting_unit" scale="4" />

（可选）如果你的 CPU 中其他组件数量不足，合成单元只是用来填充空间，使其成为一个完整的长方体。它们也是其他组件的基础材料。

<RecipeFor id="crafting_unit" />

# 合成存储

<Row>
  <BlockImage id="1k_crafting_storage" scale="4" />

  <BlockImage id="4k_crafting_storage" scale="4" />

  <BlockImage id="16k_crafting_storage" scale="4" />

  <BlockImage id="64k_crafting_storage" scale="4" />

  <BlockImage id="256k_crafting_storage" scale="4" />
</Row>

（必需）合成存储器提供所有标准存储元件容量规格（1k、4k、16k、64k、256k）。它们用于存储参与合成的材料和中间材料，因此如果要让 CPU 处理包含更多材料的合成任务，就需要更大容量或更多的存储器。

<Column>
  <Row>
    <RecipeFor id="1k_crafting_storage" />

    <RecipeFor id="4k_crafting_storage" />

    <RecipeFor id="16k_crafting_storage" />
  </Row>

  <Row>
    <RecipeFor id="64k_crafting_storage" />

    <RecipeFor id="256k_crafting_storage" />
  </Row>
</Column>

# 并行处理单元

<BlockImage id="crafting_accelerator" scale="4" />

（可选）合成协处理器可以让系统更频繁地从 <ItemLink id="pattern_provider" /> 发出材料批次，
因为它会让 CPU tick 得更快。
这使其能够跟上处理速度很快的机器。例如，一个被 <ItemLink id="molecular_assembler" /> 环绕的样板供应器
能够比单个装配器更快地推送材料，
从而将这些材料批次分配给周围的装配器。

有些复杂的配方包含多个可以并行完成的步骤，例如为了制作书架，同时制作木板和书。

在合成状态界面中（可通过右键单击 CPU，或点击[终端](terminals.md))中的锤子图标打开），这些步骤都会显示为“计划合成”。每增加一个并行处理单元，就可以多并行执行其中一个步骤（因此会显示为“合成中”）。

不过，这一点其实没那么重要，因为相比配方中理论上可以并行完成的步骤数，你通常更需要更多并行处理单元来提升插入速度。

<RecipeFor id="crafting_accelerator" />

# 合成监视器

<BlockImage id="crafting_monitor" scale="4" />

（可选）合成监控器会显示 CPU 当前正在处理的任务。
可以使用 <ItemLink id="color_applicator" /> 为屏幕染色。

<RecipeFor id="crafting_monitor" />