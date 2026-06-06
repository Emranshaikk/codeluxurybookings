import os

workspace_dir = r"c:\Users\imran\OneDrive\Desktop\ELB code"
files = os.listdir(workspace_dir)

print("HTML files containing 'island':")
for f in files:
    if f.endswith('.html') and 'island' in f.lower():
        print(f"  - {f}")

print("\nHTML files containing 'villa':")
for f in files:
    if f.endswith('.html') and 'villa' in f.lower():
        print(f"  - {f}")
