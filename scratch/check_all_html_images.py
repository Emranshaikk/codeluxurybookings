import os
import re

workspace_dir = r"c:\Users\imran\OneDrive\Desktop\ELB code"
html_files = [f for f in os.listdir(workspace_dir) if f.endswith('.html')]

print(f"Checking {len(html_files)} HTML files for relative assets/ paths...")

unslashed_pattern = re.compile(r'(?:src|href|url)\(["\']?assets/|["\']assets/')

unslashed_references = {}

for filename in html_files:
    filepath = os.path.join(workspace_dir, filename)
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    
    # Search for occurrences of src="assets/... or url('assets/... or href="assets/...
    # but not starting with /
    matches_src = re.findall(r'src=["\'](assets/[^"\']+)["\']', content)
    matches_url = re.findall(r'url\(["\']?(assets/[^"\')]+)["\']?\)', content)
    matches_href = re.findall(r'href=["\'](assets/[^"\']+)["\']', content)
    
    all_matches = matches_src + matches_url + matches_href
    if all_matches:
        unslashed_references[filename] = all_matches

if unslashed_references:
    print("\nFound unslashed references:")
    for file, refs in unslashed_references.items():
        print(f"\n{file}:")
        for ref in set(refs):
            print(f"  - {ref}")
else:
    print("\nNo unslashed assets/ references found in any HTML file!")
