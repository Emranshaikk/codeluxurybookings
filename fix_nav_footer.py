import os
import glob
import re

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
.mobile-menu { display: none; position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: #050505; padding: 72px 2rem 2rem; z-index: 100000; flex-direction: column; gap: 0.5rem; overflow-y: auto; }
.mobile-menu.open { display: flex !important; }
.mobile-menu a { color: rgba(255, 255, 255, 0.8) !important; text-decoration: none !important; font-size: 1.1rem; text-transform: uppercase; letter-spacing: 2px; padding: 1.2rem 0; border-bottom: 1px solid rgba(255, 255, 255, 0.05); }
@media (max-width: 1024px) { .nav-links { display: none !important; } .nav-hamburger { display: flex !important; } }
/* --- END ELITE MOBILE NAV --- */
"""

with open('style.css', 'r', encoding='utf-8') as f:
    css_content = f.read()

if 'ELITE MOBILE NAV STANDARDIZATION' not in css_content:
    with open('style.css', 'a', encoding='utf-8') as f:
        f.write(CSS_BLOCK)
    print("Added Elite Mobile Nav CSS to style.css")


NAV_BLOCK = """    <!-- ELB_NAV_START -->
    <nav class="global-nav">
        <div class="container global-nav-inner">
            <a href="/" class="nav-brand">Elite Luxury <span class="nav-gold">Bookings</span></a>
            <ul class="nav-links">
                <li><a href="/elite-private-jet-charter.html">Private Jets</a></li>
                <li><a href="/luxury-yacht-rentals.html">Yachts</a></li>
                <li><a href="/luxury-villa-rentals.html">Villas</a></li>
                <li><a href="/blog.html">Blog</a></li>
                <li><a href="/contact.html">Contact</a></li>
            </ul>
            <div class="nav-hamburger" id="navHamburger" onclick="toggleMobileMenu()"><span></span><span></span><span></span></div>
        </div>
    </nav>
    <div class="mobile-menu" id="elbMobileMenu">
        <a href="/elite-private-jet-charter.html">✈ Private Jets</a>
        <a href="/luxury-villa-rentals.html">🏡 Luxury Villas</a>
        <a href="/luxury-yacht-rentals.html">⚓ Luxury Yachts</a>
        <a href="/blog.html">📰 Blog</a>
        <a href="/contact.html">📞 Contact</a>
    </div>
    <!-- ELB_NAV_END -->"""

FOOTER_BLOCK = """    <!-- ELB_FOOTER_START -->
    <footer style="background:#000; border-top:1px solid rgba(255,255,255,0.05); padding:6rem 0;">
        <div class="container">
            <div style="font-family:'Cormorant Garamond', serif; font-size: 2.2rem; margin-bottom: 1.5rem; text-align: center; color: #D4AF37;">Elite Luxury Bookings</div>
            <div style="display: flex; justify-content: center; gap: 2rem; margin-bottom: 2rem; flex-wrap: wrap;">
                <a href="/elite-private-jet-charter.html" style="color: rgba(255, 255, 255, 0.7); text-decoration: none; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px; transition: 0.3s;" onmouseover="this.style.color='#D4AF37'" onmouseout="this.style.color='rgba(255,255,255,0.7)'">Private Jets</a>
                <a href="/luxury-yacht-rentals.html" style="color: rgba(255, 255, 255, 0.7); text-decoration: none; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px; transition: 0.3s;" onmouseover="this.style.color='#D4AF37'" onmouseout="this.style.color='rgba(255,255,255,0.7)'">Yachts</a>
                <a href="/luxury-villa-rentals.html" style="color: rgba(255, 255, 255, 0.7); text-decoration: none; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px; transition: 0.3s;" onmouseover="this.style.color='#D4AF37'" onmouseout="this.style.color='rgba(255,255,255,0.7)'">Villas</a>
                <a href="/blog.html" style="color: rgba(255, 255, 255, 0.7); text-decoration: none; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px; transition: 0.3s;" onmouseover="this.style.color='#D4AF37'" onmouseout="this.style.color='rgba(255,255,255,0.7)'">Blog</a>
                <a href="/contact.html" style="color: rgba(255, 255, 255, 0.7); text-decoration: none; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px; transition: 0.3s;" onmouseover="this.style.color='#D4AF37'" onmouseout="this.style.color='rgba(255,255,255,0.7)'">Contact</a>
            </div>
            <p style="color: rgba(255, 255, 255, 0.5); font-size: 0.8rem; text-align: center;">&copy; 2026 Elite Luxury Bookings. All rights reserved. Global Concierge Service.</p>
        </div>
    </footer>
    <!-- ELB_FOOTER_END -->"""

JS_BLOCK = """    <!-- ELB_JS_START -->
    <script>
        function toggleMobileMenu() {
            var m = document.getElementById('elbMobileMenu'), b = document.getElementById('navHamburger');
            if (m && b) { m.classList.toggle('open'); b.classList.toggle('open'); }
        }
    </script>
    <!-- ELB_JS_END -->"""

def process_file(filepath):
    # Do not process index.html (already perfect) or the raw template
    if 'index.html' in filepath or filepath.endswith('template_blog_master.html'):
        return
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    original = content
    
    # 1. Replace Nav
    if '<!-- ELB_NAV_START -->' in content and '<!-- ELB_NAV_END -->' in content:
        content = re.sub(r'<!-- ELB_NAV_START -->.*?<!-- ELB_NAV_END -->', NAV_BLOCK, content, flags=re.DOTALL)
    else:
        content = re.sub(r'<div class="mobile-menu".*?</div>', '', content, flags=re.DOTALL)
        content = re.sub(r'<nav class="global-nav">.*?</nav>', NAV_BLOCK, content, flags=re.DOTALL)

    # 2. Replace Footer
    if '<!-- ELB_FOOTER_START -->' in content and '<!-- ELB_FOOTER_END -->' in content:
        content = re.sub(r'<!-- ELB_FOOTER_START -->.*?<!-- ELB_FOOTER_END -->', FOOTER_BLOCK, content, flags=re.DOTALL)
    else:
        content = re.sub(r'<footer.*?>.*?</footer>', FOOTER_BLOCK, content, flags=re.DOTALL)

    # 3. Add JS toggle function if missing
    if 'toggleMobileMenu()' not in content:
        content = content.replace('</body>', f'{JS_BLOCK}\n</body>')
        
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {filepath}")

for f in glob.glob('*.html'):
    process_file(f)
