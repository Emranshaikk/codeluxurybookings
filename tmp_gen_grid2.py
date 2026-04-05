import os
import glob
import re

ROOT_DIR = r'c:\Users\imran\OneDrive\Desktop\ELB code'

system_folders = {'assets', 'core', 'css', 'js', 'fonts', 'images', 'layouts', 'blog', 'elite-private-jet-charter', 'luxury-yacht-rentals', 'luxury-villa-rentals', 'contact', 'private-jet-rental-prices', 'types-of-private-jets', 'empty-leg-flights-discount', 'private-jet-for-business-travel', 'luxury-villas'}

def is_blog(folder_name):
    if folder_name in system_folders:
         return False
    if folder_name.startswith('.'):
         return False
    return True

blogs = []
for f in os.listdir(ROOT_DIR):
    p = os.path.join(ROOT_DIR, f)
    if os.path.isdir(p) and is_blog(f):
         idx = os.path.join(p, 'index.html')
         if os.path.exists(idx):
             blogs.append(f)

# generate html grid
grid_html = '<div class="blog-grid" id="blogGrid" style="display: grid; grid-template-columns: repeat(auto-fill, minmax(350px, 1fr)); gap: 2.5rem;">\n'

for slug in blogs:
    idx = os.path.join(ROOT_DIR, slug, 'index.html')
    try:
        with open(idx, 'r', encoding='utf-8') as file:
            content = file.read()
            
        t_m = re.search(r'<title>(.*?)</title>', content)
        title = t_m.group(1).split('|')[0].strip() if t_m else slug.replace('-', ' ').title()
        
        d_m = re.search(r'<meta name="description" content="(.*?)">', content)
        desc = d_m.group(1) if d_m else 'Explore premium global aviation options.'
        if len(desc) > 120:
             desc = desc[:117] + '...'
             
        i_m = re.search(r'<img[^>]+src="([^"]+)"[^>]*class="[^"]*blog-hero-img[^"]*"', content)
        if not i_m:
            i_m = re.search(r'<img[^>]+src="([^"]+)"', content)
            
        img_src = i_m.group(1) if i_m else 'https://images.pexels.com/photos/7233354/pexels-photo-7233354.jpeg'
        if img_src.startswith('//'):
             if 'yachting.com' in img_src: 
                  img_src = 'https://images.pexels.com/photos/7233354/pexels-photo-7233354.jpeg'
        if '1729a6e6' in img_src or 'yachting.com' in img_src or '{{HERO_IMAGE}}' in img_src:
             img_src = 'https://images.pexels.com/photos/7233354/pexels-photo-7233354.jpeg'
             
        # determine category
        cat = 'private jets'
        if 'yacht' in slug or 'boat' in slug or 'catamaran' in slug:
             cat = 'yachts'
        elif 'villa' in slug and 'mediterranean' not in slug:
             cat = 'villas'

        grid_html += f'''
    <a href="/{slug}/" class="blog-card" data-category="{cat}" style="display: block; background: var(--graphene); border: 1px solid var(--glass-border); border-radius: 20px; overflow: hidden; text-decoration: none; transition: transform 0.3s ease;">
        <div class="card-img-container" style="height: 250px; overflow: hidden;">
            <img src="{img_src}" alt="{title}" onerror="this.src=\'https://images.pexels.com/photos/7233354/pexels-photo-7233354.jpeg?auto=compress&cs=tinysrgb&w=800\'" style="width: 100%; height: 100%; object-fit: cover; transition: transform 0.5s ease;" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
        </div>
        <div class="card-content" style="padding: 2rem;">
            <div class="card-meta" style="color: var(--primary-gold); font-size: 0.8rem; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 1rem;">{cat}</div>
            <h3 style="color: #fff; font-size: 1.4rem; margin-bottom: 1rem; line-height: 1.3; font-family: 'Cormorant Garamond', serif;">{title}</h3>
            <p style="color: var(--text-muted); font-size: 0.95rem; line-height: 1.6; margin-bottom: 0;">{desc}</p>
        </div>
    </a>
'''
    except Exception as e:
        pass

grid_html += '</div>'

blog_idx_path = os.path.join(ROOT_DIR, 'blog', 'index.html')
try:
    with open(blog_idx_path, 'r', encoding='utf-8') as f:
        blog_content = f.read()

    # Find where <div class="blog-grid" id="blogGrid"> starts and where it ends
    # It ends right before <!-- Dynamic Conversion Logic --> or <div class="pagination">
    
    start_str = '<div class="blog-grid" id="blogGrid">'
    end_str = '<div class="pagination"'
    end_str2 = '<!-- Dynamic Conversion Logic -->'
    
    if start_str in blog_content:
        top = blog_content.split(start_str)[0]
        bot_section = blog_content.split(start_str)[1]
        
        if end_str in bot_section:
            bot = end_str + bot_section.split(end_str)[1]
        elif end_str2 in bot_section:
            bot = end_str2 + bot_section.split(end_str2)[1]
        else:
            bot = '</div>' # fallback
            
        final_html = top + grid_html + '\n\n' + bot
        
        with open(blog_idx_path, 'w', encoding='utf-8') as f:
            f.write(final_html)
        print(f"Successfully replaced grid with {len(blogs)} blogs.")
    else:
        print("Couldn't find target div.")
except Exception as e:
    print('Failed to merge:', e)
