
import os
import re

def get_blog_links():
    index_file = 'blog/index.html'
    if not os.path.exists(index_file): 
        print("MISSING_INDEX")
        return []
    with open(index_file, 'r', encoding='utf-8') as f:
        content = f.read()
    # Extract all <a href="/folder-name/"> links from the blog grid
    # Patterns look like href="/private-jet-charter-expert-guide-to-luxury/"
    links = re.findall(r'href="/([^/]+)/"', content)
    # Filter out common base pages
    filtered = [l for l in links if l not in ['elite-private-jet-charter', 'luxury-yacht-rentals', 'luxury-villa-rentals', 'blog', 'contact']]
    return list(set(filtered))

if __name__ == "__main__":
    blog_slugs = get_blog_links()
    if blog_slugs:
        print(",".join(blog_slugs))
