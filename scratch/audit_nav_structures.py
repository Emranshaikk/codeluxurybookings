import os
import re

def audit_nav():
    root_dir = '.'
    files = [f for f in os.listdir(root_dir) if f.endswith('.html')]
    files.sort()
    
    mangled_files = []
    
    for filename in files:
        if filename in ['old_blog.html']:
            continue
        filepath = os.path.join(root_dir, filename)
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        issues = []
        
        # Exact check for nesting:
        # Find index of top-intel-bar
        intel_idx = content.find('class="top-intel-bar"')
        nav_idx = content.find('class="global-nav"')
        
        if intel_idx != -1 and nav_idx != -1:
            # Let's count open/close divs from intel_idx to see where top-intel-bar closes
            # Since we just want to know if global-nav is inside top-intel-bar:
            # If global-nav is inside top-intel-bar, then the top-intel-bar div tag's close tag
            # will appear AFTER the global-nav tag.
            # Let's extract content between intel_idx and nav_idx
            if nav_idx > intel_idx:
                between_content = content[intel_idx:nav_idx]
                # Count opening divs vs closing divs in between
                # Note: <div class="top-intel-bar">, <div class="ticker-wrap">, <div class="ticker-content">
                # That is 3 opening divs. If the closing divs do not match, it means top-intel-bar is not closed!
                open_divs = len(re.findall(r'<div[^>]*>', between_content, re.IGNORECASE))
                close_divs = len(re.findall(r'</div>', between_content, re.IGNORECASE))
                
                # If close_divs < open_divs, it means the top-intel-bar is still open when global-nav starts!
                if close_divs < open_divs:
                    issues.append(f"global-nav nested inside top-intel-bar (open: {open_divs}, close: {close_divs} before nav)")
            
        # 1. Are there duplicate mobile menus?
        mobile_menu_count = len(re.findall(r'id="elbMobileMenu"', content))
        if mobile_menu_count > 1:
            issues.append(f"Duplicate mobile menu (count: {mobile_menu_count})")
            
        # 2. Is there a stray </nav> close tag after </nav>?
        if len(re.findall(r'</nav>\s*</nav>', content)) > 0 or len(re.findall(r'</nav>\s*</div>\s*</nav>', content)) > 0:
            issues.append("Stray nested </nav> close tags")
            
        if issues:
            mangled_files.append((filename, issues))
            
    print(f"Audited {len(files)} HTML files.\n")
    print(f"=== DETECTED NAV ISSUES ({len(mangled_files)} files) ===")
    for filename, issues in mangled_files:
        print(f"[{filename}]")
        for issue in issues:
            print(f"  - {issue}")
        print()

if __name__ == '__main__':
    audit_nav()
