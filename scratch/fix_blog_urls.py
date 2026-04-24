import json
import re

file_path = r'c:\Users\imran\OneDrive\Desktop\ELB code\blog-data.json'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace trailing slash URLs with .html URLs in the JSON content
# Specifically targeting the "url" value
new_content = re.sub(r'("url":\s*"/([^"]+)/")', r'"url": "/\2.html"', content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Successfully updated blog-data.json URLs.")
