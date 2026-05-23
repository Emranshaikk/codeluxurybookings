import json
import os

json_path = r'c:\Users\imran\OneDrive\Desktop\ELB code\blog-data.json'
root_dir = r'c:\Users\imran\OneDrive\Desktop\ELB code'

with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

missing_files = []
for entry in data:
    url = entry['url']
    # Remove leading slash and handle .html
    file_name = url.lstrip('/')
    if not file_name.endswith('.html'):
        file_name += '.html'
    
    full_path = os.path.join(root_dir, file_name)
    if not os.path.exists(full_path):
        missing_files.append(url)

if missing_files:
    print(f"Warning: Found {len(missing_files)} missing files:")
    for f in missing_files:
        print(f" - {f}")
else:
    print("Success: All blog URLs have matching HTML files.")
