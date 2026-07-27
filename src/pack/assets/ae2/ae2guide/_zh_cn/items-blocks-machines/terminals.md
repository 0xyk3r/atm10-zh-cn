---
navigation:
  parent: items-blocks-machines/items-blocks-machines-index.md
  title: 终端
  icon: crafting_terminal
  position: 210
categories:
- devices
item_ids:
- ae2:terminal
- ae2:crafting_terminal
- ae2:pattern_encoding_terminal
- ae2:pattern_access_terminal
---

# 终端

<GameScene zoom="6" background="transparent">
  <ImportStructure src="../assets/assemblies/terminals.snbt" />
  <IsometricCamera yaw="195" pitch="30" />
</GameScene>

虽然 <ItemLink id="pattern_provider" />s、<ItemLink id="import_bus" />ses、<ItemLink id="storage_bus" />ses 等等是 AE2 网络与世界交互的主要方式，但终端则是 AE2 网络与你 *本人* 交互的主要方式。终端有多个变种，功能各不相同。

终端会继承其所安装在[cable](cables.md)上的颜色。

它们是[线缆部件](../ae2-mechanics/cable-subparts.md)。

## 终端放置

由于终端通常是玩家最先放置的[subpart](../ae2-mechanics/cable-subparts.md)之一，
因此经常会放错，把终端背面朝外放置。下面是该怎么做和不该怎么做的示例：

<GameScene zoom="6" background="transparent">
  <ImportStructure src="../assets/assemblies/terminal_placement.snbt" />
  <IsometricCamera yaw="195" pitch="30" />

  <LineAnnotation color="#ff3333" from="2.5 .5 .5" to="4.5 2.5 .5" alwaysOnTop={true} thickness="0.05"/>
  <LineAnnotation color="#ff3333" from="2.5 2.5 .5" to="4.5 .5 .5" alwaysOnTop={true} thickness="0.05"/>

  <LineAnnotation color="#33ff33" from="-.5 2.5 .5" to="1 .5 .5" alwaysOnTop={true} thickness="0.05"/>
  <LineAnnotation color="#33ff33" from="1 .5 .5" to="1.5 1 .5" alwaysOnTop={true} thickness="0.05"/>
</GameScene>

你仍然有一个终端和一个能源接收器，只不过现在终端的朝向正确了，而且也确实连接到了网络上，整体还占用更小的空间。

<a name="terminal-ui"></a>

# 终端搜索

搜索框支持 Regex 表达式，因此你可以例如输入“gtceu:.*ore”来获取 Gregtech 的所有矿石。至于学习
Regex，就留给读者自己练习吧。

# 终端

<GameScene zoom="6" background="transparent">
  <ImportStructure src="../assets/blocks/terminal.snbt" />
  <IsometricCamera yaw="180" />
</GameScene>

你的基础终端，可让你查看并访问[网络存储器](../ae2-mechanics/import-export-storage.md)中的内容，
并从你的[自动合成](../ae2-mechanics/autocrafting.md)系统中请求物品。

## 界面

基础终端的 UI 分为几个部分

中间区域可用于访问你网络的存储。你可以将物品放入其中，也可以从中取出。有几个
鼠标/按键快捷操作：

*   左击会抓取一组物品，右击会抓取半组物品。
*   如果某个物品、流体等可以被[自动合成](../ae2-mechanics/autocrafting.md)，
    按下你绑定为“选取方块”的按键（通常是鼠标中键）会打开一个 UI，让你指定要合成的数量。你也可以输入诸如 `3*64/2` 这样的公式，
    或输入 `=32`，这样就只会合成将你的存储数量补到 32 所需的物品。
*   按住 Shift 会将显示的物品固定在原位，阻止它们在数量变化或有新物品进入系统时重新排列。
*   手持桶或其他流体容器右击会将流体存储到容器，左击终端中的某种流体且手持空的流体容器时，则会取出该流体。

左侧部分有一些设置按钮，用于：

*   按名称、模组和数量等不同属性排序
*   查看已存储、可合成，或两者同时查看
*   查看物品、流体，或两者同时查看
*   更改排序
*   打开详细的终端设置窗口
*   更改终端界面的高度

右侧有用于放置<ItemLink id="view_cell" />的槽位

中间区域右上角（锤子按钮）会打开[自动合成](../ae2-mechanics/autocrafting.md)状态界面，让你查看自动合成的进度，以及每个[合成器CPU](crafting_cpu_multiblock.md)正在做什么。

