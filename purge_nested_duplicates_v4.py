import os
import re

def purge_duplicates_in_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return False

    original_content = content
    modified = False
    
    # 1. Purge Duplicated Navigation Blocks
    nav_pattern = re.compile(r'<!-- ELB_NAV_START -->.*?<!-- ELB_NAV_END -->', re.DOTALL)
    nav_matches = list(nav_pattern.finditer(content))
    if len(nav_matches) > 1:
        first_nav = nav_matches[0].group(0)
        content = nav_pattern.sub('', content)
        # Re-insert FIRST match after <body>
        content = content.replace('<body>', '<body>\n' + first_nav, 1)
        modified = True

    # 2. Purge Duplicated HUB Sections (Aggressive)
    # Target common patterns of the aviation hub section
    hub_patterns = [
        re.compile(r'<div id="footer-silo-placeholder">.*?Global <span class="gold-text">Aviation Network</span>.*?</div>\s*</div>', re.DOTALL),
        re.compile(r'<section class="section-padding"[^>]*>.*?Global <span class="gold-text">Aviation Network</span>.*?</section>', re.DOTALL)
    ]
    
    for hub_pattern in hub_patterns:
        hub_matches = list(hub_pattern.finditer(content))
        if len(hub_matches) > 1:
            first_hub = hub_matches[0].group(0)
            content = hub_pattern.sub('', content)
            # Re-insert exactly one BEFORE the <footer> tag
            if '<footer>' in content:
                content = content.replace('<footer>', first_hub + '\n<footer>', 1)
            else:
                content = content + '\n' + first_hub
            modified = True

    # 3. Purge Duplicated CSS / Style Blocks for ELB components
    elb_css_patterns = [
        re.compile(r'/\* ELB_CSS_START \*/.*?/\* ELB_CSS_END \*/', re.DOTALL),
        re.compile(r'/\* ELB_BLOG_SIDEBAR_START \*/.*?/\* ELB_BLOG_SIDEBAR_END \*/', re.DOTALL)
    ]
    
    for css_pattern in elb_css_patterns:
        css_matches = list(css_pattern.finditer(content))
        if len(css_matches) > 1:
            first_css = css_matches[0].group(0)
            content = css_pattern.sub('', content)
            # Re-insert exactly ONE before </head>
            style_tag = f"<style>\n{first_css}\n</style>"
            content = content.replace('</head>', f"{style_tag}\n</head>", 1)
            modified = True

    # 4. Purge Duplicated Widget (keeping first)
    widget_pattern = re.compile(r'<!-- ELB_YACHTING_WIDGET_START -->.*?<!-- ELB_YACHTING_WIDGET_END -->', re.DOTALL)
    widget_matches = list(widget_pattern.finditer(content))
    if len(widget_matches) > 1:
        first_widget = widget_matches[0].group(0)
        content = widget_pattern.sub('', content)
        # Find the sidebar container and insert there
        if '<aside class="blog-sidebar">' in content:
            content = content.replace('<aside class="blog-sidebar">', f'<aside class="blog-sidebar">\n{first_widget}', 1)
        modified = True

    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    root_dir = r"c:\Users\imran\OneDrive\Desktop\ELB code"
    modified_count = 0
    for root, dirs, files in os.walk(root_dir):
        if any(ignored in root for ignored in ['assets', '.gemini', 'tmp', '.git']):
            continue
        for file in files:
            if file.endswith('.html'):
                if purge_duplicates_in_file(os.path.join(root, file)):
                    modified_count += 1
    print(f"Purged duplicates in {modified_count} files.")

if __name__ == "__main__":
    main()
