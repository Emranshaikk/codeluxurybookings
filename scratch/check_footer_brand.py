import os
import re

def find_footer_brand_styles(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        
    pattern = re.compile(r'(\.footer-brand[^}]+})', re.DOTALL | re.IGNORECASE)
    matches = pattern.findall(content)
    return matches

def main():
    html_files = []
    for root, dirs, files in os.walk('.'):
        if '.git' in root or '_archive' in root or 'scratch' in root or 'fragments' in root:
            continue
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
                
    for filepath in html_files:
        matches = find_footer_brand_styles(filepath)
        if matches:
            # Check if any matches have something different or if we can see them
            print(f"--- {filepath} ---")
            for m in matches:
                print(m.strip())
            print()

if __name__ == '__main__':
    main()
