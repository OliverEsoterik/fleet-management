#!/usr/bin/env bash
# tools/delegate.sh — Launch a primary agent in a new tmux session
#
# Usage:
#   ./delegate.sh <project-dir> <agent-name> "<task-description>"
#
# Example:
#   ./delegate.sh /home/oliver/my-project code-reviewer "Review the auth module for vulnerabilities"
#
# Creates a tmux session named: pi-agent-<unix-timestamp>-<agent-name>
# The session runs `cat brain.md WORKFLOW.md | pi -p "<task>"` inside the agent's directory.
# After completion it prints "--- PRIMARY DONE ---" and sleeps 3600s for manual inspection.

set -euo pipefail

if [ $# -lt 3 ]; then
  echo "Usage: $0 <project-dir> <agent-name> <task-description>"
  exit 1
fi

PROJECT_DIR="$1"
AGENT_NAME="$2"
TASK_DESC="$3"
SESSION="pi-agent-$(date +%s)-${AGENT_NAME}"
AGENT_DIR="${PROJECT_DIR}/agents/${AGENT_NAME}"
WORKFLOW_FILE="${PROJECT_DIR}/agents/shared/WORKFLOW.md"

if [ ! -d "$AGENT_DIR" ]; then
  echo "Error: agent directory not found at $AGENT_DIR"
  exit 1
fi

if [ ! -f "$WORKFLOW_FILE" ]; then
  echo "Warning: WORKFLOW.md not found at $WORKFLOW_FILE"
fi

tmux new-session -d -s "$SESSION" -n agent \
  "cd '$AGENT_DIR' && cat brain.md '$WORKFLOW_FILE' 2>/dev/null | pi -p \"$TASK_DESC\"; echo '--- PRIMARY DONE ---'; sleep 3600"

echo "$SESSION"