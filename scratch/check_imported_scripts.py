import sys
from bs4 import BeautifulSoup

# Ensure stdout uses UTF-8
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

path = "premium-jet-charter.html"
with open(path, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

soup = BeautifulSoup(content, 'html.parser')
scripts = soup.find_all('script')

print(f"Found {len(scripts)} scripts in premium-jet-charter.html:")
for s in scripts:
    src = s.get('src', '')
    if src:
        print(f"  External: {src}")
    else:
        text = s.string if s.string else ""
        print(f"  Inline script block (length: {len(text)}) | content starts with: {text.strip()[:100]}...")
