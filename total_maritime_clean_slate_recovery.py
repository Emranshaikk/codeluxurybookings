import os
import re

def total_maritime_clean_slate_recovery():
    count = 0
    # The Corrected Clean Content Hub Template
    def get_clean_content_hub(title):
        # SANITIZE TITLE: Remove SEO fluff like ": The Ultimate", "| Elite", etc.
        clean_name = title.split(':')[0].split('|')[0].replace("Yacht Charter", "").replace("Private Yacht", "").strip()
        return f"""
    <!-- ELB_CONTENT_HUB_START -->
    <section class="section-padding" style="background: rgba(212, 175, 55, 0.02); border-bottom: 1px solid rgba(212,175,55,0.1); padding: 4rem 0;">
        <div class="container">
            <div class="grid-2" style="display: grid; grid-template-columns: 1fr 1fr; gap: 4rem; align-items: start;">
                <div class="seo-content">
                    <h2 class="serif" style="font-size: 2.3rem; margin-bottom: 1.5rem;">Bespoke Excellence: {clean_name} Charter Guide</h2>
                    <p style="margin-bottom: 1.2rem; color: #fff; opacity: 0.9; line-height: 1.6;">Securing a <strong>Elite {clean_name} Charter</strong> is the coordination of a world-class maritime experience. Our fleet selection is curated for those who demand absolute discretion and Michelin-tier standards on the water.</p>
                    <p style="color: #fff; opacity: 0.9; line-height: 1.6;">From the Balearics to the Amalfi Coast, every itinerary is tailored to your specific requirements, ensuring your time at sea is as productive or as relaxing as you desire.</p>
                </div>
                <div class="glass-panel" style="padding: 2.5rem; background: rgba(5,5,5,0.6); border: 1px solid rgba(212,175,55,0.15); border-radius: 20px; backdrop-filter: blur(20px);">
                    <h3 class="serif gold-text" style="margin-top:0; font-size: 1.8rem; margin-bottom: 1.5rem;">Charter Standards</h3>
                    <ul class="luxury-list" style="list-style: none; padding: 0;">
                        <li style="margin-bottom: 1.2rem; padding-left: 0; position: relative;"><strong style="color:#fff;">Professional Crew:</strong> Fully vetted, multi-lingual elite maritime staff.</li>
                        <li style="margin-bottom: 1.2rem; padding-left: 0; position: relative;"><strong style="color:#fff;">Onboard Culinary:</strong> Private chefs trained in Michelin-starred environments.</li>
                        <li style="padding-left: 0; position: relative;"><strong style="color:#fff;">Worldwide Access:</strong> From hidden coves to the world's most exclusive marinas.</li>
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
                
                # 1. TOTAL AGGRESSIVE PURGE of any old "Bespoke" or "Aviation" content blocks
                content = re.sub(r'<!-- ELB_CONTENT_HUB_START -->.*?<!-- ELB_CONTENT_HUB_END -->', '', content, flags=re.DOTALL)
                content = re.sub(r'<section class="section-padding".*?Bespoke Excellence:.*?</section>', '', content, flags=re.DOTALL)
                content = re.sub(r'<section class="section-padding container">.*?Elite Itinerary Highlights.*?</section>', '', content, flags=re.DOTALL)
                content = re.sub(r'<section class="section-padding container"><div class="blog-content">.*?</div></section>', '', content, flags=re.DOTALL)

                # 2. Extract and Sanitize Title
                title_match = re.search(r'<title>(.*?) \|', content)
                if not title_match: title_match = re.search(r'<title>(.*?)</title>', content)
                page_title = title_match.group(1) if title_match else "Maritime"
                
                # 3. SINGLE CLEAN INJECTION
                if "</header>" in content:
                    content = content.replace("</header>", f"</header>\n{get_clean_content_hub(page_title)}")

                # 4. Final deduplication (Fixing the Duplicate Footer Bug)
                content = re.sub(r'(<!-- ELB_FOOTER_START -->.*?<!-- ELB_FOOTER_END -->\s*)+', r'\1', content, flags=re.DOTALL)

                if content != original:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    count += 1

    print(f"Total Maritime Clean-Slate: {count} pages restored to Pristine Elite Standard.")

if __name__ == "__main__":
    total_maritime_clean_slate_recovery()
