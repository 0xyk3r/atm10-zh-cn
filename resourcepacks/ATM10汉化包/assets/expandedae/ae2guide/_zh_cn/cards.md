---
navigation:
  parent: expandedae-index.md
  title: 升级卡
  icon: auto_complete_card
  position: 5
categories:
- expandedae
item_ids:
- expandedae:auto_complete_card
- expandedae:pattern_refiller_card
---

## 当前，该模组仅添加了以下两种升级卡片
- 自动完成卡：此卡片用于升级样板供应器，一旦推送样板便会自动取消合成任务。
_注意：与合成类样板配合使用时会导致异常，请谨慎使用_
<ItemImage id="auto_complete_card" />
- 空白样板重填卡：此卡片用于升级 <ItemLink id="wireless_exp_encoding_terminal" /> 与 <ItemLink id="ae2wtlib:wireless_universal_terminal" />，可自动为拓充样板编码终端中的空白样板槽位补充样板

_注意：该卡片仅在每次点击编码按钮时尝试补充样板，这是资源消耗最低的实现方案_
<ItemImage id="pattern_refiller_card" />