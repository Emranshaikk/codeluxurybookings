import urllib.request
import re

urls = [
    "https://eliteluxurybookings.com/7-best-private-jet-charter-in-dubai/",
    "https://eliteluxurybookings.com/abudhabi-to-doha-private-jet-cost/"
]

for url in urls:
    try:
        print(f"\n--- Fetching {url} ---")
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8', errors='ignore')
        
        # Find the <head> section
        head_match = re.search(r'<head[^>]*>(.*?)</head>', html, re.DOTALL | re.IGNORECASE)
        if head_match:
            head_content = head_match.group(1)
            # Find all stylesheet links
            links = re.findall(r'<link[^>]*rel="stylesheet"[^>]*>', head_content, re.IGNORECASE)
            links2 = re.findall(r'<link[^>]*href="[^"]*"[^>]*>', head_content, re.IGNORECASE)
            
            print("Stylesheet links:")
            for link in links:
                print(f"  {link}")
            
            # Print first 200 chars of style tag if exists
            style_matches = re.findall(r'<style[^>]*>(.*?)</style>', head_content, re.DOTALL | re.IGNORECASE)
            print(f"Number of style tags: {len(style_matches)}")
            for i, style in enumerate(style_matches):
                print(f"  Style tag {i+1} first 200 chars: {style[:200].strip()}...")
        else:
            print("No head tag found.")
            
    except Exception as e:
        print(f"Error: {e}")
