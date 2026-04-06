import os
import re

root_dir = r"c:\Users\imran\OneDrive\Desktop\ELB code"

# 1 & 3 & 4: Append premium styles to style.css for padding, hero-sub, and forms
css_path = os.path.join(root_dir, "assets", "css", "style.css")
if os.path.exists(css_path):
    with open(css_path, "a", encoding="utf-8") as f:
        f.write("\n/* --- USER REQUESTED PREMIUM UPGRADES --- */\n")
        # 1: Padding below header
        f.write("body { padding-top: 110px !important; }\n")
        # 3 & 4: Premium card and hero-sub formatting
        f.write(".hero-sub {\n    font-size: 1.3rem;\n    max-width: 800px;\n    margin: 0 auto 2.5rem auto;\n    color: rgba(255, 255, 255, 0.8);\n    line-height: 1.8;\n    text-align: center;\n}\n")
        f.write(".form-wrapper.glass-panel {\n    background: rgba(20, 20, 20, 0.8);\n    border: 1px solid rgba(212, 175, 55, 0.3);\n    box-shadow: 0 30px 60px rgba(0, 0, 0, 0.9);\n    backdrop-filter: blur(30px);\n    padding: 3rem;\n    border-radius: 20px;\n}\n")
        # Improve the overall layout text for 4
        f.write(".hero h1 {\n    margin-bottom: 1.5rem !important;\n}\n")

print("Updated style.css with premium formatting and padding.")

# 2: Fix the "/ Date Freshness" syntax error globally
syntax_fixed = 0
for subdir, dirs, files in os.walk(root_dir):
    if "-private-jet" in subdir:
        for file in files:
            if file == "index.html":
                filepath = os.path.join(subdir, file)
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # Replace the exact syntax error
                if "/ Date Freshness" in content and "// Date Freshness" not in content:
                    content = content.replace("/ Date Freshness", "// Date Freshness")
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(content)
                    syntax_fixed += 1

print(f"Fixed JS date syntax error on {syntax_fixed} pages.")

# 5: Fix duplicated blocks on luxury-villa-rentals/index.html
villa_idx = os.path.join(root_dir, "luxury-villa-rentals", "index.html")
if os.path.exists(villa_idx):
    with open(villa_idx, "r", encoding="utf-8") as f:
        html = f.read()
    
    # We will simply parse the file to find the duplicate block
    # "Elite Luxury Bookings operates 1,200+ global city-pairs."
    dup_text = "Elite Luxury Bookings operates 1,200+ global city-pairs."
    
    # Since the user literally duplicated:
    # <!-- Column 2: The Americas Hub -->
    # ... down to </section>
    
    # The safest way is to find the exact duplicate chunks and remove them.
    # To be extremely precise, we can use a regex to strip any duplicate text block 
    # if it appears more than once at the bottom.
    
    # Let's count how many times dup_text appears
    parts = html.split(dup_text)
    if len(parts) > 2:
        print(f"Found {len(parts)-1} instances of the duplicated text. Trimming...")
        # Since it's at the end of the file, just cut off the string at the second occurrence of a large repeated block.
        # Let's do a smart regex or just manual replace
        pattern = r"(\s+</div>\s+<!-- Column 2: The Americas Hub -->.*?bespoke pricing on request\.</p>\s+</div>\s+</div>\s+</section>)"
        # We find all matches of the repeated block
        matches = list(re.finditer(pattern, html, flags=re.DOTALL))
        if len(matches) > 1:
            # Reconstruct string without all but the first match
            # Actually, the user duplicated it 2 or 3 times. We'll simply remove ALL instances EXCEPT the first.
            first_match_end = matches[0].end()
            clean_html = html[:first_match_end] + html[matches[-1].end():]
            
            # Ensure we didn't remove the footer entirely
            if "<!-- ELB_FOOTER_START -->" not in clean_html:
                # If footer got cut off, re-attach it from the original
                footer_start = html.find("<!-- ELB_FOOTER_START -->")
                if footer_start != -1:
                    clean_html = html[:first_match_end] + "\n\n" + html[footer_start:]
            
            with open(villa_idx, "w", encoding="utf-8") as f:
                f.write(clean_html)
            print("Cleaned up duplicated blocks in luxury villa rentals.")
