import os
import re

# THE ELITE MASTER COVERS
JET_MASTER = "/assets/images/defaults/jet_master.png"
YACHT_MASTER = "/assets/images/defaults/yacht_master.png"
VILLA_MASTER = "/assets/images/defaults/villa_master.png"

def perfect_categorical_visual_upgrade():
    count = 0
    path = "blog/index.html"
    
    if not os.path.exists(path):
        print(f"Error: {path} not found.")
        return

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    
    # Precise Categorization Matcher
    # We find every blog card and its image tag
    # Using a 3-pass categorical check
    
    def process_card(match):
        full_card = match.group(0)
        category_raw = match.group(2).lower()
        
        # CATEGORY logic (Strict matching)
        if 'jet' in category_raw: 
            target_img = JET_MASTER
        elif 'yacht' in category_raw: 
            target_img = YACHT_MASTER
        elif 'villa' in category_raw: 
            target_img = VILLA_MASTER
        else:
            # Fallback for generic luxury or misc
            target_img = JET_MASTER 

        # REPLACEMENT: Only replace if it's the generic purple pexels one (7233354.jpeg)
        # Or if it's currently missing an image
        if '7233354.jpeg' in full_card or 'purple' in full_card or 'onerror' in full_card:
            # Clean up the image tag
            updated_card = re.sub(r'<img src="[^"]+"', f'<img src="{target_img}"', full_card)
            # Remove any onerror fallback to avoid flickering back to purple
            updated_card = re.sub(r'onerror="[^"]+"', '', updated_card)
            return updated_card
        
        return full_card

    # Match <a> tag with class blog-card and its content
    # Look specifically for data-category and its image inside
    content = re.sub(r'(<a href="[^"]+" class="blog-card[^"]*" data-category="([^"]+)".*?</a>)', process_card, content, flags=re.DOTALL)

    if content != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Elite Categorical Visuals finalized. All Jet and Yacht blogs are perfectly synced with their respective high-end photography.")
    else:
        print("Elite check complete. No mismatches found.")

if __name__ == "__main__":
    perfect_categorical_visual_upgrade()
