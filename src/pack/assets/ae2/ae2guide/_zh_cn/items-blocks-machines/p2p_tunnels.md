---
navigation:
  parent: items-blocks-machines/items-blocks-machines-index.md
  title: P2P通道
  icon: me_p2p_tunnel
  position: 210
categories:
- devices
item_ids:
- ae2:me_p2p_tunnel
- ae2:redstone_p2p_tunnel
- ae2:item_p2p_tunnel
- ae2:fluid_p2p_tunnel
- ae2:fe_p2p_tunnel
- ae2:light_p2p_tunnel
---

# 点对点通道

<GameScene zoom="6" background="transparent">
  <ImportStructure src="../assets/assemblies/p2p_tunnels.snbt" />
  <IsometricCamera yaw="195" pitch="30" />
</GameScene>

P2P通道是一种在网络中传输物品、流体、红石信号、电力、光以及[频道](../ae2-mechanics/channels.md)
等内容的方式，而不会让它们直接与网络交互。P2P通道有许多不同变种，但每一种
都只能传输其特定类型的内容。它们本质上就像直接连接
相距较远的两个方块面的传送门。它们不是双向的，而是有明确的输入端和输出端。

![Portal](../assets/assemblies/p2p_portal.png)

例如，朝向物品 P2P 的漏斗会像直接连接到木桶一样运作，物品会流动。

<GameScene zoom="4" background="transparent">
  <ImportStructure src="../assets/assemblies/p2p_hopper_barrel.snbt" />
  <IsometricCamera yaw="195" pitch="30" />
</GameScene>

不过，两个彼此相邻的木桶不会相互传输物品。

<GameScene zoom="4" background="transparent">
  <ImportStructure src="../assets/assemblies/p2p_barrel_barrel.snbt" />
  <IsometricCamera yaw="195" pitch="30" />
</GameScene>

也有其他变种，例如红石 P2P。

<GameScene zoom="4" background="transparent">
  <ImportStructure src="../assets/assemblies/p2p_redstone.snbt" />
  <IsometricCamera yaw="195" pitch="30" />
</GameScene>

以及会传输频道的 ME P2P。

<GameScene zoom="4" background="transparent">
  <ImportStructure src="../assets/assemblies/p2p_channels.snbt" />
  <IsometricCamera yaw="195" pitch="30" />
</GameScene>

## P2P通道的类型与调谐

<GameScene zoom="6" background="transparent">
  <ImportStructure src="../assets/assemblies/p2p_tunnels.snbt" />
  <IsometricCamera yaw="180" pitch="90" />
</GameScene>

P2P通道有很多种类型。只有 ME P2P通道 可以直接合成，其他类型则需要用特定物品右击其他
P2P通道来制作：
- ME P2P通道 通过手持任意[cable](../items-blocks-machines/cables.md)右击来选择。
- 红石 P2P通道 通过手持各种红石构件右击来选择。
- 物品 P2P通道 通过手持箱子或漏斗右击来选择。
- 流体 P2P通道 通过手持桶或瓶子右击来选择。
- 能源 P2P通道 通过手持几乎任何含有能量的物品右击来选择。
- 光照 P2P通道 通过手持火把或荧石右击来选择。

某些通道类型有一些特殊之处。例如，ME P2P通道的频道不能穿过其他 ME P2P通道，而能源P2P通道会通过提高其[能量](../ae2-mechanics/energy.md)消耗，间接对流经自身的 FE 抽取 2.5% 的“税”。

## 最常用的 P2P 形式

P2P 通道最常见的用途，是使用 ME P2P通道来压缩[channel](../ae2-mechanics/channels.md)传输的通道密度。
你可以用一根致密线缆在各处传输大量通道，而不必铺设成束的致密线缆。

在这个例子中，8 个 ME P2P 输入端从主网络的 <ItemLink id="controller" /> 获取了 256 个通道（8*32），而 8 个 ME P2P 输出端则会
将这些通道输出到别处。注意，每个 P2P 隧道的输入端或输出端都会占用 1 个通道。因此，我们就能让许多通道
通过一根细线缆传输。而且由于我们的 P2P 隧道位于专用的[子网络](../ae2-mechanics/subnetworks.md)上，我们
甚至完全不会占用主网络的任何通道来做到这一点！另外还要注意，虽然 P2P 隧道可以直接放置在
控制器旁边，但也可以在中间放置一根[致密智能线缆](../items-blocks-machines/cables.md#smart-cable)，以便更直观地查看通道情况。

<GameScene zoom="4" interactive={true}>
  <ImportStructure src="../assets/assemblies/p2p_compact_channels.snbt" />

  <BoxAnnotation color="#dddddd" min="1.3 1.3 6.3" max="2 2.7 6.7">
        石英纤维会在主网络与 p2p 子网络之间共享能量。
  </BoxAnnotation>

  <BoxAnnotation color="#dddddd" min="4.1 0 5.7" max="5 2.3 6.4">
        你既可以将通道输入直接放在控制器上，也可以用线缆连接到它。
  </BoxAnnotation>

  <IsometricCamera yaw="225" pitch="30" />
</GameScene>

再举一个例子（包括它与[量子桥](quantum_bridge.md))的配合使用），请看这张我懒得再用 MS Paint 修饰的示意图：

![P2P and quantum bridges](../assets/diagrams/p2p_quantum_network.png)

## 嵌套

但是，你不能用它通过单根线缆传输无限多个频道。ME P2P通道的频道无法通过另一个 ME P2P通道，因此你不能递归地嵌套它们。注意红色线缆上的外层 ME P2P通道处于离线状态。需要注意的是，这只适用于 ME P2P通道，其他类型的 P2P通道可以通过 ME P2P通道传输，正如正常工作的红石 P2P通道所示。

<GameScene zoom="4" background="transparent">
  <ImportStructure src="../assets/assemblies/p2p_nesting.snbt" />
  <IsometricCamera yaw="225" pitch="30" />
</GameScene>

## 链接

<GameScene zoom="6" background="transparent">
  <ImportStructure src="../assets/assemblies/p2p_linking_frequency.snbt" />
  <IsometricCamera yaw="195" pitch="30" />
</GameScene>

P2P通道连接的两端可以使用 <ItemLink id="memory_card" /> 进行链接。链接频率会以 2x2 的颜色阵列显示在通道背面。
- Shift+右键单击以生成新的 P2P链接频率。
- 右键单击以粘贴设置、升级卡或链接频率。

你潜行右键点击的通道将作为输入，直接右键点击的通道将作为输出。你可以拥有多个输出，
但对于 ME P2P通道，流入输入端的频道会在各个输出端之间分配，因此你无法复制频道。

## 配方

<RecipeFor id="me_p2p_tunnel" />