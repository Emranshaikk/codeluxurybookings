"""
Fix missing og:title tags on pages that have other OG tags but no og:title
"""
import os, re

MISSING_OG_TITLE = [
    'about.html',
    'business-jet-charter-guide-tips-pricing.html',
    'catamaran-vs-monohull-comparison.html',
    'empty-leg-flights-guide.html',
    'flying-pets-on-private-jets.html',
    'heavy-jet-vs-light-jet-charter.html',
    'how-to-book-luxury-villa-guide.html',
    'how-to-rent-superyacht-guide.html',
    'luxury-villa-rentals.html',
    'luxury-yacht-rentals.html',
    'multi-modal-luxury-itinerary-2026.html',
    'privacy.html',
    'private-boat-trip-mallorca-to-formentera.html',
    'private-jet-charter-cost-estimator.html',
    'private-jet-to-maldives-bora-bora.html',
    'terms.html',
    'ultimate-luxury-villa-rental-guide-2026.html',
    'villa-vs-luxury-hotel-comparison.html',
    'yacht-charter-apa-guide.html',
]

BASE_URL = "https://eliteluxurybookings.com"
DEFAULT_OG_IMAGE = f"{BASE_URL}/assets/elite_jet_master_hero.png"

fixed = 0
for filename in MISSING_OG_TITLE:
    if not os.path.exists(filename):
        print(f"  SKIP (not found): {filename}")
        continue

    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract title
    title_match = re.search(r'<title>(.*?)</title>', content, re.DOTALL)
    title = title_match.group(1).strip().replace('\n', ' ').replace('  ', ' ') if title_match else "Elite Luxury Bookings"

    # Extract description
    desc_match = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']+)["\']', content)
    if not desc_match:
        desc_match = re.search(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+name=["\']description["\']', content)
    desc = desc_match.group(1)[:200] if desc_match else "Elite Luxury Bookings - World-class private jet, yacht, and villa experiences."

    # Derive canonical URL
    slug = filename.replace('.html', '')
    canonical_url = f"{BASE_URL}/{slug}/" if slug != 'index' else f"{BASE_URL}/"

    og_block = f"""    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{desc}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{canonical_url}">
    <meta property="og:image" content="{DEFAULT_OG_IMAGE}">
    <meta property="og:site_name" content="Elite Luxury Bookings">"""

    # Check if we already have some OG tags and just need og:title
    if 'og:url' in content or 'og:description' in content:
        # Just add og:title before the first og: meta
        content = re.sub(
            r'(<meta property="og:)',
            f'<meta property="og:title" content="{title}">\n    \\1',
            content,
            count=1
        )
    else:
        # Insert full OG block before </head>
        content = content.replace('</head>', f'{og_block}\n</head>', 1)

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    fixed += 1
    print(f"  Fixed OG tags: {filename}")

print(f"\nTotal fixed: {fixed} files")
