import os
import re
import xml.etree.ElementTree as ET

# Root directory of codebase
ROOT_DIR = r"c:\Users\imran\OneDrive\Desktop\ELB code"

# Get all local html files and their slugs
html_files = [f for f in os.listdir(ROOT_DIR) if f.endswith(".html")]
local_slugs = set()
for f in html_files:
    slug = f[:-5] # remove '.html'
    if slug == "index":
        local_slugs.add("")
        local_slugs.add("index")
    else:
        local_slugs.add(slug)

VALID_EXCEPTIONS = {
    "submit-lead.php",
    "robots.txt",
    "sitemap.xml",
    "favicon.png",
    "favicon.ico",
    "zoho-domain-verification.html",
    "zohoverify.html",
    "verifyforzoho.html"
}

def is_asset(href):
    # Ignore static assets, social media, external sites
    href_lower = href.lower()
    if any(ext in href_lower for ext in [".css", ".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg", ".js", ".json", ".ico"]):
        return True
    if "assets/" in href_lower:
        return True
    return False

# 1. Parse sitemap.xml
sitemap_path = os.path.join(ROOT_DIR, "sitemap.xml")
sitemap_broken_urls = []
sitemap_urls_count = 0

if os.path.exists(sitemap_path):
    try:
        tree = ET.parse(sitemap_path)
        root = tree.getroot()
        ns = ""
        if root.tag.startswith("{"):
            ns = root.tag.split("}")[0] + "}"
        
        for url_node in root.findall(f"{ns}url"):
            loc_node = url_node.find(f"{ns}loc")
            if loc_node is not None:
                url = loc_node.text.strip()
                sitemap_urls_count += 1
                if url.startswith("https://eliteluxurybookings.com"):
                    path = url.replace("https://eliteluxurybookings.com", "").strip("/")
                    if path not in local_slugs and path not in VALID_EXCEPTIONS:
                        sitemap_broken_urls.append((url, path))
    except Exception as e:
        print(f"Error parsing sitemap.xml: {e}")

print(f"Total HTML files in workspace: {len(html_files)}")
print(f"Total URLs in sitemap.xml: {sitemap_urls_count}")
print(f"Broken URLs in sitemap.xml: {len(sitemap_broken_urls)}")
for url, path in sitemap_broken_urls:
    print(f"  - {url} (slug: '{path}')")

# 2. Parse HTML files for broken page links
broken_links_by_file = {}
checked_links_count = 0
broken_links_count = 0

for filename in html_files:
    filepath = os.path.join(ROOT_DIR, filename)
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        hrefs = re.findall(r'href=["\']([^"\']+)["\']', content)
        
        for href in hrefs:
            if is_asset(href):
                continue
                
            is_internal = False
            path_part = ""
            
            if href.startswith("/") and not href.startswith("//"):
                is_internal = True
                path_part = href.split("?")[0].split("#")[0].strip("/")
            elif href.startswith("https://eliteluxurybookings.com"):
                is_internal = True
                path_part = href.replace("https://eliteluxurybookings.com", "").split("?")[0].split("#")[0].strip("/")
            elif not href.startswith("http") and not href.startswith("mailto:") and not href.startswith("tel:") and not href.startswith("javascript:") and not href.startswith("#") and not href.startswith("ws:") and not href.startswith("wss:"):
                is_internal = True
                path_part = href.split("?")[0].split("#")[0].strip("/")
            
            if is_internal:
                checked_links_count += 1
                test_slug = path_part
                if test_slug.endswith(".html"):
                    test_slug = test_slug[:-5]
                
                if test_slug == "":
                    continue
                
                if test_slug not in local_slugs and path_part not in VALID_EXCEPTIONS and href not in VALID_EXCEPTIONS:
                    broken_links_count += 1
                    if filename not in broken_links_by_file:
                        broken_links_by_file[filename] = []
                    broken_links_by_file[filename].append(href)
    except Exception as e:
        print(f"Error reading {filename}: {e}")

print(f"\nTotal page links checked: {checked_links_count}")
print(f"Total broken page links: {broken_links_count}")
print("Broken page links detail (grouped by source file):")
for source_file, hrefs in sorted(broken_links_by_file.items()):
    print(f"In [ {source_file} ]:")
    for href in set(hrefs):
        print(f"  - {href}")
