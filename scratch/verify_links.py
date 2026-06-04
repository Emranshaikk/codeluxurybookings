import re
import os

REQUIRED_LINKS = [
    "/yacht-charter-available-now",
    "/all-inclusive-yacht-charter",
    "/yacht-charter-with-crew",
    "/last-minute-yacht-charter",
    "/private-yacht-vacation-package",
    "/yacht-charter-for-private-events",
    "/yacht-charter-for-wedding",
    "/yacht-charter-for-corporate-events",
    "/luxury-yacht-charter-caribbean",
    "/luxury-yacht-rental-for-parties"
]

def check_html_links(file_path):
    print(f"Auditing file: {file_path}")
    if not os.path.exists(file_path):
        print("File does not exist!")
        return
        
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    missing = []
    found = []
    for link in REQUIRED_LINKS:
        # Match either exact href="/path" or href="https://eliteluxurybookings.com/path" or similar
        # Since we use relative clean URLs in the cluster: e.g. href="/yacht-charter-available-now"
        pattern = rf'href=["\'](?:https?://eliteluxurybookings\.com)?{re.escape(link)}/?["\']'
        if re.search(pattern, content):
            found.append(link)
        else:
            missing.append(link)
            
    print(f"Total links found: {len(found)}/{len(REQUIRED_LINKS)}")
    for link in found:
        print(f"  [PASS] Found: {link}")
    if missing:
        print("Missing links:")
        for link in missing:
            print(f"  [FAIL] Missing: {link}")
    else:
        print("All required links are present!")

if __name__ == "__main__":
    check_html_links("luxury-yacht-charter-for-family-vacation.html")
