import os
import re

# Define the Perfect Snippets from index.html

PERFECT_STYLE = """<style>
/* ELB_STYLE_START */
    .global-nav { position:fixed; top:0; left:0; right:0; background:rgba(5,5,5,0.98); backdrop-filter:blur(24px); border-bottom:1px solid rgba(212,175,55,0.2); z-index:99999; }
    .global-nav-inner { display:flex; align-items:center; justify-content:space-between; height:72px; gap:1rem; max-width:1400px; margin:0 auto; padding:0 2rem; box-sizing: border-box; }
    .nav-brand { font-family:'Cormorant Garamond',serif; font-size:1.75rem; font-weight:600; color:#fff !important; text-decoration:none !important; }
    .nav-gold { color:#D4AF37 !important; }
    .nav-links { display:flex; align-items:center; gap:0.25rem; list-style:none; flex:1; justify-content:center; margin:0; padding:0; }
    .nav-links a { color:rgba(255,255,255,0.7) !important; text-decoration:none !important; font-size:0.82rem; text-transform:uppercase; letter-spacing:1.5px; padding:0.5rem 0.9rem; border-radius:6px; transition:all 0.4s; font-family: 'Inter', sans-serif !important; }
    .nav-links a:hover { color:#D4AF37 !important; }
    .nav-dropdown { position:relative; }
    .dropdown-menu { position:absolute; top:calc(100% + 8px); left:0; background:#0a0a0a; border:1px solid rgba(212,175,55,0.15); border-radius:12px; padding:0.75rem; min-width:240px; opacity:0; visibility:hidden; transform:translateY(-8px); transition:all 0.4s; box-shadow:0 20px 40px rgba(0,0,0,0.8); z-index:100; }
    .nav-dropdown:hover .dropdown-menu { opacity:1 !important; visibility:visible !important; transform:translateY(0) !important; }
    .dropdown-menu a { display:block !important; padding:0.7rem 1.2rem !important; color:rgba(255,255,255,0.7) !important; border-radius:8px; font-size:0.85rem !important; text-transform: none !important; }
    .nav-hamburger { display:none; flex-direction:column; gap:5px; cursor:pointer; padding:0.5rem; z-index:100001; }
    .nav-hamburger span { display:block; width:24px; height:2px; background:rgba(255,255,255,0.8); border-radius:2px; transition:all 0.4s; }
    .mobile-menu { display:none; position:fixed; top:0; left:0; right:0; bottom:0; background:#050505; padding:72px 2rem 2rem; z-index:100000; flex-direction:column; gap:0.5rem; overflow-y: auto; }
    .mobile-menu.open { display:flex !important; }
    .mobile-menu a { color:rgba(255,255,255,0.8) !important; text-decoration:none !important; font-size:1.1rem; text-transform:uppercase; letter-spacing:2px; padding:1.2rem 0; border-bottom:1px solid rgba(255,255,255,0.05); }
    .mobile-cta { margin-top:2rem; text-align:center; background:linear-gradient(135deg,#D4AF37,#B8860B); color:#000 !important; border-radius:8px; padding:1.2rem !important; font-weight:700; }
    @media (max-width:1024px) { .nav-links { display:none !important; } .nav-hamburger { display:flex !important; } }
    body { padding-top: 72px !important; }
    .luxury-list li::before { content: '✓' !important; }
/* ELB_STYLE_END */
</style>"""

PERFECT_NAV = """<!-- ELB_NAV_START -->
    <nav class="global-nav">
        <div class="container global-nav-inner">
            <a href="/" class="nav-brand"><span class="nav-gold">Elite</span> Luxury Bookings</a>
            <ul class="nav-links">
                <li class="nav-dropdown"><a href="/elite-private-jet-charter/">Private Jets</a>
                    <div class="dropdown-menu">
                        <a href="/elite-private-jet-charter/">Jet Charters Overview</a>
                        <a href="/private-jet-rental-prices/">Rental Prices</a>
                        <a href="/types-of-private-jets/">Types of Jets</a>
                        <a href="/empty-leg-flights-discount/">Empty Leg Deals</a>
                        <a href="/private-jet-for-business-travel/">Business Travel</a>
                    </div>
                </li>
                <li class="nav-dropdown"><a href="/luxury-yacht-rentals/">Yacht Charter</a>
                    <div class="dropdown-menu">
                        <a href="/luxury-yacht-rentals/">Yacht Rental Overview</a>
                        <a href="/luxury-yacht-rentals/renting-catamaran/">Catamaran Rental</a>
                        <a href="/luxury-yacht-rentals/best-sailing-yacht-charter/">Sailing Yachts</a>
                        <a href="/luxury-yacht-rentals/bareboat-charter-guide/">Bareboat Guide</a>
                    </div>
                </li>
                <li><a href="/luxury-villa-rentals/">Villas</a></li>
                <li><a href="/blog/">Blog</a></li>
                <li><a href="/contact/">Contact</a></li>
            </ul>
            <div class="nav-cta">
                <a href="https://wa.me/918801079030" class="btn btn-gold btn-sm">Direct Concierge</a>
                <div class="nav-hamburger" id="navHamburger" onclick="toggleMobileMenu()">
                    <span></span><span></span><span></span>
                </div>
            </div>
        </div>
    </nav>
    <div class="mobile-menu" id="elbMobileMenu">
        <a href="/elite-private-jet-charter/">Private Jets</a>
        <a href="/luxury-yacht-rentals/">Luxury Yachts</a>
        <a href="/luxury-villa-rentals/">Exclusive Villas</a>
        <a href="/blog/">Articles & News</a>
        <a href="/contact/">Contact Us</a>
        <a href="https://wa.me/918801079030" class="mobile-cta">WhatsApp Concierge</a>
    </div>
<!-- ELB_NAV_END -->"""

