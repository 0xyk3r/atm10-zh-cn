#!/usr/bin/env bash
# atm10-zh-cn — All the Mods 10 简体中文汉化补丁「绿油油版」
# Copyright (C) 2026 星野夢華 (Hoshino Yumeka)
# SPDX-License-Identifier: GPL-3.0-or-later
# ATM10 7.2 汉化补丁「绿油油版」安装器 (macOS / Linux)
# 用法：把整个汉化文件夹放进 ATM10 实例根目录后运行：
#   bash install.sh                    # 交互菜单
#   bash install.sh apply              # 应用汉化（自动先备份，不含可选mods）
#   bash install.sh apply-with-pinyin  # 应用汉化 + 安装可选 JEI 拼音搜索 mod
#   bash install.sh backup             # 仅备份
#   bash install.sh restore [备份名]   # 恢复备份
set -euo pipefail
cd "$(dirname "$0")"
SCRIPT_DIR="$(pwd)"
TARGET="$(cd .. && pwd)"
PACK_DIRS="config kubejs mods resourcepacks vaultpatcher"
PACK_ENTRY='file/ATM10汉化包-7.2.zip'
PINYIN_DIR="可选mods-拼音搜索"
TS=""
BK=""
# 就地解压：用户把压缩包内容直接解到实例根目录，源与目标同一层，
# 再复制一次就是自己覆盖自己。这种情况文件本来就已到位。
IN_PLACE=0

say() { printf '%s\n' "$*"; }

