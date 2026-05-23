import glob, re

count = 0
for file in glob.glob('*.html'):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    if '.grid-3 {' in content and '.grid-2, .grid-3 { grid-template-columns: 1fr' not in content:
        # We need to insert the grid media query right before the closing brace of the @media (max-width: 768px)
        # We know that the last rule inside this media query is .btn-gold { ... }
        
        new_content = re.sub(
            r'(\.btn-gold\s*\{[^}]+\}\s*)\}',
            r'\1    .grid-2, .grid-3 { grid-template-columns: 1fr !important; gap: 2rem !important; }\n        }',
            content
        )
        
        if new_content != content:
            with open(file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            count += 1
            print(f"Fixed grids in {file}")

print(f"Total files updated: {count}")
