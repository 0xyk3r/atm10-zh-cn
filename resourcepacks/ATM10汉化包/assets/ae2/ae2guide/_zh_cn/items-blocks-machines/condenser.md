---
navigation:
  parent: items-blocks-machines/items-blocks-machines-index.md
  title: 物质聚合器
  icon: condenser
  position: 310
categories:
- machines
item_ids:
- ae2:condenser
---

# 物质聚合器

<BlockImage id="condenser" scale="8" />

物质凝聚器既可以用作垃圾桶，也可以用来制造 <ItemLink id="matter_ball" />
[奇点](singularities.md)。它可以接收存储元件能够存储的任何物品、流体等内容。

## 设置/配方

*   在垃圾桶模式下，物质凝聚器会直接销毁所有进入其中的东西
*   在物质球模式下，凝聚器会将你放入其中的任何东西制成 <ItemLink id="matter_ball" />。
    此模式要求你在凝聚器的顶部槽位中放入一个存储组件。每个物质球需要 256 个物品或桶，
    因此一个 <ItemLink id="cell_component_1k" />（可提供 8192 bit 的容量）就绰绰有余了。
*   在物质奇点模式下，凝聚器会将你放入其中的任何东西制成 [奇点](singularities.md)。
    此模式要求你在凝聚器的顶部槽位中放入一个存储组件。每个奇点需要 256,000 个物品或桶，
    因此一个 <ItemLink id="cell_component_64k" />（可提供 524,288 bit 的容量）就绰绰有余了。

请注意，在后两种会产出某种资源的模式下，如果能量缓冲区和产出物品缓冲区都被完全填满，物质聚合器*可能会堵塞*，并且将不再接受任何进一步的输入。

## 配方

<RecipeFor id="condenser" />