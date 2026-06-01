import os
import re

workspace_dir = r"c:\Users\imran\OneDrive\Desktop\ELB code"

html_files = [f for f in os.listdir(workspace_dir) if f.endswith(".html")]
print(f"Found {len(html_files)} HTML files to process.")

favicon_tag = '    <link rel="icon" type="image/png" href="/favicon.png">\n'
fixed_files = []
already_have = []

for file_name in html_files:
    file_path = os.path.join(workspace_dir, file_name)
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    # Check specifically if there is an actual HTML link tag for the icon
    # Search for <link ... rel="icon" ...> or <link ... rel='icon' ...> or <link ... rel="shortcut icon" ...>
    has_icon_link = False
    
    # Let's search using a regular expression for a link tag with rel containing "icon"
    if re.search(r'<link[^>]+rel=["\'](?:shortcut\s+)?icon["\'][^>]*>', content, re.IGNORECASE):
        has_icon_link = True
    elif re.search(r'<link[^>]+href=["\'][^"\']*favicon\.(?:png|ico)["\'][^>]*>', content, re.IGNORECASE):
        has_icon_link = True

    if has_icon_link:
        already_have.append(file_name)
        continue

    # Find the head tag and insert the favicon link right after <head>
    head_match = re.search(r"<head[^>]*>", content, re.IGNORECASE)
    if head_match:
        pos = head_match.end()
        new_content = content[:pos] + "\n" + favicon_tag + content[pos:]
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        fixed_files.append(file_name)
    else:
        print(f"Warning: No <head> tag found in {file_name}")

print(f"\nAlready had favicon link: {len(already_have)}")
print(f"Added favicon link to: {len(fixed_files)}")
print(f"Fixed files: {fixed_files}")
