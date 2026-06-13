import os
import re

def apply_seo_fixes():
    root_dir = r'c:\Users\imran\OneDrive\Desktop\ELB code'
    
    # Define fixes as (filename, target_regex, replacement)
    fixes = [
        # Monaco Jet Guide
        (
            'private-jet-charter-to-monaco.html',
            r'<meta name="description" content="Book a private jet charter to Monaco in 2026\. Full guide covering Nice airport transfers, helicopter connections, Grand Prix slots, fleet selection, and pricing\. Expert Monaco jet hire from EliteLuxuryBookings\.com\.">',
            '<meta name="description" content="Book a private jet to Monaco in 2026. Full guide on Nice transfers, helicopter links, Grand Prix slots, and pricing. Elite procurement by Elite Luxury Bookings.">'
        ),
        # Villa Guide 2026
        (
            'ultimate-luxury-villa-rental-guide.html',
            r'<meta name="description"\s+content="The definitive guide to luxury villa rentals in 2026\. Learn about privacy benchmarks, full-staffed estates, security protocols, and the world\'s most exclusive destinations\.">',
            '<meta name="description" content="The definitive 2026 guide to luxury villa rentals. Expert insights on privacy benchmarks, staffed estates, and security protocols for the discerning traveler.">'
        ),
        # Route Page: Amsterdam to London (Example of meta cleanup)
        (
            'amsterdam-to-london-private-jet-cost.html',
            r'<meta name="description" content="Book a private jet charter from Amsterdam to London\. 2026 pricing guide covering light jets, midsize aircraft, and heavy jets\. Elite procurement and mission flight support from EliteLuxuryBookings\.com\.">',
            '<meta name="description" content="Private jet charter from Amsterdam to London. 2026 pricing guide for light and heavy jets. Elite procurement and mission support by Elite Luxury Bookings.">'
        ),
        # Route Page: Ibiza to London
        (
            'ibiza-to-london-private-jet-cost.html',
            r'<meta name="description" content="Book a private jet charter from Ibiza to London\. 2026 pricing guide covering light jets, midsize aircraft, and heavy jets\. Elite procurement and mission flight support from EliteLuxuryBookings\.com\.">',
            '<meta name="description" content="Private jet charter from Ibiza to London. 2026 pricing for light and heavy jets. Elite procurement and luxury mission support by Elite Luxury Bookings.">'
        )
    ]

    for filename, pattern, replacement in fixes:
        filepath = os.path.join(root_dir, filename)
        if not os.path.exists(filepath):
            print(f"Skipping {filename} - not found")
            continue
            
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        new_content = re.sub(pattern, replacement, content)
        
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Applied SEO fix to {filename}")
        else:
            print(f"Pattern not found in {filename}")

if __name__ == "__main__":
    apply_seo_fixes()
