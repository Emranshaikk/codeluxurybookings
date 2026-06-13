import os
import re
from bs4 import BeautifulSoup

def audit_blog_seo():
    root_dir = r'c:\Users\imran\OneDrive\Desktop\ELB code'
    # Define files that are likely "Articles" or "Guides"
    blog_files = [
        '7-best-private-jet-charter-in-dubai.html',
        'business-jet-charter-guide-tips-pricing.html',
        'heavy-jet-vs-light-jet-charter.html',
        'luxury-experience-of-flying-private.html',
        'motor-yacht-vs-sailing-yacht-charter.html',
        'multi-modal-luxury-itinerary-2026.html',
        'private-jet-charter-cost-guide-2026.html',
        'ultimate-luxury-villa-rental-guide.html',
        'villa-vs-luxury-hotel-comparison.html',
        'private-jet-charter-to-monaco.html'
    ]
    
    results = []

    for filename in blog_files:
        filepath = os.path.join(root_dir, filename)
        if not os.path.exists(filepath):
            continue
            
        with open(filepath, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
            
        # SEO Audit
        title = soup.title.string if soup.title else "MISSING"
        desc_meta = soup.find('meta', attrs={'name': 'description'})
        desc = desc_meta['content'] if desc_meta else "MISSING"
        h1 = soup.find('h1')
        h1_text = h1.get_text().strip() if h1 else "MISSING"
        
        # Check for Interlinking (links to pillar pages)
        links = [a['href'] for a in soup.find_all('a', href=True)]
        links_to_pillars = any('elite-private-jet-charter' in l or 'luxury-yacht-rentals' in l or 'luxury-villa-rentals' in l for l in links)
        
        # Check for 2026 keyword (user preference)
        has_2026 = '2026' in title or '2026' in desc
        
        results.append({
            'file': filename,
            'title': title,
            'desc_len': len(desc),
            'h1': h1_text,
            'pillars': links_to_pillars,
            'has_2026': has_2026
        })

    # Print results in a markdown table format for the user
    print("| File | Title | Desc Len | H1 | Links to Pillars? | Has 2026? |")
    print("| :--- | :--- | :--- | :--- | :--- | :--- |")
    for r in results:
        print(f"| {r['file']} | {r['title']} | {r['desc_len']} | {r['h1']} | {r['pillars']} | {r['has_2026']} |")

if __name__ == "__main__":
    audit_blog_seo()
