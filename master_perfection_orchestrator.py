import os
import re

def perfect_page(filepath, root):
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return False

    original = content
    
    # --- 1. GLOBAL DEDUPLICATIONS ---
    
    # Deduplicate Navigation
    content = re.sub(r'<!-- ELB_NAV_START -->.*?<!-- ELB_NAV_END -->', '', content, flags=re.DOTALL)
    # Re-inject single nav at the top
    ELB_NAV = """<!-- ELB_NAV_START -->
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
    
    if "<body>" in content:
        content = content.replace("<body>", f"<body>\n{ELB_NAV}")
    
    # Deduplicate Footer
    content = re.sub(r'<!-- ELB_FOOTER_START -->.*?<!-- ELB_FOOTER_END -->', '', content, flags=re.DOTALL)
    ELB_FOOTER = """<!-- ELB_FOOTER_START -->
    <footer class="section-padding" style="background: #000; border-top: 1px solid rgba(255,255,255,0.05); text-align: center !important; margin-top: 6rem; padding: 6rem 0;">
        <div class="container" style="display: block !important; text-align: center !important;">
            <a href="/" style="display: inline-block; margin-bottom: 2rem; font-family:'Cormorant Garamond',serif; font-size:2.2rem; font-weight:600; color:#fff; text-decoration:none;"><span style="color:#D4AF37;">Elite</span> Luxury Bookings</a>
            <div style="display: flex; justify-content: center; gap: 3rem; flex-wrap: wrap; margin-bottom: 2.5rem;">
                <a href="/elite-private-jet-charter/" style="color: rgba(255,255,255,0.6); text-decoration: none; font-size: 0.9rem; letter-spacing: 1.5px; text-transform: uppercase;">Aviation</a>
                <a href="/luxury-yacht-rentals/" style="color: rgba(255,255,255,0.6); text-decoration: none; font-size: 0.9rem; letter-spacing: 1.5px; text-transform: uppercase;">Maritime</a>
                <a href="/luxury-villa-rentals/" style="color: rgba(255,255,255,0.6); text-decoration: none; font-size: 0.9rem; letter-spacing: 1.5px; text-transform: uppercase;">Villas</a>
                <a href="/blog/" style="color: rgba(255,255,255,0.6); text-decoration: none; font-size: 0.9rem; letter-spacing: 1.5px; text-transform: uppercase;">Blog</a>
                <a href="/contact/" style="color: rgba(255,255,255,0.6); text-decoration: none; font-size: 0.9rem; letter-spacing: 1.5px; text-transform: uppercase;">Contact</a>
            </div>
            <p style="color: #444; font-size: 0.8rem; letter-spacing: 1px;">© 2026 Elite Luxury Bookings. Concierge Dispatch Worldwide.</p>
        </div>
    </footer>
<!-- ELB_FOOTER_END -->"""

    if "</body>" in content:
        content = content.replace("</body>", f"{ELB_FOOTER}\n</body>")

    # Deduplicate Silo Hubs (Americas, Asia, Middle East columns)
    # We target the specific pattern and keep only the first set found in a section
    content = re.sub(r'(<div class="glass-panel" style="padding: 2rem;">\s*<h3 class="serif gold-text"[^>]*>(The Americas Hub|Asia & Pacific Hub|Middle East & Islands) Hub</h3>.*?</ul>\s*</div>\s*)+', r'\1', content, flags=re.DOTALL)
    # Target simpler variants
    content = re.sub(r'(<div class="glass-panel" style="padding: 2.5rem;">\s*<h3 class="serif gold-text"[^>]*>(The Americas Hub|Asia & Pacific Hub|Middle East & Islands)</h3>.*?</ul>\s*</div>\s*)+', r'\1', content, flags=re.DOTALL)
    content = re.sub(r'(<div class="glass-panel" style="padding: 2rem;">\s*<h3 class="serif gold-text"[^>]*>(The Americas Hub|Asia & Pacific Hub|Middle East & Islands)</h3>.*?</ul>\s*</div>\s*)+', r'\1', content, flags=re.DOTALL)

    # --- 2. CATEGORICAL PERFECTION ---
    
    # VILLA PAGES
    if "villa" in root.lower() or "villa" in filepath.lower():
        # Remove all Villa Hubs
        content = re.sub(r'<!-- ELB_VILLA_LEAD_HUB_START -->.*?<!-- ELB_VILLA_LEAD_HUB_END -->', '', content, flags=re.DOTALL)
        content = re.sub(r'<!-- ELITE VILLA INQUIRY HUB -->.*?<!-- ELITE VILLA INQUIRY HUB -->', '', content, flags=re.DOTALL)
        content = re.sub(r'<section id="villa-inquiry".*?</section>', '', content, flags=re.DOTALL)
        content = re.sub(r'<div class="villa-lead-hub".*?</div>\s*</div>', '', content, flags=re.DOTALL)
        
        # Inject ONE Elite Villa Lead Hub
        VILLA_HUB = """
