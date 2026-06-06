import json

blog_data_path = r"c:\Users\imran\OneDrive\Desktop\ELB code\blog-data.json"

with open(blog_data_path, "r", encoding="utf-8") as f:
    data = json.load(f)

urls_to_check = [
    "/luxury-villa-rentals.html",
    "/private-island-for-rent.html",
    "/maldives-private-island-rental.html"
]

for entry in data:
    if entry.get("url") in urls_to_check:
        print(f"URL: {entry.get('url')}\nTitle: {entry.get('title')}\nExcerpt: '{entry.get('excerpt')}'\n")
