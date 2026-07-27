---
navigation:
  parent: ae2-mechanics/ae2-mechanics-index.md
  title: 能量
  icon: energy_cell
---

# 能量

你的网络需要能量才能运行。网络拥有一个能量池，[devices](../ae2-mechanics/devices.md) 会直接从中提取能量，而
<ItemLink id="vibration_chamber" />、<ItemLink id="energy_acceptor" />（以及 <ItemLink id="controller" />）则会向其中添加能量。你可以
通过手持 <ItemLink id="network_tool" /> 右键点击网络中的任意位置来查看网络的能量统计信息，或者
在网络有控制器的情况下，右键点击网络控制器来查看。这种覆盖整个网络的存储与分配方式意味着
不存在能量传输速率限制，因此设备可以提取任意高数量的能量，而
能量接收器也能以实际上无限的速度接收能量，唯一的限制就是你的能量存储量。

## 能量接收

<Row>
  <BlockImage id="energy_acceptor" scale="4" />

  <GameScene zoom="4" background="transparent">
  <ImportStructure src="../assets/blocks/cable_energy_acceptor.snbt" />
  </GameScene>

  <BlockImage id="controller" p:state="online" scale="4" />

  <BlockImage id="vibration_chamber" p:active="true" scale="4" />
  
  <BlockImage id="crystal_resonance_generator" scale="4" />
</Row>

AE2 内部不使用 Forge Energy（在 Forge 上）或 TechReborn Energy（在 Fabric 上）。
相反，它会将它们转换为自己的单位 AE。这个转换是单向的。能量可通过 <ItemLink id="energy_acceptor" /> 和
<ItemLink id="controller" /> 进行转换，不过控制器的面更适合用来提供更多[频道](../ae2-mechanics/channels.md)。
它也可以由 <ItemLink id="vibration_chamber" /> 产生，或通过 <ItemLink id="crystal_resonance_generator" /> 被动产生，但 AE2 的设计理念
是与其他拥有更强发电能力的科技模组配合使用。

这意味着，在规划基地的能源分配基础设施时，最好将 AE2 网络视为一台大型的多方块机器。

Forge 能量与 Techreborn 能量的转换比例如下

*   2 FE 等于 1 AE (Forge)
*   1 E 等于 2 AE (Fabric)

## 能量存储

<Row>
  <BlockImage id="energy_cell" scale="4" p:fullness="4" />

  <BlockImage id="dense_energy_cell" scale="4" p:fullness="4" />

  <BlockImage id="creative_energy_cell" scale="4" />
</Row>

出于相对显而易见的原因，网络在一个游戏刻内能够接收或消耗的能量，不能超过其可存储的能量。如果一个网络只能存储 800 AE，那么当它的[ME设备](../ae2-mechanics/devices.md)请求能量时，它们最多只能使用 800 AE（假设存储已满），而能源接收器也只能向网络中输入最多 800 AE（假设存储为空）。

这是一种导致异常行为的常见原因：有些人只用能源接收器、幻影刃、终端和一些设备搭了一个小型网络，然后尝试将自己物品栏里满满一栏的圆石倒入网络。一次在单个游戏刻内插入这么多圆石，所需的能量会超过网络当前储存的能量，因此并不是所有圆石都能被插入。这样一来，网络会耗尽能量，从而重启。

**这可以通过添加能量单元来解决。**

网络具有内置能量缓冲，每条线缆、机器或部件可储存 25 AE。

<ItemLink id="controller" />具有少量内部能量存储，容量为 8,000 AE

<ItemLink id="energy_cell" /> 可存储 200k AE，仅需一个就足以满足大多数用途，能够轻松应对普通网络使用中的电力峰值。

<ItemLink id="dense_energy_cell" /> 可存储 1.6M AE，适用于你想依靠储存的电力来运行网络时，或者处理大型[空间塔](spatial-io.md)装置带来的巨大瞬时能量消耗。

<ItemLink id="creative_energy_cell" /> 是一个用于测试的创造模式物品，提供无限 POWAHHHH 之类的东西。