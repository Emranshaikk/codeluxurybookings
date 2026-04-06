import os
import re

def perfect_maritime_balance():
    count = 0
    
    # 1. Perfectly Balanced "Mirror" Layout
    # Height is fixed to ~680px to align the widget with the lead form perfectly.
    BALANCED_MARITIME_LAYOUT = """
            <div class="elite-maritime-hero-split" style="display: flex; gap: 2rem; margin-top: 3.5rem; align-items: stretch; flex-wrap: wrap; text-align: left; justify-content: center;">
                
                <!-- LEFT: PARTNER WIDGET (Balanced Height & Width) -->
                <div class="maritime-partner-sidebar" style="flex: 0 0 350px; max-width: 350px; width: 100%; height: 680px; display: flex; flex-direction: column;">
                    <p style="color: var(--primary-gold); font-size: 0.7rem; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 1.5rem; text-align: center; font-weight: 600;">Global Partner Fleet</p>
                    <div class="yachting-affiliate-container" style="background: rgba(255,255,255,0.02); padding: 0.5rem; border-radius: 20px; border: 1px solid var(--primary-gold); box-shadow: 0 15px 40px rgba(0,0,0,0.4); overflow: hidden; flex: 1; position: relative;">
                        <a href="https://www.yachting.com/en-gb?AffiliateID=elbookings&BannerID=1729a6e6" target="_top" style="display: block; width: 100%; height: 100%; border-radius: 12px; overflow: hidden;">
                            <img src="//affiliate.yachting.com/accounts/default1/ne6ayxbkog/1729a6e6.png" alt="Exclusive Yacht Charter" width="320" height="1200" style="width:100%; height:100%; object-fit: cover; display:block;" />
                        </a>
                        <div style="position: absolute; bottom: 0; left: 0; right: 0; background: linear-gradient(transparent, rgba(0,0,0,0.8)); padding: 1rem; text-align: center;">
                            <span style="color: #fff; font-size: 0.7rem; text-transform: uppercase; letter-spacing: 1.5px;">Official Maritime Partner</span>
                        </div>
                    </div>
                </div>

                <!-- RIGHT: ELITE FORM HUB (Balanced Height) -->
                <div class="maritime-lead-core" style="flex: 1; min-width: 380px; max-width: 750px; display: flex; flex-direction: column; justify-content: flex-start;">
                    <div class="urgency-alert" style="background: rgba(255, 77, 77, 0.05); border: 1px solid rgba(255, 77, 77, 0.4); padding: 12px 20px; border-radius: 15px; margin-bottom: 2rem; display: flex; align-items: center; justify-content: center; gap: 15px;">
                        <span style="position: relative; display: flex; height: 10px; width: 10px;">
                            <span style="animation: ping 1.5s infinite; position: absolute; height: 100%; width: 100%; border-radius: 50%; background-color: #ff4d4d; opacity: 0.75;"></span>
                            <span style="border-radius: 50%; height: 10px; width: 10px; background-color: #ff4d4d;"></span>
                        </span>
                        <span style="color: #ff4d4d; font-size: 0.8rem; font-weight: 700; text-transform: uppercase; letter-spacing: 2px;">Strategic Slot Alert: High Demand Season</span>
                    </div>

                    <div class="glass-panel" style="padding: 2.5rem; border: 1px solid var(--primary-gold); background: rgba(5,5,5,0.92); border-radius: 20px; box-shadow: 0 30px 70px rgba(0,0,0,0.6); flex: 1; display: flex; flex-direction: column; justify-content: center;">
                        <h3 class="serif gold-text" style="font-size: 2.3rem; margin-bottom: 0.5rem; text-align: center;">Elite Maritime Inquiry</h3>
                        <p style="text-align: center; color: var(--text-muted); font-size: 0.8rem; margin-bottom: 2.5rem; text-transform: uppercase; letter-spacing: 3px;">Direct Senior Broker Dispatch</p>
                        
                        <form action="https://formspree.io/f/xwvwanlj" method="POST" style="display: flex; flex-direction: column; gap: 1.2rem;">
                            <input type="text" name="name" placeholder="Full Name" style="width: 100%; border-radius: 8px; border: 1px solid rgba(255,255,255,0.12); padding: 1.1rem; background: rgba(0,0,0,0.4); color: #fff;" required>
                            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                                <input type="email" name="email" placeholder="Email Address" style="border-radius: 8px; border: 1px solid rgba(255,255,255,0.12); padding: 1.1rem; background: rgba(0,0,0,0.4); color: #fff;" required>
                                <input type="tel" name="phone" placeholder="WhatsApp / Phone" style="border-radius: 8px; border: 1px solid rgba(255,255,255,0.12); padding: 1.1rem; background: rgba(0,0,0,0.4); color: #fff;" required>
                            </div>
                            <textarea name="requirements" placeholder="Preferred Destination, Yacht Categories (Superyacht, Sailing...), or Group Size..." style="width: 100%; border-radius: 8px; border: 1px solid rgba(255,255,255,0.12); padding: 1.1rem; background: rgba(0,0,0,0.4); color: #fff; min-height: 100px;" required></textarea>
                            <button type="submit" class="btn btn-gold" style="width: 100%; font-size: 1.2rem; min-height: 75px; font-weight: 800; text-transform: uppercase; letter-spacing: 4px;">Request Charter Portfolio</button>
                            <p style="text-align: center; font-size: 0.7rem; color: var(--text-muted); margin-top: 1rem;">Elite Luxury Bookings: Private Concierge Response within 15 Minutes.</p>
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
                
                # 1. Clean legacy blocks
                content = re.sub(r'<div class="elite-maritime-hero-split".*?</div>\s*</div>\s*</div>', '', content, flags=re.DOTALL)
                content = re.sub(r'<!-- (ELB_YACHTING_AFFILIATE_WIDGET|ELB_YACHTING_WIDGET|ELB_YACHTING_PARTNER_WIDGET)_START -->.*?<!-- (ELB_YACHTING_AFFILIATE_WIDGET|ELB_YACHTING_WIDGET|ELB_YACHTING_PARTNER_WIDGET)_END -->', '', content, flags=re.DOTALL)

                # 2. Rebuild the Hero with Balanced Split
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
            <h1 style="margin-bottom: 0px;">{page_title}</h1>
            {BALANCED_MARITIME_LAYOUT}
        </div>
    </header>
"""
                # Replace the broken hero container
                content = re.sub(r'<header class="hero">.*?</header>', final_header, content, flags=re.DOTALL)

                # 3. Final Consolidation (No repeated footers)
                content = re.sub(r'(<!-- ELB_FOOTER_START -->.*?<!-- ELB_FOOTER_END -->\s*)+', r'\1', content, flags=re.DOTALL)

                if content != original:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    count += 1

    print(f"Perfect Maritime Balance: {count} pages mirror-standardized.")

if __name__ == "__main__":
    perfect_maritime_balance()
