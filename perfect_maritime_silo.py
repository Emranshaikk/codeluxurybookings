import os
import re

def perfect_maritime_silo():
    count = 0
    FORMSPREE_ENDPOINT = "https://formspree.io/f/xwvwanlj"
    
    # 1. The Standardized Maritime Lead Form Template
    MARITIME_FORM_HTML = """
            <!-- ELB_MARITIME_FORM_START -->
            <div class="maritime-lead-hub glass-panel" style="margin: 2rem auto; max-width: 800px; padding: 2.5rem; border: 1px solid var(--primary-gold); background: rgba(5,5,5,0.8); backdrop-filter: blur(20px); border-radius: 20px; box-shadow: 0 20px 50px rgba(0,0,0,0.5);">
                <h3 class="serif gold-text" style="font-size: 2rem; margin-bottom: 0.5rem; text-align: center;">Bespoke Maritime Inquiry</h3>
                <p style="text-align: center; color: var(--text-muted); font-size: 0.85rem; margin-bottom: 2.5rem; text-transform: uppercase; letter-spacing: 3px;">Direct Fleet Advisor Access</p>
                
                <form action="https://formspree.io/f/xwvwanlj" method="POST" style="display: flex; flex-direction: column; gap: 1.2rem;">
                    <input type="text" name="name" placeholder="Full Name" style="width: 100%; border-radius: 8px; border: 1px solid rgba(255,255,255,0.12); padding: 1.1rem; background: rgba(255,255,255,0.03); color: #fff;" required>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                        <input type="email" name="email" placeholder="Email Address" style="border-radius: 8px; border: 1px solid rgba(255,255,255,0.12); padding: 1.1rem; background: rgba(255,255,255,0.03); color: #fff;" required>
                        <input type="tel" name="phone" placeholder="WhatsApp Number" style="border-radius: 8px; border: 1px solid rgba(255,255,255,0.12); padding: 1.1rem; background: rgba(255,255,255,0.03); color: #fff;" required>
                    </div>
                    <textarea name="requirements" placeholder="Preferred Destination, Yacht Type, or Group Size..." style="width: 100%; border-radius: 8px; border: 1px solid rgba(255,255,255,0.12); padding: 1.1rem; background: rgba(255,255,255,0.03); color: #fff; min-height: 120px;" required></textarea>
                    
                    <button type="submit" class="btn btn-gold" style="width: 100%; margin-top: 1rem; font-size: 1.1rem; min-height: 65px; font-weight: 700; text-transform: uppercase; letter-spacing: 3px;">Inquire for Elite Rates</button>
                    <p style="text-align: center; font-size: 0.75rem; color: var(--text-muted); margin-top: 1rem;">Secure 256-bit Encrypted Submission. Guaranteed Response within 120 Minutes.</p>
                </form>
            </div>
            <!-- ELB_MARITIME_FORM_END -->
"""

    for root, dirs, files in os.walk("."):
        for file in files:
            if file == "index.html":
                filepath = os.path.join(root, file)
                
                # Target: Yacht or Boat pages
                if not ("yacht" in root.lower() or "boat" in root.lower() or "yacht" in file.lower()):
                    continue

                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                original = content
                
                # A. EXTRACT THE AFFILIATE WIDGET (IF AT TOP)
                # We look for the Yachting.com widget blocks
                widget_match = re.search(r'<!-- ELB_YACHTING_AFFILIATE_WIDGET_START -->.*?<!-- ELB_YACHTING_AFFILIATE_WIDGET_END -->', content, flags=re.DOTALL)
                widget_html = ""
                if widget_match:
                    widget_html = widget_match.group(0)
                    # Remove it from top
                    content = content.replace(widget_html, "")
                    
                # B. REMOVE IMAGES ABOVE HUB (Search for images in header/hero area)
                # We specifically target any images sitting near the title
                content = re.sub(r'<div class="hero-image-container">.*?</div>', '', content, flags=re.DOTALL)
                content = re.sub(r'<img src="[^"]+" alt="[^"]+" class="blog-hero-img".*?>', '', content, flags=re.DOTALL)

                # C. INJECT FORM AT TOP (After H1)
                # If form already exists, we replace it with our standardized one.
                if FORMSPREE_ENDPOINT in content or "ELB_MARITIME_FORM_START" in content:
                    # Replace existing form block
                    content = re.sub(r'<!-- ELB_MARITIME_FORM_START -->.*?<!-- ELB_MARITIME_FORM_END -->', MARITIME_FORM_HTML, content, flags=re.DOTALL)
                    # Also replace any raw formspree 
                    content = re.sub(r'<form action="https://formspree.io/f/xwvwanlj".*?</form>', MARITIME_FORM_HTML, content, flags=re.DOTALL)
                else:
                    # Inject for the first time after H1
                    content = re.sub(r'(<h1.*?>.*?</h1>)', f'\\1\n{MARITIME_FORM_HTML}', content, flags=re.DOTALL, count=1)

                # D. MOVE WIDGET TO SIDEBAR (OR BOTTOM IF NO SIDEBAR)
                if widget_html:
                    # We inject it back into a sidebar container, or just before the footer
                    # Using a sidebar wrapper for elite layout
                    sidebar_widget = f"""
<div class="yacht-sidebar-affiliate" style="margin-top: 3rem; text-align: center;">
    <p style="color: var(--primary-gold); font-size: 0.7rem; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 1rem;">Global Partner Fleet</p>
    {widget_html}
</div>
"""
                    # Inject before footer
                    content = content.replace("<!-- ELB_FOOTER_START -->", f"{sidebar_widget}\n<!-- ELB_FOOTER_START -->")

                # E. CLEANUP DUPLICATES
                content = re.sub(r'(<!-- ELB_FOOTER_START -->.*?<!-- ELB_FOOTER_END -->\s*)+', r'\1', content, flags=re.DOTALL)

                if content != original:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    count += 1

    print(f"Maritime Silo Perfection: {count} pages upgraded to Elite Status.")

if __name__ == "__main__":
    perfect_maritime_silo()
