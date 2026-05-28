with open(r'c:\Users\imran\OneDrive\Desktop\ELB code\7-best-private-jet-charter-in-dubai.html', 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'style.css' in line:
        print(f"Line {i+1}: {line.strip()}")
