import os
from bs4 import BeautifulSoup
import sys

# Ensure stdout uses UTF-8
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

files = [
    "amalfi-coast-yacht-rental.html",
    "hongkong-to-singapore-private-jet-cost.html",
    "multi-modal-luxury-itinerary.html",
    "solar-eclipse-balearic-islands-private-yacht.html",
    "ultimate-luxury-villa-rental-guide.html"
]

workspace_dir = r"c:\Users\imran\OneDrive\Desktop\ELB code"

for fn in files:
    path = os.path.join(workspace_dir, fn)
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()
    soup = BeautifulSoup(html, 'html.parser')
    
    title = soup.title.string.strip() if soup.title else "NO TITLE"
    desc_tag = soup.find('meta', attrs={'name': 'description'}) or soup.find('meta', attrs={'property': 'og:description'})
    desc = desc_tag.get('content', '').strip() if desc_tag else "NO DESCRIPTION"
    
    print(f"=== {fn} ===")
    print(f"  Title: {title}")
    print(f"  Desc:  {desc}")
    print("-" * 80)
