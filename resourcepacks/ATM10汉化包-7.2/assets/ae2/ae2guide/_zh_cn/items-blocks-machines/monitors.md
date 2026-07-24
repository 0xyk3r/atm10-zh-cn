---
navigation:
  parent: items-blocks-machines/items-blocks-machines-index.md
  title: 监控器
  icon: storage_monitor
  position: 210
categories:
- devices
item_ids:
- ae2:storage_monitor
- ae2:conversion_monitor
---

# 监视器

<GameScene zoom="8" background="transparent">
<ImportStructure src="../assets/assemblies/monitors.snbt" />
<IsometricCamera yaw="195" pitch="30" />
</GameScene>

监视器可让你在不打开 GUI 的情况下，对单一种类的物品或流体进行可视化与交互。

监视器会继承其所安装在[cable](cables.md)上的颜色。

如果监视器放在地板或天花板上，你可以用<ItemLink id="certus_quartz_wrench" />旋转它。

它们是[线缆部件](../ae2-mechanics/cable-subparts.md)。

# 存储监视器

会显示一种物品或流体及其数量。把它们放在你的农场旁边之类的地方……

*不*需要[频道](../ae2-mechanics/channels.md)。

按键绑定：

*   手持物品右击，或用流体容器双击右击，将监控器设置为该物品/流体。
*   空手右击以清除监控器。
*   空手 Shift+右击以锁定监控器。

## 配方

<RecipeFor id="storage_monitor" />

# 转换监视器

转换监控器与存储监控器类似，但允许你插入或提取其配置的物品。

如果配置的物品是[可自动合成](../ae2-mechanics/autocrafting.md)，且存储中没有该物品，那么尝试取出该物品时，将会改为打开一个界面以指定要合成的数量。

*确实*需要一个[频道](../ae2-mechanics/channels.md)。

额外按键绑定：

*   左键点击可提取一组已配置的物品；如果存储中没有，则会请求合成该物品。
*   手持任意物品右键点击可插入该物品。
*   空手右键点击可将你物品栏中所有已配置的物品全部插入。

## 配方

<RecipeFor id="conversion_monitor" />