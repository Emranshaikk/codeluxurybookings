import os
import re
from bs4 import BeautifulSoup
import sys

# Ensure stdout uses UTF-8
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

path = r"c:\Users\imran\OneDrive\Desktop\ELB code\about.html"
with open(path, 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

print("Searching for testimonials/endorsements/quotes in about.html:")
print("=" * 80)

# Check blockquotes or paragraphs with quotes
quotes = soup.find_all(['blockquote', 'q'])
print(f"Found {len(quotes)} blockquote/q elements:")
for q in quotes:
    print(f"  Tag: {q.name} | Text: {q.get_text().strip()[:100]}...")

# Check for divs/panels containing quote-like text
panels = soup.find_all(class_=re.compile(r'testimonial|quote|endorse|glass', re.I))
print(f"Found {len(panels)} panels matching class patterns:")
for p in panels[:10]:
    txt = p.get_text().strip()
    if len(txt) > 20:
        print(f"  Class: {p.get('class')} | Text: {txt[:100]}...")

# Let's search raw html for lines containing "Partner" or "Client" or "Endorsement" to see what's going on
print("\nRaw HTML lines containing 'Partner' or 'Client':")
lines = html.split('\n')
for i, line in enumerate(lines):
    if any(k in line.lower() for k in ['partner', 'client', 'endorse', 'quote']):
        # strip tags for safe printing
        clean_l = re.sub(r'<[^>]+>', ' ', line).strip()
        clean_l = re.sub(r'\s+', ' ', clean_l)
        if len(clean_l) > 10:
            print(f"  Line {i+1}: {clean_l[:120]}")
