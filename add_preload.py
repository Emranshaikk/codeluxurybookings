import glob

files_changed = 0
files = glob.glob('*.html')

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    old_content = content
    
    if 'preload" href="/style.css"' not in content and '<link rel="stylesheet" href="/style.css">' in content:
        content = content.replace('<link rel="stylesheet" href="/style.css">', '<link rel="preload" href="/style.css" as="style">\n    <link rel="stylesheet" href="/style.css">')
        
    if content != old_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        files_changed += 1

print(f'Updated {files_changed} files with CSS preload.')
