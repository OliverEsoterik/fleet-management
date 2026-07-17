#!/usr/bin/env bash
# search-archive.sh — Search Archive.org via public API
# Usage: bash search-archive.sh <query> [max_results]
# Outputs markdown to stdout.

set -euo pipefail

QUERY="${1:?Usage: search-archive.sh <query> [max_results]}"
MAX="${2:-10}"

# URL-encode the query
ENCODED_QUERY=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$QUERY'))")

URL="https://archive.org/advancedsearch.php?q=${ENCODED_QUERY}&fl%5B%5D=identifier&fl%5B%5D=title&fl%5B%5D=description&fl%5B%5D=creator&fl%5B%5D=date&fl%5B%5D=downloads&fl%5B%5D=avg_rating&fl%5B%5D=mediatype&fl%5B%5D=collection&sort%5B%5D=downloads+desc&sort%5B%5D=&rows=${MAX}&page=1&output=json"

RESPONSE=$(curl -s -f "$URL" 2>/dev/null) || {
  echo "Error: Archive.org API request failed (status $?)"
  exit 1
}

python3 -c "
import json, sys

data = json.loads(sys.stdin.read())
response = data.get('response', {})
num_found = response.get('numFound', 0)
docs = response.get('docs', [])

print(f'# Archive.org Search Results')
print(f'Query: {sys.argv[1]}')
print(f'Total results: {num_found}')
print(f'Showing: {len(docs)}')
print()

for doc in docs:
    title = doc.get('title', 'No title')
    creator = doc.get('creator', 'Unknown')
    date = str(doc.get('date', ''))[:10] if doc.get('date') else 'Unknown'
    mediatype = doc.get('mediatype', 'unknown')
    downloads = doc.get('downloads', 0)
    rating = doc.get('avg_rating', 'N/A')
    identifier = doc.get('identifier', '')
    description = doc.get('description', '')
    if description and len(description) > 400:
        description = description[:400] + '...'
    
    collection = doc.get('collection', [])
    collection_str = ', '.join(collection[:5]) if collection else ''
    
    url = f'https://archive.org/details/{identifier}' if identifier else ''
    
    print(f'## {title}')
    print(f'- **Creator:** {creator}')
    print(f'- **Date:** {date}')
    print(f'- **Type:** {mediatype}')
    print(f'- **Downloads:** {downloads}  **Rating:** {rating}')
    if collection_str:
        print(f'- **Collections:** {collection_str}')
    if url:
        print(f'- **URL:** {url}')
    if description:
        print()
        print(f'{description}')
    print()
    print('---')
    print()
" "$QUERY" <<< "$RESPONSE"