import os

def check_silos():
    root_dir = r"c:\Users\imran\OneDrive\Desktop\ELB code"
    files = [f for f in os.listdir(root_dir) if f.endswith('.html')]
    
    yacht_count = 0
    aviation_count = 0
    villa_count = 0
    no_silo_count = 0
    overlapping = []
    
    for filename in sorted(files):
        filepath = os.path.join(root_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        has_yacht = '<!-- YACHTING AUTHORITY SILO -->' in content
        has_aviation = '<!-- AVIATION AUTHORITY SILO -->' in content
        has_villa = '<!-- VILLA AUTHORITY SILO -->' in content
        
        silos_found = []
        if has_yacht: silos_found.append("Yacht")
        if has_aviation: silos_found.append("Aviation")
        if has_villa: silos_found.append("Villa")
        
        if len(silos_found) > 1:
            overlapping.append((filename, silos_found))
        elif len(silos_found) == 1:
            if has_yacht: yacht_count += 1
            if has_aviation: aviation_count += 1
            if has_villa: villa_count += 1
        else:
            no_silo_count += 1
            
    print(f"=== Silo Distribution ===")
    print(f"  Yacht Silos: {yacht_count}")
    print(f"  Aviation Silos: {aviation_count}")
    print(f"  Villa Silos: {villa_count}")
    print(f"  No Silos: {no_silo_count}")
    
    if overlapping:
        print(f"\n[ERROR] Overlapping silos found in {len(overlapping)} files:")
        for filename, silos in overlapping:
            print(f"  {filename}: {silos}")
    else:
        print("\n[SUCCESS] No files with overlapping silos!")

if __name__ == '__main__':
    check_silos()
