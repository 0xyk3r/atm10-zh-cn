---
navigation:
  parent: ae2-mechanics/ae2-mechanics-index.md
  title: 子网络
---

# 子网络

<GameScene zoom="4" interactive={true}>
<ImportStructure src="../assets/assemblies/subnet_demonstration.snbt" />

<DiamondAnnotation pos="6.5 2.5 0.5" color="#00ff00">
        物品管道子网络
    </DiamondAnnotation>

<DiamondAnnotation pos="5.5 2.5 0.5" color="#00ff00">
        流体管道子网络
    </DiamondAnnotation>

<DiamondAnnotation pos="4.5 2.5 0.5" color="#00ff00">
        已过滤的 ME破坏面板
    </DiamondAnnotation>

<DiamondAnnotation pos="3.5 2.5 0.5" color="#00ff00">
        成型平面子网络
    </DiamondAnnotation>

<DiamondAnnotation pos="2.5 2.5 0.5" color="#00ff00">
        使用接口-存储总线交互的子网络，可作为主网络能够访问的本地子存储
    </DiamondAnnotation>

<DiamondAnnotation pos="1.5 1.5 0.5" color="#00ff00">
        Another item pipe subnet, to return the charged items to the Pattern Provider
    </DiamondAnnotation>

<IsometricCamera yaw="195" pitch="30" />
</GameScene>

“子网络”是一个定义相当宽泛的术语，但可以说，子网络是任何支持你的
主网络或执行某些小任务的[网络](../ae2-mechanics/me-network-connections.md)。它们通常规模较小，小到不需要控制器。其两个最常见的用途通常是：

* 用于限制[设备](../ae2-mechanics/devices.md)可以访问哪些存储（你肯定不希望“管道”子网上的导入总线能访问主网
    存储，否则它会把物品放进你的存储元件，而不是目标容器中）。
* 用于节省主网络上的信道，例如让一个样板供应器输出到一个接口，而这个接口连接着若干台机器上的多个存储总线，
    这样只占用 1 个信道；而不是在每台机器上各放一个样板供应器，占用多个信道。

制作子网时，非常重要的一点是要理清[网络连接](../ae2-mechanics/me-network-connections.md)。
很多时候，人们把一堆接口、总线之类的东西胡乱拼在一起，就以为那是一个子网，
实际上所有设备仍然通过各种整块设备连接在主网络上。

不同颜色的线缆与创建子网络并没有关系，除了它们彼此不会互相连接这一点。

一些示例如下：

* 用一整套 AE2 网络替代你的垃圾桶/虚空升级，由它来决定如何最有效地利用你的垃圾。它会根据可用性和需求，智能地将物品输送到堆肥桶阵列或某些模组的回收机中。
* 构建抽象层。在子网络中管理复杂合成流程的所有细节，这样从主网络的视角来看，整个工厂“看起来”就像一台机器。
* 并行化。用 10 台相同的慢速机器替换掉一台慢速机器。从主网络的视角来看，什么都没有改变，而且你甚至不会占用更多频道。
* 使用导入总线和存储总线，将物品或流体从一个容器转移到另一个容器，就像物品管道或流体管道一样。
* 使用一个 ME破坏面板和存储总线，这样 ME破坏面板破坏掉的东西唯一能放入的位置就是存储总线，从而让你能够过滤这个面板。
* 使用接口和成型面板，这样无论什么东西被插入接口，都会被推送到成型面板并放置/丢弃到世界中。
* 搭建一套自动制造赛特斯石英的装置，并由主网络上的 <ItemLink id="level_emitter" /> 进行调节和控制。
* 通过特殊的“在接口上放置存储总线”交互，构建一个可从主网络访问的专用存储系统，用来存放农场产出，从而避免主存储被不断撑爆。
* 等等

对于构建子网络来说，<ItemLink id="quartz_fiber" /> 非常有用。它可以在不将网络连接起来的情况下在网络之间传输电力，让你无需到处放置能源接收器和电缆，也能为子网络供电。