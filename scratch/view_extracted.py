import json
from bs4 import BeautifulSoup
import sys

with open("scratch/extracted_raw_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

def write_clean_body(key, filename):
    if key not in data:
        print(f"Key '{key}' not found.")
        return
    html = data[key]["content"]
    soup = BeautifulSoup(html, "html.parser")
    
    # Remove script and style
    for s in soup(["script", "style"]):
        s.decompose()
        
    out_lines = []
    out_lines.append(f"=======================================================")
    out_lines.append(f"CLEAN TEXT FOR: {key}")
    out_lines.append(f"=======================================================")
    
    # Print h1, h2, h3 and p tags
    for elem in soup.find_all(["h1", "h2", "h3", "h4", "p", "li", "tr"]):
        text = elem.get_text().strip()
        if text and len(text) > 10:
            # Let's write everything to verify
            out_lines.append(f"[{elem.name}]: {text}")
            
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(out_lines))
    print(f"Saved clean text for {key} to {filename}")

write_clean_body("private-yacht-from-ibiza-to-mallorca", "scratch/ibiza_to_mallorca_content.txt")
write_clean_body("mallorca-to-ibiza-private-boat-charter", "scratch/mallorca_to_ibiza_charter_content.txt")
write_clean_body("boat-trip-from-mallorca-to-formentera", "scratch/boat_trip_from_mallorca_to_formentera_content.txt")
write_clean_body("yacht charter mallorca to formentera", "scratch/yacht_charter_mallorca_to_formentera_content.txt")
