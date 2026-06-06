import os

workspace_dir = r"c:\Users\imran\OneDrive\Desktop\ELB code"
files_to_fix = [
    'about.html',
    'bahamas-private-island-rental.html',
    'caribbean-private-island-rental.html',
    'exclusive-private-island-rental.html',
    'luxury-private-island-rental.html',
    'maldives-private-island-rental.html',
    'partners.html',
    'private-island-for-rent.html',
    'private-island-honeymoon-rental.html'
]

replacements = [
    ('src="assets/', 'src="/assets/'),
    ("src='assets/", "src='/assets/"),
    ('url(\'assets/', 'url(\'/assets/'),
    ('url("assets/', 'url("/assets/'),
    ('url(assets/', 'url(/assets/'),
    ('href="assets/', 'href="/assets/'),
    ("href='assets/", "href='/assets/"),
    ("url('assets/", "url('/assets/"),
    ('content="assets/', 'content="/assets/'),
    ("content='assets/", "content='/assets/")
]

for filename in files_to_fix:
    filepath = os.path.join(workspace_dir, filename)
    if not os.path.exists(filepath):
        print(f"Skipping (not found): {filename}")
        continue
        
    print(f"\nFixing unslashed assets in: {filename}")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    fixed_content = content
    for target, replacement in replacements:
        count = fixed_content.count(target)
        if count > 0:
            fixed_content = fixed_content.replace(target, replacement)
            print(f"  Replaced {count} occurrences of '{target}'")
            
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(fixed_content)

print("\nDone fixing all unslashed asset references globally.")
