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
    
    # Check by keywords in filename
    if any(x in filename_lower for x in ['yacht', 'boat', 'sailing', 'catamaran', 'bareboat', 'sunreef', 'mallorca', 'formentera']):
        return 'private yacht'
    if any(x in filename_lower for x in ['jet', 'aviation', 'flight', 'route', 'airport', 'flying', 'heavy-jet', 'empty-leg']):
        return 'private jet'
    if any(x in filename_lower for x in ['villa', 'island', 'honeymoon']):
        return 'luxury villa'
        
    # Check by content keywords if filename is ambiguous
    content_lower = content.lower()
    if 'yacht' in content_lower or 'catamaran' in content_lower:
        return 'private yacht'
    if 'private jet' in content_lower or 'aircraft' in content_lower:
        return 'private jet'
    if 'villa' in content_lower or 'island rental' in content_lower:
        return 'luxury villa'
        
    return 'private jet'  # Default fallback

def get_label(category):
    if category == 'private yacht':
        return 'Charter Authority'
    elif category == 'private jet':
        return 'Aviation Authority'
    else:
        return 'Estate Portfolio'

def get_link_text(category):
    if category == 'private yacht':
        return 'Explore Yacht Fleet'
    elif category == 'private jet':
        return 'Configure Sourcing Solution'
    else:
        return 'View Luxury Portfolio'

def sync_blog():
    root_dir = r"c:\Users\imran\OneDrive\Desktop\ELB code"
    filepath = os.path.join(root_dir, "blog-data.json")
    
    if not os.path.exists(filepath):
        print("blog-data.json not found!")
        return
        
    with open(filepath, 'r', encoding='utf-8') as f:
        blog_data = json.load(f)
        
    existing_urls = {item.get('url') for item in blog_data}
    
    html_files = [f for f in os.listdir(root_dir) if f.endswith('.html') and not f.startswith('_') and f not in EXCLUDE_FILES]
    
    added_count = 0
    
    for filename in sorted(html_files):
        # blog-data.json uses format: /filename.html
        url = f"/{filename}"
        
        if url in existing_urls:
            continue
            
        full_path = os.path.join(root_dir, filename)
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        category = classify_page(filename, content)
        
        # Extract title
        title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
        title = title_match.group(1).strip().replace('\n', ' ').replace('  ', ' ') if title_match else filename.replace('.html', '').replace('-', ' ').title()
        
        # Clean title suffix if standard
        title = re.split(r'\s*\|\s*', title)[0]
        
        # Extract description
        desc_match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']+)["\']', content, re.IGNORECASE)
        if not desc_match:
            desc_match = re.search(r'<meta\s+content=["\']([^"\']+)["\']\s+name=["\']description["\']', content, re.IGNORECASE)
            
        excerpt = desc_match.group(1).strip() if desc_match else f"Elite luxury guide for {title.lower()} experiences."
        
        new_item = {
            "url": url,
            "category": category,
            "label": get_label(category),
            "title": title,
            "excerpt": excerpt,
            "link_text": get_link_text(category)
        }
        
        blog_data.append(new_item)
        print(f"  [ADDED] {url} -> Category: '{category}' | Title: '{title}'")
        added_count += 1
        
    if added_count > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(blog_data, f, indent=4)
        print(f"Successfully updated blog-data.json! Added {added_count} items. Total: {len(blog_data)}")
    else:
        print("No missing HTML files found. blog-data.json is already fully synchronized!")

if __name__ == "__main__":
    sync_blog()
