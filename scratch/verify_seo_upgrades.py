import os
import re
import sys
from bs4 import BeautifulSoup

# Ensure stdout uses UTF-8
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

workspace_dir = r"c:\Users\imran\OneDrive\Desktop\ELB code"

expected = {
    "index.html": {
        "title": "Private Jet, Yacht & Villa Charter | From $4,500/hr",
        "desc": "Book private jets from $4,500/hr, yacht charters from $15,000/week, and luxury villas from $5,000/night with our 24/7 global concierge. Request a quote."
    },
    "about.html": {
        "title": "About Elite Luxury Bookings | Vetted Global Concierge",
        "desc": "We coordinate private jet charters, luxury yacht rentals, and elite villa bookings across 40+ countries with NDA-level client discretion. Meet our team."
    },
    "contact.html": {
        "title": "Contact Elite Luxury Bookings | 24/7 Concierge Desk",
        "desc": "Reach our concierge desk by WhatsApp or email for private jet, luxury yacht, or villa bookings. Available 24/7 worldwide for fast responses. Book now."
    },
    "luxury-villa-rentals.html": {
        "title": "Luxury Villa Rentals from $5,000/Night | Vetted Estates",
        "desc": "Rent fully staffed beachfront villas, mountain chalets, and private estates from $5,000/night. Access off-market luxury properties worldwide. Book now."
    },
    "sunreef-catamaran-charter-price.html": {
        "title": "Sunreef Catamaran Charter Price | From $45,000/Week",
        "desc": "Learn the true Sunreef catamaran charter price. Compare weekly rates from $45,000 for Sunreef 60 to 100, and calculate APA or crew costs. Compare options."
    },
    "elite-private-jet-charter.html": {
        "title": "Private Jet Charter from $4,500/hr | Vetted Operators",
        "desc": "Charter light, midsize, and heavy private jets from $4,500/hr. Access empty leg flight deals with 24/7 global support and full NDA privacy. Get a quote."
    },
    "luxury-yacht-rentals.html": {
        "title": "Luxury Yacht Charter from $15,000/Week | Global Fleet",
        "desc": "Rent motor yachts, sailing yachts, and catamarans from $15,000/week. Vetted crews and custom itineraries in the Mediterranean and Bahamas. Get a quote."
    },
    "blog.html": {
        "title": "Luxury Jets, Yachts & Villas Blog | Elite Luxury Bookings",
        "desc": "Expert insights, route guides, and pricing intel for private jet charter, luxury yacht rental, and elite villa bookings. Compare luxury travel options."
    },
    "7-best-private-jet-charter-in-dubai.html": {
        "title": "7 Best Private Jet Charter Options in Dubai | From $3,500/hr",
        "desc": "Compare the top 7 private jet charter options in Dubai. Explore hourly rates from $3,500/hr, airport options, empty legs, and booking tips. Request a quote."
    },
    "private-boat-trip-mallorca-to-formentera.html": {
        "title": "Boat Charter Mallorca to Formentera | From €2,500/Day",
        "desc": "Skip the crowded ferry. Vetted private boat charters from Mallorca to Formentera from €2,500/day. Discover top routes, beach clubs & coves. Request a quote."
    },
    "mallorca-to-ibiza-private-boat.html": {
        "title": "Boat Charter Mallorca to Ibiza from €800/Day | Vetted Fleet",
        "desc": "Skip the crowded ferry. Rent a private boat from Mallorca to Ibiza from €800/day. Explore elite charters, return sailing wind warnings & ports. Request a quote."
    },
    "amalfi-coast-yacht-rental.html": {
        "title": "7 Best Amalfi Coast Yacht Rental Deals | Vetted Boats",
        "desc": "Discover the best Amalfi Coast yacht rental options. Explore top routes (Capri, Positano), boat types, pricing tables, and booking strategies. Get a quote."
    },
    "hongkong-to-singapore-private-jet-cost.html": {
        "title": "Hongkong to Singapore Private Jet Cost | Rates from $13,500",
        "desc": "Hongkong to Singapore private jet cost from $13,500 USD (3h 50m). Compare rates across Light, Midsize & Heavy jets between HKBAC and Seletar. Get a quote."
    },
    "multi-modal-luxury-itinerary.html": {
        "title": "Multi-Modal Luxury Travel Integration | Vetted Guide",
        "desc": "Discover the art of the multi-modal luxury itinerary. Learn how to seamlessly integrate private jet travel, superyacht charters, and villa stays. Get a quote."
    },
    "solar-eclipse-balearic-islands-private-yacht.html": {
        "title": "Solar Eclipse in Balearic Islands Private Yacht | ELB",
        "desc": "Secure a private yacht charter in the Balearic Islands for the upcoming solar eclipse. Bypass land obstructions for a mobile sunset view. Request a quote."
    },
    "ultimate-luxury-villa-rental-guide.html": {
        "title": "Luxury Villa Rental Guide: Vetted Private Estates | ELB",
        "desc": "The definitive guide to luxury villa rentals. Expert insights on privacy benchmarks, staffed estates, and security protocols for guests. Request a quote."
    }
}

