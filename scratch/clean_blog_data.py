import json
import os

def normalize_url(url):
    u = url.strip('/')
    if u.endswith('.html'):
        u = u[:-5]
    return u

with open('blog-data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

cleaned_data = []
seen_urls = {}

for entry in data:
    norm = normalize_url(entry['url'])
    # Update URL to clean format
    entry['url'] = f"/{norm}/"
    
    if norm in seen_urls:
        # Merge if the new one has better info (longer excerpt or title)
        existing = seen_urls[norm]
        if len(entry.get('excerpt', '')) > len(existing.get('excerpt', '')):
            existing['excerpt'] = entry['excerpt']
        if len(entry.get('title', '')) > len(existing.get('title', '')):
            existing['title'] = entry['title']
        if len(entry.get('label', '')) > len(existing.get('label', '')) and entry['label'] != 'Private Jet Route':
            existing['label'] = entry['label']
    else:
        seen_urls[norm] = entry
        cleaned_data.append(entry)

with open('blog-data.json', 'w', encoding='utf-8') as f:
    json.dump(cleaned_data, f, indent=4)

print(f"Cleaned blog-data.json. Reduced from {len(data)} to {len(cleaned_data)} entries.")
