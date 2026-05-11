import os
import re

def fix_nav_and_schema():
    root_dir = r'c:\Users\imran\OneDrive\Desktop\ELB code'
    
    # 1. NAVIGATION BLOCK
    nav_block = """
    <div class="top-intel-bar">
        <div class="ticker-wrap">
            <div class="ticker-content">
                <strong>⚠️ Intelligence Alert:</strong> Strategic Procurement Windows Open for Summer 2026. 
                <strong>Empty Leg Flights Available:</strong> <a href="https://wa.me/918801079030">Connect for Instant Procurement</a>
                <strong>⚠️ Global Inventory Update:</strong> Off-Market Assets Now Accessible via Elite Concierge.
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
                <li><a href="https://eliteluxurybookings.com/blog/">Blog</a></li>
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
"""

    # 2. SCHEMA BLOCK
    schema_block = """
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "Organization",
      "name": "Elite Luxury Bookings",
      "url": "https://eliteluxurybookings.com",
      "logo": "https://eliteluxurybookings.com/favicon.png",
      "contactPoint": {
        "@type": "ContactPoint",
        "telephone": "+918801079030",
        "contactType": "Concierge Customer Service",
        "availableLanguage": "English"
      }
    }
    </script>
"""

    # Files needing NAV
    nav_files = [
        'dubai-private-jet-routes.html',
        'losangeles-private-jet-routes.html',
        'newyork-private-jet-routes.html',
        'paris-private-jet-routes.html',
        'request-quote.html'
    ]

    # Files needing SCHEMA
    schema_files = [
        'about.html',
        'business-jet-charter-guide-tips-pricing.html',
        'luxury-experience-of-flying-private.html',
        'privacy.html',
        'terms.html'
    ]

    for filename in nav_files:
        filepath = os.path.join(root_dir, filename)
        if not os.path.exists(filepath): continue
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace the placeholder or inject after <body>
        placeholder = "<!-- [ELB Global Nav Here] -->"
        if placeholder in content:
            content = content.replace(placeholder, nav_block)
            print(f"Replaced placeholder nav in {filename}")
        elif '<body>' in content:
            content = content.replace('<body>', '<body>' + nav_block)
            print(f"Injected nav into {filename}")
            
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

    for filename in schema_files:
        filepath = os.path.join(root_dir, filename)
        if not os.path.exists(filepath): continue
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if 'application/ld+json' not in content:
            if '</head>' in content:
                content = content.replace('</head>', schema_block + '</head>')
                print(f"Added Schema to {filename}")
                
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

if __name__ == "__main__":
    fix_nav_and_schema()
