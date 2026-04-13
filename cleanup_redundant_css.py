import os
import re

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern for the redundant CSS block often found between the mobile media query and redesign marker.
    # We look for the first @media (max-width: 768px) block and the ELB_STYLE_START_REDESIGN marker.
    
    # In many files, the redundancy starts after the first media query closes.
    # We want to identify the block between line ~380 and ~430 that duplicates mobile styles.
    
    # Pattern 1: The mangled Sydney case (extra properties or duplication)
    # We will specifically target the mangled lines in Sydney as a priority.
    content = content.replace(
        "            .form-grid { grid-template-columns: 1fr !important; gap: 1rem !important; }\n            font-weight: 600;\n            color: #fff !important;\n            text-decoration: none !important;\n        }",
        "            .form-grid { grid-template-columns: 1fr !important; gap: 1rem !important; }\n            .nav-brand { font-size: 1.3rem !important; }\n            .btn-gold { padding: 0.6rem 1rem !important; font-size: 0.7rem !important; }\n        }"
    )
    
    # Also handle variants with slightly different spacing
    content = content.replace(
        "            .form-grid { grid-template-columns: 1fr !important; gap: 1rem !important; }\r\n            font-weight: 600;\r\n            color: #fff !important;\r\n            text-decoration: none !important;\r\n        }",
        "            .form-grid { grid-template-columns: 1fr !important; gap: 1rem !important; }\r\n            .nav-brand { font-size: 1.3rem !important; }\r\n            .btn-gold { padding: 0.6rem 1rem !important; font-size: 0.7rem !important; }\r\n        }"
    )

    # Global redundancy cleanup:
    # Identify the block starting with ".hero h1 {" and ending shortly before "/* ELB_STYLE_START_REDESIGN */"
    # only if it's NOT inside a media query.
    
    # This is trickier to do with regex safely. 
    # Let's target the exact block found in the audited files.
    
    redundant_block_pattern = r'\}\s+\.hero h1 \{\s+font-size: 2\.2rem !important;\s+line-height: 1\.1;\s+padding: 0 1rem;\s+\}\s+\.hero-sub \{\s+font-size: 1rem !important;\s+padding: 0 1\.5rem;\s+\}\s+\.grid-2,\s+\.grid-3 \{\s+grid-template-columns: 1fr !important;\s+gap: 2\.5rem !important;\s+\}\s+\.section-padding \{\s+padding: 4rem 1rem !important;\s+\}\s+\.search-grid,\s+\.contact-grid \{\s+grid-template-columns: 1fr !important;\s+\}\s+\.aviation-search-engine \{\s+padding: 1\.5rem !important;\s+margin: 1rem !important;\s+\}\s+/\* ELB_STYLE_START_REDESIGN \*/'
    
    # Note: Use a more flexible regex that survives minor whitespace differences
    redundant_block_regex = re.compile(
        r'\}\s+\.hero h1 \{\s+font-size: 2\.2rem !important;.*?' 
        r'\.aviation-search-engine \{\s+padding: 1\.5rem !important;\s+margin: 1rem !important;\s+\}\s+', 
        re.DOTALL
    )
    
    new_content = redundant_block_regex.sub('}\n\n        ', content)
    
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
            if fix_file(os.path.join(directory, filename)):
                print(f"Fixed: {filename}")
                files_fixed += 1
    print(f"Total files fixed: {files_fixed}")

if __name__ == "__main__":
    main()
