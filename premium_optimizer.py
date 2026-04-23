import os
import re

def optimize_all():
    files = [f for f in os.listdir('.') if f.endswith('.html')]
    count = 0
    for filename in files:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        changed = False
        
        # 1. Update Contrast (Internal Styles)
        if 'rgba(255, 255, 255, 0.75)' in content:
            content = content.replace('rgba(255, 255, 255, 0.75)', 'rgba(255, 255, 255, 0.85)')
            changed = True
        
        # 2. Async Fonts (Performance) - look for Google Fonts pattern
        if 'fonts.googleapis.com' in content and 'media="print"' not in content:
            # Replace the rel="stylesheet" part specifically for fonts
            content = re.sub(r'(href="https://fonts\.googleapis\.com/[^"]+" )rel="stylesheet"', r'\1rel="stylesheet" media="print" onload="this.media=\'all\'"', content)
            changed = True
        
        # 3. Optimize Image Sizing (w=1920 to w=1200)
        if 'w=1920' in content:
            content = content.replace('w=1920', 'w=1200')
            changed = True
        
        # 4. Accessibility Labels (Inputs)
        if '<input' in content and 'aria-label' not in content:
            content = re.sub(r'<input (?!.*aria-label)([^>]*)>', r'<input aria-label="Form Input" \1>', content)
            changed = True
        if '<select' in content and 'aria-label' not in content:
            content = re.sub(r'<select (?!.*aria-label)([^>]*)>', r'<select aria-label="Form Selection" \1>', content)
            changed = True
            
        if changed:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            count += 1
            
    print(f"Successfully optimized {count} files.")

if __name__ == "__main__":
    optimize_all()
