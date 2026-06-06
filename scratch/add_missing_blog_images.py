import json
import os
import re

workspace_dir = r"c:\Users\imran\OneDrive\Desktop\ELB code"
json_path = os.path.join(workspace_dir, "blog-data.json")

with open(json_path, 'r', encoding='utf-8') as f:
    blog_data = json.load(f)

# Define some fallback images by category if no image is found in the HTML
fallbacks = {
    'private jet': '/assets/elite_jet_master_hero.png',
    'private yacht': '/assets/luxury_superyacht_hero.png',
    'luxury villa': '/assets/villa_master.png'
}

updated_count = 0

for item in blog_data:
    url = item.get('url', '')
    category = item.get('category', '')
    
    # If image is missing or empty
    if 'image' not in item or not item['image']:
        filename = url.strip('/')
        filepath = os.path.join(workspace_dir, filename)
        
        found_img = None
        
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                html_content = f.read()
                
            # Let's search for a hero image or any main image first
            # Pattern 1: Any img tag containing "hero" in class or alt or src
            hero_img_match = re.search(r'<img[^>]+src=["\']([^"\']+)["\'][^>]*hero[^>]*>', html_content, re.IGNORECASE)
            if not hero_img_match:
                hero_img_match = re.search(r'<img[^>]*hero[^>]*src=["\']([^"\']+)["\']', html_content, re.IGNORECASE)
            
            # Pattern 2: Any background-image url referencing a hero
            if not hero_img_match:
                hero_bg_match = re.search(r'background:[^;]+url\(["\']?([^"\'\)]+hero[^"\'\)]+)["\']?\)', html_content, re.IGNORECASE)
                if hero_bg_match:
                    found_img = hero_bg_match.group(1).strip()
            
            if hero_img_match:
                found_img = hero_img_match.group(1).strip()
                
            # Pattern 3: If no hero image is found, search for the very first img tag in the body or header
            if not found_img:
                first_img_match = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', html_content, re.IGNORECASE)
                if first_img_match:
                    found_img = first_img_match.group(1).strip()
                    
            # Pattern 4: If no img tag at all, search for the first background url
            if not found_img:
                first_bg_match = re.search(r'url\(["\']?([^"\'\)]+)["\']?\)', html_content, re.IGNORECASE)
                if first_bg_match:
                    found_img = first_bg_match.group(1).strip()
                    
        # If we found an image reference, verify it starts with a slash
        if found_img:
            # Ignore telemetry and clarity pixels
            if 'clarity.ms' in found_img or 'yandex.ru' in found_img or found_img.startswith('http'):
                found_img = None
            else:
                if not found_img.startswith('/'):
                    found_img = '/' + found_img
                    
        # If still no image found or it's invalid, use the fallback for that category
        if not found_img and category in fallbacks:
            found_img = fallbacks[category]
            
        if found_img:
            item['image'] = found_img
            print(f"Assigned image to {url}: {found_img}")
            updated_count += 1

# Save the updated blog-data.json
if updated_count > 0:
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(blog_data, f, indent=4, ensure_ascii=False)
    print(f"\nSuccessfully populated {updated_count} missing images in blog-data.json.")
else:
    print("\nNo entries needed updating.")