# 判定一个目录是不是游戏实例根目录。
# 不能只看 options.txt —— **刚装好、一次都没启动过的整合包没有 options.txt**
# （它是 Minecraft 首次退出时才写的）。也不能只看 mods/ —— 汉化包自己的文件夹里
# 也有个 mods/（装着 vaultpatcher.jar）。用 jar 数量区分：ATM10 有 400+ 个，汉化包只有 1 个。
is_instance() {
  [ -d "$1/mods" ] || return 1
  [ -f "$1/options.txt" ] && return 0
  n=$(ls "$1"/mods/*.jar 2>/dev/null | wc -l | tr -d ' ')
  [ "${n:-0}" -ge 20 ]
}

set_in_place() {
  if [ "$(cd "$SCRIPT_DIR" && pwd -P)" = "$(cd "$TARGET" && pwd -P)" ]; then
    IN_PLACE=1
    say "ℹ️ 检测到汉化文件已经在实例根目录里（压缩包内容被直接解压到了这一层）。"
    say "   文件本来就已到位，无需复制；本次只做 options.txt 的资源包启用。"
    say "   ⚠️ 这种装法没有备份可回退——原文件在你解压覆盖的那一刻就没了。"
    say "   想要可回退的安装，请解压到别处、把整个文件夹放进实例根目录再运行安装器。"
  fi
}

check_target() {
  if is_instance "$TARGET"; then
    set_in_place
    return
  fi
  # 就地解压：脚本自己所在的这一层就是实例根目录
  if is_instance "$SCRIPT_DIR"; then
    TARGET="$SCRIPT_DIR"
    set_in_place
    return
  fi
  say "⚠️ 上一级目录不是游戏实例根目录（含 mods/ 的那一层）。"
  if [ -t 0 ]; then
    while :; do
      printf '请输入 ATM10 实例根目录完整路径（q 退出）: '
      read -r inp || exit 1
      [ "$inp" = "q" ] && exit 1
      # 清洗输入：复制/粘贴/拖拽常带成对引号或反斜杠转义空格
      case "$inp" in
        \"*\") inp="${inp#\"}"; inp="${inp%\"}" ;;
        \'*\') inp="${inp#\'}"; inp="${inp%\'}" ;;
      esac
      case "$inp" in *\\*) inp="$(printf '%s' "$inp" | sed 's/\\\(.\)/\1/g')" ;; esac
      inp="${inp%/}"
      case "$inp" in "~"*) inp="$HOME${inp#\~}" ;; esac
      if is_instance "$inp"; then
        TARGET="$inp"
        say "✅ 目标实例: $TARGET"
        set_in_place
        return
      fi
      say "❌ 该路径下没找到 ATM10 的 mods/（应该有几百个 .jar），请重试。"
    done
  fi
  say "   请把整个汉化文件夹放进实例根目录（含 mods/ 的那一层）后再运行本脚本。"
  exit 1
}

payload_files() {
  for d in $PACK_DIRS; do
    [ -d "$d" ] && find "$d" -type f ! -name '.DS_Store'
  done
}

do_backup() {
  if [ "$IN_PLACE" = "1" ]; then
    say "⚠️ 就地解压模式下没有可备份的原文件（已被解压覆盖），跳过备份。"
    return
  fi
  TS="$(date +%Y%m%d-%H%M%S)"
  BK="$SCRIPT_DIR/backups/$TS"
  mkdir -p "$BK"
  n=0
  while IFS= read -r f; do
    if [ -f "$TARGET/$f" ]; then
      mkdir -p "$BK/$(dirname "$f")"
      cp -p "$TARGET/$f" "$BK/$f"
      n=$((n + 1))
    else
      printf '%s\n' "$f" >> "$BK/新增文件清单.txt"
    fi
  done < <(payload_files)
  [ -f "$TARGET/options.txt" ] && cp -p "$TARGET/options.txt" "$BK/options.txt"
  say "✅ 已备份 $n 个将被覆盖的文件到 backups/$TS/"
}

##
# 清理 7.2 release8 之前的遗留文件。
#
# 那之前本包的任务书 delta 用的是 `<章节名>.snbt`，与整合包自带的同名文件**撞名**，
# 安装时直接覆盖 —— 整合包那一章上百条翻译当场没了，任务书变英文。
# （已经启动过的实例看不出来：整合包那批早合并完并改名成 .snbt_merged 了。）
#
# 现在统一加 zz_hanhua_ 前缀，不会再撞名。这里把旧名字的残留删掉，
# 且只在**内容与本包同名新文件逐字节相同**时才删 —— 这样能确定它是本包的旧产物，
# 绝不会误删整合包自己的文件。
clean_legacy_quest_lang() {
  QD="$TARGET/config/ftbquests/quests/lang/zh_cn/chapters"
  SD="$SCRIPT_DIR/config/ftbquests/quests/lang/zh_cn/chapters"
  [ -d "$QD" ] && [ -d "$SD" ] || return 0
  hit=0
  for new in "$SD"/zz_hanhua_*.snbt; do
    [ -f "$new" ] || continue
    base="$(basename "$new")"; base="${base#zz_hanhua_}"
    for old in "$QD/$base" "$QD/_$base"; do
      if [ -f "$old" ] && cmp -s "$old" "$new"; then
        rm -f "$old"
        hit=$((hit + 1))
      fi
    done
  done
  if [ "$hit" -gt 0 ]; then
    say "🧹 清理了 $hit 个旧版本残留的任务书语言文件。"
    say "⚠️ 旧版本可能覆盖过整合包自带的任务书翻译。若任务书仍有整章英文，"
    say "   请重装一次整合包再运行本安装器（本包已不会再覆盖整合包的文件）。"
  fi
}

# ATM10 7.2 默认启用的资源包，顺序照抄游戏自己写出来的 options.txt。
# 为什么要写死这一串：全新实例没有 options.txt，如果只写我们一个包，
# 游戏首次启动会把这 15 个内置包**全部插到我们后面**（实测汉化包落到第 3 位，
# 被 mod_resources 和五百多个模组包压在底下，汉化基本不生效）。
# 资源包是**后面的覆盖前面的**，我们必须排在最后一个。
DEFAULT_PACKS='"modularbees:dynamic_assets","vanilla","mod_resources","add_xycraft_overrides_stone","add_xycraft_overrides_metal","add_xycraft_overrides_glass","moonlight:merged_pack","mod/towntalk:respack","mod/dyenamicsandfriends:compat_packs/productivemetalworks/","mod/dyenamicsandfriends:compat_packs/connectedglass/","mod/dyenamicsandfriends:compat_packs/luminax/","mod/dyenamicsandfriends:compat_packs/cookingforblockheads/","mod/dyenamicsandfriends:compat_packs/botanypots/","mod/dyenamicsandfriends:compat_packs/chromacarvings/","modern_industrialization/generated"'

patch_options() {
  OPT="$TARGET/options.txt"
  # 全新实例还没启动过，options.txt 尚不存在（Minecraft 退出时才写）。
  # 建一份含默认包列表 + 汉化包（放最后）的：Minecraft 启动时会把其余选项
  # 按默认值补齐再回写，部分 options.txt 是合法的。
  # （不要指望 config/defaultoptions —— ATM10 7.2 并没有装 DefaultOptions 模组，
  #   那个目录是历史遗留，写进去没有任何东西会读它。）
  if [ ! -f "$OPT" ]; then
    printf 'lang:zh_cn\nresourcePacks:[%s,"%s"]\n' "$DEFAULT_PACKS" "$PACK_ENTRY" > "$OPT"
    say "ℹ️ 这个实例还没启动过（没有 options.txt），已新建一份并写入中文语言与汉化资源包。"
    say "   首次启动游戏时 Minecraft 会自动补齐其余设置。"
    return
  fi
  cur="$(grep '^resourcePacks:' "$OPT" | head -1)"
  if [ -z "$cur" ]; then
    say "⚠️ options.txt 中没有 resourcePacks 行，请进游戏手动启用资源包"
    return
  fi
  body="${cur#resourcePacks:[}"; body="${body%]}"
  # 先把已有的汉化包条目摘掉，再追加到**末尾**。
  # 不能只判断「已存在就跳过」——旧版本装出来的实例里它可能排在很前面，
  # 那样等于没启用（后面的包会把它整个盖掉），必须重新挪到最后。
  body="$(printf '%s' "$body" | sed "s|\"$PACK_ENTRY\"||g; s|,,*|,|g; s|^,||; s|,$||")"
  if [ -n "$body" ]; then
    new="resourcePacks:[$body,\"$PACK_ENTRY\"]"
  else
    new="resourcePacks:[\"$PACK_ENTRY\"]"
  fi
  if [ "$new" = "$cur" ]; then
    say "options.txt 已正确启用汉化资源包（在列表最后），跳过"
    return
  fi
  awk -v n="$new" '/^resourcePacks:/{print n; next} {print}' "$OPT" > "$OPT.hanhua-tmp" \
    && mv "$OPT.hanhua-tmp" "$OPT"
  say "✅ 已在 options.txt 启用汉化资源包并置于列表最后（不在最后会被其他包盖掉）"
}

do_apply() {
  if [ "$IN_PLACE" = "1" ]; then
    clean_legacy_quest_lang
    patch_options
    say "✅ 汉化文件已在位，options.txt 已处理完毕。"
    return
  fi
  do_backup
  clean_legacy_quest_lang
  while IFS= read -r f; do
    mkdir -p "$TARGET/$(dirname "$f")"
    [ "$SCRIPT_DIR/$f" = "$TARGET/$f" ] && continue   # 双保险：源即目标就跳过
    cp -p "$f" "$TARGET/$f"
  done < <(payload_files)
  patch_options
  say "✅ 汉化已应用。备份在 backups/$TS/，如需回退运行: bash install.sh restore $TS"
}

# 可选 mods（JEI 拼音搜索）：装进实例 mods/，并登记进当前备份以便恢复时删除
do_pinyin() {
  if [ ! -d "$PINYIN_DIR" ]; then
    say "（未找到 $PINYIN_DIR 目录，跳过可选mods）"
    return
  fi
  found=0
  for j in "$PINYIN_DIR"/*.jar; do
    [ -e "$j" ] || continue
    found=1
    base="$(basename "$j")"
    # 就地解压模式没有本次备份（BK 为空），只装不登记
    if [ -n "$BK" ]; then
      if [ -f "$TARGET/mods/$base" ]; then
        mkdir -p "$BK/mods"
        cp -p "$TARGET/mods/$base" "$BK/mods/$base"
      else
        printf 'mods/%s\n' "$base" >> "$BK/新增文件清单.txt"
      fi
    fi
    cp -p "$j" "$TARGET/mods/$base"
    say "  已安装: mods/$base"
  done
  if [ "$found" = 1 ]; then
    say "✅ 可选 mod（JEI 拼音搜索）已安装"
  else
    say "（$PINYIN_DIR 内没有 jar，跳过）"
  fi
}

do_restore() {
  BROOT="$SCRIPT_DIR/backups"
  if [ ! -d "$BROOT" ] || [ -z "$(ls -1 "$BROOT" 2>/dev/null)" ]; then
    say "❌ 没有任何备份"
    exit 1
  fi
  choice="${1:-}"
  if [ -z "$choice" ]; then
    say "可用备份："
    ls -1 "$BROOT"
    latest="$(ls -1 "$BROOT" | tail -1)"
    printf '要恢复的备份名 [回车 = %s]: ' "$latest"
    read -r choice || choice=""
    [ -z "$choice" ] && choice="$latest"
  fi
  BKR="$BROOT/$choice"
  if [ ! -d "$BKR" ]; then
    say "❌ 备份不存在: $choice"
    exit 1
  fi
  if [ -f "$BKR/新增文件清单.txt" ]; then
    while IFS= read -r f; do
      rm -f "$TARGET/$f"
    done < "$BKR/新增文件清单.txt"
  fi
  (cd "$BKR" && find . -type f ! -name '新增文件清单.txt' | while IFS= read -r f; do
    f="${f#./}"
    mkdir -p "$TARGET/$(dirname "$f")"
    cp -p "$f" "$TARGET/$f"
  done)
  say "✅ 已恢复备份 ${choice}（含 options.txt，安装时新增的文件已删除）"
}

check_target
case "${1:-}" in
  apply)             do_apply ;;
  apply-with-pinyin) do_apply; do_pinyin ;;
  backup)            do_backup ;;
  restore)           do_restore "${2:-}" ;;
  *)
    say "══════════════════════════════════════════"
    say " ATM10 7.2 汉化补丁 · 绿油油版 — 安装器"
    say " 目标实例: $TARGET"
    say "══════════════════════════════════════════"
    say " [1] 应用汉化（自动先备份被覆盖文件）"
    say " [2] 仅备份"
    say " [3] 恢复备份"
    say " [q] 退出"
    printf '请选择: '
    read -r c || c=""
    case "$c" in
      1)
        do_apply
        printf '是否同时安装可选的 JEI 拼音搜索 mod？[y/N]: '
        read -r ans || ans=""
        case "$ans" in
          y|Y) do_pinyin ;;
          *)   say "（跳过可选mods，之后可运行: bash install.sh apply-with-pinyin）" ;;
        esac
        ;;
      2) do_backup ;;
      3) do_restore "" ;;
      *) say "已退出" ;;
    esac
    ;;
esac
