---
navigation:
  parent: items-blocks-machines/items-blocks-machines-index.md
  title: 线缆
  icon: fluix_glass_cable
  position: 110
categories:
- network infrastructure
item_ids:
- ae2:white_glass_cable
- ae2:orange_glass_cable
- ae2:magenta_glass_cable
- ae2:light_blue_glass_cable
- ae2:yellow_glass_cable
- ae2:lime_glass_cable
- ae2:pink_glass_cable
- ae2:gray_glass_cable
- ae2:light_gray_glass_cable
- ae2:cyan_glass_cable
- ae2:purple_glass_cable
- ae2:blue_glass_cable
- ae2:brown_glass_cable
- ae2:green_glass_cable
- ae2:red_glass_cable
- ae2:black_glass_cable
- ae2:fluix_glass_cable
- ae2:white_covered_cable
- ae2:orange_covered_cable
- ae2:magenta_covered_cable
- ae2:light_blue_covered_cable
- ae2:yellow_covered_cable
- ae2:lime_covered_cable
- ae2:pink_covered_cable
- ae2:gray_covered_cable
- ae2:light_gray_covered_cable
- ae2:cyan_covered_cable
- ae2:purple_covered_cable
- ae2:blue_covered_cable
- ae2:brown_covered_cable
- ae2:green_covered_cable
- ae2:red_covered_cable
- ae2:black_covered_cable
- ae2:fluix_covered_cable
- ae2:white_covered_dense_cable
- ae2:orange_covered_dense_cable
- ae2:magenta_covered_dense_cable
- ae2:light_blue_covered_dense_cable
- ae2:yellow_covered_dense_cable
- ae2:lime_covered_dense_cable
- ae2:pink_covered_dense_cable
- ae2:gray_covered_dense_cable
- ae2:light_gray_covered_dense_cable
- ae2:cyan_covered_dense_cable
- ae2:purple_covered_dense_cable
- ae2:blue_covered_dense_cable
- ae2:brown_covered_dense_cable
- ae2:green_covered_dense_cable
- ae2:red_covered_dense_cable
- ae2:black_covered_dense_cable
- ae2:fluix_covered_dense_cable
- ae2:white_smart_cable
- ae2:orange_smart_cable
- ae2:magenta_smart_cable
- ae2:light_blue_smart_cable
- ae2:yellow_smart_cable
- ae2:lime_smart_cable
- ae2:pink_smart_cable
- ae2:gray_smart_cable
- ae2:light_gray_smart_cable
- ae2:cyan_smart_cable
- ae2:purple_smart_cable
- ae2:blue_smart_cable
- ae2:brown_smart_cable
- ae2:green_smart_cable
- ae2:red_smart_cable
- ae2:black_smart_cable
- ae2:fluix_smart_cable
- ae2:white_smart_dense_cable
- ae2:orange_smart_dense_cable
- ae2:magenta_smart_dense_cable
- ae2:light_blue_smart_dense_cable
- ae2:yellow_smart_dense_cable
- ae2:lime_smart_dense_cable
- ae2:pink_smart_dense_cable
- ae2:gray_smart_dense_cable
- ae2:light_gray_smart_dense_cable
- ae2:cyan_smart_dense_cable
- ae2:purple_smart_dense_cable
- ae2:blue_smart_dense_cable
- ae2:brown_smart_dense_cable
- ae2:green_smart_dense_cable
- ae2:red_smart_dense_cable
- ae2:black_smart_dense_cable
- ae2:fluix_smart_dense_cable
---

# 电缆

<GameScene zoom="3" background="transparent">
  <ImportStructure src="../assets/assemblies/cables.snbt" />
  <IsometricCamera yaw="180" pitch="30" />
</GameScene>

虽然相邻的支持 ME 的机器也能形成 ME网络，但线缆是在更大范围内
扩展 ME网络的主要方式。

不同颜色的线缆可用于确保相邻的线缆彼此不会连接，
从而让 [channels](../ae2-mechanics/channels.md) 的分配更加高效。它们还会影响与其连接的终端的颜色，
这样你的终端就不必全都是紫色了。福鲁伊克斯色线缆可以连接到所有其他颜色。

需要注意的是，**频道与线缆颜色毫无关系**

## 重要说明

**如果你刚接触应用能源且不熟悉频道，请尽可能使用智能线缆和致密智能线缆。
它会显示频道是如何通过你的网络进行布线的，让它们的行为更容易理解。**

## 另一条说明