## 配方

<RecipeFor id="terminal" />

<a name="crafting-terminal-ui"></a>

# 合成终端

<GameScene zoom="6" background="transparent">
  <ImportStructure src="../assets/blocks/crafting_terminal.snbt" />
  <IsometricCamera yaw="180" />
</GameScene>

合成终端与普通终端类似，拥有相同的设置和分区，但额外添加了一个合成网格，它会自动
从[存储网络](../ae2-mechanics/import-export-storage.md)中补充。使用 Shift 点击输出时要小心！

你应该尽快把你的终端升级为合成终端。

## 界面

合成终端的界面与普通终端相同，但中间额外增加了一个合成网格。

左上角还有 2 个额外按钮，可将合成网格中的物品清空到网络存储或你的物品栏中。

## 配方

<RecipeFor id="crafting_terminal" />

<a name="pattern-encoding-terminal-ui"></a>

# 样板编码终端

<GameScene zoom="6" background="transparent">
  <ImportStructure src="../assets/blocks/pattern_encoding_terminal.snbt" />
  <IsometricCamera yaw="180" />
</GameScene>

样板编码终端与普通终端类似，具有相同的设置和分区，但额外增加了[样板](patterns.md) 编码界面。它看起来类似于合成终端的 UI，但这个合成网格实际上并不会
执行合成。

除了合成终端外，你还应该准备一个这个。

## 界面

合成终端拥有与普通终端相同的 UI，并额外添加了[样板](patterns.md)编码界面。

样板编码界面分为几个部分：

用于插入 <ItemLink id="blank_pattern" /> 的槽位。

一个用于对样式进行编码的大箭头。

用于放置编码样板的槽位。将已经编码好的样板放入此槽位以进行编辑，然后点击“编码”箭头。

右侧有 4 个标签页，可用于切换要编码的样板类型，分别为

*   合成
*   加工
*   锻造
*   切石

中央 UI 会根据要编码的样板类型而变化：

*   在合成模式下：
    *   在 JEI/REI 中左键点击材料，或从中拖拽材料来组成配方。右键可移除该材料。
    *   启用替换后，你可以使用任意类型的木板来合成木棍之类的物品。此功能仅应在绝对必要时使用。
    *   流体替换允许使用已存储流体来代替桶装流体。
    *   你也可以直接从 JEI/REI 的配方界面将配方编码到样板中。

*   在处理模式中：
    * 在 JEI/REI 中左键或右键点击配方材料，或从 JEI/REI 中拖动材料，以指定配方的输入和输出。
    * 使用流体容器（如桶或流体储罐）右键点击，可将其中的流体设为一种材料，而不是将桶或储罐物品本身设为材料。
    * 手持一组物品时，左键会放置整组，右键会放置一个物品。对已有的材料堆栈左键可移除整组，右键可将堆栈数量减少 1。使用你绑定为“选取方块”的按键（通常是中键）
        可以精确指定物品或流体的数量。
    * 输出槽有一个主产物槽位，并留有空间用于放置你希望自动合成算法识别的任何副产物。
    * 输入槽和输出槽都可以滚动，因此你最多可以设置 81 种不同的材料和 26 种副产物
    * 你也可以直接从 JEI/REI 的配方界面编码一个模具。

*   锻造模式和切石模式的界面分别与锻造台和切石机的界面类似。

## 配方

<RecipeFor id="pattern_encoding_terminal" />

<a name="pattern-access-terminal-ui"></a>

# 样板管理终端

<GameScene zoom="6" background="transparent">
  <ImportStructure src="../assets/blocks/pattern_access_terminal.snbt" />
  <IsometricCamera yaw="180" />
</GameScene>

样板管理终端用于解决一个特定问题：在由 <ItemLink id="pattern_provider" /> 和 <ItemLink id="molecular_assembler" /> 密集堆叠而成的高塔中，
你无法实际接触到那些样板供应器来插入新的样板。此外，
也许你比较懒，不想为了插入一个[样板](patterns.md)而横穿整个基地。样板管理终端
可让你访问网络中的所有样板供应器。

## 界面

这个终端的 UI 与所有其他终端都不同。

它有用于设置终端高度以及显示哪些样板供应器的选项。

终端中的每一行都对应一个特定的样板供应器。

终端中的样板供应器会按照它们连接到的方块，或你为它们设定的名称（在铁砧中或使用 <ItemLink id="name_press" />）进行排序。

## 配方

<RecipeFor id="pattern_access_terminal" />