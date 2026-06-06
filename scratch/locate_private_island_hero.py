import re
import os

workspace_dir = r"c:\Users\imran\OneDrive\Desktop\ELB code"
html_files = [f for f in os.listdir(workspace_dir) if f.endswith('.html')]

for filename in html_files:
    filepath = os.path.join(workspace_dir, filename)
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()
        for idx, line in enumerate(lines):
            if "private_island_hero" in line:
                print(f"{filename}:{idx+1}: {line.strip()}")
