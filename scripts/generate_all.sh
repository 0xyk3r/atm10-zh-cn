#!/usr/bin/env bash
# atm10-zh-cn — All the Mods 10 简体中文汉化补丁「绿油油版」
# Copyright (C) 2026 星野夢華 (Hoshino Yumeka)
# SPDX-License-Identifier: GPL-3.0-or-later
#
# 从 src/ 摊出货树，再把全部「由脚本产出」的汉化资源生成进去。
#
# 仓库里**没有任何一棵出货用的目录树**：`kubejs/`、`config/`、`resourcepacks/`、
# `mods/` 都是产物，落在 build/ 下（.gitignore 排除）。仓库里只有 src/（手写真源
# 与上游改动映射）和 scripts/（生成器）。这样就不可能出现「仓库里躺着一份手改过、
# 和生成器输出对不上的文件」，也不可能把「旧上游 + 我们的改动」当成新版本发出去。
#
# 需要两样东西：
#   - assets-src/fonts/    全部 OFL，跑 scripts/fetch_fonts.sh 取（同样不入 git）
#   - 整合包本体           ATM_PACK_ROOT 指向实例根目录，或官方包解压出的 overrides 目录
#     其中读取 mod jar 的那几步还需要 mods/ 里有真实的 jar；官方包的 overrides 里没有，
#     所以在 CI 上要么指向装好的实例，要么按 manifest 把 jar 备齐（见 build.yml）。
#
# 两者都不依赖 macOS：字体是下载来的，源图与 jar 来自整合包。
# Linux 与 macOS 的产物**像素级基本一致**：2026-07-27 拿 CI 产物与本机产物逐张比，
# 200 张横幅里 197 张像素完全相同，3 张（ATM / ATM之星 / ATM之星自动化）因两边
# freetype 版本不同、字形栅格化有细微差别——目视等价，位置字号都对。
# PNG 字节则普遍不同（zlib 版本差异），所以**别拿 sha1 当回归判据**，要比就比像素。
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

HAVE_JARS=0
[ -d "$ATM_PACK_ROOT/mods" ] && [ "$(ls "$ATM_PACK_ROOT"/mods/*.jar 2>/dev/null | wc -l)" -ge 20 ] && HAVE_JARS=1

echo "▶ 从 src/ 摊出货树（含 VaultPatcher 模块与跟随原版的文件）"
python3 scripts/assemble.py

echo "▶ 任务书横幅艺术字（200 张）"
python3 scripts/gen_quest_banners.py
echo "▶ 主菜单按钮（14 张）"
python3 scripts/gen_menu_buttons.py

if [ "$HAVE_JARS" = 1 ]; then
  # 这几步要读 mod jar 里的 en_us / 注册表 / 导览书，只有 overrides 是不够的
  echo "▶ 导览书（Patchouli / AE2 Guide / Oracle Index …）：拿 jar 里那份现套译文"
  python3 scripts/gen_books.py
  echo "▶ 资源蜂：双端脚本（真源是资源包的 productivebees/zh_cn.json，这里只做派生）"
  python3 scripts/gen_pb_hanhua.py
  echo "▶ 奖杯名（约 2.5 万条）"
  python3 scripts/gen_trophy_names.py
  echo "▶ 精致存储木头名（约 1500 条）"
  python3 scripts/gen_wood_names.py
  echo "▶ 上游格式串快照（check.py 的占位符校验靠它）"
  python3 scripts/gen_format_snapshot.py "$ATM_PACK_ROOT"
else
  echo "⚠️ ATM_PACK_ROOT 下没有 mod jar，跳过需要读 jar 的生成器"
  echo "   （资源蜂脚本 / 奖杯名 / 木头名 / 格式串快照）"
  echo "   这些产物缺失时 build_dist.sh 会报错，CI 请把 jar 备齐。"
fi
echo "✅ 生成完毕：build/common/"
