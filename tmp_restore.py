import subprocess
import os

ROOT_DIR = r'c:\Users\imran\OneDrive\Desktop\ELB code'

target_dirs = [
    'private-jet-rental-prices/index.html',
    'luxury-yacht-rentals/renting-catamaran/index.html',
    'types-of-private-jets/index.html',
    'empty-leg-flights-discount/index.html',
    'private-jet-for-business-travel/index.html',
    'luxury-yacht-rentals/best-sailing-yacht-charter/index.html',
    'luxury-yacht-rentals/bareboat-charter-guide/index.html',
    'luxury-yacht-rentals/guide-to-mediterranean-yacht-charter/index.html',
    'luxury-villas/index.html',
    'contact/index.html'
]

# 1. explicitly checkout the ten ones the user mentioned
for p in target_dirs:
    idx = os.path.join(ROOT_DIR, p.replace('/', '\\'))
    print(f'Restoring {p} from 03c0c5e...')
    try:
        subprocess.check_call(['git', 'checkout', '03c0c5e', '--', p], cwd=ROOT_DIR)
    except Exception as e:
        print(f'Failed to restore {p}: {e}')

# 2. Iterate through all files. If they contain my dummy string, try to restore from 03c0c5e to get their WP content back
restored_count = 0
for root, d, files in os.walk(ROOT_DIR):
    for f in files:
        if f == 'index.html':
            p = os.path.join(root, f)
            rel_path = os.path.relpath(p, ROOT_DIR).replace('\\', '/')
            if rel_path in target_dirs:
                continue # already did
                
            try:
                with open(p, 'r', encoding='utf-8') as file:
                    c = file.read()
                    
                if 'Elite Aviation Insights' in c or 'Elite Authority Insights' in c:
                    print(f'Attempting to restore {rel_path}...')
                    try:
                        subprocess.check_call(['git', 'checkout', '03c0c5e', '--', rel_path], cwd=ROOT_DIR)
                        restored_count += 1
                    except Exception as checkout_e:
                        print(f'Could not checkout {rel_path} (maybe did not exist in 03c0c5e?): {checkout_e}')
            except Exception as e:
                pass

print(f'Restore complete. Checked out targeting 10 files + {restored_count} auto-detected files.')
