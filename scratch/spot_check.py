import os
import re

files_to_check = [
    "hongkong-to-singapore-private-jet-cost.html",
    "abudhabi-to-doha-private-jet-cost.html",
    "amsterdam-to-london-private-jet-cost.html",
    "aspen-to-miami-private-jet-cost.html",
    "barcelona-to-london-private-jet-cost.html",
    "beijing-to-seoul-private-jet-cost.html",
    "chicago-to-newyork-private-jet-cost.html",
    "dubai-to-london-private-jet-cost.html",
    "geneva-to-london-private-jet-cost.html",
    "ibiza-to-london-private-jet-cost.html"
]

base_dir = r"c:\Users\imran\OneDrive\Desktop\ELB code"

results = {}

for filename in files_to_check:
    filepath = os.path.join(base_dir, filename)
    if not os.path.exists(filepath):
        print(f"File not found: {filename}")
        continue
    
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # 1. Product Schema Check
    has_product_schema = '"@type": "Product"' in content or "'@type': 'Product'" in content
    product_currency = None
    product_prices = None
    if has_product_schema:
        # Extract offers pricing
        match = re.search(r'"offers":\s*\{\s*"@type":\s*"AggregateOffer",\s*"lowPrice":\s*"([^"]+)",\s*"highPrice":\s*"([^"]+)",\s*"priceCurrency":\s*"([^"]+)"', content)
        if match:
            product_prices = (match.group(1), match.group(2))
            product_currency = match.group(3)
    
    # 2. Hardcoded Email Check
    has_hardcoded_email = "formsubmit.co/ajax/contactshaikk@gmail.com" in content
    
    # 3. Corrupted Nav Check
    has_corrupted_nav = "? Private Jets" in content or "?? Intelligence Alert" in content
    
    # 4. Breadcrumb Mismatch Check
    has_visible_guide = "/private-jet-booking-guide/" in content
    has_schema_charter = False
    breadcrumb_schema_matches = re.findall(r'"@type":\s*"ListItem",\s*"position":\s*2,\s*"name":\s*"Private Jet Charter",\s*"item":\s*"([^"]+)"', content)
    if breadcrumb_schema_matches:
        has_schema_charter = "elite-private-jet-charter" in breadcrumb_schema_matches[0]
    
    breadcrumb_mismatch = has_visible_guide and has_schema_charter
    
    # 5. LocalBusiness Image Check
    localbusiness_image = None
    image_match = re.search(r'"@type":\s*"LocalBusiness".*?"image":\s*"([^"]+)"', content, re.DOTALL)
    if image_match:
        localbusiness_image = os.path.basename(image_match.group(1))
    
    results[filename] = {
        "has_product_schema": has_product_schema,
        "product_prices": product_prices,
        "product_currency": product_currency,
        "has_hardcoded_email": has_hardcoded_email,
        "has_corrupted_nav": has_corrupted_nav,
        "breadcrumb_mismatch": breadcrumb_mismatch,
        "localbusiness_image": localbusiness_image
    }

# Print summary
print("--- SPOT CHECK RESULTS ---")
for fn, res in results.items():
    print(f"\nFile: {fn}")
    print(f"  1. Product Schema: {'Found (' + str(res['product_prices']) + ' ' + str(res['product_currency']) + ')' if res['has_product_schema'] else 'Not Found'}")
    print(f"  2. Hardcoded Email (client-side): {'YES' if res['has_hardcoded_email'] else 'NO'}")
    print(f"  3. Corrupted Nav: {'YES' if res['has_corrupted_nav'] else 'NO'}")
    print(f"  4. Breadcrumb Mismatch: {'YES (Visible links guide, Schema links charter)' if res['breadcrumb_mismatch'] else 'NO'}")
    print(f"  5. LocalBusiness Image: {res['localbusiness_image']}")
