import os
import re
from bs4 import BeautifulSoup

EXCLUDE_FILES = {'test_bot.html', '_template_master.html', '_template_blog_master.html'}

def audit_all_files():
    root_dir = r"c:\Users\imran\OneDrive\Desktop\ELB code"
    files = [f for f in os.listdir(root_dir) if f.endswith('.html') and f not in EXCLUDE_FILES]
    
    print(f"Auditing headers, footers, and themes across {len(files)} HTML files...")
    
    discrepancies = []
    
    for filename in sorted(files):
        filepath = os.path.join(root_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        soup = BeautifulSoup(content, 'html.parser')
        issues = []
        
        # 1. Check style sheet
        style_links = [link.get('href') for link in soup.find_all('link', rel='stylesheet')]
        if not any(href and '/style.css' in href or href == 'style.css' for href in style_links):
            issues.append("Missing style.css link")
            
        # 2. Check navigation header
        navs = soup.find_all('nav', class_='global-nav')
        if len(navs) != 1:
            issues.append(f"Expected 1 nav element, found {len(navs)}")
        else:
            nav_links = [a.get('href') for a in navs[0].find_all('a')]
            # Expected main links: brand (home), private jets, yachts, villas, blog, contact
            # Let's check for standard destinations in nav links
            has_brand = any(href and 'eliteluxurybookings.com/' in href or href == '/' for href in nav_links)
            has_jets = any(href and 'elite-private-jet-charter' in href for href in nav_links)
            has_yachts = any(href and 'luxury-yacht-rentals' in href for href in nav_links)
            has_villas = any(href and 'luxury-villa-rentals' in href for href in nav_links)
            has_blog = any(href and '/blog' in href for href in nav_links)
            has_contact = any(href and '/contact' in href for href in nav_links)
            
            nav_issues = []
            if not has_brand: nav_issues.append("brand/home")
            if not has_jets: nav_issues.append("private-jets")
            if not has_yachts: nav_issues.append("luxury-yachts")
            if not has_villas: nav_issues.append("luxury-villas")
            if not has_blog: nav_issues.append("blog")
            if not has_contact: nav_issues.append("contact")
            
            if nav_issues:
                issues.append(f"Nav missing links to: {', '.join(nav_issues)}")
                
        # 3. Check mobile menu
        mob_menu = soup.find(id='elbMobileMenu')
        if not mob_menu:
            issues.append("Missing mobile menu (#elbMobileMenu)")
        else:
            mob_links = [a.get('href') for a in mob_menu.find_all('a')]
            has_jets = any(href and 'elite-private-jet-charter' in href for href in mob_links)
            has_yachts = any(href and 'luxury-yacht-rentals' in href for href in mob_links)
            has_villas = any(href and 'luxury-villa-rentals' in href for href in mob_links)
            has_blog = any(href and '/blog' in href for href in mob_links)
            has_contact = any(href and '/contact' in href for href in mob_links)
            
            mob_issues = []
            if not has_jets: mob_issues.append("private-jets")
            if not has_yachts: mob_issues.append("luxury-yachts")
            if not has_villas: mob_issues.append("luxury-villas")
            if not has_blog: mob_issues.append("blog")
            if not has_contact: mob_issues.append("contact")
            
            if mob_issues:
                issues.append(f"Mobile menu missing links to: {', '.join(mob_issues)}")
                
        # 4. Check footer
        footers = soup.find_all('footer')
        if len(footers) != 1:
            issues.append(f"Expected 1 footer, found {len(footers)}")
        else:
            footer_links = [a.get('href') for a in footers[0].find_all('a')]
            has_jets = any(href and 'elite-private-jet-charter' in href for href in footer_links)
            has_yachts = any(href and 'luxury-yacht-rentals' in href for href in footer_links)
            has_villas = any(href and 'luxury-villa-rentals' in href for href in footer_links)
            has_blog = any(href and '/blog' in href for href in footer_links)
            has_contact = any(href and '/contact' in href for href in footer_links)
            
            footer_issues = []
            if not has_jets: footer_issues.append("private-jets")
            if not has_yachts: footer_issues.append("luxury-yachts")
            if not has_villas: footer_issues.append("luxury-villas")
            if not has_blog: footer_issues.append("blog")
            if not has_contact: footer_issues.append("contact")
            
            if footer_issues:
                issues.append(f"Footer missing links to: {', '.join(footer_issues)}")
                
        # 5. Check WhatsApp float link
        wa_links = [a.get('href') for a in soup.find_all('a') if a.get('href') and 'wa.me' in a.get('href')]
        if not wa_links:
            issues.append("Missing WhatsApp float link")
        elif not any('918801079030' in link for link in wa_links):
            issues.append(f"WhatsApp link has incorrect number: {wa_links}")
            
        if issues:
            discrepancies.append((filename, issues))
            
    print(f"\nAudit completed. Found {len(discrepancies)} files with issues.")
    if discrepancies:
        for filename, issues in discrepancies:
            print(f"\nFile: {filename}")
            for issue in issues:
                print(f"  - {issue}")
    else:
        print("[SUCCESS] All audited files have consistent headers, footers, mobile menus, stylesheets, and WhatsApp links!")

if __name__ == '__main__':
    audit_all_files()
