import os
import re

root_dir = r"c:\Users\imran\OneDrive\Desktop\ELB code"

# 1. Fix the JS on the home page (index.html)
home_idx = os.path.join(root_dir, "index.html")
if os.path.exists(home_idx):
    with open(home_idx, "r", encoding="utf-8") as f:
        html = f.read()

    # Replace JSON fetch with urlencoded fetch for GAS support
    old_fetch1 = """            try {
                await fetch(endpoint, {
                    method: 'POST', mode: 'no-cors',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });"""
    new_fetch1 = """            try {
                const urlParams = new URLSearchParams(data).toString();
                await fetch(endpoint, {
                    method: 'POST', mode: 'no-cors',
                    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                    body: urlParams
                });"""
    html = html.replace(old_fetch1, new_fetch1)

    with open(home_idx, "w", encoding="utf-8") as f:
        f.write(html)
    print("Fixed home page forms.")

# 2. Add Valens Affiliate iframe to routes pages
valens_iframe = '''
                <div class="valens-widget" style="width: 100%; border-radius: 12px; overflow: hidden; height: 600px;">
                    <iframe src="https://valens.jetluxe.com/?AffiliateID=elbookings" width="100%" height="100%" frameborder="0" style="border:none; background:#fff;"></iframe>
                </div>
'''

modified = 0
for subdir, dirs, files in os.walk(root_dir):
    if "-private-jet" in subdir:
        for file in files:
            if file == "index.html":
                filepath = os.path.join(subdir, file)
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # Replace the form-container AND success-panel with the iframe
                pattern = r'<div id="form-container">.*?</div>\s*<div id="success-panel".*?</div>'
                new_content, count = re.subn(pattern, valens_iframe.strip(), content, flags=re.DOTALL)
                
                # Clean up old JS variables for tripForm
                js_pattern = r"const ENDPOINT =.*?document\.querySelectorAll\('\.current-year'\)\.forEach.*?;"
                new_content, c2 = re.subn(js_pattern, "// Valens Affiliate Embed Loaded", new_content, flags=re.DOTALL)
                
                if count > 0:
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    modified += 1

print(f"Injected Valens iframe into {modified} route pages.")
