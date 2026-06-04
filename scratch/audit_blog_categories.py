import json
import os

def audit_categories():
    filepath = "blog-data.json"
    if not os.path.exists(filepath):
        print("blog-data.json not found!")
        return
        
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    mismatches = []
    overlapped = []
    
    print(f"Auditing category mapping for {len(data)} items...")
    
    for item in data:
        url = item.get('url', '').lower()
        itemCat = item.get('category', '').lower()
        
        # Replicate JS logic
        is_route = '-private-jet-cost' in url or 'private-jet' in url or 'aviation' in url
        is_yacht = 'yacht' in url or 'boat' in url or 'catamaran' in url
        is_villa = 'villa' in url or 'island' in url or 'estate' in url
        
        in_jet = 'jet' in itemCat or 'aviation' in itemCat or 'aircraft' in itemCat or is_route or 'lifestyle' in itemCat
        in_yacht = 'yacht' in itemCat or 'boat' in itemCat or 'catamaran' in itemCat or is_yacht or 'lifestyle' in itemCat
        in_villa = 'villa' in itemCat or 'island' in itemCat or 'estate' in itemCat or is_villa or 'lifestyle' in itemCat
        
        matched_tabs = []
        if in_jet: matched_tabs.append("Private Jet")
        if in_yacht: matched_tabs.append("Private Yacht")
        if in_villa: matched_tabs.append("Luxury Villa")
        
        # Check for overlaps (appearing in more than one category)
        if len(matched_tabs) > 1:
            overlapped.append((item.get('url'), itemCat, matched_tabs))
            
        # Check if the page is placed in a category that doesn't make sense
        # E.g. a villa page appearing in private jet, etc.
        if 'villa' in url or 'island' in url:
            if 'Private Jet' in matched_tabs and 'Luxury Villa' not in matched_tabs:
                mismatches.append((item.get('url'), itemCat, matched_tabs, "Should be Villa"))
        if 'yacht' in url or 'boat' in url:
            if 'Private Jet' in matched_tabs and 'Private Yacht' not in matched_tabs:
                mismatches.append((item.get('url'), itemCat, matched_tabs, "Should be Yacht"))
                
    print("-" * 50)
    print(f"Overlapped items (appearing in multiple tabs) ({len(overlapped)}):")
    for url, cat, tabs in overlapped:
        print(f"  {url} | Category in JSON: '{cat}' | Appears in tabs: {tabs}")
        
    print("-" * 50)
    print(f"Misclassified items ({len(mismatches)}):")
    for url, cat, tabs, note in mismatches:
        print(f"  {url} | Category in JSON: '{cat}' | Appears in tabs: {tabs} | Note: {note}")

if __name__ == "__main__":
    audit_categories()