<!-- ELB_VILLA_LEAD_HUB_START -->
    <section id="villa-inquiry" style="padding: 100px 0; background: #050505; border-bottom: 1px solid rgba(212,175,55,0.1); position: relative;">
        <div class="container" style="max-width: 850px; margin: 0 auto; text-align: center;">
            <div style="display: inline-block; padding: 10px 20px; background: rgba(212,175,55,0.05); border: 1px solid rgba(212,175,55,0.2); border-radius: 50px; color: #D4AF37; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 3px; margin-bottom: 30px;">
                Elite Estate Concierge Desk
            </div>
            <h2 class="serif" style="font-size: 3.5rem; color: #fff; margin-bottom: 20px;">Secure Your Private Sanctuary</h2>
            <p style="color: var(--text-muted); font-size: 1.1rem; margin-bottom: 40px; max-width: 600px; margin-left: auto; margin-right: auto;">Direct off-market access to the world's most exclusive estates. Your requirements, coordinated with absolute discretion.</p>
            
            <div class="glass-panel" style="padding: 3.5rem; background: rgba(10,10,10,0.8); border: 1px solid var(--primary-gold); border-radius: 24px; box-shadow: 0 40px 100px rgba(0,0,0,0.8); text-align: left;">
                <form action="https://formspree.io/f/xwvwanlj" method="POST" style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                    <div style="grid-column: span 1;">
                        <input type="text" name="name" placeholder="Principal Name" required style="width: 100%; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.12); padding: 18px; color: #fff; border-radius: 12px;">
                    </div>
                    <div style="grid-column: span 1;">
                        <input type="email" name="email" placeholder="Priority Contact (Email)" required style="width: 100%; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.12); padding: 18px; color: #fff; border-radius: 12px;">
                    </div>
                    <div style="grid-column: span 2;">
                        <textarea name="requirements" placeholder="Preferred Destination, Dates, and Specialist Staffing Requirements..." required style="width: 100%; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.12); padding: 18px; color: #fff; border-radius: 12px; min-height: 120px;"></textarea>
                    </div>
                    <button type="submit" class="btn btn-gold" style="grid-column: span 2; font-size: 1.2rem; min-height: 75px; font-weight: 700; text-transform: uppercase; letter-spacing: 4px;">Request Exclusive Portfolio</button>
                </form>
            </div>
        </div>
    </section>