**这些不是物品、流体、能量等管道。** 它们没有内部容器，样板供应器和机器也不会向其中“推送”内容，它们唯一的作用就是将应用能源 ME设备](../ae2-mechanics/devices.md)连接成一个网络。

## 玻璃电缆

<GameScene zoom="6" background="transparent">
<ImportStructure src="../assets/assemblies/fluix_glass_cable.snbt" />
<IsometricCamera yaw="195" pitch="30" />
</GameScene>

<ItemLink id="fluix_glass_cable" /> 是最基础的线缆，能够传输能量
以及最多 8 个[信道](../ae2-mechanics/channels.md)。它有 17 种不同颜色，默认颜色
为福鲁伊克斯，也可以使用 16 种染料中的任意一种将其染成对应颜色。

要制作有色线缆，将任意一种染料放在中间，周围放上 8 个相同类型的线缆即可
（线缆的颜色无关紧要，但它们必须是同一种类型，
例如玻璃、智能等）。你也可以在世界中使用任意与 Forge 兼容的画笔为线缆上色。

你可以将任意彩色线缆与一桶水合成以去除染色。

你可以用羊毛包覆电缆来制作 <ItemLink id="fluix_covered_cable" />，并合成 <ItemLink id="fluix_smart_cable" />，以便更好地了解你的
[频道](../ae2-mechanics/channels.md) 的情况。

<RecipeFor id="fluix_glass_cable" />

<RecipeFor id="blue_glass_cable" />

## 包层电缆

<GameScene zoom="6" background="transparent">
  <ImportStructure src="../assets/assemblies/fluix_covered_cable.snbt" />
  <IsometricCamera yaw="195" pitch="30" />
</GameScene>

包覆线缆变种相比其 <ItemLink id="fluix_glass_cable" /> 对应版本没有任何玩法上的优势。不过，如果你更喜欢包覆外观，它也可以作为另一种美观选择。

可以像 <ItemLink id="fluix_glass_cable" /> 一样进行染色。四个 <ItemLink id="fluix_covered_cable" /> 可与红石和萤石合成，制成 <ItemLink id="fluix_covered_dense_cable" />。

<Recipe id="network/cables/covered_fluix" />

<RecipeFor id="blue_covered_cable" />

## 致密电缆

<GameScene zoom="6" background="transparent">
  <ImportStructure src="../assets/assemblies/fluix_covered_dense_cable.snbt" />
  <IsometricCamera yaw="195" pitch="30" />
</GameScene>

高容量电缆，可传输 32 个频道，而标准电缆只能传输 8 个。
不过它不支持总线，因此在使用总线或
面板之前，你必须先将稠密电缆降级为更小的电缆
（例如 <ItemLink id="fluix_glass_cable" /> 或 <ItemLink id="fluix_smart_cable" />）。

致密线缆会在一定程度上覆盖频道的“最短路径”行为，频道会先沿最短路径到达致密线缆，然后再经由该致密线缆沿最短路径连接到控制器。

<Recipe id="network/cables/dense_covered_fluix" />

<RecipeFor id="blue_covered_dense_cable" />

## 智能电缆

<Row>
<GameScene zoom="6" background="transparent">
  <ImportStructure src="../assets/assemblies/fluix_smart_cable.snbt" />
  <IsometricCamera yaw="195" pitch="30" />
</GameScene>
<GameScene zoom="6" background="transparent">
  <ImportStructure src="../assets/assemblies/fluix_smart_dense_cable.snbt" />
  <IsometricCamera yaw="195" pitch="30" />
</GameScene>
</Row>

虽然它们在外观上与 <ItemLink id="fluix_covered_cable" /> 有些相似，但其提供了诊断功能：通过将线缆上的频道使用情况可视化来实现。频道会显示为沿着线缆黑色条纹延伸的发光彩色线条，让你了解网络中的频道是如何被使用的。对于普通智能线缆，前四个频道会显示为与线缆颜色相同的线条，后四个则显示为白色线条。对于致密智能线缆，每一条纹代表 4 个频道。

在带有 <ItemLink id="controller" /> 的网络中，电缆上的线条会显示信道经过的确切路径。

临时网络中的智能线缆将改为显示整个网络中正在使用的频道数量，而不是流经该特定线缆的频道数量。

这些也可以用与 <ItemLink id="fluix_glass_cable" /> 相同的方式染色。

<Recipe id="network/cables/smart_fluix" />

<Recipe id="network/cables/dense_smart_fluix" />

<RecipeFor id="blue_smart_cable" />