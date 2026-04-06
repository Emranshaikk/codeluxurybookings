import os
import re

def purge_maritime_widgets():
    count = 0
    
    # Standardized Centered Elite Maritime Lead Hub (Formspree)
    MARITIME_CENTERED_HERO = """
            <div class="urgency-alert" style="background: rgba(255, 77, 77, 0.05); border: 1px solid rgba(255, 77, 77, 0.4); padding: 12px 20px; border-radius: 15px; margin: 2rem auto 2rem; max-width: 700px; display: flex; align-items: center; justify-content: center; gap: 15px;">
                <span style="position: relative; display: flex; height: 12px; width: 12px;">
                    <span style="animation: ping 1.5s infinite; position: absolute; height: 100%; width: 100%; border-radius: 50%; background-color: #ff4d4d; opacity: 0.75;"></span>
                    <span style="border-radius: 50%; height: 12px; width: 12px; background-color: #ff4d4d;"></span>
                </span>
                <span style="color: #ff4d4d; font-size: 0.9rem; font-weight: 700; text-transform: uppercase; letter-spacing: 2px;">Strategic Slot Alert: High Demand Season</span>
            </div>

            <div class="maritime-lead-hub glass-panel" style="margin: 0 auto 4rem; max-width: 800px; padding: 3rem; border: 1px solid var(--primary-gold); background: rgba(5,5,5,0.92); border-radius: 25px; box-shadow: 0 40px 100px rgba(0,0,0,0.7); text-align: left;">
                <h3 class="serif gold-text" style="font-size: 2.5rem; margin-bottom: 0.5rem; text-align: center;">Elite Maritime Inquiry</h3>
                <p style="text-align: center; color: var(--text-muted); font-size: 0.85rem; margin-bottom: 3rem; text-transform: uppercase; letter-spacing: 4px;">Direct Concierge Dispatch</p>
                
                <form action="https://formspree.io/f/xwvwanlj" method="POST" style="display: flex; flex-direction: column; gap: 1.5rem;">
                    <input type="text" name="name" placeholder="Full Name" style="width: 100%; border-radius: 10px; border: 1px solid rgba(255,255,255,0.12); padding: 1.3rem; background: rgba(0,0,0,0.4); color: #fff;" required>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.2rem;">
                        <input type="email" name="email" placeholder="Email Address" style="border-radius: 10px; border: 1px solid rgba(255,255,255,0.12); padding: 1.3rem; background: rgba(0,0,0,0.4); color: #fff;" required>
                        <input type="tel" name="phone" placeholder="WhatsApp / Phone Number" style="border-radius: 10px; border: 1px solid rgba(255,255,255,0.12); padding: 1.3rem; background: rgba(0,0,0,0.4); color: #fff;" required>
                    </div>
                    <textarea name="requirements" placeholder="Preferred Charter Destination, Yacht Portfolio Selection, or Specialist Requirements..." style="width: 100%; border-radius: 10px; border: 1px solid rgba(255,255,255,0.12); padding: 1.3rem; background: rgba(0,0,0,0.4); color: #fff; min-height: 140px;" required></textarea>
                    
                    <button type="submit" class="btn btn-gold" style="width: 100%; font-size: 1.3rem; min-height: 80px; font-weight: 800; text-transform: uppercase; letter-spacing: 5px;">Secure Priority Portfolio</button>
                    <p style="text-align: center; font-size: 0.75rem; color: var(--text-muted); margin-top: 1.5rem; letter-spacing: 1px;">Official Elite Luxury Network: Response Guaranteed within 15 Minutes.</p>
                </form>
            </div>
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
                
                # 1. Broad Widget Silo Purge (Left, Sidebar, Partner, etc)
                content = re.sub(r'<!-- (ELB_YACHTING_AFFILIATE_WIDGET|ELB_YACHTING_WIDGET|ELB_YACHTING_PARTNER_WIDGET)_START -->.*?<!-- (ELB_YACHTING_AFFILIATE_WIDGET|ELB_YACHTING_WIDGET|ELB_YACHTING_PARTNER_WIDGET)_END -->', '', content, flags=re.DOTALL)
                content = re.sub(r'<div class="elite-maritime-hero-split".*?<!-- RIGHT: ELITE .*?</div>\s*</div>\s*</div>', '', content, flags=re.DOTALL)
                content = re.sub(r'<div class="yacht-sidebar-affiliate".*?</div>\s*</div>', '', content, flags=re.DOTALL)
                
                # 2. Extract Title & Rebuild Single Centered Hero
                title_match = re.search(r'<title>(.*?) \|', content)
                page_title = title_match.group(1) if title_match else "Elite Yacht Charter"
                
                final_centered_header = f"""
    <header class="hero">
        <div class="container">
            <div class="tag-strip" style="margin-bottom: 2.5rem;">
                <span class="tag-item">Global Yacht Network</span>
                <span class="tag-item">5-Star Crewed Charters</span>
                <span class="tag-item">Confidential Coordination</span>
            </div>
            <h1 style="margin-bottom: 1rem;">{page_title}</h1>
            {MARITIME_CENTERED_HERO}
        </div>
    </header>
"""
                # Re-inject the centered Elite hero
                content = re.sub(r'<header class="hero">.*?</header>', final_centered_header, content, flags=re.DOTALL)

                # 3. Final Consolidation & Cleanup
                content = re.sub(r'(<!-- ELB_FOOTER_START -->.*?<!-- ELB_FOOTER_END -->\s*)+', r'\1', content, flags=re.DOTALL)

                if content != original:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    count += 1

    print(f"Maritime Purge Successful: {count} pages brought to the Centered Elite Standard.")

if __name__ == "__main__":
    purge_maritime_widgets()
