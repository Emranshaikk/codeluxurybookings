
import os
import re

def deep_nuclear_cleanup():
    silo_file = 'global-route-silo/index.html'
    if not os.path.exists(silo_file): 
        print("Silo file missing!")
        return
    with open(silo_file, 'r', encoding='utf-8') as f:
        pure_silo = f.read().strip()

    # The ultimate "Junk Zone" pattern:
    # Matches from <!-- SILO TARGET --> all the way to <footer...
    # This captures the old columns AND the placeholder.
    junk_pattern = re.compile(r'(?s)<!-- SILO TARGET -->.*?<footer', re.IGNORECASE)

    for root, dirs, files in os.walk('.'):
        if any(x in root for x in ['.git', 'assets', 'global-route-silo', 'node_modules']): continue
        
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    
                    if '<!-- SILO TARGET -->' in content and '<footer' in content.lower():
                        # Replace the entire junk zone with EXACTLY ONE SILO + the footer tag we matched
                        new_content = re.sub(junk_pattern, f'<!-- SILO TARGET -->\n<div id="footer-silo-placeholder">\n{pure_silo}\n</div>\n<footer', content)
                        
                        if new_content != content:
                            with open(filepath, 'w', encoding='utf-8') as f:
                                f.write(new_content)
                except Exception as e:
                    print(f"Error on {filepath}: {e}")

if __name__ == "__main__":
    deep_nuclear_cleanup()
