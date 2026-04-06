import os
import subprocess

root_dir = r"c:\Users\imran\OneDrive\Desktop\ELB code"
link_tag = '<link rel="stylesheet" href="/assets/css/style.css">'

restored_count = 0
injected_count = 0

for subdir, dirs, files in os.walk(root_dir):
    if "-private-jet" in subdir:
        for file in files:
            if file == "index.html":
                filepath = os.path.join(subdir, file)
                
                # 1. Restore the file with git
                rel_path = os.path.relpath(filepath, root_dir)
                subprocess.run(["git", "checkout", "--", rel_path], cwd=root_dir)
                restored_count += 1
                
                # 2. Inject CSS string
                with open(filepath, "r", encoding="utf-8") as f:
                    html = f.read()

                if link_tag not in html:
                    if "</head>" in html:
                        html = html.replace("</head>", f"    {link_tag}\n</head>")
                        with open(filepath, "w", encoding="utf-8") as f:
                            f.write(html)
                        injected_count += 1

print(f"Restored forms for {restored_count} pages and injected CSS into {injected_count} pages.")
