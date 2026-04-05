import os
import re

def purge_and_fix_nav(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        return False

    original_content = content
    
    # 1. Remove the Hub sections that look odd (The 4-hub grid)
    # We empty the placeholder and any redundant section matching the Hub pattern
    content = re.sub(r'<div id=\"footer-silo-placeholder\">.*?</div>', '<div id=\"footer-silo-placeholder\"></div>', content, flags=re.DOTALL)
    
    # Also look for the Global Aviation Network section if it is outside the placeholder
    content = re.sub(r'<section[^>]*>\s*<div[^>]*>\s*<h2[^>]*>Global <span[^>]*>Aviation Network</span></h2>.*?Resulting in removal of hub grid.*?/section>', '', content, flags=re.DOTALL)
    
    # Specifically target the section we saw in lines 1507-1573 of index.html
    hub_section_pattern = r'<section class=\"section-padding\" style=\"background: rgba\(212, 175, 55, 0.02\); border-top: 1px solid var\(--glass-border\);\">\s*<div class=\"container\">\s*<h2 class=\"serif\" style=\"font-size: 3rem; text-align: center; margin-bottom: 4rem;\">Global <span class=\"gold-text\">Aviation Network</span></h2>.*?/section>'
    content = re.sub(hub_section_pattern, '', content, flags=re.DOTALL)

    # 2. Fix the Blog link
    # Change /blog/ to /blog/index.html to ensure it works in all environments
    content = content.replace('href=\"/blog/\"', 'href=\"/blog/index.html\"')
    content = content.replace('href=\'/blog/\'', 'href=\'/blog/index.html\'')
    
    # 3. Clean up any duplicated styles that might have come from previous runs
    content = re.sub(r'<style>\s*/\* ELB_CSS_START \*/.*?/\* ELB_CSS_END \*/\s*</style>\s*<style>\s*/\* ELB_CSS_START \*/', '<style>\n/* ELB_CSS_START */', content, flags=re.DOTALL)

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    root_dir = r"c:\Users\imran\OneDrive\Desktop\ELB code"
    modified_count = 0
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.html'):
                if purge_and_fix_nav(os.path.join(root, file)):
                    modified_count += 1
    print(f"Purged and Fixed {modified_count} files.")

if __name__ == "__main__":
    main()
