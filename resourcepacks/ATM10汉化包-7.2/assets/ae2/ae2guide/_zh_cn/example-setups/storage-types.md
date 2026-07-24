---
navigation:
  parent: example-setups/example-setups-index.md
  title: 存储类型与网络整洁度
  icon: drive
---

# 各种存储类型与保持网络整洁有序

利用筛选器、[分区](../items-blocks-machines/cell_workbench.md)和[存储优先级](../ae2-mechanics/import-export-storage.md#storage-priority)，
你可以为各种不同类型的物品建立多层存储。

存储类型通常分为：
* 通用存储，用于存放你持有数量从几个到几千个不等的各种零散物品。这通常使用小型[存储元](../items-blocks-machines/storage_cells.md)，
例如 4k 或 16k。
* 大容量存储，用于存放你持有数量超过几千个的物品，比如圆石或铁。这通常使用大型存储元，例如 256k
或 MEGA 附属提供的存储元。
* 农场处的本地存储，如[专用本地存储](specialized-local-storage.md)以及各种
[赛特斯](semiauto-certus-farm.md)[农场](advanced-certus-farm.md)中所述的[various](simple-certus-farm.md)。

优先级的设置方式是：当物品被输入主网络时，系统会先尝试将其存入专用的大容量存储或本地存储；如果无法存入（由于过滤器和分区限制），才会把物品放入通用存储。
这意味着物品**不会主动**从一种存储移动到另一种存储，而是在进出网络的过程中“迁移”。
如果想主动移动物品，请使用一个 <ItemLink id="io_port" />。

<GameScene zoom="3" interactive={true}>
  <ImportStructure src="../assets/assemblies/network_storage_types.snbt" />

    <BoxAnnotation color="#33dd33" min="11 0 1" max="12 1.3 2" thickness="0.05">
        大容量存储。在这个例子中，使用的是连接到高容量存储（如抽屉）上的已过滤存储总线。这个存储总线被过滤为
        煤炭。它具有较高优先级，因此每当煤炭进入网络时，都会进入这个存储总线；而每当煤炭从网络中被提取时，
        都会从*这里以外的其他地方*提取，因此煤炭会“迁移”到这个抽屉中。

        重要说明：像抽屉这样经过优化的大型容器很适合这样使用，但像
        巨型箱子这样拥有大量槽位、且*未*优化的大型容器，在搭配存储总线使用时会严重影响性能。
    </BoxAnnotation>

<BoxAnnotation color="#33dd33" min="11 0 3" max="12 1 4" thickness="0.05">
        大容量存储方案。在这个例子中，是将一个已分区的 256k 元件放入磁盘仓，并设置较高优先级。这个元件被分区为
        圆石和铁。它装有一张均分卡，因此不会被圆石完全占满，从而不给
        铁留下空间。由于该磁盘仓具有较高优先级，所以每当圆石或铁进入网络时，都会进入这个存储总线；
        而每当从网络中取出圆石或铁时，都会从*除这里以外的任何地方*取出，因此圆石和铁就会“迁移”到这个元件中。
    </BoxAnnotation>

    <BoxAnnotation color="#33dddd" min="11 0 5" max="12 1 6" thickness="0.05">
        通用存储。在这个例子中，使用的是一个装满 16k 存储元的磁盘驱动器。这些存储元没有分区。该驱动器具有中性优先级
        （此处为 0），因此每当有物品进入网络时，会优先进入专用的大容量存储或本地存储；
        而每当从网络中提取物品时，则会优先从这里提取，因此那些拥有专用存储位置的物品会自然地
        从通用存储中“迁移”出去。
    </BoxAnnotation>

    <BoxAnnotation color="#88ff88" min="11 0 8" max="12 1 9" thickness="0.05">
        这个 IO端口 在保持网络有序方面扮演着重要角色。由于存储优先级并不会*主动*
        移动物品，因此用于通用存储的存储元应定期经过 IO端口 “洗牌”，以便把那些在
        专用存储中有归属位置的物品移入对应的专用存储。这相当于对存储进行“碎片整理”，确保物品不会
        分散存放在多个位置。
    </BoxAnnotation>

    <BoxAnnotation color="#dd3333" min="14 0 11" max="15 1 12" thickness="0.05">
        刷怪场的本地存储。这个驱动器中的存储元件已分区为你想保留的掉落物，例如骨头和箭。
        驱动器本身没有被赋予优先级，因为真正影响优先级的是主网访问该子网时所用的存储总线。
        这些存储元件装有均分卡和溢出销毁卡。
    </BoxAnnotation>

    <BoxAnnotation color="#dd3333" min="14 1 10" max="15 2.3 11" thickness="0.05">
        刷怪场的本地存储。这个存储总线 - 接口的配置可以让主网络访问这个子网的存储。
        该存储总线被赋予了较高优先级，并筛选为该子网存储元件中存放的那些物品。

        重要：由于子网上有垃圾桶设置，请务必为这个存储总线设置筛选，否则它会开始销毁
        *进入网络的每一个物品、流体等等*！
    </BoxAnnotation>

    <BoxAnnotation color="#dd3333" min="14 0 9" max="15 1.3 10" thickness="0.05">
        刷怪场的本地存储。这个位于物质聚合器上的存储总线优先级低于驱动器。这意味着
        无法进入驱动器中存储元件的怪物掉落物会溢出到这里并被销毁。这一点很重要，
        以防止子网被诸如大量半损坏弓之类的随机垃圾塞满。
    </BoxAnnotation>

    <BoxAnnotation color="#dd33dd" min="8 1 11.7" max="9 2.3 13" thickness="0.05">
        西瓜农场的本地存储。这个配置使用了与各种赛特斯农场示例类似的方法。子网上的一个存储总线
        会将正在种植的产物插入木桶。主网络上的另一个存储总线（筛选为西瓜片并设置高优先级）
        则让主网络可以访问这些农场产物。
    </BoxAnnotation>

  <IsometricCamera yaw="270" pitch="30" />
</GameScene>