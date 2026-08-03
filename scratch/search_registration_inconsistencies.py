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

print("Searching all HTML files for registration/footer details...")
print("=" * 80)

# We will search for keywords like 'Telangana', 'Hyderabad', 'United Arab', 'Dubai Marina', 'License No. 1035587', 'ELB Travel Services'
keywords = ['telangana', 'hyderabad', 'united arab', 'dubai marina', 'elb travel services', 'license no', 'registered in india']

matches = []
for fn in html_files:
    path = os.path.join(workspace_dir, fn)
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    for kw in keywords:
        # Search case-insensitively
        matches_kw = re.findall(rf'[^.!?\n]*{re.escape(kw)}[^.!?\n]*', content, re.I)
        for m in matches_kw:
            cleaned = re.sub(r'<[^>]+>', ' ', m).strip()
            cleaned = re.sub(r'\s+', ' ', cleaned)
            matches.append((fn, kw, cleaned))

# Deduplicate matches
unique_matches = list(set(matches))

print(f"Found {len(unique_matches)} matches:")
for fn, kw, text in sorted(unique_matches):
    print(f"File: {fn} (Keyword: {kw})")
    print(f"  Text: {text[:150]}")
    print("-" * 80)
