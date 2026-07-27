---
navigation:
  parent: ae2-mechanics/ae2-mechanics-index.md
  title: 空间IO
  icon: spatial_storage_cell_2
---

# 空间IO

<GameScene zoom="6" interactive={true}>
  <ImportStructure src="../assets/assemblies/spatial_storage_1x1x1.snbt" />

  <BoxAnnotation color="#33dd33" min="1 1 1" max="2 2 2">
        将要移动的体积
  </BoxAnnotation>

  <IsometricCamera yaw="195" pitch="30" />

</GameScene>

空间IO是一种在你的世界中剪切并粘贴物理空间体积的方法。它可以用来移动 <ItemLink id="flawless_budding_quartz" />，
在你的基地中建造一个房间，通过替换各种内部结构来将其用于不同用途，甚至还能移动末地传送门！

它的工作原理是将设定体积与空间存储维度中一个大小相同的体积进行*交换*，把塔阵列中的内容送入空间存储维度，再把该维度中的内容送回塔阵列。

这意味着，如果你有办法在维度之间移动（空间 IO *可以* 用来制作一台传送机，但实现起来非常复杂、有点别扭，而且超出了本指南的范围），你就可以把它们当作自定义大小的压缩空间机械或口袋维度来使用。

# 多方块结构搭建

空间 IO 需要其组件按特定方式排列才能运行，并定义要被剪切并粘贴的体积。

所有组件必须位于同一[网络](me-network-connections.md)上才能运行，并且一个网络上只能有一套空间IO装置。因此，建议使用[子网络](subnetworks.md)。

## 空间IO端口

<BlockImage id="spatial_io_port" p:powered="true" scale="4" />

<ItemLink id="spatial_io_port" /> 用于控制空间 IO 操作。它会显示多方块结构的搭建状态，并容纳
[空间元件](../items-blocks-machines/spatial_cells.md)

它会显示
- 网络中已存储的和最大[能量](energy.md)
- 执行操作所需的能量。这个数值可能相当大，并且会瞬间消耗，因此请确保你有足够的
  [能量单元](../items-blocks-machines/energy_cells.md)来容纳这些能量。
- 塔柱阵列的效率
- 已定义区域的大小

要执行一次空间 IO 操作，请将一个空间存储元放入输入槽，并向空间IO端口提供一个红石脉冲。

随后，它会将传送晶塔中的区域与空间存储维度中的区域进行*交换*。这意味着，如果你先将一组方块发送到空间存储维度，*然后再在传送晶塔内放置另一组方块*，接着把空间存储元放回输入槽，并再次触发 IO 端口，那么第二组方块会消失，而第一组方块会重新出现。

**小心，定义体积内的任何实体，包括你自己，都会被一并带走；如果你没有脱身的方法，你就会被困在空间存储维度中一个黑暗、毫无特征的盒子里。** 用这个来捉弄你的朋友吧！

## 空间塔

<BlockImage id="spatial_pylon" p:powered_on="true" scale="4" />

<ItemLink id="spatial_pylon" /> 是空间 IO 装置的主要组成部分，并定义了会受影响的体积。

该体积由传送晶塔外侧的边界框定义，并在所有方向上向内收缩 1 个方块。

规则如下：
- 最小尺寸为 3x3x3（定义一个 1x1x1 的体积）
- 所有空间塔都必须位于外部边界框内
- 所有空间塔都必须在同一网络上
- 所有空间塔的长度都必须至少为 2 格

例如，假设你想定义一个 3x3x3 的区域。根据规则 2，所有塔柱都必须位于你要定义的区域外围的 5x5x5 外壳内。它们几乎可以采用任意布局，只要都包含在这个厚度为 1 格的 5x5x5 外壳内即可。

<GameScene zoom="4" interactive={true}>
<ImportStructure src="../assets/assemblies/spatial_storage_3x3x3_pylon_demonstration.snbt" />

<BoxAnnotation color="#33dd33" min="1 1 1" max="4 4 4">
        将要移动的体积
  </BoxAnnotation>

<BoxAnnotation color="#3333ff" min="5 5 0" max="0 0 5">
  </BoxAnnotation>

<IsometricCamera yaw="195" pitch="30" />
</GameScene>

一个更合理的搭建是这样的：

<GameScene zoom="4" interactive={true}>
<ImportStructure src="../assets/assemblies/better_spatial_storage_3x3x3.snbt" />

<BoxAnnotation color="#33dd33" min="1 1 1" max="4 4 4">
        将要移动的体积
  </BoxAnnotation>

<BoxAnnotation color="#3333ff" min="5 5 0" max="0 0 5">
  </BoxAnnotation>

<IsometricCamera yaw="195" pitch="30" />
</GameScene>

## 效率

晶塔阵列的效率取决于你填充外壳的程度。围绕大体积区域搭建的最小化配置效率会非常低，甚至可能需要 *数十亿* AE。

## 存储元尺寸

一旦[空间存储元件](../items-blocks-machines/spatial_cells.md)被使用过，它就会获得一组永久定义的 XYZ 尺寸（例如 3x4x2），
并与空间存储维度中的一片空间体积绑定。**空间存储元件一旦使用，
你就无法重置、重新格式化或调整其大小。** 如果你想使用不同的尺寸，请制作一个新的元件。

这些并不是单元名称中所表示的相同尺寸，一个 16^3 单元的尺寸可以是*不超过* 16x16x16 的任意大小

请注意，该体积具有方向性，无法旋转。2x2x3 的体积与 3x2x2 的体积并不相同，尽管它们的大小相同。

如果电芯的 XYZ 尺寸与设定的体积（可在 IO端口中查看）不匹配，IO端口将无法运作。