import re

live_content_path = r"C:\Users\imran\.gemini\antigravity-ide\brain\396a10cd-35c6-476d-9347-22fae41e2038\.system_generated\steps\914\content.md"

with open(live_content_path, "r", encoding="utf-8") as f:
    content = f.read()

# Find all occurrences of assets/ without a leading slash
# Look at img src, background url, etc.
img_srcs = re.findall(r'src=["\']([^"\']+)["\']', content)
bg_urls = re.findall(r'url\(["\']?([^"\')]+)["\']?\)', content)

print("--- LIVE IMG SRCs ---")
for src in img_srcs:
    if "assets/" in src:
        print(f"src: {src} -> starts with slash: {src.startswith('/')}")

print("\n--- LIVE BG URLs ---")
for url in bg_urls:
    if "assets/" in url:
        print(f"url: {url} -> starts with slash: {url.startswith('/')}")
