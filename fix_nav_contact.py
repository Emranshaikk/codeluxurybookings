"""
Fix missing Contact link in desktop nav across all pages.
Uses safe string replacement - no HTML parsing, no design changes.
"""
import os, re

CONTACT_LINK = '<li><a href="https://eliteluxurybookings.com/contact/" style="color: rgba(255, 255, 255, 0.85); text-decoration:none; font-size:0.9rem; transition:color 0.3s;" onmouseover="this.style.color=\'#D4AF37\'" onmouseout="this.style.color=\'rgba(255, 255, 255, 0.85)\'">Contact</a></li>'

# The Blog nav item appears in different forms - match all variants
BLOG_PATTERNS = [
    # Pattern 1: Blog with inline style (most common)
    (r'(<li><a href="https://eliteluxurybookings\.com/blog/"[^>]*>Blog</a></li>)(\s*\n?\s*</ul>)',
     lambda m: m.group(1) + '\n                ' + CONTACT_LINK + m.group(2)),
    # Pattern 2: Blog without inline style  
    (r'(<li><a href="https://eliteluxurybookings\.com/blog/">Blog</a></li>)(\s*\n?\s*</ul>)',
     lambda m: m.group(1) + '\n                ' + CONTACT_LINK + m.group(2)),
]

fixed = 0
skipped = 0
already_has = 0

for f in sorted(os.listdir('.')):
    if not f.endswith('.html') or f.startswith('_'):
        continue
    
    with open(f, 'r', encoding='utf-8') as fp:
        content = fp.read()

    # Check if nav-links block exists
    if 'class="nav-links"' not in content:
        skipped += 1
        continue

    # Check if already has contact in nav-links
    nav_match = re.search(r'class="nav-links".*?</ul>', content, re.DOTALL)
    if nav_match and '/contact/' in nav_match.group(0):
        already_has += 1
        continue

    original = content
    applied = False

    for pattern, replacement in BLOG_PATTERNS:
        new_content = re.sub(pattern, replacement, content, count=1)
        if new_content != content:
            content = new_content
            applied = True
            break

    if applied and content != original:
        with open(f, 'w', encoding='utf-8') as fp:
            fp.write(content)
        fixed += 1
        print(f'  Fixed: {f}')
    elif not applied:
        print(f'  WARN (pattern not matched): {f}')

print(f'\n{"="*50}')
print(f'Fixed:       {fixed} pages')
print(f'Already had: {already_has} pages')
print(f'Skipped:     {skipped} pages (no nav-links)')
print(f'{"="*50}')
