import os
import re

workspace_dir = r"c:\Users\imran\OneDrive\Desktop\ELB code"
html_files = [f for f in os.listdir(workspace_dir) if f.endswith('.html')]

print(f"Auditing meta descriptions in {len(html_files)} HTML files using robust multi-line parser...")

fixed_files = []

for filename in html_files:
    filepath = os.path.join(workspace_dir, filename)
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
        
    # Extract main description using a robust regex that handles newlines/whitespace
    # Match <meta name="description" content="..." > in any order, multi-line
    # We can match name="description" and then content="...", or vice-versa
    
    # Clean up any potential newline issues in search
    # Let's search for content in the description tag
    desc_content = None
    
    # 1. Search for <meta ... name="description" ...>
    # Find all <meta ...> tags
    meta_tags = re.findall(r'<meta\s+[^>]+>', content, re.IGNORECASE | re.DOTALL)
    
    for tag in meta_tags:
        # Check if this is the description tag
        if re.search(r'name=["\']description["\']', tag, re.IGNORECASE):
            content_match = re.search(r'content=["\']([^"\']+)["\']', tag, re.IGNORECASE | re.DOTALL)
            if content_match:
                desc_content = content_match.group(1).strip()
                # Remove newlines and collapse multiple spaces inside the description
                desc_content = re.sub(r'\s+', ' ', desc_content)
                break
                
    if not desc_content:
        continue
        
    modified = False
    
    # Look for og:description tag
    for tag in meta_tags:
        if re.search(r'property=["\']og:description["\']', tag, re.IGNORECASE):
            content_match = re.search(r'content=["\']([^"\']+)["\']', tag, re.IGNORECASE | re.DOTALL)
            if content_match:
                og_desc = content_match.group(1).strip()
                og_desc_clean = re.sub(r'\s+', ' ', og_desc)
                if og_desc_clean != desc_content and len(og_desc_clean) < len(desc_content):
                    # Replace in content
                    # Form a clean tag
                    new_tag = f'<meta property="og:description" content="{desc_content}">'
                    content = content.replace(tag, new_tag)
                    modified = True
                    print(f"  [{filename}] Fixed og:description: '{og_desc}' -> '{desc_content[:30]}...'")
                    
        # Look for twitter:description tag
        if re.search(r'name=["\']twitter:description["\']', tag, re.IGNORECASE):
            content_match = re.search(r'content=["\']([^"\']+)["\']', tag, re.IGNORECASE | re.DOTALL)
            if content_match:
                tw_desc = content_match.group(1).strip()
                tw_desc_clean = re.sub(r'\s+', ' ', tw_desc)
                if tw_desc_clean != desc_content and len(tw_desc_clean) < len(desc_content):
                    new_tag = f'<meta name="twitter:description" content="{desc_content}">'
                    content = content.replace(tag, new_tag)
                    modified = True
                    print(f"  [{filename}] Fixed twitter:description: '{tw_desc}' -> '{desc_content[:30]}...'")
                    
    if modified:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        fixed_files.append(filename)

print(f"\nCompleted! Fixed meta descriptions in {len(fixed_files)} files.")
