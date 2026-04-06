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

def restore_global_footers():
    count_missing = 0
    count_extra = 0
    
    # Robust patterns
    footer_block_pattern = r'\s*<!-- ELB_FOOTER_START -->.*?<!-- ELB_FOOTER_END -->'
    js_start_pattern = r'\s*<!-- ELB_JS_START -->'
    body_end_pattern = r'\s*</body>'
    
    for root, dirs, files in os.walk('.'):
        if 'index.html' in files:
            path = os.path.join(root, 'index.html')
            
            # Skip assets/temp
            if any(x in root for x in ['assets', '.', 'tmp']):
                continue
                
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original = content
                
                # 1. Purge all existing footer markers (indented or not)
                blocks = list(re.finditer(footer_block_pattern, content, re.DOTALL))
                if len(blocks) > 0:
                    content = re.sub(footer_block_pattern, "", content, flags=re.DOTALL)
                
                # 2. Inject fresh template before the first valid anchor
                if re.search(js_start_pattern, content):
                    content = re.sub(js_start_pattern, f"{FOOTER_TEMPLATE}\n    <!-- ELB_JS_START -->", content, count=1)
                elif re.search(body_end_pattern, content):
                    content = re.sub(body_end_pattern, f"{FOOTER_TEMPLATE}\n</body>", content, count=1)
                
                if content != original:
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    if len(blocks) == 0: count_missing += 1
                    if len(blocks) > 1: count_extra += 1
                        
            except Exception as e:
                print(f"Error processing {path}: {e}")

    print(f"Success: Fixed {count_missing} missing footers and deduplicated {count_extra} files.")

if __name__ == "__main__":
    restore_global_footers()
