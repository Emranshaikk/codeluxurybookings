import os
import re

def fix_style_links():
    root_dir = r"c:\Users\imran\OneDrive\Desktop\ELB code"
    
    # 1. Fix style links in guide-to-mediterranean-yacht-charter.html, london-to-ibiza-private-jet-cost-guide.html, old_blog.html
    style_link = '    <link rel="stylesheet" href="/style.css">\n'
    for fn in ["guide-to-mediterranean-yacht-charter.html", "london-to-ibiza-private-jet-cost-guide.html", "old_blog.html"]:
        path = os.path.join(root_dir, fn)
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            if 'style.css' not in content:
                # Insert before </head>
                content = content.replace('</head>', style_link + '</head>', 1)
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Fixed: Added style.css link to {fn}")
                
    # 2. Fix mallorca-to-ibiza-private-boat.html double footer
    boat_path = os.path.join(root_dir, "mallorca-to-ibiza-private-boat.html")
    if os.path.exists(boat_path):
        with open(boat_path, 'r', encoding='utf-8') as f:
            content = f.read()
        parts = content.split('</html>')
        if len(parts) > 2:
            new_content = parts[0] + '</html>\n'
            # Check line 838 fix as well
            if 'margin-b      <div' in new_content:
                new_content = new_content.replace(
                    'margin-b      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 2rem;">',
                    'margin-bottom: 3rem;">Related Intelligence</h2>\n      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 2rem;">'
                )
            with open(boat_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print("Fixed: Cleaned up double footer and restored malformed tag in mallorca-to-ibiza-private-boat.html")

    # 3. Fix business-jet-charter-guide-tips-pricing.html missing mobile menu
    pricing_path = os.path.join(root_dir, "business-jet-charter-guide-tips-pricing.html")
    if os.path.exists(pricing_path):
        with open(pricing_path, 'r', encoding='utf-8') as f:
            content = f.read()
        if 'id="elbMobileMenu"' not in content:
            mobile_menu = """    <div class="mobile-menu" id="elbMobileMenu">
        <a href="https://eliteluxurybookings.com/elite-private-jet-charter/">✈ Private Jets</a>
        <a href="https://eliteluxurybookings.com/luxury-villa-rentals/">🏡 Luxury Villas</a>
        <a href="https://eliteluxurybookings.com/luxury-yacht-rentals/">⚓ Luxury Yachts</a>
        <a href="https://eliteluxurybookings.com/blog/">📰 Blog</a>
        <a href="https://eliteluxurybookings.com/contact/">📞 Contact</a>
    </div>"""
            # Insert right after </nav>
            content = content.replace('</nav>', '</nav>\n' + mobile_menu, 1)
            with open(pricing_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print("Fixed: Injected mobile menu into business-jet-charter-guide-tips-pricing.html")

    # 4. Fix thank-you.html missing navigation and mobile menu
    thank_path = os.path.join(root_dir, "thank-you.html")
    if os.path.exists(thank_path):
        with open(thank_path, 'r', encoding='utf-8') as f:
            content = f.read()
        if '<nav class="global-nav">' not in content:
            nav_block = """    <!-- ELB_NAV_START -->
<div class="top-intel-bar">
    <div class="ticker-wrap">
        <div class="ticker-content">
            <strong>⚠️ Intelligence Alert:</strong> Strategic Procurement Windows Open for Summer 2026. <strong>Empty Leg Flights Available:</strong> <a href="https://wa.me/918801079030">Connect for Instant Procurement</a> <strong>⚠️ Global Inventory Update:</strong> Off-Market Assets Now Accessible via Elite Concierge.
        </div>
    </div>
</div>

<nav class="global-nav">
    <div class="container global-nav-inner">
        <a href="https://eliteluxurybookings.com/" class="nav-brand">Elite Luxury <span class="nav-gold">Bookings</span></a>
        <ul class="nav-links">
            <li><a href="https://eliteluxurybookings.com/elite-private-jet-charter/">Private Jets</a></li>
            <li><a href="https://eliteluxurybookings.com/luxury-yacht-rentals/">Yachts</a></li>
            <li><a href="https://eliteluxurybookings.com/luxury-villa-rentals/">Villas</a></li>
            <li><a href="https://eliteluxurybookings.com/blog/" style="color: rgba(255, 255, 255, 0.85); text-decoration:none; font-size:0.9rem; transition:color 0.3s;" onmouseover="this.style.color='#D4AF37'" onmouseout="this.style.color='rgba(255, 255, 255, 0.85)'">Blog</a></li>
            <li><a href="https://eliteluxurybookings.com/contact/" style="color: rgba(255, 255, 255, 0.85); text-decoration:none; font-size:0.9rem; transition:color 0.3s;" onmouseover="this.style.color='#D4AF37'" onmouseout="this.style.color='rgba(255, 255, 255, 0.85)'">Contact</a></li>
        </ul>
        <div class="nav-hamburger" id="navHamburger" onclick="toggleMobileMenu()">
            <span></span><span></span><span></span>
        </div>
    </div>
</nav>
<div class="mobile-menu" id="elbMobileMenu">
    <a href="https://eliteluxurybookings.com/elite-private-jet-charter/">✈ Private Jets</a>
    <a href="https://eliteluxurybookings.com/luxury-villa-rentals/">🏡 Luxury Villas</a>
    <a href="https://eliteluxurybookings.com/luxury-yacht-rentals/">⚓ Luxury Yachts</a>
    <a href="https://eliteluxurybookings.com/blog/">📰 Blog</a>
    <a href="https://eliteluxurybookings.com/contact/">📞 Contact</a>
</div>
<!-- ELB_NAV_END -->"""
            # Insert right after <body>
            content = content.replace('<body>', '<body>\n' + nav_block, 1)
            with open(thank_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print("Fixed: Injected navigation and mobile menu into thank-you.html")

    # 5. Fix private-jet-charter-cost-estimator.html outdated footer
    estimator_path = os.path.join(root_dir, "private-jet-charter-cost-estimator.html")
    if os.path.exists(estimator_path):
        with open(estimator_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        standard_footer = """<footer class="footer">
        <div class="container" style="max-width: 1200px;">
            <div class="footer-grid">
                <div class="footer-brand">
                    <h2>Elite Luxury <span class="gold-text">Bookings</span></h2>
                    <p>Curating world-class luxury experiences through our global partner network. Private Jets. Yachts. Villas.</p>
                    <div class="footer-socials">
                        <a href="https://www.facebook.com/eliteluxurybookings"><i class="fab fa-facebook"></i></a>
                        <a href="https://www.instagram.com/eliteluxurybookings"><i class="fab fa-instagram"></i></a>
                        <a href="https://www.linkedin.com/company/elite-luxury-bookings/"><i class="fab fa-linkedin"></i></a>
                        <a href="https://x.com/eliteluxuryb"><i class="fab fa-x-twitter"></i></a>
                    </div>
                </div>
                <div class="footer-col">
                    <h4>SERVICES</h4>
                    <ul>
                        <li><a href="https://eliteluxurybookings.com/elite-private-jet-charter/">Private Jets</a></li>
                        <li><a href="https://eliteluxurybookings.com/luxury-yacht-rentals/">Luxury Yachts</a></li>
                        <li><a href="https://eliteluxurybookings.com/luxury-villa-rentals/">Luxury Villas</a></li>
                        <li><a href="https://eliteluxurybookings.com/global-route-silo/">Route Directory</a></li>
                        <li><a href="https://eliteluxurybookings.com/blog/">Blog</a></li>
                    </ul>
                </div>
                <div class="footer-col">
                    <h4>AUTHORITY</h4>
                    <ul>
                        <li><a href="https://eliteluxurybookings.com/about/">The Mission</a></li>
                        <li><a href="https://eliteluxurybookings.com/privacy/">Privacy Protocol</a></li>
                        <li><a href="https://eliteluxurybookings.com/terms/">Terms of Engagement</a></li>
                        <li><a href="https://eliteluxurybookings.com/contact/">Connect</a></li>
                    </ul>
                </div>
            </div>
            
            <!-- AVIATION AUTHORITY SILO -->
            <div style="max-width: 1200px; margin: 2rem auto 0; padding: 2rem 0 0; border-top: 1px solid rgba(212,175,55,0.1); text-align: center;">
                <h4 class="serif gold-text" style="font-size: 1.4rem; margin-bottom: 1.5rem; letter-spacing: 2px;">Aviation Authority Silo</h4>
                <div style="display: flex; justify-content: center; gap: 1.5rem; flex-wrap: wrap; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px;">
                    <a href="https://eliteluxurybookings.com/private-jet-charter-cost-estimator/" style="color: rgba(255,255,255,0.6); text-decoration: none; transition: 0.3s;" onmouseover="this.style.color='#D4AF37'" onmouseout="this.style.color='rgba(255,255,255,0.6)'">Jet Cost Estimator</a>
                    <a href="https://eliteluxurybookings.com/heavy-jet-vs-light-jet-charter/" style="color: rgba(255,255,255,0.6); text-decoration: none; transition: 0.3s;" onmouseover="this.style.color='#D4AF37'" onmouseout="this.style.color='rgba(255,255,255,0.6)'">Jet Class Analysis</a>
                    <a href="https://eliteluxurybookings.com/empty-leg-flights-guide/" style="color: rgba(255,255,255,0.6); text-decoration: none; transition: 0.3s;" onmouseover="this.style.color='#D4AF37'" onmouseout="this.style.color='rgba(255,255,255,0.6)'">Empty Leg Mastery</a>
                    <a href="https://eliteluxurybookings.com/elite-private-jet-charter/" style="color: rgba(255,255,255,0.6); text-decoration: none; transition: 0.3s;" onmouseover="this.style.color='#D4AF37'" onmouseout="this.style.color='rgba(255,255,255,0.6)'">View Global Fleet</a>
                </div>
            </div>
            <!-- END AVIATION AUTHORITY SILO -->
            
            <div class="footer-bottom">
                <p>&copy; 2026 Elite Luxury Bookings. All rights reserved. Global Authority in Luxury Procurement.</p>
                <div class="footer-legal">
                    <a href="https://eliteluxurybookings.com/privacy/">Privacy</a>
                    <a href="https://eliteluxurybookings.com/terms/">Terms</a>
                </div>
            </div>
        </div>
    </footer>"""
        
        # Locate the <footer class="footer">...</footer> block and replace it
        new_content = re.sub(r'<footer class="footer">.*?</footer>', standard_footer, content, flags=re.DOTALL)
        with open(estimator_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("Fixed: Replaced outdated footer with standard footer in private-jet-charter-cost-estimator.html")

    # 6. Fix old_blog.html missing links
    old_blog_path = os.path.join(root_dir, "old_blog.html")
    if os.path.exists(old_blog_path):
        with open(old_blog_path, 'r', encoding='utf-8') as f:
            content = f.read()
        if 'Contact' not in content:
            # Let's add contact link to the nav links list
            content = content.replace(
                '<li><a href="https://eliteluxurybookings.com/blog/"',
                '<li><a href="https://eliteluxurybookings.com/blog/" style="color: rgba(255, 255, 255, 0.85); text-decoration:none; font-size:0.9rem; transition:color 0.3s;" onmouseover="this.style.color=\'#D4AF37\'" onmouseout="this.style.color=\'rgba(255, 255, 255, 0.85)\'">Blog</a></li>\n                <li><a href="https://eliteluxurybookings.com/contact/" style="color: rgba(255, 255, 255, 0.85); text-decoration:none; font-size:0.9rem; transition:color 0.3s;" onmouseover="this.style.color=\'#D4AF37\'" onmouseout="this.style.color=\'rgba(255, 255, 255, 0.85)\'">Contact</a></li><!--'
            )
            with open(old_blog_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print("Fixed: Restored contact navigation link in old_blog.html")

if __name__ == '__main__':
    fix_style_links()
