---
navigation:
  parent: example-setups/example-setups-index.md
  title: 桶填充器
  icon: minecraft:water_bucket
---

# 装桶器

另见 [倒桶器](bucket-emptier.md)。

请注意，由于这里使用了<ItemLink id="pattern_provider" />，因此它是为了整合进你的[自动合成](../ae2-mechanics/autocrafting.md)
系统而设计的。

有时候情况就是这么不方便：你需要的是某种流体桶，而不是流体本身。有时机器也许能替你处理这个问题
（比如热力膨胀的流体转置机），但你不一定总有这样方便的模组可用。幸运的是，
原版 Minecraft 也提供了一种稍微没那么方便的办法，那就是 <ItemLink id="minecraft:dispenser" />。

**注意，你通常并不需要这么做，因为
[样板编码终端](../items-blocks-machines/terminals.md#pattern-encoding-terminal)中的流体替换允许你在
合成配方中直接使用流体本身，而不是桶。**

<GameScene zoom="6" interactive={true}>
  <ImportStructure src="../assets/assemblies/bucket_filler.snbt" />

<BoxAnnotation color="#dddddd" min="2 1 0" max="3 2 1">
        (1) 样板供应器：设置为在“With redstone signal”时锁定合成，放入相关的处理样板。

        <Row>
        ![Fill Pattern](../assets/diagrams/water_fill_pattern_small.png)
        ![Fill Pattern](../assets/diagrams/lava_fill_pattern_small.png)
        </Row>
  </BoxAnnotation>

<BoxAnnotation color="#dddddd" min="3 1.1 0.1" max="3.2 1.9 0.9">
        (2) 接口：使用默认配置。
  </BoxAnnotation>

<BoxAnnotation color="#dddddd" min="3.1 1.1 0.8" max="3.9 1.9 1">
        (3) 存储总线 #1：使用默认配置。
  </BoxAnnotation>

<BoxAnnotation color="#dddddd" min="4.05 1.05 0.8" max="4.95 1.95 1">
        (4) 成型面板：筛选为将桶列入黑名单，并使用反转卡。
        <Row><ItemImage id="minecraft:bucket" scale="2" /><ItemImage id="inverter_card" scale="2" /></Row>
  </BoxAnnotation>

<BoxAnnotation color="#dddddd" min="3.2 2 1.2" max="3.8 2.2 1.8">
        (5) 输入总线：筛选为将桶列入黑名单，并使用反转卡。
        <Row><ItemImage id="minecraft:bucket" scale="2" /><ItemImage id="inverter_card" scale="2" /></Row>
  </BoxAnnotation>

<BoxAnnotation color="#dddddd" min="2.1 2 0.1" max="2.9 2.2 0.9">
        (6) 存储总线 #2：使用默认配置。
  </BoxAnnotation>

<DiamondAnnotation pos="0 1.5 0.5" color="#00ff00">
        连接到主网络
    </DiamondAnnotation>

  <IsometricCamera yaw="225" pitch="45" />
</GameScene>

## 配置

* <ItemLink id="pattern_provider" />（1）已设置为在“With redstone signal”时锁定合成，放入相关的 <ItemLink id="processing_pattern" />。
  
    ![Charger Pattern](../assets/diagrams/water_fill_pattern.png)
    ![Charger Pattern](../assets/diagrams/lava_fill_pattern.png)

* <ItemLink id="interface" />（2）处于默认配置。
* 第一个 <ItemLink id="storage_bus" />（3）处于默认配置。
* <ItemLink id="formation_plane" />（4）使用反转卡筛选为桶黑名单。
  <Row><ItemImage id="minecraft:bucket" scale="2" /><ItemImage id="inverter_card" scale="2" /></Row>
* <ItemLink id="import_bus" />（5）使用反转卡筛选为桶黑名单。
  <Row><ItemImage id="minecraft:bucket" scale="2" /><ItemImage id="inverter_card" scale="2" /></Row>
* 第二个 <ItemLink id="storage_bus" />（6）处于默认配置。

## 工作原理

1. <ItemLink id="pattern_provider" /> 会将材料送入 <ItemLink id="interface" />。
   （实际上，作为一种优化，它会像存储总线和成型面板是供应器各个面的延伸一样，直接经由它们推送过去。物品实际上从未进入接口。）
2. 通过[管道子网络](pipe-subnet.md#providing-to-multiple-places) 和 <ItemLink id="formation_plane" />中描述的机制，
   桶最终会进入 <ItemLink id="minecraft:dispenser" />，并由成型面板放置流体。
3. <ItemLink id="minecraft:comparator" /> 会检测到发射器中的桶，因此会同时为发射器供电并锁定
   <ItemLink id="pattern_provider" />。
4. 发射器会用桶舀起流体，这样它内部现在就有了一个装满流体的桶。
5. <ItemLink id="import_bus" /> 会将装满流体的桶从发射器中拉出，并经由
   <ItemLink id="storage_bus" /> 将其存入样板供应器，使其返回主网络。
6. 比较器会检测到发射器已空，从而解除供应器的锁定。