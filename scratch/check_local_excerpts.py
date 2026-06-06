import json

blog_data_path = r"c:\Users\imran\OneDrive\Desktop\ELB code\blog-data.json"

with open(blog_data_path, "r", encoding="utf-8") as f:
    data = json.load(f)

print("Excerpts under 80 characters in local blog-data.json:")
found = False
for idx, entry in enumerate(data):
    url = entry.get("url", "")
    excerpt = entry.get("excerpt", "")
    title = entry.get("title", "")
    if len(excerpt) < 80:
        found = True
        print(f"Index {idx}: url={url} | title={title} | excerpt='{excerpt}' (length: {len(excerpt)})")

if not found:
    print("None found!")
