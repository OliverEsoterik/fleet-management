#!/usr/bin/env bash
# tools/orchestrate.sh — Poll the work/ directory and route consultation requests
#
# Usage:
#   ./orchestrate.sh <project-dir> <primary-agent-name> [max-depth]
#
# Example:
#   ./orchestrate.sh /home/oliver/my-project code-reviewer 5
#
# Loops up to max-depth times, checking for:
#   - work/escalation.md  → break (unresolvable issue)
#   - work/done/<primary>.md → break (completion)
#   - work/todo/*.md → route each to the appropriate consultant in tmux
#
# Default max-depth: 5

set -euo pipefail

if [ $# -lt 2 ]; then
  echo "Usage: $0 <project-dir> <primary-agent-name> [max-depth]"
  exit 1
fi

PROJECT_DIR="$1"
PRIMARY_AGENT="$2"
MAX_DEPTH="${3:-5}"
DEPTH=0

cd "$PROJECT_DIR"

while [ $DEPTH -lt $MAX_DEPTH ]; do
  # Check for escalation
  if [ -f work/escalation.md ]; then
    echo "--- Escalation detected ---"
    cat work/escalation.md
    break
  fi

  # Check for completion
  if [ -f "work/done/${PRIMARY_AGENT}.md" ]; then
    echo "--- Primary agent completed ---"
    break
  fi

  # Check for consultation requests
  # Use nullglob behaviour: if no .md files, set is empty
  shopt -s nullglob
  todo_files=(work/todo/*.md)
  shopt -u nullglob

  if [ ${#todo_files[@]} -eq 0 ]; then
    echo "No todos, primary still working... (depth ${DEPTH}/${MAX_DEPTH})"
    sleep 10
    DEPTH=$((DEPTH + 1))
    continue
  fi

  for todo in "${todo_files[@]}"; do
    agent=$(basename "$todo" .md)
    echo "--- Routing to consultant: $agent ---"

    # Extract the requesting agent from the todo file header
    requested_by=$(head -1 "$todo" | sed 's/.*requested_by: //')

    session="pi-agent-$(date +%s)-${agent}"
    agent_dir="${PROJECT_DIR}/agents/${agent}"
    workflow_file="${PROJECT_DIR}/agents/shared/WORKFLOW.md"

    if [ ! -d "$agent_dir" ]; then
      echo "Warning: agent directory $agent_dir not found — writing gap to work/recap.md"
      echo "Missing agent: $agent (requested by $requested_by)" >> work/recap.md
      rm "$todo"
      continue
    fi

    tmux new-session -d -s "$SESSION" -n agent \
      "cd '$agent_dir' && cat brain.md '$workflow_file' 2>/dev/null | pi -p \"Read $todo and provide your consultation. Write your response to work/response/${requested_by}/${agent}.md\"; echo '--- CONSULTANT DONE ---'; sleep 3600"
    echo "Consultant started in tmux session: $session"

    # Wait for consultant to finish, capture output
    sleep 30
    tmux capture-pane -t "$session" -p || true
    tmux kill-session -t "$session" 2>/dev/null || true
    rm "$todo"
  done

  DEPTH=$((DEPTH + 1))
done

# Handle incomplete work
if [ $DEPTH -ge $MAX_DEPTH ]; then
  echo "--- Reached max depth (${MAX_DEPTH}) ---"
  shopt -s nullglob
  remaining=(work/todo/*.md)
  shopt -u nullglob
  if [ ${#remaining[@]} -gt 0 ]; then
    echo "Unresolved consultations:"
    cat "${remaining[@]}"
  fi
fi