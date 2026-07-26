#!/usr/bin/env bash
# atm10-zh-cn — All the Mods 10 简体中文汉化补丁「绿油油版」
# Copyright (C) 2026 星野夢華 (Hoshino Yumeka)
# SPDX-License-Identifier: GPL-3.0-or-later
#
# 取任务书横幅生成脚本要用的点阵中文字体。
#
# 字体本身不入 git（十来 MB，而生成好的 PNG 已经在仓库里，玩家和 CI 都不需要它），
# 只有要重跑 scripts/gen_quest_banners.py 时才需要跑这个。版本号写死，
# 保证同一份脚本任何时候跑出来的图都一样。
#
# 字体：缝合像素字体 Fusion Pixel Font（OFL-1.1），TakWolf 出品，
# 由方舟像素字体 + Cubic 11 + Galmuri 拼合补全覆盖，随包 OFL 一并下载。
# 选它而不是方舟本体，是因为方舟 zh_cn 12px 缺「旋热然聚嗡蟒骏」这类常用字，
# 缺字会渲染成 .notdef 豆腐块。
set -euo pipefail

VER=2026.07.20
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/assets-src/fonts"
BASE="https://github.com/TakWolf/fusion-pixel-font/releases/download/${VER}"

mkdir -p "$DIR"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

for px in 10 12; do
    f="fusion-pixel-font-${px}px-proportional-ttf-v${VER}.zip"
    echo "下载 ${f} ..."
    curl -fsSL -o "$TMP/$f" "$BASE/$f"
    unzip -o -q "$TMP/$f" -d "$TMP/x$px"
    cp "$TMP/x$px/fusion-pixel-${px}px-proportional-zh_hans.ttf" "$DIR/pixel-${px}.ttf"
done
cp "$TMP/x12/OFL.txt" "$DIR/pixel-OFL.txt"
rm -rf "$DIR/pixel-LICENSES"
cp -R "$TMP/x12/LICENSES" "$DIR/pixel-LICENSES"

echo "完成："
ls -1 "$DIR"
