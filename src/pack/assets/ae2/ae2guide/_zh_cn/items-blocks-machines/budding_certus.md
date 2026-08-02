---
navigation:
  parent: items-blocks-machines/items-blocks-machines-index.md
  title: 赛特斯石英母岩
  icon: flawless_budding_quartz
  position: 8
categories:
- misc ingredients blocks
item_ids:
- ae2:flawless_budding_quartz
- ae2:flawed_budding_quartz
- ae2:chipped_budding_quartz
- ae2:damaged_budding_quartz
- ae2:small_quartz_bud
- ae2:medium_quartz_bud
- ae2:large_quartz_bud
- ae2:quartz_cluster
---

# 赛特斯石英母岩

（另见[赛特斯生长](../ae2-mechanics/certus-growth.md)）

<GameScene zoom="4" background="transparent">
  <ImportStructure src="../assets/assemblies/budding_blocks.snbt" />
  <IsometricCamera yaw="195" pitch="30" />
</GameScene>

赛特斯石英芽会从赛特斯石英母岩中长出，类似于紫水晶。这些可在[陨石](../ae2-mechanics/meteorites.md)中找到。
赛特斯石英母岩共有 4 个等级：无瑕、有瑕、开裂和损坏。最简单的辨认方式
是搭配 HWYLA、Jade、The One Probe 之类的模组使用（或查看 f3 界面）

对于有瑕、开裂和损坏的赛特斯石英母岩，每当晶芽生长到下一阶段时，母岩方块都有概率降级一个等级，最终变成普通的 <ItemLink id="quartz_block" />。

无瑕的赛特斯石英母岩在生长晶芽时不会退化，并且可作为无限来源。

如果用普通镐破坏，赛特斯石英母岩方块会降级 1 个品阶。如果使用附有精准采集魔咒的镐破坏，它们就不会降级，除非它们原本是无瑕的。**这意味着无瑕的赛特斯石英母岩方块无法用镐拾取并移动**。不过，可以使用[封闭空间](../ae2-mechanics/spatial-io.md)来剪切并粘贴这些无瑕的母岩方块。

## 配方

有瑕的、开裂的和损坏的赛特斯石英母岩，可以通过将前一等级的母岩（或一个 <ItemLink id="quartz_block" />）与一个或多个 <ItemLink id="charged_certus_quartz_crystal" /> 一起丢入水中来合成。

无瑕的赛特斯晶簇无法合成，只能在世界中找到。

<Row>
  <RecipeFor id="damaged_budding_quartz" />

  <RecipeFor id="chipped_budding_quartz" />

  <RecipeFor id="flawed_budding_quartz" />
</Row>