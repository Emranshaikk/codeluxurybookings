import os
import re

def comprehensive_audit():
    root_dir = r'c:\Users\imran\OneDrive\Desktop\ELB code'
    files = [f for f in os.listdir(root_dir) if f.endswith('.html')]
    
    results = {
        "missing_nav": [],
        "missing_footer": [],
        "missing_schema": [],
        "legacy_hubs": [],
        "missing_analytics": [],
        "broken_canonical": [],
        "inconsistent_meta_desc": []
    }
    
    for filename in files:
        if filename in ['404.html', 'thank-you.html']: continue
        
        filepath = os.path.join(root_dir, filename)
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        # Check Global Nav
        if 'global-nav' not in content:
            results["missing_nav"].append(filename)
            
        # Check Master Footer
        if 'footer-grid' not in content:
            results["missing_footer"].append(filename)
            
        # Check Schema
        if 'application/ld+json' not in content:
            results["missing_schema"].append(filename)
            
        # Check Analytics
        if 'G-J56D1LJLFM' not in content:
            results["missing_analytics"].append(filename)
            
        # Check for legacy Authority Hubs (the 4-column grid)
        if 'Strategic Maritime Resources' in content or 'Strategic Aviation Resources' in content:
            results["legacy_hubs"].append(filename)
            
        # Check Canonical
        canonical_match = re.search(r'<link rel="canonical" href="https://eliteluxurybookings.com/([^"]+)"', content)
        if canonical_match:
            slug = canonical_match.group(1).rstrip('/')
            expected_slug = filename.replace('.html', '')
            if slug != expected_slug and slug != "":
                 results["broken_canonical"].append(f"{filename} (Canonical: {slug}, Expected: {expected_slug})")
        else:
             results["broken_canonical"].append(f"{filename} (Missing)")

    print("### COMPREHENSIVE ELB AUDIT RESULTS ###\n")
    for key, list_files in results.items():
        print(f"**{key.upper()}** ({len(list_files)} files):")
        for f in list_files[:10]: # Show first 10
            print(f"  - {f}")
        if len(list_files) > 10:
            print(f"  ... and {len(list_files) - 10} more.")
        print()

if __name__ == "__main__":
    comprehensive_audit()
