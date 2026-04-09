import re

targets = ['global-route-silo', 'global-yacht-silo']

files = [
    (r'c:\Users\imran\OneDrive\Desktop\ELB code\blog\index\index.html', 'utf-8'),
    (r'c:\Users\imran\OneDrive\Desktop\ELB code\blog\index.html', 'latin-1'),
]

for filepath, enc in files:
    with open(filepath, encoding=enc, errors='replace') as f:
        content = f.read()

    before = sum(content.count(t) for t in targets)

    for slug in targets:
        # Remove the full <a href="/slug/"> ... </a> card block
        pattern = r'\s*<a[^>]*href="/' + slug + r'/"[^>]*>.*?</a>'
        content = re.sub(pattern, '', content, flags=re.DOTALL)

    after = sum(content.count(t) for t in targets)
    print(f'{filepath}: removed {before - after} silo references')

    with open(filepath, 'w', encoding=enc) as f:
        f.write(content)

print('Done!')
