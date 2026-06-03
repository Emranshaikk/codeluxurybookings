import re
import os

def convert_markdown_bold():
    filepath = r"c:\Users\imran\OneDrive\Desktop\ELB code\yacht-charter-available-now.html"
    if not os.path.exists(filepath):
        print("File not found")
        return
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Find all instances of **something**
    matches = re.findall(r'\*\*([^*]+)\*\*', content)
    if not matches:
        print("No markdown bold patterns found.")
        return
        
    print(f"Found {len(matches)} markdown bold pattern(s):")
    for m in matches:
        print(f"  - **{m}**")
        
    # Replace **something** with <strong>something</strong>
    new_content = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
        
    print("Successfully replaced all markdown bold patterns with HTML <strong> tags.")

if __name__ == "__main__":
    convert_markdown_bold()
