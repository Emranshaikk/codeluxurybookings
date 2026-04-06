import os
import re

def metadata_sync():
    # Only target the Nurture hubs we just switched to Formspree
    target_files = [
        'contact/index.html',
        'luxury-villa-rentals/index.html',
        'luxury-yacht-rentals/index.html'
    ]
    
    metadata_snippet = """            data['_subject'] = f"Elite Concierge Inquiry: {data.get('services', 'General Service')}";
            data['_replyto'] = data.get('email');"""

    for target in target_files:
        path = os.path.join('.', target)
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original = content
                
                # Find the form data loop and insert metadata
                pattern = r"formData\.forEach\(\(value, key\) => data\[key\] = value\);"
                if re.search(pattern, content):
                    # For Contact page or Villa hub which uses direct data mapping
                    replacement = "formData.forEach((value, key) => data[key] = value);\n            data['_subject'] = `Elite Inquiry: ${data.services || 'General'}`;\n            data['_replyto'] = data.email;"
                    content = re.sub(pattern, replacement, content)
                
                if content != original:
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(content)
                        
            except Exception as e:
                print(f"Error on {path}: {e}")

if __name__ == "__main__":
    metadata_sync()
