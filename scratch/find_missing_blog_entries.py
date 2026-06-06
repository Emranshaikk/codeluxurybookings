import os
import json

EXCLUDE_FILES = {
    'index.html', '404.html', 'thank-you.html', 'test_bot.html', 'contact.html',
    'about.html', 'privacy.html', 'terms.html', 'partners.html', 'request-quote.html',
    'luxury-charter-inquiry.html', 'blog.html', 'old_blog.html', 'thank-you.html',
    '_template_master.html', '_template_blog_master.html'
}

workspace_dir = r"c:\Users\imran\OneDrive\Desktop\ELB code"
json_path = os.path.join(workspace_dir, "blog-data.json")

with open(json_path, 'r', encoding='utf-8') as f:
    blog_data = json.load(f)

registered_urls = {item['url'] for item in blog_data}

html_files = [f for f in os.listdir(workspace_dir) if f.endswith('.html') and f not in EXCLUDE_FILES]

missing_entries = []

for filename in sorted(html_files):
    url = f"/{filename}"
    # Check both clean URL and HTML URL
    url_clean = url.replace('.html', '')
    
    if url not in registered_urls and url_clean not in registered_urls:
        missing_entries.append(filename)

print(f"Total HTML files to verify: {len(html_files)}")
print(f"Total missing from blog-data.json: {len(missing_entries)}")
for m in missing_entries:
    print(f"  - {m}")
