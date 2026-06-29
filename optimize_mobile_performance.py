import os
import re

# Set the path to the workspace directory
workspace_dir = r"c:\Users\imran\OneDrive\Desktop\ELB code"

# Target Javascript scroll listener pattern
old_js_pattern = """        // ===== STICKY MOBILE CTA =====
        function dismissStickyMobileCta(event) {
            event.stopPropagation();
            event.preventDefault();
            const cta = document.getElementById('stickyMobileCta');
            cta.style.transform = 'translateY(100px)';
            cta.style.opacity = '0';
            setTimeout(() => {
                cta.style.display = 'none';
            }, 500);
            sessionStorage.setItem('sticky_dismissed', '1');
        }

        window.addEventListener('scroll', function () {
            if (window.innerWidth >= 768) {
                document.getElementById('stickyMobileCta').style.display = 'none';
                return;
            }

            if (sessionStorage.getItem('sticky_dismissed') === '1') {
                return;
            }

            const cta = document.getElementById('stickyMobileCta');
            if (window.scrollY > 400) {
                if (cta.style.display !== 'block') {
                    cta.style.display = 'block';
                    cta.offsetHeight; // force reflow
                    cta.style.transform = 'translateY(0)';
                    cta.style.opacity = '1';
                }
            } else {
                if (cta.style.display === 'block') {
                    cta.style.transform = 'translateY(100px)';
                    cta.style.opacity = '0';
                    setTimeout(() => {
                        if (window.scrollY <= 400) {
                            cta.style.display = 'none';
                        }
                    }, 500);
                }
            }
        });"""

new_js_code = """        // ===== STICKY MOBILE CTA =====
        function dismissStickyMobileCta(event) {
            event.stopPropagation();
            event.preventDefault();
            const cta = document.getElementById('stickyMobileCta');
            if (cta) {
                cta.style.transform = 'translateY(100px)';
                cta.style.opacity = '0';
                cta.style.pointerEvents = 'none';
                sessionStorage.setItem('sticky_dismissed', '1');
            }
        }

        // Initialize sticky mobile CTA styles safely to prevent layout reflows on scroll
        const initStickyCta = document.getElementById('stickyMobileCta');
        if (initStickyCta) {
            initStickyCta.style.display = 'block';
            initStickyCta.style.pointerEvents = 'none';
        }

        window.addEventListener('scroll', function () {
            const cta = document.getElementById('stickyMobileCta');
            if (!cta) return;

            if (window.innerWidth >= 768) {
                cta.style.transform = 'translateY(100px)';
                cta.style.opacity = '0';
                cta.style.pointerEvents = 'none';
                return;
            }

            if (sessionStorage.getItem('sticky_dismissed') === '1') {
                return;
            }

            if (window.scrollY > 400) {
                cta.style.transform = 'translateY(0)';
                cta.style.opacity = '1';
                cta.style.pointerEvents = 'auto';
            } else {
                cta.style.transform = 'translateY(100px)';
                cta.style.opacity = '0';
                cta.style.pointerEvents = 'none';
            }
        });"""

# Target HTML footer socials pattern
old_socials = """                    <div class="footer-socials">
                        <a href="https://www.facebook.com/eliteluxurybookings" target="_blank" rel="noopener noreferrer"><i class="fab fa-facebook"></i></a>
                        <a href="https://www.instagram.com/eliteluxurybookings" target="_blank" rel="noopener noreferrer"><i class="fab fa-instagram"></i></a>
                        <a href="https://www.linkedin.com/company/elite-luxury-bookings/" target="_blank" rel="noopener noreferrer"><i class="fab fa-linkedin"></i></a>
                        <a href="https://x.com/eliteluxuryb" target="_blank" rel="noopener noreferrer"><i class="fab fa-x-twitter"></i></a>
                    </div>"""

new_socials = """                    <div class="footer-socials">
                        <a href="https://www.facebook.com/eliteluxurybookings" target="_blank" rel="noopener noreferrer" aria-label="Follow Elite Luxury Bookings on Facebook"><i class="fab fa-facebook"></i></a>
                        <a href="https://www.instagram.com/eliteluxurybookings" target="_blank" rel="noopener noreferrer" aria-label="Follow Elite Luxury Bookings on Instagram"><i class="fab fa-instagram"></i></a>
                        <a href="https://www.linkedin.com/company/elite-luxury-bookings/" target="_blank" rel="noopener noreferrer" aria-label="Follow Elite Luxury Bookings on LinkedIn"><i class="fab fa-linkedin"></i></a>
                        <a href="https://x.com/eliteluxuryb" target="_blank" rel="noopener noreferrer" aria-label="Follow Elite Luxury Bookings on X (Twitter)"><i class="fab fa-x-twitter"></i></a>
                    </div>"""

def process_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    modified = False
    
    # 1. Replace Javascript reflow block if found
    if old_js_pattern in content:
        content = content.replace(old_js_pattern, new_js_code)
        modified = True
    else:
        # Fallback regex search for cases with minor spacing differences
        # Normalize carriage returns for the search
        normalized_content = content.replace('\r\n', '\n')
        normalized_pattern = old_js_pattern.replace('\r\n', '\n')
        if normalized_pattern in normalized_content:
            normalized_content = normalized_content.replace(normalized_pattern, new_js_code.replace('\r\n', '\n'))
            content = normalized_content.replace('\n', '\n') # Maintain normal line endings if needed
            modified = True

    # 2. Replace Footer social links if found
    if old_socials in content:
        content = content.replace(old_socials, new_socials)
        modified = True
    else:
        normalized_content = content.replace('\r\n', '\n')
        normalized_socials = old_socials.replace('\r\n', '\n')
        if normalized_socials in normalized_content:
            normalized_content = normalized_content.replace(normalized_socials, new_socials.replace('\r\n', '\n'))
            content = normalized_content
            modified = True

    if modified:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Processed: {os.path.basename(file_path)}")
        return True
    return False

def main():
    html_files = [os.path.join(workspace_dir, f) for f in os.listdir(workspace_dir) if f.endswith(".html")]
    modified_count = 0
    
    print(f"Scanning {len(html_files)} HTML files...")
    for file_path in html_files:
        if process_file(file_path):
            modified_count += 1
            
    print(f"\nDone! Modified {modified_count} out of {len(html_files)} HTML files.")

if __name__ == "__main__":
    main()
