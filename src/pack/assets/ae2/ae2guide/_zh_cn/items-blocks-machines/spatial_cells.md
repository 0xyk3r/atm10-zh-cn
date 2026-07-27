---
navigation:
  parent: items-blocks-machines/items-blocks-machines-index.md
  title: 空间单元
  icon: spatial_storage_cell_128
  position: 410
categories:
- tools
item_ids:
- ae2:spatial_storage_cell_2
- ae2:spatial_storage_cell_16
- ae2:spatial_storage_cell_128
- ae2:spatial_cell_component_2
- ae2:spatial_cell_component_16
- ae2:spatial_cell_component_128
---

# 空间存储元

  <Row>
    <ItemImage id="spatial_storage_cell_2" scale="4" />

    <ItemImage id="spatial_storage_cell_16" scale="4" />

    <ItemImage id="spatial_storage_cell_128" scale="4" />
  </Row>

空间存储元用于[存储物理空间体积](../ae2-mechanics/spatial-io.md)。
它们会用在 <ItemLink id="spatial_io_port" /> 中。

与[存储单元](../items-blocks-machines/storage_cells.md)不同，空间存储元无法重新格式化。

再次强调，**空间存储元件一旦使用过，就无法重置、重新格式化或调整大小。** 如果你想使用不同的尺寸，请制作一个新的存储元件。


## 配方

  <Row>
    <Recipe id="network/cells/spatial_storage_cell_2_cubed_storage" />

    <Recipe id="network/cells/spatial_storage_cell_16_cubed_storage" />

    <Recipe id="network/cells/spatial_storage_cell_128_cubed_storage" />
  </Row>

# 外壳

单元可以用一个空间组件和一个外壳制作，也可以使用以空间组件为中心的外壳配方来制作：

<Row>
  <Recipe id="network/cells/spatial_storage_cell_2_cubed" />

  <Recipe id="network/cells/spatial_storage_cell_2_cubed_storage" />
</Row>

外壳本身的合成方式如下：

  <RecipeFor id="item_cell_housing" />

# 空间组件

空间组件是空间存储元的核心。每个等级都会使可
存储体积的尺寸增加 8 倍。

  <Row>
    <RecipeFor id="spatial_cell_component_2" />

    <RecipeFor id="spatial_cell_component_16" />

    <RecipeFor id="spatial_cell_component_128" />
  </Row>