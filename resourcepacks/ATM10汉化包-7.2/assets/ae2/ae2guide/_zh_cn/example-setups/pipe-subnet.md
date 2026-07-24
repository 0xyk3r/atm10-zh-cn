---
navigation:
  parent: example-setups/example-setups-index.md
  title: 物品/流体“管道”子网络
  icon: storage_bus
---

# 物品/流体“管道”子网络

一种使用 AE2 [ME设备](../ae2-mechanics/devices.md) 来模拟物品和/或流体管道的简单方法。总之，凡是你会用到物品管道或流体管道的地方，它都很有用。
这也包括将合成结果返回到 <ItemLink id="pattern_provider" />。

通常有两种不同的方法来实现这一点：

## 输入总线 -> 存储总线

<GameScene zoom="6" background="transparent">
  <ImportStructure src="../assets/assemblies/import_storage_pipe.snbt" />

<BoxAnnotation color="#dddddd" min="3.7 0 0" max="4 1 1">
        (1) 输入总线：可设置过滤条件。
  </BoxAnnotation>

<BoxAnnotation color="#dddddd" min="1 0 0" max="1.3 1 1">
        (2) 存储总线：可进行过滤。这个存储总线（以及其他你希望作为目标端的存储总线）
        必须是网络中唯一的存储。
  </BoxAnnotation>

<DiamondAnnotation pos="4.5 0.5 0.5" color="#00ff00">
        来源
    </DiamondAnnotation>

<DiamondAnnotation pos="0.5 0.5 0.5" color="#00ff00">
        目标位置
    </DiamondAnnotation>

  <IsometricCamera yaw="195" pitch="30" />
</GameScene>

源容器上的 <ItemLink id="import_bus" />（1）会导入物品或流体，并尝试将其存入[网络存储](../ae2-mechanics/import-export-storage.md)。
由于网络中唯一的存储是 <ItemLink id="storage_bus" />（2）（这就是为什么这是一个子网络，而不是连接在你的主网络上），物品或流体
会被放入目标容器中，从而完成传输。能量通过一个 <ItemLink id="quartz_fiber" /> 提供。
导入总线和存储总线都可以设置过滤，但如果未应用任何过滤器，该装置会传输它所能访问到的一切内容。
这种搭建方式同样适用于多个导入总线和多个存储总线。

## 存储总线 -> 输出总线

<GameScene zoom="6" background="transparent">
  <ImportStructure src="../assets/assemblies/storage_export_pipe.snbt" />

<BoxAnnotation color="#dddddd" min="3.7 0 0" max="4 1 1">
        (1) 存储总线：可进行筛选。这个存储总线（以及其他你想设为来源的存储总线）
        必须是网络中唯一的存储设备。
  </BoxAnnotation>

<BoxAnnotation color="#dddddd" min="1 0 0" max="1.3 1 1">
        (2) 输出总线：必须设置过滤条件。
  </BoxAnnotation>

<DiamondAnnotation pos="4.5 0.5 0.5" color="#00ff00">
        来源
    </DiamondAnnotation>

<DiamondAnnotation pos="0.5 0.5 0.5" color="#00ff00">
        目标位置
    </DiamondAnnotation>

  <IsometricCamera yaw="195" pitch="30" />
</GameScene>

目标容器上的 <ItemLink id="export_bus" /> 会尝试从[网络存储](../ae2-mechanics/import-export-storage.md)中拉取其筛选器内的物品。
由于网络上唯一的存储就是 <ItemLink id="storage_bus" />（这也是为什么这是一个子网，而不是在你的主网络上），这些物品或流体
就会从源容器中被拉出，从而完成传输。能量则通过 <ItemLink id="quartz_fiber" /> 提供。
由于导出总线必须设置筛选器才能工作，因此只有在你为导出总线设置了筛选器时，这个布局才会运行。
这个布局同样适用于多个存储总线和多个导出总线。

## 无法工作的设置（输入总线 -> 输出总线）

<GameScene zoom="6" background="transparent">
  <ImportStructure src="../assets/assemblies/import_export_pipe.snbt" />

<BoxAnnotation color="#dd3333" min="3.7 0 0" max="4 1 1">
        输入总线：由于网络没有存储空间，因此它没有可导入到的地方。
  </BoxAnnotation>

<BoxAnnotation color="#dd3333" min="1 0 0" max="1.3 1 1">
        (2) 输出总线：由于网络没有存储空间，因此没有任何可供导出的内容。
  </BoxAnnotation>

<DiamondAnnotation pos="4.5 0.5 0.5" color="#ff0000">
        来源
    </DiamondAnnotation>

<DiamondAnnotation pos="0.5 0.5 0.5" color="#ff0000">
        目标位置
    </DiamondAnnotation>

  <IsometricCamera yaw="195" pitch="30" />
</GameScene>

