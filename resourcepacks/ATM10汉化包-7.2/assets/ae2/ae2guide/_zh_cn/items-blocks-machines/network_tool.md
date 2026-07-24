---
navigation:
  parent: items-blocks-machines/items-blocks-machines-index.md
  title: 网络工具
  icon: network_tool
  position: 410
categories:
- tools
item_ids:
- ae2:network_tool
---

# 网络工具

<ItemImage id="network_tool" scale="4" />

网络工具是一种改造过的[扳手](wrench.md)，还会显示网络诊断信息，并且可以存储[升级卡](upgrade_cards.md)。
虽然它保留了扳手快速拆解物品以及从数据线上取下[子部件](../ae2-mechanics/cable-subparts.md)的能力，但它不能旋转物品。

它有 9 个槽位可用于存放[升级卡](upgrade_cards.md)，并且只要该工具位于你的物品栏中的任意位置，它们就能在任何 AE2 设备 UI 中使用。

右键点击网络的任意部分都会显示一个诊断信息窗口，类似于右键点击 <ItemLink id="controller" /> 时显示的窗口。
此窗口会显示

*   网络中正在使用的频道数量
*   用于切换全局设置，以 AE 或 E/FE 显示能量
*   网络中存储的[能量](../ae2-mechanics/energy.md)量，以及网络的最大能量容量
*   进入网络并被网络使用的能量数量
*   网络中所有 [ME设备](../ae2-mechanics/devices.md) 和组件的列表

当你摆弄[子网络](../ae2-mechanics/subnetworks.md)时，这个窗口也有助于判断两根不同的线缆或设备是否属于同一个网络。

## 隐藏伪装板

当任一只手持有网络工具时，<a href="facades.md">伪装板</a> 将会被隐藏。

你可以直接与隐藏伪装板后的方块交互，而无需先移除伪装板。

## 配方

<RecipeFor id="network_tool" />