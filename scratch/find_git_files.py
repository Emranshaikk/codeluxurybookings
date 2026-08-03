import subprocess
import os
import json

# Branches to search
branches = ["main", "fixing-broken-links", "work-from-valens"]

# Paths we want to check or extract
files_to_find = [
    # Cluster A
    ("boat-trip-from-mallorca-to-formentera", [
        "boat-trip-from-mallorca-to-formentera.html",
        "boat-trip-from-mallorca-to-formentera/index.html"
    ]),
    ("yacht-charter-mallorca-to-formentera", [
        "yacht charter mallorca to formentera.html",
        "yacht-charter-mallorca-to-formentera.html",
        "yacht-charter-mallorca-to-formentera/index.html"
    ]),
    ("mallorca-to-formentera-private-boat-cost", [
        "mallorca-to-formentera-private-boat-cost.html",
        "mallorca-to-formentera-private-boat-cost/index.html"
    ]),
    ("yacht-charter-mallorca-formentera", [
        "yacht-charter-mallorca-formentera.html",
        "yacht-charter-mallorca-formentera/index.html"
    ]),
    ("luxury-yacht-rentals/boat-trip-from-mallorca-to-formentera", [
        "luxury-yacht-rentals/boat-trip-from-mallorca-to-formentera/index.html",
        "luxury-yacht-rentals/boat-trip-from-mallorca-to-formentera.html"
    ]),
    # Cluster B
    ("mallorca-to-ibiza-private-boat-charter", [
        "mallorca-to-ibiza-private-boat-charter.html",
        "mallorca-to-ibiza-private-boat-charter/index.html"
    ]),
    ("luxury-yacht-rentals/mallorca-to-ibiza-private-boat", [
        "luxury-yacht-rentals/mallorca-to-ibiza-private-boat/index.html",
        "luxury-yacht-rentals/mallorca-to-ibiza-private-boat.html",
        "luxury-yacht-rentals/mallorca-to-ibiza-private-boat/index.html"
    ]),
    ("private-yacht-from-ibiza-to-mallorca", [
        "private-yacht-from-ibiza-to-mallorca.html",
        "private-yacht-from-ibiza-to-mallorca/index.html"
    ])
]

canonicals = [
    "private-boat-trip-mallorca-to-formentera.html",
    "mallorca-to-ibiza-private-boat.html"
]

print("Searching Git repository for files...")

found_files = {}

for key, paths in files_to_find:
    found = False
    for path in paths:
        for branch in branches:
            cmd = ["git", "show", f"{branch}:{path}"]
            result = subprocess.run(cmd, capture_output=True)
            if result.returncode == 0:
                try:
                    # Decode as UTF-8, ignore errors
                    content = result.stdout.decode('utf-8', errors='ignore')
                    print(f"FOUND: key='{key}' at branch='{branch}', path='{path}'")
                    found_files[key] = (branch, path, content)
                    found = True
                    break
                except Exception as e:
                    print(f"Error decoding {path}: {e}")
        if found:
            break
    if not found:
        print(f"NOT FOUND: key='{key}' in any branch/path combo.")

# Also read current canonical files
for path in canonicals:
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            found_files[path] = ("local", path, f.read())
            print(f"FOUND: canonical local path='{path}'")
    else:
        print(f"WARNING: canonical file '{path}' not found locally!")

# Save the extracted information to a text file for parsing
output_data = {}
for k, (branch, path, content) in found_files.items():
    output_data[k] = {
        "branch": branch,
        "path": path,
        "content_length": len(content),
        "content": content
    }

with open("scratch/extracted_raw_data.json", "w", encoding="utf-8") as out:
    json.dump(output_data, out, ensure_ascii=False, indent=2)

print("Saved raw data to scratch/extracted_raw_data.json")
