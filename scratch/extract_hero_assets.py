import os
import re

files = [
    "all-inclusive-private-island-rental.html",
    "bahamas-private-island-rental.html",
    "caribbean-private-island-rental.html",
    "exclusive-private-island-rental.html",
    "luxury-private-island-rental.html",
    "maldives-private-island-rental.html",
    "private-island-for-rent.html"
]

directory = r"c:\Users\imran\OneDrive\Desktop\ELB code"

for filename in files:
    path = os.path.join(directory, filename)
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            with open(path, 'r', encoding='latin-1') as f:
                content = f.read()
        
        print(f"\n================ FILE: {filename} ================")
        
        # Find Canonical URL
        canonical = ""
        canonical_match = re.search(r'rel="canonical"\s+href="([^"]+)"', content)
        if canonical_match:
            canonical = canonical_match.group(1)
        else:
            canonical_match = re.search(r"rel='canonical'\s+href='([^']+)'", content)
            if canonical_match:
                canonical = canonical_match.group(1)
        print(f"Canonical URL: {canonical}")
        
        # Find Hero Image
        hero_img = ""
        # Look for background: url(...) or background-image: url(...) in style tag
        bg_match = re.search(r"url\(['\"]?([^'\")]+)['\"]?\)", content)
        if bg_match:
            hero_img = bg_match.group(1)
        print(f"First image asset found: {hero_img}")
