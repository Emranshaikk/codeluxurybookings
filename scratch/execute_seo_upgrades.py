import os
import re
import sys

# Ensure stdout uses UTF-8
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

workspace_dir = r"c:\Users\imran\OneDrive\Desktop\ELB code"

replacements = {
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
    
    # Scanned non-evergreen pages
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

print(f"Starting SEO updates on {len(replacements)} files...")
print("=" * 80)

def replace_meta_tag(html, key_attr, key_val, new_content):
    # Find all meta tags
    meta_tags = re.findall(r'(<meta\b[^>]*>)', html, re.I)
    
    count = 0
    for tag in meta_tags:
        # Check if key_attr="key_val" is in the tag
        attr_pattern = rf'\b{key_attr}\s*=\s*["\']{key_val}["\']'
        if re.search(attr_pattern, tag, re.I):
            # Locate content attribute
            content_match = re.search(r'\bcontent\s*=\s*(["\'])(.*?)\1', tag, re.I | re.S)
            if content_match:
                quote = content_match.group(1)
                start, end = content_match.span()
                # Construct new tag without using regex replacement engine
                new_tag = tag[:start] + f'content={quote}{new_content}{quote}' + tag[end:]
                if new_tag != tag:
                    html = html.replace(tag, new_tag)
                    count += 1
    return html, count

for fn, meta in replacements.items():
    path = os.path.join(workspace_dir, fn)
    if not os.path.exists(path):
        print(f"File not found: {fn}")
        continue
        
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()
        
    orig_html = html
    
    new_title = meta["title"]
    new_desc = meta["desc"]
    
    # 1. Replace <title>
    html, title_count = re.subn(r'<title\b[^>]*>.*?</title>', f'<title>{new_title}</title>', html, flags=re.I | re.S)
    
    # 2. Replace meta description
    html, desc_count = replace_meta_tag(html, "name", "description", new_desc)
    
    # 3. Replace og:title
    html, og_title_count = replace_meta_tag(html, "property", "og:title", new_title)
    
    # 4. Replace og:description
    html, og_desc_count = replace_meta_tag(html, "property", "og:description", new_desc)
    
    # 5. Replace twitter:title
    html, tw_title_count = replace_meta_tag(html, "name", "twitter:title", new_title)
    if tw_title_count == 0:
        html, tw_title_count = replace_meta_tag(html, "property", "twitter:title", new_title)
        
    # 6. Replace twitter:description
    html, tw_desc_count = replace_meta_tag(html, "name", "twitter:description", new_desc)
    if tw_desc_count == 0:
        html, tw_desc_count = replace_meta_tag(html, "property", "twitter:description", new_desc)
        
    if html != orig_html:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Updated {fn}:")
        print(f"  Title count: {title_count} | Description count: {desc_count}")
        print(f"  OG: {og_title_count}/{og_desc_count} | Twitter: {tw_title_count}/{tw_desc_count}")
    else:
        print(f"No changes made to {fn} (already updated or matches).")
    print("-" * 80)

print("SEO update execution completed.")
