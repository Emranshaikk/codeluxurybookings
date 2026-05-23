import os
import sys
from bs4 import BeautifulSoup

if sys.platform.startswith('win'):
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())

FIRST_3 = [
    "index.html",
    "elite-private-jet-charter.html",
    "luxury-yacht-rentals.html"
]

def audit_file(filename):
    print(f"\n================ AUDITING {filename} ================")
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    soup = BeautifulSoup(content, 'html.parser')
    
    stylesheets = [link.get('href') for link in soup.find_all('link', rel='stylesheet')]
    print(f"Stylesheets: {stylesheets}")
    print(f"Has Navigation & Ticker lock: {'ELITE NAV & TICKER STANDARDIZATION' in content}")
    
    navs = soup.find_all('nav', class_='global-nav')
    print(f"Nav elements: {len(navs)}")
    if len(navs) == 1:
        links = [(a.text.strip(), a.get('href')) for a in navs[0].find_all('a')]
        print(f"  Links: {links}")
        
    footers = soup.find_all('footer', class_='footer')
    if not footers:
        footers = soup.find_all('footer')
    print(f"Footers: {len(footers)}")
    if len(footers) == 1:
        cols = footers[0].find_all('div', class_='footer-col')
        print(f"  Columns: {len(cols)}")
        for i, col in enumerate(cols):
            h4 = col.find('h4')
            col_links = [(a.text.strip(), a.get('href')) for a in col.find_all('a')]
            print(f"    Col {i+1} ({h4.text.strip() if h4 else 'No Title'}): {col_links}")
            
    ticker = soup.find('div', class_='top-intel-bar')
    print(f"Has Ticker: {ticker is not None}")
    if ticker:
        print(f"  Ticker content snippet: {ticker.text.strip()[:100]}...")

    forms = soup.find_all('form')
    print(f"Forms: {len(forms)}")
    for i, form in enumerate(forms):
        print(f"  Form {i+1}: action=\"{form.get('action')}\" id=\"{form.get('id')}\"")

def main():
    for f in FIRST_3:
        audit_file(f)

if __name__ == '__main__':
    main()
