---
navigation:
  parent: ae2-mechanics/ae2-mechanics-index.md
  title: 网络连接
  icon: fluix_glass_cable
---

# 网络连接

## “网络”是什么意思？

“网络”是一组由能够传递[频道](../ae2-mechanics/channels.md)的方块连接起来的[设备](../ae2-mechanics/devices.md)，
例如[线缆](../items-blocks-machines/cables.md)或完整方块机器和[设备](../ae2-mechanics/devices.md)。
(<ItemLink id="charger" />、<ItemLink id="interface" />、<ItemLink id="drive" /> 等。)
严格来说，实际上单根线缆也算是一个网络。

## 设备位置的补充说明

对于具有特定网络功能的[设备](../ae2-mechanics/devices.md)（例如可向[网络存储](../ae2-mechanics/import-export-storage.md)推送和从中拉取物品的 <ItemLink id="interface" />、
读取网络存储内容的 <ItemLink id="level_emitter" />、
作为网络存储的 <ItemLink id="drive" />，等等），
设备的实际位置并不重要。

再次强调，**设备的物理位置并不重要**。真正重要的是设备已连接到网络
（当然，还包括它连接的是哪个网络）。

## 网络连接

判断网络中连接了什么的一种简单方法是使用 <ItemLink id="network_tool" />。它会显示网络中的每个
组件，所以如果你看到了本不该出现的东西，或者没看到本该出现的东西，那就说明出了问题。

例如，这就是 2 个彼此独立的网络。

<GameScene zoom="6" background="transparent">
  <ImportStructure src="../assets/assemblies/2_networks_1.snbt" />

  <BoxAnnotation color="#915dcd" min="0 0 0" max="1 2 2">
        网络 1
  </BoxAnnotation>

<BoxAnnotation color="#5CA7CD" min="2 0 0" max="3 2 2">
        网络 2
  </BoxAnnotation>

  <IsometricCamera yaw="195" pitch="30" />
</GameScene>

这同样也是两个独立的网络，因为 <ItemLink id="quartz_fiber" /> 共享了 [energy](../ae2-mechanics/energy.md)
却没有提供网络连接。

<GameScene zoom="6" background="transparent">
  <ImportStructure src="../assets/assemblies/2_networks_2.snbt" />

  <BoxAnnotation color="#915dcd" min="0 0 0" max="1 2 2">
        网络 1
  </BoxAnnotation>

  <BoxAnnotation color="#5CA7CD" min="1.3 0 0" max="3 2 2">
        网络 2
  </BoxAnnotation>

  <IsometricCamera yaw="195" pitch="30" />
</GameScene>

