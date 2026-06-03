import os
import re

path = r"c:\Users\imran\OneDrive\Desktop\ELB code\all-inclusive-private-island-rental.html"
with open(path, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# find all absolute or relative links to other island pages
links = re.findall(r'href="([^"]*island-rental[^"]*)"', content)
links += re.findall(r'href="([^"]*island-for-rent[^"]*)"', content)
print("Found links:")
for l in set(links):
    print(f" - {l}")
