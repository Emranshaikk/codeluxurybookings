import sys
import re

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

files = [
    "elite-private-jet-charter.html",
    "luxury-yacht-rentals.html"
]

for fn in files:
    print(f"=== {fn} ===")
    with open(fn, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()
    
    # search for digits with $, €, £, AED
    matches = re.findall(r'[^.!?]*[\$€£]|AED\s*\d+[^.!?]*', html, re.I)
    for m in matches[:10]:
        cleaned = re.sub(r'<[^>]+>', ' ', m).strip()
        cleaned = re.sub(r'\s+', ' ', cleaned)
        # only keep if it has digits
        if any(c.isdigit() for c in cleaned):
            print(f"  Found: {cleaned[:100]}")
