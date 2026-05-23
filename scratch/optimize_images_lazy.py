import os
import re

def optimize_images_lazy():
    root_dir = r'c:\Users\imran\OneDrive\Desktop\ELB code'
    files = [f for f in os.listdir(root_dir) if f.endswith('.html')]
    
    for filename in files:
        filepath = os.path.join(root_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        modified = False
        
        # 1. IMAGE LAZY LOADING & ASYNC DECODING
        # Regex to find all <img> tags
        img_pattern = re.compile(r'<img\s+([^>]*src="([^"]+)"[^>]*)>')
        
        def img_replacer(match):
            attrs = match.group(1)
            src = match.group(2)
            
            # Skip if it's already got loading or is clearly a hero/logo
            if 'loading=' in attrs or 'fetchpriority=' in attrs:
                return match.group(0)
            
            # Rule: Don't lazy load the logo or hero images
            # Check for keywords in attributes or src
            is_hero = any(k in attrs.lower() or k in src.lower() for k in ['hero', 'logo', 'brand', 'nav'])
            
            new_attrs = attrs
            if not is_hero:
                if 'loading=' not in new_attrs:
                    new_attrs += ' loading="lazy"'
                if 'decoding=' not in new_attrs:
                    new_attrs += ' decoding="async"'
                return f'<img {new_attrs}>'
            else:
                # For hero images, ensure decoding="async" but NO loading="lazy"
                if 'decoding=' not in new_attrs:
                    new_attrs += ' decoding="async"'
                return f'<img {new_attrs}>'

        new_content = img_pattern.sub(img_replacer, content)
        if new_content != content:
            content = new_content
            modified = True
            print(f"Applied lazy loading/decoding to images in {filename}")

        if modified:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

if __name__ == "__main__":
    optimize_images_lazy()
