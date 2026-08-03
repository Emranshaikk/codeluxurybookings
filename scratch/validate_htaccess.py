import re

HTACCESS_PATH = r"c:\Users\imran\OneDrive\Desktop\ELB code\.htaccess"

print("Validating .htaccess rewrite rules...")

with open(HTACCESS_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

# Regular expression to extract RewriteRules
# Syntax: RewriteRule Pattern Target [Flags]
rule_pattern = re.compile(r'^\s*RewriteRule\s+([^\s]+)\s+([^\s]+)\s+\[([^\]]+)\]', re.M | re.I)

rules = rule_pattern.findall(content)

print(f"Parsed {len(rules)} RewriteRules from .htaccess:")

# Target mappings we expect
expected_mappings = {
    # Cluster A -> private-boat-trip-mallorca-to-formentera/
    "boat-trip-from-mallorca-to-formentera": "https://eliteluxurybookings.com/private-boat-trip-mallorca-to-formentera/",
    "yacht-charter-mallorca-to-formentera": "https://eliteluxurybookings.com/private-boat-trip-mallorca-to-formentera/",
    "mallorca-to-formentera-private-boat-cost": "https://eliteluxurybookings.com/private-boat-trip-mallorca-to-formentera/",
    "yacht-charter-mallorca-formentera": "https://eliteluxurybookings.com/private-boat-trip-mallorca-to-formentera/",
    "luxury-yacht-rentals/boat-trip-from-mallorca-to-formentera": "https://eliteluxurybookings.com/private-boat-trip-mallorca-to-formentera/",
    
    # Cluster B -> mallorca-to-ibiza-private-boat/
    "mallorca-to-ibiza-private-boat-charter": "https://eliteluxurybookings.com/mallorca-to-ibiza-private-boat/",
    "luxury-yacht-rentals/mallorca-to-ibiza-private-boat": "https://eliteluxurybookings.com/mallorca-to-ibiza-private-boat/",
    "private-yacht-from-ibiza-to-mallorca": "https://eliteluxurybookings.com/mallorca-to-ibiza-private-boat/",
    
    # Loops/Fixes
    "luxury-private-jets": "https://eliteluxurybookings.com/elite-private-jet-charter/",
    "blogs": "https://eliteluxurybookings.com/blog/",
    "our-services": "https://eliteluxurybookings.com/",
    "how-private-jet-flight-bookings-work": "https://eliteluxurybookings.com/private-jet-booking-guide/",
    "luxury-yacht-re": "https://eliteluxurybookings.com/luxury-yacht-rentals/"
}

matched_expected = set()

for pattern, target, flags in rules:
    # Clean pattern regex characters
    clean_pat = pattern.replace('^', '').replace('$', '').replace('?', '').replace('(', '').replace(')', '').replace('\\.', '.').replace('/?', '')
    if clean_pat.endswith('(\\.html)'):
        clean_pat = clean_pat[:-8]
    
    # Check if this matches any expected key
    found_key = None
    for key in expected_mappings:
        if clean_pat == key or clean_pat.replace('(\.html)?', '') == key or clean_pat == key + "(\\.html)":
            found_key = key
            break
            
    if found_key:
        expected_target = expected_mappings[found_key]
        if target == expected_target:
            print(f"  [OK] Pattern '{pattern}' -> '{target}' (Flags: {flags})")
            matched_expected.add(found_key)
        else:
            print(f"  [ERROR] Pattern '{pattern}' matches key '{found_key}' but target is '{target}' instead of '{expected_target}'!")
    else:
        # Check other rules
        print(f"  [INFO] Other Rule: '{pattern}' -> '{target}' (Flags: {flags})")

missing = set(expected_mappings.keys()) - matched_expected
if missing:
    print(f"\n[WARNING] Missing expected redirects for keys: {missing}")
else:
    print("\n[SUCCESS] All expected redirects are correctly configured in .htaccess!")
