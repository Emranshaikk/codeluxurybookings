import os

pages_data = {
    'last-minute-yacht-charter.html': 'Last Minute Yacht Charter',
    'all-inclusive-yacht-charter.html': 'All-Inclusive Yacht Charter',
    'yacht-charter-available-now.html': 'Yacht Charter Available Now',
    'yacht-charter-with-crew.html': 'Yacht Charter with Crew'
}

authority_hub_html = """
        <section style="padding: 8rem 0; border-top: 1px solid rgba(255,255,255,0.05);">
            <div class="container">
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 4rem;">
                    <div>
                        <h2 style="border: none; font-size: 2rem;" class="serif">Yachting <span class="gold-text">Authority Hub</span></h2>
                        <p style="color: var(--text-muted); margin-bottom: 2rem;">Elite Luxury Bookings maintains global maritime authority. Explore our pillar guides for deeper strategic intelligence.</p>
                        <ul style="list-style: none; padding: 0;">
                            <li style="margin-bottom: 1.2rem;"><a href="https://eliteluxurybookings.com/motor-yacht-vs-sailing-yacht-charter/" style="color: #d4af37; text-decoration: none; font-weight: 600;">⚓ Motor vs Sailing Yacht Comparison</a></li>
                            <li style="margin-bottom: 1.2rem;"><a href="https://eliteluxurybookings.com/how-to-rent-superyacht-guide/" style="color: #d4af37; text-decoration: none; font-weight: 600;">📜 Master Superyacht Rental Guide</a></li>
                            <li style="margin-bottom: 1.2rem;"><a href="https://eliteluxurybookings.com/yacht-charter-apa-guide/" style="color: #d4af37; text-decoration: none; font-weight: 600;">💰 APA & Financial Protocol Guide</a></li>
                            <li style="margin-bottom: 1.2rem;"><a href="https://eliteluxurybookings.com/luxury-yacht-rentals/" style="color: #d4af37; text-decoration: none; font-weight: 600;">🚢 View Global Charter Fleet</a></li>
                        </ul>
                    </div>
                    <div>
                         <h2 style="border: none; font-size: 2rem;" class="serif">Elite <span class="gold-text">Intelligence</span></h2>
                        <p style="color: var(--text-muted); margin-bottom: 2rem;">Our multi-modal concierge covers maritime, aviation, and exclusive estates. Navigate the full ecosystem below.</p>
                        <ul style="list-style: none; padding: 0;">
                            <li style="margin-bottom: 1rem;"><a href="https://eliteluxurybookings.com/elite-private-jet-charter/" style="color: #d4af37; text-decoration: none; font-weight: 600;">✈️ Private Jet Charters</a></li>
                            <li style="margin-bottom: 1rem;"><a href="https://eliteluxurybookings.com/luxury-villa-rentals/" style="color: #d4af37; text-decoration: none; font-weight: 600;">🏡 Exclusive Villa Rentals</a></li>
                            <li style="margin-bottom: 1rem;"><a href="https://eliteluxurybookings.com/blog/" style="color: #d4af37; text-decoration: none; font-weight: 600;">📰 Global Intelligence Blog</a></li>
                        </ul>
                    </div>
                </div>
            </div>
        </section>
"""

root_dir = r"c:\Users\imran\OneDrive\Desktop\ELB code"

for filename, title in pages_data.items():
    filepath = os.path.join(root_dir, filename)
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        continue
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Check if breadcrumbs are already injected
    if "<!-- BREADCRUMBS -->" in content:
        print(f"Breadcrumbs already exist in {filename}")
    else:
        breadcrumbs_html = f"""
    <!-- BREADCRUMBS -->
    <div class="container" style="padding: 2rem 0; font-size: 0.8rem; color: rgba(255,255,255,0.4); text-transform: uppercase; letter-spacing: 1px;">
        <a href="https://eliteluxurybookings.com/" style="color: #d4af37; text-decoration: none;">Home</a> / 
        <a href="https://eliteluxurybookings.com/luxury-yacht-rentals/" style="color: #d4af37; text-decoration: none;">Luxury Yachts</a> / 
        <span style="color: rgba(255,255,255,0.6);">{title}</span>
    </div>
"""
        # Inject breadcrumbs after <!-- ELB_NAV_END -->
        if "<!-- ELB_NAV_END -->" in content:
            content = content.replace("<!-- ELB_NAV_END -->", "<!-- ELB_NAV_END -->\n" + breadcrumbs_html)
            print(f"Injected Breadcrumbs into {filename}")
        else:
            print(f"Warning: <!-- ELB_NAV_END --> not found in {filename}")
            
    # Check if Yachting Authority Hub is already injected
    if "Yachting Authority Hub" in content:
        print(f"Authority Hub already exists in {filename}")
    else:
        # Inject before <!-- Master Footer -->
        if "<!-- Master Footer -->" in content:
            content = content.replace("<!-- Master Footer -->", authority_hub_html + "\n    <!-- Master Footer -->")
            print(f"Injected Yachting Authority Hub into {filename}")
        else:
            print(f"Warning: <!-- Master Footer --> not found in {filename}")
            
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Done processing.")
