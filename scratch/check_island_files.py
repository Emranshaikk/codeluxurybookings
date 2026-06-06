import os

assets_dir = r"c:\Users\imran\OneDrive\Desktop\ELB code\assets"
files = os.listdir(assets_dir)

print("Matching files in assets/ containing 'island':")
for f in files:
    if 'island' in f.lower():
        print(f)
