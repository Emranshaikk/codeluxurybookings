import os
import re

def re_center_maritime_footer():
    count = 0
    # The Corrected Standard Elite Footer (Centered)
    CENTERED_FOOTER_HTML = """
<!-- ELB_FOOTER_START -->
    <footer class="section-padding" style="background: #000; border-top: 1px solid rgba(255,255,255,0.05); text-align: center !important; margin-top: 4rem; padding: 5rem 0;">
        <div class="container" style="display: block !important; text-align: center !important;">
            <a href="/" style="display: inline-block; margin-bottom: 2rem; font-family:'Cormorant Garamond',serif; font-size:2.2rem; font-weight:600; color:#fff; text-decoration:none;"><span style="color:#D4AF37;">Elite</span> Luxury Bookings</a>
            <div style="display: flex; justify-content: center; gap: 3rem; flex-wrap: wrap; margin-bottom: 2.5rem;">
                <a href="/elite-private-jet-charter/" style="color: rgba(255,255,255,0.6); text-decoration: none; font-size: 0.9rem; letter-spacing: 1.5px; text-transform: uppercase;">Aviation</a>
                <a href="/luxury-yacht-rentals/" style="color: rgba(255,255,255,0.6); text-decoration: none; font-size: 0.9rem; letter-spacing: 1.5px; text-transform: uppercase;">Maritime</a>
                <a href="/luxury-villa-rentals/" style="color: rgba(255,255,255,0.6); text-decoration: none; font-size: 0.9rem; letter-spacing: 1.5px; text-transform: uppercase;">Villas</a>
                <a href="/blog/" style="color: rgba(255,255,255,0.6); text-decoration: none; font-size: 0.9rem; letter-spacing: 1.5px; text-transform: uppercase;">Blog</a>
                <a href="/contact/" style="color: rgba(255,255,255,0.6); text-decoration: none; font-size: 0.9rem; letter-spacing: 1.5px; text-transform: uppercase;">Contact</a>
            </div>
            <p style="color: #555; font-size: 0.8rem; letter-spacing: 1px;">© 2026 Elite Luxury Bookings. Discrete Concierge Worldwide.</p>
        </div>
    </footer>
<!-- ELB_FOOTER_END -->
"""

    for root, dirs, files in os.walk("."):
        for file in files:
            if file == "index.html":
                filepath = os.path.join(root, file)
                if not ("yacht" in root.lower() or "boat" in root.lower() or "yacht" in file.lower() or "luxury-yacht" in root.lower()):
                    continue

                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                original = content
                
                # 1. Surgical Footer Replacement
                # Ensure the entire footer block is replaced with the centered version
                content = re.sub(r'<!-- ELB_FOOTER_START -->.*?<!-- ELB_FOOTER_END -->', CENTERED_FOOTER_HTML, content, flags=re.DOTALL)
                
                # 2. Cleanup any loose footer fragments outside the start/end markers
                # (Deleting duplicated logos if they somehow leaked out)
                content = re.sub(r'<footer class="section-padding" style="background: #000;.*?</footer>', CENTERED_FOOTER_HTML, content, flags=re.DOTALL, count=1)

                # 3. Final Deduplication (No double-footers)
                content = re.sub(r'(<!-- ELB_FOOTER_START -->.*?<!-- ELB_FOOTER_END -->\s*)+', r'\1', content, flags=re.DOTALL)

                if content != original:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    count += 1

    print(f"Maritime Footer Corrected: {count} pages re-centered.")

if __name__ == "__main__":
    re_center_maritime_footer()
