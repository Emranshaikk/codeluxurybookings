import os
import re

NAV_STYLE_LOCKED = """        /* --- ELITE NAV & TICKER STANDARDIZATION --- */
        .top-intel-bar { background: rgba(5, 5, 5, 0.98) !important; border-bottom: 1px solid rgba(212, 175, 55, 0.3) !important; height: 36px !important; overflow: hidden !important; position: fixed !important; top: 0 !important; left: 0 !important; right: 0 !important; z-index: 100000 !important; display: flex !important; align-items: center !important; }
        .ticker-wrap { white-space: nowrap !important; overflow: hidden !important; width: 100% !important; }
        .ticker-content { display: inline-block !important; white-space: nowrap !important; padding-left: 100% !important; animation: ticker-scroll 40s linear infinite !important; font-size: 0.72rem !important; letter-spacing: 2px !important; text-transform: uppercase !important; color: rgba(255, 255, 255, 0.9) !important; }
        @keyframes ticker-scroll { 0% { transform: translate3d(0, 0, 0); } 100% { transform: translate3d(-200%, 0, 0); } }
        .ticker-content strong { color: #D4AF37 !important; margin: 0 40px !important; }
        .ticker-content a { color: #fff !important; text-decoration: underline !important; text-underline-offset: 4px !important; margin-left: 10px !important; font-weight: 600 !important; }
        
        .global-nav { position: fixed !important; top: 0 !important; left: 0 !important; right: 0 !important; background: rgba(5, 5, 5, 0.98) !important; backdrop-filter: blur(24px) !important; border-bottom: 1px solid rgba(212, 175, 55, 0.2) !important; z-index: 99999 !important; transition: top 0.3s ease !important; }
        .top-intel-bar ~ .global-nav { top: 36px !important; }
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
        .mobile-menu a { color: rgba(255, 255, 255, 0.8) !important; text-decoration: none !important; font-size: 1.1rem !important; text-transform: uppercase !important; letter-spacing: 2px !important; padding: 1.2rem 0 !important; border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important; }
        @media (max-width: 1024px) { .nav-links { display: none !important; } .nav-hamburger { display: flex !important; } }
        
        body { padding-top: 72px !important; }
        body:has(.top-intel-bar) { padding-top: 108px !important; }
        
        @media (max-width: 768px) {
            .top-intel-bar { height: 32px !important; }
            .top-intel-bar ~ .global-nav { top: 32px !important; }
            body:has(.top-intel-bar) { padding-top: 104px !important; }
        }
        /* --- END ELITE NAV & TICKER --- */"""

def fix_file(path):
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    modified = False

    # 1. Look for the older version of the mobile nav block and replace it
    old_nav_pattern = re.compile(
        r'/\*\s*---\s*ELITE MOBILE NAV STANDARDIZATION\s*---\s*\*/.*?/\*\s*---\s*END ELITE MOBILE NAV\s*---\s*\*/', 
        re.DOTALL
    )
    new_nav_pattern = re.compile(
        r'/\*\s*---\s*ELITE NAV & TICKER STANDARDIZATION\s*---\s*\*/.*?/\*\s*---\s*END ELITE NAV & TICKER\s*---\s*\*/', 
        re.DOTALL
    )

    if old_nav_pattern.search(content):
        content = old_nav_pattern.sub(NAV_STYLE_LOCKED.strip(), content)
        modified = True
    elif new_nav_pattern.search(content):
        new_content = new_nav_pattern.sub(NAV_STYLE_LOCKED.strip(), content)
        if new_content != content:
            content = new_content
            modified = True
    else:
        # Safety injection if neither block exists but </style> does
        if "ELITE NAV & TICKER STANDARDIZATION" not in content and "</style>" in content:
            content = content.replace("</style>", NAV_STYLE_LOCKED + "\n    </style>")
            modified = True

    # 2. Clean up any hardcoded layout-shifting loose body styles
    body_pattern = re.compile(r'body\s*\{\s*[^}]*padding-top:\s*[^;}\n]+;?\s*\}', re.DOTALL)
    if body_pattern.search(content):
        # We can safely clean loose padding-top since our standardized block now handles body padding dynamically via:
        # body { padding-top: 72px !important; }
        # body:has(.top-intel-bar) { padding-top: 108px !important; }
        # Let's remove any loose body style block that has padding-top and matches standard patterns
        content = re.sub(
            r'body\s*\{\s*[^}]*padding-top:\s*(?:110px|108px)\s*!important\s*;?\s*\}',
            '',
            content
        )
        modified = True

    if modified:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def fix_style_css():
    path = "style.css"
    if not os.path.exists(path):
        return
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    modified = False

    # Standardize global nav and ticker in style.css as well to avoid conflicts
    # Let's look for .global-nav block in style.css
    global_nav_css = """/* --- GLOBAL NAVIGATION --- */
.global-nav {
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    right: 0 !important;
    background: rgba(5, 5, 5, 0.98) !important;
    backdrop-filter: blur(24px) !important;
    border-bottom: 1px solid rgba(212, 175, 55, 0.2) !important;
    z-index: 99999 !important;
    transition: top 0.3s ease !important;
}

.top-intel-bar ~ .global-nav {
    top: 36px !important;
}

body {
    padding-top: 72px !important;
}

body:has(.top-intel-bar) {
    padding-top: 108px !important;
}

@media (max-width: 768px) {
    .top-intel-bar ~ .global-nav {
        top: 32px !important;
    }
    body:has(.top-intel-bar) {
        padding-top: 104px !important;
    }
}"""

    # Replace the old global nav block in style.css
    nav_pattern = re.compile(r'/\*\s*---\s*GLOBAL NAVIGATION\s*---\s*\*/.*?\.global-nav-inner\s*\{', re.DOTALL)
    if nav_pattern.search(content):
        content = nav_pattern.sub(global_nav_css + "\n\n.global-nav-inner {", content)
        modified = True
    
    # Also clean up loose top-intel-bar and body styles inside style.css
    # We want body padding-top in style.css to match
    body_pattern = re.compile(r'body\s*\{\s*[^}]*padding-top:\s*108px\s*!important\s*;?\s*\}', re.DOTALL)
    if body_pattern.search(content):
        content = body_pattern.sub('', content)
        modified = True

    if modified:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Successfully updated style.css with dynamic layout-locked rules!")

def main():
    fix_style_css()
    directory = "."
    count = 0
    for root, dirs, files in os.walk(directory):
        if '.git' in root or '_archive' in root or 'scratch' in root or 'fragments' in root:
            continue
        for file in files:
            if file.endswith('.html'):
                path = os.path.join(root, file)
                try:
                    if fix_file(path):
                        count += 1
                        print(f"Standardized dynamic layout: {path}")
                except Exception as e:
                    print(f"Error on {path}: {e}")
    print(f"\nSuccessfully deployed dynamic layout-locks to {count} HTML files!")

if __name__ == '__main__':
    main()
