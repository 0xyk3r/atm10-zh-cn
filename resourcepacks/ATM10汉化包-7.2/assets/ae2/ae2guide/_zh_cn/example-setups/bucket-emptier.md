---
navigation:
  parent: example-setups/example-setups-index.md
  title: 桶清空器
  icon: minecraft:bucket
---

# 倒桶器

另见 [装桶器](bucket-filler.md)。

请注意，由于这里使用了<ItemLink id="pattern_provider" />，因此它是为了整合进你的[自动合成](../ae2-mechanics/autocrafting.md)
系统而设计的。

有时候情况就是这么不方便：你需要的是流体本身，但你却只能把这种流体做成桶装。有时机器也许能替你处理这个问题
（比如热力膨胀的流体转置机），但你不一定总有这样方便的模组可用。幸运的是，
原版 Minecraft 也提供了一种稍微没那么方便的办法，那就是 <ItemLink id="minecraft:dispenser" />。

<GameScene zoom="6" interactive={true}>
  <ImportStructure src="../assets/assemblies/bucket_emptier.snbt" />

<BoxAnnotation color="#dddddd" min="2 1 0" max="3 2 1">
        (1) 样板供应器：设置为在“With redstone signal”时锁定合成，并开启阻塞模式，放入相关的处理样板。

        <Row>
        ![Fill Pattern](../assets/diagrams/water_empty_pattern_small.png)
        ![Fill Pattern](../assets/diagrams/lava_empty_pattern_small.png)
        </Row>
  </BoxAnnotation>

<BoxAnnotation color="#dddddd" min="2.1 2 0.1" max="2.9 2.2 0.9">
        (2) 接口：使用默认配置。
  </BoxAnnotation>

<BoxAnnotation color="#dddddd" min="3.1 2 1.1" max="3.9 2.2 1.9">
        (3) 存储总线 #1：使用默认配置。
  </BoxAnnotation>

<BoxAnnotation color="#dddddd" min="4.05 1.05 0.8" max="4.95 1.95 1">
        (4) ME破坏面板：没有可配置的 GUI。
  </BoxAnnotation>

<BoxAnnotation color="#dddddd" min="3.2 1.2 0.8" max="3.8 1.8 1">
        (5) 输入总线：筛选为桶。
        <ItemImage id="minecraft:bucket" scale="2" />
  </BoxAnnotation>

<BoxAnnotation color="#dddddd" min="3 1.1 0.1" max="3.2 1.9 0.9">
        (6) 存储总线 #2：使用默认配置。
  </BoxAnnotation>

<DiamondAnnotation pos="0 1.5 0.5" color="#00ff00">
        连接到主网络
    </DiamondAnnotation>

  <IsometricCamera yaw="225" pitch="45" />
</GameScene>

## 配置

* <ItemLink id="pattern_provider" />（1）已设置为在“With redstone signal”时锁定合成，并开启阻塞模式，
  放入相关的 <ItemLink id="processing_pattern" />。
  
    ![Charger Pattern](../assets/diagrams/water_empty_pattern.png)
    ![Charger Pattern](../assets/diagrams/lava_empty_pattern.png)

* <ItemLink id="interface" />（2）处于默认配置。
* 第一个 <ItemLink id="storage_bus" />（3）处于默认配置。
* <ItemLink id="annihilation_plane" />（4）没有 GUI，无法配置。
* <ItemLink id="import_bus" />（5）被筛选为桶。
  <ItemImage id="minecraft:bucket" scale="2" />
* 第二个 <ItemLink id="storage_bus" />（6）处于默认配置。

## 工作原理

1. <ItemLink id="pattern_provider" /> 将原料推入 <ItemLink id="interface" />。
   （实际上，作为一种优化，它会通过存储总线直接推送过去，就像它是供应器表面的延伸一样。物品实际上从未进入接口。）
2. 通过 [管道子网](pipe-subnet.md#providing-to-multiple-places) 中描述的机制，
   桶最终会进入 <ItemLink id="minecraft:dispenser" />。
3. <ItemLink id="minecraft:comparator" /> 检测到桶位于发射器中，因此会同时为发射器供能并锁定
   <ItemLink id="pattern_provider" />。
4. 发射器会倒出桶中的流体，此时它内部就有了一个空桶。
5. <ItemLink id="import_bus" /> 将空桶从发射器中拉出，并通过
   <ItemLink id="storage_bus" /> 存入样板供应器，使其返回主网络。
6. 比较器检测到发射器为空，于是解锁供应器。