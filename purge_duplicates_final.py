import os
import re

# Robust patterns to target for deduplication
PATTERNS = [
    (re.compile(r'<!-- ELB_NAV_START -->.*?<!-- ELB_NAV_END -->', re.DOTALL), "Navigation Block"),
    (re.compile(r'<!-- ELB_JS_START -->.*?<!-- ELB_JS_END -->', re.DOTALL), "JS Block"),
    # Target the entire placeholder div as a unit
    (re.compile(r'<div id="footer-silo-placeholder">.*?</div>\s*</div>', re.DOTALL), "Silo Placeholder Block"),
    # Fallback for hub grid if placeholder is missing but grid exists separately
    (re.compile(r'<section class="section-padding"[^>]*>\s*<div class="container">\s*<h2[^>]*>Global <span class="gold-text">Aviation Network</span></h2>.*?<p[^>]*>Elite Luxury Bookings operates 1,200\+ global city-pairs\..*?</p>\s*</div>\s*</section>', re.DOTALL), "Aviation Grid Fallback"),
    (re.compile(r'/\* ELB_CSS_START \*/.*?/\* ELB_CSS_END \*/', re.DOTALL), "CSS Block"),
    (re.compile(r'/\* ELB_BLOG_SIDEBAR_START \*/.*?/\* ELB_BLOG_SIDEBAR_END \*/', re.DOTALL), "Sidebar CSS Block")
]

def sanitize_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content
        modified = False

        for pattern, label in PATTERNS:
            matches = list(pattern.finditer(content))
            if len(matches) > 1:
                # Keep only the FIRST match
                first_match = matches[0]
                
                new_content = content[:first_match.end()]
                rest_of_content = content[first_match.end():]
                
                # Remove all subsequent matches in the rest of the content
                rest_of_content = pattern.sub('', rest_of_content)
                
                content = new_content + rest_of_content
                modified = True

        if modified:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def main():
    root_dir = r"c:\Users\imran\OneDrive\Desktop\ELB code"
    processed_count = 0
    modified_count = 0

    for root, dirs, files in os.walk(root_dir):
        if any(ignored in root for ignored in ['assets', '.gemini', 'tmp', '.git']):
            continue
            
        for file in files:
            if file.endswith('.html'):
                processed_count += 1
                if sanitize_file(os.path.join(root, file)):
                    modified_count += 1

    print(f"\nFinal Audit Complete.")
    print(f"Files Processed: {processed_count}")
    print(f"Files Deduplicated: {modified_count}")

if __name__ == "__main__":
    main()
