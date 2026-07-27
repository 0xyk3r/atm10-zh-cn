# 贡献指南

感谢你想让这份汉化更好。这个仓库有几条**高压线**——都是真实炸过的雷，
CI 会拦截其中大部分，但请先读完再动手。

## 高压线（违反即炸游戏或毁玩家数据）

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
   曾经的"服务端语言注入 mod"就是因此被废除的。
   同理：`mysticalcustomization/`（作物名）是纯客户端配置，
   **绝不能进服务端包**——会让所有玩家进服刷
   `error creating crop with id null`。
4. **禁止贪婪字符串替换。**
   所有显示层替换必须整词 / 整段精确匹配（词边界、长名优先、
   hasOwnProperty 防原型链穿透）。半截替换（`Ter-蜜蜂-Nator`）比不翻更糟。

## 仓库结构：只有源，没有出货树

仓库里**没有** `kubejs/`、`config/`、`resourcepacks/`、`mods/` 这些目录。
它们是整合包的目录结构，属于产物，由 `scripts/assemble.py` 从 `src/` 现摊到
`build/` 下。动手前先跑一次：

```bash
python3 scripts/assemble.py                             # 只摊源（无需网络）
ATM_PACK_ROOT=<整合包目录> ./scripts/generate_all.sh    # 摊 + 跑全部生成器
```

- `src/pack/` 资源包内容 · `src/config/` 本包独有 config · `src/kubejs/` 本包独有脚本
- `src/upstream/<路径>.json` **上游文件的行级改写映射**

**改整合包自带的文件，改的是映射，不是文件。** 把上游文件改几个字符串后整份提交，
等于把上游内容和我们的改动焊死——ATM 一升级，我们发出去的就是「旧上游 + 我们的改动」，
把人家的修复整个覆盖掉。7.1→7.2 之间 ATM 换过 `CustomAdditions.js` 里冰与火的类名，
拿 7.2 的副本发给 7.1 用户当场 `ClassNotFound`，就是这么来的。改法：

```bash
python3 scripts/gen_upstream_patches.py build/packsrc/7.2 build/v/7.2  # 先摊出该版官方文件+现有改动
$EDITOR build/v/7.2/kubejs/startup_scripts/CustomAdditions.js          # 在出货树里改
python3 scripts/extract_upstream_patch.py \
    build/packsrc/7.2/kubejs/startup_scripts/CustomAdditions.js \
    build/v/7.2/kubejs/startup_scripts/CustomAdditions.js \
    kubejs/startup_scripts/CustomAdditions.js \
    > src/upstream/kubejs/startup_scripts/CustomAdditions.js.json      # 反解回映射
```

- **资源蜜蜂译名唯一真源** = `src/pack/assets/productivebees/lang/zh_cn.json`
  的实体键。改蜂名只改这里，然后重跑 `generate_all.sh`。双端 kubejs 脚本是产物，
  **不在仓库里，也不许手改**。
- 任务书补丁放 `src/config/ftbquests/quests/lang/zh_cn/chapters/*.snbt`
  （分章 delta，langsplitter 启动时按文件名字母序合并）。
- 同一数据出现在多个表面（tooltip / JEI / 快捷栏 / 名牌 / Jade / GUI）时，
  修复必须**一次修齐所有表面**并逐面自测——不接受打地鼠式补丁。
- 译名统一：同一事物在任务书、罗盘、物品名中的叫法必须一致
  （例：iceandfire 的 graveyard 统一为「墓园」）。

## 本地开发

```bash
python3 scripts/assemble.py                             # 摊出货树 → build/common
ATM_PACK_ROOT=<整合包目录> ./scripts/generate_all.sh    # 摊 + 跑全部生成器
python3 scripts/check.py build/v/7.2                    # CI 同款校验（全部硬检查）
python3 scripts/test_installer.py                       # 安装器端到端测试
./scripts/build_dist.sh r12                             # 出全部声明过的整合包版本
./scripts/build_dist.sh r12 7.2                         # 只出 7.2
```

- **ci.yml**：上游漂移检测（逐版本套映射）+ 汉化校验，每个 PR / push 必跑
- **installer-test.yml**：`installer/` 一动就在 macOS / Windows / Linux
  三系统跑端到端测试
- **release.yml**：推 tag `v7.2-release1` / `v7.2-beta1` 自动构建发布，
  Release 说明自动取 `CHANGELOG.md` 对应版本段落——**发版前记得写 CHANGELOG**

## PR 约定

- 一个 PR 只做一件事；用户可见改动更新 `CHANGELOG.md`
- 版本号格式：`<整合包版本>-<release|beta|rc><序号>`（如 `7.2-release1`）
- commit 说明写清"为什么"，尤其是译名决策（附投票 / 出处更好）
