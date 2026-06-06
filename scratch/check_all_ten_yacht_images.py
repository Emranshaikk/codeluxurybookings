import os
import re

files_to_check = [
    'yacht-charter-available-now.html',
    'all-inclusive-yacht-charter.html',
    'yacht-charter-with-crew.html',
    'last-minute-yacht-charter.html',
    'private-yacht-vacation-package.html',
    'yacht-charter-for-private-events.html',
    'yacht-charter-for-wedding.html',
    'luxury-yacht-charter-caribbean.html',
    'luxury-yacht-rental-for-parties.html',
    'luxury-yacht-charter-for-family-vacation.html'
]

workspace_dir = r"c:\Users\imran\OneDrive\Desktop\ELB code"

missing_count = 0
found_count = 0

print("Scanning all 10 yacht pages for image references...")

for filename in files_to_check:
    filepath = os.path.join(workspace_dir, filename)
    if not os.path.exists(filepath):
        print(f"\n[ERROR] File not found: {filename}")
        continue
        
    print(f"\nScanning: {filename}")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Find img tags and background style urls
    imgs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', content)
    bg_urls = re.findall(r'url\(["\']?([^"\'\)]+)["\']?\)', content)
    
    all_refs = sorted(list(set(imgs + bg_urls)))
    
    for ref in all_refs:
        if ref.startswith('http') or ref.startswith('data:') or ref.startswith('var') or ref.startswith('#') or not ref.strip():
            continue
            
        clean_ref = ref.lstrip('/')
        local_path = os.path.join(workspace_dir, clean_ref.replace('/', os.sep))
        
        if os.path.exists(local_path):
            found_count += 1
            print(f"  [OK] {ref}")
        else:
            missing_count += 1
            print(f"  [MISSING] {ref}")

print(f"\nAudit complete: {found_count} images found, {missing_count} images missing.")
