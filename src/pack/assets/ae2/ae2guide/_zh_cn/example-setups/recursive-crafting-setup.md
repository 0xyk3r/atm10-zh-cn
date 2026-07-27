---
navigation:
  parent: example-setups/example-setups-index.md
  title: 递归合成
  icon: minecraft:netherite_upgrade_smithing_template
---

# 一个递归合成布局

正如[自动合成](../ae2-mechanics/autocrafting.md)中所述，自动合成的规划算法无法处理主产物同时又是输入之一的配方。
例如，它无法处理复制 <ItemLink id="minecraft:netherite_upgrade_smithing_template" />。

一种解决方案是利用 <ItemLink id="level_emitter" /> 伪装成 [样板](../items-blocks-machines/patterns.md) 的能力。

随后，这将用于启动一个持续执行该合成的小型装置。在这个例子中，我们将看看如何搭建一个
复制 <ItemLink id="minecraft:netherite_upgrade_smithing_template" /> 的装置。

<RecipeFor id="minecraft:netherite_upgrade_smithing_template" />

***

<GameScene zoom="6" interactive={true}>
  <ImportStructure src="../assets/assemblies/recursive_recipe_setup.snbt" />

  <BoxAnnotation color="#dddddd" min="1 0 0" max="2 1 1">
        （1）接口：设置为储备所需的额外材料：钻石和下界岩。
        <Row><ItemImage id="minecraft:diamond" scale="2" /> <ItemImage id="minecraft:netherrack" scale="2" /></Row>
  </BoxAnnotation>

  <BoxAnnotation color="#dddddd" min="2.3 1 0.3" max="2.7 1.3 0.7">
        (2) 存储状态发信器：配置为“下界合金锻造模板”，设为“发出红石信号以合成物品”。
        <Row><ItemImage id="minecraft:netherite_upgrade_smithing_template" scale="2" /> <ItemImage id="crafting_card" scale="2" /></Row>
  </BoxAnnotation>

  <BoxAnnotation color="#dddddd" min="2 0 0" max="2.3 1 1">
        （3）导入总线 #1：过滤为接口正在补货的物品。安装了一张红石卡。红石模式设置为
        “有信号时激活”。
        <Row>
        <ItemImage id="minecraft:diamond" scale="2" />
        <ItemImage id="minecraft:netherrack" scale="2" />
        <ItemImage id="redstone_card" scale="2" />
        </Row>
  </BoxAnnotation>

  <BoxAnnotation color="#dddddd" min="3 1 1" max="4 1.3 2">
        （4）存储总线 #1：设置为比另一个存储总线更高的优先级。非常重要。
  </BoxAnnotation>

  <BoxAnnotation color="#dddddd" min="3 0 1" max="4 1 2">
        （5）分子装配室：其中包含用于复制锻造模板的样板。

        ![Pattern](../assets/diagrams/smithing_template_pattern_small.png)

        第一次搭建时，还要手动往里放一个锻造模板。
  </BoxAnnotation>

  <BoxAnnotation color="#dddddd" min="2.7 0 1" max="3 1 2">
        (6) 导入总线 #2：使用默认配置。
  </BoxAnnotation>

  <BoxAnnotation color="#dddddd" min="1 0 1" max="2 1 1.3">
        (7) 存储总线 #2：筛选为“下界合金锻造模板”。其优先级设置得低于另一个存储总线。
        <ItemImage id="minecraft:netherite_upgrade_smithing_template" scale="2" />
  </BoxAnnotation>

<DiamondAnnotation pos="0 0.5 0.5" color="#00ff00">
        连接到主网络
    </DiamondAnnotation>

  <IsometricCamera yaw="15" pitch="30" />
</GameScene>

## 配置

* 将 <ItemLink id="interface" />（1）设置为储备所需的额外材料：钻石和下界岩。
* 将 <ItemLink id="level_emitter" />（2）配置为“下界合金锻造模板”，并设置为“发出红石信号以合成物品”。
* 第一个 <ItemLink id="import_bus" />（3）被筛选为接口正在储备的物品。它装有一张红石卡。红石模式设置为“收到信号工作”。
* 将第一个 <ItemLink id="storage_bus" />（4）设置为比第二个存储总线具有*更高*的[优先级](../ae2-mechanics/import-export-storage.md#storage-priority)。
* <ItemLink id="molecular_assembler" />（5）中放有用于复制锻造模板的样板，并且已经手动放入了一个锻造模板。

  ![Pattern](../assets/diagrams/smithing_template_pattern.png)

* 第二个 <ItemLink id="import_bus" />（6）处于默认配置。
* 第二个 <ItemLink id="storage_bus" />（7）被筛选为“下界合金锻造模板”。它的[优先级](../ae2-mechanics/import-export-storage.md#storage-priority)比第一个存储总线*更低*。

## 工作原理

1. 由于插入了 <ItemLink id="crafting_card" />，并将其设置为“发出红石信号以合成物品”，<ItemLink id="level_emitter" /> 会伪装成一个 [pattern](../items-blocks-machines/patterns.md)。因此，“下界合金锻造模板”会在 [terminals](../items-blocks-machines/terminals.md) 中显示为可 [autocraft](../ae2-mechanics/autocrafting.md) 的有效项目。
2. 当收到合成该物品的请求时，无论是来自玩家还是系统自身，能级发信器都会开启。
3. 第一个 <ItemLink id="import_bus" /> 会被能级发信器激活，并从 <ItemLink id="interface" /> 中拉出已储备的材料。
4. 网络上唯一能够存储这些材料的 <ItemLink id="storage_bus" />，就是装配器上的那个。
5. <ItemLink id="molecular_assembler" /> 会接收这些材料（其内部已经有 1 个锻造样板），并执行合成，产出 2 个锻造样板。
6. 第二个 <ItemLink id="import_bus" /> 会取出 1 个锻造样板。
7. 第一个存储总线的优先级更高，因此这个锻造样板会回到装配器中。
8. 第二个 <ItemLink id="import_bus" /> 会取出 1 个锻造样板。
9. 装配器无法再接收另一个锻造样板，因此第二个锻造样板会进入优先级较低的存储总线，并被插入到接口中。
10. 由于 <ItemLink id="interface" /> 未被设置为储备锻造样板，它会将其插入网络中。