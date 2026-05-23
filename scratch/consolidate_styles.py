import os
import re

def consolidate_styles():
    root_dir = r'c:\Users\imran\OneDrive\Desktop\ELB code'
    files = [f for f in os.listdir(root_dir) if f.endswith('.html')]
    
    # These are the patterns we want to remove because they are now in style.css
    # We look for large blocks of CSS that match our global styles
    patterns_to_remove = [
        re.compile(r':root\s*{[^}]*--primary-gold:[^}]*}', re.DOTALL),
        re.compile(r'\*\s*{[^}]*margin:\s*0;[^}]*}', re.DOTALL),
        re.compile(r'body\s*{[^}]*font-family:\s*\'Inter\'[^}]*}', re.DOTALL),
        re.compile(r'\.global-nav\s*{[^}]*}', re.DOTALL),
        re.compile(r'\.global-nav-inner\s*{[^}]*}', re.DOTALL),
        re.compile(r'\.nav-brand\s*{[^}]*}', re.DOTALL),
        re.compile(r'\.nav-links\s*{[^}]*}', re.DOTALL),
        re.compile(r'\.footer\s*{[^}]*}', re.DOTALL),
        re.compile(r'\.footer-grid\s*{[^}]*}', re.DOTALL),
        re.compile(r'\.top-intel-bar\s*{[^}]*}', re.DOTALL),
        re.compile(r'\.ticker-wrap\s*{[^}]*}', re.DOTALL),
        re.compile(r'\.ticker-content\s*{[^}]*}', re.DOTALL),
    ]

    for filename in files:
        filepath = os.path.join(root_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        modified = False
        
        # 1. Add link to style.css if not present
        if 'style.css' not in content:
            link_tag = '    <link rel="stylesheet" href="style.css">'
            if '</head>' in content:
                content = content.replace('</head>', link_tag + '\n</head>')
                modified = True
                print(f"Added style.css link to {filename}")

        # 2. Clean up redundant styles
        # This is tricky because we don't want to leave empty <style> tags
        # We'll try to find the <style> block containing the :root
        style_block_match = re.search(r'<style>(.*?)</style>', content, re.DOTALL)
        if style_block_match:
            style_content = style_block_match.group(1)
            original_style_content = style_content
            
            for pattern in patterns_to_remove:
                style_content = pattern.sub('', style_content)
            
            if style_content != original_style_content:
                # If the style content is now mostly whitespace, remove the whole tag?
                # No, better to just replace the inner content to be safe.
                # If it's totally empty, we can remove it.
                if not style_content.strip():
                    content = content.replace(style_block_match.group(0), '')
                else:
                    content = content.replace(original_style_content, style_content)
                modified = True
                print(f"Cleaned up styles in {filename}")

        if modified:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

if __name__ == "__main__":
    consolidate_styles()
