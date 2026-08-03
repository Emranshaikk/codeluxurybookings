import sys
import re

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

path = "mallorca-to-ibiza-private-boat.html"
with open(path, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

lines = content.split('\n')
for idx, line in enumerate(lines):
    if 'async function handleEnquiry' in line:
        for j in range(0, 100):
            print(f"{idx+j+1}: {re.sub(r'[^\x00-\x7F]+', '?', lines[idx+j].strip())}")
            if 'cost-comparison' in lines[idx+j].lower():
                break
        break
