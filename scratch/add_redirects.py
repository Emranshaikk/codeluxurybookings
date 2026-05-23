import os
import re

directory = r'c:\Users\imran\OneDrive\Desktop\ELB code'
redirect_input = '<input type="hidden" name="_redirect" value="https://eliteluxurybookings.com/thank-you.html">'
form_pattern = re.compile(r'(<form\s+action="https://formspree.io/f/xwvwanlj"\s+method="POST"[^>]*>)', re.IGNORECASE)

files_updated = 0

for filename in os.listdir(directory):
    if filename.endswith('.html'):
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'formspree.io/f/xwvwanlj' in content:
            # Check if redirect already exists
            if '_redirect' in content and 'thank-you.html' in content:
                print(f"Skipping {filename}: Redirect already exists.")
                continue
            
            # Find the form tag and insert the redirect
            new_content = form_pattern.sub(r'\1\n                        ' + redirect_input, content)
            
            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Updated {filename}")
                files_updated += 1

print(f"Total files updated: {files_updated}")