<!-- ELB_VILLA_LEAD_HUB_END -->
"""
        # Place it after Nav/Header
        if "<!-- ELB_NAV_END -->" in content:
            content = content.replace("<!-- ELB_NAV_END -->", f"<!-- ELB_NAV_END -->\n{VILLA_HUB}")
            
    # MARITIME PAGES
    elif "yacht" in root.lower() or "boat" in root.lower() or "yacht" in filepath.lower():
        # Remove all Maritime Hubs
        content = re.sub(r'<!-- ELB_MARITIME_FORM_START -->.*?<!-- ELB_MARITIME_FORM_END -->', '', content, flags=re.DOTALL)
        content = re.sub(r'<div class="maritime-lead-hub".*?</div>\s*</div>', '', content, flags=re.DOTALL)
        content = re.sub(r'<div class="maritime-lead-core".*?</div>', '', content, flags=re.DOTALL)

        # Maritime uses the Side-by-Side Hero (Correct Layout)
        # We ensure it's clean in the <header class="hero">
        # Extract title
        title_match = re.search(r'<h1>(.*?)</h1>', content)
        page_title = title_match.group(1) if title_match else "Elite Yacht Charter"
        
        MARITIME_HERO = f"""
    <header class="hero">
        <div class="container">
            <div class="tag-strip" style="margin-bottom: 2.5rem;">
                <span class="tag-item">Global Yacht Network</span>
                <span class="tag-item">Hand-Picked Fleet</span>
                <span class="tag-item">Michelin-Tier Service</span>
            </div>
            <h1 style="margin-bottom: 1.5rem;">{page_title}</h1>
            
            <div class="elite-maritime-split" style="display: flex; gap: 3rem; margin-top: 3rem; align-items: flex-start; flex-wrap: wrap; text-align: left;">
                <!-- LEFT: Partner Skyscraper -->
                <div class="maritime-partner-sidebar" style="flex: 0 0 320px; max-width: 320px; width: 100%;">
                    <div style="background: rgba(255,255,255,0.02); padding: 0.5rem; border-radius: 15px; border: 1px solid rgba(212,175,55,0.15); box-shadow: 0 20px 40px rgba(0,0,0,0.4);">
                        <a href="https://www.yachting.com/en-gb?AffiliateID=elbookings&BannerID=1729a6e6" target="_top">
                            <img src="//affiliate.yachting.com/accounts/default1/ne6ayxbkog/1729a6e6.png" alt="Elite Yacht Access" width="320" height="800" style="width:100%; height:auto; display:block; border-radius:10px;" />
                        </a>
                    </div>
                </div>
                <!-- RIGHT: Lead Hub -->
                <div class="maritime-lead-main" style="flex: 1; min-width: 350px;">
                    <div class="glass-panel" style="padding: 3rem; border: 1px solid var(--primary-gold); background: rgba(5,5,5,0.9); box-shadow: 0 30px 70px rgba(0,0,0,0.6);">
                        <h3 class="serif gold-text" style="font-size: 2.3rem; margin-bottom: 0.5rem; text-align: center;">Maritime Inquiry</h3>
                        <p style="text-align: center; color: var(--text-muted); font-size: 0.8rem; margin-bottom: 2.5rem; text-transform: uppercase; letter-spacing: 4px;">Direct Concierge Dispatch</p>
                        <form action="https://formspree.io/f/xwvwanlj" method="POST" style="display: flex; flex-direction: column; gap: 1.5rem;">
                            <input type="text" name="name" placeholder="Full Name" style="width:100%; border-radius:8px; border:1px solid rgba(255,255,255,0.12); padding:1.2rem; background:rgba(0,0,0,0.3); color:#fff;" required>
                            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                                <input type="email" name="email" placeholder="Email" style="border-radius:8px; border:1px solid rgba(255,255,255,0.12); padding:1.2rem; background:rgba(0,0,0,0.3); color:#fff;" required>
                                <input type="tel" name="phone" placeholder="WhatsApp" style="border-radius:8px; border:1px solid rgba(255,255,255,0.12); padding:1.2rem; background:rgba(0,0,0,0.3); color:#fff;" required>
                            </div>
                            <textarea name="requirements" placeholder="Preferred Destination, Yacht Category, or Specific Dates..." style="width:100%; border-radius:8px; border:1px solid rgba(255,255,255,0.12); padding:1.2rem; background:rgba(0,0,0,0.3); color:#fff; min-height:120px;" required></textarea>
                            <button type="submit" class="btn btn-gold" style="width:100%; font-size:1.2rem; min-height:75px; font-weight:700; text-transform:uppercase; letter-spacing:4px;">Request Priority Proposal</button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </header>
"""
        content = re.sub(r'<header class="hero">.*?</header>', MARITIME_HERO, content, flags=re.DOTALL)

    # --- 3. FINAL CLEANUP ---
    # Fix massive empty space / line breaks
    content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content)
    # Ensure ONE footer (already done by replacing with single string above)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    modified = 0
    for root, dirs, files in os.walk("."):
        if "assets" in root or ".git" in root: continue
        for file in files:
            if file == "index.html":
                if perfect_page(os.path.join(root, file), root):
                    modified += 1
    print(f"Master Perfection: {modified} pages sanitized and standardized.")

if __name__ == "__main__":
    main()
