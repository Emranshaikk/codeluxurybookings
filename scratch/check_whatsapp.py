import os
import re

files_to_check = [
    "7-best-private-jet-charter-in-dubai.html",
    "boat-trip-from-mallorca-to-formentera.html",
    "private-boat-trip-mallorca-to-formentera.html",
    "private-jet-travel-with-pet.html"
]

root_dir = r'c:\Users\imran\OneDrive\Desktop\ELB code'

for filename in files_to_check:
    filepath = os.path.join(root_dir, filename)
    if not os.path.exists(filepath):
        print(f"Error: {filename} does not exist!")
        continue
        
    print(f"\n======================================")
    print(f"  AUDITING: {filename}")
    print(f"======================================")
    
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        
    # 1. Check for WhatsApp button
    wa_match = re.search(r'href=["\'](https://wa\.me/[^"\']+)["\']', content)
    if wa_match:
        print(f"[OK] WhatsApp link found: {wa_match.group(1)}")
    else:
        print(f"[FAIL] WhatsApp link missing or broken!")
        
    # Check for whatsapp class
    if 'wa-float' in content:
        print(f"[OK] 'wa-float' CSS class found in HTML.")
    elif 'whatsapp-float' in content:
        print(f"[INFO] 'whatsapp-float' class found instead of 'wa-float'.")
    else:
        print(f"[FAIL] 'wa-float' class missing.")
        
    # 2. Check for FontAwesome stylesheet link
    if 'font-awesome' in content or 'all.min.css' in content:
        print(f"[OK] FontAwesome CSS is loaded.")
    else:
        print(f"[FAIL] FontAwesome CSS missing! (Floating WA button icon might be broken)")
        
    # 3. Check for broken relative links (e.g. href="style.css" or assets paths)
    asset_paths = re.findall(r'src=["\']([^"\']+)["\']', content)
    broken_assets = [path for path in asset_paths if not path.startswith('/') and not path.startswith('http') and not path.startswith('data:')]
    if broken_assets:
        print(f"[FAIL] Broken relative asset paths found (needs leading slash for rewritten directories):")
        for p in broken_assets:
            print(f"    - src=\"{p}\"")
    else:
        print(f"[OK] All image assets use absolute root paths.")
        
    # 4. Check for broken href link paths (e.g. standard internal links missing leading slash)
    hrefs = re.findall(r'href=["\']([^"\']+)["\']', content)
    broken_hrefs = []
    for href in hrefs:
        # Ignore external links, mailto, tel, whatsapp, hash anchors
        if href.startswith('http') or href.startswith('mailto:') or href.startswith('tel:') or href.startswith('#') or href.startswith('javascript:'):
            continue
        if not href.startswith('/'):
            broken_hrefs.append(href)
    if broken_hrefs:
        print(f"[FAIL] Relative links without leading slash found (broken on rewritten slash URLs):")
        for h in broken_hrefs:
            print(f"    - href=\"{h}\"")
    else:
        print(f"[OK] All internal navigation links use absolute root paths.")
        
    # 5. Check if double navigation bar exists (some manual mergers duplicate the navbar!)
    nav_count = len(re.findall(r'class="global-nav"', content))
    nav_start_count = content.count('ELB_NAV_START')
    print(f"Navbar count: {nav_count}, NAV_START tags: {nav_start_count}")
    if nav_count > 1 or nav_start_count > 1:
        print(f"[X] Duplicate Navigation blocks detected!")
        
    # 6. Check for standard Master Footer duplicates
    footer_count = len(re.findall(r'class="footer"', content))
    print(f"Footer tag count: {footer_count}")
    if footer_count > 1:
        print(f"[X] Duplicate Footer blocks detected!")
