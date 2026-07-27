---
navigation:
  parent: items-blocks-machines/items-blocks-machines-index.md
  title: 存储单元
  icon: item_storage_cell_1k
  position: 410
categories:
- tools
item_ids:
- ae2:item_cell_housing
- ae2:fluid_cell_housing
- ae2:cell_component_1k
- ae2:cell_component_4k
- ae2:cell_component_16k
- ae2:cell_component_64k
- ae2:cell_component_256k
- ae2:item_storage_cell_1k
- ae2:item_storage_cell_4k
- ae2:item_storage_cell_16k
- ae2:item_storage_cell_64k
- ae2:item_storage_cell_256k
- ae2:fluid_storage_cell_1k
- ae2:fluid_storage_cell_4k
- ae2:fluid_storage_cell_16k
- ae2:fluid_storage_cell_64k
- ae2:fluid_storage_cell_256k
---

# 存储单元

<Column>
  <Row>
    <ItemImage id="item_storage_cell_1k" scale="4" />

    <ItemImage id="item_storage_cell_4k" scale="4" />

    <ItemImage id="item_storage_cell_16k" scale="4" />

    <ItemImage id="item_storage_cell_64k" scale="4" />

    <ItemImage id="item_storage_cell_256k" scale="4" />
  </Row>

  <Row>
    <ItemImage id="fluid_storage_cell_1k" scale="4" />

    <ItemImage id="fluid_storage_cell_4k" scale="4" />

    <ItemImage id="fluid_storage_cell_16k" scale="4" />

    <ItemImage id="fluid_storage_cell_64k" scale="4" />

    <ItemImage id="fluid_storage_cell_256k" scale="4" />
  </Row>
</Column>

存储单元是应用能源中主要的存储方式之一。它们可放入 <ItemLink id="drive" /> 或 <ItemLink id="chest" /> 中。

关于它们以字节和类型表示的容量说明，请参见[字节与类型](../ae2-mechanics/bytes-and-types.md)。

如果电芯是空的，手持该电芯并潜行右击，即可将存储组件从外壳中取出。

<Row>
    <Recipe id="upgrade/item_storage_cell_1k_to_4k" />

    你可以在合成网格中将存储元件与更高等级的存储组件组合，从而将其升级到更高阶。其内容会被保留，并且低阶组件会被返还。
</Row>

## 不同类型数量下的存储容量

[类型](../ae2-mechanics/bytes-and-types.md)的前期成本决定了，只存储 1 种类型的存储元件，其容量可以达到 63 种类型全部占用的存储元件的 2 倍。

| 存储元件                                     | 使用 1 种类型时的总容量 | 使用 63 种类型时的总容量 |
| ---------------------------------------- | ----------------------------------------: | ------------------------------------------: |
| <ItemLink id="item_storage_cell_1k" />   |                                     8,128 |                                       4,160 |
| <ItemLink id="item_storage_cell_4k" />   |                                    32,512 |                                      16,640 |
| <ItemLink id="item_storage_cell_16k" />  |                                   130,048 |                                      66,560 |
| <ItemLink id="item_storage_cell_64k" />  |                                   520,192 |                                     266,240 |
| <ItemLink id="item_storage_cell_256k" /> |                                 2,080,768 |                                   1,064,960 |


## 分区

单元可以设置过滤器，使其只接受特定物品，类似于 <ItemLink id="storage_bus" />ses 也可以被过滤。这是在 <ItemLink id="cell_workbench" /> 中完成的。

即使你实际上并没有该物品，也可以从 JEI/REI 将物品拖入这些槽位中。

## 升级

存储元支持以下[升级](upgrade_cards.md)，通过 <ItemLink id="cell_workbench" /> 插入：

*   <ItemLink id="fuzzy_card" />（流体单元上不可用）可让元件按耐久等级分区，和/或忽略物品NBT
*   <ItemLink id="inverter_card" /> 可将过滤器从白名单切换为黑名单
*   <ItemLink id="equal_distribution_card" /> 会为每种类型分配相同数量的元件字节空间，因此某一种类型无法占满整个元件
*   <ItemLink id="void_card" /> 会在元件已满时清空插入的物品（如果使用了均分卡，则是在该特定类型分配的空间已满时），可用于防止农场产物堆积堵塞。请务必先对此进行分区！
*   便携元件可以安装 <ItemLink id="energy_card" /> 来提高其电池容量

