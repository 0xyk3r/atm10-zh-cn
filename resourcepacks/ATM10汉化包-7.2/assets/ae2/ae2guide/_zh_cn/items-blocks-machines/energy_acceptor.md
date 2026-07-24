---
navigation:
  parent: items-blocks-machines/items-blocks-machines-index.md
  title: 能源接收器
  icon: energy_acceptor
  position: 110
categories:
- network infrastructure
item_ids:
- ae2:energy_acceptor
---

# 能源接收器

<Row gap="20">
<BlockImage id="energy_acceptor" scale="8" /> 

<GameScene zoom="8" background="transparent">
  <ImportStructure src="../assets/blocks/cable_energy_acceptor.snbt" />
</GameScene>
</Row>

能源接收器可以将来自其他科技模组的常见能量形式转换为 AE2 的内部[能源](../ae2-mechanics/energy.md)，
即 AE。虽然 <ItemLink id="controller" /> 也能做到这一点，但控制器的表面很宝贵，因此通常最好改用能源接收器。

Forge 能量与 Techreborn 能量的转换比例如下

*   2 FE 等于 1 AE (Forge)
*   1 E 等于 2 AE (Fabric)

转化速度完全取决于你的网络能存储多少 AE，原因会在
[这一页](../ae2-mechanics/energy.md)上说明。

## 变种

能源接收器有 2 种不同的变体：普通和 flat/[subpart](../ae2-mechanics/cable-subparts.md)。这让你可以将一些装置布置得更加紧凑。

能量接收器可以在合成网格中于普通与扁平两种形态之间切换。

## 配方

<RecipeFor id="energy_acceptor" />

<RecipeFor id="cable_energy_acceptor" />