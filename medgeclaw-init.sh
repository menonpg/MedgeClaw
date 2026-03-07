#!/usr/bin/env bash
# medgeclaw-init.sh — 将 MedgeClaw 项目配置注入 OpenClaw
# 用法: cd <MedgeClaw项目目录> && bash medgeclaw-init.sh
#
# 本脚本调用 sync.py（配置驱动的同步脚本）
# 修改同步内容请编辑 .medgeclaw-sync.yml

set -euo pipefail

MEDGECLAW_DIR="$(cd "$(dirname "$0")" && pwd)"

# 从 .env 加载配置
if [ -f "$MEDGECLAW_DIR/.env" ]; then
    set -a
    source "$MEDGECLAW_DIR/.env"
    set +a
fi

OPENCLAW_DIR="${OPENCLAW_DIR:-$HOME/.openclaw}"
CONFIG="$OPENCLAW_DIR/openclaw.json"

if [ ! -f "$CONFIG" ]; then
    echo "❌ 未找到 OpenClaw 配置: $CONFIG"
    echo "   请先安装并初始化 OpenClaw: https://docs.openclaw.ai"
    exit 1
fi

# 调用配置驱动的同步脚本
python3 "$MEDGECLAW_DIR/sync.py"

echo ""
echo "============================================================"
echo "✅ MedgeClaw 已注入 OpenClaw！"
echo ""
echo "   重启 gateway 使 skills 生效:"
echo "   openclaw gateway restart"
echo "============================================================"
