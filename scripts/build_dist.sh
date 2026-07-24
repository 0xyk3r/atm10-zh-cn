#!/usr/bin/env bash
# 打分发包：dist/ATM10-7.2-汉化补丁-绿油油版-星野夢華-v<版本>.zip
# 资源包 zip 不入 git，由本脚本从 resourcepacks/ATM10汉化包-7.2/ 源码目录现场压缩。
# 用法: ./scripts/build_dist.sh 7.2.0
set -euo pipefail
cd "$(dirname "$0")/.."

VERSION="${1:?用法: build_dist.sh <版本号, 如 7.2.0>}"
PACK_NAME="ATM10汉化包-7.2"
DIST_NAME="ATM10-7.2-汉化补丁-绿油油版-星野夢華"

python3 scripts/check.py

STAGE="dist/${DIST_NAME}"
rm -rf "$STAGE"
mkdir -p "$STAGE/resourcepacks"

# 资源包：源码目录 → zip（zip 根必须直接是 assets/ pack.mcmeta）
(cd "resourcepacks/${PACK_NAME}" && zip -X -q -r "../../${STAGE}/resourcepacks/${PACK_NAME}.zip" . -x '*.DS_Store')

# 其余汉化文件 + 安装脚本 + 文档
cp -R config kubejs mods vaultpatcher 可选mods-拼音搜索 "$STAGE/"
cp installer/install.sh installer/install.ps1 "installer/双击安装-Windows.bat" "$STAGE/"
cp README.md CHANGELOG.md "关于内置汉化Mod的说明(BBSMC).txt" "原版说明与致谢(BBSMC).txt" "$STAGE/"
chmod +x "$STAGE/install.sh"
find "$STAGE" -name '.DS_Store' -delete

OUT="dist/${DIST_NAME}-v${VERSION}.zip"
rm -f "$OUT"
(cd dist && zip -X -q -r "${DIST_NAME}-v${VERSION}.zip" "${DIST_NAME}")

echo "已生成: $OUT ($(du -h "$OUT" | cut -f1))"
unzip -l "$OUT" | tail -1
