---
navigation:
  parent: example-setups/example-setups-index.md
  title: 投水自动化
  icon: fluix_crystal
---

# “投水”配方的自动化

请注意，由于这里使用了<ItemLink id="pattern_provider" />，因此它是为了整合进你的[自动合成](../ae2-mechanics/autocrafting.md)
系统而设计的。

某些配方需要将物品投入水中（不过，类似的装置也可以用来将物品投掷到其他地方）。
这可以借助 <ItemLink id="formation_plane" />、<ItemLink id="annihilation_plane" /> 和一些配套
基础设施实现自动化（这本质上就是 2 个改造过的[管道子网络](pipe-subnet.md)）。

此设置旨在与[充电器自动化](charger-automation.md)配合使用，以提供这些<ItemLink id="charged_certus_quartz_crystal" />。

<GameScene zoom="6" interactive={true}>
  <ImportStructure src="../assets/assemblies/throw_in_water.snbt" />

<BoxAnnotation color="#dddddd" min="2 0 1" max="3 1 2">
        (1) 样板供应器：在其默认配置下，装有相应的处理样板。

        ![Fluix Pattern](../assets/diagrams/fluix_pattern_small.png) ![Flawed Budding Pattern](../assets/diagrams/flawed_budding_pattern_small.png)
  </BoxAnnotation>

<BoxAnnotation color="#dddddd" min="1.7 0 1" max="2 1 2">
        (2) 接口：使用默认配置。
  </BoxAnnotation>

<BoxAnnotation color="#dddddd" min="1 .7 1" max="2 1 2">
        （3）成型面板：设置为将输入以物品形式掉落。
  </BoxAnnotation>

<BoxAnnotation color="#dddddd" min="1 2 1" max="2 2.3 2">
        (4) ME破坏面板：没有可配置的 GUI。
  </BoxAnnotation>

<BoxAnnotation color="#dddddd" min="2 1 1" max="3 1.3 2">
        （5）存储总线：已过滤为样式的输出
        <Row><ItemImage id="fluix_crystal" scale="2" /><BlockImage id="flawless_budding_quartz" scale="2" /></Row>
  </BoxAnnotation>

<DiamondAnnotation pos="3.9 0.5 1.5" color="#00ff00">
        连接至主网络与充电器自动化
        <GameScene zoom="3" background="transparent">
          <ImportStructure src="../assets/assemblies/charger_automation.snbt" />
          <IsometricCamera yaw="195" pitch="30" />
        </GameScene>
    </DiamondAnnotation>

  <IsometricCamera yaw="180" pitch="0" />
</GameScene>

## 配置与样式

* <ItemLink id="pattern_provider" />（1）处于默认配置，并带有相关的 <ItemLink id="processing_pattern" />
  * 对于 <ItemLink id="fluix_crystal" />，使用 JEI/REI 中的默认配方即可：

    ![Fluix Pattern](../assets/diagrams/fluix_pattern.png)

* 对于 <ItemLink id="flawed_budding_quartz" />，最好直接用 <ItemLink id="quartz_block" /> 来制作，
    这样可以避免某个配方的输入是另一个配方的输出所带来的问题，从而导致存储总线无法进行过滤：

    ![Flawed Budding Pattern](../assets/diagrams/flawed_budding_pattern.png)

* <ItemLink id="interface" />（2）处于其默认配置。
* <ItemLink id="formation_plane" />（3）被设置为将输入作为物品丢出。
* <ItemLink id="annihilation_plane" />（4）没有 GUI，且无法进行配置。
* <ItemLink id="storage_bus" />（5）被过滤为这些图样的输出。

## 工作原理

1.  <ItemLink id="pattern_provider" /> 会将材料推入其侧面的 <ItemLink id="interface" /> 中，也就是绿色子网上的那个
2.  该接口（默认配置为不存储任何东西）会尝试将其内容推入[网络存储](../ae2-mechanics/import-export-storage.md)
3.  绿色子网上唯一的存储是 <ItemLink id="formation_plane" />，它会将接收到的物品丢进水里
4.  橙色子网上的 <ItemLink id="annihilation_plane" /> 会尝试拾取刚刚被丢下的物品，但无法做到，因为
    样板供应器顶部的 <ItemLink id="storage_bus" />（橙色子网上唯一的存储）被筛选为只接受可能合成结果
5.  这些物品会在世界中完成转化。
6.  现在，破坏面板可以拾取它前方的物品了，因为存储总线已被允许存储它们。
7.  存储总线会将生成的物品存入样板供应器，并将它们返回到网络中。