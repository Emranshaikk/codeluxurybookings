import os
import re

def maritime_visual_upgrade():
    # Elite Horizontal Yacht Gallery CSS
    FLEET_GALLERY_HTML = """
<style>
    .elite-fleet-gallery {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 1.5rem !important;
        overflow-x: auto !important;
        padding: 2rem 0 !important;
        margin: 3rem 0 !important;
        scrollbar-width: none;
        -ms-overflow-style: none;
    }
    .elite-fleet-gallery::-webkit-scrollbar { display: none; }
    .fleet-card {
        flex: 0 0 320px !important;
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(212,175,55,0.15);
        border-radius: 15px;
        overflow: hidden;
        transition: transform 0.4s ease;
    }
    .fleet-card:hover { transform: translateY(-5px); border-color: var(--primary-gold); }
    .fleet-img { width: 100%; height: 200px; object-fit: cover; }
    .fleet-info { padding: 1.5rem; }
    .fleet-info h4 { font-family: 'Cormorant Garamond', serif; font-size: 1.3rem; color: #fff; margin-bottom: 0.5rem; }
    .fleet-info p { color: var(--primary-gold); font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1.5px; }
</style>
<div class="elite-fleet-gallery container">
    <div class="fleet-card">
        <img src="/assets/images/defaults/yacht_master.png" class="fleet-img" alt="Superyacht Rental">
        <div class="fleet-info">
            <h4>Serenity Series</h4>
            <p>180ft+ Mega Yacht</p>
        </div>
    </div>
    <div class="fleet-card">
        <img src="https://images.pexels.com/photos/163236/luxury-yacht-boat-speed-water-163236.jpeg" class="fleet-img" alt="Motor Yacht Rental">
        <div class="fleet-info">
            <h4>Azure Collection</h4>
            <p>135ft Motor Yacht</p>
        </div>
    </div>
    <div class="fleet-card">
        <img src="/assets/images/defaults/villa_master.png" class="fleet-img" alt="Luxury Villa Transfer">
        <div class="fleet-info">
            <h4>Oceanis Heritage</h4>
            <p>Sailing Catamaran</p>
        </div>
    </div>
</div>
"""

    count = 0
    for root, dirs, files in os.walk("."):
        for file in files:
            if file == "index.html":
                filepath = os.path.join(root, file)
                if not ("yacht" in root.lower() or "boat" in root.lower() or "yacht" in file.lower()):
                    continue

                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                original = content
                
                # A. Kill generic headers and silhouettes
                content = re.sub(r'<header class="hero">.*?</header>', '<header class="hero"><div class="container"><!-- HERO_CONTENT --></header>', content, flags=re.DOTALL)
                # Cleanup duplicated sidebars
                content = re.sub(r'<div class="yacht-sidebar-affiliate".*?Explore Global Partner Fleet</p>\s*</div>', '', content, flags=re.DOTALL)

                # B. Inject Visual Gallery after Lead Form
                if "ELB_MARITIME_FORM_END" in content:
                    if "elite-fleet-gallery" not in content:
                        content = content.replace("<!-- ELB_MARITIME_FORM_END -->", f"<!-- ELB_MARITIME_FORM_END -->\n{FLEET_GALLERY_HTML}")

                if content != original:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    count += 1

    print(f"Maritime Visual Upgrade: {count} pages enhanced with Fleet Gallery.")

if __name__ == "__main__":
    maritime_visual_upgrade()
