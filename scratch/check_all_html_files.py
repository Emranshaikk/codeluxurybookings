import json
import os
import re

EXCLUDE_FILES = {
    'index.html', '404.html', 'thank-you.html', 'test_bot.html', 'contact.html',
    'about.html', 'privacy.html', 'terms.html', 'partners.html', 'request-quote.html',
    'luxury-charter-inquiry.html', 'blog.html', 'old_blog.html'
}

def determine_correct_category(filename, title, content):
    name_lower = filename.lower()
    title_lower = title.lower()
    content_lower = content.lower()
    
    # Check Villa indicators first
    villa_indicators = ['villa', 'island', 'estate', 'mansion', 'honeymoon', 'chalet', 'resort']
    if any(x in name_lower for x in villa_indicators):
        return 'luxury villa'
    if any(x in title_lower for x in ['villa', 'island', 'estate', 'mansion', 'honeymoon', 'chalet']):
        return 'luxury villa'
        
    # Check Yacht indicators
    yacht_indicators = ['yacht', 'boat', 'sailing', 'catamaran', 'bareboat', 'sunreef', 'mallorca', 'formentera', 'maritime', 'charter', 'seadeck', 'ocean', 'cruise', 'superyacht']
    # But check if it's jet charter
    if any(x in name_lower for x in yacht_indicators):
        if 'private-jet-charter' in name_lower or 'business-jet' in name_lower or 'corporate-jet' in name_lower:
            return 'private jet'
        return 'private yacht'
    if any(x in title_lower for x in ['yacht', 'boat', 'sailing', 'catamaran', 'bareboat', 'sunreef', 'maritime', 'superyacht', 'charter']):
        if 'jet' in title_lower or 'aircraft' in title_lower or 'flight' in title_lower:
            return 'private jet'
        return 'private yacht'
        
    # Check Jet indicators
    jet_indicators = ['jet', 'aviation', 'flight', 'route', 'airport', 'flying', 'heavy-jet', 'empty-leg', 'citation', 'gulfstream', 'bombardier', 'embraer', 'boeing', 'airbus', 'pilot', 'charter-cost']
    if any(x in name_lower for x in jet_indicators):
        return 'private jet'
    if any(x in title_lower for x in ['jet', 'aviation', 'flight', 'route', 'airport', 'flying', 'aircraft', 'gulfstream', 'citation', 'pilot']):
        return 'private jet'
        
    # Fallback to scanning content body for keyword densities or strong indicators
    if 'villa' in content_lower or 'private island' in content_lower:
        # Check if it talks about villas more than jets/yachts
        v_count = content_lower.count('villa') + content_lower.count('island')
        j_count = content_lower.count('jet') + content_lower.count('aircraft') + content_lower.count('flight')
        y_count = content_lower.count('yacht') + content_lower.count('boat') + content_lower.count('catamaran')
        if v_count > j_count and v_count > y_count:
            return 'luxury villa'
            
    if 'yacht' in content_lower or 'catamaran' in content_lower or 'boat' in content_lower:
        v_count = content_lower.count('villa') + content_lower.count('island')
        j_count = content_lower.count('jet') + content_lower.count('aircraft') + content_lower.count('flight')
        y_count = content_lower.count('yacht') + content_lower.count('boat') + content_lower.count('catamaran')
        if y_count > j_count and y_count > v_count:
            return 'private yacht'
            
    if 'jet' in content_lower or 'aviation' in content_lower or 'aircraft' in content_lower:
        return 'private jet'
        
    return 'private jet' # Default

def check_all():
    root_dir = r"c:\Users\imran\OneDrive\Desktop\ELB code"
    json_path = os.path.join(root_dir, "blog-data.json")
    
    with open(json_path, 'r', encoding='utf-8') as f:
        blog_data = json.load(f)
        
    blog_dict = {item['url']: item for item in blog_data}
    
    html_files = [f for f in os.listdir(root_dir) if f.endswith('.html') and f not in EXCLUDE_FILES]
    
    print(f"Auditing {len(html_files)} HTML files for content and metadata matches...")
    
    issues = []
    for filename in sorted(html_files):
        url = f"/{filename}"
        full_path = os.path.join(root_dir, filename)
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Get title
        title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
        title = title_match.group(1).strip() if title_match else filename
        
        correct_cat = determine_correct_category(filename, title, content)
        
        if url in blog_dict:
            current_cat = blog_dict[url].get('category')
            if current_cat != correct_cat:
                issues.append({
                    'url': url,
                    'title': title,
                    'current': current_cat,
                    'correct': correct_cat
                })
        else:
            issues.append({
                'url': url,
                'title': title,
                'current': 'MISSING',
                'correct': correct_cat
            })
            
    print(f"\nFound {len(issues)} discrepancy cases:")
    for iss in issues:
        print(f"URL: {iss['url']}")
        print(f"  Title: {iss['title']}")
        print(f"  Current category: {iss['current']}")
        print(f"  Correct category: {iss['correct']}")
        print("-" * 40)

if __name__ == '__main__':
    check_all()
