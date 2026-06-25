import os
import re

# Standardized Footer HTML with E-E-A-T disclaimer (no 2026 year)
FOOTER_HTML = """
    <!-- Master Footer -->
    <footer class="footer">
        <div class="container" style="max-width: 1200px;">
            <div class="footer-grid">
                <div class="footer-brand">
                    <h2>Elite Luxury <span class="gold-text">Bookings</span></h2>
                    <p>Curating world-class luxury experiences through our global partner network. Private Jets. Yachts. Villas.</p>
                    <div class="footer-socials">
                        <a href="https://www.facebook.com/eliteluxurybookings" target="_blank" rel="noopener noreferrer"><i class="fab fa-facebook"></i></a>
                        <a href="https://www.instagram.com/eliteluxurybookings" target="_blank" rel="noopener noreferrer"><i class="fab fa-instagram"></i></a>
                        <a href="https://www.linkedin.com/company/elite-luxury-bookings/" target="_blank" rel="noopener noreferrer"><i class="fab fa-linkedin"></i></a>
                        <a href="https://x.com/eliteluxuryb" target="_blank" rel="noopener noreferrer"><i class="fab fa-x-twitter"></i></a>
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
                <p>&copy; Elite Luxury Bookings. All rights reserved. Global Authority in Luxury Procurement. Elite Luxury Bookings acts as an air charter broker and does not operate aircraft. Flights are operated by certified direct carriers meeting ARGUS, Wyvern, and CAA/EASA safety standards.</p>
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

def clean_year_references(content):
    # 1. Update Ticker alert references: "Summer 2026" or "Upcoming Summer 2026" -> "Upcoming Summer"
    content = re.sub(r'Summer 2026', 'the Upcoming Summer', content)
    content = re.sub(r'summer 2026', 'the upcoming summer', content)
    
    # 2. Update common title, meta, or heading patterns
    content = re.sub(r'Cost Guide 2026', 'Cost Guide', content)
    content = re.sub(r'cost guide 2026', 'cost guide', content)
    content = re.sub(r'2026 Private Jet', 'Private Jet', content)
    content = re.sub(r'2026 private jet', 'private jet', content)
    content = re.sub(r'2026 Price Estimator', 'Bespoke Price Estimator', content)
    content = re.sub(r'2026 price estimator', 'bespoke price estimator', content)
    content = re.sub(r'2026 pricing', 'current pricing', content)
    content = re.sub(r'2026 Pricing', 'Current Pricing', content)
    content = re.sub(r'2026 Edition', 'Latest Edition', content)
    content = re.sub(r'2026 edition', 'latest edition', content)
    
    # 3. Clean up other generic 2026 references in content (meta descriptions / paragraphs)
    content = re.sub(r'for 2026', 'currently', content)
    content = re.sub(r'for the 2026 season', 'for the upcoming season', content)
    content = re.sub(r'in 2026', 'currently', content)
    
    # 4. Clean up any literal occurrences of "2026" in page titles/h1s if not caught above
    # Match patterns like: "Dubai 2026:" -> "Dubai:" or "Dubai 2026" -> "Dubai"
    content = re.sub(r'Dubai 2026', 'Dubai', content)
    content = re.sub(r'dubai 2026', 'dubai', content)
    
    # But leave copyright year references in the footer clean, which we replace completely anyway.
    return content

def process_html_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Apply year cleanup
    content = clean_year_references(content)
    
    # Replace footer with standard E-E-A-T disclaimer footer
    # 1. Clean up redundant old footer style definitions if any
    content = re.sub(r'/\* --- STANDARDIZED FOOTER --- \*/.*?/\* --- END ELITE MOBILE NAV --- \*/', '', content, flags=re.DOTALL)
    
    # 2. Standardize existing footer block or replace standard tags
    content = re.sub(r'<footer.*?>.*?</footer>', FOOTER_HTML.strip(), content, flags=re.DOTALL)
    content = re.sub(r'<!-- ELB_FOOTER_START -->.*?<!-- ELB_FOOTER_END -->', FOOTER_HTML.strip(), content, flags=re.DOTALL)
    
    # 3. Ensure the mobile menu toggle function script is present and not duplicated
    if "toggleMobileMenu()" in content:
        content = re.sub(r'<script>\s*function toggleMobileMenu.*?</script>', '', content, flags=re.DOTALL)
    
    if "</body>" in content:
        footer_script_block = f"\n{MOBILE_SCRIPT.strip()}\n"
        # Avoid duplicate injections
        if footer_script_block.strip() not in content:
            content = content.replace("</body>", footer_script_block + "</body>")

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def run_upgrades():
    directory = "."
    files = [f for f in os.listdir(directory) if f.endswith(".html")]
    print(f"Auditing and upgrading {len(files)} files...")
    
    updated_count = 0
    for filename in files:
        filepath = os.path.join(directory, filename)
        try:
            if process_html_file(filepath):
                print(f"Successfully optimized: {filename}")
                updated_count += 1
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            
    print(f"Upgrades complete. Optimized {updated_count} files.")

if __name__ == "__main__":
    run_upgrades()
