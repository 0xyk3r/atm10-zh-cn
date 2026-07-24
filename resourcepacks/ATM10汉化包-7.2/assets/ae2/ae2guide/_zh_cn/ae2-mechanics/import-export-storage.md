---
navigation:
  parent: ae2-mechanics/ae2-mechanics-index.md
  title: 导入、导出与存储
---

# 导入、导出与存储

**你的 ME 系统与世界**

应用能源中的一个重要概念是“网络存储”。它是存放网络内容的地方，
通常是[存储元](../items-blocks-machines/storage_cells.md)，或者是 <ItemLink id="storage_bus" /> 所连接到的任何容器。
大多数应用能源[ME设备](../ae2-mechanics/devices.md)都会以这样或那样的方式与它交互。

例如，

*   <ItemLink id="import_bus" />ses 会将物品存入网络存储
*   <ItemLink id="export_bus" />ses 会从网络存储中抽取物品
*   <ItemLink id="interface" />s 既会从网络存储中抽取，也会将物品存入网络存储
*   [Terminals](../items-blocks-machines/terminals.md) 会在你放入或取出物品时，或在补充合成槽位时，既将物品存入网络存储，也从网络存储中抽取物品
*   <ItemLink id="storage_bus" />ses 并不是真的向存储中输出或从存储中抽取，它们是向相连的容器中输出或从相连的容器中抽取
    以便将其用作网络存储（所以实际上是其他设备向*它们*输出或从*它们*抽取）

<GameScene zoom="4" interactive={true}>
  <ImportStructure src="../assets/assemblies/import_export_storage.snbt" />

<BoxAnnotation color="#dddddd" min="8 1 1" max="9 1.3 2">
        输入总线会将其所指向容器中的物品导入到网络存储中
  </BoxAnnotation>

<BoxAnnotation color="#dddddd" min="8 2 1" max="9 3 1.3">
        将物品从你的物品栏放入终端，会被视为网络正在导入它
  </BoxAnnotation>

<BoxAnnotation color="#dddddd" min="7 0 1" max="8 1 2">
        如果某个槽位未被配置为补货任何物品，或者该槽位中的物品数量超过了设定的补货数量，接口就会从其内部容器中导入物品，因此你也可以将物品推入其中，以便插入网络中
  </BoxAnnotation>

  <BoxAnnotation color="#dddddd" min="6 0 1" max="7 1 2">
        Pattern Providers will import from their internal return slot inventory, so things can be pushed into them to insert into the network
  </BoxAnnotation>

  <BoxAnnotation color="#dddddd" min="4 1 1" max="5 2 2">
        驱动器会将插入的存储元作为网络存储提供出来
  </BoxAnnotation>

  <BoxAnnotation color="#dddddd" min="3 1 1" max="4 1.3 2">
        存储总线会将其所指向的容器作为网络存储使用
  </BoxAnnotation>

<BoxAnnotation color="#dddddd" min="1 1 1" max="2 1.3 2">
        输出总线会将物品从网络存储中导出到它们所指向的容器中
  </BoxAnnotation>

  <BoxAnnotation color="#dddddd" min="1 2 1" max="2 3 1.3">
        从终端中取出某样物品也算作网络将其导出
  </BoxAnnotation>

<BoxAnnotation color="#dddddd" min="0 1 1" max="1 2 2">
        如果接口中的某个槽位被配置为存放某种物品，接口就会导出到其内部容器中，
        因此可以从中抽取物品，以便从网络中提取
  </BoxAnnotation>

  <IsometricCamera yaw="195" pitch="30" />
</GameScene>

在设计自动化和物流系统方案时，务必牢记向存储网络推送物品和从存储网络拉取物品这两种操作/事件。

## 存储优先级

可以通过点击某些 GUI 右上角的扳手来设置优先级。

进入网络的物品会首先以优先级最高的存储作为其首个目标；如果两个存储具有相同的优先级，且其中一个已经包含该物品，那么物品会优先进入该存储，而不是其他存储。任何已加入白名单的单元，在与其他存储处于同一优先级组时，都会被视为已经包含该物品。

从存储中取出物品时，物品会从优先级最低的存储中移除。该优先级系统意味着，随着物品被插入和从网络存储中移除，高优先级存储会被逐渐填满，而低优先级存储会被逐渐清空。