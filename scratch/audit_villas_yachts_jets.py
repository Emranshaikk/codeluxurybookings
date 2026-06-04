import json
import os
import re

EXCLUDE_FILES = {
    'index.html', '404.html', 'thank-you.html', 'test_bot.html', 'contact.html',
    'about.html', 'privacy.html', 'terms.html', 'partners.html', 'request-quote.html',
    'luxury-charter-inquiry.html', 'blog.html', 'old_blog.html'
}

def analyze_pages():
    root_dir = r"c:\Users\imran\OneDrive\Desktop\ELB code"
    json_path = os.path.join(root_dir, "blog-data.json")
    
    with open(json_path, 'r', encoding='utf-8') as f:
        blog_data = json.load(f)
        
    blog_dict = {item['url']: item for item in blog_data}
    html_files = [f for f in os.listdir(root_dir) if f.endswith('.html') and f not in EXCLUDE_FILES]
    
    villa_related = []
    yacht_related = []
    jet_related = []
    
    for filename in sorted(html_files):
        url = f"/{filename}"
        full_path = os.path.join(root_dir, filename)
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read().lower()
            
        title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
        title = title_match.group(1).strip() if title_match else filename
        
        # Determine keywords
        has_villa_kw = any(x in filename.lower() for x in ['villa', 'island', 'estate']) or 'villa' in title.lower() or 'island' in title.lower()
        has_yacht_kw = any(x in filename.lower() for x in ['yacht', 'boat', 'catamaran', 'sailing', 'mallorca', 'formentera']) or 'yacht' in title.lower() or 'boat' in title.lower()
        has_jet_kw = any(x in filename.lower() for x in ['jet', 'aviation', 'flight', 'route', 'airport', 'heavy-jet', 'empty-leg']) or 'jet' in title.lower() or 'flight' in title.lower() or 'aviation' in title.lower()
        
        current_cat = blog_dict.get(url, {}).get('category', 'MISSING')
        
        if has_villa_kw:
            villa_related.append((url, title, current_cat))
        if has_yacht_kw:
            # Avoid jet false positives in yacht keywords (e.g. if it has jet, but wait, if it's charter...)
            if 'jet' in filename.lower() and 'charter' in filename.lower() and not any(x in filename.lower() for x in ['yacht', 'boat', 'catamaran', 'sailing']):
                pass
            else:
                yacht_related.append((url, title, current_cat))
        if has_jet_kw:
            jet_related.append((url, title, current_cat))

    print(f"=== Villa Related Pages ({len(villa_related)}) ===")
    for url, title, cat in villa_related:
        print(f"  {url} | Cat: '{cat}' | Title: {title[:60]}")
        
    print(f"\n=== Yacht Related Pages ({len(yacht_related)}) ===")
    for url, title, cat in yacht_related:
        print(f"  {url} | Cat: '{cat}' | Title: {title[:60]}")
        
    print(f"\n=== Jet Related Pages ({len(jet_related)}) ===")
    # Print a summary of jet pages instead of all of them (since there are many)
    incorrect_jets = [x for x in jet_related if x[2] != 'private jet']
    print(f"  Total jet pages: {len(jet_related)}")
    print(f"  Jet pages with non-'private jet' category in JSON ({len(incorrect_jets)}):")
    for url, title, cat in incorrect_jets:
        print(f"    {url} | Cat: '{cat}' | Title: {title[:60]}")

if __name__ == '__main__':
    analyze_pages()
