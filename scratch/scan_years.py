import os
import re
from bs4 import BeautifulSoup
import sys

# Ensure stdout uses UTF-8
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

workspace_dir = r"c:\Users\imran\OneDrive\Desktop\ELB code"
html_files = [f for f in os.listdir(workspace_dir) if f.endswith('.html')]

print(f"Scanning {len(html_files)} HTML files for year references in metadata...")
print("=" * 80)

year_pattern = re.compile(r'\b(202\d)\b')

found_count = 0
for fn in sorted(html_files):
    path = os.path.join(workspace_dir, fn)
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()
        
    soup = BeautifulSoup(html, 'html.parser')
    
    # 1. Check title
    title = soup.title.string if soup.title else ""
    title_matches = year_pattern.findall(title)
    
    # 2. Check meta description
    meta_desc = ""
    meta_tag = soup.find('meta', attrs={'name': 'description'}) or soup.find('meta', attrs={'property': 'og:description'})
    if meta_tag:
        meta_desc = meta_tag.get('content', '')
    else:
        # fallback regex
        match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']+)["\']', html, re.I)
        if match:
            meta_desc = match.group(1)
            
    desc_matches = year_pattern.findall(meta_desc)
    
    if title_matches or desc_matches:
        found_count += 1
        print(f"File: {fn}")
        if title_matches:
            print(f"  Title matches {title_matches}: {title}")
        if desc_matches:
            print(f"  Desc matches {desc_matches}: {meta_desc}")
        print("-" * 80)

print(f"Scan complete. Found {found_count} files with year references in metadata.")
