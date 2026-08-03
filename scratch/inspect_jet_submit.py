import sys
import re

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

path = "premium-jet-charter.html"
with open(path, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

lines = content.split('\n')
for idx, line in enumerate(lines):
    if 'function submitLead' in line:
        for j in range(0, 30):
            print(f"{idx+j+1}: {lines[idx+j].strip()}")
        break
