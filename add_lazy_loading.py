import glob
import re

files_changed = 0

for filepath in glob.glob("*.html"):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        
    old_content = content
    
    # Simple regex to find img tags and add loading="lazy" if not present
    # Assuming the first image might be a logo or hero, but in these pages, most images can be lazy loaded.
    # Actually, the user asked to implement image lazy-loading.
    
    def add_lazy(match):
        img_tag = match.group(0)
        if 'loading="lazy"' not in img_tag and "loading='lazy'" not in img_tag:
            return img_tag.replace('<img ', '<img loading="lazy" ')
        return img_tag

    # Wait, some tags might be <img\n src...
    # Let's use a regex to replace <img with <img loading="lazy"
    
    content = re.sub(r'<img\s+(?![^>]*loading=)', r'<img loading="lazy" ', content, flags=re.IGNORECASE)

    if content != old_content:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        files_changed += 1

print(f"Updated {files_changed} files with lazy loading.")
