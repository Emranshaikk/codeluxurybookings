import os
import re

def universal_lead_fix():
    count = 0
    
    # 1. Patterns to identify and replace
    json_header = r"headers:\s*{\s*'Content-Type':\s*'application/json'\s*}"
    url_header = "headers: { 'Content-Type': 'application/x-www-form-urlencoded' }"
    
    json_body = r"body:\s*JSON\.stringify\(data\)"
    url_body = "body: new URLSearchParams(data).toString()"
    
    success_conditional = r"if\s*\(response\.ok\)\s*\{(.*?)\}"
    
    # 2. Targeted replacement logic
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.html'):
                path = os.path.join(root, file)
                
                # Skip known libraries/assets
                if any(x in root for x in ['assets', 'node_modules', '.git']):
                    continue
                
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    original = content
                    
                    # Fix Protocol (JSON to URL-Encoded)
                    content = re.sub(json_header, url_header, content)
                    content = re.sub(json_body, url_body, content)
                    
                    # Fix Success Trigger (Remove if(response.ok) block but keep the interior)
                    # We look for the standard block used in your templates
                    if "if (response.ok)" in content:
                        # Extract the inner logic and place it outside the condition
                        # Pattern targets the most common route/template style
                        matches = re.findall(success_conditional, content, re.DOTALL)
                        for match in matches:
                            # We replace the whole if block with its contents
                            # This ensures the UI updates (msg visible, form hidden) happen immediately
                            content = re.sub(success_conditional, match.strip(), content, flags=re.DOTALL)

                    if content != original:
                        with open(path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        count += 1
                        
                except Exception as e:
                    print(f"Error on {path}: {e}")

    print(f"Elite Global Conversion Lock: Standardized {count} lead capture points site-wide.")

if __name__ == "__main__":
    universal_lead_fix()
