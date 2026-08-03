import os
import re
import sys

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

for fn in files:
    path = os.path.join(r"c:\Users\imran\OneDrive\Desktop\ELB code", fn)
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()
    
    print(f"=== {fn} ===")
    lines = html.split('\n')
    for i, line in enumerate(lines):
        if '<h1>' in line or '<h1 ' in line or 'class="hero-' in line.lower() or 'class="page-hero' in line.lower():
            print(f"  Line {i+1}: {line.strip()[:120]}")
            # print subsequent 5 lines
            for j in range(1, 6):
                if i+j < len(lines):
                    print(f"    + {lines[i+j].strip()[:100]}")
    print("-" * 80)
