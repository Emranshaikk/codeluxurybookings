import re

fname = 'business-jet-charter-guide-tips-pricing.html'
with open(fname, 'r', encoding='utf-8') as f:
    c = f.read()

old_url = 'https://eliteluxurybookings.com/business-jet-charter-guide-tips-pricing.html'
new_url = 'https://eliteluxurybookings.com/business-jet-charter-guide-tips-pricing/'
c2 = c.replace(old_url, new_url)
if c2 != c:
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(c2)
    print(f'Fixed canonical in {fname}')
else:
    m = re.search(r'rel="canonical" href="([^"]+)"', c)
    print(f'Current canonical: {m.group(1) if m else "NOT FOUND"}')
    print('No change needed or already correct')
