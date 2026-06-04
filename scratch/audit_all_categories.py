import json
import os
import re

EXCLUDE_FILES = {
    'index.html', '404.html', 'thank-you.html', 'test_bot.html', 'contact.html',
    'about.html', 'privacy.html', 'terms.html', 'partners.html', 'request-quote.html',
    'luxury-charter-inquiry.html', 'blog.html', 'old_blog.html'
}

def classify_page(filename, content):
    filename_lower = filename.lower()
    
    # 1. First prioritize Villa rules
    if any(x in filename_lower for x in ['villa', 'island', 'estate', 'mansion', 'honeymoon']):
        return 'luxury villa'
        
    # 2. Yacht rules
    if any(x in filename_lower for x in ['yacht', 'boat', 'sailing', 'catamaran', 'bareboat', 'sunreef', 'mallorca', 'formentera', 'maritime', 'charter']):
        # Except if it's private jet charter
        if 'private-jet-charter' in filename_lower:
            return 'private jet'
        return 'private yacht'
        
    # 3. Jet rules
    if any(x in filename_lower for x in ['jet', 'aviation', 'flight', 'route', 'airport', 'flying', 'heavy-jet', 'empty-leg', 'cost-to', 'cost-from', 'to-london', 'to-miami', 'to-paris', 'to-geneva', 'to-seoul', 'to-perth', 'to-melbourne', 'to-newyork', 'to-maldives', 'to-brisbane', 'to-goldcoast', 'to-singapore', 'to-hongkong', 'to-sydney', 'to-losangeles', 'to-beijing']):
        return 'private jet'

    # Fallback to content scanning
    content_lower = content.lower()
    if 'villa' in content_lower or 'island rental' in content_lower or 'private estate' in content_lower:
        return 'luxury villa'
    if 'yacht' in content_lower or 'catamaran' in content_lower or 'boat charter' in content_lower:
        return 'private yacht'
    if 'private jet' in content_lower or 'aircraft' in content_lower or 'flight cost' in content_lower or 'aviation' in content_lower:
        return 'private jet'
        
    return None

def main():
    root_dir = r"c:\Users\imran\OneDrive\Desktop\ELB code"
    json_path = os.path.join(root_dir, "blog-data.json")
    
    if not os.path.exists(json_path):
        print("blog-data.json not found!")
        return
        
    with open(json_path, 'r', encoding='utf-8') as f:
        blog_data = json.load(f)
        
    blog_dict = {item['url']: item for item in blog_data}
    
    html_files = [f for f in os.listdir(root_dir) if f.endswith('.html') and f not in EXCLUDE_FILES]
    
    print(f"Total HTML files found in workspace (excluding system files): {len(html_files)}")
    print(f"Total entries in blog-data.json: {len(blog_data)}")
    
    errors = []
    missing_in_json = []
    
    for filename in sorted(html_files):
        url = f"/{filename}"
        full_path = os.path.join(root_dir, filename)
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        proposed_cat = classify_page(filename, content)
        
        if url not in blog_dict:
            missing_in_json.append((filename, proposed_cat))
            continue
            
        current_cat = blog_dict[url].get('category')
        
        # If proposed is None, let's keep the current or default it
        if proposed_cat is None:
            proposed_cat = current_cat
            
        if current_cat != proposed_cat:
            errors.append({
                'url': url,
                'current': current_cat,
                'proposed': proposed_cat
            })
            
    print("\n--- Misclassified Pages ---")
    if errors:
        for err in errors:
            print(f"URL: {err['url']} | Current Category: '{err['current']}' | Proposed Category: '{err['proposed']}'")
    else:
        print("No misclassified pages found!")
        
    print("\n--- Pages Missing from JSON ---")
    if missing_in_json:
        for filename, cat in missing_in_json:
            print(f"Filename: {filename} | Proposed Category: '{cat}'")
    else:
        print("No missing pages from JSON!")

if __name__ == '__main__':
    main()
