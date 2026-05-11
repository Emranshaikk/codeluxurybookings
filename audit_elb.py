import os
import re

def audit_files():
    root_dir = r'c:\Users\imran\OneDrive\Desktop\ELB code'
    files = [f for f in os.listdir(root_dir) if f.endswith('.html')]
    
    problems = []
    
    # Pattern for the broken CSS
    broken_css_pattern = re.compile(r'\}\s+background: rgba\(255, 255, 255, 0\.8\);', re.MULTILINE)
    
    for filename in files:
        filepath = os.path.join(root_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if broken_css_pattern.search(content):
            problems.append(f"{filename}: Broken CSS (missing selector for background)")
            
        if '<footer' in content and 'footer-grid' not in content:
             # Exclude files that might not need the full footer but check anyway
             if filename not in ['404.html', 'thank-you.html']:
                problems.append(f"{filename}: Legacy footer detected")

    if not problems:
        print("No problems found.")
    else:
        print("Problems found:")
        for p in problems:
            print(f"- {p}")

if __name__ == "__main__":
    audit_files()
