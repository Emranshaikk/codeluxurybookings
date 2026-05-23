import os
import re

NAV_STYLE_LOCKED = """        /* --- ELITE MOBILE NAV STANDARDIZATION --- */
        .global-nav { position: fixed !important; top: 36px !important; left: 0 !important; right: 0 !important; background: rgba(5, 5, 5, 0.98) !important; backdrop-filter: blur(24px) !important; border-bottom: 1px solid rgba(212, 175, 55, 0.2) !important; z-index: 99999 !important; }
        .global-nav-inner { display: flex !important; align-items: center !important; justify-content: space-between !important; height: 72px !important; gap: 1rem !important; max-width: 1400px !important; margin: 0 auto !important; padding: 0 2rem !important; box-sizing: border-box !important; }
        .nav-brand { font-family: 'Cormorant Garamond', serif !important; font-size: 1.75rem !important; font-weight: 600 !important; color: #fff !important; text-decoration: none !important; }
        .nav-gold { color: #D4AF37 !important; }
        .nav-links { display: flex !important; align-items: center !important; gap: 0.25rem !important; list-style: none !important; flex: 1 !important; justify-content: center !important; margin: 0 !important; padding: 0 !important; }
        .nav-links a { color: rgba(255, 255, 255, 0.7) !important; text-decoration: none !important; font-size: 0.82rem !important; text-transform: uppercase !important; letter-spacing: 1.5px !important; padding: 0.5rem 0.9rem !important; border-radius: 6px !important; transition: all 0.4s !important; font-family: 'Inter', sans-serif !important; }
        .nav-links a:hover { color: #D4AF37 !important; }
        .nav-hamburger { display: none !important; flex-direction: column !important; gap: 5px !important; cursor: pointer !important; padding: 0.5rem !important; z-index: 100001 !important; }
        .nav-hamburger span { display: block !important; width: 24px !important; height: 2px !important; background: rgba(255, 255, 255, 0.8) !important; border-radius: 2px !important; transition: all 0.4s !important; }
        .nav-hamburger.open span:nth-child(1) { transform: rotate(45deg) translate(5px, 5px) !important; }
        .nav-hamburger.open span:nth-child(2) { opacity: 0 !important; }
        .nav-hamburger.open span:nth-child(3) { transform: rotate(-45deg) translate(4px, -4px) !important; }
        .mobile-menu { display: none !important; position: fixed !important; top: 0 !important; left: 0 !important; right: 0 !important; bottom: 0 !important; background: #050505 !important; padding: 72px 2rem 2rem !important; z-index: 100000 !important; flex-direction: column !important; gap: 0.5rem !important; overflow-y: auto !important; }
        .mobile-menu.open { display: flex !important; }
        .mobile-menu a { color: rgba(255, 255, 255, 0.8) !important; text-decoration: none !important; font-size: 1.1rem !important; text-transform: uppercase; letter-spacing: 2px !important; padding: 1.2rem 0 !important; border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important; }
        @media (max-width: 1024px) { .nav-links { display: none !important; } .nav-hamburger { display: flex !important; } }
        /* --- END ELITE MOBILE NAV --- */"""

def fix_header_and_styles(path):
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    modified = False

    # 1. Strip Facebook and Instagram links from the global nav element ONLY
    nav_pattern = re.compile(r'(<nav class="global-nav">.*?</nav>)', re.DOTALL)
    nav_match = nav_pattern.search(content)
    if nav_match:
        nav_block = nav_match.group(1)
        # Remove any <li> containing instagram or facebook inside this navigation element
        cleaned_nav = re.sub(
            r'\s*<li>\s*<a href="https://www\.(?:instagram|facebook)\.com/.*?</li>', 
            '', 
            nav_block, 
            flags=re.DOTALL | re.IGNORECASE
        )
        if cleaned_nav != nav_block:
            content = content.replace(nav_block, cleaned_nav)
            modified = True

    # 2. Enforce style-locked properties in internal style blocks
    style_pattern = re.compile(r'/\*\s*---\s*ELITE MOBILE NAV STANDARDIZATION\s*---\s*\*/.*?/\*\s*---\s*END ELITE MOBILE NAV\s*---\s*\*/', re.DOTALL)
    if style_pattern.search(content):
        new_content = style_pattern.sub(NAV_STYLE_LOCKED.strip(), content)
        if new_content != content:
            content = new_content
            modified = True
    else:
        # If the block isn't present, but </style> is, inject it
        # (This acts as a safety backup, but most pages already have it)
        if "ELITE MOBILE NAV STANDARDIZATION" not in content and "</style>" in content:
            content = content.replace("</style>", NAV_STYLE_LOCKED + "\n    </style>")
            modified = True

    # 3. Standardize body padding-top site-wide to prevent gaps
    body_pattern = re.compile(r'body\s*\{\s*[^}]*padding-top:\s*[^;}\n]+;?\s*\}', re.DOTALL)
    # If the file has a specific body style with padding-top inside its stylesheet
    if body_pattern.search(content):
        content = re.sub(r'body\s*\{\s*[^}]*padding-top:\s*[^;}\n]+;?\s*\}', 'body { padding-top: 110px !important; }', content)
        modified = True

    # 4. Strip any loose custom overrides for global-nav outside the standard block
    loose_pattern = re.compile(r'\.global-nav\s*\{\s*top:\s*0\s*;?\s*\}', re.IGNORECASE)
    if loose_pattern.search(content):
        content = loose_pattern.sub('', content)
        modified = True

    if modified:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    directory = "."
    count = 0
    for root, dirs, files in os.walk(directory):
        if '.git' in root or '_archive' in root or 'scratch' in root or 'fragments' in root:
            continue
        for file in files:
            if file.endswith('.html'):
                path = os.path.join(root, file)
                try:
                    if fix_header_and_styles(path):
                        count += 1
                        print(f"Standardized header & navigation styles: {path}")
                except Exception as e:
                    print(f"Error on {path}: {e}")
    print(f"\nSuccessfully standard-locked header navigation in {count} HTML files!")

if __name__ == '__main__':
    main()
