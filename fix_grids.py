import glob

target = """            .btn-gold { padding: 0.6rem 1rem !important; font-size: 0.7rem !important; }
        }"""

replacement = """            .btn-gold { padding: 0.6rem 1rem !important; font-size: 0.7rem !important; }
            .grid-2, .grid-3 { grid-template-columns: 1fr !important; gap: 2rem !important; }
        }"""

count = 0
for file in glob.glob('*.html'):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    if target in content and '.grid-2, .grid-3 { grid-template-columns: 1fr !important;' not in content:
        content = content.replace(target, replacement)
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        count += 1
        print(f"Fixed grids in {file}")

print(f"Total files updated: {count}")
