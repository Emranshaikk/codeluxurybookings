import sys
import re

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

path = "bahamas-private-island-rental.html"
with open(path, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

match = re.search(r'function\s+handleInquirySubmit\b.*?\n\s*\n', content, re.S | re.I)
if not match:
    # try other pattern
    match = re.search(r'handleInquirySubmit\s*=\s*.*?\n\s*\n', content, re.S | re.I)
    
if match:
    print(match.group(0))
else:
    # let's find the function lines
    lines = content.split('\n')
    for idx, line in enumerate(lines):
        if 'handleInquirySubmit' in line:
            for j in range(0, 30):
                print(f"{idx+j+1}: {lines[idx+j].strip()}")
            break
