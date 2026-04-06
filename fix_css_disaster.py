import os
import re

root_dir = r"c:\Users\imran\OneDrive\Desktop\ELB code"
old_index = os.path.join(root_dir, "index_old.txt")
css_dir = os.path.join(root_dir, "assets", "css")
css_file = os.path.join(css_dir, "style.css")

# 1. Read the old index and extract the massive style block
with open(old_index, "r", encoding="utf-8") as f:
    content = f.read()

# We know the master style starts after google fonts and ends before google analytics
# Let's extract the first major <style> block
match = re.search(r'<style>(\s*:root.*?)</style>', content, re.DOTALL)
if match:
    master_css = match.group(1)
    os.makedirs(css_dir, exist_ok=True)
    with open(css_file, "w", encoding="utf-8") as f:
        f.write("/* MASTER ELB STYLE - AUTO-EXTRACTED */\n")
        f.write(master_css)
    print(f"Extracted {len(master_css)} bytes of CSS to {css_file}")
else:
    print("Could not find master CSS in index_old.txt")
    exit(1)

link_tag = '<link rel="stylesheet" href="/assets/css/style.css">'

# 2. Inject it into all HTML pages
modified_count = 0
for subdir, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith(".html"):
            filepath = os.path.join(subdir, file)
            with open(filepath, "r", encoding="utf-8") as f:
                html = f.read()

            if link_tag not in html:
                # Insert before </head>
                if "</head>" in html:
                    html = html.replace("</head>", f"    {link_tag}\n</head>")
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(html)
                    modified_count += 1

print(f"Injected master style.css into {modified_count} files.")
