
import os
import re

def fix_all_links():
    # 1. Get live dirs
    live_dirs = set(d.lower() for d in os.listdir('.') if os.path.isdir(d))
    live_dirs.add('elite-private-jet-charter')
    live_dirs.add('luxury-yacht-rentals')
    live_dirs.add('luxury-villa-rentals')
    live_dirs.add('blog')
    live_dirs.add('contact')
    live_dirs.add('index.html')
    live_dirs.add('sitemap.xml')
    live_dirs.add('robots.txt')

    # 2. Iterate through all html files
    for root, dirs, files in os.walk('.'):
        if '.git' in root or 'assets' in root:
            continue
            
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                except: continue

                def fix_link(match):
                    href = match.group(1)
                    if not href or 'http' in href or 'mailto' in href or 'tel' in href or href.startswith('#'):
                        return match.group(0)
                        
                    parts = [p for p in href.split('/') if p]
                    if not parts: return match.group(0)
                    
                    target = parts[0].lower()
                    if target not in live_dirs:
                        # If a route, redirect to jet hub
                        if 'jet-cost' in target:
                            return match.group(0).replace(match.group(1), '/elite-private-jet-charter/')
                        # If a yacht, redirect to yacht hub
                        if 'yacht' in target:
                            return match.group(0).replace(match.group(1), '/luxury-yacht-rentals/')
                        # Otherwise leave it or redirect to home
                        return match.group(0).replace(match.group(1), '/')
                    return match.group(0)

                new_content = re.sub(r'href=["\'](.*?)["\']', fix_link, content)
                
                if new_content != content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)

if __name__ == "__main__":
    fix_all_links()
