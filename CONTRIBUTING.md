# 贡献指南

感谢你想让这份汉化更好。这个仓库有几条**高压线**——都是真实炸过的雷，
CI 会拦截其中大部分，但请先读完再动手。

## 务必注意

1. **枚举协议值绝不可翻译。**
   McJtyLib 系（RFTools 等）GUI 里的模式选项（`Ignored` / `Off` / `On` /
   `Copy` / `Move` / `Swap`…）是存储与网络协议值，翻译会导致
   `IllegalStateException` 崩溃。资源包 `.gui` 文件里 `choice('...')`
   的参数同理必须保持英文。`scripts/check.py` 有硬检查。
2. **玩家自定义名神圣不可侵犯。**
   命名牌 / 铁砧起的名字绝不允许被改写或"翻译"。资源蜜蜂的迁移与显示
   都通过"系统生成名封闭集合"（PB_SYS）把关——不要绕过它。
3. **服务端数据层禁止注入中文。**
   服务器侧的语言表 / 配方数据必须保持上游英文，否则服务端现算的文本
   与 JEI / 配方（客户端由英文数据现算）分裂，玩家查不到配方。
   在服务端注入语言表的做法因此一律不予采纳。
   同理：`mysticalcustomization/`（作物名）是纯客户端配置，
   **绝不能进服务端包**——会让所有玩家进服刷
   `error creating crop with id null`。
4. **禁止贪婪字符串替换。**
   所有显示层替换必须整词 / 整段精确匹配（词边界、长名优先、
   hasOwnProperty 防原型链穿透）。半截替换（`Ter-蜜蜂-Nator`）比不翻更糟。
   同一个词在不同上下文里可能是两回事：`星辉`既是 Starlight（星辉水晶、符文星辉祭坛）
   又被误用于 Starry Bee；`遗迹`是废墟，Relics 那个模组说的是随身`遗物`；
   `冰与火`在沉浸工程里是热逆转附魔的风味文字，跟那个模组无关。全局替换会把它们一起毁掉。
5. **有几类字符串译了就崩，或者译了也白译。**
   - 建筑棒（structurize）以 `/` 开头的**路径键**是 Map 的键，译了直接 NPE 闪退。
   - blockui 的 `top` / `horizontal` 这类**对齐标志**是字符串枚举，译了会让整个
     MineColonies / 建筑棒界面错位。
   - **物品 tooltip 里不能有 `\n`**，会被画成 LF 方框；GUI 提示和聊天才认换行。
     物品说明太长只能改措辞压短。
   - CC: Tweaked 的终端字形表只有 256 格，**画不出汉字**，`help` 之类整体不译。
6. **删文件 CI 直接红。**
   `src/` 有一份保护清单（`scripts/compliance/protect.py`），汉化**只许加不许删**。
   新加文件要 `git add` 之后再跑 `protect.py --update` 登记（它靠 `git ls-files`，
   顺序反了会「新收 0 个」）。红了通常是删错了，别去改闸。

## 仓库结构：只有源，没有出货树

仓库里**没有任何一棵出货用的目录树**。`kubejs/`、`config/`、`resourcepacks/`、`mods/`
这些整合包目录都是**产物**，构建时现摊、现产、现打补丁，全部落在 `build/` 下（不入库）。
仓库里只有 `src/`（手写的真源与改动映射）和 `scripts/`（生成器）。

