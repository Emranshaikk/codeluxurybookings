import os
import re
import random

# Path to the website directory
ROOT_DIR = r"c:\Users\imran\OneDrive\Desktop\ELB code"

# Get all route pages (e.g. london-to-newyork-private-jet-cost.html)
route_pages = []
for f in os.listdir(ROOT_DIR):
    if f.endswith("-private-jet-cost.html"):
        route_pages.append(f)

print(f"Found {len(route_pages)} route pages.")

# Parse origins and destinations
# filename format: origin-to-destination-private-jet-cost.html
routes_info = []
for filename in route_pages:
    parts = filename.replace("-private-jet-cost.html", "").split("-to-")
    if len(parts) == 2:
        origin, dest = parts[0], parts[1]
        routes_info.append({
            "filename": filename,
            "origin": origin,
            "dest": dest,
            "url": f"/{filename.replace('.html', '/')}" if filename != "index.html" else "/"
        })

def format_city(city):
    # Capitalize appropriately
    if city == "newyork": return "New York"
    if city == "losangeles": return "Los Angeles"
    if city == "sanfrancisco": return "San Francisco"
    if city == "lasvegas": return "Las Vegas"
    if city == "turksandcaicos": return "Turks and Caicos"
    if city == "goldcoast": return "Gold Coast"
    if city == "hongkong": return "Hong Kong"
    return city.title()

def generate_link_html(route):
    origin_fmt = format_city(route['origin'])
    dest_fmt = format_city(route['dest'])
    text = f"{origin_fmt} to {dest_fmt} Charter"
    
    return f"""                    <a href="{route['url']}"
                        style="color: var(--text-muted); text-decoration: none; border-bottom: 1px solid transparent; transition: all 0.3s;"
                        onmouseover="this.style.color='#D4AF37'; this.style.borderColor='#D4AF37'"
                        onmouseout="this.style.color='rgba(255,255,255,0.6)'; this.style.borderColor='transparent'">{text}</a>"""

internal_linking_pattern = re.compile(
    r'(<!-- INTERNAL LINKING -->.*?<div style="display: flex; gap: 2rem; flex-wrap: wrap; justify-content: center;">)(.*?)(</div>\s*</div>\s*</section>)',
    re.DOTALL
)

duplicate_section_pattern = re.compile(
    r'<section class="section-padding" style="border-top: 1px solid rgba\(255,255,255,0\.05\); background: rgba\(0,0,0,0\.5\);">.*?</section>',
    re.DOTALL
)

modified_count = 0

for route in routes_info:
    filepath = os.path.join(ROOT_DIR, route["filename"])
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Pick 3 routes to link to
    # Try to pick 1 from same origin (different dest), 1 from same dest (different origin), and 1 random
    same_origin = [r for r in routes_info if r['origin'] == route['origin'] and r['filename'] != route['filename']]
    same_dest = [r for r in routes_info if r['dest'] == route['dest'] and r['filename'] != route['filename']]
    
    link1 = random.choice(same_origin) if same_origin else random.choice(routes_info)
    link2 = random.choice(same_dest) if same_dest else random.choice(routes_info)
    
    # Exclude link1 and link2 and current from remaining pool for random choice
    pool = [r for r in routes_info if r['filename'] not in [route['filename'], link1['filename'], link2['filename']]]
    link3 = random.choice(pool) if pool else random.choice(routes_info)

    # Make sure we don't duplicate links in the 3 slots (unlikely but possible if fallback)
    selected_links = []
    for l in [link1, link2, link3]:
        if l not in selected_links:
            selected_links.append(l)
    
    # Fill remaining with randoms if we got deduped
    while len(selected_links) < 3:
        cand = random.choice(routes_info)
        if cand not in selected_links and cand['filename'] != route['filename']:
            selected_links.append(cand)

    links_html = "\n" + "\n".join(generate_link_html(l) for l in selected_links) + "\n                "

    # 2. Replace INTERNAL LINKING block
    new_content = internal_linking_pattern.sub(r'\1' + links_html + r'\3', content)

    # 3. Remove duplicate footer block
    # The structure usually has <!-- ELB_FOOTER_START --> ... </footer>
    if "<!-- ELB_FOOTER_START -->" in new_content:
        parts = new_content.split("<!-- ELB_FOOTER_START -->")
        footer_part = parts[1]
        # Remove the <section ...> inside the footer
        footer_part_cleaned = duplicate_section_pattern.sub("", footer_part)
        new_content = parts[0] + "<!-- ELB_FOOTER_START -->" + footer_part_cleaned

    if new_content != content:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        modified_count += 1

print(f"Successfully updated interlinking and removed duplicates in {modified_count} files.")
