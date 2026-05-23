import os
import re

# Standardized Footer CSS
FOOTER_CSS = """
        /* ===== MASTER FOOTER (INJECTED SITE-WIDE) ===== */
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
        }
"""

FOOTER_HTML = """
    <!-- Master Footer -->
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
    </footer>
"""

MOBILE_SCRIPT = """
    <script>
        function toggleMobileMenu() { 
            var m = document.getElementById('elbMobileMenu'), 
                b = document.getElementById('navHamburger'); 
            if (m && b) { 
                m.classList.toggle('open'); 
                b.classList.toggle('open'); 
                document.body.style.overflow = m.classList.contains('open') ? 'hidden' : '';
            } 
        }
    </script>
"""

FONTAWESOME_LINK = '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">'

directory = r"c:\Users\imran\OneDrive\Desktop\ELB code"

for filename in os.listdir(directory):
    if filename.endswith(".html"):
        path = os.path.join(directory, filename)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 1. Clean up redundant CSS
        # Remove legacy footer CSS block if it exists
        content = re.sub(r'/\* --- STANDARDIZED FOOTER --- \*/.*?/\* --- END ELITE MOBILE NAV --- \*/', '', content, flags=re.DOTALL)
        
        # 2. Inject MASTER FOOTER CSS into <style> if missing
        if "MASTER FOOTER (INJECTED SITE-WIDE)" not in content:
            if "</style>" in content:
                content = content.replace("</style>", FOOTER_CSS + "\n    </style>")
        
        # 3. Add FontAwesome if missing
        if "font-awesome" not in content:
            if "</head>" in content:
                content = content.replace("</head>", f"    {FONTAWESOME_LINK}\n</head>")
        
        # 4. Clean up stray </div> tags and redundant comments before the footer
        # This matches the pattern seen in the blog pages: </div> followed by comments and whitespace
        content = re.sub(r'(</div>\s*){1,5}(<!-- Master Footer -->\s*)+', '', content, flags=re.DOTALL)
        
        # 5. REPLACE FOOTER
        # Remove any existing footer
        content = re.sub(r'<footer.*?>.*?</footer>', '', content, flags=re.DOTALL)
        # Remove legacy hubs
        content = re.sub(r'<!-- Elite Intelligence Hubs -->.*?</div>\s*</div>\s*</div>', '', content, flags=re.DOTALL)
        content = re.sub(r'<div class="intel-hub-section".*?</div>\s*</div>\s*</div>', '', content, flags=re.DOTALL)
        
        # Additional cleanup for excessive empty lines before the footer
        content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content)
        
        # 6. Inject Footer and Mobile Script
        if "</body>" in content:
            # Remove existing mobile script if present to avoid duplicates
            content = re.sub(r'<script>\s*function toggleMobileMenu.*?</script>', '', content, flags=re.DOTALL)
            
            # Place Footer and Script before </body>
            # We use a clean block and ensure only one Master Footer comment exists
            footer_block = f"\n    <!-- Master Footer -->\n{FOOTER_HTML.strip()}\n{MOBILE_SCRIPT.strip()}\n"
            content = content.replace("</body>", footer_block + "</body>")
            
            # Final deduplication of the Master Footer comment
            content = re.sub(r'(<!-- Master Footer -->\s*)+', '<!-- Master Footer -->\n', content)

        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Standardized {filename}")

