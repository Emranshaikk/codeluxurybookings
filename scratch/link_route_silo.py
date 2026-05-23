import os
import re

TARGET_PATTERN = re.compile(
    r'(<li><a\s+href="https://eliteluxurybookings\.com/luxury-villa-rentals/"[^>]*>Luxury Villas</a></li>)',
    re.IGNORECASE
)

REPLACEMENT = (
    '<li><a href="https://eliteluxurybookings.com/luxury-villa-rentals/">Luxury Villas</a></li>\n'
    '                        <li><a href="https://eliteluxurybookings.com/global-route-silo/">Route Directory</a></li>'
)

def inject_silo_link(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        
    # Check if the global-route-silo directory link is already present
    if 'global-route-silo' in content:
        # Ignore files that already have it (like global-route-silo.html or files already updated)
        if 'global-route-silo/' in content and 'Route Silo Directory' in content:
            return False
            
    if TARGET_PATTERN.search(content):
        print(f"Injecting route silo link in: {file_path}")
        new_content = TARGET_PATTERN.sub(REPLACEMENT, content)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

def main():
    html_files = []
    for root, dirs, files in os.walk('.'):
        if '.git' in root or '_archive' in root or 'scratch' in root or 'fragments' in root:
            continue
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
                
    injected_count = 0
    for file_path in html_files:
        if inject_silo_link(file_path):
            injected_count += 1
            
    print(f"\nCompleted! Injected Route Silo link in {injected_count} footers.")

if __name__ == '__main__':
    main()
