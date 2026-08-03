import sys
import re

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

path = "contact.html"
with open(path, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

lines = content.split('\n')
for i, line in enumerate(lines):
    if any(k in line.lower() for k in ['whatsapp', 'email', 'phone', 'address', 'tel:', 'mailto:']):
        cleaned = re.sub(r'<[^>]+>', ' ', line).strip()
        cleaned = re.sub(r'\s+', ' ', cleaned)
        cleaned = ''.join(c if ord(c) < 128 else '?' for c in cleaned)
        if len(cleaned) > 5:
            print(f"Line {i+1}: {cleaned[:120]}")
