import os
import re
import sys

# Ensure stdout uses UTF-8
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

workspace_dir = r"c:\Users\imran\OneDrive\Desktop\ELB code"
html_files = [f for f in os.listdir(workspace_dir) if f.endswith('.html')]

print("Scanning for forms with missing javascript handler definitions...")
print("=" * 80)

broken_files = []

for fn in sorted(html_files):
    path = os.path.join(workspace_dir, fn)
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()
        
    # Find onsubmit attributes
    onsubmits = re.findall(r'onsubmit=["\'](\w+)\(', html)
    if not onsubmits:
         # check for simple attributes
         onsubmits = re.findall(r'onsubmit=["\']([^"\'\(]+)\(', html)
         
    for func_name in onsubmits:
        func_name = func_name.strip()
        if not func_name:
            continue
            
        # check if this function name is defined in scripts
        func_def_pattern = rf'function\s+{func_name}\b|{func_name}\s*=\s*'
        if not re.search(func_def_pattern, html):
            broken_files.append((fn, func_name))

print(f"Found {len(broken_files)} instances of missing submit handlers:")
for fn, func in broken_files:
    print(f"File: {fn}")
    print(f"  Missing handler function: {func}")
    print("-" * 80)
