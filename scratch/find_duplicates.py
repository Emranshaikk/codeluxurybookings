import json

with open('blog-data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

urls = {}
duplicates = []

for i, entry in enumerate(data):
    url = entry['url'].strip('/')
    if url.endswith('.html'):
        url = url[:-5]
    
    if url in urls:
        duplicates.append((urls[url], i, entry['url']))
    else:
        urls[url] = i

if duplicates:
    print(f"Found {len(duplicates)} duplicates:")
    for d in duplicates:
        print(f"Index {d[0]} and Index {d[1]} (URL: {d[2]})")
else:
    print("No duplicates found.")
