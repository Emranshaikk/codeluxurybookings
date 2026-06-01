import os

files = [
    r"c:\Users\imran\OneDrive\Desktop\ELB code\private-island-for-rent.html",
    r"c:\Users\imran\OneDrive\Desktop\ELB code\partners.html",
    r"c:\Users\imran\OneDrive\Desktop\ELB code\about.html"
]

queries = ["isca", "12", "people", "guests", "capacity"]

for file_path in files:
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        continue
    print(f"\nSearching in {os.path.basename(file_path)}:")
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    for idx, line in enumerate(lines):
        line_lower = line.lower()
        for q in queries:
            if q in line_lower:
                print(f"Line {idx+1}: {line.strip()[:120]}")
                break
