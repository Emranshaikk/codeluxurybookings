import os

ROOT_DIR = r'c:\Users\imran\OneDrive\Desktop\ELB code'

for root, d, files in os.walk(ROOT_DIR):
    for f in files:
        if f == 'index.html':
            p = os.path.join(root, f)
            try:
                with open(p, 'r', encoding='utf-8') as file:
                    c = file.read()
                    
                changed = False
                
                # 1. Remove unicode dropdown arrow
                if r"\u25be" in c:
                    c = c.replace(r"\u25be", "")
                    changed = True
                    
                # 2. Fix the broken hyphen in the slot alert if it exists
                if r"â€“" in c:
                    c = c.replace(r"â€“", "-")
                    changed = True
                    
                # 3. Capitalize specific city names that were lowercase in silos
                lower_cities = {'newyork': 'New York', 'losangeles': 'Los Angeles', 'lasvegas': 'Las Vegas', 'abudhabi': 'Abu Dhabi', 'tokyo': 'Tokyo', 'hongkong': 'Hong Kong'}
                for lc, cap in lower_cities.items():
                    # Only replace in <title> and <h1> to avoid breaking URLs
                    if f'title>Private Jet cost (Bookings + {lc} to' in c:
                        c = c.replace(f'title>Private Jet cost (Bookings + {lc} to', f'title>Private Jet Cost (Bookings + {cap} to')
                        changed = True
                    if f'title>Private Jet cost (Bookings + ' in c and f' to {lc} Flight' in c:
                        c = c.replace(f' to {lc} Flight', f' to {cap} Flight')
                        changed = True
                    if f'<h1>Private Jet Cost (Bookings + {lc} to' in c:
                        c = c.replace(f'<h1>Private Jet Cost (Bookings + {lc} to', f'<h1>Private Jet Cost (Bookings + {cap} to')
                        changed = True
                    if f' to {lc} Flight Cost Breakdown' in c:
                        c = c.replace(f' to {lc} Flight Cost Breakdown', f' to {cap} Flight Cost Breakdown')
                        changed = True

                # Align Whatsapp button
                # In navigation: .mobile-cta { margin-top:1rem; text-align:center; background:linear-gradient... }
                # Let's just make it center and fix padding
                if '.mobile-cta { margin-top:1rem;' in c and 'padding:1.2rem !important;' not in c:
                    c = c.replace(
                        '.mobile-cta { margin-top:1rem; text-align:center; background:linear-gradient(135deg,#D4AF37,#B8860B); color:#000 !important; border-radius:8px; padding:1rem; font-weight:600; letter-spacing:2px; border-bottom:none !important; }',
                        '.mobile-cta { margin-top:2rem; text-align:center; background:linear-gradient(135deg,#D4AF37,#B8860B); color:#000 !important; border-radius:8px; padding:1.2rem !important; font-weight:700; border-bottom:none !important; }'
                    )
                    changed = True

                # Fix blog links
                # In the navigation, ensure blog links to /blog/index.html instead of /blog/ if they prefer, actually /blog/ works perfectly now that we regenerated it
                
                if changed:
                    with open(p, 'w', encoding='utf-8') as file:
                        file.write(c)
                        
            except Exception as e:
                pass

print("Standardizations applied.")
