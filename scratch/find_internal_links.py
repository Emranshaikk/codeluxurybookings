import os
import re

ROOT_DIR = r"c:\Users\imran\OneDrive\Desktop\ELB code"

old_urls = [
    # Cluster A
    "boat-trip-from-mallorca-to-formentera",
    "yacht-charter-mallorca-to-formentera",
    "mallorca-to-formentera-private-boat-cost",
    "yacht-charter-mallorca-formentera",
    "luxury-yacht-rentals/boat-trip-from-mallorca-to-formentera",
    # Cluster B
    "mallorca-to-ibiza-private-boat-charter",
    "luxury-yacht-rentals/mallorca-to-ibiza-private-boat",
    "private-yacht-from-ibiza-to-mallorca"
]

html_files = [f for f in os.listdir(ROOT_DIR) if f.endswith(".html")]

print("Scanning all HTML files for references to old cluster URLs...")

matches_found = {}

for filename in html_files:
    filepath = os.path.join(ROOT_DIR, filename)
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    for url in old_urls:
        # Search for exact or variations with/without trailing slashes and extensions
        pattern = re.compile(r'href=["\'][^"\']*' + re.escape(url) + r'[^"\']*["\']', re.I)
        matches = pattern.findall(content)
        if matches:
            if url not in matches_found:
                matches_found[url] = []
            matches_found[url].append((filename, matches))

# Also search sitemap.xml
sitemap_path = os.path.join(ROOT_DIR, "sitemap.xml")
if os.path.exists(sitemap_path):
    with open(sitemap_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    for url in old_urls:
        if url in content:
            if url not in matches_found:
                matches_found[url] = []
            matches_found[url].append(("sitemap.xml", [f"Reference in sitemap.xml"]))

for url, refs in sorted(matches_found.items()):
    print(f"\nReferences for URL: '{url}' ({len(refs)} files):")
    for file, matches in refs:
        print(f"  - In {file}:")
        for m in set(matches):
            print(f"    {m}")
