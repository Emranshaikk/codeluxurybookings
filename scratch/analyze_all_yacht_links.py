import os
import re

yacht_pages = [
    'luxury-yacht-rentals.html', # Hub
    'yacht-charter-available-now.html',
    'all-inclusive-yacht-charter.html',
    'yacht-charter-with-crew.html',
    'last-minute-yacht-charter.html',
    'private-yacht-vacation-package.html',
    'yacht-charter-for-private-events.html',
    'yacht-charter-for-wedding.html',
    'luxury-yacht-charter-caribbean.html',
    'luxury-yacht-rental-for-parties.html',
    'luxury-yacht-charter-for-family-vacation.html',
    'vip-event-yacht-charters.html'
]

workspace_dir = r"c:\Users\imran\OneDrive\Desktop\ELB code"

print("Scanning links between pages...")
links_map = {}

for page in yacht_pages:
    filepath = os.path.join(workspace_dir, page)
    if not os.path.exists(filepath):
        print(f"Skipped (Not Found): {page}")
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Find all href links
    hrefs = re.findall(r'href=["\']([^"\']+)["\']', content)
    
    # We want to see which of our yacht_pages are targeted by this page
    targets = []
    for h in hrefs:
        # Normalize the link to see if it targets one of our pages
        # Links can be absolute (https://eliteluxurybookings.com/slug), relative clean (/slug), or relative file (slug.html)
        normalized = h.replace('https://eliteluxurybookings.com', '')
        normalized = normalized.strip('/')
        
        for yp in yacht_pages:
            yp_clean = yp.replace('.html', '')
            if normalized == yp_clean or normalized == yp or normalized + '.html' == yp:
                targets.append(yp)
                
    links_map[page] = sorted(list(set(targets)))

for src, dests in links_map.items():
    print(f"\n{src} links to:")
    for d in dests:
        print(f"  - {d}")
