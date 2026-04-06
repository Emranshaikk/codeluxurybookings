import os
import re

FOOTER_TEMPLATE = """
    <!-- ELB_FOOTER_START -->
    <footer class="section-padding" style="background: #000; border-top: 1px solid rgba(255,255,255,0.05); text-align: center; margin-top: 5rem;">
        <div class="container">
            <a href="/" style="display: block; margin-bottom: 2rem; font-family:'Cormorant Garamond',serif; font-size:2rem; font-weight:600; color:#fff; text-decoration:none;"><span style="color:#D4AF37;">Elite</span> Luxury Bookings</a>
            <div style="display: flex; justify-content: center; gap: 3rem; flex-wrap: wrap; margin-bottom: 2rem;">
                <a href="/elite-private-jet-charter/" style="color: rgba(255,255,255,0.6); text-decoration: none; font-size: 0.9rem;">Aviation Services</a>
                <a href="/luxury-yacht-rentals/" style="color: rgba(255,255,255,0.6); text-decoration: none; font-size: 0.9rem;">Yacht Charter</a>
                <a href="/luxury-villa-rentals/" style="color: rgba(255,255,255,0.6); text-decoration: none; font-size: 0.9rem;">Villa Rentals</a>
                <a href="/blog/" style="color: rgba(255,255,255,0.6); text-decoration: none; font-size: 0.9rem;">Blog</a>
                <a href="/contact/" style="color: rgba(255,255,255,0.6); text-decoration: none; font-size: 0.9rem;">Contact</a>
            </div>
            <p style="color: #444; font-size: 0.8rem;">© 2026 Elite Luxury Bookings. All rights reserved.</p>
        </div>
    </footer>
    <!-- ELB_FOOTER_END -->
"""

def emergency_patch():
    # Base directory
    base = "c:\\Users\\imran\\OneDrive\\Desktop\\ELB code"
    count = 0
    
    # 1. Get all folders in base
    items = os.listdir(base)
    
    for item in items:
        item_path = os.path.join(base, item)
        if os.path.isdir(item_path):
            # Check for index.html in this folder
            index_path = os.path.join(item_path, 'index.html')
            if os.path.exists(index_path):
                try:
                    with open(index_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Skip if footer already present
                    if "<!-- ELB_FOOTER_START -->" in content:
                        continue
                        
                    # Inject before </body>
                    if "</body>" in content:
                        # Clean duplicate section ends if they exist (common in routes)
                        content = content.replace("</div>\n    </section>\n\n</body>", "</div>\n    </section>")
                        
                        modified = content.replace("</body>", f"{FOOTER_TEMPLATE}\n</body>")
                        with open(index_path, 'w', encoding='utf-8') as f:
                            f.write(modified)
                        count += 1
                except Exception as e:
                    print(f"Error on {index_path}: {e}")
                    
    # Also do the root index.html
    root_index = os.path.join(base, 'index.html')
    # Use existing logic for root if footer missing
    print(f"Emergency Patch Complete: Restored footer to {count} service directories.")

if __name__ == "__main__":
    emergency_patch()
