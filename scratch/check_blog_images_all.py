import json
import os

workspace_dir = r"c:\Users\imran\OneDrive\Desktop\ELB code"
json_path = os.path.join(workspace_dir, "blog-data.json")

with open(json_path, 'r', encoding='utf-8') as f:
    blog_data = json.load(f)

categories = set(item.get('category', 'none') for item in blog_data)
print(f"Categories found: {categories}")

for cat in sorted(categories):
    items = [item for item in blog_data if item.get('category') == cat]
    with_img = [item for item in items if 'image' in item and item['image']]
    print(f"\nCategory '{cat}':")
    print(f"  Total items: {len(items)}")
    print(f"  With image: {len(with_img)}")
    print(f"  Missing image: {len(items) - len(with_img)}")
    
    # Print some examples of missing images
    missing = [item for item in items if 'image' not in item or not item['image']]
    if missing:
        print("  Examples of missing images:")
        for m in missing[:5]:
            print(f"    - {m['url']} (Title: {m.get('title', 'none')})")
