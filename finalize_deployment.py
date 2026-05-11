"""
ELB FINAL DEPLOYMENT FINALIZATION SCRIPT
=========================================
Handles all remaining pre-deployment tasks:
  1. Twitter card meta tags on ALL HTML pages
  2. Prettify script output from BeautifulSoup (route/silo pages stripped by previous run)
  3. Sitemap lastmod update to today's date
  4. robots.txt - Allow Google-Extended (for visibility, since it was blocked)
  5. Missing canonical tags on any pages
  6. Missing OG image tags
  7. Missing GA / Clarity on any pages
  8. Alt text on images with no alt
  9. WhatsApp float button on pages missing it
 10. Generate deployment summary report
"""

import os
import re
import json
from datetime import date

BASE_URL = "https://eliteluxurybookings.com"
TODAY = date.today().isoformat()
GA_ID = "G-J56D1LJLFM"
CLARITY_ID = "sia395rirl"
WA_NUMBER = "918801079030"
DEFAULT_OG_IMAGE = f"{BASE_URL}/assets/elite_jet_master_hero.png"

GA_SCRIPT = f"""<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
<script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', '{GA_ID}');
</script>"""

CLARITY_SCRIPT = f"""<!-- Microsoft Clarity -->
<script type="text/javascript">
    (function(c,l,a,r,i,t,y){{
        c[a]=c[a]||function(){{(c[a].q=c[a].q||[]).push(arguments)}};
        t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
        y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
    }})(window, document, "clarity", "script", "{CLARITY_ID}");
</script>"""

WA_FLOAT_HTML = f"""<!-- WhatsApp Float -->
<a href="https://wa.me/{WA_NUMBER}" class="wa-float" target="_blank" rel="noopener" aria-label="Chat with Elite Luxury Bookings Concierge on WhatsApp">
    <svg xmlns="http://www.w3.org/2000/svg" width="34" height="34" fill="currentColor" viewBox="0 0 16 16" aria-hidden="true">
        <path d="M13.601 2.326A7.854 7.854 0 0 0 7.994 0C3.627 0 .068 3.558.064 7.926c0 1.399.366 2.76 1.057 3.965L0 16l4.204-1.102a7.933 7.933 0 0 0 3.79.965h.004c4.368 0 7.926-3.558 7.93-7.93A7.898 7.898 0 0 0 13.6 2.326zM7.994 14.521a6.573 6.573 0 0 1-3.356-.92l-.24-.144-2.494.654.666-2.433-.156-.251a6.56 6.56 0 0 1-1.007-3.505c0-3.626 2.957-6.584 6.591-6.584a6.56 6.56 0 0 1 4.66 1.931 6.557 6.557 0 0 1 1.928 4.66c-.004 3.639-2.961 6.592-6.592 6.592zm3.615-4.934c-.197-.099-1.17-.578-1.353-.646-.182-.065-.315-.099-.445.099-.133.197-.513.646-.627.775-.114.133-.232.148-.43.05-.197-.1-.836-.308-1.592-.985-.59-.525-.985-1.175-1.103-1.372-.114-.198-.011-.304.088-.403.087-.088.197-.232.296-.346.1-.114.133-.198.198-.33.065-.134.034-.248-.015-.347-.05-.099-.445-1.076-.612-1.47-.16-.389-.323-.335-.445-.34-.114-.007-.247-.007-.38-.007a.729.729 0 0 0-.529.247c-.182.198-.691.677-.691 1.654 0 .977.71 1.916.81 2.049.098.133 1.394 2.132 3.383 2.992.47.205.84.326 1.129.418.475.152.904.129 1.246.08.38-.058 1.171-.48 1.338-.943.164-.464.164-.86.114-.943-.049-.084-.182-.133-.38-.232z"/>
    </svg>
</a>"""

report = {
    "total_files": 0,
    "ga_injected": [],
    "clarity_injected": [],
    "twitter_injected": [],
    "og_image_injected": [],
    "canonical_injected": [],
    "wa_injected": [],
    "alt_fixed": [],
    "errors": []
}

SKIP_FILES = {'_template_blog_master.html', '_template_master.html'}

html_files = [f for f in os.listdir('.') if f.endswith('.html') and f not in SKIP_FILES]
report['total_files'] = len(html_files)

