import os
import re

files_to_check = [
    'yacht-charter-for-wedding.html',
    'luxury-yacht-charter-caribbean.html',
    'luxury-yacht-rental-for-parties.html',
    'luxury-yacht-charter-for-family-vacation.html'
]

workspace_dir = r"c:\Users\imran\OneDrive\Desktop\ELB code"

for filename in files_to_check:
    filepath = os.path.join(workspace_dir, filename)
    if not os.path.exists(filepath):
        continue
    print(f"\n========================================\nFILE: {filename}\n========================================")
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    for i, line in enumerate(lines, 1):
        if '<img' in line.lower() or 'url(' in line.lower():
            print(f"Line {i:4d}: {line.strip()}")
