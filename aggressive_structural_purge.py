import os
import re

def aggressive_purge(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        return False

    original_content = content
    
    # 1. Targeted Sections for Purge
    # We look for the "SEO SILO DIRECTORY" and "Global Aviation Network" blocks
    # and remove the entire <section> containing them.
    
    # Pattern for "SEO SILO DIRECTORY"
    silo_pattern = r'<!-- SEO SILO DIRECTORY -->\s*<section.*?>.*?</section>'
    content = re.sub(silo_pattern, '', content, flags=re.DOTALL | re.IGNORECASE)
    
    # Pattern for "Global Aviation Route Network"
    route_pattern = r'<section[^>]*>\s*<div[^>]*>\s*<h2[^>]*>Global Aviation <span[^>]*>Route Network</span></h2>.*?</section>'
    content = re.sub(route_pattern, '', content, flags=re.DOTALL | re.IGNORECASE)

    # Pattern for the "Global Aviation Network" remnants (the 4-hub grid)
    network_pattern = r'<section[^>]*>\s*<div[^>]*>\s*<h2[^>]*>Global <span[^>]*>Aviation Network</span></h2>.*?</section>'
    content = re.sub(network_pattern, '', content, flags=re.DOTALL | re.IGNORECASE)
    
    # Also catch any stray silo placeholders or hub containers
    content = re.sub(r'<div id=\"footer-silo-placeholder\">.*?</div>', '', content, flags=re.DOTALL)
    
    # Clean up excessive whitespace left by the removals
    content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)

    # 2. Navigation Link Consistency
    # Ensure Blog link works everywhere.
    content = content.replace('href=\"/blog/\"', 'href=\"/blog/index.html\"')
    content = content.replace('href=\'/blog/\'', 'href=\'/blog/index.html\'')

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
                if aggressive_purge(os.path.join(root, file)):
                    modified_count += 1
    print(f"Aggressively Purged {modified_count} files.")

if __name__ == "__main__":
    main()