```
src/pack/                       资源包内容（译文；lang 按命名空间索引，跨版本通用）
src/config/                     本包独有的 config（任务书 delta、VaultPatcher 主配置…）
src/kubejs/                     本包独有的 KubeJS 脚本
src/upstream/<路径>.json        整合包自带文件的行级改写映射
src/books/<路径>.json           导览书的「位置 + 原文 + 译文」映射
src/vaultpatcher/modules/       硬编码文本模块（只留译文与目标类）；内容哈希钉在 src/module_hashes.json
src/keep_english.json           刻意保留英文的词及其理由（MekaSuit 之类）
src/protected.json              保护清单：src/ 下不许消失的文件
src/mods.lock.json              随包分发的第三方 jar：项目 / 版本 / 地址 / sha256
src/rules/*.json                发版校验的**规则**（check.py 只是它们的解释器）
src/toolchain.lock.json         构建工具链：容器 digest / Pillow / 字体哈希
requirements.lock               Pillow 的全平台 wheel 哈希（装的时候必须 --require-hashes）
versions/<版本>/                手写的版本专属层（任务书覆盖、默认资源包顺序）
versions/<版本>/overrides.sha256 该版官方 overrides 的整棵树指纹（CI 缓存键 + 门控）
versions/<版本>/unobtainable.json 该版 manifest 里已从 CurseForge 消失的 jar（必须逐个登记）
versions/db/<版本>/             该版的核验数据库与英文底本
versions/db/<版本>/jars.json    该版每个 jar 的 sha256 + 不可变的 CurseForge fileID
versions/db/<版本>/keybinds.json 该版全部按键分类与注册名（含拼名字用的字符串原子）
scripts/                        生成器
scripts/compliance/             闸（gate）与它们的反例测试

build/common/                   摊好的出货树（版本中立部分）
build/v/<版本>/                 该版的完整出货树，check.py 查的就是它
build/packsrc/<版本>/           该版官方 overrides（fetch_pack.py --no-jars 取）
```

动手前先摊一次：

```bash
python3 scripts/assemble.py                             # 只摊源（不需要整合包）
ATM_PACK_ROOT=<整合包目录> ./scripts/generate_all.sh    # 摊 + 跑全部生成器
```

### 一条判据：能算出来的，一律不写进仓库

**这个值换个整合包版本还对吗？能从官方文件 / 字节码 / manifest 算出来吗？**
两条任一为真，就写生成器，不写文件；而且算不出来要**报错退出**，不许回退成默认值。

手写死的版本相关字段，在多版本发布下必然「三个包里两个是错的」，而且**不报错**。
已知会出错的做法：

| 做法 | 后果 | 应当怎么做 |
|---|---|---|
| `kubejs/*.js`、`config/*.json` 改几个字符串后整份提交 | ATM 升级后，发出去的是「旧上游 + 我们的改动」，上游的修复被整份覆盖。7.1→7.2 之间 ATM 改过 `CustomAdditions.js` 里冰与火的类名，把 7.2 的副本发给 7.1 用户会直接 `ClassNotFound` | `src/upstream/` 存「找这几行 → 换成这几行」，对**目标版本的官方文件**套用，找不到原文就退出 |
| 导览书整份副本 | 模组更新导览书时，旧副本把新内容整份覆盖，玩家看不到、也不报错（PneumaticCraft 的「切换维度」整页曾因此不显示）| `src/books/` 只存「位置 + 原文 + 译文」，构建时拿 jar 里那份重新套 |
| VaultPatcher 模块头部写死带版本号的 jar 名 | 以 7.2 那份比对，7.1 只有 116/152 对得上，7.0 只有 83/152 | 按 `versions/db/<版本>/` 现填 |
| 安装器界面写死「ATM10 7.2」 | 7.0 / 7.1 的包印着别的版本号 | `@@MCVER@@` 占位，打包时填 |
| `pack.mcmeta` 写死 `pack_format: 34`、字体抄一份原版 provider 列表 | 换 MC 版本资源包被判不兼容；原版加 provider 会被我们吞掉 | 取原版客户端 `version.json` 与 `font/*.json` |

### 改上游自带的文件

```bash
python3 scripts/gen_upstream_patches.py build/packsrc/7.2 build/v/7.2  # 摊出官方文件+现有改动
$EDITOR build/v/7.2/kubejs/startup_scripts/CustomAdditions.js          # 在出货树里改
python3 scripts/extract_upstream_patch.py \
    build/packsrc/7.2/kubejs/startup_scripts/CustomAdditions.js \
    build/v/7.2/kubejs/startup_scripts/CustomAdditions.js \
    kubejs/startup_scripts/CustomAdditions.js \
    > src/upstream/kubejs/startup_scripts/CustomAdditions.js.json      # 反解回映射
```

### 改导览书译文

```bash
ATM_PACK_ROOT=<整合包目录> ./scripts/generate_all.sh    # 先把书生成到 build/common
$EDITOR build/common/resourcepacks/ATM10汉化包/assets/<模组>/patchouli_books/…/x.json
python3 scripts/extract_books.py <整合包目录>/mods       # 从**构建树**反解回 src/books/
```

