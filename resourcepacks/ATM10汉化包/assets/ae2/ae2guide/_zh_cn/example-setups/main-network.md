---
navigation:
  parent: example-setups/example-setups-index.md
  title: “主网络”示例
  icon: controller
---

# “主网络”示例

许多其他配置都会提到“主网络”。你也可能会问，所有这些[设备](../ae2-mechanics/devices.md)是如何组合在一起，成为一个可运行的系统的。以下是一个示例：

<GameScene zoom="2.5" interactive={true}>
  <ImportStructure src="../assets/assemblies/small_base_network.snbt" />

<BoxAnnotation color="#33dd33" min="5 1 10" max="9 7 14" thickness="0.05">
        大量样板供应器和组装机组成的大型集群，提供了充足的空间来处理合成、切石和锻造台样板。
        棋盘格布局可以让样板供应器紧凑地并行利用多个组装机。
        以 8 个为一组，可以避免频道错误路由。
    </BoxAnnotation>

    <BoxAnnotation color="#33dd33" min="13 10 12" max="14 11 14" thickness="0.05">
        实际上你并不需要那么大的控制器，你在别人基地里看到的那些巨大的环形和立方体设计
        主要只是为了好看。
    </BoxAnnotation>

    <BoxAnnotation color="#33dd33" min="13 12 13" max="14 13 14" thickness="0.05">
        每个优秀的网络都该有一个能量元，用于提高每游戏刻的能量输入上限，
        并平滑电力波动。
    </BoxAnnotation>
    
    <BoxAnnotation color="#33dd33" min="2 1 10" max="4 4 13" thickness="0.05">
        你大概会想使用其他模组的电源，比如反应堆、太阳能板、发电机之类的东西。
        振动仓还算勉强能用，但 AE2 的设计理念是用于整合包中，并接入你
        基地的主发电系统。
    </BoxAnnotation>

    <BoxAnnotation color="#33dd33" min="15 1 9" max="16 3 14" thickness="0.05">
        伪装板可用于将东西隐藏在墙后。
    </BoxAnnotation>
    <BoxAnnotation color="#33dd33" min="15 3 12" max="16 10 14" thickness="0.05">
        伪装板可用于将东西隐藏在墙后。
    </BoxAnnotation>

    <BoxAnnotation color="#33dd33" min="13 9 7" max="14 10 9" thickness="0.05">
        你的通用存储并不需要那么多驱动器槽位和存储元件，2-4 个驱动器、搭配 4k 或 16k
        存储元件，几乎总是足够的。
    </BoxAnnotation>

    <BoxAnnotation color="#33dd33" min="13 9 10" max="14 11 11" thickness="0.05">
        对于大宗存储，你会希望使用过滤为特定物品的大容量存储元件，并将它们放入单独的存储驱动器中，
        同时将这些驱动器设置为更高优先级。
    </BoxAnnotation>

    <BoxAnnotation color="#33dd33" min="10 9 13" max="11.7 13 14" thickness="0.05">
        基于接口的自动补货。
    </BoxAnnotation>

    <BoxAnnotation color="#33dd33" min="6 10 12" max="9 12 15" thickness="0.05">
        将充能器自动化方案在逻辑上扩展到多个充能器。
    </BoxAnnotation>

    <BoxAnnotation color="#33dd33" min="2 10 12" max="5 11 15" thickness="0.05">
        这是另一种自动化处理器的方法，因为压印器在 1.20 中现在可以自动弹出产物了。
    </BoxAnnotation>

    <BoxAnnotation color="#33dd33" min="3 10 10" max="4 12 11" thickness="0.05">
        这是另一种自动化处理器的方法，因为压印器在 1.20 中现在可以自动弹出产物了。
    </BoxAnnotation>

    <BoxAnnotation color="#33dd33" min="7.2 9.2 8.2" max="7.8 10 8.8" thickness="0.05">
        无线接入点位于中间，因为它的作用范围是球形的。
    </BoxAnnotation>

    <BoxAnnotation color="#33dd33" min="14 1 2" max="16 5 7" thickness="0.05">
        通常你会准备 1 到 2 个大型合成器CPU 来处理大型任务，再配备几个较小的来在大型 CPU 忙碌时处理次要
        任务。
    </BoxAnnotation>

    <BoxAnnotation color="#33dd33" min="5 3 6" max="6 4 7" thickness="0.05">
        有时子网络可能需要自己的控制器，前提是设备数量超过 8 个（例如需要分发到
        8 个以上的位置时）。
    </BoxAnnotation>

    <BoxAnnotation color="#33dd33" min="7.3 1 3.3" max="9.7 4 6" thickness="0.05">
        赛特斯农场。
    </BoxAnnotation>

    <BoxAnnotation color="#33dd33" min="10.3 1 2.3" max="12.7 3.7 5" thickness="0.05">
        丢入水中的自动化。
    </BoxAnnotation>

  <IsometricCamera yaw="135" pitch="15" />
</GameScene>