import subprocess
import json

targets = [
    "yacht-charter-mallorca-to-formentera",
    "yacht charter mallorca to formentera",
    "mallorca-to-formentera-private-boat-cost",
    "luxury-yacht-rentals/mallorca-to-ibiza-private-boat"
]

print("Scanning all commits in Git history to find targets...")

# We will run git log with a custom format to get commit hashes and files changed
cmd = ["git", "log", "--all", "--name-only", "--format=COMMIT:%H"]
result = subprocess.run(cmd, capture_output=True)
output = result.stdout.decode('utf-8', errors='ignore')

current_commit = None
matches = []

for line in output.splitlines():
    line = line.strip()
    if not line:
        continue
    if line.startswith("COMMIT:"):
        current_commit = line.split(":")[1]
    else:
        # Check if this file path matches any of our targets
        for t in targets:
            if t in line:
                matches.append((current_commit, line))
                print(f"Match found: commit={current_commit}, file='{line}'")

# Now let's try to extract content for these files from the matches
extracted = {}
for commit, path in matches:
    # If we already extracted this file, we can keep the latest one (commits are listed reverse-chronological, so first match is latest)
    # But wait, we want the content before deletion. git show commit:path will work if the file was present in that commit.
    key = path
    if key in extracted:
        continue
        
    cmd_show = ["git", "show", f"{commit}:{path}"]
    res_show = subprocess.run(cmd_show, capture_output=True)
    if res_show.returncode == 0:
        content = res_show.stdout.decode('utf-8', errors='ignore')
        extracted[key] = {
            "commit": commit,
            "path": path,
            "content": content
        }
        print(f"Successfully extracted: '{path}' from commit {commit}")
    else:
        # If it failed, maybe the file was deleted in this commit. Try the parent commit.
        cmd_show_parent = ["git", "show", f"{commit}~1:{path}"]
        res_show_parent = subprocess.run(cmd_show_parent, capture_output=True)
        if res_show_parent.returncode == 0:
            content = res_show_parent.stdout.decode('utf-8', errors='ignore')
            extracted[key] = {
                "commit": f"{commit}~1",
                "path": path,
                "content": content
            }
            print(f"Successfully extracted (parent): '{path}' from commit {commit}~1")

# Load existing data
import os
raw_data_file = "scratch/extracted_raw_data.json"
existing_data = {}
if os.path.exists(raw_data_file):
    with open(raw_data_file, 'r', encoding='utf-8') as f:
        existing_data = json.load(f)

# Merge
for k, data in extracted.items():
    # Use the basename or a clean key
    clean_key = k
    if "/" in clean_key:
        clean_key = clean_key.split("/")[-1]
    if clean_key.endswith(".html"):
        clean_key = clean_key[:-5]
        
    existing_data[clean_key] = {
        "branch": f"commit:{data['commit']}",
        "path": data["path"],
        "content_length": len(data["content"]),
        "content": data["content"]
    }

# Save back
with open(raw_data_file, 'w', encoding='utf-8') as f:
    json.dump(existing_data, f, ensure_ascii=False, indent=2)

print("Updated raw data in scratch/extracted_raw_data.json")
