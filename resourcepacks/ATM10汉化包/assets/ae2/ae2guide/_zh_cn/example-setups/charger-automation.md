---
navigation:
  parent: example-setups/example-setups-index.md
  title: 充电器自动化
  icon: charger
---

# 充电器自动化

注意，由于这会使用 <ItemLink id="pattern_provider" />，它是设计为集成到你的[自动合成](../ae2-mechanics/autocrafting.md)
设置中的。如果你只是想单独自动化一个 <ItemLink id="charger" />，那就用漏斗、箱子之类的东西。

<ItemLink id="charger" /> 的自动化相当简单。<ItemLink id="pattern_provider" /> 会将材料推入充电器，然后由[管道子网](pipe-subnet.md)
或其他物流管道将产物推回供应器。

<GameScene zoom="6" interactive={true}>
  <ImportStructure src="../assets/assemblies/charger_automation.snbt" />

<BoxAnnotation color="#dddddd" min="1 0 0" max="2 1 1">
        (1) 样板供应器：在其默认配置下，配有相应的处理样板。同时还会为充电器供电。

        ![Charger Pattern](../assets/diagrams/charger_pattern_small.png)
  </BoxAnnotation>

<BoxAnnotation color="#dddddd" min="0 1 0" max="1 1.3 1">
        (2) 输入总线：使用默认配置。
  </BoxAnnotation>

<BoxAnnotation color="#dddddd" min="1 1 0" max="2 1.3 1">
        (3) 存储总线：使用默认配置。
  </BoxAnnotation>

<DiamondAnnotation pos="4 0.5 0.5" color="#00ff00">
        连接到主网络
    </DiamondAnnotation>

  <IsometricCamera yaw="195" pitch="30" />
</GameScene>

## 配置

* <ItemLink id="pattern_provider" /> (1) 处于默认配置，并带有相关的 <ItemLink id="processing_pattern" />。
  它还会为 <ItemLink id="charger" /> 提供 [能量](../ae2-mechanics/energy.md)，因为它的作用类似于 [线缆](../items-blocks-machines/cables.md)。
  
    ![Charger Pattern](../assets/diagrams/charger_pattern.png)

* <ItemLink id="import_bus" /> (2) 使用默认配置。
* <ItemLink id="storage_bus" /> (3) 使用默认配置。

## 工作原理

1. <ItemLink id="pattern_provider" /> 会将原料推入 <ItemLink id="charger" />。
2. 充电器会进行充电。
3. 绿色子网络上的 <ItemLink id="import_bus" /> 会将结果从充电器中拉出，并尝试将其存入
   [网络存储](../ae2-mechanics/import-export-storage.md)。
4. 绿色子网络上唯一的存储设备是 <ItemLink id="storage_bus" />，它会将生成的物品存入样板供应器，并将其返回主网络。