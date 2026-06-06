import os
import json
import re

workspace_dir = r"c:\Users\imran\OneDrive\Desktop\ELB code"
json_path = os.path.join(workspace_dir, "blog-data.json")

with open(json_path, 'r', encoding='utf-8') as f:
    blog_data = json.load(f)

updated_count = 0

for item in blog_data:
    url = item.get('url', '')
    excerpt = item.get('excerpt', '')
    
    # Check if the excerpt is very short
    if url.endswith('.html') and len(excerpt.strip()) < 30:
        filename = url.strip('/')
        filepath = os.path.join(workspace_dir, filename)
        
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                html_content = f.read()
                
            # Regex designed to match either double-quoted content or single-quoted content
            # e.g., content="value" or content='value'
            # We match content="([^"]+)" or content='([^']+)'
            # Let's locate the meta tag with name="description"
            # Since the tag might span multiple lines, we can search globally in the header.
            meta_match = re.search(r'<meta\s+[^>]*name=["\']description["\'][^>]*>', html_content, re.IGNORECASE | re.DOTALL)
            if not meta_match:
                # Try search with content before name
                meta_match = re.search(r'<meta\s+[^>]*content=["\'][^"\']+["\'][^>]*name=["\']description["\'][^>]*>', html_content, re.IGNORECASE | re.DOTALL)
                
            if meta_match:
                meta_tag = meta_match.group(0)
                # Now extract content from this specific tag
                content_match = re.search(r'content="([^"]+)"', meta_tag, re.IGNORECASE)
                if not content_match:
                    content_match = re.search(r"content='([^']+)'", meta_tag, re.IGNORECASE)
                
                if content_match:
                    full_desc = content_match.group(1).strip()
                    item['excerpt'] = full_desc
                    print(f"Updated {filename}:")
                    print(f"  Old excerpt: '{excerpt}'")
                    print(f"  New excerpt: '{full_desc}'")
                    updated_count += 1
                else:
                    print(f"Could not extract content attribute in meta tag of {filename}")
            else:
                print(f"Could not find meta description tag in {filename}")
        else:
            print(f"File not found: {filename}")

# Save the updated blog-data.json
if updated_count > 0:
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(blog_data, f, indent=4, ensure_ascii=False)
    print(f"\nSuccessfully updated {updated_count} entries in blog-data.json.")
else:
    print("\nNo entries needed updating.")
