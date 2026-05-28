import os
import re

def audit_html_files():
    root_dir = r'c:\Users\imran\OneDrive\Desktop\ELB code'
    files = [f for f in os.listdir(root_dir) if f.endswith('.html')]
    
    no_body_bg = []
    has_body_bg = []
    
    for filename in files:
        filepath = os.path.join(root_dir, filename)
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        # Check if the internal style has a body block setting the background
        # e.g., body { ... background: ... } or body { ... background-color: ... }
        # Let's extract the <style> tags and check them
        style_blocks = re.findall(r'<style[^>]*>(.*?)</style>', content, re.DOTALL | re.IGNORECASE)
        
        has_bg = False
        for block in style_blocks:
            # Look for body selector
            # It could be: body { ... } or body, html { ... } etc.
            # Let's search if "body" is defined as a selector in the CSS block
            # We want to check if the selector sets background or background-color
            # A simple way is to match body { ... }
            body_matches = re.findall(r'body\s*\{([^}]*)\}', block, re.IGNORECASE)
            for body_content in body_matches:
                if 'background' in body_content or 'bg' in body_content:
                    has_bg = True
                    break
            
            # Also check if there is an override like body { background: ... }
            if re.search(r'body\s*,?\s*[^{]*\{\s*[^}]*background', block, re.IGNORECASE):
                has_bg = True
                break
                
        if has_bg:
            has_body_bg.append(filename)
        else:
            no_body_bg.append(filename)
            
    print(f"Files WITH body background internally ({len(has_body_bg)}):")
    # print(has_body_bg)
    print("\nFiles WITHOUT body background internally:")
    for f in sorted(no_body_bg):
        print(f"- {f}")

if __name__ == "__main__":
    audit_html_files()
