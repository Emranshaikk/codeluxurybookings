import os
import re

# 1. Get live dirs
live_dirs = set(d.lower() for d in os.listdir('.') if os.path.isdir(d))
live_dirs.add('elite-private-jet-charter')

# 2. Read silo
with open('global-route-silo/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 3. Find all internal links in the list
def fix_link(match):
    href = match.group(1)
    # Extract folder name
    parts = [p for p in href.split('/') if p]
    if not parts: return match.group(0)
    
    target = parts[0].lower()
    if target not in live_dirs and 'http' not in href:
        # Redirect ghost link to hub
        return match.group(0).replace(match.group(1), '/elite-private-jet-charter/')
    return match.group(0)

# Replace hrefs inside the list items
new_content = re.sub(r'href=["\'](.*?)["\']', fix_link, content)

with open('global-route-silo/index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)
