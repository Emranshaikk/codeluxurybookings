import os
import re

def tighten_maritime_spacing():
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
                
                # 1. Tighten the Hero section (H1 to Form)
                content = content.replace('style="margin-bottom: 2.5rem;"', 'style="margin-bottom: 1.5rem;"') # Tag-strip
                content = content.replace('style="margin: 2rem auto 2rem;', 'style="margin: 1.5rem auto 1.5rem;') # Urgency alert
                content = content.replace('style="margin: 0 auto 4rem;', 'style="margin: 0 auto 2.5rem;') # Lead Hub
                
                # 2. Tighten the Partner Footer section
                content = content.replace('style="margin: 4rem auto 2rem;', 'style="margin: 2.5rem auto 1.5rem;')
                content = content.replace('padding-top: 3rem;"', 'padding-top: 2rem;"')
                
                # 3. Tighten the global section-padding class if it exists inline
                content = content.replace('class="section-padding"', 'class="section-padding" style="padding: 3rem 0 !important;"')

                if content != original:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    count += 1

    print(f"Maritime Spacing Tightened: {count} pages brought to the Refined Elite Standard.")

if __name__ == "__main__":
    tighten_maritime_spacing()
