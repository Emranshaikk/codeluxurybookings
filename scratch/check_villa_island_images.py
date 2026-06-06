import os
import re

files_to_check = [
    # Island files
    "all-inclusive-private-island-rental.html",
    "bahamas-private-island-rental.html",
    "caribbean-private-island-rental.html",
    "exclusive-private-island-rental.html",
    "luxury-private-island-rental.html",
    "maldives-private-island-rental.html",
    "private-island-for-rent.html",
    "private-island-honeymoon-rental.html",
    # Villa files
    "how-to-book-luxury-villa-guide.html",
    "luxury-villa-rentals.html",
    "ultimate-luxury-villa-rental-guide-2026.html",
    "villa-vs-luxury-hotel-comparison.html"
]

workspace_dir = r"c:\Users\imran\OneDrive\Desktop\ELB code"
assets_dir = os.path.join(workspace_dir, "assets")

results = {}

for filename in files_to_check:
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
        
    missing = []
    unslashed = []
    
    for p in set(all_paths):
        # Check for unslashed relative references
        # e.g., src="assets/..." instead of src="/assets/..."
        if p.startswith("assets/"):
            unslashed.append(p)
            
        # normalize and check existence
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
                
    if missing or unslashed:
        results[filename] = {
            "missing": missing,
            "unslashed": unslashed
        }

print("\n--- RESULTS OF DETAILED AUDIT ---")
if not results:
    print("All island and villa pages are 100% correct! No missing images and no unslashed assets/ paths.")
else:
    for file, data in results.items():
        print(f"\n{file}:")
        if data["unslashed"]:
            print("  Unslashed Relative Paths:")
            for path in data["unslashed"]:
                print(f"    - {path}")
        if data["missing"]:
            print("  Missing/Broken Image Files:")
            for path, full_path in data["missing"]:
                print(f"    - Reference: {path} (Expected at: {full_path})")
