---
navigation:
  parent: example-setups/example-setups-index.md
  title: 熔炉自动化
  icon: minecraft:furnace
---

# 熔炉自动化

请注意，由于这里使用了 <ItemLink id="pattern_provider" />，它旨在集成到你的 [自动合成](../ae2-mechanics/autocrafting.md)
配置中。如果你只是想单独自动化一个熔炉，就用漏斗、箱子之类的东西。

<ItemLink id="minecraft:furnace" /> 的自动化比像 [charger](../example-setups/charger-automation.md) 这样的简单机器的自动化要稍微复杂一些。  
熔炉需要从两个不同的面输入，并从第三个面抽取。要被冶炼的物品必须从顶部面推入，
燃料必须从侧面推入，而结果必须从底部取出。

这可以通过以下方式实现：顶部放置一个 <ItemLink id="pattern_provider" />，侧面放置一个 <ItemLink id="export_bus" /> 以持续输入燃料，底部放置一个 <ItemLink id="import_bus" /> 将结果导入网络。不过，这会占用 3 个[频道](../ae2-mechanics/channels.md)。

以下是只用 1 个频道的做法：

<GameScene zoom="6" interactive={true}>
  <ImportStructure src="../assets/assemblies/furnace_automation.snbt" />

<BoxAnnotation color="#dddddd" min="1 0 0" max="2 1 1">
        (1) 样板供应器：可使用赛特斯石英扳手调整朝向的变种，其中放入相应的处理样板。

        ![Iron Pattern](../assets/diagrams/furnace_pattern_small.png)
  </BoxAnnotation>

<BoxAnnotation color="#dddddd" min="1 1 0" max="2 1.3 1">
        (2) 接口：使用默认配置。
  </BoxAnnotation>

<BoxAnnotation color="#dddddd" min="1 1 0" max="1.3 2 1">
        (3) 存储总线 #1：过滤为煤炭。
        <ItemImage id="minecraft:coal" scale="2" />
  </BoxAnnotation>

<BoxAnnotation color="#dddddd" min="0 2 0" max="1 2.3 1">
        (4) 存储总线 #2：筛选为将煤炭列入黑名单，并使用反转卡。
        <Row><ItemImage id="minecraft:coal" scale="2" /><ItemImage id="inverter_card" scale="2" /></Row>
  </BoxAnnotation>

<DiamondAnnotation pos="4 0.5 0.5" color="#00ff00">
        连接到主网络
    </DiamondAnnotation>

  <IsometricCamera yaw="195" pitch="30" />
</GameScene>

## 配置

* <ItemLink id="pattern_provider" />（1）处于默认配置，并带有相应的<ItemLink id="processing_pattern" />。
    对其使用 <ItemLink id="certus_quartz_wrench" /> 后，它就会变为有方向性。

  ![Iron Pattern](../assets/diagrams/furnace_pattern.png)

* <ItemLink id="interface" />（2）处于其默认配置。
* 第一个 <ItemLink id="storage_bus" />（3）被筛选为煤炭，或者你想使用的任何燃料。
* 第二个 <ItemLink id="storage_bus" />（4）被筛选为将你正在使用的燃料加入黑名单，方法是使用一个 <ItemLink id="inverter_card" />。

## 工作原理

1. <ItemLink id="pattern_provider" />把材料推进<ItemLink id="interface" />。
   （实际上出于优化，它是直接穿过存储总线推的，就好像那些总线是供应器自己的面一样——材料从来没真正进过接口。）
2. 接口被设为不存放任何东西，于是它试着把材料推进[网络存储](../ae2-mechanics/import-export-storage.md)。
3. 绿色子网上唯一的存储就是那两个<ItemLink id="storage_bus" />。过滤为煤炭的那个从侧面把煤炭放进熔炉的燃料槽；
    过滤为「非煤炭」的那个从顶面把待冶炼的物品放进上方槽位。
4. 熔炉干它该干的活
5. 漏斗从熔炉底部把产物抽出来，放进供应器的返回槽，产物就回到主网络了。