import os
import glob

CSS_BLOCK = """
        /* --- ELITE MOBILE NAV STANDARDIZATION --- */
        .global-nav { position: fixed; top: 0; left: 0; right: 0; background: rgba(5, 5, 5, 0.98); backdrop-filter: blur(24px); border-bottom: 1px solid rgba(212, 175, 55, 0.2); z-index: 99999; }
        .global-nav-inner { display: flex; align-items: center; justify-content: space-between; height: 72px; gap: 1rem; max-width: 1400px; margin: 0 auto; padding: 0 2rem; box-sizing: border-box; }
        .nav-brand { font-family: 'Cormorant Garamond', serif; font-size: 1.75rem; font-weight: 600; color: #fff !important; text-decoration: none !important; }
        .nav-gold { color: #D4AF37 !important; }
        .nav-links { display: flex; align-items: center; gap: 0.25rem; list-style: none; flex: 1; justify-content: center; margin: 0; padding: 0; }
        .nav-links a { color: rgba(255, 255, 255, 0.7) !important; text-decoration: none !important; font-size: 0.82rem; text-transform: uppercase; letter-spacing: 1.5px; padding: 0.5rem 0.9rem; border-radius: 6px; transition: all 0.4s; font-family: 'Inter', sans-serif !important; }
        .nav-links a:hover { color: #D4AF37 !important; }
        .nav-hamburger { display: none; flex-direction: column; gap: 5px; cursor: pointer; padding: 0.5rem; z-index: 100001; }
        .nav-hamburger span { display: block; width: 24px; height: 2px; background: rgba(255, 255, 255, 0.8); border-radius: 2px; transition: all 0.4s; }
        .nav-hamburger.open span:nth-child(1) { transform: rotate(45deg) translate(5px, 5px); }
        .nav-hamburger.open span:nth-child(2) { opacity: 0; }
        .nav-hamburger.open span:nth-child(3) { transform: rotate(-45deg) translate(4px, -4px); }
        .mobile-menu { display: none; position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: #050505; padding: 72px 2rem 2rem; z-index: 100000; flex-direction: column; gap: 0.5rem; overflow-y: auto; }
        .mobile-menu.open { display: flex !important; }
        .mobile-menu a { color: rgba(255, 255, 255, 0.8) !important; text-decoration: none !important; font-size: 1.1rem; text-transform: uppercase; letter-spacing: 2px; padding: 1.2rem 0; border-bottom: 1px solid rgba(255, 255, 255, 0.05); }
        @media (max-width: 1024px) { .nav-links { display: none !important; } .nav-hamburger { display: flex !important; } }
        /* --- END ELITE MOBILE NAV --- */
</style>"""

def process_file(filepath):
    if 'index.html' in filepath or filepath.endswith('template_blog_master.html'):
        return
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    if 'ELITE MOBILE NAV STANDARDIZATION' not in content:
        # Insert right before </style>
        new_content = content.replace('</style>', CSS_BLOCK)
        
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Injected mobile nav CSS into {filepath}")

for f in glob.glob('*.html'):
    process_file(f)
