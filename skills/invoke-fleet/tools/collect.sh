#!/usr/bin/env bash
# tools/collect.sh — Capture and clean up a tmux agent session
#
# Usage:
#   ./collect.sh <session-name>
#
# Example:
#   ./collect.sh pi-agent-1744234567-code-reviewer
#
# Captures pane output to stdout, then kills the session.

set -euo pipefail

if [ $# -lt 1 ]; then
  echo "Usage: $0 <session-name>"
  exit 1
fi

SESSION="$1"

if ! tmux has-session -t "$SESSION" 2>/dev/null; then
  echo "Warning: session '$SESSION' not found"
  exit 0
fi

tmux capture-pane -t "$SESSION" -p
tmux kill-session -t "$SESSION"