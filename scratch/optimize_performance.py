import os
import re

def optimize_performance():
    root_dir = r'c:\Users\imran\OneDrive\Desktop\ELB code'
    files = [f for f in os.listdir(root_dir) if f.endswith('.html')]
    
    for filename in files:
        filepath = os.path.join(root_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        modified = False
        
        # 1. LAZY LOADING & DECODING
        # Add loading="lazy" and decoding="async" to images, but EXCLUDE hero images
        # We'll identify hero images later, for now let's tag all <img>
        img_pattern = re.compile(r'<img\s+([^>]*src="([^"]+)"[^>]*)>')
        
        def img_replacer(match):
            attrs = match.group(1)
            src = match.group(2)
            
            # If already has loading or it's a hero image (rough guess: first img in body)
            if 'loading=' in attrs:
                return match.group(0)
            
            # If it's a small icon or logo, maybe don't lazy load? 
            # For simplicity, lazy load everything that's not clearly a hero.
            new_attrs = attrs
            if 'hero' not in attrs.lower() and 'logo' not in attrs.lower():
                new_attrs += ' loading="lazy" decoding="async"'
            return f'<img {new_attrs}>'

        # content = img_pattern.sub(img_replacer, content) # Temporarily disabled to avoid breaking hero
        
        # 2. HERO PRELOADING
        # Find the first image or background image in the hero section
        hero_img_match = re.search(r'class="[^"]*hero[^"]*"[^>]*background:.*?url\(\'?(.*?)\'?\)', content, re.DOTALL)
        if not hero_img_match:
             hero_img_match = re.search(r'class="[^"]*hero[^"]*".*?<img.*?src="([^"]+)"', content, re.DOTALL)
             
        if hero_img_match:
            hero_url = hero_img_match.group(1)
            if not re.search(r'<link rel="preload" as="image" href="' + re.escape(hero_url) + r'"', content):
                preload_tag = f'\n    <link rel="preload" as="image" href="{hero_url}" fetchpriority="high">'
                if '</head>' in content:
                    content = content.replace('</head>', preload_tag + '\n</head>')
                    modified = True
                    print(f"Preloaded hero image {hero_url} in {filename}")

        # 3. FONT LOADING (display=swap)
        if 'fonts.googleapis.com' in content and 'display=swap' not in content:
            content = content.replace('family=', 'display=swap&family=')
            modified = True
            print(f"Added display=swap to fonts in {filename}")

        # 4. DEFER SCRIPTS
        # Find scripts with src and add defer
        script_pattern = re.compile(r'<script\s+([^>]*src="[^"]+"[^>]*)>')
        def script_replacer(match):
            attrs = match.group(1)
            if 'defer' not in attrs and 'async' not in attrs:
                return f'<script {attrs} defer>'
            return match.group(0)
            
        new_content = script_pattern.sub(script_replacer, content)
        if new_content != content:
            content = new_content
            modified = True
            print(f"Deferred scripts in {filename}")

        if modified:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

if __name__ == "__main__":
    optimize_performance()
