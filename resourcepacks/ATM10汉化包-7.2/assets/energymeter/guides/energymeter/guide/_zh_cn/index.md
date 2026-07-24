---
navigation:
  title: 电能表
  icon: meter
item_ids:
- meter
---

# 电能表

欢迎了解**电能表**模组！

<br clear="all" />

![](assets/preview.png)

<FloatingImage src="assets/logo.png" align="right"/>

电能表是一个小型内容模组，添加了一种名为<ItemLink id="meter" components="rarity=epic"/>的方块，可用于测量能量流速。
该方块功能类似电缆：输入请求会直接转发至输出端。所有请求的数值均被储存，并在可配置的时间间隔内用于计算流速。

除了功能完备的用户界面外，该方块正面还配备了一个数字显示屏，可随时查看当前流速。显示屏支持任意方向旋转，包括向上和向下。由于电能表正面专用于显示，因此仅剩余五个侧面可配置为输入或输出。

若需回顾此前各时间间隔的流速数据，电能表的用户界面还包含图表视图。该视图显示最近10个时间间隔的测量结果，并支持暂停功能。界面还提供大量其他配置选项：除多种测量方式外，还可调整测量时间间隔与计算模式。<br/>
更多详情请参阅[界面](interface.md)页面。

<br clear="all" />
<RecipeFor id="meter"/>