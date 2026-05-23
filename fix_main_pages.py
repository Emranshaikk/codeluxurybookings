import os

def fix_page(filepath, grid_classes):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if we already have a 768px media query
    if '@media (max-width: 768px)' in content:
        # Find where it is and inject our classes
        # We'll look for the first @media (max-width: 768px) and add after the opening brace
        insertion = "\n            " + ", ".join(grid_classes) + " { grid-template-columns: 1fr !important; gap: 2rem !important; }"
        if grid_classes[0] + " { grid-template-columns: 1fr" not in content:
             content = content.replace('@media (max-width: 768px) {', '@media (max-width: 768px) {' + insertion)
             print(f"Updated {filepath}")
    elif '@media (max-width: 1024px)' in content:
        # Fallback to 1024px if 768px doesn't exist
        insertion = "\n            " + ", ".join(grid_classes) + " { grid-template-columns: 1fr !important; gap: 2rem !important; }"
        if grid_classes[0] + " { grid-template-columns: 1fr" not in content:
             content = content.replace('@media (max-width: 1024px) {', '@media (max-width: 1024px) {' + insertion)
             print(f"Updated {filepath} (at 1024px)")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

# Fix main pages
fix_page('blog.html', ['.blog-grid'])
fix_page('index.html', ['.form-grid'])
fix_page('luxury-villa-rentals.html', ['.form-grid'])
fix_page('luxury-yacht-rentals.html', ['.form-grid'])
fix_page('elite-private-jet-charter.html', ['.grid-3'])
fix_page('contact.html', ['.grid-2'])
