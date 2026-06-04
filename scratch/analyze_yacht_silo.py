import re
pages = [
    'last-minute-yacht-charter.html', 
    'all-inclusive-yacht-charter.html', 
    'yacht-charter-available-now.html', 
    'yacht-charter-with-crew.html'
]
for p in pages:
    try:
        with open(p, 'r', encoding='utf-8') as f:
            c = f.read()
        print(f"=== {p} ===")
        print("Has Yachting Authority Silo block:", "Yachting Authority Silo" in c or "YACHTING" in c)
        links = re.findall(r'href=["\']([^"\']+)["\']', c)
        yacht_links = [l for l in links if 'yacht' in l.lower() or 'boat' in l.lower() or 'superyacht' in l.lower()]
        print("Yacht-related links found:")
        for yl in sorted(set(yacht_links)):
            print(f"  - {yl}")
    except Exception as e:
        print(f"Error reading {p}: {e}")
