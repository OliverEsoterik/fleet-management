#!/usr/bin/env bash
# search-github.sh — Search GitHub repositories via gh CLI
# Usage: bash search-github.sh <query> [max_results]
# Outputs markdown to stdout.

set -euo pipefail

QUERY="${1:?Usage: search-github.sh <query> [max_results]}"
MAX="${2:-10}"

if ! command -v gh &>/dev/null; then
  echo "Error: 'gh' CLI not found. Install from https://cli.github.com/"
  exit 1
fi

if ! gh auth status &>/dev/null; then
  echo "Error: not authenticated with GitHub. Run 'gh auth login' first."
  exit 1
fi

OUTPUT=$(gh search repos "$QUERY" \
  --limit "$MAX" \
  --json fullName,description,url,stargazersCount,forksCount,language,updatedAt,createdAt,license 2>/dev/null) || {
  echo "Error: GitHub search failed. Check network or rate limits."
  exit 1
}

python3 -c "
import json, sys

results = json.loads(sys.stdin.read())

print('# GitHub Search Results')
print(f'Query: {sys.argv[1]}')
print(f'Showing: {len(results)}')
print()

for r in results:
    full_name = r.get('fullName', 'Unknown')
    desc = r.get('description') or ''
    stars = r.get('stargazersCount', 0)
    forks = r.get('forksCount', 0)
    lang = r.get('language') or ''
    lang_str = f'  **Language:** {lang}' if lang else ''
    updated = r.get('updatedAt', '')[:10] if r.get('updatedAt') else ''
    created = r.get('createdAt', '')[:10] if r.get('createdAt') else ''
    license_name = r.get('license', {})
    license_str = f'  **License:** {license_name[\"name\"]}' if license_name else ''
    url = r.get('url', '')

    print(f'## {full_name}')
    if desc:
        print(f'- **Description:** {desc}')
    print(f'- **Stars:** {stars}  **Forks:** {forks}{lang_str}{license_str}')
    print(f'- **Created:** {created}  **Updated:** {updated}')
    print(f'- **URL:** {url}')
    print()
    print('---')
    print()
" "$QUERY" <<< "$OUTPUT"