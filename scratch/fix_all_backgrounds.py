import os
import re

def fix_html_files():
    root_dir = r'c:\Users\imran\OneDrive\Desktop\ELB code'
    files = [f for f in os.listdir(root_dir) if f.endswith('.html')]
    
    # Files to exclude from processing
    exclude_files = {'_template_blog_master.html', '_template_master.html'}
    
    fixed_count = 0
    link_fixed_count = 0
    
    body_style_template = """
        body {
            font-family: 'Inter', sans-serif;
            background: var(--deep-black);
            color: var(--text-main);
            line-height: 1.6;
            overflow-x: hidden;
        }"""
        
    for filename in sorted(files):
        if filename in exclude_files:
            continue
            
        filepath = os.path.join(root_dir, filename)
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        original = content
        modified = False
        
        # 1. Fix relative style.css links to absolute /style.css
        # Match href="style.css" or href='style.css' (without leading slash)
        # Note we want to be careful not to match preloaded fonts or standard cdn css
        # We target style.css specifically
        href_pattern = re.compile(r'href=["\']style\.css["\']', re.IGNORECASE)
        if href_pattern.search(content):
            content = href_pattern.sub('href="/style.css"', content)
            link_fixed_count += 1
            modified = True
            
        # 2. Check if the internal style tag lacks a body selector with background styling
        style_blocks = re.findall(r'<style[^>]*>(.*?)</style>', content, re.DOTALL | re.IGNORECASE)
        
        has_body_bg = False
        for block in style_blocks:
            # Check if there is body selector setting background or background-color
            body_matches = re.findall(r'body\s*\{([^}]*)\}', block, re.IGNORECASE)
            for body_content in body_matches:
                if 'background' in body_content or 'bg' in body_content:
                    has_body_bg = True
                    break
            if re.search(r'body\s*,?\s*[^{]*\{\s*[^}]*background', block, re.IGNORECASE):
                has_body_bg = True
                break
                
        if not has_body_bg:
            # We need to inject the body style block internally
            # Let's find the first <style> block and inject immediately after the :root block (if it exists)
            # or right after <style> if :root is not found.
            style_match = re.search(r'(<style[^>]*>)(.*?)(</style>)', content, re.DOTALL | re.IGNORECASE)
            if style_match:
                style_open = style_match.group(1)
                style_body = style_match.group(2)
                style_close = style_match.group(3)
                
                # Check for :root block inside style_body
                root_match = re.search(r'(:root\s*\{[^}]*\})', style_body, re.DOTALL | re.IGNORECASE)
                if root_match:
                    root_block = root_match.group(1)
                    # Inject body styles immediately after the :root block
                    new_style_body = style_body.replace(root_block, root_block + body_style_template, 1)
                else:
                    # Inject at the very beginning of the style block
                    new_style_body = body_style_template + "\n" + style_body
                    
                # Reconstruct content
                new_style_tag = f"{style_open}{new_style_body}{style_close}"
                content = content.replace(style_match.group(0), new_style_tag, 1)
                fixed_count += 1
                modified = True
                
        if modified:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed {filename}: CSS links fixed? {href_pattern.search(original) is not None}, Body injected? {not has_body_bg}")

    print("\n" + "="*50)
    print(f"Total HTML files checked: {len(files)}")
    print(f"Total files with link fixed: {link_fixed_count}")
    print(f"Total files with body background injected: {fixed_count}")
    print("="*50)

if __name__ == "__main__":
    fix_html_files()
