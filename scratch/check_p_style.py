import os
import re

def check_p_style(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        
    # Search for styles styling p tag like "p {" or "p,"
    pattern = re.compile(r'(p\s*\{[^}]+\})', re.DOTALL | re.IGNORECASE)
    matches = pattern.findall(content)
    return matches

def main():
    files = ['index.html', 'elite-private-jet-charter.html', 'about.html', 'private-jet-booking-guide.html']
    for file in files:
        if os.path.exists(file):
            matches = check_p_style(file)
            print(f"--- {file} ---")
            for m in matches:
                # filter out .footer-brand p or other specific p selectors
                if '.footer' not in m and '.form' not in m and '.blog' not in m:
                    print(m.strip())
                    print()

if __name__ == '__main__':
    main()
