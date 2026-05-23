import os
import re

FOOTER_CSS = """        /* ===== MASTER FOOTER (INJECTED SITE-WIDE) ===== */
        .footer { background: #000 !important; padding: 5rem 0 3rem !important; border-top: 1px solid rgba(212, 175, 55, 0.1) !important; margin-top: 5rem !important; text-align: left !important; }
        .footer-grid { display: grid !important; grid-template-columns: 2fr 1fr 1fr !important; gap: 4rem !important; padding-bottom: 4rem !important; border-bottom: 1px solid rgba(212, 175, 55, 0.1) !important; text-align: left !important; }
        .footer-brand { text-align: left !important; }
        .footer-brand h2 { font-family: 'Cormorant Garamond', serif !important; font-size: 2.2rem !important; margin-bottom: 1.5rem !important; color: #fff !important; text-align: left !important; }
        .footer-brand p { font-family: 'Inter', sans-serif !important; font-size: 0.9rem !important; line-height: 1.8 !important; max-width: 380px !important; margin-bottom: 2rem !important; color: rgba(255, 255, 255, 0.7) !important; text-align: left !important; }
        .footer-socials { display: flex !important; gap: 1.5rem !important; justify-content: flex-start !important; }
        .footer-socials a { color: rgba(255, 255, 255, 0.6) !important; transition: 0.3s !important; font-size: 1.5rem !important; }
        .footer-socials a:hover { color: #D4AF37 !important; }
        .footer-col { text-align: left !important; }
        .footer-col h4 { color: #D4AF37 !important; text-transform: uppercase !important; letter-spacing: 2px !important; font-size: 0.9rem !important; margin-bottom: 2rem !important; text-align: left !important; }
        .footer-col ul { list-style: none !important; padding: 0 !important; margin: 0 !important; text-align: left !important; }
        .footer-col ul li { margin-bottom: 1rem !important; text-align: left !important; }
        .footer-col ul li a { color: rgba(255, 255, 255, 0.8) !important; text-decoration: none !important; transition: 0.3s !important; font-size: 0.95rem !important; }
        .footer-col ul li a:hover { color: #D4AF37 !important; padding-left: 5px !important; }
        .footer-bottom { display: flex !important; justify-content: space-between !important; align-items: center !important; padding-top: 3rem !important; color: rgba(255, 255, 255, 0.4) !important; font-size: 0.85rem !important; }
        .footer-legal { display: flex !important; gap: 2rem !important; }
        .footer-legal a { color: inherit !important; text-decoration: none !important; }
        @media (max-width: 992px) { 
            .footer-grid { grid-template-columns: 1fr 1fr !important; } 
            .footer-brand { grid-column: span 2 !important; } 
        }
        @media (max-width: 600px) { 
            .footer-grid { grid-template-columns: 1fr !important; } 
            .footer-brand { grid-column: span 1 !important; text-align: center !important; } 
            .footer-brand h2 { text-align: center !important; }
            .footer-brand p { text-align: center !important; margin: 0 auto 2rem auto !important; }
            .footer-socials { justify-content: center !important; }
            .footer-col { text-align: center !important; }
            .footer-col h4 { text-align: center !important; }
            .footer-col ul { text-align: center !important; }
            .footer-col ul li { text-align: center !important; }
            .footer-bottom { flex-direction: column !important; gap: 2rem !important; text-align: center !important; } 
        }"""

def clean_file(path):
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    style_pattern = re.compile(r'(<style.*?>)(.*?)(</style>)', re.DOTALL)
    match = style_pattern.search(content)
    if not match:
        return False

    start_tag, style_content, end_tag = match.groups()
    
    if "MASTER FOOTER (INJECTED SITE-WIDE)" not in style_content:
        return False

    # Split and take only the style part before any injected footer block
    parts = style_content.split("/* ===== MASTER FOOTER (INJECTED SITE-WIDE) ===== */")
    clean_style = parts[0].strip()

    # Reassemble style content with exactly one clean injected style block
    new_style_content = f"{clean_style}\n\n{FOOTER_CSS.strip()}\n    "
    new_content = content.replace(style_content, new_style_content)

    # Deduplicate toggleMobileMenu if any multiple blocks exists
    if "toggleMobileMenu" in new_content:
        new_content = re.sub(r'<script>\s*function toggleMobileMenu.*?</script>', '', new_content, flags=re.DOTALL)
        
        MOBILE_SCRIPT = """    <script>
        function toggleMobileMenu() { 
            var m = document.getElementById('elbMobileMenu'), 
                b = document.getElementById('navHamburger'); 
            if (m && b) { 
                m.classList.toggle('open'); 
                b.classList.toggle('open'); 
                document.body.style.overflow = m.classList.contains('open') ? 'hidden' : '';
            } 
        }
    </script>"""
        new_content = new_content.replace("</body>", MOBILE_SCRIPT.strip() + "\n</body>")

    # Final cleanup of any stray duplicate comments
    new_content = re.sub(r'(<!-- Master Footer -->\s*)+', '<!-- Master Footer -->\n', new_content)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    return True

def main():
    directory = "."
    count = 0
    for root, dirs, files in os.walk(directory):
        if '.git' in root or '_archive' in root or 'scratch' in root or 'fragments' in root:
            continue
        for file in files:
            if file.endswith('.html'):
                path = os.path.join(root, file)
                try:
                    if clean_file(path):
                        count += 1
                        print(f"Deduplicated and updated: {path}")
                except Exception as e:
                    print(f"Error on {path}: {e}")
    print(f"\nSuccessfully cleaned and standardized {count} files!")

if __name__ == '__main__':
    main()
