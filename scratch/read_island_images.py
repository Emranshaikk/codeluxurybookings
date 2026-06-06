import os
import re

workspace_dir = r"c:\Users\imran\OneDrive\Desktop\ELB code"
filepath = os.path.join(workspace_dir, "all-inclusive-private-island-rental.html")

content = None
# Try different encodings
for encoding in ['utf-8', 'utf-16', 'utf-16le', 'latin-1']:
    try:
        with open(filepath, 'r', encoding=encoding) as f:
            content = f.read()
        print(f"Successfully read file with encoding: {encoding}")
        break
    except Exception as e:
        continue

if not content:
    print("Could not read file!")
    exit(1)

# Find all img src, background style URLs
imgs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', content, re.IGNORECASE)
bg_urls = re.findall(r'url\(["\']?([^"\'\)]+)["\']?\)', content, re.IGNORECASE)

all_refs = sorted(list(set(imgs + bg_urls)))

print(f"Total image/background references found: {len(all_refs)}")
for ref in all_refs:
    # Resolve the path
    clean_ref = ref.lstrip('/')
    local_path = os.path.join(workspace_dir, clean_ref.replace('/', os.sep))
    exists = os.path.exists(local_path)
    
    print(f"\nRef: {ref}")
    print(f"  Local path: {local_path}")
    print(f"  Exists: {exists}")
    if exists:
        print(f"  File size: {os.path.getsize(local_path)} bytes")
