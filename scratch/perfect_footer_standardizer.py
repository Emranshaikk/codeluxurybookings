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

FOOTER_HTML = """    <!-- Master Footer -->
    <footer class="footer">
        <div class="container" style="max-width: 1200px;">
            <div class="footer-grid">
                <div class="footer-brand">
                    <h2>Elite Luxury <span class="gold-text">Bookings</span></h2>
                    <p>Curating world-class luxury experiences through our global partner network. Private Jets. Yachts. Villas.</p>
                    <div class="footer-socials">
                        <a href="https://www.facebook.com/eliteluxurybookings"><i class="fab fa-facebook"></i></a>
                        <a href="https://www.instagram.com/eliteluxurybookings"><i class="fab fa-instagram"></i></a>
                        <a href="https://www.linkedin.com/company/elite-luxury-bookings/"><i class="fab fa-linkedin"></i></a>
                        <a href="https://x.com/eliteluxuryb"><i class="fab fa-x-twitter"></i></a>
                    </div>
                </div>
                <div class="footer-col">
                    <h4>SERVICES</h4>
                    <ul>
                        <li><a href="https://eliteluxurybookings.com/elite-private-jet-charter/">Private Jets</a></li>
                        <li><a href="https://eliteluxurybookings.com/luxury-yacht-rentals/">Luxury Yachts</a></li>
                        <li><a href="https://eliteluxurybookings.com/luxury-villa-rentals/">Luxury Villas</a></li>
                        <li><a href="https://eliteluxurybookings.com/global-route-silo/">Route Directory</a></li>
                        <li><a href="https://eliteluxurybookings.com/blog/">Blog</a></li>
                    </ul>
                </div>
                <div class="footer-col">
                    <h4>AUTHORITY</h4>
                    <ul>
                        <li><a href="https://eliteluxurybookings.com/about/">The Mission</a></li>
                        <li><a href="https://eliteluxurybookings.com/privacy/">Privacy Protocol</a></li>
                        <li><a href="https://eliteluxurybookings.com/terms/">Terms of Engagement</a></li>
                        <li><a href="https://eliteluxurybookings.com/contact/">Connect</a></li>
                    </ul>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2026 Elite Luxury Bookings. All rights reserved. Global Authority in Luxury Procurement.</p>
                <div class="footer-legal">
                    <a href="https://eliteluxurybookings.com/privacy/">Privacy</a>
                    <a href="https://eliteluxurybookings.com/terms/">Terms</a>
                </div>
            </div>
        </div>
    </footer>"""

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

FONTAWESOME_LINK = '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">'

def standardize_file(path):
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Skip known layout files that should not have footer, or legacy
    if any(k in path for k in ['old_blog.html', 'fragments']):
        return False

    modified = False

    # 1. Strip ALL master footer blocks, regardless of equal sign length or carriage returns
    clean_content = re.sub(r'/\*\s*=+\s*MASTER FOOTER \(INJECTED SITE-WIDE\)\s*=+\s*\*/.*?(?=\s*</style>)', '', content, flags=re.DOTALL)
    if clean_content != content:
        content = clean_content
        modified = True

    # 2. Inject exactly one clean copy of FOOTER_CSS before the last </style>
    last_style_idx = content.rfind('</style>')
    if last_style_idx != -1:
        if "MASTER FOOTER (INJECTED SITE-WIDE)" not in content:
            content = content[:last_style_idx] + FOOTER_CSS + "\n    " + content[last_style_idx:]
            modified = True

    # 3. Add FontAwesome if missing
    if "font-awesome" not in content.lower():
        if "</head>" in content:
            content = content.replace("</head>", f"    {FONTAWESOME_LINK}\n</head>")
            modified = True

    # 4. Standardize Footer HTML
    footer_pattern = re.compile(r'<footer.*?>.*?</footer>', re.DOTALL)
    if footer_pattern.search(content):
        new_content = footer_pattern.sub(FOOTER_HTML.strip(), content)
        if new_content != content:
            content = new_content
            modified = True
    else:
        if "</body>" in content:
            footer_block = f"\n    <!-- Master Footer -->\n{FOOTER_HTML.strip()}\n{MOBILE_SCRIPT.strip()}\n"
            content = content.replace("</body>", footer_block + "</body>")
            modified = True

    # 5. Clean toggleMobileMenu
    if "toggleMobileMenu" in content:
        new_content = re.sub(r'<script>\s*function toggleMobileMenu.*?</script>', '', content, flags=re.DOTALL)
        if new_content != content:
            content = new_content
            modified = True
        content = content.replace("</body>", MOBILE_SCRIPT.strip() + "\n</body>")
        modified = True

    # 6. Deduplicate Master Footer comment
    new_content = re.sub(r'(<!-- Master Footer -->\s*)+', '<!-- Master Footer -->\n', content)
    if new_content != content:
        content = new_content
        modified = True

    if modified:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

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
                    if standardize_file(path):
                        count += 1
                        print(f"Standardized: {path}")
                except Exception as e:
                    print(f"Error on {path}: {e}")
    print(f"\nSuccessfully cleaned and standardized {count} files!")

if __name__ == '__main__':
    main()