`gen_books.py` 会告诉你哪些位置套不上（上游改了那一段），以及哪些散文页的英文原稿变了。
命中率跌破 90% 直接构建失败——不会让「悄悄少翻一半」的包发出去。

### 单一真源

- **资源蜜蜂译名** = `src/pack/assets/productivebees/lang/zh_cn.json` 的实体键。
  改蜂名只改这里，然后重跑 `generate_all.sh`。双端 kubejs 脚本是产物，
  **不在仓库里，也不许手改**。
- 任务书补丁放 `src/config/ftbquests/quests/lang/zh_cn/chapters/*.snbt`
  （分章 delta，langsplitter 启动时按文件名字母序合并，文件名必须 `zz_hanhua_` 打头）。
- 同一数据出现在多个表面（tooltip / JEI / 快捷栏 / 名牌 / Jade / GUI）时，
  修复必须**一次修齐所有表面**并逐面自测——不接受打地鼠式补丁。
- 译名统一：同一事物在任务书、罗盘、物品名中的叫法必须一致
  （例：iceandfire 的 graveyard 统一为「墓园」）。
- **物品名是单一真源**：任务书 / 图鉴 / 界面里提到某件东西，用的必须是玩家在 JEI 里
  搜得到的那个名字。判据是机械的（英文原文出现某物品名 → 中文必须出现它的中文名），
  已经做成闸。注意有些名字是**运行时拼出来的**、lang 里没有独立的键
  （资源蜜蜂的蜜脾块 = 本地化蜂名去掉 `" Bee"` 再套模板），扫静态键表扫不到它们。

## 本地开发

```bash
./scripts/fetch_fonts.sh                                # 取字体（全 OFL，不入库）
ATM_PACK_ROOT=<整合包目录> ./scripts/generate_all.sh    # 摊 + 跑全部生成器 → build/common
python3 scripts/check.py build/v/7.2                    # CI 同款校验（全部硬检查）
python3 scripts/test_installer.py                       # 安装器端到端测试
./scripts/build_dist.sh r18                             # 出全部声明过的整合包版本
./scripts/build_dist.sh r18 7.3                         # 只出 7.3
```

`build_dist.sh` 会自动为每个目标版本取一份官方 `overrides`，在 `build/v/<版本>/` 合成
该版完整出货树，逐版跑 `check.py`，最后 `verify_dist.py` 拆开每个 zip 数内容——
一个没汉化的包发不出去。

### 机械校验清单

| 脚本 | 查什么 |
|---|---|
| `check.py` | 规则解释器；规则在 `src/rules/*.json`。加同类规则只改 JSON，不动脚本 |
| `toolchain.py` | 这次构建是不是标准工具链——不是就明说产物哈希不作数，绝不假装能比 |
| `scan_keybinds.py` | 扫出全部按键分类与注册名，喂给 `vp-keybind-registration-names` 规则 |
| `gen_upstream_patches.py` | 整合包自带文件被改动过没有——原文找不到就构建失败 |
| `gen_books.py` | 导览书译文能否落到上游那份 JSON 上——命中率跌破 90% 就构建失败 |
| `gen_vaultpatcher.py` | 模块头部写的 jar 名是否是**该版**真实存在的那个 |
| `gen_vanilla_assets.py` | 原版字体 provider 列表与 `pack_format` 跟不跟得上原版 |
| `check_vaultpatcher_strings.py` | 硬编码文本的 key 是否还在目标模组的字节码里（失配是**静默**的） |
| `check_en_drift.py` | 英文底本变了而译文没跟着变——上游改文案必然被发现 |
| `verify_dist.py` | 打好的 zip 里每一类内容够不够量——空壳包发不出去；标准工具链下还比内容指纹 |
| `build_version_db.py --verify` | 一个 mods 目录是不是**逐字节**就是那一版官方的那批 jar |

`scripts/compliance/` 下是**闸**（gate），跟生成器分开放。除上表外还有：

