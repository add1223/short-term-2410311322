#!/usr/bin/env bash
# 本地 CI 检查脚本（复用集中期 arena-lite 的三步结构）
# 随 W3 实现推进,如需扩展(如 mypy、ruff)在此追加。
set -euo pipefail

echo "== python tests =="
if [ -d tests ] && find tests -name 'test_*.py' -o -name '*_test.py' | grep -q .; then
  python -m pytest -q
else
  echo "no tests yet, skip"
fi

echo "== python syntax =="
if [ -d app ]; then
  python -m compileall -q app
fi
if [ -d tests ]; then
  python -m compileall -q tests
fi

echo "== whitespace check =="
git diff --check 2>/dev/null || echo "not a git repo yet, skip whitespace check"

echo "local checks passed"
