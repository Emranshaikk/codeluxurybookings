import sys
import re

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

path = "elite-private-jet-charter.html"
with open(path, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

lines = content.split('\n')
for idx, line in enumerate(lines):
    if 'async function submitLead' in line or 'function submitLead' in line:
        for j in range(0, 100):
            if idx+j < len(lines):
                # replace emoji for safe print
                cleaned = re.sub(r'[^\x00-\x7F]+', '?', lines[idx+j])
                print(f"{idx+j+1}: {cleaned.strip()}")
                if '</script>' in lines[idx+j]:
                    break
        break
