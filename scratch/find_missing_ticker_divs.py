import os

def check_files():
    html_files = [f for f in os.listdir('.') if f.endswith('.html') and not f.startswith('_') and f != 'old_blog.html']
    html_files.sort()
    
    missing_div = []
    for fname in html_files:
        with open(fname, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Check if the actual <div class="top-intel-bar"> (or similar format) is in the content
        # We search inside body
        body_idx = content.find('<body')
        if body_idx != -1:
            body_content = content[body_idx:]
            if 'class="top-intel-bar"' not in body_content and "class='top-intel-bar'" not in body_content:
                missing_div.append(fname)
        else:
            missing_div.append(fname + " (no body)")
            
    print(f"Audited {len(html_files)} files.")
    print(f"Found {len(missing_div)} files missing the top-intel-bar div inside their body:")
    for f in missing_div:
        print(f"  - {f}")

if __name__ == '__main__':
    check_files()