然而，这仍然只是 1 个网络，而不是 2 个独立的网络。[量子环](../items-blocks-machines/quantum_bridge.md) 的作用类似于无线的[致密线缆](../items-blocks-machines/cables.md#dense-cable)，因此两端位于同一网络中。

<GameScene zoom="4" background="transparent">
  <ImportStructure src="../assets/assemblies/actually_1_network.snbt" />

  <BoxAnnotation color="#915dcd" min="0 0 0" max="7 3 3">
        全部属于 1 个网络
  </BoxAnnotation>

  <IsometricCamera yaw="195" pitch="30" />
</GameScene>

这也仍然只是 1 个网络，因为[cable](../items-blocks-machines/cables.md) 颜色除了不同颜色的数据线不会彼此连接之外，与网络连接无关。所有颜色都可以连接到福鲁伊克斯（或“无色”）数据线。

<GameScene zoom="6" background="transparent">
  <ImportStructure src="../assets/assemblies/actually_1_network_2.snbt" />

  <BoxAnnotation color="#915dcd" min="0 0 0" max="4 2 2">
        全部属于 1 个网络
  </BoxAnnotation>

  <IsometricCamera yaw="195" pitch="30" />
</GameScene>

## 子网络语境下的连接

[子网络](../ae2-mechanics/subnetworks.md) 利用网络连接（以及特别是**不**连接）
来限制[设备](../ae2-mechanics/devices.md) 能访问哪些其他设备。

子网本质上就只是一个独立的网络。

例如，以 [自动矿石时运机](../example-setups/ore-fortuner.md) 为例。这里有 3 个彼此独立的网络，
它们各自负责该装置中的特定功能。

<GameScene zoom="6" interactive={true}>
  <ImportStructure src="../assets/assemblies/ore_fortuner.snbt" />

  <BoxAnnotation color="#915dcd" min="0 0 2" max="3 1 3">
        网络 1，像一个管道子网一样工作，限制导入总线可访问的内容，从而通过
        成型面板“存储”矿石方块。
  </BoxAnnotation>

  <BoxAnnotation color="#5CA7CD" min="0 0 0" max="3 1 1">
        网络 2，像另一个管道子网一样工作，限制 ME破坏面板可访问的内容，使它们将
        时运处理后的矿石碎块存入木桶，而不是你的主网络中。同时也意味着它们不会占用
        主网络上的任何频道。
  </BoxAnnotation>

  <BoxAnnotation color="#82CD5C" min="2 0 1" max="4 1 2">
        网络 3，主网络，承载你所有的存储和合成。它实际上只是用来供电的，并且明确地
        *没有*连接到前面两个子网。
  </BoxAnnotation>

  <IsometricCamera yaw="195" pitch="30" />
</GameScene>

## P2P 语境下的连接

[P2P通道](../items-blocks-machines/p2p_tunnels.md) 的一种变体传输的是[频道](channels.md)，而不是物品、流体
或红石信号，而这不知为何总会让人困惑。通道所安装的那个网络与它所传输的
网络毫无关系。它们*可以*是同一个网络，但并不必须，而且通常也不是。

<GameScene zoom="6" background="transparent">
  <ImportStructure src="../assets/assemblies/p2p_channels_network_connection.snbt" />

  <BoxAnnotation color="#915dcd" min="0 0 0" max="1.98 2 1">
        网络 1，被传输的网络（通常是你的主网络）
  </BoxAnnotation>

  <BoxAnnotation color="#5CA7CD" min="2.02 0 0" max="3.98 1 1">
        网络 2，运行 ME P2P通道 的网络（通常*不是*你的主网络）
  </BoxAnnotation>

  <BoxAnnotation color="#915dcd" min="4.02 0 0" max="6 1 1">
        网络 1，被传输的网络（通常是你的主网络）
  </BoxAnnotation>

  <IsometricCamera yaw="195" pitch="30" />
</GameScene>

## 不那么直观的连接方式

在这种情况下，这仍然只是 1 个网络，因为 <ItemLink id="pattern_provider" /> 作为一个完整方块设备，会像数据线一样工作，而 <ItemLink id="inscriber" /> 也同样如此。因此，网络连接会穿过供应器和压印器。

<GameScene zoom="6" background="transparent">
  <ImportStructure src="../assets/assemblies/pattern_provider_network_connection_1.snbt" />

  <BoxAnnotation color="#915dcd" min="0 0 0" max="4 2 2">
        全部属于 1 个网络
  </BoxAnnotation>

  <IsometricCamera yaw="195" pitch="30" />
</GameScene>

为防止这种情况发生（这对许多涉及[subnetworks](../ae2-mechanics/subnetworks.md)的自动合成配置都很有用），
你可以手持 <ItemLink id="certus_quartz_wrench" /> 右键点击供应器，使其变为定向模式，这样它就不会通过其中一侧传递通道。

<Row gap="40">
<GameScene zoom="6" background="transparent">
  <ImportStructure src="../assets/assemblies/pattern_provider_network_connection_2.snbt" />

  <BoxAnnotation color="#915dcd" min="0 0 0" max="1.98 2 2">
        网络 1
  </BoxAnnotation>

  <BoxAnnotation color="#5CA7CD" min="2.02 0 0" max="4 2 2">
        网络 2
  </BoxAnnotation>

  <IsometricCamera yaw="195" pitch="30" />
</GameScene>

<GameScene zoom="6" background="transparent">
  <ImportStructure src="../assets/assemblies/pattern_provider_directional_connection.snbt" />

  <BoxAnnotation color="#ee3333" min="1 .3 .3" max="1.3 .7 .7">
        注意观察线缆是如何没有连接上的
  </BoxAnnotation>

  <IsometricCamera yaw="255" pitch="30" />
</GameScene>
</Row>

其他不提供定向网络连接的部件大多是[subpart](../ae2-mechanics/cable-subparts.md)
[devices](../ae2-mechanics/devices.md)，例如 <ItemLink id="import_bus" />ses、<ItemLink id="storage_bus" />ses 和
<ItemLink id="cable_interface" />s。

<GameScene zoom="6" background="transparent">
  <ImportStructure src="../assets/assemblies/subpart_no_connection.snbt" />
  <IsometricCamera yaw="195" pitch="30" />
</GameScene>