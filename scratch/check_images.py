import re
import os

html_path = r"c:\Users\imran\OneDrive\Desktop\ELB code\all-inclusive-private-island-rental.html"
assets_dir = r"c:\Users\imran\OneDrive\Desktop\ELB code\assets"

with open(html_path, "r", encoding="utf-8") as f:
    content = f.read()

# Find all image paths in img src, background url, og:image, etc.
img_srcs = re.findall(r'src=["\']([^"\']+)["\']', content)
bg_urls = re.findall(r'url\(["\']?([^"\')]+)["\']?\)', content)
og_images = re.findall(r'content=["\'](https://eliteluxurybookings.com/assets/[^"\']+)["\']', content)

print("--- IMG SRCs ---")
for src in img_srcs:
    print(src)

print("\n--- BG URLs ---")
for url in bg_urls:
    print(url)

print("\n--- OG IMAGES ---")
for img in og_images:
    print(img)

all_paths = []
for src in img_srcs:
    if "mc.yandex.ru" not in src and "googletagmanager" not in src:
        all_paths.append(src)
for url in bg_urls:
    all_paths.append(url)
for img in og_images:
    # extract relative path after domain
    rel = img.replace("https://eliteluxurybookings.com/", "/")
    all_paths.append(rel)

print("\n--- CHECKING EXISTENCE ---")
for p in set(all_paths):
    # remove leading slash if present to join with assets_dir
    clean_p = p.lstrip('/')
    if clean_p.startswith('assets/'):
        sub_p = clean_p[7:] # remove 'assets/'
        full_path = os.path.join(assets_dir, sub_p.replace('/', '\\'))
        exists = os.path.exists(full_path)
        print(f"Path: {p} -> {full_path} -> Exists: {exists}")
    else:
        print(f"Non-asset Path: {p}")
