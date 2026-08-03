import os
import re
import sys
from bs4 import BeautifulSoup

# Ensure stdout uses UTF-8
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

workspace_dir = r"c:\Users\imran\OneDrive\Desktop\ELB code"
html_files = [f for f in os.listdir(workspace_dir) if f.endswith('.html')]

print(f"Injecting WhatsApp click tracking across {len(html_files)} HTML files...")
print("=" * 80)

whatsapp_event_code = "if(typeof gtag==='function'){gtag('event','whatsapp_click',{'page_location':window.location.href});}"

modified_count = 0
total_links_tracked = 0

for fn in sorted(html_files):
    path = os.path.join(workspace_dir, fn)
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()
        
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find_all('a')
    
    file_modified = False
    for link in links:
        href = link.get('href', '')
        if 'wa.me' in href or 'api.whatsapp.com' in href:
            existing_onclick = link.get('onclick', '')
            
            # Check if already tracked
            if 'whatsapp_click' in existing_onclick:
                total_links_tracked += 1
                continue
                
            # Prepend or set the new onclick
            if existing_onclick:
                # Add semicolon if needed
                if not existing_onclick.strip().endswith(';'):
                    existing_onclick += ';'
                new_onclick = f"{whatsapp_event_code} {existing_onclick}"
            else:
                new_onclick = whatsapp_event_code
                
            link['onclick'] = new_onclick
            file_modified = True
            total_links_tracked += 1
            
    if file_modified:
        # Write back HTML
        # We want to preserve formatting, but BeautifulSoup might restructure a bit.
        # However, for pure HTML sites, bs4 output is perfectly fine.
        # Wait! Let's check if we can do this using bs4 or if we need a regex.
        # Using bs4 is generally safer for complex HTML trees.
        # Let's save the modified HTML
        with open(path, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        modified_count += 1
        print(f"Updated {fn}")

print("-" * 80)
print(f"WhatsApp tracking injection complete. Modified {modified_count} files, tracked {total_links_tracked} total links.")
