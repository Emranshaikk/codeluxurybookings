
import os
import re

WIDGET_CODE = """
<!-- ELB_YACHTING_WIDGET_START -->
<aside class="blog-sidebar">
    <div class="yacht-widget-container">
        <a href="https://www.yachting.com/en-gb?AffiliateID=elbookings&amp;BannerID=1729a6e6" target="_top">
            <img src="//affiliate.yachting.com/accounts/default1/ne6ayxbkog/1729a6e6.png" alt="Exclusive Yacht Charter" title="Book Premium Yachts" width="320" height="1200" style="width:100%; height:auto; display:block;" />
        </a>
        <img style="border:0" src="https://affiliate.yachting.com/scripts/ne6ayxikog?AffiliateID=elbookings&amp;BannerID=1729a6e6" width="1" height="1" alt="" />
    </div>
</aside>
<!-- ELB_YACHTING_WIDGET_END -->
"""

SIDEBAR_CSS = """
/* ELB_BLOG_SIDEBAR_START */
@media (min-width: 1100px) {
    .blog-main-layout { display: flex; gap: 4rem; align-items: flex-start; max-width: 1300px; margin: 0 auto; padding-top: 100px; }
    .blog-content-area { flex: 1; min-width: 0; }
    .blog-sidebar { width: 320px; flex-shrink: 0; position: sticky; top: 120px; }
}
@media (max-width: 1099px) {
    .blog-sidebar { margin: 4rem auto; text-align: center; }
    .yacht-widget-container { display: inline-block; max-width: 320px; }
}
.yacht-widget-container { border-radius: 20px; overflow: hidden; border: 1px solid var(--glass-border); background: var(--graphene); box-shadow: 0 15px 35px rgba(0,0,0,0.4); }
/* ELB_BLOG_SIDEBAR_END */
"""

def get_blog_slugs():
    index_file = 'blog/index.html'
    if not os.path.exists(index_file): return []
    with open(index_file, 'r', encoding='utf-8') as f:
        content = f.read()
    links = re.findall(r'href="/([^/]+)/"', content)
    filtered = [l for l in links if l not in ['elite-private-jet-charter', 'luxury-yacht-rentals', 'luxury-villa-rentals', 'blog', 'contact']]
    return list(set(filtered))

def inject_widget(slug):
    post_file = os.path.join(slug, 'index.html')
    if not os.path.exists(post_file): return False
    
    with open(post_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    if 'ELB_YACHTING_WIDGET_START' in content: return False # Skip if already done
    
    # 1. Inject CSS into <style> block
    if '</style>' in content:
        content = content.replace('</style>', f'\n{SIDEBAR_CSS}\n</style>')
    
    # 2. Update .container width
    content = content.replace('.container { max-width: 900px;', '.container { max-width: 1300px; padding-top: 2rem;')
    
    # 3. Inject structural wrappers around <article>
    # Wrap article content in blog-main-layout
    article_pattern = re.compile(r'(?s)<article[^>]*?>(.*?)</article>', re.IGNORECASE)
    match = article_pattern.search(content)
    if match:
        original_article = match.group(0)
        inner_content = match.group(1)
        
        # New wrapped content
        wrapped_article = f"""
<div class="blog-main-layout">
    <div class="blog-content-area">
        <article class="container" style="max-width: 900px; padding: 0;">
            {inner_content}
        </article>
    </div>
    {WIDGET_CODE}
</div>
"""
        content = content.replace(original_article, wrapped_article)
        
        # Finally save
        with open(post_file, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

if __name__ == "__main__":
    slugs = get_blog_slugs()
    count = 0
    for s in slugs:
        if inject_widget(s):
            count += 1
    print(f"DONE: {count} posts updated.")
