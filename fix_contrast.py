import glob

files_changed = 0

# Replace --text-muted values
for filepath in glob.glob("*.html") + ['style.css']:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    old_content = content
    
    # Update CSS variables
    content = content.replace('--text-muted: rgba(255, 255, 255, 0.6);', '--text-muted: rgba(255, 255, 255, 0.75);')
    content = content.replace('--text-muted: rgba(255, 255, 255, 0.65);', '--text-muted: rgba(255, 255, 255, 0.75);')
    
    # Update inline styles
    content = content.replace('color: rgba(255, 255, 255, 0.6)', 'color: rgba(255, 255, 255, 0.75)')
    content = content.replace('color: rgba(255,255,255,0.6)', 'color: rgba(255, 255, 255, 0.75)')
    content = content.replace('color:rgba(255,255,255,0.6)', 'color: rgba(255, 255, 255, 0.75)')
    
    content = content.replace('color: rgba(255, 255, 255, 0.5)', 'color: rgba(255, 255, 255, 0.75)')
    content = content.replace('color: rgba(255,255,255,0.5)', 'color: rgba(255, 255, 255, 0.75)')
    content = content.replace('color:rgba(255,255,255,0.5)', 'color: rgba(255, 255, 255, 0.75)')
    
    if content != old_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        files_changed += 1

print(f"Updated {files_changed} files for contrast.")
