---
navigation:
  parent: example-setups/example-setups-index.md
  title: 专用本地存储
  icon: drive
---

# 专用本地存储

利用 Interface 的一种[特殊行为](../items-blocks-machines/interface.md#special-interactions)，可以让[subnetwork](../ae2-mechanics/subnetworks.md) 将其存储中的内容提供给主网络，而自身
无法看到主网络中的存储内容，并且只占用 1 个[channel](../ae2-mechanics/channels.md)。

这适合在某个农场处进行本地存储，这样物品就不会溢出到你的主存储中了。

<GameScene zoom="6" interactive={true}>
  <ImportStructure src="../assets/assemblies/local_storage.snbt" />

<BoxAnnotation color="#dddddd" min="4 0 0" max="5 2 1">
        （1）某种导入物品的方法（此处为接口）
  </BoxAnnotation>

<BoxAnnotation color="#dddddd" min="3 0 0" max="4 1 1">
        (2) 驱动器：里面有一些存储元件。这些存储元件应过滤为农场的产出物。
        存储元件可以安装平均分配卡和溢出销毁卡。
        <Row><ItemImage id="item_storage_cell_4k" scale="2" /> <ItemImage id="equal_distribution_card" scale="2" /> <ItemImage id="void_card" scale="2" /></Row>
  </BoxAnnotation>

<BoxAnnotation color="#dddddd" min="3 1 0" max="4 2 0.3">
        (3) 合成终端：它可以查看子网中幻影刃里的内容，但无法查看你主网络存储中的内容。
  </BoxAnnotation>

<BoxAnnotation color="#dddddd" min="2 0 0" max="2.3 1 1">
        (4) 接口 #2：使用默认配置。
  </BoxAnnotation>

<BoxAnnotation color="#dddddd" min="1.7 0 0" max="2 1 1">
        (5) 存储总线：优先级设置得高于主存储，可以筛选为农场产出的任何物品。
  </BoxAnnotation>

<BoxAnnotation color="#dddddd" min="1 1 0" max="2 2 0.3">
        合成终端：它可以同时查看主网络的 ME网络存储内容 *以及* 子网络。
  </BoxAnnotation>

<DiamondAnnotation pos="0 0.5 0.5" color="#00ff00">
        连接到主网络
    </DiamondAnnotation>

  <IsometricCamera yaw="195" pitch="30" />
</GameScene>

## 配置

* 第一个 <ItemLink id="interface" />（1）只是接收你拥有的任意农场产出的物品，并将它们推送到子网中。
* <ItemLink id="drive" />（2）内放有一些[cell](../items-blocks-machines/storage_cells.md)。这些存储元件应当
  [分区](../items-blocks-machines/cell_workbench.md)为农场产出的物品。
  这些存储元件可以包含 <ItemLink id="equal_distribution_card" /> 和 <ItemLink id="void_card" />。
* 第二个 <ItemLink id="interface" />（4）处于默认配置。
* <ItemLink id="storage_bus" /> 的[优先级](../ae2-mechanics/import-export-storage.md#storage-priority)设置得
  高于主存储。它可以被过滤为农场产出的物品。

## 工作原理

* 子网络上的 <ItemLink id="interface" /> 会向主网络上的 <ItemLink id="storage_bus" /> 显示 <ItemLink id="drive" /> 的内容。
这意味着存储总线可以直接从驱动器中的存储元件拉取物品，并将物品推送到这些存储元件中。
* 存储总线被设为高[优先级](../ae2-mechanics/import-export-storage.md#storage-priority)，这样物品会优先放回子网络，而不是放进你的主存储中。
* 重要的是，如果子网络中的存储元件被装满了，物品也不会溢出到主网络中。如果农场属于一旦堆积就会出问题的类型，则可以改用 <ItemLink id="void_card" />s 来删除多余的物品。 
* 如果农场会产出多种物品，<ItemLink id="equal_distribution_card" />s 可以防止某一种物品占满所有存储元件，导致其他物品无法存储。