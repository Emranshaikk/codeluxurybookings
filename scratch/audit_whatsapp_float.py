import os
import re

directory = r"c:\Users\imran\OneDrive\Desktop\ELB code"
html_files = [f for f in os.listdir(directory) if f.endswith(".html")]

print(f"Total HTML files found: {len(html_files)}")

missing_element = []
has_element = []
gold_styled = []
green_styled = []
no_wa_float_class = []

# Regex patterns
wa_float_style_pat = re.compile(r'\.wa-float\s*\{([^}]+)\}', re.DOTALL)

for filename in html_files:
    path = os.path.join(directory, filename)
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        with open(path, 'r', encoding='latin-1') as f:
            content = f.read()
    
    # Check if HTML element for wa-float exists
    has_wa_float_el = "class=\"wa-float\"" in content or "class='wa-float'" in content or "class=wa-float" in content
    
    # Check style blocks for wa-float
    style_matches = wa_float_style_pat.findall(content)
    
    is_gold = False
    is_green = False
    if style_matches:
        for match in style_matches:
            if "#D4AF37" in match or "linear-gradient" in match or "gold" in match:
                is_gold = True
            if "#25D366" in match:
                is_green = True
    
    if has_wa_float_el:
        has_element.append(filename)
    else:
        missing_element.append(filename)
        
    if is_gold:
        gold_styled.append(filename)
    if is_green:
        green_styled.append(filename)

print(f"\nSummary:")
print(f"Files with wa-float element: {len(has_element)}")
print(f"Files missing wa-float element: {len(missing_element)}")
print(f"Files with gold wa-float styles: {len(gold_styled)}")
print(f"Files with green wa-float styles: {len(green_styled)}")

print("\nSample missing elements (first 20):")
for f in missing_element[:20]:
    print(f" - {f}")

print("\nSample gold styled (first 20):")
for f in gold_styled[:20]:
    print(f" - {f}")
