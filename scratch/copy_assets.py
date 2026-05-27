import shutil
import os

src_dir = r"C:\Users\imran\.gemini\antigravity-ide\brain\dc86e305-a73d-409b-af8f-c6c5ab6432c3"
dest_dir = r"c:\Users\imran\OneDrive\Desktop\ELB code\assets"

files_to_copy = {
    "luxury_charter_hero_1779875155866.png": "luxury_charter_hero.png",
    "luxury_cabin_interior_1779875178255.png": "luxury_cabin_interior.png",
    "vip_boarding_tarmac_1779875200265.png": "vip_boarding_tarmac.png"
}

for src_name, dest_name in files_to_copy.items():
    src_path = os.path.join(src_dir, src_name)
    dest_path = os.path.join(dest_dir, dest_name)
    if os.path.exists(src_path):
        shutil.copy2(src_path, dest_path)
        print(f"Copied {src_name} to {dest_name} successfully.")
    else:
        print(f"Source file {src_path} does not exist!")
