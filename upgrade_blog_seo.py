import os
import re
from bs4 import BeautifulSoup

# Configuration
BASE_URL = "https://eliteluxurybookings.com"
DRY_RUN = False

def upgrade_seo(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')
    
    # 1. Standardize Metadata
    head = soup.head
    if not head:
        return

    # Add Twitter Tags if missing
    if not soup.find('meta', attrs={'name': 'twitter:card'}):
        twitter_card = soup.new_tag('meta', attrs={'name': 'twitter:card', 'content': 'summary_large_image'})
        head.append(twitter_card)
    
    if not soup.find('meta', attrs={'name': 'twitter:site'}):
        twitter_site = soup.new_tag('meta', attrs={'name': 'twitter:site', 'content': '@eliteluxuryb'})
        head.append(twitter_site)

    # 2. Inject BlogPosting Schema
    title = soup.title.string if soup.title else "Elite Luxury Intelligence"
    desc_tag = soup.find('meta', attrs={'name': 'description'})
    desc = desc_tag['content'] if desc_tag else ""
    og_image_tag = soup.find('meta', attrs={'property': 'og:image'})
    og_image = og_image_tag['content'] if og_image_tag else f"{BASE_URL}/assets/elite_jet_master_hero.png"
    
    # Extract date if possible (placeholder for now)
    date_published = "2026-05-11T12:00:00+00:00"
    
    schema_script = soup.new_tag('script', type='application/ld+json')
    schema_data = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": title,
        "description": desc,
        "image": og_image,
        "author": {
            "@type": "Organization",
            "name": "Elite Luxury Bookings",
            "url": BASE_URL
        },
        "publisher": {
            "@type": "Organization",
            "name": "Elite Luxury Bookings",
            "logo": {
                "@type": "ImageObject",
                "url": f"{BASE_URL}/favicon.png"
            }
        },
        "datePublished": date_published,
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": f"{BASE_URL}/{os.path.basename(file_path).replace('.html', '')}/"
        }
    }
    
    # Check if already exists
    existing_schema = soup.find_all('script', type='application/ld+json')
    is_already_present = False
    for s in existing_schema:
        if '"BlogPosting"' in s.string:
            is_already_present = True
            break
            
    if not is_already_present:
        import json
        schema_script.string = json.dumps(schema_data, indent=2)
        head.append(schema_script)

    # 3. Inject Table of Contents (Placeholder for JS or static)
    content = soup.find('article', class_='blog-content')
    if content and not soup.find('div', class_='authority-toc'):
        toc_div = soup.new_tag('div', id='authorityTOC', attrs={'class': 'authority-toc'})
        toc_h3 = soup.new_tag('h3')
        toc_h3.string = "Intelligence Index"
        toc_div.append(toc_h3)
        
        # Build TOC from H2s
        toc_ul = soup.new_tag('ul')
        headers = content.find_all(['h2', 'h3'])
        for i, h in enumerate(headers):
            if not h.get('id'):
                h['id'] = f"section-{i}"
            
            li = soup.new_tag('li')
            a = soup.new_tag('a', href=f"#{h['id']}")
            a.string = h.get_text()
            li.append(a)
            toc_ul.append(li)
        
        toc_div.append(toc_ul)
        content.insert(0, toc_div)

    # 4. Inject Related Intelligence Silos at bottom
    if content and not soup.find('section', class_='related-intelligence'):
        related_section = BeautifulSoup("""
        <section class="related-intelligence">
            <h2 class="serif">Related <span class="gold-text">Intelligence</span></h2>
            <div class="related-grid">
                <a href="https://eliteluxurybookings.com/elite-private-jet-charter/" class="related-card">
                    <h4>Private Jets</h4>
                    <p>Global aviation orchestration and discrete charter procurement.</p>
                </a>
                <a href="https://eliteluxurybookings.com/luxury-yacht-rentals/" class="related-card">
                    <h4>Luxury Yachts</h4>
                    <p>Maritime excellence across the world's premier yachting hubs.</p>
                </a>
                <a href="https://eliteluxurybookings.com/luxury-villa-rentals/" class="related-card">
                    <h4>Private Villas</h4>
                    <p>Absolute sanctuary procurement in the most exclusive destinations.</p>
                </a>
            </div>
        </section>
        """, 'html.parser')
        content.append(related_section)

    # 5. Fix Image Alt Text
    for img in soup.find_all('img'):
        if not img.get('alt'):
            # Generate alt from filename
            src = img.get('src', '')
            alt_text = os.path.basename(src).split('.')[0].replace('_', ' ').replace('-', ' ').title()
            img['alt'] = f"Elite Luxury Bookings - {alt_text}"

    # 6. Normalize Internal Links
    for a in soup.find_all('a', href=True):
        href = a['href']
        if href.startswith('https://eliteluxurybookings.com/') and not href.endswith('/') and '.' not in os.path.basename(href):
             a['href'] = href + '/'

    # Save
    if not DRY_RUN:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(soup.prettify())
        print(f"Upgraded: {file_path}")

# Find all blog posts
files = [f for f in os.listdir('.') if f.endswith('.html')]
blog_files = []
for f in files:
    try:
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
            if 'blog-content' in content:
                blog_files.append(f)
    except:
        pass

print(f"Found {len(blog_files)} blog posts to upgrade.")
for f in blog_files:
    upgrade_seo(f)
