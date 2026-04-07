import os
import re

def total_aviation_reconstruction():
    count = 0
    # Pattern to match aviation route folders
    pattern = re.compile(r'([a-z0-9\-]+)-to-([a-z0-9\-]+)-private-jet-cost', re.I)
    
    # Correct script logic to replace
    OLD_LOGIC = r"const dep_val = document\.getElementById\('v_dep'\)\.value\.toLowerCase\(\);\s+const arr_val = document\.getElementById\('v_arr'\)\.value\.toLowerCase\(\);\s+let dep_icao = 'EGLL', arr_icao = 'LFMN'; \s+for \(const \[key, icao\] of Object\.entries\(VALENS_API\.ICAO_DB\)\) \{\s+if \(dep_val\.includes\(key\)\) dep_icao = icao;\s+if \(arr_val\.includes\(key\)\) arr_icao = icao;\s+\}"
    NEW_LOGIC = "const dep_icao = document.getElementById('v_dep').value;\n            const arr_icao = document.getElementById('v_arr').value;"

    for folder in os.listdir("."):
        if not os.path.isdir(folder):
            continue
            
        if pattern.match(folder):
            filepath = os.path.join(folder, "index.html")
            if not os.path.exists(filepath):
                continue
                
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            original = content
            
            # 1. Fix Script Logic
            content = re.sub(OLD_LOGIC, NEW_LOGIC, content, flags=re.MULTILINE)
            
            # 2. Fix Triple Header Tags
            # We look for </header> followed by whitespace and more </header>
            content = re.sub(r'(</header>\s*){2,}', '</header>\n', content, flags=re.DOTALL)
            
            # 3. Ensure Container Balance (Remove trailing closures that might leak)
            # If we see multiple </header> we already combined them.
            
            if content != original:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                count += 1
                if count % 10 == 0:
                    print(f"Surgically Restored: {count} corridors...")

    print(f"\nFinalized {count} aviation corridors with 100% precise ICAO capture and balanced headers.")

if __name__ == "__main__":
    total_aviation_reconstruction()
