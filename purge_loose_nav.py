import os
import re

def purge_loose_nav(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        return False

    original = content
    
    # We want to remove any <nav class="global-nav"> ... </nav> 
    # EXCEPT the one that is inside <!-- ELB_NAV_START --> ... <!-- ELB_NAV_END -->
    
    # 1. Temporarily replace the good nav with a placeholder
    elb_nav_pattern = r'(<!-- ELB_NAV_START -->.*?<!-- ELB_NAV_END -->)'
    match = re.search(elb_nav_pattern, content, flags=re.DOTALL)
    
    good_nav = ""
    if match:
        good_nav = match.group(1)
        content = content.replace(good_nav, "@@GOOD_NAV_PLACEHOLDER@@")
    
    # 2. Remove any remaining <nav class="global-nav">
    # Wait, the old nav in blog/index.html has <nav class="global-nav"> ... </nav>
    # We can match it carefully balancing tags, but regex can be tricky.
    # We'll match <nav class="global-nav"> and stop at the first </nav> then check if it's the right one.
    content = re.sub(r'<nav class="global-nav">.*?</nav>', '', content, flags=re.DOTALL)
    
    # Also remove any stray mobile menus that are loose: <div class="mobile-menu" id="elbMobileMenu"> ... </div>
    content = re.sub(r'<div class="mobile-menu" id="elbMobileMenu">.*?</div>', '', content, flags=re.DOTALL)
    
    # 3. Put the good nav back
    if good_nav:
        content = content.replace("@@GOOD_NAV_PLACEHOLDER@@", good_nav)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

root = r'c:\Users\imran\OneDrive\Desktop\ELB code'
count = 0
for r, d, files in os.walk(root):
    for f in files:
        if f.endswith('.html'):
            if purge_loose_nav(os.path.join(r, f)):
                count += 1
print(f'Purged loose navs in {count} files.')
