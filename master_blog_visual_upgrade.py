import os
import re

# THE ELITE MASTER COVERS
JET_MASTER = "/assets/images/defaults/jet_master.png"
YACHT_MASTER = "/assets/images/defaults/yacht_master.png"
VILLA_MASTER = "/assets/images/defaults/villa_master.png"

def upgrade_blog_visuals():
    count = 0
    path = "blog/index.html"
    
    if not os.path.exists(path):
        print(f"Error: {path} not found.")
        return

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    
    # 1. Update the Card Images based on data-category
    # Regex to find each blog-card link and its internal img
    def replace_card_img(match):
        full_card = match.group(0)
        category = match.group(1).lower()
        
        target_img = JET_MASTER
        if 'yacht' in category: target_img = YACHT_MASTER
        elif 'villa' in category: target_img = VILLA_MASTER
        
        # Replace the src and onerror with the Master Cover
        # We also want to KEEP specific unique images if they aren't the generic purple pexels one
        # The generic one often ends in 7233354.jpeg
        
        is_generic = '7233354.jpeg' in full_card or 'purple' in full_card
        
        if is_generic:
            # Replace the img tag src
            updated_card = re.sub(r'src="[^"]+"', f'src="{target_img}"', full_card)
            # Remove onerror to keep it clean
            updated_card = re.sub(r'onerror="[^"]+"', '', updated_card)
            return updated_card
        return full_card

    # Match the entire <a> tag for blog-card
    content = re.sub(r'(<a href="[^"]+" class="blog-card[^"]*" data-category="([^"]+)".*?</a>)', replace_card_img, content, flags=re.DOTALL)

    if content != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Successfully upgraded Blog Index with Elite Master Covers.")
    else:
        print("No changes needed or matching patterns found.")

if __name__ == "__main__":
    upgrade_blog_visuals()
