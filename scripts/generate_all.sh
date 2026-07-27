#!/usr/bin/env bash
# atm10-zh-cn — All the Mods 10 简体中文汉化补丁「绿油油版」
# Copyright (C) 2026 星野夢華 (Hoshino Yumeka)
# SPDX-License-Identifier: GPL-3.0-or-later
#
# 重新生成全部「由脚本产出」的汉化资源。
#
# 这些产物**不入 git**：仓库里只留生成器和手写的源数据，图片按需重建。
# 这样仓库里不可能出现一张手改过、与生成器输出不一致的图——多版本维护下这点尤其要紧，
# 因为同一份生成器要对三个整合包版本负责，任何「手动补一下」都会在别的版本上失效。
#
# 需要两样东西：
#   - assets-src/fonts/    全部 OFL，跑 scripts/fetch_fonts.sh 取（不入 git）
#   - 整合包本体           ATM_PACK_ROOT 指向实例根目录，或官方包解压出的 overrides 目录
#
# 两者都不依赖 macOS：字体是下载来的，源图来自整合包，所以 Linux 的 CI
# 能产出与本机**逐字节相同**的结果（已实测 200 张全等）。
#
# 用法:
#   ATM_PACK_ROOT=/path/to/instance ./scripts/generate_all.sh
set -euo pipefail
cd "$(dirname "$0")/.."

: "${ATM_PACK_ROOT:=/Users/yumeka/Documents/minecraft/.minecraft/versions/All the Mods 10}"
export ATM_PACK_ROOT
[ -d "$ATM_PACK_ROOT/kubejs" ] || {
  echo "❌ ATM_PACK_ROOT 不像整合包目录（缺 kubejs/）: $ATM_PACK_ROOT"; exit 1; }

for f in pixel-10.ttf pixel-12.ttf bold.otf thin.otf serif.otf; do
  [ -f "assets-src/fonts/$f" ] || {
    echo "❌ 缺字体 assets-src/fonts/$f —— 先跑 scripts/fetch_fonts.sh"; exit 1; }
done

echo "▶ 任务书横幅艺术字（200 张）"
python3 scripts/gen_quest_banners.py
echo "▶ 主菜单按钮（14 张）"
python3 scripts/gen_menu_buttons.py
echo "✅ 生成完毕"
