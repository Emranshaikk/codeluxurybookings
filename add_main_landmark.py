import glob
import re

files_changed = 0

for filepath in glob.glob("*.html"):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        
    old_content = content
    
    if "<main>" not in content:
        # Try to insert after navigation
        if "<!-- ELB_NAV_END -->" in content:
            content = content.replace("<!-- ELB_NAV_END -->", "<!-- ELB_NAV_END -->\n\n    <main>")
        else:
            # Fallback if comment is missing
            content = re.sub(r'(</nav>\s*<div class="mobile-menu"[^>]*>.*?</div>)', r'\1\n\n    <main>', content, flags=re.DOTALL)
            
        # Try to insert before footer
        if "<!-- ELB_FOOTER_START -->" in content:
            content = content.replace("<!-- ELB_FOOTER_START -->", "</main>\n\n    <!-- ELB_FOOTER_START -->")
        elif "<footer" in content:
            content = re.sub(r'(<footer)', r'</main>\n\n    \1', content)

    if content != old_content:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        files_changed += 1

print(f"Updated {files_changed} files.")
