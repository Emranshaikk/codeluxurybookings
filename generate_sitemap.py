import os
from datetime import datetime

def generate_sitemap():
    base_url = "https://eliteluxurybookings.com"
    html_files = [f for f in os.listdir('.') if f.endswith('.html')]
    
    # Exclude templates and 404
    exclude = ['_template_master.html', '_template_blog_master.html', '404.html', 'thank-you.html']
    valid_files = [f for f in html_files if f not in exclude]
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    sitemap_xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    sitemap_xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    
    for filename in valid_files:
        if filename == 'index.html':
            url = f"{base_url}/"
            priority = "1.0"
        elif filename in ['elite-private-jet-charter.html', 'luxury-villa-rentals.html', 'luxury-yacht-rentals.html', 'blog.html']:
            url = f"{base_url}/{filename.replace('.html', '')}/"
            priority = "0.9"
        else:
            url = f"{base_url}/{filename.replace('.html', '')}/"
            priority = "0.8"
            
        sitemap_xml.append('  <url>')
        sitemap_xml.append(f'    <loc>{url}</loc>')
        sitemap_xml.append(f'    <lastmod>{today}</lastmod>')
        sitemap_xml.append('    <changefreq>weekly</changefreq>')
        sitemap_xml.append(f'    <priority>{priority}</priority>')
        sitemap_xml.append('  </url>')
        
    sitemap_xml.append('</urlset>')
    
    with open('sitemap.xml', 'w', encoding='utf-8') as f:
        f.write('\n'.join(sitemap_xml))
        
    print(f"Sitemap generated with {len(valid_files)} URLs.")

if __name__ == "__main__":
    generate_sitemap()
