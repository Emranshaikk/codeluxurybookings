import os
import re

def emergency_maritime_deduplication():
    count = 0
    # Final Standardized Bottom Widget (Single Instance)
    FINAL_WIDGET_HTML = """
            <div class="maritime-partner-footer-banner" style="margin: 4rem auto 2rem; max-width: 800px; text-align: center; border-top: 1px solid rgba(212,175,55,0.1); padding-top: 3rem;">
                <p style="color: var(--primary-gold); font-size: 0.75rem; text-transform: uppercase; letter-spacing: 3px; margin-bottom: 2rem; font-weight: 600;">Explore Global Partner Fleet</p>
                <div class="partner-banner-wrap" style="display: inline-block; background: rgba(255,255,255,0.02); padding: 0.5rem; border-radius: 12px; border: 1px solid rgba(212,175,55,0.1); box-shadow: 0 10px 30px rgba(0,0,0,0.3); overflow: hidden;">
                    <a href="https://www.yachting.com/en-gb?AffiliateID=elbookings&BannerID=df2a515b" target="_top">
                        <img src="//affiliate.yachting.com/accounts/default1/ne6ayxbkog/df2a515b.png" alt="Exclusive Yacht Charter" title="Elite Partner Fleet" width="728" height="90" style="max-width: 100%; height: auto; display: block; filter: grayscale(0.2) contrast(1.1); transition: filter 0.3s ease;" onmouseover="this.style.filter='grayscale(0) contrast(1.2)'" onmouseout="this.style.filter='grayscale(0.2) contrast(1.1)'" />
                    </a>
                </div>
                <img style="border:0" src="https://affiliate.yachting.com/scripts/ne6ayxikog?AffiliateID=elbookings&BannerID=df2a515b" width="1" height="1" alt="" />
                <p style="color: var(--text-muted); font-size: 0.7rem; margin-top: 1.5rem; letter-spacing: 1px;">Official Yachting Partner of Elite Luxury Bookings</p>
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
                
                # A. AGGRESSIVE PURGE (Targeting any and all variant blocks)
                # We target by class name first
                content = re.sub(r'<div class="maritime-partner-footer-banner".*?</div>\s*</div>\s*</div>', '', content, flags=re.DOTALL)
                content = re.sub(r'<div class="maritime-partner-footer-banner".*?</div>\s*</div>', '', content, flags=re.DOTALL)
                content = re.sub(r'<div class="maritime-partner-footer-banner".*?</div>', '', content, flags=re.DOTALL)
                
                # Wipe any skyscraper sidebar remnants
                content = re.sub(r'<div class="yacht-sidebar-affiliate".*?</div>\s*</div>', '', content, flags=re.DOTALL)
                content = re.sub(r'<div class="yacht-sidebar-affiliate".*?</div>', '', content, flags=re.DOTALL)
                
                # Check for raw widget injections
                content = re.sub(r'<!-- (ELB_YACHTING_AFFILIATE_WIDGET|ELB_YACHTING_WIDGET|ELB_YACHTING_PARTNER_WIDGET)_START -->.*?<!-- (ELB_YACHTING_AFFILIATE_WIDGET|ELB_YACHTING_WIDGET|ELB_YACHTING_PARTNER_WIDGET)_END -->', '', content, flags=re.DOTALL)
                content = re.sub(r'<div class="yachting-affiliate-container".*?</div>', '', content, flags=re.DOTALL)

                # B. SINGLE INJECTION above Footer
                if "<!-- ELB_FOOTER_START -->" in content:
                    content = content.replace("<!-- ELB_FOOTER_START -->", f"{FINAL_WIDGET_HTML}\n<!-- ELB_FOOTER_START -->")

                # C. Final Dedeplication of Footer Markers
                content = re.sub(r'(<!-- ELB_FOOTER_START -->.*?<!-- ELB_FOOTER_END -->\s*)+', r'\1', content, flags=re.DOTALL)

                if content != original:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    count += 1

    print(f"Emergency Deduplication Success: {count} pages restored with SINGLE Elite Partner Footer.")

if __name__ == "__main__":
    emergency_maritime_deduplication()
