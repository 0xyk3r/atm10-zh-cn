# 服务端汉化包 · 安装说明

[![GitHub](https://img.shields.io/badge/GitHub-chiba233%2Fatm10--zh--cn-181717?logo=github)](https://github.com/chiba233/atm10-zh-cn)
[![Contributing](https://img.shields.io/badge/Contributing-guide-blue.svg)](./CONTRIBUTING.md)
[![Security](https://img.shields.io/badge/Security-policy-red.svg)](./SECURITY.md)
[![License](https://img.shields.io/badge/License-GPL--3.0-green.svg)](./LICENSE)

> 适用于 ATM10 @@MCVER@@ **专用服务器**（dedicated server）。**单机玩家不需要本包**——
> 单机时你自己的客户端就兼任逻辑服务端，蜂名迁移脚本已包含在客户端包里。

## 目录

- [兼容版本](#兼容版本)
- [为什么服务端也要单独装](#为什么服务端也要单独装)
- [包里有什么](#包里有什么)
- [安装](#安装)
- [验证](#验证)
- [不包含什么 · 为什么](#不包含什么--为什么)
- [安全性说明](#安全性说明)

## 兼容版本

| 项 | 版本 |
|---|---|
| 整合包 | All the Mods 10 **v@@MCVER@@** 专用服务器 |
| Minecraft | 1.21.1 |
| 加载器 | NeoForge @@NEOFORGE@@ |

**客户端包与服务端包必须匹配同一版本**，且服务器每个玩家的客户端也要装对应的客户端汉化包。

## 为什么服务端也要单独装

有三类文本是**服务端下发给客户端**的，客户端装什么都救不回来：

1. **任务书**（量最大）：FTB Quests 的章节名、任务标题 / 副标题 / 描述由服务端下发。
   服务端没装，玩家客户端装了也白搭——大家读到的还是服务端那一份。
   本包每一版的任务书修正（物品名对齐、语句、断行）都要双端一起装才对得上。
2. **资源蜜蜂的蜂笼 / 实体名**：抓蜂时服务端把蜂名解析成纯字符串烙进物品 NBT。
   `kubejs/server_scripts/pb_hanhua_cage_migrate.js` 会按 NBT 里的真实蜂种 ID，
   把蜂笼名与实体名改写为权威译名（与客户端资源包**同源**）。
   老蜂笼把它放进背包待几秒即自动转正；**玩家用命名牌起的名字绝不会被改**。
3. **RFTools 建造机 / 形状卡的聊天反馈**（「未选择建造机！」等）：由服务端逻辑发送。
   `mods/vaultpatcher.jar` + `vaultpatcher/modules/` 里的 RFTools 定向模块让服务端发出的就是中文。

> **为什么不用「服务端语言注入 mod」？** 那会让服务端**现算**的文本变中文，而 JEI / 配方
> （客户端由英文数据现算）不变，两边名字对不上、玩家查不到配方。本包早已废弃该方案，
> 只做「按 NBT ID 精确改写纯显示字段」这一件事。

## 包里有什么

```
mods/vaultpatcher.jar                          # 字节码文本补丁工具（上游原版，未改）
vaultpatcher/modules/*.json                    # 仅 10 个 RFTools/mcjty 类定向模块（清单见 scripts/server_modules.txt）
kubejs/server_scripts/pb_hanhua_cage_migrate.js # 蜂笼/实体显示名按 NBT ID 迁移
config/ftbquests/…                             # 任务书中文（服务端也要，否则任务标题/描述回退英文）
config/vaultpatcher_asm/…                       # VaultPatcher 主配置
请安装前务必看我.md · LICENSE · 项目主页与反馈.url
```

> ⚠️ **任务书语言文件是整份替换，不是往里加文件。**
> `config/ftbquests/quests/lang/zh_cn/` 下发的是「整合包自己那份中文 + 本包的修正」，
> 文件名与整合包原本的一模一样，装的时候会把同名文件覆盖掉。
>
> 之所以不能只发修正：`ftbquestslangsplitter` 合并同目录下的 `*.snbt` 时**不排序**
> （`chapters/` 里是 `Files.list(...).forEach(...)`，一个 comparator 都没有），
> 而 `Files.list` 不保证顺序——NTFS/APFS 恰好按名字返回，**ext4 返回哈希序**。
> 同一个键要是同时躺在「整合包那份」和「本包的修正」两个文件里，谁生效在 Linux
> 服务器上是随机的：在服务器第一次启动**之前**就装包的机器，会有随机一批修正被顶回
> 整合包原文。整份替换之后，一个键只由一份文件持有，顺序彻底不参与决策。
>
> 包里那些内容只有 `{}` 的 `zz_hanhua_*.snbt` / `_*.snbt` 是**空壳**，不是漏生成：
> 旧版本按这些名字发过带内容的 delta，而安装是只覆盖不删除的，留在盘上会拿旧值
> 跟新文件抢同一个键。照原名发一个空壳就把它们盖住了，且全程不删任何文件。
>
> 已经跑过一次的服务器不用担心「两份文件」：整合包那份早就被改名成 `.snbt_merged`，
> 而 splitter 只读文件名以 `.snbt` 结尾的（`isValidLangFile`），`.snbt_merged` 不会再被
> 读第二次。硬盘上多出来的那份是死文件，删不删都行。

## 安装

1. **先备份**服务器数据目录里的 `config/`、`kubejs/`、`vaultpatcher/`、`mods/vaultpatcher.jar`
   （若已存在）。本包不带自动安装器，请手动备份以便回退。
2. 把本包内的 `mods/` `vaultpatcher/` `kubejs/` `config/` **覆盖**到服务器数据目录
   （含 `mods/`、`server.properties` 的那一层）。
3. **完整重启服务器**（VaultPatcher 在类加载时生效，热重载无效）。

> **只更新任务书文本时可以不重启**：`config/ftbquests/quests/lang/` 下的语言文件
> 覆盖后，执行 `ftbquests reload` 即可让所有在线玩家生效（玩家侧重新打开任务书，
> 或重连一次）。Docker 部署可用：
>
> ```bash
> docker exec <容器名> rcon-cli ftbquests reload
> ```
>
> 控制台直接敲 `ftbquests reload` 也一样。VaultPatcher / kubejs 的改动仍需完整重启。

## 验证

- 服务器**能正常启动、无报错**（尤其别出现 `error creating crop with id null`——若出现，
  说明误把客户端包的 `config/mysticalcustomization` 上了服务器，见下）。
- 进服后：任务书标题 / 描述为中文；建造机未选择时的聊天提示为中文；
  抓到的新蜂 / 放进背包的老蜂笼名字为中文。
- 任务书里提到的物品名，应当与你在 JEI 里搜到的**完全一致**（本包以「任务绑定的
  物品真名」为单一真源做过全量反查对齐）。若发现对不上，请
  [提 Issue](https://github.com/chiba233/atm10-zh-cn/issues) 附任务截图。

## 不包含什么 · 为什么

⚠️ **神秘农业作物名配置（`config/mysticalcustomization`）是纯客户端的，绝不能上服务器**。
服务器带上改名后的作物配置，会让**所有玩家进服时刷**
`An error occurred creating crop with id null`（2026-07-24 实测定位）。
**本服务端包已不含该目录**；请也确认你没从客户端包手动拷贝它上去。

## 安全性说明

服务端只附带**类定向**（target_class 指向具体 GUI/逻辑类）的 VaultPatcher 模块，
清单与准入标准见 `scripts/server_modules.txt`。**全局替换模块**（如客户端的蜂名基因模块）
绝不能装到服务端——会污染 NBT / 注册名导致存档损坏。CI 会拦截对该清单的越界变更。
