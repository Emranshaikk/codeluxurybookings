import os
import re
import urllib.parse

directory = r"c:\Users\imran\OneDrive\Desktop\ELB code"
broken_links = []

html_files = [f for f in os.listdir(directory) if f.endswith('.html')]
valid_files = set(html_files)
# Also add index.html for root requests
valid_files.add('')

for file in html_files:
    file_path = os.path.join(directory, file)
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    hrefs = re.findall(r'href="(.*?)"', content)
    for href in hrefs:
        if href.startswith(('mailto:', 'tel:', '#')):
            continue
        if href.startswith('http') and 'eliteluxurybookings.com' not in href:
            continue
            
        if re.search(r'\.(css|js|png|jpg|jpeg|svg|webp|ico|xml|json)(\?.*)?$', href, re.IGNORECASE):
            continue
            
        parsed = urllib.parse.urlparse(href)
        path = parsed.path
        
        if 'eliteluxurybookings.com' in parsed.netloc or path.startswith('https://eliteluxurybookings.com'):
            path = path.replace('https://eliteluxurybookings.com', '')
            path = path.replace('http://eliteluxurybookings.com', '')
            
        path = path.split('?')[0].split('#')[0].strip('/')
        
        if not path: # Root
            continue
            
        filename = path.split('/')[-1]
        
        if filename.endswith('.html'):
            expected_file = filename
        else:
            expected_file = f"{filename}.html"
            
        if expected_file not in valid_files:
            broken_links.append({
                'source_file': file,
                'broken_href': href,
                'expected_file': expected_file
            })

unique_broken = {}
for item in broken_links:
    key = (item['source_file'], item['broken_href'])
    unique_broken[key] = item

print(f"Found {len(unique_broken)} unique broken links.")
for key, item in unique_broken.items():
    print(f"{item['source_file']} contains broken link: {item['broken_href']}")
