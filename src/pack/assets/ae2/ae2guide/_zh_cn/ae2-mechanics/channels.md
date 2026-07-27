---
navigation:
  parent: ae2-mechanics/ae2-mechanics-index.md
  title: 频道
  icon: controller
---

# 频道

应用能源2的[ME网络](me-network-connections.md)需要
频道来支持使用网络存储或其他网络
服务的[设备](../ae2-mechanics/devices.md)。你可以把频道想象成连接所有设备的 USB 线。就像一台电脑只有有限的 USB 接口，因此也只能支持
有限数量的已连接设备一样。大多数机器、整方块设备和标准线缆都只能传输
最多 8 个频道。你可以将整方块设备和标准线缆看作一束由 8 根“频道线”组成的线束。
不过，[ME致密线缆](../items-blocks-machines/cables.md#dense-cable)最多可以支持
32 个频道。除此之外，唯一还能传输 32 个频道的设备是 <ItemLink id="me_p2p_tunnel" />
和[量子环](../items-blocks-machines/quantum_bridge.md)。每当一个设备占用一个频道时，你就可以想象是从
这束线里抽走了一根 USB“线”，这显然意味着这根“线”在线路更后方就无法再使用了。

<GameScene zoom="7" interactive={true}>
  <ImportStructure src="../assets/assemblies/channel_demonstration_1.snbt" />

  <LineAnnotation color="#33ff33" from="1 .4 .7" to="2.4 .4 .7" alwaysOnTop={true}/>
  <LineAnnotation color="#33ff33" from="1 .6 .7" to="2.4 .6 .7" alwaysOnTop={true}/>
  <LineAnnotation color="#33ff33" from="1 .4 .6" to="2.6 .4 .6" alwaysOnTop={true}/>
  <LineAnnotation color="#33ff33" from="1 .6 .6" to="2.6 .6 .6" alwaysOnTop={true}/>
  <LineAnnotation color="#33ff33" from="1 .6 .6" to="2.6 .6 .6" alwaysOnTop={true}/>

  <LineAnnotation color="#33ff33" from="2.4 .6 .7" to="2.4 .6 1.5" alwaysOnTop={true}/>
  <LineAnnotation color="#33ff33" from="2.4 .4 .7" to="2.4 .4 1.5" alwaysOnTop={true}/>
  <LineAnnotation color="#33ff33" from="2.6 .6 .6" to="2.6 .6 1.5" alwaysOnTop={true}/>
  <LineAnnotation color="#33ff33" from="2.6 .4 .6" to="2.6 .4 1.5" alwaysOnTop={true}/>

  <LineAnnotation color="#33ff33" from="2.1 .6 1.5" to="2.4 .6 1.5" alwaysOnTop={true}/>
  <LineAnnotation color="#33ff33" from="2.6 .4 1.5" to="2.9 .4 1.5" alwaysOnTop={true}/>

  <LineAnnotation color="#33ff33" from="2.6 .6 1.5" to="2.6 .9 1.5" alwaysOnTop={true}/>
  <LineAnnotation color="#33ff33" from="2.4 .1 1.5" to="2.4 .4 1.5" alwaysOnTop={true}/>

  <LineAnnotation color="#33ff33" from="1 .6 .4" to="3.5 .6 .4" alwaysOnTop={true}/>
  <LineAnnotation color="#33ff33" from="1 .4 .4" to="3.5 .4 .4" alwaysOnTop={true}/>

  <LineAnnotation color="#33ff33" from="3.5 .6 .4" to="3.5 .9 .4" alwaysOnTop={true}/>
  <LineAnnotation color="#33ff33" from="3.5 .1 .4" to="3.5 .4 .4" alwaysOnTop={true}/>

  <LineAnnotation color="#33ff33" from="1 .6 .3" to="1.5 .6 .3" alwaysOnTop={true}/>
  <LineAnnotation color="#33ff33" from="1 .4 .3" to="1.5 .4 .3" alwaysOnTop={true}/>

  <LineAnnotation color="#33ff33" from="1.5 .6 .3" to="1.5 .9 .3" alwaysOnTop={true}/>
  <LineAnnotation color="#33ff33" from="1.5 .1 .3" to="1.5 .4 .3" alwaysOnTop={true}/>

  <LineAnnotation color="#ff3333" from="3.5 .5 .5" to="5.5 .5 .5" alwaysOnTop={true}>
  缆线中的 8 个频道已全部被占用，因此驱动器分不到频道。  
  </LineAnnotation>

  <LineAnnotation color="#993333" from="1 .5 .5" to="1.25 .5 .5" alwaysOnTop={true}/>
  <LineAnnotation color="#993333" from="1.5 .5 .5" to="1.75 .5 .5" alwaysOnTop={true}/>
  <LineAnnotation color="#993333" from="2 .5 .5" to="2.25 .5 .5" alwaysOnTop={true}/>
  <LineAnnotation color="#993333" from="2.5 .5 .5" to="2.75 .5 .5" alwaysOnTop={true}/>
  <LineAnnotation color="#993333" from="3 .5 .5" to="3.25 .5 .5" alwaysOnTop={true}/>

  <DiamondAnnotation pos="3.6 0.5 0.5" color="#ff0000">
        缆线中的 8 个频道已全部被占用，因此驱动器分不到频道。
    </DiamondAnnotation>

  <IsometricCamera yaw="15" pitch="30" />
</GameScene>

想要轻松查看通道在你的网络中是如何使用和路由的，可以使用[智能线缆](../items-blocks-machines/cables.md)，它们会在线缆上显示通道的路径和使用情况。

频道每经过 1 个节点会消耗 1⁄128 AE/t，这意味着对于一个拥有 8 台设备且超过 96 个节点的网络，添加一个 <ItemLink id="controller" /> 反而可能会降低能耗，因为它会改变频道的分配方式。

值得注意的是，**频道与线缆颜色毫无关系**，线缆颜色唯一的作用就是让线缆彼此不连接。

## 频道布线

当你使用 <ItemLink id="controller" /> 时，
通道会通过 3 个步骤进行传输。它们首先会通过相邻机器，以最短路径到达最近的[普通线缆](../items-blocks-machines/cables.md)
（玻璃、包层或智能）。然后，它们会通过该普通线缆，以最短路径到达最近的[致密线缆](../items-blocks-machines/cables.md)
（致密或致密智能）。接着，它们会通过该致密线缆，以最短路径到达 <ItemLink id="controller" />。
如果最短路径上的通道已经满了，那么某些[设备](devices.md) 可能无法获得所需的通道，请善用
彩色线缆、线缆锚和隧道，确保你的通道沿着你想要的路径传输。

例如，在这种情况下，有些存储元件无法获得频道，因为尽管线缆容量足够，频道仍会尝试走最短路径，导致部分线缆过载，而其他线缆却处于空闲状态。

<GameScene zoom="4" interactive={true}>
  <ImportStructure src="../assets/assemblies/channel_path_length_issue.snbt" />

  <LineAnnotation color="#33ff33" from="3 .5 1.4" to="0.4 0.5 1.4" alwaysOnTop={true} thickness="0.05"/>
  <LineAnnotation color="#33ff33" from="0.4 .5 1.4" to="0.4 0.5 3.6" alwaysOnTop={true} thickness="0.05"/>
  <LineAnnotation color="#33ff33" from="0.4 0.5 3.6" to="1.4 0.5 3.6" alwaysOnTop={true} thickness="0.05"/>
  <LineAnnotation color="#33ff33" from="1.4 0.5 3.6" to="1.4 0.5 5" alwaysOnTop={true} thickness="0.05"/>

  <LineAnnotation color="#33ff33" from="3 0.5 3.6" to="1.6 0.5 3.6" alwaysOnTop={true} thickness="0.05"/>
  <LineAnnotation color="#33ff33" from="1.6 0.5 3.6" to="1.6 0.5 5" alwaysOnTop={true} thickness="0.05"/>

  <LineAnnotation color="#ff3333" from="3 .5 1.6" to="0.6 .5 1.6" alwaysOnTop={true} thickness="0.05"/>
  <LineAnnotation color="#ff3333" from="0.6 .5 1.6" to="0.6 .5 3.4" alwaysOnTop={true} thickness="0.05"/>
  <LineAnnotation color="#ff3333" from="0.6 .5 3.4" to="1.4 .5 3.4" alwaysOnTop={true} thickness="0.05"/>

  <LineAnnotation color="#ff3333" from="3 .5 3.4" to="1.6 .5 3.4" alwaysOnTop={true} thickness="0.05"/>

  <BoxAnnotation color="#dddddd" min="1.2 0.2 3.2" max="1.8 0.8 3.8" alwaysOnTop={true} thickness="0.05">
        有超过 8 个频道尝试从这里通过，因此其中一些会被切断。
  </BoxAnnotation>

  <IsometricCamera yaw="90" pitch="90" />

</GameScene>

这可以通过更谨慎地限制通道可采用的路径来解决。网络应呈树状（或灌木状）。
应尽量减少回路和模棱两可的通道路径。

<GameScene zoom="4" interactive={true}>
  <ImportStructure src="../assets/assemblies/channel_path_length_issue_fix.snbt" />

  <LineAnnotation color="#33ff33" from="3 .5 1.4" to="0.4 0.5 1.4" alwaysOnTop={true} thickness="0.05"/>
  <LineAnnotation color="#33ff33" from="0.4 .5 1.4" to="0.4 0.5 5.6" alwaysOnTop={true} thickness="0.05"/>
  <LineAnnotation color="#33ff33" from="0.4 0.5 5.6" to="1 0.5 5.6" alwaysOnTop={true} thickness="0.05"/>

  <LineAnnotation color="#33ff33" from="3 0.5 3.6" to="1.6 0.5 3.6" alwaysOnTop={true} thickness="0.05"/>
  <LineAnnotation color="#33ff33" from="1.6 0.5 3.6" to="1.6 0.5 5" alwaysOnTop={true} thickness="0.05"/>

  <IsometricCamera yaw="90" pitch="90" />

</GameScene>

## 临时网络

没有 <ItemLink id="controller" /> 的网络会被视为临时网络，最多只能支持 8 个使用频道的设备。
一旦超过 8 个设备，网络中使用频道的设备就会关闭，
你可以移除一些设备，或者添加一个 <ItemLink id="controller" />。

与控制器网络不同，临时网络上的[智能线缆](../items-blocks-machines/cables.md)会显示整个网络中已使用的通道数量，而不是流经该特定线缆的通道数量。

使用临时网络时，每个设备都会占用整个网络中的 1 个频道，这与 <ItemLink id="controller" /> 根据最短路径分配频道的方式截然不同。

## 设计

如前文在 [通道路由](channels.md#channel-routing) 中提到的那样，最好将你的网络设计成树状结构：致密线缆从控制器处分支出去，普通线缆再从致密线缆处分支，而[设备](../ae2-mechanics/devices.md) 则以 8 个或更少为一组分布在普通线缆上。

下面是一个错误示例：

沿着频道路径，

1. 从控制器出来后立刻向右，由于驱动器的行为和普通线缆一样，因此这里被限制为 8 个频道。
不过由于这里没有使用智能线缆，我们无法看出已有多少频道在使用中。还剩 8 个频道。
2. 驱动器会占用 1 个频道。
还剩 7 个频道。
3. 有 2 个频道向上连接到终端。
还剩 5 个频道。
4. 继续向右，接口会再占用 1 个频道。
还剩 4 个频道。
5. 有 1 个频道向上连接到样板供应器。
还剩 3 个频道。
6. 继续向右，有 1 个频道向上连接到输入总线。
还剩 2 个频道。
7. 那组为装配机供料的样板供应器只分到了 2 个频道，因此其中有 2 个样板供应器没有分到频道。

归根结底，问题在于将通道卡在瓶颈上，而没有考虑清楚这些通道将如何分配。

<GameScene zoom="4" interactive={true}>
  <ImportStructure src="../assets/assemblies/bad_network_structure.snbt" />

<LineAnnotation color="#33ff33" from="6.5 .5 1.5" to="6 .5 1.5" alwaysOnTop={true} thickness="0.4">
  32 个频道
</LineAnnotation>

<LineAnnotation color="#33ff33" from="6 .5 1.5" to="5.5 .5 1.5" alwaysOnTop={true} thickness="0.2">
  8 个频道
</LineAnnotation>

<LineAnnotation color="#33ff33" from="5.5 .5 1.5" to="5.5 1.5 1.5" alwaysOnTop={true} thickness="0.1">
  2 个频道
</LineAnnotation>

<LineAnnotation color="#33ff33" from="5.5 .5 1.5" to="5.5 .3 1.5" alwaysOnTop={true} thickness="0.071">
  1 个频道
</LineAnnotation>

<LineAnnotation color="#33ff33" from="5.5 1.5 1.5" to="5.5 2.5 1.5" alwaysOnTop={true} thickness="0.071">
  1 个频道
</LineAnnotation>

<LineAnnotation color="#33ff33" from="5.5 2.5 1.5" to="5.5 2.5 1.1" alwaysOnTop={true} thickness="0.071">
  1 个频道
</LineAnnotation>

<LineAnnotation color="#33ff33" from="5.5 .5 1.5" to="4.5 .5 1.5" alwaysOnTop={true} thickness="0.158">
  5 个频道
</LineAnnotation>

<LineAnnotation color="#33ff33" from="4.5 .5 1.5" to="4.5 .3 1.5" alwaysOnTop={true} thickness="0.071">
  1 个频道
</LineAnnotation>

<LineAnnotation color="#33ff33" from="4.5 .5 1.5" to="4.5 1.5 1.5" alwaysOnTop={true} thickness="0.071">
  1 个频道
</LineAnnotation>

<LineAnnotation color="#33ff33" from="4.5 .5 1.5" to="3.5 .5 1.5" alwaysOnTop={true} thickness="0.122">
  3 个频道
</LineAnnotation>

<LineAnnotation color="#33ff33" from="3.5 .5 1.5" to="3.5 2.5 1.5" alwaysOnTop={true} thickness="0.071">
  1 个频道
</LineAnnotation>

<LineAnnotation color="#33ff33" from="3.5 2.5 1.5" to="3.7 2.5 1.5" alwaysOnTop={true} thickness="0.071">
  1 个频道
</LineAnnotation>

<LineAnnotation color="#33ff33" from="3.5 .5 1.5" to="1.5 .5 1.5" alwaysOnTop={true} thickness="0.1">
  2 个频道
</LineAnnotation>

<LineAnnotation color="#33ff33" from="1.5 0.5 1.5" to="1.5 0.3 1.5" alwaysOnTop={true} thickness="0.071">
  1 个频道
</LineAnnotation>

<LineAnnotation color="#33ff33" from="1.5 0.5 1.5" to="0.5 0.5 1.5" alwaysOnTop={true} thickness="0.071">
  1 个频道
</LineAnnotation>

<LineAnnotation color="#33ff33" from="0.5 0.5 1.5" to="0.5 0.5 0.5" alwaysOnTop={true} thickness="0.071">
  1 个频道
</LineAnnotation>

<LineAnnotation color="#ff3333" from="0.5 1.5 1.5" to="0.5 1.3 1.5" alwaysOnTop={true} thickness="0.071">
  无频道
</LineAnnotation>

<LineAnnotation color="#ff3333" from="1.5 1.5 0.5" to="1.5 1.3 0.5" alwaysOnTop={true} thickness="0.071">
  无频道
</LineAnnotation>

  <IsometricCamera yaw="195" pitch="30" />
</GameScene>

---

以下是一个良好的结构示例：

<GameScene zoom="2.5" interactive={true}>
  <ImportStructure src="../assets/assemblies/treelike_network_structure.snbt" />

    <BoxAnnotation color="#dddddd" min="6.9 0 4.9" max="9.1 4 7.1" thickness="0.05">
        注意，样板供应器是按每 8 个分成一组的。
    </BoxAnnotation>

<BoxAnnotation color="#dddddd" min="5 4 4" max="8 5 5" thickness="0.05">
        两根已占满频道的普通线缆连接到一起，意味着你需要使用致密线缆。
    </BoxAnnotation>

    <BoxAnnotation color="#dddddd" min="5 0 13" max="8 1 14" thickness="0.05">
        使用不同颜色的线缆来防止相邻线缆连接。
    </BoxAnnotation>


  <IsometricCamera yaw="315" pitch="30" />
</GameScene>

## 频道模式

适用于 Minecraft 1.18 的应用能源 10.0.0 引入了新的选项，用于更改应用能源频道在你的世界中的工作方式。

在常规设置部分中新增了一个配置选项（`channels`）来控制此功能，同时还新增了一个供管理员在游戏内更改模式和配置的命令。用于更改模式的命令是 `/ae2 channelmode <mode>`，而 `/ae2 channelmode` 则用于显示当前模式。当在游戏内更改模式时，所有现有网格都会重启，并立即使用新模式。

这复活并改进了 Minecraft 1.12 中提供的选项，同时为那些只想要更轻松一些的游戏体验、但又不希望这一机制被完全移除的玩家带来了更好的选择。

下表列出了配置文件和命令中可用的模式。

| 设置       | 说明                                                                                                                                                                                                                   |
| ---------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `default`  | 标准模式，线缆网络和临时网络的频道容量与本网站其余部分所述一致                                                                                                                                                          |
| `x2`       | 所有频道容量翻倍（普通线缆为 16，致密线缆为 64，临时网络支持 16 个频道）                                                                                                                                                 |
| `x3`       | 所有频道容量变为三倍（普通线缆为 24，致密线缆为 92，临时网络支持 24 个频道）                                                                                                                                             |
| `x4`       | 所有频道容量变为四倍（普通线缆为 32，致密线缆为 128，临时网络支持 32 个频道）                                                                                                                                            |
| `infinite` | 移除所有频道限制。控制器仍然会*显著*降低网络的耗电量。智能线缆只会在完全关闭（未传输任何频道）和完全开启（传输 1 个或更多频道）之间切换。                                                                                |