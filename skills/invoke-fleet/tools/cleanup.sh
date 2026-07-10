#!/usr/bin/env bash
# tools/cleanup.sh — Remove work/ artifacts from a project
#
# Usage:
#   ./cleanup.sh [project-dir]
#
# Defaults to current directory.
# Removes: work/todo/ work/response/ work/done/ work/escalation.md

set -euo pipefail

PROJECT_DIR="${1:-$(pwd)}"
cd "$PROJECT_DIR"

rm -rf work/todo work/response work/done work/escalation.md 2>/dev/null
echo "Cleaned up work/ artifacts in $PROJECT_DIR"