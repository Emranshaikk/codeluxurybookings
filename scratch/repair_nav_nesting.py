import os
import re

def extract_ticker_content(content):
    match = re.search(r'class="ticker-content"\s*>(.*?)</div>', content, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None

def repair_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        
    modified = False
    
    # 1. Extract ticker content
    ticker_content = extract_ticker_content(content)
    if not ticker_content:
        # Fallback if ticker-content class is not formatted exactly
        # Let's search inside top-intel-bar
        m = re.search(r'class="top-intel-bar".*?<strong>(.*?)<!--', content, re.DOTALL)
        if m:
            ticker_content = "<strong>" + m.group(1).strip()
        else:
            ticker_content = "<strong>⚠️ Intelligence Alert:</strong> High Demand for Summer 2026 Mediterranean Charters. <strong>Empty Leg Flights Available:</strong> <a href=\"https://wa.me/918801079030\">Connect for Instant Procurement</a> <strong>⚠️ Global Inventory Update:</strong> Off-Market Superyachts Now Accessible via Maritime Concierge."

    # Standard clean blocks:
    clean_top_bar = f"""<div class="top-intel-bar">
    <div class="ticker-wrap">
        <div class="ticker-content">
            {ticker_content}
        </div>
    </div>
</div>"""

    clean_nav = """<!-- ELB_NAV_START -->
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

    # We want to replace the entire range from <div class="top-intel-bar"> to <!-- ELB_NAV_END -->
    # Let's find the start index of top-intel-bar and the end index of <!-- ELB_NAV_END -->
    start_tag = 'class="top-intel-bar"'
    end_tag = '<!-- ELB_NAV_END -->'
    
    start_idx = content.find(start_tag)
    end_idx = content.find(end_tag)
    
    if start_idx != -1 and end_idx != -1:
        # Find the actual <div class="top-intel-bar"> starting index
        div_start_idx = content.rfind('<div', 0, start_idx)
        if div_start_idx != -1:
            # We want to replace everything from div_start_idx to end_idx + len(end_tag)
            full_end_idx = end_idx + len(end_tag)
            original_block = content[div_start_idx:full_end_idx]
            
            new_block = clean_top_bar + "\n\n" + clean_nav
            
            if original_block != new_block:
                content = content[:div_start_idx] + new_block + content[full_end_idx:]
                modified = True
    else:
        # If the file does not have top-intel-bar but has ELB_NAV_START to ELB_NAV_END
        # Let's clean duplicate mobile menus inside that block
        nav_start = content.find('<!-- ELB_NAV_START -->')
        nav_end = content.find('<!-- ELB_NAV_END -->')
        if nav_start != -1 and nav_end != -1:
            full_end_idx = nav_end + len('<!-- ELB_NAV_END -->')
            original_block = content[nav_start:full_end_idx]
            if original_block != clean_nav:
                content = content[:nav_start] + clean_nav + content[full_end_idx:]
                modified = True

    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    mangled_files = [
        '7-best-private-jet-charter-in-dubai.html',
        '_template_blog_master.html',
        'charter-yacht-in-montenegro.html',
        'luxury-experience-of-flying-private.html',
        'mallorca-to-ibiza-private-boat.html',
        'private-boat-trip-mallorca-to-formentera.html',
        'private-jet-charter-cost-guide-2026.html',
        'private-jet-for-short-trips.html',
        'private-jet-travel-with-pet.html'
    ]
    
    repaired_count = 0
    for filename in mangled_files:
        if os.path.exists(filename):
            if repair_file(filename):
                print(f"Successfully repaired nav layout and duplicate mobile menus in: {filename}")
                repaired_count += 1
            else:
                print(f"Already correct or no changes needed in: {filename}")
        else:
            print(f"File not found: {filename}")
            
    print(f"\nRepaired {repaired_count} files.")

if __name__ == '__main__':
    main()
