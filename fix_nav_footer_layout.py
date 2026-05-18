import os
import re

CONTACT_LINK = '<li><a href="https://eliteluxurybookings.com/contact/" style="color: rgba(255, 255, 255, 0.85); text-decoration:none; font-size:0.9rem; transition:color 0.3s;" onmouseover="this.style.color=\'#D4AF37\'" onmouseout="this.style.color=\'rgba(255, 255, 255, 0.85)\'">Contact</a></li>'

NEW_NAV_LINKS_CSS = """        .nav-links {
            display: flex;
            align-items: center;
            gap: 0.25rem;
            list-style: none;
            flex: 1;
            justify-content: center;
            margin: 0;
            padding: 0;
        }"""

directory = r"c:\Users\imran\OneDrive\Desktop\ELB code"

for filename in os.listdir(directory):
    if not filename.endswith(".html"):
        continue
        
    path = os.path.join(directory, filename)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    original = content
    
    # 1. Normalize Nav HTML: Replace chaotic inline styles with class="nav-links"
    # E.g. <ul style="display:flex; gap:2rem; list-style:none; margin:0; padding:0; align-items:center;">
    content = re.sub(r'<ul\s+style="display:flex;?\s*gap:[^>]+align-items:center;?">', '<ul class="nav-links">', content)
    content = re.sub(r'<ul\s+style="display:\s*flex;\s*gap:\s*2rem;\s*list-style:\s*none;\s*margin:\s*0;\s*padding:\s*0;\s*align-items:\s*center;">', '<ul class="nav-links">', content)
    
    # 2. Inject Contact Link into any <ul class="nav-links"> that lacks it
    nav_match = re.search(r'<ul class="nav-links">.*?</ul>', content, re.DOTALL)
    if nav_match:
        nav_block = nav_match.group(0)
        if '/contact/' not in nav_block:
            # Inject right before </ul>
            new_nav_block = nav_block.replace('</ul>', f'    {CONTACT_LINK}\n                    </ul>')
            content = content.replace(nav_block, new_nav_block)

    # 3. Standardize .nav-links CSS inside <style>
    # Find existing .nav-links block and replace it
    content = re.sub(r'\.nav-links\s*\{[^}]*align-items:\s*center;\s*\}', NEW_NAV_LINKS_CSS, content)
    
    # Just to be sure we also catch the one in index.html exactly:
    content = re.sub(r'\.nav-links\s*\{\s*display:\s*flex;\s*gap:\s*0\.5rem;\s*list-style:\s*none;\s*margin:\s*0;\s*padding:\s*0;\s*align-items:\s*center;\s*\}', NEW_NAV_LINKS_CSS, content)

    # 4. Strip old legacy FOOTER CSS blocks
    # Looking for /* FOOTER */ up to .footer-links a:hover { ... } or up to @keyframes
    content = re.sub(r'/\*\s*FOOTER\s*\*/.*?\.footer-links\s*a:hover\s*\{[^}]*\}', '', content, flags=re.DOTALL)
    
    if content != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed {filename}")

print("Done fixing navigation and footers.")
