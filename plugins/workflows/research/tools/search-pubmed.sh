#!/usr/bin/env bash
# search-pubmed.sh — Search PubMed via NCBI EUtils API (free, no auth)
# Usage: bash search-pubmed.sh <query> [max_results]
# Outputs markdown to stdout.

set -euo pipefail

QUERY="${1:?Usage: search-pubmed.sh <query> [max_results]}"
MAX="${2:-10}"

# Step 1: Search for IDs
ENCODED_QUERY=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$QUERY'))")

SEARCH_URL="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=${ENCODED_QUERY}&retmax=${MAX}&retmode=json"
SEARCH_RESULT=$(curl -s -f "$SEARCH_URL" 2>/dev/null) || {
  echo "Error: PubMed search request failed"
  exit 1
}

ID_LIST=$(echo "$SEARCH_RESULT" | python3 -c "
import json, sys
data = json.load(sys.stdin)
ids = data.get('esearchresult', {}).get('idlist', [])
total = data.get('esearchresult', {}).get('count', '0')
print(f'TOTAL:{total}')
for i in ids:
    print(i)
")

TOTAL=$(echo "$ID_LIST" | grep '^TOTAL:' | cut -d: -f2)
IDS=$(echo "$ID_LIST" | grep -v '^TOTAL:' | paste -sd ',' -)

if [ -z "$IDS" ]; then
  echo "# PubMed Search Results"
  echo "Query: $QUERY"
  echo "Total results: 0"
  echo "No results found."
  exit 0
fi

# Step 2: Fetch details for found IDs
FETCH_URL="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id=${IDS}&retmode=json"
FETCH_RESULT=$(curl -s -f "$FETCH_URL" 2>/dev/null) || {
  echo "Error: PubMed fetch request failed"
  exit 1
}

python3 -c "
import json, sys

data = json.loads(sys.stdin.read())
results = data.get('result', {})
uids = results.get('uids', [])

print(f'# PubMed Search Results')
print(f'Query: {sys.argv[1]}')
print(f'Total results: {sys.argv[2]}')
print(f'Showing: {len(uids)}')
print()

for uid in uids:
    r = results.get(uid, {})
    title = r.get('title', 'No title')
    source = r.get('source', '')
    pubdate = r.get('pubdate', '')
    
    authors = r.get('authors', [])
    author_names = [a.get('name', '') for a in authors[:10]]
    authors_str = ', '.join(author_names) if author_names else 'Unknown'
    
    doi = ''
    for aid in r.get('articleids', []):
        if aid.get('idtype') == 'doi':
            doi = aid.get('value', '')
            break
    pubmed_url = f'https://pubmed.ncbi.nlm.nih.gov/{uid}/'
    
    print(f'## {title}')
    print(f'- **Authors:** {authors_str}')
    print(f'- **Source:** {source}')
    print(f'- **Published:** {pubdate}')
    if doi:
        print(f'- **DOI:** {doi}')
    print(f'- **URL:** {pubmed_url}')
    print()
    print('---')
    print()
" "$QUERY" "$TOTAL" <<< "$FETCH_RESULT"