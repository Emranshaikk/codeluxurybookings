import os
import re

def marine_blog_content_recovery():
    count = 0
    # Standardized Centered Elite Maritime Lead Hub (Formspree)
    MARITIME_FORM_HUB = """
            <div class="urgency-alert" style="background: rgba(255, 77, 77, 0.05); border: 1px solid rgba(255, 77, 77, 0.4); padding: 12px 20px; border-radius: 15px; margin: 2rem auto 2rem; max-width: 700px; display: flex; align-items: center; justify-content: center; gap: 15px;">
                <span style="position: relative; display: flex; height: 12px; width: 12px;">
                    <span style="animation: ping 1.5s infinite; position: absolute; height: 100%; width: 100%; border-radius: 50%; background-color: #ff4d4d; opacity: 0.75;"></span>
                    <span style="border-radius: 50%; height: 12px; width: 12px; background-color: #ff4d4d;"></span>
                </span>
                <span style="color: #ff4d4d; font-size: 0.9rem; font-weight: 700; text-transform: uppercase; letter-spacing: 2px;">Strategic Slot Alert: High Demand Season</span>
            </div>

            <div class="maritime-lead-hub glass-panel" style="margin: 0 auto 3rem; max-width: 800px; padding: 3rem; border: 1px solid var(--primary-gold); background: rgba(5,5,5,0.92); border-radius: 25px; box-shadow: 0 40px 100px rgba(0,0,0,0.7); text-align: left;">
                <h3 class="serif gold-text" style="font-size: 2.3rem; margin-bottom: 0.5rem; text-align: center;">Elite Maritime Inquiry</h3>
                <p style="text-align: center; color: var(--text-muted); font-size: 0.8rem; margin-bottom: 2.5rem; text-transform: uppercase; letter-spacing: 3px;">Direct Concierge Dispatch</p>
                <form action="https://formspree.io/f/xwvwanlj" method="POST" style="display: flex; flex-direction: column; gap: 1.5rem;">
                    <input type="text" name="name" placeholder="Full Name" style="width: 100%; border-radius: 10px; border: 1px solid rgba(255,255,255,0.12); padding: 1.2rem; background: rgba(0,0,0,0.4); color: #fff;" required>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.2rem;">
                        <input type="email" name="email" placeholder="Email Address" style="border-radius: 10px; border: 1px solid rgba(255,255,255,0.12); padding: 1.2rem; background: rgba(0,0,0,0.4); color: #fff;" required>
                        <input type="tel" name="phone" placeholder="WhatsApp Number" style="border-radius: 10px; border: 1px solid rgba(255,255,255,0.12); padding: 1.2rem; background: rgba(0,0,0,0.4); color: #fff;" required>
                    </div>
                    <textarea name="requirements" placeholder="Preferred Destination, Yacht Selection, or Specialized Requirements..." style="width: 100%; border-radius: 10px; border: 1px solid rgba(255,255,255,0.12); padding: 1.2rem; background: rgba(0,0,0,0.4); color: #fff; min-height: 120px;" required></textarea>
                    <button type="submit" class="btn btn-gold" style="width: 100%; font-size: 1.2rem; min-height: 75px; font-weight: 800; text-transform: uppercase; letter-spacing: 4px;">Request Priority Portfolio</button>
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
                
                # 1. Clean up Duplicated Footers & Stray Widgets (Seen in Ibiza-Mallorca)
                content = re.sub(r'(<!-- ELB_FOOTER_START -->.*?<!-- ELB_FOOTER_END -->\s*)+', r'\1', content, flags=re.DOTALL)
                content = re.sub(r'(<div class="maritime-partner-footer-banner".*?</div>\s*)+', r'\1', content, flags=re.DOTALL)

                # 2. Inject Lead Form if Missing (Checking for both WordPress and Hero structures)
                if "maritime-lead-hub" not in content:
                    # Target H1 as the anchor for both blog and hero pages
                    h1_pattern = r'</h1>'
                    if re.search(h1_pattern, content):
                        content = re.sub(h1_pattern, f'</h1>\n{MARITIME_FORM_HUB}', content, count=1)

                # 3. Clean up broken containers (blog-content wrappers that are empty)
                content = re.sub(r'<div class="blog-content">\s*</div>', '', content)

                if content != original:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    count += 1

    print(f"Marine Blog Recovery: {count} pages restored and lead forms re-injected.")

if __name__ == "__main__":
    marine_blog_content_recovery()
