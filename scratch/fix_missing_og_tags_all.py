import os
import re

TARGET_FILES = [
    'all-inclusive-yacht-charter.html',
    'amalfi-coast-yacht-rental.html',
    'business-jet-charter-guide-tips-pricing.html',
    'business-jet-charter.html',
    'corporate-jet-charter.html',
    'last-minute-yacht-charter.html',
    'luxury-private-jet-charter.html',
    'luxury-yacht-charter-caribbean.html',
    'luxury-yacht-charter-for-family-vacation.html',
    'luxury-yacht-rental-for-parties.html',
    'private-jet-available-now.html',
    'private-yacht-vacation-package.html',
    'yacht-charter-available-now.html',
    'yacht-charter-for-private-events.html',
    'yacht-charter-for-wedding.html',
    'yacht-charter-with-crew.html'
]

BASE_URL = "https://eliteluxurybookings.com"

def fix_og_tags():
    print("Fixing missing OG tags for target files...")
    fixed_count = 0
    
    for filename in TARGET_FILES:
        if not os.path.exists(filename):
            print(f"  [SKIP] File not found: {filename}")
            continue
            
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if 'property="og:title"' in content or "property='og:title'" in content:
            print(f"  [SKIP] og:title already present in: {filename}")
            continue
            
        # Extract title
        title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
        if not title_match:
            print(f"  [ERROR] No title tag found in: {filename}")
            continue
        title = title_match.group(1).strip().replace('\n', ' ').replace('  ', ' ')
        
        # Extract description
        desc_match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']+)["\']', content, re.IGNORECASE)
        if not desc_match:
            desc_match = re.search(r'<meta\s+content=["\']([^"\']+)["\']\s+name=["\']description["\']', content, re.IGNORECASE)
            
        if desc_match:
            description = desc_match.group(1).strip()
        else:
            description = "Book a luxury private yacht charter. Customized itineraries, child-friendly layouts, full crew, and quotes."
            print(f"  [WARN] No description meta tag found in: {filename}, using default")
            
        # Build url
        slug = filename.replace('.html', '')
        url = f"{BASE_URL}/{slug}/"
        
        # Build the tags block
        og_block = f"""    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{url}">"""

        # We will insert og_block before the og:image tag if present, or before </head>
        og_image_match = re.search(r'(<meta\s+property=["\']og:image["\'].*?>)', content, re.IGNORECASE)
        
        if og_image_match:
            # Insert before the og:image tag
            matched_tag = og_image_match.group(1)
            content = content.replace(matched_tag, og_block + "\n" + matched_tag, 1)
        else:
            # Insert before </head>
            content = content.replace('</head>', og_block + '\n</head>', 1)
            
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"  [FIXED] Added OG tags to: {filename}")
        fixed_count += 1
        
    print(f"Done! Fixed {fixed_count} files.")

if __name__ == "__main__":
    fix_og_tags()
