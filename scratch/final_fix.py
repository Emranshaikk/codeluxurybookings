"""
ELB FINAL FIX SCRIPT
====================
Fixes all remaining issues before deployment:
1. Missing Twitter card meta tags (10 files)
2. Missing Clarity tracking (1 file)
3. Missing og:image (1 file)
4. Missing JSON-LD schema (2 files)
5. Add global-route-silo.html to sitemap
6. Update all sitemap lastmod dates to today
7. old_blog.html - exclude from deployment (skip/archive)
"""

import os
import re
from datetime import date

BASE_URL = "https://eliteluxurybookings.com"
TODAY = date.today().isoformat()
GA_ID = "G-J56D1LJLFM"
CLARITY_ID = "sia395rirl"
DEFAULT_OG_IMAGE = f"{BASE_URL}/assets/elite_jet_master_hero.png"

CLARITY_SCRIPT = f"""<!-- Microsoft Clarity -->
<script type="text/javascript">
    (function(c,l,a,r,i,t,y){{
        c[a]=c[a]||function(){{(c[a].q=c[a].q||[]).push(arguments)}};
        t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
        y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
    }})(window, document, "clarity", "script", "{CLARITY_ID}");
</script>"""

SKIP_FILES = {'_template_blog_master.html', '_template_master.html', 'old_blog.html'}

html_files = [f for f in os.listdir('.') if f.endswith('.html') and f not in SKIP_FILES and not f.startswith('_')]

report = {
    'twitter_injected': [],
    'clarity_injected': [],
    'og_image_injected': [],
    'schema_injected': [],
    'errors': []
}

def build_organization_schema():
    return """{
      "@context": "https://schema.org",
      "@type": "Organization",
      "name": "Elite Luxury Bookings",
      "url": "https://eliteluxurybookings.com",
      "logo": "https://eliteluxurybookings.com/assets/elite_jet_master_hero.png",
      "contactPoint": {
        "@type": "ContactPoint",
        "telephone": "+918801079030",
        "contactType": "customer service",
        "availableLanguage": "English"
      }
    }"""

for filename in sorted(html_files):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()

        original = content
        modified = False

        # ── 1. Twitter Card Tags ──
        if 'twitter:card' not in content:
            title_match = re.search(r'<title>(.*?)</title>', content, re.DOTALL)
            title = title_match.group(1).strip() if title_match else "Elite Luxury Bookings"
            # Strip any pipe suffix for twitter title
            title = re.sub(r'\s*\|.*$', '', title).strip()
            
            desc_match = re.search(r'<meta name="description" content="(.*?)"', content)
            desc = desc_match.group(1) if desc_match else "Elite Luxury Bookings - Private Jets, Yachts & Villas"

            og_img = DEFAULT_OG_IMAGE
            # Try to get page-specific og:image if it exists
            og_img_match = re.search(r'og:image" content="(.*?)"', content)
            if og_img_match:
                og_img = og_img_match.group(1)

            twitter_block = f"""
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:site" content="@eliteluxuryb">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{desc[:200]}">
    <meta name="twitter:image" content="{og_img}">"""
            
            content = content.replace('</head>', f'{twitter_block}\n</head>', 1)
            report['twitter_injected'].append(filename)
            modified = True

        # ── 2. Clarity ──
        if CLARITY_ID not in content:
            content = content.replace('</head>', f'{CLARITY_SCRIPT}\n</head>', 1)
            report['clarity_injected'].append(filename)
            modified = True

        # ── 3. OG Image ──
        if 'og:image' not in content:
            og_img_tag = f'    <meta property="og:image" content="{DEFAULT_OG_IMAGE}">\n'
            content = content.replace('</head>', f'{og_img_tag}</head>', 1)
            report['og_image_injected'].append(filename)
            modified = True

        # ── 4. JSON-LD Schema ──
        if 'application/ld+json' not in content:
            schema = build_organization_schema()
            schema_block = f'\n<script type="application/ld+json">\n{schema}\n</script>'
            content = content.replace('</head>', f'{schema_block}\n</head>', 1)
            report['schema_injected'].append(filename)
            modified = True

        if modified:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)

    except Exception as e:
        report['errors'].append(f"{filename}: {str(e)}")

# ── Update Sitemap ──
print("Updating sitemap...")
try:
    with open('sitemap.xml', 'r', encoding='utf-8') as f:
        sitemap = f.read()

    # Update lastmod dates
    sitemap = re.sub(r'<lastmod>\d{4}-\d{2}-\d{2}</lastmod>', f'<lastmod>{TODAY}</lastmod>', sitemap)

    # Add global-route-silo.html if missing
    silo_url = f"{BASE_URL}/global-route-silo/"
    if silo_url not in sitemap and '/global-route-silo' not in sitemap:
        silo_entry = f"""    <url>
        <loc>{silo_url}</loc>
        <lastmod>{TODAY}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.6</priority>
    </url>"""
        sitemap = sitemap.replace('</urlset>', f'{silo_entry}\n</urlset>')
        print("  Added global-route-silo.html to sitemap")

    with open('sitemap.xml', 'w', encoding='utf-8') as f:
        f.write(sitemap)
    print(f"  Sitemap updated: all dates set to {TODAY}")
except Exception as e:
    report['errors'].append(f"sitemap.xml: {e}")

# ── Print Report ──
print("\n" + "="*60)
print("  ELB FINAL FIX REPORT")
print("="*60)
print(f"  Twitter cards injected:  {len(report['twitter_injected'])} files")
print(f"  Clarity injected:        {len(report['clarity_injected'])} files")
print(f"  OG image injected:       {len(report['og_image_injected'])} files")
print(f"  Schema injected:         {len(report['schema_injected'])} files")
print(f"  Files affected:")
affected = set(report['twitter_injected'] + report['clarity_injected'] + 
               report['og_image_injected'] + report['schema_injected'])
for f in sorted(affected):
    print(f"    - {f}")

if report['errors']:
    print(f"\n  ERRORS ({len(report['errors'])}):")
    for e in report['errors']:
        print(f"    X {e}")
else:
    print("\n  No errors encountered.")
print("="*60)
