import os
import re
import sys

# Ensure stdout uses UTF-8
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

workspace_dir = r"c:\Users\imran\OneDrive\Desktop\ELB code"
files = [
    "index.html",
    "elite-private-jet-charter.html",
    "luxury-yacht-rentals.html",
    "luxury-villa-rentals.html"
]

schema_content = """
    <!-- TravelAgency E-E-A-T Schema -->
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "TravelAgency",
      "name": "Elite Luxury Bookings",
      "url": "https://eliteluxurybookings.com/",
      "logo": "https://eliteluxurybookings.com/favicon.png",
      "image": "https://eliteluxurybookings.com/assets/elite_jet_master_hero.png",
      "telephone": "+918801079030",
      "address": {
        "@type": "PostalAddress",
        "streetAddress": "[PLACEHOLDER: Add Hyderabad Office Address Here]",
        "addressLocality": "Hyderabad",
        "addressRegion": "Telangana",
        "postalCode": "[PLACEHOLDER: Add Postal Code Here]",
        "addressCountry": "IN"
      },
      "sameAs": [
        "https://www.facebook.com/eliteluxurybookings",
        "https://www.instagram.com/eliteluxurybookings",
        "https://www.linkedin.com/company/elite-luxury-bookings/",
        "https://x.com/eliteluxuryb"
      ]
    }
    </script>
"""

print("Injecting TravelAgency E-E-A-T JSON-LD Schema...")
print("=" * 80)

for fn in files:
    path = os.path.join(workspace_dir, fn)
    if not os.path.exists(path):
        print(f"File not found: {fn}")
        continue
        
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()
        
    if "TravelAgency" in html:
        print(f"Schema already present in {fn}")
        continue
        
    if "</head>" in html:
        # Inject right before </head>
        new_html = html.replace("</head>", schema_content.strip() + "\n</head>")
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_html)
        print(f"Successfully injected schema into {fn}")
    else:
        print(f"Could not find </head> in {fn}")

print("Schema injection complete.")
