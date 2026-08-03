import os
import re
from bs4 import BeautifulSoup

files_to_check = [
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

print("Extracting current metadata and price indicators...")
print("=" * 80)

for filename in files_to_check:
    path = os.path.join(r"c:\Users\imran\OneDrive\Desktop\ELB code", filename)
    if not os.path.exists(path):
        print(f"File not found: {filename}")
        continue
        
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()
        
    soup = BeautifulSoup(html, 'html.parser')
    
    title = soup.title.string if soup.title else "NO TITLE"
    
    meta_desc = ""
    meta_tag = soup.find('meta', attrs={'name': 'description'}) or soup.find('meta', attrs={'property': 'og:description'})
    if meta_tag:
        meta_desc = meta_tag.get('content', '')
    else:
        # manual search for meta description
        match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']+)["\']', html, re.I)
        if match:
            meta_desc = match.group(1)
            
    # Find price indicators in text (e.g. from $X or €X)
    prices = re.findall(r'(?:from\s+)?(?:[\$\u20ac\u00a3]|EUR|USD)\s*\d{1,3}(?:[,\.]\d{3})*(?:\s*/\s*(?:hr|hour|day|week|night))?', html, re.I)
    unique_prices = sorted(list(set(prices)))[:10] # limit to first 10
    
    print(f"File: {filename}")
    print(f"  Title:       {title}")
    print(f"  Description: {meta_desc}")
    print(f"  Prices found in text: {unique_prices}")
    print("-" * 80)
