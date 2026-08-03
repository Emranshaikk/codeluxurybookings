import os
import sys
import json
import re
from bs4 import BeautifulSoup

# Ensure stdout uses UTF-8
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

files = [
    "index.html",
    "elite-private-jet-charter.html",
    "luxury-yacht-rentals.html",
    "luxury-villa-rentals.html"
]

workspace_dir = r"c:\Users\imran\OneDrive\Desktop\ELB code"

for fn in files:
    path = os.path.join(workspace_dir, fn)
    print(f"=== {fn} ===")
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()
    
    soup = BeautifulSoup(html, 'html.parser')
    schemas = soup.find_all('script', type='application/ld+json')
    print(f"Found {len(schemas)} JSON-LD schema blocks:")
    for idx, s in enumerate(schemas):
        try:
            data = json.loads(s.string)
            print(f"  Block {idx+1}: @type is {data.get('@type', 'No type')} or key is {list(data.keys())[:3]}")
            if '@graph' in data:
                print(f"    Graph contains types: {[x.get('@type') for x in data['@graph']]}")
            else:
                print(f"    Type: {data.get('@type')}")
        except Exception as e:
            print(f"    Failed to parse block {idx+1}: {e}")
    print("-" * 80)
