"""
REGENERATE SITEMAP - Ensures all HTML pages are indexed
with correct priorities and today's lastmod date.
"""
import os
from datetime import date

BASE_URL = "https://eliteluxurybookings.com"
TODAY = date.today().isoformat()

# Priority map by page type
PRIORITY_MAP = {
    'index': '1.0',
    'elite-private-jet-charter': '0.95',
    'luxury-yacht-rentals': '0.95',
    'luxury-villa-rentals': '0.95',
    'blog': '0.90',
    'contact': '0.90',
    'request-quote': '0.85',
    'private-jet-booking-guide': '0.85',
    'private-jet-charter-cost-guide-2026': '0.85',
    'private-jet-charter-cost-estimator': '0.85',
    'heavy-jet-vs-light-jet-charter': '0.85',
    'empty-leg-flights-guide': '0.85',
    'cost-to-charter-superyacht-2026': '0.85',
    'ultimate-luxury-villa-rental-guide-2026': '0.85',
}

# Excluded from sitemap (non-indexable pages)
EXCLUDE = {
    '_template_blog_master', '_template_master',
    '404', 'thank-you', 'test_bot', 'global-route-silo'
}

html_files = [f.replace('.html', '') for f in os.listdir('.') 
              if f.endswith('.html') and f.replace('.html', '') not in EXCLUDE]

xml_entries = []

for slug in sorted(html_files):
    if slug == 'index':
        url = f"{BASE_URL}/"
    else:
        url = f"{BASE_URL}/{slug}/"

    # Determine priority
    priority = '0.75'
    for key, prio in PRIORITY_MAP.items():
        if slug == key:
            priority = prio
            break
    
    # Route pages (cost pages) get 0.8
    if 'private-jet-cost' in slug or 'private-boat' in slug:
        priority = '0.80'
    
    # Pillar authority pages get 0.82
    if any(x in slug for x in ['guide', 'charter', 'yacht-charter', 'villa-rental']):
        if priority == '0.75':
            priority = '0.80'

    changefreq = 'weekly' if priority >= '0.85' else 'monthly'

    xml_entries.append(f"""  <url>
    <loc>{url}</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>{changefreq}</changefreq>
    <priority>{priority}</priority>
  </url>""")

sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(xml_entries)}
</urlset>"""

with open('sitemap.xml', 'w', encoding='utf-8') as f:
    f.write(sitemap)

print(f"Sitemap regenerated: {len(xml_entries)} URLs | lastmod: {TODAY}")
