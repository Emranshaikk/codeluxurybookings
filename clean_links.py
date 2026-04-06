import os
import re

def fix_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Regex to find these excessive hyphens that break strings across lines
        # Pattern looks for 10+ hyphens potentially surrounded by whitespace/newlines
        # within href attributes or text content.
        
        original = content
        
        # Fixing common artifacts found in previous results
        # Pattern 1: Hyphens in the middle of a word/URL
        content = re.sub(r'(\w)-\-+(\w)', r'\1\2', content)
        
        # Pattern 2: Hyphens at the start of a line that are part of a broken URL
        content = re.sub(r'href="([^"]+)\n\s*-+([^"]+)"', r'href="\1\2"', content)
        
        # Pattern 3: Simple removal of long hyphen strings that shouldn't be there
        content = re.sub(r'-{10,}', '', content)
        
        if content != original:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
    except Exception as e:
        print(f"Error: {e}")
    return False

if __name__ == "__main__":
    count = 0
    for root, _, files in os.walk('.'):
        for file in files:
            if file.endswith('.html'):
                if fix_file(os.path.join(root, file)):
                    count += 1
    print(f"Cleaned hyphen artifacts in {count} files.")
