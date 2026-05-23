import os

directory = r"c:\Users\imran\OneDrive\Desktop\ELB code"

for filename in os.listdir(directory):
    if filename.endswith(".html"):
        path = os.path.join(directory, filename)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove literal \n strings
        content = content.replace("\\n", "\n")
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Cleaned literals from {filename}")
