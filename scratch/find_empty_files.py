import os

def find_small_files():
    html_files = []
    for root, dirs, files in os.walk('.'):
        if '.git' in root or '_archive' in root or 'scratch' in root:
            continue
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
                
    small_files = []
    for filepath in html_files:
        size = os.path.getsize(filepath)
        # If size is less than 5KB, it might be a blank placeholder or missing content
        if size < 5000:
            small_files.append((filepath, size))
            
    print(f"Total HTML files audited: {len(html_files)}")
    print(f"HTML files smaller than 5KB: {len(small_files)}")
    for filepath, size in small_files:
        print(f" - {filepath} ({size} bytes)")

if __name__ == '__main__':
    find_small_files()