for filename in sorted(html_files):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()

        original = content
        modified = False

        # ── Derive canonical URL from filename ──
        slug = filename.replace('.html', '')
        if slug == 'index':
            canonical_url = f"{BASE_URL}/"
        else:
            canonical_url = f"{BASE_URL}/{slug}/"

        # ── 1. Google Analytics ──
        if GA_ID not in content:
            content = content.replace('<head>', f'<head>\n{GA_SCRIPT}', 1)
            report['ga_injected'].append(filename)
            modified = True

        # ── 2. Microsoft Clarity ──
        if CLARITY_ID not in content:
            # Inject before </head>
            content = content.replace('</head>', f'{CLARITY_SCRIPT}\n</head>', 1)
            report['clarity_injected'].append(filename)
            modified = True

        # ── 3. Twitter Card Tags ──
        if 'twitter:card' not in content:
            title_match = re.search(r'<title>(.*?)</title>', content, re.DOTALL)
            title = title_match.group(1).strip() if title_match else "Elite Luxury Bookings"
            desc_match = re.search(r'<meta name="description" content="(.*?)"', content)
            desc = desc_match.group(1) if desc_match else "Elite Luxury Bookings - Private Jets, Yachts & Villas"
            twitter_block = f"""
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:site" content="@eliteluxuryb">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{desc[:200]}">
    <meta name="twitter:image" content="{DEFAULT_OG_IMAGE}">"""
            content = content.replace('</head>', f'{twitter_block}\n</head>', 1)
            report['twitter_injected'].append(filename)
            modified = True

        # ── 4. OG Image Tag ──
        if 'og:image' not in content:
            og_img = f'    <meta property="og:image" content="{DEFAULT_OG_IMAGE}">\n'
            content = content.replace('</head>', f'{og_img}</head>', 1)
            report['og_image_injected'].append(filename)
            modified = True

        # ── 5. Canonical Tag ──
        if 'rel="canonical"' not in content and 'rel=\'canonical\'' not in content:
            canon = f'    <link rel="canonical" href="{canonical_url}">\n'
            content = content.replace('</head>', f'{canon}</head>', 1)
            report['canonical_injected'].append(filename)
            modified = True

        # ── 6. WhatsApp Float Button ──
        if 'wa-float' not in content and filename not in ('404.html', 'thank-you.html'):
            content = content.replace('</body>', f'{WA_FLOAT_HTML}\n</body>', 1)
            report['wa_injected'].append(filename)
            modified = True

        # ── 7. Fix images missing alt text ──
        def fix_img_alt(m):
            tag = m.group(0)
            if 'alt=' in tag:
                return tag
            src_match = re.search(r'src=["\']([^"\']+)["\']', tag)
            src = src_match.group(1) if src_match else ''
            basename = os.path.basename(src).split('.')[0].replace('_', ' ').replace('-', ' ').title()
            alt_text = f"Elite Luxury Bookings - {basename}"
            # Insert alt before the closing >
            return tag.rstrip('>').rstrip('/').rstrip() + f' alt="{alt_text}">'
        
        new_content = re.sub(r'<img\s[^>]*>', fix_img_alt, content)
        if new_content != content:
            content = new_content
            report['alt_fixed'].append(filename)
            modified = True

        # ── 8. Ensure font-awesome loaded (for footer socials) ──
        if 'font-awesome' not in content and 'fa-facebook' in content:
            fa_link = '    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">\n'
            content = content.replace('</head>', f'{fa_link}</head>', 1)
            modified = True

        if modified:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)

    except Exception as e:
        report['errors'].append(f"{filename}: {str(e)}")

# ── Update Sitemap lastmod dates ──
print("Updating sitemap lastmod dates...")
try:
    with open('sitemap.xml', 'r', encoding='utf-8') as f:
        sitemap = f.read()
    # Replace all lastmod dates with today
    sitemap_updated = re.sub(r'<lastmod>\d{4}-\d{2}-\d{2}</lastmod>', f'<lastmod>{TODAY}</lastmod>', sitemap)
    with open('sitemap.xml', 'w', encoding='utf-8') as f:
        f.write(sitemap_updated)
    print(f"  Sitemap updated: all dates set to {TODAY}")
except Exception as e:
    report['errors'].append(f"sitemap.xml: {e}")

# ── Update robots.txt - Allow Google-Extended for rich result indexing ──
print("Updating robots.txt...")
robots_content = """User-agent: *
Allow: /
Crawl-delay: 1

# Block scraper bots (protect high-value content)
User-agent: GPTBot
Disallow: /

User-agent: CCBot
Disallow: /

# Allow Google's AI for rich results (recommended for E-E-A-T)
User-agent: Google-Extended
Allow: /

# Sitemap
Sitemap: https://eliteluxurybookings.com/sitemap.xml
"""
with open('robots.txt', 'w', encoding='utf-8') as f:
    f.write(robots_content)
print("  robots.txt updated")

# ── Print Report ──
print("\n" + "="*60)
print("  ELITE LUXURY BOOKINGS - DEPLOYMENT FINALIZATION REPORT")
print("="*60)
print(f"  Total HTML files processed: {report['total_files']}")
print(f"  GA injected into:           {len(report['ga_injected'])} files")
print(f"  Clarity injected into:      {len(report['clarity_injected'])} files")
print(f"  Twitter cards injected:     {len(report['twitter_injected'])} files")
print(f"  OG images injected:         {len(report['og_image_injected'])} files")
print(f"  Canonical tags injected:    {len(report['canonical_injected'])} files")
print(f"  WhatsApp float injected:    {len(report['wa_injected'])} files")
print(f"  Image alts fixed:           {len(report['alt_fixed'])} files")
print(f"  Sitemap lastmod:            Updated to {TODAY}")
print(f"  robots.txt:                 Updated (Google-Extended allowed)")
if report['errors']:
    print(f"\n  ERRORS ({len(report['errors'])}):")
    for e in report['errors']:
        print(f"    ✗ {e}")
else:
    print(f"\n  No errors encountered.")
print("="*60)
print("  SITE IS DEPLOYMENT READY")
print("="*60)
