---
navigation:
  parent: items-blocks-machines/items-blocks-machines-index.md
  title: 处理器
  icon: logic_processor
  position: 8
categories:
- misc ingredients blocks
item_ids:
- ae2:logic_processor
- ae2:calculation_processor
- ae2:engineering_processor
- ae2:printed_silicon
- ae2:printed_logic_processor
- ae2:printed_calculation_processor
- ae2:printed_engineering_processor
- ae2:silicon
---

# 处理器

<Row>
  <ItemImage id="logic_processor" scale="4" />

  <ItemImage id="calculation_processor" scale="4" />

  <ItemImage id="engineering_processor" scale="4" />
</Row>

处理器是应用能源 [devices](../ae2-mechanics/devices.md) 和机器的主要材料之一。它们也是你最早会遇到的
大型自动化挑战之一。处理器共有三种类型，分别使用金、<ItemLink id="certus_quartz_crystal" />
和钻石制成。它们要使用 [presses](presses.md) 在 <ItemLink id="inscriber" /> 中，经过多步骤
流程制成（通常通过一系列压印器和过滤管道来实现）。

## 生产步骤

<Column gap="5">
  1.  收集/制作所需材料：硅单质、红石、金矿、<ItemLink id="certus_quartz_crystal" />、钻石。

  <RecipeFor id="silicon" />

  <br />

  2. 压制所需的印刷电路前置组件

  <Row>
    <RecipeFor id="printed_silicon" />

    <RecipeFor id="printed_logic_processor" />
  </Row>

  <Row>
    <RecipeFor id="printed_calculation_processor" />

    <RecipeFor id="printed_engineering_processor" />
  </Row>

  <br />

  3.  最终组装

  <Row>
    <RecipeFor id="logic_processor" />

    <RecipeFor id="calculation_processor" />
  </Row>

  <RecipeFor id="engineering_processor" />
</Column>