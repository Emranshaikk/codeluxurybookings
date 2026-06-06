import json
import os

workspace_dir = r"c:\Users\imran\OneDrive\Desktop\ELB code"
json_path = os.path.join(workspace_dir, "blog-data.json")

with open(json_path, 'r', encoding='utf-8') as f:
    blog_data = json.load(f)

print(f"Total entries in blog-data.json: {len(blog_data)}")

yacht_entries = [item for item in blog_data if item.get('category') == 'private yacht']
print(f"Total 'private yacht' entries: {len(yacht_entries)}")

required_keys = ['url', 'category', 'label', 'title', 'excerpt', 'link_text']

for item in yacht_entries:
    url = item.get('url')
    print(f"\nUrl: {url}")
    for key in required_keys:
        val = item.get(key)
        print(f"  {key:10s}: {'[OK]' if val else '[MISSING]'}")
    has_image = 'image' in item
    print(f"  image     : {'[OK] ' + item['image'] if has_image else '[MISSING]'}")
