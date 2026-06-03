import re
import os

def check_styles():
    filepath = r"c:\Users\imran\OneDrive\Desktop\ELB code\yacht-charter-available-now.html"
    if not os.path.exists(filepath):
        print("File not found")
        return
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    lines = content.split('\n')
    errors = 0
    for idx, line in enumerate(lines):
        line_num = idx + 1
        # Find all style="..." attributes
        matches = re.findall(r'style="([^"]*)"', line)
        for match in matches:
            # Check for common mistakes: class names inside style
            # Classes like mb-4, p-4, mt-4, font-bold etc. usually do not contain a colon.
            # Inline styles should be name:value declarations separated by semicolons.
            declarations = match.split(';')
            for dec in declarations:
                dec = dec.strip()
                if not dec:
                    continue
                if ':' not in dec:
                    print(f"Potential Syntax Error on Line {line_num}:")
                    print(f"  Line content: {line.strip()}")
                    print(f"  Style Attribute: style=\"{match}\"")
                    print(f"  Failed declaration (missing colon): '{dec}'")
                    print("-" * 50)
                    errors += 1
                    
    print(f"Style check completed. Found {errors} potential inline style errors.")

if __name__ == "__main__":
    check_styles()
