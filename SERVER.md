# 服务端汉化包 · 安装说明

> 适用于 ATM10 7.2 **专用服务器**（dedicated server）。单机玩家不需要本包。

## 为什么服务端也要装

有两类文本是**服务端生成后直接发给客户端**的，客户端装什么都救不回来：

1. **资源蜜蜂蜂笼**：抓蜂时服务端把蜂名解析成纯字符串烙进物品 NBT。
   专用服务器语言表只有英文 → 蜂笼永远显示 `Cyanite Bee` 之类。
   `mods/pb_hanhua_server-*.jar` 以语言注入方式让服务端解析出中文
   （已包含 461 种蜂名）。**注意：只对新抓的蜂生效，旧蜂笼的名字已烙死。**
2. **RFTools 建造机/形状卡的聊天反馈**（"未选择建造机！"等）：由服务端逻辑
   发送。`mods/vaultpatcher.jar` + `vaultpatcher/modules/` 的 RFTools 定向
   模块让服务端发出的就是中文。
3. **config/**：仅任务书语言（ftbquests）与 VaultPatcher 主配置。
   ⚠️ **神秘农业作物名配置（mysticalcustomization）是纯客户端的，绝不能
   覆盖到服务器**——服务器带改名后的作物配置会让所有玩家进服时刷
   「An error occurred creating crop with id null」（实测定位）。本包已不含该目录。

## 安装

把本包内以下内容覆盖到服务器数据目录（含 `mods/`、`server.properties` 的那层）：

```
mods/pb_hanhua_server-*.jar
mods/vaultpatcher.jar
vaultpatcher/modules/*.json
config/
```

然后重启服务器。

## 安全性说明

服务端只附带**类定向**的 VaultPatcher 模块（见 `scripts/server_modules.txt`
清单及准入标准）。全局替换模块（如客户端的蜂名基因模块）绝不能装到服务端——
会污染 NBT / 注册名导致存档损坏，CI 会拦截此类清单变更。
