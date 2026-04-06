import os
import re

def maritime_standard_deployer():
    count = 0
    
    # 1. Standardized Maritime Lead Hub with Urgency (Formspree)
    # Using the high-end Amsterdam-style logic
    MARITIME_UBER_HERO = """
            <div class="urgency-alert" style="background: rgba(255, 77, 77, 0.05); border: 1px solid rgba(255, 77, 77, 0.3); padding: 12px 20px; border-radius: 12px; margin: 2rem auto 1.5rem; max-width: 700px; display: flex; align-items: center; justify-content: center; gap: 15px; animation: fadeIn 1s ease-out;">
                <span style="position: relative; display: flex; height: 12px; width: 12px;">
                    <span style="animation: ping 1.5s cubic-bezier(0, 0, 0.2, 1) infinite; position: absolute; display: inline-flex; height: 100%; width: 100%; border-radius: 50%; background-color: #ff4d4d; opacity: 0.75;"></span>
                    <span style="position: relative; display: inline-flex; border-radius: 50%; height: 12px; width: 12px; background-color: #ff4d4d;"></span>
                </span>
                <span style="color: #ff4d4d; font-size: 0.95rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;">Strategic Slot Alert: Peak Season Demand - Inquire Early</span>
            </div>

            <!-- ELB_MARITIME_FORM_START -->
            <div class="maritime-lead-hub glass-panel" style="margin: 2rem auto; max-width: 800px; padding: 2.5rem; border: 1px solid var(--primary-gold); background: rgba(5,5,5,0.85); backdrop-filter: blur(20px); border-radius: 20px; box-shadow: 0 20px 50px rgba(0,0,0,0.6);">
                <h3 class="serif gold-text" style="font-size: 2.2rem; margin-bottom: 0.5rem; text-align: center;">Elite Maritime Inquiry</h3>
                <p style="text-align: center; color: var(--text-muted); font-size: 0.85rem; margin-bottom: 2.5rem; text-transform: uppercase; letter-spacing: 3px;">Direct Support from a Senior Yacht Advisor</p>
                
                <form action="https://formspree.io/f/xwvwanlj" method="POST" style="display: flex; flex-direction: column; gap: 1.2rem;">
                    <input type="text" name="name" placeholder="Full Name" style="width: 100%; border-radius: 8px; border: 1px solid rgba(212,175,55,0.2); padding: 1.2rem; background: rgba(0,0,0,0.3); color: #fff;" required>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                        <input type="email" name="email" placeholder="Email Address" style="border-radius: 8px; border: 1px solid rgba(212,175,55,0.2); padding: 1.2rem; background: rgba(0,0,0,0.3); color: #fff;" required>
                        <input type="tel" name="phone" placeholder="WhatsApp Number" style="border-radius: 8px; border: 1px solid rgba(212,175,55,0.2); padding: 1.2rem; background: rgba(0,0,0,0.3); color: #fff;" required>
                    </div>
                    <textarea name="requirements" placeholder="Preferred Destination, Yacht Type (Superyacht, Catamaran...), or Group Size..." style="width: 100%; border-radius: 8px; border: 1px solid rgba(212,175,55,0.2); padding: 1.2rem; background: rgba(0,0,0,0.3); color: #fff; min-height: 120px;" required></textarea>
                    
                    <button type="submit" class="btn btn-gold" style="width: 100%; margin-top: 1rem; font-size: 1.2rem; min-height: 70px; font-weight: 700; text-transform: uppercase; letter-spacing: 3px;">Secure Exclusive Yacht Rates</button>
                    <p style="text-align: center; font-size: 0.75rem; color: var(--text-muted); margin-top: 1.2rem;">Elite Luxury Bookings: Concierge Dispatch within 120 Minutes.</p>
                </form>
            </div>
            <!-- ELB_MARITIME_FORM_END -->
"""

    for root, dirs, files in os.walk("."):
        for file in files:
            if file == "index.html":
                filepath = os.path.join(root, file)
                
                # Check if it's a maritime page
                if not ("yacht" in root.lower() or "boat" in root.lower() or "yacht" in file.lower() or "luxury-yacht" in root.lower()):
                    continue

                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                original = content
                
                # A. EXTRACT WIDGET (Any Variant)
                widget_match = re.search(r'<!-- (ELB_YACHTING_AFFILIATE_WIDGET|ELB_YACHTING_WIDGET)_START -->.*?<!-- (ELB_YACHTING_AFFILIATE_WIDGET|ELB_YACHTING_WIDGET)_END -->', content, flags=re.DOTALL)
                widget_html = ""
                if widget_match:
                    widget_html = widget_match.group(0)
                    content = content.replace(widget_html, "")
                    
                # B. REMOVE IMAGES ABOVE HUB (Strict images purge)
                content = re.sub(r'<div class="hero-image-container">.*?</div>', '', content, flags=re.DOTALL)
                content = re.sub(r'<img src="[^"]+" alt="[^"]+" class="blog-hero-img".*?>', '', content, flags=re.DOTALL)
                # Remove common header pexels images if they sit near the top
                content = re.sub(r'<div class="hero-parallax-bg".*?></div>', '', content, flags=re.DOTALL)

                # C. INJECT Standardized Hero Hub after H1
                h1_match = re.search(r'(<h1.*?>.*?</h1>)', content, flags=re.DOTALL)
                if h1_match:
                    # Wipe any existing urgency/form blocks
                    content = re.sub(r'<div class="urgency-alert".*?</div>', '', content, flags=re.DOTALL)
                    content = re.sub(r'<!-- (ELB_MARITIME_FORM|MARITIME_LEAD)_START -->.*?<!-- (ELB_MARITIME_FORM|MARITIME_LEAD)_END -->', '', content, flags=re.DOTALL)
                    content = re.sub(r'<form action="https://formspree.io/f/xwvwanlj".*?</form>', '', content, flags=re.DOTALL)
                    # Inject standardized Hub
                    content = content.replace(h1_match.group(1), f"{h1_match.group(1)}\n{MARITIME_UBER_HERO}")

                # D. Sidebar/Bottom injection for Affiliate Partner
                if widget_html:
                    sidebar_wrap = f"""
<div class="yacht-sidebar-affiliate" style="margin-top: 4rem; text-align: center; border-top: 1px solid rgba(212,175,55,0.1); padding-top: 3rem;">
    <p style="color: var(--primary-gold); font-size: 0.7rem; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 2rem;">Explore Global Partner Fleet</p>
    {widget_html}
</div>
"""
                    content = content.replace("<!-- ELB_FOOTER_START -->", f"{sidebar_wrap}\n<!-- ELB_FOOTER_START -->")

                # E. Cleanup silhouettes & duplicate sidebars
                content = re.sub(r'<div class="yacht-sidebar-affiliate" style="margin-top: 3rem; text-align: center;">\s*<p.*?>Global Partner Fleet</p>\s*</div>', '', content, flags=re.DOTALL)
                content = re.sub(r'(<!-- ELB_FOOTER_START -->.*?<!-- ELB_FOOTER_END -->\s*)+', r'\1', content, flags=re.DOTALL)

                if content != original:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    count += 1

    print(f"Maritime Reform Successful: {count} pages brought to Elite Standard.")

if __name__ == "__main__":
    maritime_standard_deployer()
