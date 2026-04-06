import os
import re

def maritime_legacy_content_alignment():
    count = 0
    # Standardized Centered Elite Maritime Lead Hub (Formspree)
    MARITIME_CENTERED_HERO_TEMPLATE = """
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
                if not ("yacht" in root.lower() or "boat" in root.lower() or "yacht" in file.lower()):
                    continue

                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                original = content
                
                # 1. Surgical Legacy Purge
                # Remove WordPress "post-meta" / "entry-header" if they exist near the top
                content = re.sub(r'<div class="entry-meta">.*?</div>', '', content, flags=re.DOTALL)
                content = re.sub(r'<div class="blog-meta">.*?</div>', '', content, flags=re.DOTALL)
                
                # 2. Content Order Alignment
                # Ensure H1 Header -> Lead Hub -> Content
                title_match = re.search(r'<title>(.*?) \|', content)
                page_title = title_match.group(1) if title_match else "Elite Yacht Charter"
                
                # We normalize the header structure to our Elite Centered standard
                final_centered_header = f"""
    <header class="hero">
        <div class="container">
            <div class="tag-strip" style="margin-bottom: 2.5rem;">
                <span class="tag-item">Global Yacht Network</span>
                <span class="tag-item">5-Star Crewed Charters</span>
                <span class="tag-item">Confidential Coordination</span>
            </div>
            <h1 style="margin-bottom: 1rem;">{page_title}</h1>
            {MARITIME_CENTERED_HERO_TEMPLATE}
        </div>
    </header>
"""
                # Replace the entire existing hero area
                content = re.sub(r'<header class="hero">.*?</header>', final_centered_header, content, flags=re.DOTALL)
                
                # Ensure there are no duplicate H1 tags if they exist inside the content
                content = re.sub(r'<h1(?! style="margin-bottom: 1rem;").*?>.*?</h1>', '', content, flags=re.DOTALL, count=1)

                # 3. Final Content Alignment
                # Align all legacy content to a container if not already there
                if '<div class="blog-content' not in content:
                    # Wrap any loose content between hero-end and footer-start
                    content = re.sub(r'</header>(.*?)<!-- ELB_FOOTER_START -->', r'</header>\n<section class="section-padding container"><div class="blog-content">\1</div></section>\n<!-- ELB_FOOTER_START -->', content, flags=re.DOTALL)

                if content != original:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    count += 1

    print(f"Maritime Legacy Alignment Successful: {count} pages brought to the Orderly Elite Standard.")

if __name__ == "__main__":
    maritime_legacy_content_alignment()
