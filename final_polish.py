import os
import re

def final_polish():
    html_files = [f for f in os.listdir('.') if f.endswith('.html')]
    count = 0
    for filename in html_files:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        changed = False
        
        # 1. Async Fonts (Performance)
        # We target the rel="stylesheet" that follows a Google Fonts link
        if 'fonts.googleapis.com' in content and 'media="print"' not in content:
            # Simple replacement for the first occurrence which is usually the fonts
            content = content.replace('rel="stylesheet"', 'rel="stylesheet" media="print" onload="this.media=\'all\'"', 1)
            changed = True
            
        if changed:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            count += 1
    print(f"Final polish applied to {count} files.")

if __name__ == "__main__":
    final_polish()