print("Running SEO validation suite...")
print("=" * 80)

failures = 0
for fn, expected_meta in expected.items():
    path = os.path.join(workspace_dir, fn)
    if not os.path.exists(path):
        print(f"[FAIL] File not found: {fn}")
        failures += 1
        continue
        
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()
        
    soup = BeautifulSoup(html, 'html.parser')
    
    title = soup.title.string.strip() if soup.title else ""
    
    desc_tag = soup.find('meta', attrs={'name': 'description'}) or soup.find('meta', attrs={'property': 'og:description'})
    desc = desc_tag.get('content', '').strip() if desc_tag else ""
    
    # 1. Title verification
    title_len = len(title)
    expected_title = expected_meta["title"]
    if title != expected_title:
        print(f"[FAIL] {fn} title mismatch:")
        print(f"  Got:  '{title}'")
        print(f"  Want: '{expected_title}'")
        failures += 1
    elif not (50 <= title_len <= 60):
        print(f"[FAIL] {fn} title length of {title_len} is outside 50-60 characters!")
        failures += 1
    else:
        print(f"[PASS] {fn} title: '{title}' ({title_len} chars)")
        
    # 2. Description verification
    desc_len = len(desc)
    expected_desc = expected_meta["desc"]
    if desc != expected_desc:
        print(f"[FAIL] {fn} description mismatch:")
        print(f"  Got:  '{desc}'")
        print(f"  Want: '{expected_desc}'")
        failures += 1
    elif not (150 <= desc_len <= 160):
        print(f"[FAIL] {fn} description length of {desc_len} is outside 150-160 characters!")
        failures += 1
    else:
        print(f"[PASS] {fn} description: '{desc}' ({desc_len} chars)")
        
    # 3. Year pattern check
    year_pattern = re.compile(r'\b(202\d)\b')
    title_years = year_pattern.findall(title)
    desc_years = year_pattern.findall(desc)
    if title_years or desc_years:
        print(f"[FAIL] {fn} contains year references: Title: {title_years} | Desc: {desc_years}")
        failures += 1
        
    # 4. Check OG and Twitter match
    og_title_tag = soup.find('meta', attrs={'property': 'og:title'})
    if og_title_tag and og_title_tag.get('content', '').strip() != expected_title:
        print(f"[WARNING] {fn} og:title does not match title tag")
        
    og_desc_tag = soup.find('meta', attrs={'property': 'og:description'})
    if og_desc_tag and og_desc_tag.get('content', '').strip() != expected_desc:
        print(f"[WARNING] {fn} og:description does not match description tag")
        
    print("-" * 80)

if failures == 0:
    print("\n[SUCCESS] All 16 files successfully passed the SEO validation suite!")
else:
    print(f"\n[FAIL] Found {failures} validation failures.")
