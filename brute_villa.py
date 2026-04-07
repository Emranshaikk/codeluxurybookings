import os
import re

def brute_force_villa_discovery():
    file_path = "blog/index.html"
    if not os.path.exists(file_path):
        print("Missing blog index.")
        return

    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            
        print(f"Total Lines: {len(lines)}")
        
        # We look for ANY card that mentions villa or data-category="villas"
        count = 0
        villas = []
        for i, line in enumerate(lines):
            if 'villas' in line.lower() or 'villa' in line.lower() or 'estate' in line.lower():
                # Extract the href from this or near lines
                match = re.search(r'href="(/[^"]*/?)"', line)
                if match:
                    link = match.group(1)
                    if link not in villas:
                        villas.append(link)
                elif i + 1 < len(lines):
                    match = re.search(r'href="(/[^"]*/?)"', lines[i+1])
                    if match:
                        link = match.group(1)
                        if link not in villas:
                            villas.append(link)

        print(f"Discovered {len(villas)} potential routes.")
        for v in villas[:50]: # Show first 50
            # Check if directory exists for this link
            clean_rel = v.strip("/")
            full_path = os.path.join(os.getcwd(), clean_rel)
            exists = os.path.exists(full_path)
            print(f"Route: {v} | Local Path Exists: {exists}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    brute_force_villa_discovery()
