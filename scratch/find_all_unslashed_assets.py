import os
import re

workspace_dir = r"c:\Users\imran\OneDrive\Desktop\ELB code"
html_files = [f for f in os.listdir(workspace_dir) if f.endswith('.html')]

print(f"Scanning {len(html_files)} HTML files for unslashed asset references...")
unslashed_by_file = {}

unslashed_patterns = [
    r'src=["\']assets/',
    r'href=["\']assets/',
    r'url\(["\']?assets/',
    r'content=["\']assets/'
]

for filename in html_files:
    filepath = os.path.join(workspace_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    for pattern in unslashed_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        if matches:
            if filename not in unslashed_by_file:
                unslashed_by_file[filename] = 0
            unslashed_by_file[filename] += len(matches)

if unslashed_by_file:
    print(f"\nFound unslashed references in {len(unslashed_by_file)} files:")
    for fn, count in sorted(unslashed_by_file.items()):
        print(f"  - {fn}: {count} unslashed references")
else:
    print("\nSUCCESS: All asset references have correct leading slashes across all files!")
