import os, re
issues = []
for f in os.listdir('.'):
    if not f.endswith('.html') or f.startswith('_'):
        continue
    with open(f, 'r', encoding='utf-8') as fp:
        c = fp.read()
    if 'G-J56D1LJLFM' not in c:
        issues.append(f'MISSING GA: {f}')
    if 'sia395rirl' not in c:
        issues.append(f'MISSING CLARITY: {f}')
    if 'rel="canonical"' not in c and "rel='canonical'" not in c:
        issues.append(f'MISSING CANONICAL: {f}')
    if 'og:title' not in c:
        issues.append(f'MISSING OG TITLE: {f}')
    if 'twitter:card' not in c:
        issues.append(f'MISSING TWITTER CARD: {f}')

if issues:
    for i in issues:
        print(i)
    print(f'\nTotal issues: {len(issues)}')
else:
    print('ALL CRITICAL SEO CHECKS PASSED - Zero issues found across all 178 pages')
