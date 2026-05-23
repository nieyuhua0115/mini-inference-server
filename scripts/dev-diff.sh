#!/usr/bin/env bash
set -euo pipefail

echo "== Git Status =="
git status --short

echo ""
echo "== Changed Files =="
git diff --name-only

echo ""
echo "== Diff Stat =="
git diff --stat

echo ""
echo "== Tests =="
uv run pytest
