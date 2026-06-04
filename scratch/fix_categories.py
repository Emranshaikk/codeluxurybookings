import json
import os

def fix_categories():
    filepath = "blog-data.json"
    if not os.path.exists(filepath):
        print("blog-data.json not found!")
        return
        
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    updated_count = 0
    for item in data:
        cat = item.get('category')
        if cat == 'yacht':
            item['category'] = 'private yacht'
            print(f"Updated category for {item.get('url')} from 'yacht' to 'private yacht'")
            updated_count += 1
            
    if updated_count > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        print(f"\nSuccessfully updated {updated_count} items in blog-data.json!")
    else:
        print("No items with category 'yacht' found.")

if __name__ == '__main__':
    fix_categories()
