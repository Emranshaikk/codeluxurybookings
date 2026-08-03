import os

path = r"c:\Users\imran\OneDrive\Desktop\ELB code\luxury-villa-rentals.html"
with open(path, 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

import re
print("Checking for numbers or currencies in villa page:")
print("Lines with '$':")
for line in text.split('\n'):
    if '$' in line or 'USD' in line or 'EUR' in line or '€' in line or 'price' in line or 'cost' in line or 'rate' in line:
        print(line.strip()[:100])
