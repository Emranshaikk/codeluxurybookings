import os
import re

def audit_seo(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    issues = []
    
    # 1. Title Tag
    title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
    if not title_match:
        issues.append("Missing <title> tag")
    else:
        title = title_match.group(1).strip()
        if len(title) < 30 or len(title) > 65:
            issues.append(f"Title tag length is sub-optimal ({len(title)} chars): '{title}'")
            
    # 2. Meta Description
    desc_match = re.search(r'<meta\s+name="description"\s+content="(.*?)"', content, re.IGNORECASE)
    if not desc_match:
        desc_match = re.search(r'<meta\s+content="(.*?)"\s+name="description"', content, re.IGNORECASE)
    
    if not desc_match:
        issues.append("Missing meta description")
    else:
        desc = desc_match.group(1).strip()
        if len(desc) < 100 or len(desc) > 170:
            issues.append(f"Meta description length is sub-optimal ({len(desc)} chars)")
            
    # 3. Canonical Tag
    canonical_match = re.search(r'<link\s+rel="canonical"\s+href="(.*?)"', content, re.IGNORECASE)
    if not canonical_match:
        issues.append("Missing canonical link tag")
        
    # 4. H1 Header count
    h1_matches = re.findall(r'<h1[^>]*>.*?</h1>', content, re.IGNORECASE | re.DOTALL)
    if len(h1_matches) == 0:
        issues.append("Missing <h1> tag (essential for page structure)")
    elif len(h1_matches) > 1:
        issues.append(f"Multiple <h1> tags found ({len(h1_matches)}). Should be exactly 1 per page.")
        
    # 5. Missing Alt tags on images
    images = re.findall(r'<img([^>]+)>', content, re.IGNORECASE)
    missing_alt = 0
    for img in images:
        if 'alt=' not in img.lower() or 'alt=""' in img.lower():
            missing_alt += 1
    if missing_alt > 0:
        issues.append(f"{missing_alt} images are missing descriptive alt attributes")
        
    return issues

def main():
    html_files = []
    for root, dirs, files in os.walk('.'):
        if '.git' in root or '_archive' in root or 'scratch' in root or 'fragments' in root:
            continue
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
                
    print(f"Auditing SEO health of {len(html_files)} HTML pages...\n")
    
    audit_data = {}
    for filepath in html_files:
        issues = audit_seo(filepath)
        if issues:
            audit_data[filepath] = issues
            
    # Calculate stats
    total_pages = len(html_files)
    flawed_pages = len(audit_data)
    perfect_pages = total_pages - flawed_pages
    
    print(f"=== SEO AUDIT SUMMARY ===")
    print(f"Total Pages Analyzed: {total_pages}")
    print(f"Fully Optimized Pages: {perfect_pages} ({(perfect_pages/total_pages)*100:.1f}%)")
    print(f"Pages with minor SEO improvements needed: {flawed_pages} ({(flawed_pages/total_pages)*100:.1f}%)\n")
    
    print("=== REPRESENTATIVE PAGES AUDITED ===")
    # Print issues for a few main pages
    main_pages = ['index.html', 'private-jet-booking-guide.html', 'about.html', 'contact.html', 'global-route-silo.html']
    for filepath in main_pages:
        rel_path = os.path.join('.', filepath)
        if rel_path in audit_data:
            print(f"\n[NEEDS OPTIMIZATION] {filepath}")
            for issue in audit_data[rel_path]:
                print(f"   - {issue}")
        else:
            print(f"\n[FULLY OPTIMIZED] {filepath}")
            
    # Show a few cost pages as examples
    print("\n=== COST PAGES SAMPLES ===")
    cost_samples = [path for path in audit_data.keys() if 'cost' in path][:3]
    for filepath in cost_samples:
        print(f"\n[NEEDS OPTIMIZATION] {filepath}")
        for issue in audit_data[filepath]:
            print(f"   - {issue}")

if __name__ == '__main__':
    main()
