import os

def force_separation():
    html_files = [f for f in os.listdir('.') if f.endswith('.html')]
    count = 0
    for filename in html_files:
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if '/* --- PREMIUM FLEET CARD REDESIGN --- */' in content:
                # 1. Update the CSS for the cards (Safety Margin)
                if 'margin-bottom: 5rem !important;' not in content:
                    content = content.replace('.fleet-card {', '.fleet-card {\n            margin-bottom: 5rem !important;')
                
                # 2. Update the Grid container (Structural Gap)
                # We target the specific pattern used in your route pages
                if 'class="grid-3" style="margin-bottom: 4rem;"' in content:
                    content = content.replace('class="grid-3" style="margin-bottom: 4rem;"', 'class="grid-3" style="margin-bottom: 8rem !important;"')
                
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                count += 1
        except Exception as e:
            print(f"Error in {filename}: {e}")
            
    print(f"Zero-Overlap fix applied to {count} files.")

if __name__ == "__main__":
    force_separation()
