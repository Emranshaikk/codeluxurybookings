import os
import sys
import re
from bs4 import BeautifulSoup

# Ensure stdout uses UTF-8
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

workspace_dir = r"c:\Users\imran\OneDrive\Desktop\ELB code"
index_path = os.path.join(workspace_dir, "index.html")

print("Inspecting images in index.html and assets directory...")
print("=" * 80)

with open(index_path, 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')
img_tags = soup.find_all('img')

print(f"Found {len(img_tags)} img tags in index.html:")
for idx, img in enumerate(img_tags):
    src = img.get('src', '')
    alt = img.get('alt', '')
    
    # Resolve local path
    local_path = None
    if src.startswith('/'):
        local_path = os.path.join(workspace_dir, src.lstrip('/'))
    elif src.startswith('assets/'):
        local_path = os.path.join(workspace_dir, src)
        
    size_str = "File not found locally"
    if local_path and os.path.exists(local_path):
        size_bytes = os.path.getsize(local_path)
        size_str = f"{size_bytes / (1024 * 1024):.2f} MB" if size_bytes > 1024*1024 else f"{size_bytes / 1024:.1f} KB"
        
    print(f"  {idx+1}. src: {src}")
    print(f"     alt: {alt}")
    print(f"     size: {size_str}")
    print("-" * 40)

print("\nScanning all files in assets/ directory:")
assets_dir = os.path.join(workspace_dir, "assets")
if os.path.exists(assets_dir):
    large_assets = []
    for root, dirs, files in os.walk(assets_dir):
        for f in files:
            p = os.path.join(root, f)
            sz = os.path.getsize(p)
            rel_p = os.path.relpath(p, workspace_dir)
            if sz > 500 * 1024: # larger than 500KB
                large_assets.append((rel_p, sz))
    
    print(f"Found {len(large_assets)} large files (>500KB) in assets/:")
    for rp, sz in sorted(large_assets, key=lambda x: x[1], reverse=True):
        print(f"  - {rp} ({sz / (1024*1024):.2f} MB)")
else:
    print("Assets directory not found.")
