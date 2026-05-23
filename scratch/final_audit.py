import os
import re
from datetime import date

GA_ID = "G-J56D1LJLFM"
CLARITY_ID = "sia395rirl"
BASE_URL = "https://eliteluxurybookings.com"
TODAY = date.today().isoformat()

SKIP = {'old_blog.html', '_template_blog_master.html', '_template_master.html'}

html_files = [f for f in os.listdir('.') if f.endswith('.html') and f not in SKIP and not f.startswith('_')]
html_files.sort()

issues = {}

for fname in html_files:
    with open(fname, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    file_issues = []
    if GA_ID not in content:
        file_issues.append("MISSING_GA")
    if CLARITY_ID not in content:
        file_issues.append("MISSING_CLARITY")
    if 'canonical' not in content:
        file_issues.append("MISSING_CANONICAL")
    if 'og:image' not in content:
        file_issues.append("MISSING_OG_IMAGE")
    if 'twitter:card' not in content:
        file_issues.append("MISSING_TWITTER")
    if 'wa-float' not in content and fname not in ('404.html', 'thank-you.html'):
        file_issues.append("MISSING_WA")
    if 'application/ld+json' not in content:
        file_issues.append("MISSING_SCHEMA")
    if 'global-nav' not in content:
        file_issues.append("MISSING_NAV")
    if '<footer' not in content:
        file_issues.append("MISSING_FOOTER")

    if file_issues:
        issues[fname] = file_issues

print(f"=== FINAL AUDIT - {TODAY} ===")
print(f"Total files checked: {len(html_files)}")
print(f"Files with issues: {len(issues)}")
print()

for fname, file_issues in sorted(issues.items()):
    print(f"  {fname}: {', '.join(file_issues)}")

print()
print("Summary by issue type:")
all_types = {}
for fname, fissues in issues.items():
    for issue in fissues:
        all_types.setdefault(issue, []).append(fname)
for itype, files in sorted(all_types.items()):
    print(f"  {itype}: {len(files)} files")
