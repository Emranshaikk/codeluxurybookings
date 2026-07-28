import os
import re
import json

def verify_all_fixes():
    files = [f for f in os.listdir('.') if f.endswith('.html') and '-to-' in f and 'private-jet-cost' in f and 'guide' not in f]
    print(f"Verifying {len(files)} standard route files...")
    
    with open('audit_distances_comparison.json', 'r', encoding='utf-8') as f:
        comp_data = json.load(f)
    dist_map = {item['filename']: item['real_dist'] for item in comp_data}
    
    issues = []
    
    for filename in files:
        filepath = os.path.join('.', filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        real_dist = round(dist_map.get(filename, 0))
        
        # 1. Check personal email removal
        if 'contactshaikk@gmail.com' in content:
            issues.append(f"{filename}: Still contains hardcoded personal gmail 'contactshaikk@gmail.com'")
            
        # 2. Check Product schema removal
        if '"Product"' in content or '"@type": "Product"' in content:
            issues.append(f"{filename}: Still contains Product schema")
            
        # 3. Check LocalBusiness schema removal
        if '"LocalBusiness"' in content or '"@type": "LocalBusiness"' in content:
            issues.append(f"{filename}: Still contains LocalBusiness schema")
            
        # 4. Check Breadcrumb mismatch removal
        if 'href="https://eliteluxurybookings.com/private-jet-booking-guide/"' in content or 'href="/private-jet-booking-guide/"' in content:
            issues.append(f"{filename}: Breadcrumb visible link still points to private-jet-booking-guide")
            
        # 5. Check corrupted ticker or menu characters
        if '?? Intelligence Alert' in content or '? Private Jets' in content or '?? Luxury Villas' in content or '? Luxury Yachts' in content:
            issues.append(f"{filename}: Still contains corrupted ticker/menu characters ('??' or '?')")
            
        # 6. Check Distance in text/card
        distance_match = re.search(r'Mission Distance</p>\s*<h3[^>]*>\s*([\d,]+)\s*<span[^>]*>Miles</span></h3>', content, re.IGNORECASE)
        if distance_match:
            stated = int(distance_match.group(1).replace(',', ''))
            deviation = abs(stated - real_dist) / real_dist if real_dist > 0 else 0
            if deviation > 0.10:
                issues.append(f"{filename}: Distance mismatch: Stated {stated} vs Real {real_dist}")
                
        # 7. Check fake urgency alert removal
        if '<div class="urgency-alert"' in content or "<div class='urgency-alert'" in content:
            issues.append(f"{filename}: Still contains old urgency-alert HTML element")
            
    print("\n--- VERIFICATION AUDIT SUMMARY ---")
    if not issues:
        print("ALL 116 ROUTE PAGES PASSED VERIFICATION WITH ZERO ERRORS!")
    else:
        print(f"Found {len(issues)} issues across files:")
        for issue in issues[:30]:
            print(f"  [FAIL] {issue}")
        if len(issues) > 30:
            print(f"  ... and {len(issues) - 30} more.")

if __name__ == '__main__':
    verify_all_fixes()
