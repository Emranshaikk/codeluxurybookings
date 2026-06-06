import json

with open(r"c:\Users\imran\OneDrive\Desktop\ELB code\blog-data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for idx, entry in enumerate(data):
    if "private_island_hero.jpg" in str(entry):
        print(f"Index {idx}: {entry}")
