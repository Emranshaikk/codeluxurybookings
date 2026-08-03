import os
import sys
import re

# Ensure stdout uses UTF-8
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

files = [
    "index.html",
    "about.html",
    "contact.html",
    "luxury-villa-rentals.html",
    "sunreef-catamaran-charter-price.html",
    "elite-private-jet-charter.html",
    "luxury-yacht-rentals.html",
    "blog.html",
    "7-best-private-jet-charter-in-dubai.html",
    "private-boat-trip-mallorca-to-formentera.html",
    "mallorca-to-ibiza-private-boat.html"
]

print("Extracting actual prices from files:")
print("=" * 80)

for f_name in files:
    path = os.path.join(r"c:\Users\imran\OneDrive\Desktop\ELB code", f_name)
    if not os.path.exists(path):
        print(f"File not found: {f_name}")
        continue
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Let's search for prices like: $X, €X, AED X, etc.
    # We want to find references with /hr, /day, /week, /night, etc.
    price_refs = re.findall(r'(?:from\s+)?(?:\$|||AED|EUR|USD)\s*\d{1,3}(?:[,\.]\d{3})*(?:\s*/\s*(?:hr|hour|day|week|night))?', content, re.I)
    
    # Let's also search for surrounding sentences containing digits and currency indicators
    sentences = []
    for line in content.split('\n'):
        if any(c in line for c in ['$', '€', '£', 'AED', 'EUR', 'USD']):
            cleaned = re.sub(r'<[^>]+>', ' ', line).strip()
            # replace multiple spaces
            cleaned = re.sub(r'\s+', ' ', cleaned)
            if len(cleaned) > 10:
                sentences.append(cleaned[:120])
                
    print(f"File: {f_name}")
    print(f"  Price matches: {sorted(list(set(price_refs)))[:5]}")
    print("  Lines with currency:")
    for s in sentences[:5]:
        print(f"    - {s}")
    print("-" * 80)
