import os
import re

def fix_a11y_globally():
    root_dir = r'c:\Users\imran\OneDrive\Desktop\ELB code'
    html_files = [f for f in os.listdir(root_dir) if f.endswith('.html')]
    
    # Social labels mapping
    social_labels = {
        'facebook': 'Follow Elite Luxury Bookings on Facebook',
        'instagram': 'Follow Elite Luxury Bookings on Instagram',
        'linkedin': 'Follow Elite Luxury Bookings on LinkedIn',
        'x-twitter': 'Follow Elite Luxury Bookings on X (Twitter)',
        'twitter': 'Follow Elite Luxury Bookings on Twitter'
    }

    for filename in html_files:
        filepath = os.path.join(root_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        modified = False
        
        # 1. Fix Social Links
        for key, label in social_labels.items():
            # Match links with the specific icon class and no aria-label
            pattern = rf'<a href="([^"]+)"(?![^>]*aria-label)><i class="fab fa-{key}"></i></a>'
            replacement = rf'<a href="\1" aria-label="{label}"><i class="fab fa-{key}"></i></a>'
            new_content = re.sub(pattern, replacement, content)
            if new_content != content:
                content = new_content
                modified = True
                
        # 2. Fix WhatsApp Float
        wa_pattern = r'<a href="https://wa\.me/([^"]+)" class="wa-float" target="_blank"(?![^>]*aria-label)>'
        wa_replacement = r'<a href="https://wa.me/\1" class="wa-float" target="_blank" aria-label="Connect with our Elite Concierge on WhatsApp">'
        new_content = re.sub(wa_pattern, wa_replacement, content)
        if new_content != content:
            content = new_content
            modified = True

        if modified:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed A11y in {filename}")

if __name__ == "__main__":
    fix_a11y_globally()
