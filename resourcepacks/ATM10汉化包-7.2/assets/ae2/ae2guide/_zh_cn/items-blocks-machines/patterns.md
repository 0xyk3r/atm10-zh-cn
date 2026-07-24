---
navigation:
  parent: items-blocks-machines/items-blocks-machines-index.md
  title: 样板
  icon: crafting_pattern
  position: 410
categories:
- tools
item_ids:
- ae2:blank_pattern
- ae2:crafting_pattern
- ae2:processing_pattern
- ae2:smithing_table_pattern
- ae2:stonecutting_pattern
---

# 样式

<ItemImage id="crafting_pattern" scale="4" />

样板是在 <ItemLink id="pattern_encoding_terminal" /> 中由空白样板制成的，并插入到 <ItemLink id="pattern_provider" /> 或
<ItemLink id="molecular_assembler" /> 中。

针对不同用途，有几种不同类型的样板：

*   <ItemLink id="crafting_pattern" />可对工作台制作的配方进行编码。它们可以直接放入 <ItemLink id="molecular_assembler" /> 中，使其在获得材料时制作出结果，但它们的主要用途是放在分子装配室旁边的 <ItemLink id="pattern_provider" /> 中。
    在这种情况下，样板供应器具有特殊行为，会将对应的样板连同材料一起发送到相邻的组装机中。
    由于组装机会将合成结果自动弹出到相邻容器中，因此，要自动化合成样板，只需要在样板供应器上放置一台组装机即可。

***

*   <ItemLink id="smithing_table_pattern" />与合成样板非常相似，但它们记录的是锻造台配方。它们同样可以通过样板供应器
    和分子装配室自动化，且工作方式完全相同。实际上，合成、锻造和切石机样板都可以
    在同一套布局中使用。

***

*   <ItemLink id="stonecutting_pattern" /> 与合成样板非常相似，但它们编码的是切石机配方。它们同样可以由样板供应器和分子装配室自动化，且工作方式完全相同。事实上，合成、铁匠和切石机样板可以在同一套布局中使用。

***

*   <ItemLink id="processing_pattern" />s 是自动合成拥有高度灵活性的主要来源。它们是最通用的一类，本质上只是
    在说：“如果样板供应器将这些材料推送到相邻的容器中，那么 ME 系统迟早会在某个时候收到这些物品。”
    你会用它们来通过几乎任何模组机器进行自动合成，也可以用于熔炉之类的设备。正因为它们用途如此
    广泛，而且完全不关心从推送材料到收到结果之间发生了什么，你就可以玩出很多非常离谱的花活，比如把
    材料输入到一整套复杂的工厂生产链中，让它自动分拣物品、从无限产出的农场中获取其他材料、打印出整部《三倍大的蜜蜂总动员》剧本——
    只要 ME 系统最终收到了样板所指定的结果，它就根本不在乎。事实上，
    它甚至不在乎这些材料和结果之间是否有任何关系。你完全可以告诉它“1 个樱桃橡木木板 = 1 个下界之星”，然后让
    你的凋灵农场在收到一个樱桃橡木木板后击杀一只凋灵，这样同样也能正常运作。

支持多个具有相同配方的 <ItemLink id="pattern_provider" /> 同时并行工作。此外，你还可以让配方设定为例如 8 个圆石 = 8 个石子，而不是 1 个圆石 = 1 个石子，这样配方提供器每次运行时都会向你的烧炼装置中一次性插入 8 个圆石，而不是每次只插入 1 个。

## 配方

<RecipeFor id="blank_pattern" />