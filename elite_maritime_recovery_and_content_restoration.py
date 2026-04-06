import os
import re

def elite_maritime_recovery_and_content_restoration():
    count = 0
    # Standardized Centered Elite Maritime Lead Hub (Formspree)
    MARITIME_FORM_HUB = """
            <div class="urgency-alert" style="background: rgba(255, 77, 77, 0.05); border: 1px solid rgba(255, 77, 77, 0.4); padding: 12px 20px; border-radius: 15px; margin: 1.5rem auto 1.5rem; max-width: 700px; display: flex; align-items: center; justify-content: center; gap: 15px;">
                <span style="position: relative; display: flex; height: 10px; width: 10px;">
                    <span style="animation: ping 1.5s infinite; position: absolute; height: 100%; width: 100%; border-radius: 50%; background-color: #ff4d4d; opacity: 0.75;"></span>
                    <span style="border-radius: 50%; height: 10px; width: 10px; background-color: #ff4d4d;"></span>
                </span>
                <span style="color: #ff4d4d; font-size: 0.85rem; font-weight: 700; text-transform: uppercase; letter-spacing: 2px;">Strategic Slot Alert: High Demand Season</span>
            </div>

            <div class="maritime-lead-hub glass-panel" style="margin: 0 auto 2.5rem; max-width: 800px; padding: 2.5rem; border: 1px solid var(--primary-gold); background: rgba(5,5,5,0.92); border-radius: 20px; box-shadow: 0 40px 100px rgba(0,0,0,0.7); text-align: left;">
                <h3 class="serif gold-text" style="font-size: 2.2rem; margin-bottom: 0.5rem; text-align: center;">Elite Maritime Inquiry</h3>
                <p style="text-align: center; color: var(--text-muted); font-size: 0.8rem; margin-bottom: 2.5rem; text-transform: uppercase; letter-spacing: 3px;">Direct Senior Concierge Dispatch</p>
                <form action="https://formspree.io/f/xwvwanlj" method="POST" style="display: flex; flex-direction: column; gap: 1.2rem;">
                    <input type="text" name="name" placeholder="Full Name" style="width: 100%; border-radius: 8px; border: 1px solid rgba(255,255,255,0.12); padding: 1.2rem; background: rgba(0,0,0,0.4); color: #fff;" required>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                        <input type="email" name="email" placeholder="Email Address" style="border-radius: 8px; border: 1px solid rgba(255,255,255,0.12); padding: 1.2rem; background: rgba(0,0,0,0.4); color: #fff;" required>
                        <input type="tel" name="phone" placeholder="WhatsApp Number" style="border-radius: 8px; border: 1px solid rgba(255,255,255,0.12); padding: 1.2rem; background: rgba(0,0,0,0.4); color: #fff;" required>
                    </div>
                    <textarea name="requirements" placeholder="Preferred Routing, Yacht Categories (Superyacht, Sailing...), or Specialist Requirements..." style="width: 100%; border-radius: 8px; border: 1px solid rgba(255,255,255,0.12); padding: 1.2rem; background: rgba(0,0,0,0.4); color: #fff; min-height: 100px;" required></textarea>
                    <button type="submit" class="btn btn-gold" style="width: 100%; font-size: 1.2rem; min-height: 70px; font-weight: 800; text-transform: uppercase; letter-spacing: 4px;">Request Priority Portfolio</button>
                    <p style="text-align: center; font-size: 0.7rem; color: var(--text-muted); margin-top: 1rem;">Elite Luxury Bookings: Private Concierge Dispatch worldwide within 15 Minutes.</p>
                </form>
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
                
                # 1. Purge Aviation Leaks & Broken Wrappers
                content = re.sub(r'<!-- Column 2: The Americas Hub -->.*?Private Concierge Response within 120 Minutes.</p>\s*</div>\s*</div>\s*</section>', '', content, flags=re.DOTALL)
                content = re.sub(r'<p style="color: var\(--text-muted\); font-size: 0.9rem; max-width: 600px; margin: 0 auto;">Elite Luxury Bookings operates 1,200\+ global city-pairs\..*?</p>', '', content, flags=re.DOTALL)
                content = re.sub(r'<section class="section-padding container">\s*<!-- Column 2: The Americas Hub -->\s*</section>', '', content, flags=re.DOTALL)

                # 2. Extract Page Title & Rebuild Elite Hero
                title_match = re.search(r'<title>(.*?) \|', content)
                page_title = title_match.group(1) if title_match else "Elite Yacht Charter"
                
                final_header = f"""
    <header class="hero">
        <div class="container">
            <div class="tag-strip" style="margin-bottom: 1.5rem;">
                <span class="tag-item">Global Yacht Network</span>
                <span class="tag-item">5-Star Crewed Charters</span>
                <span class="tag-item">Confidential Coordination</span>
            </div>
            <h1 style="margin-bottom: 0px;">{page_title}</h1>
            {MARITIME_FORM_HUB}
        </div>
    </header>
"""
                # Restore the clean Hero
                content = re.sub(r'<header class="hero">.*?</header>', final_header, content, flags=re.DOTALL)
                content = re.sub(r'<article class="container">\s*<header class="blog-header">.*?</header>', final_header, content, flags=re.DOTALL)

                # 3. Restore Content If It Was Erased (Surgical Restoration)
                if "Ibiza to Mallorca" in page_title and ("Crossing Times" not in content):
                    content = content.replace("</header>", f"</header>\n<section class='section-padding container'><div class='blog-content'><h2>The Ultimate Balearic Crossing: Ibiza to Mallorca</h2><p>Experiencing the transition from Ibiza to Mallorca by private yacht is the pinnacle of Balearic luxury. Our expert maritime coordinators specialize in arranging seamless, discrete crossings that maximize your time on the water. From the rugged north coast of Mallorca to the vibrant shores of Ibiza, every nautical mile is coordinated for the world's most discerning travelers.</p><h3>Elite Itinerary Highlights</h3><ul class='luxury-list'><li><strong>Discrete Coordination:</strong> Precision logistics for HNWIs demanding absolute privacy.</li><li><strong>Michelin-tier Catering:</strong> Private chefs trained in Europe's most prestigious kitchens.</li><li><strong>Direct Marina Access:</strong> Secure berths in the Balearics' most exclusive yacht clubs.</li></ul></div></section>")

                # 4. Final Deduplication (Fixing the Duplicate Footer Bug)
                content = re.sub(r'(<!-- ELB_FOOTER_START -->.*?<!-- ELB_FOOTER_END -->\s*)+', r'\1', content, flags=re.DOTALL)
                content = re.sub(r'(<div class="maritime-partner-footer-banner".*?</div>\s*)+', r'\1', content, flags=re.DOTALL)

                if content != original:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    count += 1

    print(f"Elite Maritime Recovery: {count} pages restored and re-standardized.")

if __name__ == "__main__":
    elite_maritime_recovery_and_content_restoration()
