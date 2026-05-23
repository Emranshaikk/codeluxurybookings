import os
import re
from bs4 import BeautifulSoup

def audit_links_and_a11y():
    root_dir = r'c:\Users\imran\OneDrive\Desktop\ELB code'
    html_files = [f for f in os.listdir(root_dir) if f.endswith('.html')]
    
    broken_links = []
    a11y_issues = []
    
    # Internal link pattern
    internal_pattern = re.compile(r'https?://(?:www\.)?eliteluxurybookings\.com/([^/\s"]+)/?')

    for filename in html_files:
        filepath = os.path.join(root_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
            
        # 1. Check Links
        links = soup.find_all('a', href=True)
        for link in links:
            href = link['href']
            
            # Check internal links
            match = internal_pattern.search(href)
            if match:
                slug = match.group(1)
                if slug and not slug.endswith('.html'):
                    target_file = slug + '.html'
                    target_path = os.path.join(root_dir, target_file)
                    if not os.path.exists(target_path) and slug != 'blog': # blog might be a folder or handled differently
                        broken_links.append((filename, href))
            
            # Check relative links
            elif href.startswith('/') and href.endswith('.html'):
                target_path = os.path.join(root_dir, href.lstrip('/'))
                if not os.path.exists(target_path):
                    broken_links.append((filename, href))

        # 2. Check A11y
        # Images without alt
        images = soup.find_all('img')
        for img in images:
            if not img.get('alt'):
                a11y_issues.append((filename, f"Image missing alt: {img.get('src')}"))
                
        # Interactive elements without aria-labels (e.g. menu buttons)
        buttons = soup.find_all(['button', 'a'])
        for btn in buttons:
            # Check for icon-only links/buttons
            if not btn.get_text().strip() and not btn.get('aria-label'):
                # Common icons
                if btn.find('i', class_=re.compile(r'fa-|fab-|fas-')):
                    a11y_issues.append((filename, f"Icon link/button missing aria-label: {btn.get('href') or 'button'}"))

    # Output results
    if broken_links:
        print("### BROKEN LINKS FOUND")
        for f, l in list(set(broken_links))[:20]: # Limit output
            print(f"- {f} -> {l}")
    else:
        print("No broken internal links found.")
        
    if a11y_issues:
        print("\n### A11Y ISSUES FOUND")
        for f, msg in list(set(a11y_issues))[:20]: # Limit output
            print(f"- {f}: {msg}")
    else:
        print("No major A11y issues found.")

if __name__ == "__main__":
    audit_links_and_a11y()
