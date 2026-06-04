import json
import os

def inspect_blog():
    filepath = "blog-data.json"
    if not os.path.exists(filepath):
        print("blog-data.json not found!")
        return
        
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    print(f"Total items in blog-data.json: {len(data)}")
    
    categories = {}
    for item in data:
        cat = item.get('category')
        categories[cat] = categories.get(cat, 0) + 1
        
    print("Unique categories in JSON:")
    for cat, count in categories.items():
        print(f"  - '{cat}': {count} items")
        
    # Check for our 6 new pages
    new_pages = [
        "/private-yacht-vacation-package.html",
        "/yacht-charter-for-private-events.html",
        "/yacht-charter-for-wedding.html",
        "/luxury-yacht-charter-caribbean.html",
        "/luxury-yacht-rental-for-parties.html",
        "/luxury-yacht-charter-for-family-vacation.html"
    ]
    
    print("-" * 50)
    print("New pages check:")
    for page in new_pages:
        found = False
        for item in data:
            if item.get('url') == page:
                print(f"  [FOUND] {page} | Category: '{item.get('category')}'")
                found = True
                break
        if not found:
            print(f"  [MISSING] {page}")

if __name__ == "__main__":
    inspect_blog()
