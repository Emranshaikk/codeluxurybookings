import os
import re

modified_files = [
    "about.html",
    "all-inclusive-private-island-rental.html",
    "bahamas-private-island-rental.html",
    "caribbean-private-island-rental.html",
    "exclusive-private-island-rental.html",
    "luxury-private-island-rental.html",
    "maldives-private-island-rental.html",
    "partners.html",
    "private-island-for-rent.html",
    "private-island-honeymoon-rental.html"
]

workspace_dir = r"c:\Users\imran\OneDrive\Desktop\ELB code"
assets_dir = os.path.join(workspace_dir, "assets")

missing_images_by_file = {}

for filename in modified_files:
    filepath = os.path.join(workspace_dir, filename)
    if not os.path.exists(filepath):
        print(f"File {filename} does not exist!")
        continue
        
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
        
    # Extract images
    img_srcs = re.findall(r'src=["\']([^"\']+)["\']', content)
    bg_urls = re.findall(r'url\(["\']?([^"\')]+)["\']?\)', content)
    og_images = re.findall(r'content=["\'](https://eliteluxurybookings.com/assets/[^"\']+)["\']', content)
    schema_images = re.findall(r'"image":\s*["\'](https://eliteluxurybookings.com/assets/[^"\']+)["\']', content)
    
    all_paths = []
    for src in img_srcs:
        if "mc.yandex.ru" not in src and "googletagmanager" not in src:
            all_paths.append(src)
    for url in bg_urls:
        all_paths.append(url)
    for img in og_images + schema_images:
        rel = img.replace("https://eliteluxurybookings.com/", "/")
        all_paths.append(rel)
        
    # Check existence
    missing = []
    for p in set(all_paths):
        # normalize and clean path
        clean_p = p.lstrip('/')
        if clean_p.startswith('assets/'):
            sub_p = clean_p[7:] # remove 'assets/'
            full_path = os.path.join(assets_dir, sub_p.replace('/', '\\'))
            if not os.path.exists(full_path):
                missing.append((p, full_path))
        elif p.startswith('http') or p.startswith('//'):
            pass
        else:
            # check root level files like favicon.png
            full_path = os.path.join(workspace_dir, clean_p.replace('/', '\\'))
            if not os.path.exists(full_path):
                missing.append((p, full_path))
                
    if missing:
        missing_images_by_file[filename] = missing

if missing_images_by_file:
    print("\nMissing or broken images found:")
    for file, missing in missing_images_by_file.items():
        print(f"\n{file}:")
        for p, full_path in missing:
            print(f"  - Path: {p} (Expected at: {full_path})")
else:
    print("\nAll image references in all modified HTML files exist locally!")
