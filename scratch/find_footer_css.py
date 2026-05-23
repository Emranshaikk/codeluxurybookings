import os
import re

def find_footer_css(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        
    pattern = re.compile(r'\.footer-brand\s+p\s*\{([^}]+)\}', re.DOTALL)
    matches = pattern.findall(content)
    return matches

def main():
    files = ['index.html', 'elite-private-jet-charter.html', 'about.html', 'private-jet-booking-guide.html']
    for file in files:
        if os.path.exists(file):
            matches = find_footer_css(file)
            print(f"--- {file} ---")
            for m in matches:
                print(m.strip())
                print()

if __name__ == '__main__':
    main()
