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
    "contact.html",
    "luxury-villa-rentals.html",
    "luxury-yacht-rentals.html",
    "elite-private-jet-charter.html",
    "private-boat-trip-mallorca-to-formentera.html",
    "mallorca-to-ibiza-private-boat.html"
]

workspace_dir = r"c:\Users\imran\OneDrive\Desktop\ELB code"

for fn in files:
    path = os.path.join(workspace_dir, fn)
    print(f"=== {fn} ===")
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()
    
    # Search for all fetch calls or submit logic in the javascript
    # Let's extract any blocks of code containing fetch or xmlhttprequest
    fetch_blocks = re.findall(r'(\b(?:fetch|sendLeadToDestinations|formsubmit|submit-lead)\b.*?)\n\s*\n', html, re.I | re.S)
    print(f"Found {len(fetch_blocks)} matching JS blocks:")
    for idx, block in enumerate(fetch_blocks[:5]):
        # remove HTML tags in script block for clean output
        cleaned = re.sub(r'<[^>]+>', ' ', block).strip()
        cleaned = re.sub(r'\s+', ' ', cleaned)
        print(f"  Block {idx+1}: {cleaned[:200]}")
    print("-" * 80)
