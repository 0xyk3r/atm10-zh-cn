---
navigation:
  parent: items-blocks-machines/items-blocks-machines-index.md
  title: 能量单元
  icon: energy_cell
  position: 110
categories:
- network infrastructure
item_ids:
- ae2:energy_cell
- ae2:dense_energy_cell
- ae2:creative_energy_cell
---

# 能量单元

<Row gap="20">
  <BlockImage id="energy_cell" scale="8" p:fullness="4" />

  <BlockImage id="dense_energy_cell" scale="8" p:fullness="4" />

  <BlockImage id="creative_energy_cell" scale="8" />
</Row>

能量单元可为网络提供更多的[能量](../ae2-mechanics/energy.md)存储。一些内部能量缓存有助于平滑大量物品插入或提取时出现的能量消耗尖峰，而更大的能量存储则可让网络在没有发电时继续运行（例如夜晚使用太阳能板时），或应对[空间塔](../ae2-mechanics/spatial-io.md)产生的瞬时巨量能量消耗。

## 填充栏杆

<Row>
<BlockImage id="energy_cell" scale="4" p:fullness="0" />
<BlockImage id="energy_cell" scale="4" p:fullness="1" />
<BlockImage id="energy_cell" scale="4" p:fullness="2" />
<BlockImage id="energy_cell" scale="4" p:fullness="3" />
<BlockImage id="energy_cell" scale="4" p:fullness="4" />
</Row>

存储元侧面的条形指示对应其所拥有的能量。

*   电量低于 25% 时为 0
*   电量在 25% 到 50% 之间时为 1
*   电量在 50% 到 75% 之间时为 2
*   电量在 75% 到 99% 之间时为 3
*   电量高于 99% 时为 4

## 存储元类型

*   <ItemLink id="energy_cell" /> 可存储 200k AE，仅一个就足以满足大多数用途，能够轻松应对普通网络使用时的电力波动。
*   <ItemLink id="dense_energy_cell" /> 可存储 1.6M AE，适用于你想让网络依靠储存的电力运行时，或者应对大型[封闭空间](../ae2-mechanics/spatial-io.md)配置所带来的巨量瞬时能量消耗。
*   <ItemLink id="creative_energy_cell" /> 是一个用于测试的创造模式物品，能够提供无限的抛瓦啊啊啊之类的。

## 配方

<Row>
  <RecipeFor id="energy_cell" />

  <RecipeFor id="dense_energy_cell" />
</Row>