import glob

files_changed = 0

for filepath in glob.glob("*.html"):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    old_content = content
    
    preconnect_str = '<link rel="preconnect" href="https://fonts.googleapis.com">\n    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    
    if preconnect_str not in content:
        # Try to insert before the font loading
        content = content.replace(
            '<link rel="preload"\n        href="https://fonts.googleapis.com', 
            preconnect_str + '\n    <link rel="preload"\n        href="https://fonts.googleapis.com'
        )
        content = content.replace(
            '<link rel="preload" href="https://fonts.googleapis.com', 
            preconnect_str + '\n    <link rel="preload" href="https://fonts.googleapis.com'
        )
        # some files have it on one line, some have line breaks
    
    if content != old_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        files_changed += 1

print(f"Updated {files_changed} files with preconnect.")
