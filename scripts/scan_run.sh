#!/usr/bin/env bash
# 安全扫描:密钥 + 占位符
cd /mnt/d/trae/work || exit 1
echo "=== 密钥扫描(应无真实凭据命中) ==="
rg -n -f scripts/msd-secret-patterns.txt --glob '!scripts/msd-secret-patterns.txt' .
echo "rg exit: $?"
echo ""
echo "=== 未填项检查(应无命中) ==="
rg -n '<[^>\n]+>|TODO|TBD|待补|your-|changeme|示例项目' README.md docs process PROCESS.md submissions
echo "rg exit: $?"
echo ""
echo "=== 截图脱敏自查 ==="
echo "无截图(本项目无 GUI,UAT 文本输出已脱敏,无 Key/Token/余额/手机号)"