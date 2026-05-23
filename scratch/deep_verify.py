import os
import re

html_files = [f for f in os.listdir('.') if f.endswith('.html') and not f.startswith('_') and f != 'old_blog.html']
html_files.sort()

print(f"Total HTML files: {len(html_files)}")
print()

# 1. submitLead JS
missing_js = []
for fname in html_files:
    with open(fname, 'r', encoding='utf-8', errors='ignore') as f:
        c = f.read()
    if 'submitLead(event)' in c and 'async function submitLead' not in c:
        missing_js.append(fname)
print(f"[1] Forms missing submitLead JS: {missing_js if missing_js else 'NONE - OK'}")

# 2. Canonical trailing slash check
bad_canonical = []
for fname in html_files:
    with open(fname, 'r', encoding='utf-8', errors='ignore') as f:
        c = f.read()
    m = re.search(r'rel="canonical" href="([^"]+)"', c)
    if m:
        url = m.group(1)
        slug = fname.replace('.html', '')
        if slug != 'index' and not url.endswith('/'):
            bad_canonical.append(fname + ": " + url)
print(f"[2] Canonicals without trailing slash: {bad_canonical[:3] if bad_canonical else 'NONE - OK'}")

# 3. .htaccess
with open('.htaccess', 'r') as f:
    ht = f.read()
print(f"[3] HTTPS redirect: {'YES' if 'HTTPS' in ht else 'NO'}")
print(f"[3] Trailing slash rule: {'YES' if 'R=301' in ht else 'NO'}")
print(f"[3] 404 error page: {'YES' if 'ErrorDocument 404' in ht else 'NO'}")
print(f"[3] PHP blocked (security): {'YES' if 'Deny from all' in ht else 'NO'}")

# 4. robots.txt
with open('robots.txt') as f:
    robots = f.read()
print(f"[4] Sitemap in robots.txt: {'YES' if 'Sitemap' in robots else 'NO'}")
print(f"[4] Google-Extended allowed: {'YES' if 'Google-Extended' in robots else 'NO'}")
print(f"[4] GPTBot blocked: {'YES' if 'GPTBot' in robots else 'NO'}")

# 5. sitemap.xml
with open('sitemap.xml', 'r', encoding='utf-8') as f:
    sitemap = f.read()
urls = re.findall(r'<loc>(.*?)</loc>', sitemap)
dates = re.findall(r'<lastmod>(\d{4}-\d{2}-\d{2})</lastmod>', sitemap)
stale = [d for d in dates if d < '2026-05-24']
print(f"[5] Sitemap URLs: {len(urls)}")
print(f"[5] Stale dates (pre 2026-05-24): {len(stale)} - {'OK' if not stale else 'NEEDS UPDATE'}")

# 6. Git status
import subprocess
result = subprocess.run(['git', 'status', '--short'], capture_output=True, text=True)
uncommitted = result.stdout.strip()
print(f"[6] Uncommitted changes: {uncommitted if uncommitted else 'NONE - Clean'}")
result2 = subprocess.run(['git', 'log', '--oneline', '-3'], capture_output=True, text=True)
print(f"[6] Latest commits:")
for line in result2.stdout.strip().split('\n'):
    print(f"     {line}")

# 7. key files exist
key_files = ['index.html', 'style.css', '.htaccess', 'sitemap.xml', 'robots.txt', 
             'submit-lead.php', '404.html', 'thank-you.html', 'request-quote.html']
missing_key = [f for f in key_files if not os.path.exists(f)]
print(f"[7] Key files present: {'ALL OK' if not missing_key else 'MISSING: ' + str(missing_key)}")

# 8. WA float CSS in style.css
with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()
print(f"[8] WhatsApp float CSS: {'YES' if 'wa-float' in css else 'NO - MISSING'}")
print(f"[8] Nav ticker styles: {'YES' if 'top-intel-bar' in css else 'NO'}")
print(f"[8] Dynamic body padding: {'YES' if 'body:has(.top-intel-bar)' in css else 'NO'}")

print()
print("=" * 50)
print("DEPLOYMENT STATUS: " + ("READY" if not missing_js and not bad_canonical and not missing_key else "NEEDS FIXES"))
print("=" * 50)
