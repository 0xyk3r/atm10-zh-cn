---
navigation:
  parent: expandedae-index.md
  title: 生活质量特性
  icon: expandedae:exp_pattern_provider
  position: 10
categories:
- expandedae
---

# 该模组添加了以下所有生活质量（QoL）特性
## 样板供应器内的样板乘法：为样板供应器新增一个按钮，允许您对其中全部样板进行乘法或除法运算
__乘数效果可叠加！__

![modify_patterns.png](assets/modify_patterns.png)
## 额外阻塞模式：为所有样板供应器新增两种阻塞模式
### 默认：此为应用能源2默认的阻塞模式，当连接的存储中不包含当前样板供应器内任一样板输入项时，将推送样板；若存储中存在非该样板输入项的其他物品，阻塞模式会忽略该项并继续推送样板。
    
![blocking_1.png](assets/blocking/blocking_1.png)

### 完全阻塞：此阻塞模式下，若连接的存储中存有任何物品，则不会推送样板。
    
![blocking_2.png](assets/blocking/blocking_2.png)

### 智能：若目标存储中仅包含该特定样板的输入项，则允许样板供应器推送相同的样板

![blocking_3.png](assets/blocking/blocking_3.png)