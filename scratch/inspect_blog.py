with open("blog.html", "r", encoding="utf-8", errors="ignore") as f:
    lines = f.readlines()
for i in range(0, 80):
    if i < len(lines):
        # strip tags for safe output
        print(f"{i+1}: {lines[i].strip()[:120]}")
