with open("sunreef-catamaran-charter-price.html", "r", encoding="utf-8", errors="ignore") as f:
    lines = f.readlines()
for i in range(470, 510):
    if i < len(lines):
        print(f"{i+1}: {lines[i].strip()}")