仅有导入总线和导出总线的配置是无法工作的。导入总线会尝试从源容器中抽取物品或流体，并将其存入网络存储中。导出总线会尝试从网络存储中提取物品或流体，并将其放入目标容器中。然而，由于这个网络**没有存储**，导入总线无法导入，导出总线也无法导出，因此什么都不会发生。

## 通过 1 个面输入和输出

假设你有一台某个机器，它可以接收输入，并且能通过一个面抽取其输出。（例如 <ItemLink id="charger" />）
你可以将这两种管道子网方法结合起来，同时推入原料并抽出结果：

<GameScene zoom="6" background="transparent">
  <ImportStructure src="../assets/assemblies/import_storage_export_pipe.snbt" />

<BoxAnnotation color="#dddddd" min="4 1 1" max="5 1.3 2">
        (1) 输入总线：可设置过滤条件。
  </BoxAnnotation>

<BoxAnnotation color="#dddddd" min="2 1 1" max="3 1.3 2">
        (2) 存储总线：可设置过滤。这个（以及其他你想用来推拉物品的存储总线）
        必须是网络中唯一的存储设备。
  </BoxAnnotation>

<BoxAnnotation color="#dddddd" min="2 0 1" max="3 1 2">
        (3) 你想要推送到并从中拉取的对象：本例中为充电器。
  </BoxAnnotation>

<BoxAnnotation color="#dddddd" min="0 1 1" max="1 1.3 2">
        (4) 输出总线：必须设置过滤条件。
  </BoxAnnotation>

<DiamondAnnotation pos="4.5 0.5 1.5" color="#00ff00">
        来源
    </DiamondAnnotation>

<DiamondAnnotation pos="0.5 0.5 1.5" color="#00ff00">
        目标位置
    </DiamondAnnotation>

  <IsometricCamera yaw="195" pitch="30" />
</GameScene>

## 接口

事实证明，除了输入总线和输出总线之外，还有其他[设备](../ae2-mechanics/devices.md)也能将物品推入
和从[存储网络](../ae2-mechanics/import-export-storage.md)中拉出！
这里相关的是 <ItemLink id="interface" />。如果插入了某个物品，而该接口未被设置为储备该物品，接口就会
将其推入存储网络，我们可以像利用输入总线 -> 存储总线管道那样利用这一点。将接口设置为
储备某种物品时，它会从存储网络中拉取该物品，类似于存储总线 -> 输出总线管道。接口可以被设置为
储备某些物品而不储备其他物品，这样一来，如果你出于某种原因想这么做，就可以通过存储总线远程推送和拉取物品。

<GameScene zoom="6" background="transparent">
<ImportStructure src="../assets/assemblies/interface_pipes.snbt" />

<BoxAnnotation color="#dddddd" min="3.7 0 0" max="4 1 1">
        接口
  </BoxAnnotation>

<BoxAnnotation color="#dddddd" min="1 0 0" max="1.3 1 1">
        存储总线
  </BoxAnnotation>

<BoxAnnotation color="#dddddd" min="3.7 0 2" max="4 1 3">
        存储总线
  </BoxAnnotation>

<BoxAnnotation color="#dddddd" min="0 1 2" max="1 1.3 3">
        接口
  </BoxAnnotation>

<IsometricCamera yaw="195" pitch="30" />
</GameScene>

## 一对多与多对一（以及多对多）

当然，你不必只使用一种 <ItemLink id="import_bus" />、<ItemLink id="export_bus" /> 或 <ItemLink id="storage_bus" />

<GameScene zoom="3" background="transparent">
<ImportStructure src="../assets/assemblies/many_to_many_pipe.snbt" />

<IsometricCamera yaw="185" pitch="30" />
</GameScene>

## 提供到多个位置

由此，我们可以推导出一种方法，将材料从一个 <ItemLink id="pattern_provider" /> 面发送到许多不同的位置，例如一组机器，或同一台机器的几个不同面。

我们不希望使用导入 -> 存储管道或存储 -> 导出管道，因为 <ItemLink id="pattern_provider" /> 实际上
并不包含这些材料。相反，供应器会将材料*推送*到相邻的容器中，因此我们需要某个
同样能够导入物品的相邻容器。

这听起来像是……一个 <ItemLink id="interface" />！

请确保供应器处于定向或平面子部件模式，和/或接口处于平面子部件模式，这样两者之间就不会形成网络连接。

<GameScene zoom="6" background="transparent">
<ImportStructure src="../assets/assemblies/provider_interface_storage.snbt" />

<BoxAnnotation color="#dddddd" min="2.7 0 1" max="3 1 2">
        接口（必须是平的，不能是完整方块）
  </BoxAnnotation>

<BoxAnnotation color="#dddddd" min="1 0 0" max="1.3 1 4">
        存储总线
  </BoxAnnotation>

<BoxAnnotation color="#dddddd" min="0 0 0" max="1 1 4">
        你想要进行样板供应的位置（多台机器，或 1 台机器的多个面）
  </BoxAnnotation>

<IsometricCamera yaw="185" pitch="30" />
</GameScene>