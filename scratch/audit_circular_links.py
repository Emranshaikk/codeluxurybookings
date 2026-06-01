import os
import re

# Define the 6 key private island pages and their friendly names
pages = {
    "private-island-for-rent.html": "Flagship Hub",
    "luxury-private-island-rental.html": "Sub-Hub",
    "caribbean-private-island-rental.html": "Caribbean Regional",
    "bahamas-private-island-rental.html": "Bahamas Regional",
    "maldives-private-island-rental.html": "Maldives Regional",
    "exclusive-private-island-rental.html": "Exclusive Sub-Pillar"
}

workspace_dir = r"c:\Users\imran\OneDrive\Desktop\ELB code"

print("=" * 80)
print("SEO CIRCULAR CROSS-LINKING AUDIT FOR PRIVATE ISLAND PAGES")
print("=" * 80)

failures = 0

for current_file, current_name in pages.items():
    file_path = os.path.join(workspace_dir, current_file)
    if not os.path.exists(file_path):
        print(f"\n[ERROR] File not found: {current_file}")
        failures += 1
        continue
        
    print(f"\nScanning: {current_file} ({current_name})")
    
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Check for references to the other 5 pages
    for target_file, target_name in pages.items():
        if target_file == current_file:
            continue
            
        # Look for `<a href="target_file"` or `<a href="/target_file"` or similar variations
        # We also check for relative links since the files are in the same folder.
        pattern = rf'href=["\'](?:https?://eliteluxurybookings\.com/)?/?{re.escape(target_file)}["\']'
        match = re.search(pattern, content, re.IGNORECASE)
        
        if match:
            print(f"  [OK] Links to -> {target_file} ({target_name})")
        else:
            # Let's check if the slug is linked (without .html extension if URL rewritten, but in this static setup it's file name)
            slug = target_file.replace(".html", "")
            slug_pattern = rf'href=["\'](?:https?://eliteluxurybookings\.com/)?/?{re.escape(slug)}/?["\']'
            slug_match = re.search(slug_pattern, content, re.IGNORECASE)
            if slug_match:
                print(f"  [OK] Links to (slug) -> {slug} ({target_name})")
            else:
                print(f"  [MISSING] MISSING LINK to -> {target_file} ({target_name})")
                failures += 1

print("\n" + "=" * 80)
if failures == 0:
    print("SUCCESS: All 6 private island pages are 100% interconnected in a closed loop!")
else:
    print(f"AUDIT WARNING: Found {failures} missing/incomplete link connections.")
print("=" * 80)
