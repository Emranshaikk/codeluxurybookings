import os
import re

def search_styling():
    with open('elite-private-jet-charter.html', 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        
    # Find all styles block
    styles = re.findall(r'<style[^>]*>(.*?)</style>', content, re.DOTALL | re.IGNORECASE)
    
    # We want to search for selectors like "footer", "p", "brand", "center", etc.
    keywords = ['footer', 'brand', 'p {', 'p,', ',p', 'cormorant']
    
    print("=== Style Rules in elite-private-jet-charter.html ===")
    for style in styles:
        lines = style.split('\n')
        for i, line in enumerate(lines):
            for kw in keywords:
                if kw in line.lower():
                    # Print context of 5 lines before and after
                    start = max(0, i - 3)
                    end = min(len(lines), i + 4)
                    print(f"Context (lines {start}-{end}):")
                    for j in range(start, end):
                        print(f"  {j}: {lines[j]}")
                    print("-" * 30)
                    break

if __name__ == '__main__':
    search_styling()
