import os, re

missing_contact = []
has_contact = []

for f in sorted(os.listdir('.')):
    if not f.endswith('.html') or f.startswith('_'):
        continue
    with open(f, 'r', encoding='utf-8') as fp:
        c = fp.read()

    # Find the nav-links block (desktop nav ul)
    nav_match = re.search(r'class="nav-links".*?</ul>', c, re.DOTALL)
    if nav_match:
        nav_block = nav_match.group(0)
        if '/contact/' in nav_block:
            has_contact.append(f)
        else:
            missing_contact.append(f)

print(f'MISSING Contact in desktop nav ({len(missing_contact)} files):')
for f in missing_contact:
    print(f'  {f}')
print(f'\nHAS Contact in desktop nav ({len(has_contact)} files):')
for f in has_contact:
    print(f'  {f}')
