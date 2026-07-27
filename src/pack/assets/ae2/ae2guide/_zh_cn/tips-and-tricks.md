---
navigation:
  title: 提示和技巧
  position: 20
---

# 提示与技巧

一堆零散的小建议

* 别装 Optifine
* 导览书里带缩放与批注显示/隐藏按钮的场景，是可以旋转和放大的
* 网络布局尽量做成树状，别接成环
* 除非你非常清楚[频道](ae2-mechanics/channels.md)在网络里是怎么走的，否则整块型[设备](ae2-mechanics/devices.md)
  每组不要超过 8 个
* 选定一种木头，所有[样板](items-blocks-machines/patterns.md)都用它。样板的物品替换有时候确实管用，
  但从头到尾只用同一种木头能省掉大量麻烦。
* 把[样板](items-blocks-machines/patterns.md)竖着排进<ItemLink id="pattern_access_terminal" />／
  分散到多个[样板供应器](items-blocks-machines/pattern_provider.md)上，配方就能并行执行。
* 接一块[储能元件](items-blocks-machines/energy_cells.md)，网络就扛得住用电尖峰。
* <ItemLink id="condenser" />里可以用水
* 想让网络保持干净，最有效的办法是别往里塞剑、盔甲这类杂七杂八的怪物掉落物——
  附魔与耐久每换一种组合，就多占一个[类型](ae2-mechanics/bytes-and-types.md)。
* [处理样板](items-blocks-machines/patterns.md)的产物回到系统时，必须触发一次「物品进入系统」事件，
  也就是要走<ItemLink id="import_bus" />、<ItemLink id="interface" />或<ItemLink id="pattern_provider" />的返回槽；
  光把产物用管道塞进一个贴着<ItemLink id="storage_bus" />的箱子是不行的。
* 别忘了，导览书里带缩放与批注显示/隐藏按钮的场景是可以旋转和放大的
* <ItemLink id="pattern_provider" />只会整批推送配方材料，而且只从一个面推。这一点在「不让机器收到半批材料」
  时很有用，但有时候你就是想把材料分送到多个地方。这时可以用<ItemLink id="interface" />：
  既能当作[「管道」子网](example-setups/pipe-subnet.md)，也可以利用它同时存放多种物品、流体、化学品的能力，
  把它当成一个中转箱／中转罐。
* 导览书里带缩放与批注显示/隐藏按钮的场景，可以缩放也可以旋转