PERFECT_FOOTER = """<!-- ELB_FOOTER_START -->
    <footer class="section-padding" style="background: #000; border-top: 1px solid rgba(255,255,255,0.05); text-align: center; margin-top: 5rem;">
        <div class="container">
            <a href="/" style="display: block; margin-bottom: 2rem; font-family:'Cormorant Garamond',serif; font-size:2rem; font-weight:600; color:#fff; text-decoration:none;"><span style="color:#D4AF37;">Elite</span> Luxury Bookings</a>
            <div style="display: flex; justify-content: center; gap: 3rem; flex-wrap: wrap; margin-bottom: 2rem;">
                <a href="/elite-private-jet-charter/" style="color: rgba(255,255,255,0.6); text-decoration: none; font-size: 0.9rem;">Aviation Services</a>
                <a href="/luxury-yacht-rentals/" style="color: rgba(255,255,255,0.6); text-decoration: none; font-size: 0.9rem;">Yacht Charter</a>
                <a href="/luxury-villa-rentals/" style="color: rgba(255,255,255,0.6); text-decoration: none; font-size: 0.9rem;">Villa Rentals</a>
                <a href="/blog/" style="color: rgba(255,255,255,0.6); text-decoration: none; font-size: 0.9rem;">Blog</a>
                <a href="/contact/" style="color: rgba(255,255,255,0.6); text-decoration: none; font-size: 0.9rem;">Contact</a>
            </div>
            <p style="color: #444; font-size: 0.8rem;">© 2026 Elite Luxury Bookings. All rights reserved.</p>
        </div>
    </footer>
<!-- ELB_FOOTER_END -->"""

PERFECT_JS = """<!-- ELB_JS_START -->
    <script>function toggleMobileMenu(){var m=document.getElementById('elbMobileMenu'),b=document.getElementById('navHamburger');if(m&&b){m.classList.toggle('open');b.classList.toggle('open');}}</script>
<!-- ELB_JS_END -->"""

def standardize_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        return False

    original = content
    
    # 1. Replace Style Block (with tags)
    content = re.sub(r'<style>\s*/\* ELB_STYLE_START \*/.*?/\* ELB_STYLE_END \*/\s*</style>', PERFECT_STYLE, content, flags=re.DOTALL)
    # Fallback if tags are already messed up or missing
    content = re.sub(r'/\* ELB_STYLE_START \*/.*?/\* ELB_STYLE_END \*/', PERFECT_STYLE.replace('<style>','').replace('</style>',''), content, flags=re.DOTALL)
    
    # 2. Replace Nav, Footer, JS Blocks
    content = re.sub(r'<!-- ELB_NAV_START -->.*?<!-- ELB_NAV_END -->', PERFECT_NAV, content, flags=re.DOTALL)
    content = re.sub(r'<!-- ELB_FOOTER_START -->.*?<!-- ELB_FOOTER_END -->', PERFECT_FOOTER, content, flags=re.DOTALL)
    content = re.sub(r'<!-- ELB_JS_START -->.*?<!-- ELB_JS_END -->', PERFECT_JS, content, flags=re.DOTALL)
    
    # 3. Cleanup Loose Styles
    parts = re.split(r'(<style>.*?</style>)', content, flags=re.DOTALL)
    new_parts = []
    for part in parts:
        if part.startswith('<style>'):
            # If it contains global-nav or nav-links but is NOT the ELB block, drop it
            if ('global-nav' in part or 'nav-links' in part) and 'ELB_STYLE_START' not in part:
                continue 
        new_parts.append(part)
    content = "".join(new_parts)

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
            if standardize_file(os.path.join(r, f)):
                count += 1
print(f'Standardized {count} files.')
