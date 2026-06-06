import os

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
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    has_og = 'property="og:' in content or 'property=\'og:' in content
    has_twitter = 'name="twitter:' in content or 'name=\'twitter:' in content
    
    print(f"{filename}: Has OG={has_og}, Has Twitter={has_twitter}")
