import os
import re
import shutil

root_dir = r"c:\Users\imran\OneDrive\Desktop\ELB code"
template_dir = os.path.join(root_dir, "london-to-dubai-private-jet-cost")

def ensure_route(departure, arrival):
    slug = f"{departure.lower()}-to-{arrival.lower()}-private-jet-cost"
    target_dir = os.path.join(root_dir, slug)
    
    if os.path.exists(target_dir):
        return False # Already exists
    
    print(f"Creating missing route: {slug}")
    os.makedirs(target_dir, exist_ok=True)
    
    template_file = os.path.join(template_dir, "index.html")
    target_file = os.path.join(target_dir, "index.html")
    
    with open(template_file, "r", encoding="utf-8") as f:
        html = f.read()
    
    # Simple replacement:
    # We replace "London" -> Departure, "Dubai" -> Arrival
    # Note: case sensitive replace needed.
    # London -> dep_title, london -> dep_lower
    # Dubai -> arr_title, dubai -> arr_lower
    
    # We must be careful! What if 'london' appears somewhere else?
    # Let's just do exact string replacements
    html = html.replace("London", departure.title())
    html = html.replace("london", departure.lower())
    html = html.replace("Dubai", arrival.title())
    html = html.replace("dubai", arrival.lower())
    html = html.replace("LONDON", departure.upper())
    html = html.replace("DUBAI", arrival.upper())
    
    with open(target_file, "w", encoding="utf-8") as f:
        f.write(html)
    return True

created = 0
# Scan index.html for href="/some-to-some-private-jet-cost/"
with open(os.path.join(root_dir, "index.html"), "r", encoding="utf-8") as f:
    home_html = f.read()

route_pattern = re.compile(r'href="/([a-z]+)-to-([a-z]+)-private-jet-cost/"')
matches = route_pattern.findall(home_html)

for dep, arr in matches:
    if ensure_route(dep, arr):
        created += 1

print(f"Auto-generated {created} missing route pages.")
