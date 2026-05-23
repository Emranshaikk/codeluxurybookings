import os
import re

def clean_nav_overrides(path):
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Skip known templates or snippets
    if any(k in path for k in ['old_blog.html', 'fragments']):
        return False

    modified = False

    # 1. Strip loose .global-nav { ... } blocks that do NOT use !important and set top: 0 or similar
    # We match .global-nav { ... } where the content inside the curly braces does not contain '!important'
    loose_nav_pattern = re.compile(r'\.global-nav\s*\{[^{!]*?\}', re.DOTALL)
    new_content = loose_nav_pattern.sub('', content)
    if new_content != content:
        content = new_content
        modified = True

    # 2. Strip loose .global-nav-inner { ... } blocks that do NOT use !important
    loose_inner_pattern = re.compile(r'\.global-nav-inner\s*\{[^{!]*?\}', re.DOTALL)
    new_content = loose_inner_pattern.sub('', content)
    if new_content != content:
        content = new_content
        modified = True

    # 3. Clean up excessive empty lines that might have been left
    content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content)

    if modified:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    directory = "."
    count = 0
    for root, dirs, files in os.walk(directory):
        if '.git' in root or '_archive' in root or 'scratch' in root or 'fragments' in root:
            continue
        for file in files:
            if file.endswith('.html'):
                path = os.path.join(root, file)
                try:
                    if clean_nav_overrides(path):
                        count += 1
                        print(f"Cleaned legacy nav styles in: {path}")
                except Exception as e:
                    print(f"Error on {path}: {e}")
    print(f"\nSuccessfully cleaned legacy nav overrides in {count} HTML files!")

if __name__ == '__main__':
    main()
