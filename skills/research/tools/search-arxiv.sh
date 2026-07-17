#!/usr/bin/env bash
# search-arxiv.sh — Search arXiv.org via public API
# Usage: bash search-arxiv.sh <query> [max_results]
# Outputs markdown to stdout.

set -euo pipefail

QUERY="${1:?Usage: search-arxiv.sh <query> [max_results]}"
MAX="${2:-10}"

# arXiv API expects query terms in a specific format
# URL-encode the query (minimal — just spaces to +)
ENCODED_QUERY=$(echo "$QUERY" | sed 's/ /+/g')

URL="https://export.arxiv.org/api/query?search_query=all:${ENCODED_QUERY}&start=0&max_results=${MAX}"

RESPONSE=$(curl -s -f "$URL" 2>/dev/null) || {
  echo "Error: arXiv API request failed (status $?)"
  exit 1
}

# Check if we got actual XML
if ! echo "$RESPONSE" | python3 -c "import sys; xml=sys.stdin.read(); print('yes' if '<feed' in xml else 'no')" 2>/dev/null; then
  echo "Error: arXiv returned non-XML response"
  exit 1
fi

# Parse with python3
python3 -c "
import sys, xml.etree.ElementTree as ET

xml_str = sys.stdin.read()
root = ET.fromstring(xml_str)

ns = {
    'atom': 'http://www.w3.org/2005/Atom',
    'arxiv': 'http://arxiv.org/schemas/atom',
    'opensearch': 'http://a9.com/-/spec/opensearch/1.1/'
}

total = root.find('.//opensearch:totalResults', ns)
total_str = total.text if total is not None else 'unknown'

entries = root.findall('atom:entry', ns)
print(f'# arXiv Search Results')
print(f'Query: {sys.argv[1]}')
print(f'Total results: {total_str}')
print(f'Showing: {len(entries)}')
print()

for entry in entries:
    title = entry.find('atom:title', ns)
    title_text = title.text.strip().replace(chr(10), ' ') if title is not None and title.text else 'No title'
    
    summary = entry.find('atom:summary', ns)
    summary_text = summary.text.strip().replace(chr(10), ' ')[:500] if summary is not None and summary.text else ''
    
    published = entry.find('atom:published', ns)
    published_text = published.text[:10] if published is not None and published.text else 'Unknown'
    
    authors = entry.findall('atom:author/atom:name', ns)
    author_names = [a.text for a in authors if a.text]
    authors_str = ', '.join(author_names) if author_names else 'Unknown'
    
    link = entry.find('atom:id', ns)
    link_text = link.text.strip() if link is not None and link.text else ''
    
    categories = entry.findall('atom:category', ns)
    cat_terms = [c.get('term', '') for c in categories]
    cats_str = ', '.join(cat_terms) if cat_terms else ''
    
    doi = entry.find('arxiv:doi', ns)
    doi_str = doi.text if doi is not None and doi.text else ''
    
    print(f'## {title_text}')
    print(f'- **Authors:** {authors_str}')
    print(f'- **Published:** {published_text}')
    print(f'- **Categories:** {cats_str}')
    if doi_str:
        print(f'- **DOI:** {doi_str}')
    print(f'- **URL:** {link_text}')
    print()
    print(f'{summary_text}')
    print()
    print('---')
    print()
" "$QUERY" <<< "$RESPONSE"