import os
import re

CORRECT_BLOCK = """/* --- MOBILE OPTIMIZATION LOCK --- */
        @media (max-width: 768px) {
            .hero { padding: 6rem 0 3rem !important; }
            .hero h1 { font-size: 2.2rem !important; line-height: 1.1; padding: 0 1rem; }
            .hero-sub { font-size: 1rem !important; padding: 0 1.5rem; }
            .grid-2, .grid-3 { grid-template-columns: 1fr !important; gap: 2.5rem !important; }
            .section-padding { padding: 4rem 1rem !important; }
            .aviation-search-engine { padding: 1.5rem !important; margin: 1rem !important; }
            .form-grid { grid-template-columns: 1fr !important; gap: 1rem !important; }
            .nav-brand { font-size: 1.3rem !important; }
            .btn-gold { padding: 0.6rem 1rem !important; font-size: 0.7rem !important; }
        }

        """

def repair_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # We target the range between "MOBILE OPTIMIZATION LOCK" and "ELB_STYLE_START_REDESIGN"
    # This range currently contains a mangled media query.
    
    # regex to find everything from the optimization lock comment to the redesign start comment
    # We want to be careful not to eat the start/end markers themselves if we use them in the replacement.
    
    pattern = re.compile(
        r'/\* --- MOBILE OPTIMIZATION LOCK --- \*/.*?/\* ELB_STYLE_START_REDESIGN \*/',
        re.DOTALL
    )
    
    new_content = pattern.sub(CORRECT_BLOCK + "/* ELB_STYLE_START_REDESIGN */", content)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

def main():
    directory = r'c:\Users\imran\OneDrive\Desktop\ELB code'
    files_fixed = 0
    for filename in os.listdir(directory):
        if filename.endswith('.html'):
            if repair_file(os.path.join(directory, filename)):
                files_fixed += 1
    print(f"Total files repaired: {files_fixed}")

if __name__ == "__main__":
    main()
