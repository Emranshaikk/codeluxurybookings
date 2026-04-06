import os
import re

def global_maritime_content_perfection():
    count = 0
    # The Final Elite Content Hub Template (Mirrored from User's Screenshot)
    def get_content_hub(title):
        clean_title = title.replace("Yacht Charter", "").replace("|", "").strip()
        return f"""
    <!-- ELB_CONTENT_HUB_START -->
    <section class="section-padding" style="background: rgba(212, 175, 55, 0.02); border-bottom: 1px solid var(--glass-border); padding: 5rem 0;">
        <div class="container">
            <div class="grid-2" style="display: grid; grid-template-columns: 1fr 1fr; gap: 4rem; align-items: start;">
                <div class="seo-content">
                    <h2 class="serif" style="font-size: 2.5rem; margin-bottom: 2rem;">Bespoke Excellence: {clean_title} Charter Guide</h2>
                    <p style="margin-bottom: 1.5rem; color: #fff; opacity: 0.9;">Securing a <strong>{clean_title} Yacht Charter</strong> is more than a transaction; it is the coordination of a world-class maritime experience. Our fleet selection is curated for those who demand absolute discretion and Michelin-tier standards on the water.</p>
                    <p style="color: #fff; opacity: 0.9;">From the Balearics to the Amalfi Coast, every itinerary is tailored to your specific requirements, ensuring your time at sea is as productive or as relaxing as you desire.</p>
                </div>
                <div class="glass-panel" style="padding: 3rem; background: rgba(5,5,5,0.6); border: 1px solid rgba(212,175,55,0.15); border-radius: 20px; backdrop-filter: blur(20px);">
                    <h3 class="serif gold-text" style="margin-top:0; font-size: 2rem; margin-bottom: 2rem;">Charter Standards</h3>
                    <ul class="luxury-list" style="list-style: none; padding: 0;">
                        <li style="margin-bottom: 1.5rem; padding-left: 2.5rem; position: relative;"><strong style="color:#fff;">Professional Crew:</strong> Fully vetted, multi-lingual elite maritime staff.</li>
                        <li style="margin-bottom: 1.5rem; padding-left: 2.5rem; position: relative;"><strong style="color:#fff;">Onboard Culinary:</strong> Private chefs trained in Michelin-starred environments.</li>
                        <li style="padding-left: 2.5rem; position: relative;"><strong style="color:#fff;">Worldwide Access:</strong> From hidden coves to the world's most exclusive marinas.</li>
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
                if not ("yacht" in root.lower() or "boat" in root.lower() or "yacht" in file.lower() or "luxury-yacht" in root.lower()):
                    continue

                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                original = content
                
                # 1. Deduplicate/Remove old content segments
                content = re.sub(r'<!-- ELB_CONTENT_HUB_START -->.*?<!-- ELB_CONTENT_HUB_END -->', '', content, flags=re.DOTALL)
                content = re.sub(r'<section class="section-padding".*?class="seo-content".*?</section>', '', content, flags=re.DOTALL)
                
                # 2. Extract Title & Rebuild Content Hub
                title_match = re.search(r'<title>(.*?) \|', content)
                page_title = title_match.group(1) if title_match else "Elite Yacht Charter"
                
                # 3. Inject below Hero
                if "</header>" in content:
                    content = content.replace("</header>", f"</header>\n{get_content_hub(page_title)}")

                # 4. Final Spacing & Sanitization
                content = re.sub(r'(<!-- ELB_FOOTER_START -->.*?<!-- ELB_FOOTER_END -->\s*)+', r'\1', content, flags=re.DOTALL)

                if content != original:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    count += 1

    print(f"Global Maritime Content Perfection: {count} pages brought to Elite Bespoke Standard.")

if __name__ == "__main__":
    global_maritime_content_perfection()