## 染色

便携式物品元件和流体元件可以像皮革套装一样染色，只需将它们与染料一起合成即可。

# 外壳

单元可以用一个存储组件和一个外壳来制作，也可以将存储组件放在外壳的配方中进行合成：

<Row>
  <Recipe id="network/cells/item_storage_cell_1k" />

  <Recipe id="network/cells/item_storage_cell_1k_storage" />
</Row>

外壳本身的合成方式如下：

<Row>
  <RecipeFor id="item_cell_housing" />

  <RecipeFor id="fluid_cell_housing" />
</Row>

# 存储组件

存储组件是所有 AE2 存储元件的核心，用于决定存储元件的容量。每提升一个等级，容量都会增加 4 倍，并需要消耗 3 个前一等级的存储组件。

<Column>
  <Row>
    <RecipeFor id="cell_component_1k" />

    <RecipeFor id="cell_component_4k" />

    <RecipeFor id="cell_component_16k" />
  </Row>

  <Row>
    <RecipeFor id="cell_component_64k" />

    <RecipeFor id="cell_component_256k" />
  </Row>
</Column>

# 物品存储单元

物品存储元件最多可容纳 63 种不同类型的物品，并提供所有标准容量版本。

<Column>
  <Row>
    <Recipe id="network/cells/item_storage_cell_1k_storage" />

    <Recipe id="network/cells/item_storage_cell_4k_storage" />

    <Recipe id="network/cells/item_storage_cell_16k_storage" />
  </Row>

  <Row>
    <Recipe id="network/cells/item_storage_cell_64k_storage" />

    <Recipe id="network/cells/item_storage_cell_256k_storage" />
  </Row>
</Column>

## 便携物品存储

它们就像你口袋里的迷你 <ItemLink id="chest" />，或者说是一种背包。它们可以在 <ItemLink id="charger" /> 中充电

与标准存储单元不同，这些存储单元的字节容量越高，类型容量反而会*降低*，并且其总字节容量只有一半。

除了所有元件都可接受的升级卡外，它们还可以接受 <ItemLink id="energy_card" />，以升级其内部电池。

<Column>
  <Row>
    <RecipeFor id="portable_item_cell_1k" />

    <RecipeFor id="portable_item_cell_4k" />

    <RecipeFor id="portable_item_cell_16k" />
  </Row>

  <Row>
    <RecipeFor id="portable_item_cell_64k" />

    <RecipeFor id="portable_item_cell_256k" />
  </Row>
</Column>

# 流体存储单元

流体存储元件最多可容纳 5 种不同类型的流体，并且提供所有标准容量可选。

<Column>
  <Row>
    <Recipe id="network/cells/fluid_storage_cell_1k_storage" />

    <Recipe id="network/cells/fluid_storage_cell_4k_storage" />

    <Recipe id="network/cells/fluid_storage_cell_16k_storage" />
  </Row>

  <Row>
    <Recipe id="network/cells/fluid_storage_cell_64k_storage" />

    <Recipe id="network/cells/fluid_storage_cell_256k_storage" />
  </Row>
</Column>

## 便携流体储存

它们就像你口袋里的迷你 <ItemLink id="chest" />，或者说是一种背包。它们可以在 <ItemLink id="charger" /> 中充电

与标准存储单元不同，这些存储单元的字节容量越高，类型容量反而会*降低*，并且其总字节容量只有一半。

除了所有元件都可接受的升级卡外，它们还可以接受 <ItemLink id="energy_card" />，以升级其内部电池。

<Column>
  <Row>
    <RecipeFor id="portable_fluid_cell_1k" />

    <RecipeFor id="portable_fluid_cell_4k" />

    <RecipeFor id="portable_fluid_cell_16k" />
  </Row>

  <Row>
    <RecipeFor id="portable_fluid_cell_64k" />

    <RecipeFor id="portable_fluid_cell_256k" />
  </Row>
</Column>

# 创造模式存储单元

<Row>
  <ItemImage id="creative_storage_cell" scale="2" />
</Row>

创造元件**不会提供无限存储空间**。相反，它们会作为你对其进行[分区](cell_workbench.md)的任意物品或流体的无限来源与无限汇。