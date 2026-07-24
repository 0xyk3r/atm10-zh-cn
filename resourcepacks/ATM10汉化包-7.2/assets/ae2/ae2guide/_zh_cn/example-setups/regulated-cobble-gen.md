---
navigation:
  parent: example-setups/example-setups-index.md
  title: 自动调节造石机
  icon: minecraft:cobblestone
---

# 自动调节造石机

圆石刷石机的自动化很简单，只需让一个 <ItemLink id="annihilation_plane" /> 面向一个标准的原版手动刷石机即可。不过，这样做最终会让你的网络被圆石塞满，因此最好进行一些调控。

由于湮灭平面的工作方式（它们的行为类似于 <ItemLink id="import_bus" />ses），我们不能简单地放一个朝向带有 <ItemLink id="redstone_card" /> 的 <ItemLink id="export_bus" /> 的 <ItemLink id="level_emitter" />
（因为中间没有存储时，你不能直接从导入到导出）。
我们得稍微绕一点。

<ItemLink id="toggle_bus" />总线允许你使用红石信号连接和断开网络的部分组件，但每次这样做时都会导致
网络重启。一个简单的解决办法是：将切换总线放在一个[subnetwork](../ae2-mechanics/subnetworks.md)
上，这样它就只会重启子网络。

我们可以建立一个独立的 <ItemLink id="annihilation_plane" /> 和 <ItemLink id="storage_bus" /> [子网络](../ae2-mechanics/subnetworks.md)
，将物品推入主网络上的 <ItemLink id="interface" /> 中。切换总线会将子网络与
<ItemLink id="quartz_fiber" /> 连接或断开，从而切断平面的供电。

<GameScene zoom="4" interactive={true}>
  <ImportStructure src="../assets/assemblies/regulated_cobble_gen.snbt" />

<BoxAnnotation color="#dddddd" min="3 2 2" max="7 2.3 3">
        (1) 破坏面板：没有可供配置的 GUI，但可以附魔效率和耐久以降低耗电量。
  </BoxAnnotation>

  <BoxAnnotation color="#dddddd" min="2 2 2" max="2.3 3 3">
        (2) 存储总线：使用默认配置。
  </BoxAnnotation>

<BoxAnnotation color="#dddddd" min="2.3 2.3 2" max="2.7 2.7 2.3">
        (3) 切换总线：非常重要的一点是，切换总线必须位于子网络上，而不是主网络上。
  </BoxAnnotation>

<BoxAnnotation color="#dddddd" min="2.3 3 2.3" max="2.7 3.3 2.7">
        (4) 存储状态发信器：用圆石和所需数量进行配置，并设置为“当存储量低于限制时发出信号”。
  </BoxAnnotation>

  <BoxAnnotation color="#dddddd" min="1 2 3" max="2 3 2">
        (5) 接口：使用默认配置。
  </BoxAnnotation>

<DiamondAnnotation pos="0 2.5 1.5" color="#00ff00">
        连接到主网络
    </DiamondAnnotation>

<DiamondAnnotation pos="5 1.5 3.5" color="#00ff00">
        含水状态的楼梯可以阻止水流动，避免将熔岩变成黑曜石。
    </DiamondAnnotation>

  <IsometricCamera yaw="195" pitch="30" />
</GameScene>

## 配置

* <ItemLink id="annihilation_plane" />（1）没有可供配置的 GUI，但可以附魔效率和耐久，以降低耗电。
* <ItemLink id="storage_bus" />（2）处于默认配置。
* <ItemLink id="toggle_bus" />（3）必须放在石英纤维的子网络一侧，而不是主网络一侧，否则主网络每次切换时都会重启。
* <ItemLink id="level_emitter" />（4）已配置为所需的物品和数量，并设置为“当等级低于限制时发出”。
* <ItemLink id="interface" />（5）处于默认配置。

## 工作原理

1. 造石机会生成一些圆石。
2. <ItemLink id="annihilation_plane" />会破坏圆石。
3. <ItemLink id="storage_bus" />会将圆石存入 <ItemLink id="interface" /> 中，并将其发送到主网络。
4. 当主网络中的圆石数量超过设定值时，<ItemLink id="level_emitter" />会停止
   发出信号，从而关闭 <ItemLink id="toggle_bus" />。
5. 这会切断子网络的电力，使 ME破坏面板停止工作。