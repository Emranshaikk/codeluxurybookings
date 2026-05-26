import os
import re

MASTER_HEADER = """<!-- ELB_NAV_START -->
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

MASTER_STYLE = """        /* --- ELITE NAV & TICKER STANDARDIZATION --- */
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

def standardize_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    modified = False

    # 1. Ensure MASTER_STYLE block is correct in the <head>
    # We look for either old or new nav ticker block and replace it, or inject if missing
    style_pattern = re.compile(
        r'/\*\s*---\s*(?:ELITE NAV & TICKER|ELITE MOBILE NAV)\s*STANDARDIZATION\s*---\s*\*/.*?/\*\s*---\s*END\s+(?:ELITE NAV & TICKER|ELITE MOBILE NAV)\s*---\s*\*/',
        re.DOTALL
    )
    
    if style_pattern.search(content):
        new_content = style_pattern.sub(MASTER_STYLE.strip(), content)
        if new_content != content:
            content = new_content
            modified = True
    else:
        # If missing completely, inject into </style>
        if "ELITE NAV & TICKER STANDARDIZATION" not in content and "</style>" in content:
            content = content.replace("</style>", MASTER_STYLE + "\n    </style>")
            modified = True

    # Clean loose custom body styling with hardcoded padding-top
    body_pattern = re.compile(r'body\s*\{\s*[^}]*padding-top:\s*(?:110px|108px|72px)\s*!important\s*;?\s*\}', re.DOTALL)
    if body_pattern.search(content):
        content = body_pattern.sub('', content)
        modified = True

    # 2. Standardize Header HTML
    # Check if ELB_NAV comments exist
    start_tag = '<!-- ELB_NAV_START -->'
    end_tag = '<!-- ELB_NAV_END -->'
    
    start_idx = content.find(start_tag)
    end_idx = content.find(end_tag)
    
    if start_idx != -1 and end_idx != -1:
        # We replace the whole block from start_idx to end_idx + len(end_tag)
        full_end_idx = end_idx + len(end_tag)
        original_block = content[start_idx:full_end_idx]
        
        # Let's remove any loose top-intel-bar IMMEDIATELY before or around the block to be safe
        # (Though they are usually inside or absent, we make sure there is no stray top-intel-bar outside)
        before_content = content[:start_idx]
        after_content = content[full_end_idx:]
        
        # Check if there's an outer top-intel-bar we need to clean
        intel_in_before = before_content.find('<div class="top-intel-bar">')
        if intel_in_before != -1:
            # Let's find where it ends. Normally </div>\s*</div>\s*</div>
            end_intel = before_content.find('</div>', intel_in_before)
            end_intel = before_content.find('</div>', end_intel + 6)
            end_intel = before_content.find('</div>', end_intel + 6)
            if end_intel != -1:
                before_content = before_content[:intel_in_before] + before_content[end_intel + 6:]
                modified = True
                
        if original_block != MASTER_HEADER:
            content = before_content + MASTER_HEADER + after_content
            modified = True
    else:
        # If comments are missing, we locate the <nav class="global-nav">
        nav_pattern = re.compile(r'(<nav[^>]*class="[^"]*global-nav[^"]*"[^>]*>.*?</nav>)', re.DOTALL)
        nav_match = nav_pattern.search(content)
        if nav_match:
            nav_span = nav_match.span()
            nav_start_idx = nav_span[0]
            nav_end_idx = nav_span[1]
            
            # Let's check if there is an active top-intel-bar BEFORE the nav
            # We look up to 300 chars back
            lookback_start = max(0, nav_start_idx - 500)
            lookback_content = content[lookback_start:nav_start_idx]
            
            replace_start = nav_start_idx
            intel_idx = lookback_content.find('class="top-intel-bar"')
            if intel_idx != -1:
                # The top-intel-bar starts at lookback_start + exact_offset of its opening <div
                actual_intel_offset = lookback_content.rfind('<div', 0, intel_idx)
                if actual_intel_offset != -1:
                    replace_start = lookback_start + actual_intel_offset
                    
            # Let's check if there is a mobile menu after the nav
            lookahead_end = min(len(content), nav_end_idx + 1000)
            lookahead_content = content[nav_end_idx:lookahead_end]
            
            replace_end = nav_end_idx
            mobile_idx = lookahead_content.find('id="elbMobileMenu"')
            if mobile_idx != -1:
                # The mobile menu ends at closing </div>
                # Let's find the closing div of this mobile menu
                close_div = lookahead_content.find('</div>', mobile_idx)
                if close_div != -1:
                    replace_end = nav_end_idx + close_div + 6
                    
            # Replace the entire spans from replace_start to replace_end
            original_block = content[replace_start:replace_end]
            if original_block != MASTER_HEADER:
                content = content[:replace_start] + MASTER_HEADER + content[replace_end:]
                modified = True

    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    html_files = [f for f in os.listdir('.') if f.endswith('.html') and not f.startswith('_') and f != 'old_blog.html']
    html_files.sort()
    
    repaired_count = 0
    for filename in html_files:
        if standardize_file(filename):
            print(f"Standardized header & navigation menu on: {filename}")
            repaired_count += 1
            
    print(f"\nSuccessfully standard-locked header navigation on {repaired_count} files!")

if __name__ == '__main__':
    main()
