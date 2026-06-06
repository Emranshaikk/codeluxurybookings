import os

workspace_dir = r"c:\Users\imran\OneDrive\Desktop\ELB code"
html_files = [f for f in os.listdir(workspace_dir) if f.endswith('.html')]

print("Searching HTML files for card components...")
for filename in html_files:
    filepath = os.path.join(workspace_dir, filename)
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    
    # Check if there is something like "Inquire for Buyout" or "Explore Villa Collection" inside the HTML (static text)
    if "Inquire for Buyout" in content or "Explore Villa" in content or "Inquire For Buyout" in content:
        print(f"Match found in: {filename}")
        # print lines that contain it
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            for idx, line in enumerate(f):
                if any(x in line for x in ["Inquire for Buyout", "Explore Villa", "Inquire For Buyout"]):
                    print(f"  Line {idx+1}: {line.strip()}")
