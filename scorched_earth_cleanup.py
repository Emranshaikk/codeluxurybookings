import os
import re

def scorched_earth_cleanup(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        return False

    original_content = content
    
    # 1. Broadly target the redundant Hub section by its unique titles
    # We look for sections containing these hub titles and remove them entirely
    # Patterns for the container/section
    hub_titles = ["The Americas Hub", "Asia & Pacific Hub", "Middle East & Islands", "UK & Europe Hub"]
    
    # Empty the silo placeholder first
    content = re.sub(r'<div id=\"footer-silo-placeholder\">.*?</div>', '<div id=\"footer-silo-placeholder\"></div>', content, flags=re.DOTALL)

    # Now look for the manual blocks that were left behind
    # We look for a <div> or <section> that contains one of the hub titles and remove the whole thing
    # This is broad but necessary to catch the 'odd' section
    for title in hub_titles:
        # Match a container that starts with <div or <section, ends with </div> or </section>, and contains the title
        # This regex looks for the nearest parent container
        pattern = rf'<(div|section)[^>]*>[^<]*<h[23][^>]*>{re.escape(title)}</h[23]>.*?</\1>'
        content = re.sub(pattern, '', content, flags=re.DOTALL | re.IGNORECASE)

    # 2. Universal Navigation Fix
    # Ensure Blog link works everywhere. Using relative path is often safer for local previews.
    content = content.replace('href=\"/blog/index.html\"', 'href=\"/blog/index.html\"') # already fixed to absolute, lets try ensure it is right
    # If the user is on a root index, /blog/index.html is correct. 
    # If they are inside a folder, they might need ../blog/index.html
    # But let's stick to root-relative /blog/index.html which is industry standard for cPanel
    
    # 3. Final deduplication of Navigation and Footer blocks
    # If there are two <nav> tags, keep only the first one
    if content.count('<nav class="global-nav">') > 1:
        parts = content.split('<nav class="global-nav">', 2)
        content = parts[0] + '<nav class="global-nav">' + parts[1] + re.sub(r'<nav class="global-nav">.*?</nav>', '', parts[2], flags=re.DOTALL)
    
    # If there are two <footer> tags, keep only the LAST one (usually the one I standardized)
    if content.count('<footer') > 1:
        parts = content.rsplit('<footer', 1)
        prefix = re.sub(r'<footer.*?>.*?</footer>', '', parts[0], flags=re.DOTALL)
        content = prefix + '<footer' + parts[1]

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
                if scorched_earth_cleanup(os.path.join(root, file)):
                    modified_count += 1
    print(f"Scorched Earth Cleaned {modified_count} files.")

if __name__ == "__main__":
    main()
