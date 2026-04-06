import os
import re

def ultimate_maritime_sidebar_fix():
    count = 0
    
    # 1. The Elite Sidebar Layout CSS & HTML
    # Widget on the Left, Form on the Right
    ELITE_MARITIME_LAYOUT = """
            <div class="elite-maritime-hero-split" style="display: flex; gap: 2.5rem; margin-top: 3rem; align-items: flex-start; flex-wrap: wrap;">
                
                <!-- LEFT: PARTNER WIDGET -->
                <div class="maritime-partner-sidebar" style="flex: 0 0 320px; max-width: 320px;">
                    <p style="color: var(--primary-gold); font-size: 0.7rem; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 1.5rem; text-align: center;">Global Fleet Access</p>
                    <!-- ELB_YACHTING_AFFILIATE_WIDGET_START -->
                    <div class="yachting-affiliate-container" style="background: rgba(255,255,255,0.02); padding: 0.5rem; border-radius: 15px; border: 1px solid rgba(212,175,55,0.15); overflow: hidden;">
                        <a href="https://www.yachting.com/en-gb?AffiliateID=elbookings&BannerID=1729a6e6" target="_top" style="display: block; border-radius: 10px; overflow: hidden;">
                            <img src="//affiliate.yachting.com/accounts/default1/ne6ayxbkog/1729a6e6.png" alt="Exclusive Yacht Charter" width="320" height="800" style="width:100%; height:auto; display:block;" />
                        </a>
                    </div>
                    <!-- ELB_YACHTING_AFFILIATE_WIDGET_END -->
                </div>

                <!-- RIGHT: ELITE FORM HUB -->
                <div class="maritime-lead-core" style="flex: 1; min-width: 350px;">
                    <div class="urgency-alert" style="background: rgba(255, 77, 77, 0.05); border: 1px solid rgba(255, 77, 77, 0.3); padding: 12px 20px; border-radius: 12px; margin-bottom: 1.5rem; display: flex; align-items: center; justify-content: center; gap: 15px;">
                        <span style="position: relative; display: flex; height: 12px; width: 12px;">
                            <span style="animation: ping 1.5s infinite; position: absolute; height: 100%; width: 100%; border-radius: 50%; background-color: #ff4d4d; opacity: 0.75;"></span>
                            <span style="border-radius: 50%; height: 12px; width: 12px; background-color: #ff4d4d;"></span>
                        </span>
                        <span style="color: #ff4d4d; font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;">Strategic Slot Alert: High Demand Season</span>
                    </div>

                    <div class="glass-panel" style="padding: 2.5rem; border: 1px solid var(--primary-gold); background: rgba(5,5,5,0.8);">
                        <h3 class="serif gold-text" style="font-size: 2.2rem; margin-bottom: 0.5rem; text-align: center;">Elite Maritime Inquiry</h3>
                        <p style="text-align: center; color: var(--text-muted); font-size: 0.8rem; margin-bottom: 2rem; text-transform: uppercase; letter-spacing: 2px;">Direct Concierge Dispatch</p>
                        
                        <form action="https://formspree.io/f/xwvwanlj" method="POST" style="display: flex; flex-direction: column; gap: 1.2rem;">
                            <input type="text" name="name" placeholder="Full Name" style="width: 100%; border-radius: 8px; border: 1px solid rgba(255,255,255,0.1); padding: 1.2rem; background: rgba(0,0,0,0.3); color: #fff;" required>
                            <input type="email" name="email" placeholder="Email Address" style="width: 100%; border-radius: 8px; border: 1px solid rgba(255,255,255,0.1); padding: 1.2rem; background: rgba(0,0,0,0.3); color: #fff;" required>
                            <input type="tel" name="phone" placeholder="WhatsApp Number" style="width: 100%; border-radius: 8px; border: 1px solid rgba(255,255,255,0.1); padding: 1.2rem; background: rgba(0,0,0,0.3); color: #fff;" required>
                            <textarea name="requirements" placeholder="Preferred Destination, Yacht Type (Superyacht, Catamaran...), or Group Size..." style="width: 100%; border-radius: 8px; border: 1px solid rgba(255,255,255,0.1); padding: 1.2rem; background: rgba(0,0,0,0.3); color: #fff; min-height: 100px;" required></textarea>
                            <button type="submit" class="btn btn-gold" style="width: 100%; font-size: 1.1rem; min-height: 65px; font-weight: 700;">Inquire for Elite Rates</button>
                        </form>
                    </div>
                </div>
            </div>
"""

    for root, dirs, files in os.walk("."):
        for file in files:
            if file == "index.html":
                filepath = os.path.join(root, file)
                if not ("yacht" in root.lower() or "boat" in root.lower() or "yacht" in file.lower()):
                    continue

                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                original = content
                
                # 1. Restore the Hero Header (Fixing the ERASURE error)
                # We identify the title from the metadata if H1 is missing
                title_match = re.search(r'<title>(.*?) \|', content)
                page_title = title_match.group(1) if title_match else "Elite Yacht Charter"
                
                # Rebuild the Hero section completely
                new_hero = f"""
    <header class="hero">
        <div class="container">
            <div class="tag-strip" style="margin-bottom: 2rem;">
                <span class="tag-item">Global Yacht Network</span>
                <span class="tag-item">5-Star Crewed Charters</span>
                <span class="tag-item">Confidential Coordination</span>
            </div>
            <h1>{page_title}</h1>
            {ELITE_MARITIME_LAYOUT}
        </div>
    </header>
"""
                # Replace the broken header container
                content = re.sub(r'<header class="hero">.*?</header>', new_hero, content, flags=re.DOTALL)

                # 2. Cleanup misplaced widgets from sidebar/bottom
                content = re.sub(r'<div class="yacht-sidebar-affiliate".*?</div>\s*</div>', '', content, flags=re.DOTALL)
                content = re.sub(r'<!-- ELB_YACHTING_AFFILIATE_WIDGET_START -->.*?<!-- ELB_YACHTING_AFFILIATE_WIDGET_END -->', '', content, flags=re.DOTALL)

                # 3. Final Footer/Gallery Cleanup
                content = re.sub(r'(<!-- ELB_FOOTER_START -->.*?<!-- ELB_FOOTER_END -->\s*)+', r'\1', content, flags=re.DOTALL)

                if content != original:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    count += 1

    print(f"Ultimate Maritime Fix: {count} pages restored with Sidebar Layout (Partner Left, Form Right).")

if __name__ == "__main__":
    ultimate_maritime_sidebar_fix()
