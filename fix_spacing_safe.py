import os

def fix_spacing():
    # We add margin-bottom to ensure the cards don't overlap the next section
    spacing_css = "margin-bottom: 5rem !important;"
    
    html_files = [f for f in os.listdir('.') if f.endswith('.html')]
    count = 0
    for filename in html_files:
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
                
            if '/* --- PREMIUM FLEET CARD REDESIGN --- */' in content:
                if 'margin-bottom: 5rem !important;' not in content:
                    # Find the opening bracket of .fleet-card
                    new_content = content.replace('.fleet-card {', f'.fleet-card {{\n            {spacing_css}')
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    count += 1
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            
    print(f"Fixed spacing on {count} files.")

if __name__ == "__main__":
    fix_spacing()
