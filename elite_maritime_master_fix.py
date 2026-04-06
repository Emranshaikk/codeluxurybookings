import os
import re

def elite_maritime_master_fix():
    count = 0
    
    # 1. The Corrected Elite Sidebar Layout
    ELITE_MARITIME_LAYOUT = """
            <div class="elite-maritime-hero-split" style="display: flex; gap: 2.5rem; margin-top: 3rem; align-items: flex-start; flex-wrap: wrap; text-align: left;">
                
                <!-- LEFT: PARTNER WIDGET (320px Skyscraper) -->
                <div class="maritime-partner-sidebar" style="flex: 0 0 320px; max-width: 320px; width: 100%;">
                    <p style="color: var(--primary-gold); font-size: 0.7rem; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 1.5rem; text-align: center;">Global Fleet Access</p>
                    <!-- ELB_YACHTING_PARTNER_WIDGET_START -->
                    <div class="yachting-affiliate-container" style="background: rgba(255,255,255,0.02); padding: 0.5rem; border-radius: 15px; border: 1px solid rgba(212,175,55,0.15); box-shadow: 0 10px 30px rgba(0,0,0,0.3); overflow: hidden;">
                        <a href="https://www.yachting.com/en-gb?AffiliateID=elbookings&BannerID=1729a6e6" target="_top" style="display: block; border-radius: 10px; overflow: hidden;">
                            <img src="//affiliate.yachting.com/accounts/default1/ne6ayxbkog/1729a6e6.png" alt="Exclusive Yacht Charter" width="320" height="800" style="width:100%; height:auto; display:block;" />
                        </a>
                    </div>
                    <!-- ELB_YACHTING_PARTNER_WIDGET_END -->
                </div>

                <!-- RIGHT: ELITE LEAD HUB -->
                <div class="maritime-lead-core" style="flex: 1; min-width: 350px;">
                    <div class="urgency-alert" style="background: rgba(255, 77, 77, 0.05); border: 1px solid rgba(255, 77, 77, 0.3); padding: 12px 20px; border-radius: 12px; margin-bottom: 2rem; display: flex; align-items: center; justify-content: center; gap: 15px;">
                        <span style="position: relative; display: flex; height: 12px; width: 12px;">
                            <span style="animation: ping 1.5s infinite; position: absolute; height: 100%; width: 100%; border-radius: 50%; background-color: #ff4d4d; opacity: 0.75;"></span>
                            <span style="border-radius: 50%; height: 12px; width: 12px; background-color: #ff4d4d;"></span>
                        </span>
                        <span style="color: #ff4d4d; font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;">Strategic Slot Alert: Peak Season Demand</span>
                    </div>

                    <div class="glass-panel" style="padding: 3rem; border: 1px solid var(--primary-gold); background: rgba(5,5,5,0.9); box-shadow: 0 25px 60px rgba(0,0,0,0.5);">
                        <h3 class="serif gold-text" style="font-size: 2.3rem; margin-bottom: 0.5rem; text-align: center;">Bespoke Maritime Inquiry</h3>
                        <p style="text-align: center; color: var(--text-muted); font-size: 0.8rem; margin-bottom: 2.5rem; text-transform: uppercase; letter-spacing: 3px;">Direct Senior Advisor Connection</p>
                        
                        <form action="https://formspree.io/f/xwvwanlj" method="POST" style="display: flex; flex-direction: column; gap: 1.5rem;">
                            <input type="text" name="name" placeholder="Full Name" style="width: 100%; border-radius: 8px; border: 1px solid rgba(255,255,255,0.12); padding: 1.2rem; background: rgba(0,0,0,0.3); color: #fff;" required>
                            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                                <input type="email" name="email" placeholder="Email Address" style="border-radius: 8px; border: 1px solid rgba(255,255,255,0.12); padding: 1.2rem; background: rgba(0,0,0,0.3); color: #fff;" required>
                                <input type="tel" name="phone" placeholder="WhatsApp Number" style="border-radius: 8px; border: 1px solid rgba(255,255,255,0.12); padding: 1.2rem; background: rgba(0,0,0,0.3); color: #fff;" required>
                            </div>
                            <textarea name="requirements" placeholder="Preferred Destination, Yacht Type (Superyacht, Sailing...), or Dates..." style="width: 100%; border-radius: 8px; border: 1px solid rgba(255,255,255,0.12); padding: 1.2rem; background: rgba(0,0,0,0.3); color: #fff; min-height: 120px;" required></textarea>
                            <button type="submit" class="btn btn-gold" style="width: 100%; font-size: 1.2rem; min-height: 75px; font-weight: 700; text-transform: uppercase; letter-spacing: 4px;">Request Exclusive Proposal</button>
                            <p style="text-align: center; font-size: 0.7rem; color: var(--text-muted); margin-top: 1rem;">Elite Luxury Bookings: Concierge Dispatch within 15 Minutes.</p>
                        </form>
                    </div>
                </div>
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
                
                # A. PRE-INJECTION CLEANUP (Delete all legacy/broken blocks FIRST)
                content = re.sub(r'<!-- (ELB_YACHTING_AFFILIATE_WIDGET|ELB_YACHTING_WIDGET|ELB_YACHTING_PARTNER_WIDGET)_START -->.*?<!-- (ELB_YACHTING_AFFILIATE_WIDGET|ELB_YACHTING_WIDGET|ELB_YACHTING_PARTNER_WIDGET)_END -->', '', content, flags=re.DOTALL)
                content = re.sub(r'<div class="yacht-sidebar-affiliate".*?</div>\s*</div>', '', content, flags=re.DOTALL)
                content = re.sub(r'<div class="urgency-alert".*?</div>', '', content, flags=re.DOTALL)
                content = re.sub(r'<!-- ELB_MARITIME_FORM_START -->.*?<!-- ELB_MARITIME_FORM_END -->', '', content, flags=re.DOTALL)
                content = re.sub(r'<form action="https://formspree.io/f/xwvwanlj".*?</form>', '', content, flags=re.DOTALL)

                # B. IDENTIFY TITLE & REBUILD HERO
                title_match = re.search(r'<title>(.*?) \|', content)
                page_title = title_match.group(1) if title_match else "Elite Yacht Charter"
                
                final_header = f"""
    <header class="hero">
        <div class="container">
            <div class="tag-strip" style="margin-bottom: 2.5rem;">
                <span class="tag-item">Global Yacht Network</span>
                <span class="tag-item">5-Star Crewed Charters</span>
                <span class="tag-item">Confidential Coordination</span>
            </div>
            <h1 style="margin-bottom: 1rem;">{page_title}</h1>
            {ELITE_MARITIME_LAYOUT}
        </div>
    </header>
"""
                # Replace the entire broken hero container
                content = re.sub(r'<header class="hero">.*?</header>', final_header, content, flags=re.DOTALL)

                # C. Final Sanitization (No repeated footers)
                content = re.sub(r'(<!-- ELB_FOOTER_START -->.*?<!-- ELB_FOOTER_END -->\s*)+', r'\1', content, flags=re.DOTALL)

                if content != original:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    count += 1

    print(f"Elite Maritime Master Fix: {count} pages perfected with Side-by-Side conversion layout.")

if __name__ == "__main__":
    elite_maritime_master_fix()
