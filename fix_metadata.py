import os
import re

def fix_pages():
    html_files = [f for f in os.listdir('.') if f.endswith('.html')]
    print(f"Processing {len(html_files)} files...")
    
    for filename in html_files:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        changed = False
        
        # 1. Add Canonical Tag if missing
        if 'rel="canonical"' not in content:
            slug = filename.replace('.html', '')
            if slug == 'index':
                canonical_url = "https://eliteluxurybookings.com/"
            else:
                canonical_url = f"https://eliteluxurybookings.com/{slug}/"
            
            canonical_tag = f'\n    <link rel="canonical" href="{canonical_url}">'
            # Try to insert after viewport or before </head>
            if '<meta name="viewport"' in content:
                content = content.replace('<meta name="viewport"', f'<meta name="viewport"', 1)
                # Actually let's just put it after the viewport meta
                content = re.sub(r'(<meta name="viewport"[^>]*>)', r'\1' + canonical_tag, content)
                changed = True
            elif '</head>' in content:
                content = content.replace('</head>', canonical_tag + '\n</head>')
                changed = True

        # 2. Fix aria-labels on selects
        if '<select' in content and 'aria-label' not in content:
            content = re.sub(r'<select(?!.*aria-label)([^>]*)>', r'<select\1 aria-label="Selection Option">', content)
            changed = True
            
        if changed:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated {filename}")

if __name__ == "__main__":
    fix_pages()
