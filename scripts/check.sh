#!/usr/bin/env bash
# ?? CI ?????????? arena-lite ??????
# ? W3 ????,????(? mypy?ruff)?????
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
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "not a git repo yet, skip whitespace check"
else
  if git diff --check; then
    echo "no whitespace errors"
  else
    echo "ERROR: trailing whitespace or CRLF issues found above" >&2
    exit 1
  fi
fi

echo "local checks passed"
