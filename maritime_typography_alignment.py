import os
import re

def maritime_typography_alignment():
    count = 0
    
    for root, dirs, files in os.walk("."):
        for file in files:
            if file == "index.html":
                filepath = os.path.join(root, file)
                if not ("yacht" in root.lower() or "boat" in root.lower() or "yacht" in file.lower() or "luxury-yacht" in root.lower()):
                    continue

                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                original = content
                
                # 1. Apply Elite Typography to Headers
                content = re.sub(r'<h2(.*?)>(.*?)</h2>', r'<h2\1 class="serif">\2</h2>', content)
                content = re.sub(r'<h3(.*?)>(.*?)</h3>', r'<h3\1 class="serif gold-text">\2</h3>', content)
                
                # Deduplicate class injection in case it's already there
                content = content.replace('class=""', '')
                content = content.replace('class="serif" class="serif"', 'class="serif"')
                
                # 2. Re-enforce Luxury List Standard (Replacing plain text checkmarks)
                content = content.replace('✓', '') # Kill the plain text checkmark
                if '<ul' in content and 'luxury-list' not in content:
                    content = re.sub(r'<ul(.*?)>', r'<ul\1 class="luxury-list">', content)

                # 3. Final Orderly Spacing Check
                # Ensure the blog-content is properly containerized
                if '<div class="blog-content"' in content and 'serif' not in content:
                     # This helps catch pages where my previous script added the wrapper but forgot the internal styling
                     content = content.replace('<h2>', '<h2 class="serif">').replace('<h3>', '<h3 class="serif gold-text">')

                if content != original:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    count += 1

    print(f"Maritime Typography Aligned: {count} pages brought to Elite Visual Standard.")

if __name__ == "__main__":
    maritime_typography_alignment()
