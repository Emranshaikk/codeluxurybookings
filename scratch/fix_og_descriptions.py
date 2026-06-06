import os
import re

workspace_dir = r"c:\Users\imran\OneDrive\Desktop\ELB code"
html_files = [f for f in os.listdir(workspace_dir) if f.endswith('.html')]

print(f"Auditing meta descriptions in {len(html_files)} HTML files...")

fixed_files = []

for filename in html_files:
    filepath = os.path.join(workspace_dir, filename)
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
        
    # Extract meta description
    # Match content inside double quotes or single quotes
    desc_match = re.search(r'<meta name="description"\s+content=["\']([^"\']+)["\']', content, re.IGNORECASE)
    if not desc_match:
        # Try alternate attribute order
        desc_match = re.search(r'<meta content=["\']([^"\']+)["\']\s+name="description"', content, re.IGNORECASE)
        
    if not desc_match:
        continue
        
    main_desc = desc_match.group(1).strip()
    
    modified = False
    
    # Check and replace og:description
    og_desc_match = re.search(r'<meta property="og:description"\s+content=["\']([^"\']+)["\']', content, re.IGNORECASE)
    if og_desc_match:
        og_desc = og_desc_match.group(1).strip()
        if og_desc != main_desc and len(og_desc) < len(main_desc):
            # Replace it
            target = og_desc_match.group(0)
            replacement = f'<meta property="og:description" content="{main_desc}"'
            # Preserve original quote format
            if '"' in target:
                replacement = f'<meta property="og:description" content="{main_desc}">'
            else:
                replacement = f"<meta property='og:description' content='{main_desc}'>"
                
            content = content.replace(target, replacement)
            modified = True
            print(f"  [{filename}] Fixed og:description: '{og_desc}' -> '{main_desc[:30]}...'")
            
    # Check and replace twitter:description
    tw_desc_match = re.search(r'<meta name="twitter:description"\s+content=["\']([^"\']+)["\']', content, re.IGNORECASE)
    if tw_desc_match:
        tw_desc = tw_desc_match.group(1).strip()
        if tw_desc != main_desc and len(tw_desc) < len(main_desc):
            # Replace it
            target = tw_desc_match.group(0)
            replacement = f'<meta name="twitter:description" content="{main_desc}">'
            content = content.replace(target, replacement)
            modified = True
            print(f"  [{filename}] Fixed twitter:description: '{tw_desc}' -> '{main_desc[:30]}...'")
            
    if modified:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        fixed_files.append(filename)

print(f"\nCompleted! Fixed meta descriptions in {len(fixed_files)} files.")
