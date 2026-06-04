required_links = [
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

with open("luxury-yacht-charter-for-family-vacation.html", "r", encoding="utf-8") as f:
    content = f.read()

print("Verifying links in luxury-yacht-charter-for-family-vacation.html:")
all_found = True
for link in required_links:
    present = link in content
    print(f"  {link}: {'FOUND' if present else 'NOT FOUND'}")
    if not present:
        all_found = False

if all_found:
    print("SUCCESS: All 10 cluster links are present!")
else:
    print("WARNING: Some links are missing!")
