import os
import re

def add_seo_tags():
    html_files = [f for f in os.listdir('.') if f.endswith('.html')]
    print(f"Processing {len(html_files)} files...")
    
    for filename in html_files:
        if filename == 'index.html':
            continue # Already handled manually
            
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        changed = False
        
        # Determine keyword from filename
        # e.g. london-to-ibiza-private-jet-cost.html -> "london to ibiza private jet cost"
        base_name = filename.replace('.html', '')
        # Special cases like "404"
        if base_name == '404':
            continue
            
        keywords = " ".join(base_name.split('-'))
        
        # Tags to add
        tags_to_add = []
        
        if '<meta name="keywords"' not in content:
            tags_to_add.append(f'<meta name="keywords" content="{keywords}, elite luxury bookings, private jet charter">')
            
        if '<meta name="robots"' not in content:
            tags_to_add.append('<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">')
            
        if '<link rel="publisher"' not in content:
            tags_to_add.append('<link rel="publisher" href="https://eliteluxurybookings.com/">')
            
        if tags_to_add:
            tags_str = '\n    '.join(['<!-- SEO Enhancements -->'] + tags_to_add) + '\n'
            
            # Insert after canonical tag if exists, otherwise after viewport
            if '<link rel="canonical"' in content:
                content = re.sub(r'(<link rel="canonical"[^>]*>)', r'\1\n    ' + tags_str, content)
                changed = True
            elif '<meta name="viewport"' in content:
                content = re.sub(r'(<meta name="viewport"[^>]*>)', r'\1\n    ' + tags_str, content)
                changed = True
            elif '</head>' in content:
                content = content.replace('</head>', '\n    ' + tags_str + '</head>')
                changed = True
                
        if changed:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Added SEO tags to {filename}")

if __name__ == "__main__":
    add_seo_tags()
