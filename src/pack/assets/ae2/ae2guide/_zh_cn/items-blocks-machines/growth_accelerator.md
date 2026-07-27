---
navigation:
  parent: items-blocks-machines/items-blocks-machines-index.md
  title: 生长加速
  icon: growth_accelerator
  position: 310
categories:
- machines
item_ids:
- ae2:growth_accelerator
---

# 生长加速器

<BlockImage id="growth_accelerator" p:powered="true" scale="8"/>

生长加速会在放置于母岩旁边时，大幅加快[](../ae2-mechanics/certus-growth.md)赛特斯或紫水晶的生长。

有趣的是，它*也*可以加速各种植物的生长。

它的工作方式是对相邻方块施加“随机刻”，并叠加在自然发生的随机刻之上。
理论上这意味着 1 个加速器应当能让物品生长速度达到平常的约 90 倍，而且该效果可线性叠加。

<GameScene zoom="6" interactive={true}>
  <ImportStructure src="../assets/assemblies/growth_accelerator.snbt" />
  <IsometricCamera yaw="195" pitch="30" />
</GameScene>

能量可以从顶部或底部输入，既可以通过 AE2 的[线缆](cables.md)，也可以通过其他模组的电力线缆。它
既可接受 AE2 的能量（AE），也可接受 Forge 能量（FE）。

要手动为其供能，请在顶部或底部放置一个 <ItemLink id="crank" />，然后右键它。

顶部和底部可以通过其上的粉色通量装饰细节来辨认。

<GameScene zoom="6" background="transparent">
<ImportStructure src="../assets/assemblies/accelerator_connections.snbt" />
<IsometricCamera yaw="195" pitch="30" />
</GameScene>

## 配方

<RecipeFor id="growth_accelerator" />