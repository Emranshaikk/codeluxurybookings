import os
import re

def fix_route_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # We search for the first <div class="top-intel-bar"> and everything up to the second <div class="top-intel-bar">
    # Note: re.DOTALL is important to match newlines.
    # We want to replace it with just a single <div class="top-intel-bar">.
    pattern = r'<body>\s*<div class="top-intel-bar">.*?<div class="top-intel-bar">'
    
    match = re.search(pattern, content, re.DOTALL)
    if match:
        new_content = re.sub(pattern, '<body>\n\n    <div class="top-intel-bar">', content, flags=re.DOTALL)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Successfully fixed duplicate top-intel-bar in: {filepath}")
        return True
    else:
        print(f"Pattern not found (already fixed or different structure) in: {filepath}")
        return False

def main():
    route_files = [
        'dubai-private-jet-routes.html',
        'paris-private-jet-routes.html',
        'losangeles-private-jet-routes.html',
        'newyork-private-jet-routes.html'
    ]
    
    fixed_count = 0
    for filename in route_files:
        if os.path.exists(filename):
            if fix_route_file(filename):
                fixed_count += 1
        else:
            print(f"File not found: {filename}")
            
    print(f"\nDeduplicated top bars in {fixed_count} files.")

if __name__ == '__main__':
    main()
