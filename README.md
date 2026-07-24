# All the Mods 10 · 7.2 汉化补丁 —— 绿油油版

> 整理／补译：**星野夢華 (Hoshino Yumeka)** · 基于 BBSMC 汉化二次修改

原始词条来自 BBSMC 汉化组，本人在其基础上做了大量补译、纠错与机制层修复
（改动幅度较大，故独立命名为「绿油油版」）。原版说明与致谢见
[原版说明与致谢(BBSMC).txt](原版说明与致谢(BBSMC).txt)。

## 安装方法

1. 从 [Releases](../../releases) 下载最新压缩包并解压；
2. 把解压出的**整个文件夹**放进 ATM10 实例根目录
   （即含 `mods/`、`options.txt` 的那一层，通常是
   `.minecraft/versions/All the Mods 10/`）；
3. 运行安装器：
   - **Windows**：双击 `双击安装-Windows.bat`
   - **macOS / Linux**：终端运行 `bash install.sh`
4. 按菜单选 **[1] 应用汉化**。安装器会：
   - 自动**备份**所有将被覆盖的文件（可随时恢复）；
   - 复制汉化文件并在 `options.txt` 中**自动启用资源包**（不启用会全英文）；
   - 询问是否安装可选的 **JEI 拼音搜索** mod（支持拼音检索物品）。

其余功能：`[2] 仅备份`、`[3] 恢复备份`（还原被覆盖文件、删除安装时新增
的文件、还原 `options.txt`）。命令行用法见脚本头部注释
（`apply` / `apply-with-pinyin` / `backup` / `restore`）。

**服务器**：仅需覆盖 `config/`。`vaultpatcher/`、`resourcepacks/`、
`kubejs/client_scripts/` 均为纯客户端渲染层，服务器不需要。

## 补丁内容一览

| 目录 | 作用 |
|---|---|
| `resourcepacks/` | 资源包（语言 / GUI / 字体） |
| `vaultpatcher/` + `mods/vaultpatcher.jar` | 硬编码文本补丁（见下方技术说明） |
| `kubejs/` | 客户端脚本（资源蜜蜂基因名） |
| `config/` | 神秘农业作物名等配置修正 + VaultPatcher 主配置 |
| `可选mods-拼音搜索/` | 可选：JEI 拼音搜索（安装器会询问） |

## 本版额外汉化 / 修复内容

### RFTools 全系（重点）

- 26 个 `.gui` 界面文件全部汉化（建造机、存储扫描器、护盾、传送、
  维度电池、时序器、屏幕、过滤器等）
- 96 条界面**硬编码**文本汉化（不在语言文件内，需字节码层补丁）——
  覆盖形状卡类型（精准采集 / 时运 / 普通采石、抽 / 放液体）、物品过滤器
  （白 / 黑名单、按模组匹配、组件匹配）、存储扫描器（可路由 / 导出）、
  模块化存储视图、护盾红石模式、移动仓消耗、拨号器收藏、环境控制器等
- ⚠️ `Copy` / `Move` / `Ignored` 等模式选项为**协议值**，翻译会导致游戏
  崩溃，故按设计保留英文（仅译其提示文字）

### 结构罗盘 / 自然罗盘

补全 114 个缺失结构名：CTOV 大 / 中 / 小型村庄与掠夺者前哨（各生物群系）、
Towns & Towers 各风格村庄 / 前哨、Explorify 补给贮藏点 / 瞭望塔、
BWG 特色村庄、Structory 下界 / 末地塔楼等。

### 传送石碑 (Waystones)

补全 17 条维度分组名（运行时动态键，官方语言文件不含）：挖矿维度、
异界、彼岸、以太、暮色森林、深暗之园等。

### 资源蜜蜂 (Productive Bees)

- 基因样本 / 蜂笼 / 基因瓶的蜂种名汉化（462 种蜂）
- 采用客户端渲染时替换方案，解决蜂名显示为英文 ID
  （如 `productivebees:lumber_bee`）的问题

### 神秘农业 (Mystical Agriculture)

修正种子「假翻译」根因：作物显示名取自 config 的 `name` 字段而非语言
文件，已直接改 config（难得素 / 振金 / 恩特罗 / 蔚蓝银 / 深红铁等
12 种作物 + 魔法等级名）。

### 其他补译

- PotionsMaster 154 条动态药水词条
- Shiny! 闪光生物 2000+ 实体名（原版优先，去除误译）
- 属性名：灵视 (spectral_sight)、穿墙 (phase) 等
- 花粉筛升级、枫糖浆等上游漏配键
- 字体乱码 (U+FFFD) 清理

## 技术说明（给想二次修改的人）

汉化分三层，缺一不可：

1. **资源包**（仓库内为源码目录 `resourcepacks/ATM10汉化包-7.2/`，
   **zip 由 CI / 构建脚本压缩，不入 git**）
   标准 `assets/<mod>/lang/zh_cn.json` 与 McJtyLib 的 `.gui` 界面文件，
   游戏启动时加载。
2. **VaultPatcher** (`vaultpatcher/modules/*.json`)
   处理「硬编码在 class 字节码里、语言文件够不着」的界面文本。
   `config/vaultpatcher_asm/config.json` 中 `load_all_modules` 必须为
   `true`，否则自建模块不加载。**切记：枚举协议值（模式选项）不可翻，
   否则崩溃** —— CI 会拦截。
3. **KubeJS 客户端脚本** (`kubejs/client_scripts/`)
   处理运行时动态拼接的文本（如资源蜜蜂把蜂 ID 拼进 tooltip）。
   用 `NativeEvents` 订阅 `ItemTooltipEvent`，渲染时正则替换。

## 开发 / 发版

```bash
# 校验（CI 同款）：JSON 合法性、枚举协议值、VaultPatcher 配置、.gui choice
python3 scripts/check.py

# 安装脚本端到端测试（CI 在 macOS / Windows / Linux 三系统各跑一遍）
python3 scripts/test_installer.py

# 打分发包（现场压缩资源包 zip + 附带安装器）
./scripts/build_dist.sh 7.2.0
```

CI 说明：

- **ci.yml** —— 每个 PR / push 跑校验 + 试打包；
- **installer-test.yml** —— 安装脚本一旦改动，自动在
  **macOS / Windows / Linux 三台 runner** 上跑端到端测试；
- **release.yml** —— 推 tag `v*`（如 `v7.2.0`）即自动校验、打包并发布
  GitHub Release，说明取自 `CHANGELOG.md` 对应版本段落。

## 致谢

- **BBSMC 汉化组** —— 提供原始汉化底本
- **All the Mods 团队** —— 整合包本体
- 各 mod 原作者

问题反馈请走 [Issues](../../issues)，附带截图与具体物品 / 界面名。

## License

[GPL-3.0](LICENSE)。BBSMC 原始词条与各 mod 资源的权利归其原作者所有。
