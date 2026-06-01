import os
import shutil

src_dir = r"C:\Users\imran\.gemini\antigravity-ide\brain\e1b5c823-7663-4982-896c-c0c9fd9e4c0f"
dest_dir = r"c:\Users\imran\OneDrive\Desktop\ELB code\assets"

mapping = {
    "media__1780337763788.jpg": "luxury_island_bedroom.jpg",
    "media__1780337764742.jpg": "luxury_island_salon.jpg",
    "media__1780337765054.jpg": "luxury_island_dusk_pathway.jpg"
}

for src_name, dest_name in mapping.items():
    src_path = os.path.join(src_dir, src_name)
    dest_path = os.path.join(dest_dir, dest_name)
    if os.path.exists(src_path):
        shutil.copy2(src_path, dest_path)
        print(f"Copied {src_name} to {dest_path}")
    else:
        print(f"Error: {src_name} does not exist at {src_path}")
