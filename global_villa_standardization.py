import os
import re

def global_villa_standardization():
    count = 0
    # Standardized Centered Elite Villa Lead Hub (Formspree)
    VILLA_FORM_HUB = """
            <div class="urgency-alert" style="background: rgba(255, 77, 77, 0.05); border: 1px solid rgba(255, 77, 77, 0.4); padding: 12px 20px; border-radius: 15px; margin: 1.5rem auto 1.5rem; max-width: 700px; display: flex; align-items: center; justify-content: center; gap: 15px;">
                <span style="position: relative; display: flex; height: 10px; width: 10px;">
                    <span style="animation: ping 1.5s infinite; position: absolute; height: 100%; width: 100%; border-radius: 50%; background-color: #ff4d4d; opacity: 0.75;"></span>
                    <span style="border-radius: 50%; height: 10px; width: 10px; background-color: #ff4d4d;"></span>
                </span>
                <span style="color: #ff4d4d; font-size: 0.85rem; font-weight: 700; text-transform: uppercase; letter-spacing: 2px;">Strategic Slot Alert: Peak Season Demand - Inquire Early</span>
            </div>

            <div class="villa-lead-hub glass-panel" style="margin: 0 auto 2.5rem; max-width: 800px; padding: 2.5rem; border: 1px solid var(--primary-gold); background: rgba(5,5,5,0.92); border-radius: 20px; box-shadow: 0 40px 100px rgba(0,0,0,0.7); text-align: left;">
                <h3 class="serif gold-text" style="font-size: 2.2rem; margin-bottom: 0.5rem; text-align: center;">Elite Villa Inquiry</h3>
                <p style="text-align: center; color: var(--text-muted); font-size: 0.8rem; margin-bottom: 2.5rem; text-transform: uppercase; letter-spacing: 3px;">Direct Senior Villa Concierge Dispatch</p>
                <form action="https://formspree.io/f/xwvwanlj" method="POST" style="display: flex; flex-direction: column; gap: 1.2rem;">
                    <input type="text" name="name" placeholder="Full Name" style="width: 100%; border-radius: 8px; border: 1px solid rgba(255,255,255,0.12); padding: 1.2rem; background: rgba(0,0,0,0.4); color: #fff;" required>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                        <input type="email" name="email" placeholder="Email Address" style="border-radius: 8px; border: 1px solid rgba(255,255,255,0.12); padding: 1.2rem; background: rgba(0,0,0,0.4); color: #fff;" required>
                        <input type="tel" name="phone" placeholder="WhatsApp Number" style="border-radius: 8px; border: 1px solid rgba(255,255,255,0.12); padding: 1.2rem; background: rgba(0,0,0,0.4); color: #fff;" required>
                    </div>
                    <textarea name="requirements" placeholder="Preferred Estate Locations, Property Type (Pool, Beachfront, etc.), or Specialist Staffing Requirements..." style="width: 100%; border-radius: 8px; border: 1px solid rgba(255,255,255,0.12); padding: 1.2rem; background: rgba(0,0,0,0.4); color: #fff; min-height: 100px;" required></textarea>
                    <button type="submit" class="btn btn-gold" style="width: 100%; font-size: 1.2rem; min-height: 70px; font-weight: 800; text-transform: uppercase; letter-spacing: 4px;">Request Priority Estate Portfolio</button>
                    <p style="text-align: center; font-size: 0.7rem; color: var(--text-muted); margin-top: 1rem;">Elite Luxury Bookings: Private Villa Coordination worldwide within 30 Minutes.</p>
                </form>
            </div>
"""

    # The Elite Villa Content Hub Template
    def get_villa_content_hub(title):
        clean_name = title.split(':')[0].split('|')[0].replace("Villa Rental", "").replace("Villas", "").strip()
        return f"""
    <!-- ELB_CONTENT_HUB_START -->
    <section class="section-padding" style="background: rgba(212, 175, 55, 0.02); border-bottom: 1px solid rgba(212,175,55,0.1); padding: 4rem 0;">
        <div class="container">
            <div class="grid-2" style="display: grid; grid-template-columns: 1fr 1fr; gap: 4rem; align-items: start;">
                <div class="seo-content">
                    <h2 class="serif" style="font-size: 2.3rem; margin-bottom: 1.5rem;">Bespoke Excellence: {clean_name} Villa Guide</h2>
                    <p style="margin-bottom: 1.2rem; color: #fff; opacity: 0.9; line-height: 1.6;">Securing a <strong>Elite {clean_name} Sanctuary</strong> is the coordination of a world-class property experience. Our estate portfolio is curated for those who demand absolute seclusion and 5-star hospitality standards.</p>
                    <p style="color: #fff; opacity: 0.9; line-height: 1.6;">From secluded Aspen retreats to beachfront Maldives sanctuaries, every stay is tailored to your specific requirements, ensuring your time is as productive or as relaxing as you desire.</p>
                </div>
                <div class="glass-panel" style="padding: 2.5rem; background: rgba(5,5,5,0.6); border: 1px solid rgba(212,175,55,0.15); border-radius: 20px; backdrop-filter: blur(20px);">
                    <h3 class="serif gold-text" style="margin-top:0; font-size: 1.8rem; margin-bottom: 1.5rem;">Villa Standards</h3>
                    <ul class="luxury-list" style="list-style: none; padding: 0;">
                        <li style="margin-bottom: 1.2rem; padding-left: 0; position: relative;"><strong style="color:#fff;">Discrete Security:</strong> Fully vetted, high-security invisible perimeters.</li>
                        <li style="margin-bottom: 1.2rem; padding-left: 0; position: relative;"><strong style="color:#fff;">Elite Staffing:</strong> Private chefs, housekeepers, and specialized concierges.</li>
                        <li style="padding-left: 0; position: relative;"><strong style="color:#fff;">Confidential Access:</strong> Hand-selected, off-market estate portfolios.</li>
                    </ul>
                </div>
            </div>
        </div>
    </section>
    <!-- ELB_CONTENT_HUB_END -->
"""

    for root, dirs, files in os.walk("."):
        for file in files:
            if file == "index.html":
                filepath = os.path.join(root, file)
                # Filter for Villa categories
                if not ("villa" in root.lower() or "villa" in file.lower() or "luxury-villa" in root.lower()):
                    continue

                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                original = content
                
                # 1. Purge Legacy/Duplicated Content Blocks
                content = re.sub(r'<!-- ELB_CONTENT_HUB_START -->.*?<!-- ELB_CONTENT_HUB_END -->', '', content, flags=re.DOTALL)
                content = re.sub(r'<section class="section-padding".*?Bespoke Excellence:.*?</section>', '', content, flags=re.DOTALL)

                # 2. Extract and Sanitize Title
                title_match = re.search(r'<title>(.*?) \|', content)
                if not title_match: title_match = re.search(r'<title>(.*?)</title>', content)
                page_title = title_match.group(1) if title_match else "Private Villa"
                
                # 3. Inject Elite Hero (Center Alignment)
                final_header = f"""
    <header class="hero">
        <div class="container">
            <div class="tag-strip" style="margin-bottom: 1.5rem;">
                <span class="tag-item">Global Estate Network</span>
                <span class="tag-item">Hand-Selected Sanctuaries</span>
                <span class="tag-item">Confidential Coordination</span>
            </div>
            <h1 style="margin-bottom: 0px;">{page_title}</h1>
            {VILLA_FORM_HUB}
        </div>
    </header>
"""
                # Replace existing hero or prepend below Nav
                if "<header class=\"hero\">" in content:
                    content = re.sub(r'<header class="hero">.*?</header>', final_header, content, flags=re.DOTALL)
                
                # 4. Inject Elite Content Grid
                if "</header>" in content:
                    content = content.replace("</header>", f"</header>\n{get_villa_content_hub(page_title)}")

                # 5. Final Deduplication (Fixing the Duplicate Footer Bug)
                content = re.sub(r'(<!-- ELB_FOOTER_START -->.*?<!-- ELB_FOOTER_END -->\s*)+', r'\1', content, flags=re.DOTALL)
                # Ensure footer is centered
                content = content.replace('text-align: left;', 'text-align: center;')

                if content != original:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    count += 1

    print(f"Global Villa Standardization: {count} pages brought to Elite Bespoke Standard.")

if __name__ == "__main__":
    global_villa_standardization()
