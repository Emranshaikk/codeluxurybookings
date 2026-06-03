import os

path = r"c:\Users\imran\OneDrive\Desktop\ELB code\all-inclusive-private-island-rental.html"
with open(path, 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if "wa-float" in line or "whatsapp" in line.lower() or "wa.me" in line:
        print(f"Line {idx+1}: {line.strip()}")
