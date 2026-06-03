import os

files = [
    "all-inclusive-private-island-rental.html",
    "bahamas-private-island-rental.html",
    "caribbean-private-island-rental.html",
    "exclusive-private-island-rental.html",
    "luxury-private-island-rental.html",
    "maldives-private-island-rental.html",
    "private-island-for-rent.html"
]

directory = r"c:\Users\imran\OneDrive\Desktop\ELB code"

for filename in files:
    path = os.path.join(directory, filename)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        print(f"\n================ FILE: {filename} ================")
        # Title
        title = "MISSING"
        if "<title>" in content:
            title = content.split("<title>")[1].split("</title>")[0].strip()
        print(f"Title: {title}")
        
        # Description
        description = "MISSING"
        if 'name="description"' in content:
            description = content.split('name="description"')[1].split('content="')[1].split('"')[0].strip()
        elif "name='description'" in content:
            description = content.split("name='description'")[1].split("content='")[1].split("'")[0].strip()
        print(f"Description: {description}")
        
        # OG tags
        has_og = "og:title" in content
        print(f"Has Open Graph tags: {has_og}")
        
        # Twitter tags
        has_twitter = "twitter:card" in content
        print(f"Has Twitter tags: {has_twitter}")
        
        # Stylesheet link duplicates
        has_rel_css = 'href="style.css"' in content or "href='style.css'" in content
        has_root_css = 'href="/style.css"' in content or "href='/style.css'" in content
        print(f"Has style.css link: {has_rel_css}")
        print(f"Has /style.css link: {has_root_css}")
