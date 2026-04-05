import os
import re

base_dir = r"c:\Users\imran\OneDrive\Desktop\ELB code"
logo_path = "/assets/images/elb-logo.png"
favicon_path = "/assets/images/favicon.png"

# Navigation Replacement
nav_pattern = r'<a href="/" class="nav-brand">Elite Luxury <span class="nav-gold">Bookings</span></a>'
nav_replacement = f'<a href="/" class="nav-brand" style="display: flex; align-items: center;"><img src="{logo_path}" alt="Elite Luxury Bookings" style="height: 48px; width: auto; object-fit: contain; filter: drop-shadow(0 2px 5px rgba(212,175,55,0.2));"></a>'

# Footer Style 1 (Complex Footer)
footer1_pattern = r'<div style="font-family:\'Cormorant Garamond\',serif; font-size:2.2rem; color:#fff; margin-bottom:1rem; line-height:1.2;">Elite Luxury <span style="color:#D4AF37;">Bookings</span></div>'
footer1_replacement = f'<a href="/" style="display: block; margin-bottom: 1.5rem;"><img src="{logo_path}" alt="Elite Luxury Bookings" style="height: 60px; width: auto; object-fit: contain;"></a>'

# Footer Style 2 (Simple Footer)
footer2_pattern = r'<div class="serif" style="font-size: 2.2rem; margin-bottom: 2rem;">Elite Luxury Bookings</div>'
footer2_replacement = f'<a href="/" style="display: block; margin-bottom: 2rem;"><img src="{logo_path}" alt="Elite Luxury Bookings" style="height: 50px; width: auto; object-fit: contain; margin: 0 auto;"></a>'

# Favicon Injection
favicon_tag = f'    <!-- BRAND & FAVICON -->\n    <link rel="icon" type="image/png" href="{favicon_path}">'

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original = content

        # 1. Favicon
        if '<head>' in content and favicon_path not in content:
            # Inject after meta charset or first occurrence in head
            content = content.replace('<meta charset="UTF-8">', f'<meta charset="UTF-8">\n{favicon_tag}')

        # 2. Nav Logo
        content = content.replace(nav_pattern, nav_replacement)

        # 3. Footer Logos
        content = content.replace(footer1_pattern, footer1_replacement)
        content = content.replace(footer2_pattern, footer2_replacement)

        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
    except Exception as e:
        print(f"Error in {filepath}: {e}")
    return False

def main():
    updated = 0
    total = 0
    for root, dirs, files in os.walk(base_dir):
        if '.git' in root: continue
        for file in files:
            if file.endswith('.html'):
                total += 1
                if process_file(os.path.join(root, file)):
                    updated += 1
    
    print(f"Branding Applied: {updated} / {total} files updated.")

if __name__ == "__main__":
    main()
