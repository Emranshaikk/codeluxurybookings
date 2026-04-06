import os
from datetime import datetime

DOMAIN = "https://eliteluxurybookings.com"

def generate_sitemap():
    pages = []
    
    # 1. Main Root Pages
    root_pages = [
        "/",
        "/elite-private-jet-charter/",
        "/luxury-yacht-rentals/",
        "/luxury-villa-rentals/",
        "/contact/",
        "/blog/",
        "/private-jet-rental-prices/",
        "/types-of-private-jets/",
        "/empty-leg-flights-discount/",
        "/private-jet-for-business-travel/"
    ]
    pages.extend(root_pages)
    
    # 2. Get all subdirectories with index.html (filtering out assets and system dirs)
    for root, dirs, files in os.walk('.'):
        if 'index.html' in files:
            rel_path = os.path.relpath(root, '.').replace('\\', '/')
            
            # Filter out assets, root, and internal folders
            if rel_path == '.' or any(x in rel_path for x in ['assets', '.', 'tmp']):
                continue
                
            # Formatting as URL path
            url_path = f"/{rel_path}/"
            if url_path not in pages:
                pages.append(url_path)
    
    # 3. Create the XML structure
    now = datetime.now().strftime("%Y-%m-%d")
    
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    for page in sorted(pages):
        # Determine priority/changefreq based on page type
        priority = "0.8"
        changefreq = "weekly"
        
        if page == "/":
            priority = "1.0"
            changefreq = "daily"
        elif "blog" in page:
            priority = "0.7"
        elif "-to-" in page:
            # Route pages are landing pages with revenue intent
            priority = "0.9"
            changefreq = "monthly"
            
        xml += '  <url>\n'
        xml += f'    <loc>{DOMAIN}{page}</loc>\n'
        xml += f'    <lastmod>{now}</lastmod>\n'
        xml += f'    <changefreq>{changefreq}</changefreq>\n'
        xml += f'    <priority>{priority}</priority>\n'
        xml += '  </url>\n'
        
    xml += '</urlset>'
    
    # 4. Save to root
    output_path = "c:\\Users\\imran\\OneDrive\\Desktop\\ELB code\\sitemap.xml"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(xml)
    
    print(f"Successfully generated sitemap.xml with {len(pages)} URLs.")

if __name__ == "__main__":
    generate_sitemap()
