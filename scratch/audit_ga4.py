import os
import sys
import re

# Ensure stdout uses UTF-8
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

workspace_dir = r"c:\Users\imran\OneDrive\Desktop\ELB code"
html_files = [f for f in os.listdir(workspace_dir) if f.endswith('.html')]

print(f"Auditing GA4 setup across {len(html_files)} HTML files...")
print("=" * 80)

measurement_ids = {}
missing_ga = []
existing_events = []

# Regex patterns
ga_pattern = re.compile(r'googletagmanager\.com/gtag/js\?id=(G-[A-Z0-9]+)', re.I)
gtag_config_pattern = re.compile(r"gtag\('config',\s*'([^']+)'", re.I)
event_pattern = re.compile(r"gtag\('event',\s*[^)]+\)", re.I)

for fn in sorted(html_files):
    path = os.path.join(workspace_dir, fn)
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # 1. Search for measurement ID in script src
    ga_match = ga_pattern.search(content)
    # 2. Search for config call
    config_match = gtag_config_pattern.search(content)
    
    m_id = None
    if ga_match:
        m_id = ga_match.group(1)
    elif config_match:
        m_id = config_match.group(1)
        
    if m_id:
        measurement_ids[m_id] = measurement_ids.get(m_id, 0) + 1
    else:
        # Exclude temporary or verification pages
        if fn not in ['verifyforzoho.html', 'zoho-domain-verification.html', 'zohoverify.html']:
            missing_ga.append(fn)
            
    # 3. Search for existing gtag events
    events = event_pattern.findall(content)
    for ev in events:
        existing_events.append((fn, ev))

print("GA4 Measurement ID Frequencies:")
for m_id, count in measurement_ids.items():
    print(f"  - {m_id}: present in {count} files")
    
print(f"\nMissing GA4 Tracking code in {len(missing_ga)} pages:")
for fn in missing_ga[:15]:
    print(f"  - {fn}")
if len(missing_ga) > 15:
    print(f"  ... and {len(missing_ga) - 15} more files")

print(f"\nFound {len(existing_events)} existing custom events:")
for fn, ev in existing_events[:20]:
    print(f"  - {fn}: {ev}")
if len(existing_events) > 20:
    print(f"  ... and {len(existing_events) - 20} more events")
