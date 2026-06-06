import json
import os

blog_data_path = r"c:\Users\imran\OneDrive\Desktop\ELB code\blog-data.json"
assets_dir = r"c:\Users\imran\OneDrive\Desktop\ELB code\assets"

with open(blog_data_path, "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"Total entries in blog-data: {len(data)}")

missing = []
for idx, entry in enumerate(data):
    url = entry.get("url", "")
    category = entry.get("category", "")
    image = entry.get("image", "")
    
    # Check if related to villa or island
    if "island" in url.lower() or "villa" in url.lower() or category == "luxury villa":
        if not image:
            print(f"Index {idx}: Entry {url} is missing the image field entirely!")
            continue
            
        clean_img = image.lstrip('/')
        if clean_img.startswith("assets/"):
            sub_img = clean_img[7:]
            full_path = os.path.join(assets_dir, sub_img.replace('/', '\\'))
            if not os.path.exists(full_path):
                missing.append((idx, url, image, full_path))
        else:
            # check root level or other paths
            full_path = os.path.join(os.path.dirname(blog_data_path), clean_img.replace('/', '\\'))
            if not os.path.exists(full_path):
                missing.append((idx, url, image, full_path))

print("\n--- BLOG DATA PRIVATE ISLAND / VILLA CARD IMAGE AUDIT ---")
if not missing:
    print("All blog entry card images for private islands and villas exist locally and are valid!")
else:
    print(f"Found {len(missing)} missing blog card images:")
    for idx, url, image, full_path in missing:
        print(f"  - Index {idx} ({url}): Image path '{image}' (Expected at: {full_path})")
