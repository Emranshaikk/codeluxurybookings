import urllib.request
import json

url = "https://eliteluxurybookings.com/blog-data.json"
req = urllib.request.Request(
    url, 
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
)

try:
    response = urllib.request.urlopen(req)
    data = json.loads(response.read().decode('utf-8'))
    
    urls_to_check = [
        "/luxury-villa-rentals.html",
        "/private-island-for-rent.html",
        "/maldives-private-island-rental.html"
    ]
    
    print("--- LIVE BLOG-DATA.JSON ---")
    for entry in data:
        if entry.get("url") in urls_to_check:
            print(f"URL: {entry.get('url')}\nTitle: {entry.get('title')}\nExcerpt: '{entry.get('excerpt')}'\n")
            
except Exception as e:
    print(f"Error: {e}")
