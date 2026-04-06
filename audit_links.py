import os
import re

root_dir = r"c:\Users\imran\OneDrive\Desktop\ELB code"
index_html = os.path.join(root_dir, "index.html")

with open(index_html, "r", encoding="utf-8") as f:
    content = f.read()

# Find all internal links ending in /
links = re.findall(r'href="/([^"]+)/"', content)

broken = []
for link in links:
    # Skip assets, wp-content, etc.
    if any(x in link for x in ["assets", "wp-content", "tel:", "wa.me", "mailto:"]):
        continue
    
    path = os.path.join(root_dir, link, "index.html")
    if not os.path.exists(path):
        broken.append(link)

if broken:
    print(f"Found {len(broken)} broken internal links: {broken}")
    # I'll try to auto-create them using the template approach from auto_create_routes
    template_dir = os.path.join(root_dir, "london-to-dubai-private-jet-cost")
    template_file = os.path.join(template_dir, "index.html")
    
    for b in broken:
        # Only handle private-jet-cost ones
        if "private-jet-cost" in b:
            match = re.search(r'([a-z]+)-to-([a-z]+)-private-jet-cost', b)
            if match:
                dep, arr = match.groups()
                target_dir = os.path.join(root_dir, b)
                os.makedirs(target_dir, exist_ok=True)
                target_file = os.path.join(target_dir, "index.html")
                
                with open(template_file, "r", encoding="utf-8") as f:
                    html = f.read()
                
                html = html.replace("London", dep.title())
                html = html.replace("london", dep.lower())
                html = html.replace("Dubai", arr.title())
                html = html.replace("dubai", arr.lower())
                
                with open(target_file, "w", encoding="utf-8") as f:
                    f.write(html)
                print(f"Created missing route: {b}")
else:
    print("No broken internal links found in index.html.")