| 闸 | 查什么 |
|---|---|
| `protect.py` | 保护清单：`src/` 的文件只许加不许删 |
| `check_module_hashes.py` | VaultPatcher 模块被改动过没有——改了就得跑 `gen_module_hashes.py` 重钉 |
| `check_bee_names_in_quests.py` | 任务书提到某只蜜蜂时用的是不是 JEI 里那个名字；蜜脾／蜜脾块／刷怪蛋的名字是拿蜂名现拼的，一并判 |
| `check_item_names_in_quests.py` | 同一条判据推广到别的模组（mob_grinding_utils / occultism / relics） |
| `check_jetpack_tiers.py` | Iron Jetpacks 的等级名不在 lang 里而在整合包 config 里，缺了会静默回退英文 |
| `check_oracle_index_paths.py` | 神谕目录的书有两套目录约定，放错那条路径的译文永远不会被读、且不报错 |
| `check_kubejs_classfilter.py` | 脚本里 loadClass 了被 KubeJS 类过滤表拒掉的类——运行时才炸，加载阶段全绿 |
| `check_dynamic_substrings.py` | dynamic 模块的 `@` 子串键互不为子串 |
| `check_quest_formatting.py` / `check_gui_maps.py` / `check_injected_lang.py` / `check_minecolonies_paths.py` / `check_name_divergence.py` | 各自那一类的硬检查 |

**加闸就得同时加反例**：`test_gates.py` 里每一条都复刻一次真实事故，验它**真的会红**，
并且验「前提取不到时也红」（fail-closed）。CI 跑 `test_gates.py` 和 `test_protect.py`，
少一条反例过不去。写闸时最常见的错是**静默漏判**——扫不到就当没问题，那是假闸。
报数之前先拿已知真值验一遍扫描器；数不准就说数不准。

### CI

- **ci.yml**：保护闸自检 → 保护清单 → 模块哈希 → **闸的反例测试** → 摊出货树 →
  逐版本上游漂移检测 + 汉化校验 + 任务书/颜色码检查 → 安装脚本语法检查。
  每个 PR / push 必跑（不下 jar，快）。`fetch-depth: 0` 是硬要求：浅克隆下
  「清单不许变短」那道闸取不到基准，会变成静默跳过
- **build.yml**：完整构建全部版本，下整合包与 480 个 mod jar。
  跑在 `src/toolchain.lock.json` 里**按 digest 钉死**的容器里，Pillow 按
  `requirements.lock` 的哈希装——产物 PNG 的字节由 Pillow 自带的 freetype/zlib 决定，
  工具链不进依赖图，产物哈希就没有意义
- **installer-test.yml**：`installer/` 一动就在 macOS / Windows / Linux 三系统跑端到端
- **release.yml**：推 tag 自动构建并发布全部整合包版本的包。
  tag 形态：新式 `vR12` / `vR12-beta1`（补丁版本号与整合包版本解耦，`r` 大小写都认），
  旧式 `v7.2-release11` 继续认。Release 说明按**整串精确比对**（大小写不敏感）取
  `CHANGELOG.md` 的 `## <版本>` 段——tag `vR12` 对应 `## R12`；取不到就回落到文件里
  第一个 `## ` 段（当前在写的那一段），**不会**回落到 `## 7.2`，那是冻结的历史段。
  发版前记得写 CHANGELOG。
  发布前逐个点名检查「每个声明过的版本都有客户端 + 服务端两个包」，缺一个就不发。

## PR 约定

- 一个 PR 只做一件事；用户可见改动写进 `CHANGELOG.md` **最上面那一段**
  （段名就是下次要发的补丁版本号，如 `## R18`；`## 7.2` 及以下是冻结的历史，别动）
- 版本号格式：`R<序号>`，与整合包版本解耦（一份 `R18` 对应 7.0/7.1/7.2/7.3 四个包）。
  tag 写 `vR18` / `vR18-beta1`。`7.2-release1` 那种旧式仍能识别，但新版本别再用了。
- **CHANGELOG 是写给玩家的**：一句结论 + 「哪里 / 之前 / 现在」表格 + 受影响版本 +
  代价（要不要重装、服主要不要动）。机制、根因、扫描口径那些写进 commit 正文和代码注释，
  不要写进更新日志。发版那一节末尾按惯例写**致谢**（提反馈的人）。
- commit 说明写清"为什么"，尤其是译名决策（附投票 / 出处更好）。
  译名的真源是**游戏里显示的那个名字**（模组自带 lang / 创造栏 / JEI），不是百科也不是别家汉化；
  查不到中文名的模组名宁可留英文，自己编一个玩家在游戏里反而搜不到
