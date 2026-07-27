---
navigation:
  parent: items-blocks-machines/items-blocks-machines-index.md
  title: 无线访问点
  icon: wireless_access_point
  position: 210
categories:
- devices
item_ids:
- ae2:wireless_booster
- ae2:wireless_access_point
---

# 无线接入点

<BlockImage id="wireless_access_point" p:state="has_channel" scale="8" />

允许通过 <ItemLink id="wireless_terminal" /> 进行无线访问。
范围和耗电量由已安装的 <ItemLink id="wireless_booster" /> 数量决定。

一个网络可以拥有任意数量的无线接入点，每个接入点中也可以有任意数量的 <ItemLink id="wireless_booster" />，让你能够通过调整配置来优化能耗和范围。

需要一个[频道](../ae2-mechanics/channels.md)。

也可用于绑定[无线终端](wireless_terminals.md)

# 无线延长器

<ItemImage id="wireless_booster" scale="2" />

用于增加无线接入点的范围。

## 配方

<RecipeFor id="wireless_access_point" />

<RecipeFor id="wireless_booster" />