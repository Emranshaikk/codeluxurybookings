import os
import re

def perfect_aviation_silo():
    # 1. CSS for the Horizontal Hub
    HORIZONTAL_HUB_STYLE = """
<style>
    .elite-route-hub {
        display: flex;
        gap: 1.5rem;
        overflow-x: auto;
        padding: 2rem 0;
        margin: 3rem 0;
        scrollbar-width: none;
        -ms-overflow-style: none;
    }
    .elite-route-hub::-webkit-scrollbar { display: none; }
    .hub-column {
        min-width: 280px;
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(212,175,55,0.1);
        border-radius: 15px;
        padding: 1.5rem;
        backdrop-filter: blur(10px);
    }
    .hub-column h3 { font-size: 1.1rem !important; margin-bottom: 1rem !important; color: var(--primary-gold) !important; border-bottom: 1px solid rgba(212,175,55,0.1); padding-bottom: 0.5rem; }
    .hub-column ul { list-style: none; padding: 0; margin: 0; }
    .hub-column li { margin-bottom: 0.5rem; }
    .hub-column a { color: rgba(255,255,255,0.6); text-decoration: none; font-size: 0.85rem; transition: color 0.3s; }
    .hub-column a:hover { color: var(--primary-gold); }
</style>
"""

    count = 0
    # Walk through entire project
    for root, dirs, files in os.walk("."):
        for file in files:
            if file == "index.html":
                filepath = os.path.join(root, file)
                
                # We target pages that contain the Valens Jet Engine
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                if "ELB_VALENS_API_ENGINE_START" in content:
                    original = content
                    
                    # A. REMOVE YACHT WIDGET
                    content = re.sub(r'<!-- ELB_YACHTING_WIDGET_START -->.*?<!-- ELB_YACHTING_WIDGET_END -->', '', content, flags=re.DOTALL)
                    content = re.sub(r'<!-- ELB_YACHTING_AFFILIATE_WIDGET_START -->.*?<!-- ELB_YACHTING_AFFILIATE_WIDGET_END -->', '', content, flags=re.DOTALL)
                    content = re.sub(r'<aside class="blog-sidebar">.*?</aside>', '', content, flags=re.DOTALL)

                    # B. EXTRACT VALENS ENGINE 
                    engine_match = re.search(r'<!-- ELB_VALENS_API_ENGINE_START -->.*?<!-- ELB_VALENS_API_ENGINE_END -->', content, flags=re.DOTALL)
                    if engine_match:
                        engine_html = engine_match.group(0)
                        # Remove it from current position
                        content = content.replace(engine_html, "")
                        
                        # Move it to TOP (Right after H1)
                        # Find H1
                        content = re.sub(r'(<h1.*?>.*?</h1>)', f'\\1\n\n{engine_html}', content, flags=re.DOTALL, count=1)

                    # C. FIX FLIGHT HUB (HORIZONTAL & SINGLE)
                    # We look for the "Americas Hub" etc blocks and consolidate them
                    # Or just kill all existing silo blocks and inject a fresh horizontal one
                    content = re.sub(r'<!-- SINGLE SILO -->.*?</section>', '<!-- SINGLE_SILO_HUB_PLACEHOLDER -->', content, flags=re.DOTALL)
                    # Remove duplicates if any
                    content = re.sub(r'<!-- SINGLE_SILO_HUB_PLACEHOLDER -->.*<!-- SINGLE_SILO_HUB_PLACEHOLDER -->', '<!-- SINGLE_SILO_HUB_PLACEHOLDER -->', content, flags=re.DOTALL)

                    hub_html = f"""
{HORIZONTAL_HUB_STYLE}
<div class="elite-route-hub container">
    <div class="hub-column">
        <h3>Americas Corridors</h3>
        <ul>
            <li><a href="/newyork-to-miami-private-jet-cost/">New York to Miami</a></li>
            <li><a href="/losangeles-to-lasvegas-private-jet-cost/">LAX to Las Vegas</a></li>
            <li><a href="/chicago-to-miami-private-jet-cost/">Chicago to Miami</a></li>
            <li><a href="/miami-to-turksandcaicos-private-jet-cost/">Miami to Turks & Caicos</a></li>
        </ul>
    </div>
    <div class="hub-column">
        <h3>European Routes</h3>
        <ul>
            <li><a href="/london-to-nice-private-jet-cost/">London to Nice</a></li>
            <li><a href="/paris-to-dubai-private-jet-cost/">Paris to Dubai</a></li>
            <li><a href="/london-to-ibiza-private-jet-cost/">London to Ibiza</a></li>
            <li><a href="/geneva-to-london-private-jet-cost/">Geneva to London</a></li>
        </ul>
    </div>
    <div class="hub-column">
        <h3>Asia & Pacific</h3>
        <ul>
            <li><a href="/singapore-to-sydney-private-jet-cost/">Singapore to Sydney</a></li>
            <li><a href="/tokyo-to-london-private-jet-cost/">Tokyo to London</a></li>
            <li><a href="/sydney-to-perth-private-jet-cost/">Sydney to Perth</a></li>
            <li><a href="/bali-to-melbourne-private-jet-cost/">Bali to Melbourne</a></li>
        </ul>
    </div>
    <div class="hub-column">
        <h3>Middle East Hub</h3>
        <ul>
            <li><a href="/riyadh-to-maldives-private-jet-cost/">Riyadh to Maldives</a></li>
            <li><a href="/abudhabi-to-doha-private-jet-cost/">Abu Dhabi to Doha</a></li>
            <li><a href="/dubai-to-london-private-jet-cost/">Dubai to London</a></li>
            <li><a href="/sydney-to-dubai-private-jet-cost/">Sydney to Dubai</a></li>
        </ul>
    </div>
</div>
"""
                    content = content.replace('<!-- SINGLE_SILO_HUB_PLACEHOLDER -->', hub_html)

                    # D. FOOTER UNIFICATION
                    # Ensure only one footer remains. We find all ELB_FOOTER_START blocks and keep only the last one? 
                    # Actually, we can just deduplicate the entire file based on the footer tag.
                    if content.count('<!-- ELB_FOOTER_START -->') > 1:
                        # Keep the last one, remove the others
                        parts = content.split('<!-- ELB_FOOTER_START -->')
                        content = "<!-- ELB_FOOTER_START -->".join(parts[:-1]) + "<!-- ELB_FOOTER_START -->" + parts[-1]
                        # This isn't quite right for multiple, let's keep it simple: find and replace repeated blocks.
                        content = re.sub(r'(<!-- ELB_FOOTER_START -->.*?<!-- ELB_FOOTER_END -->\s*)+', r'\1', content, flags=re.DOTALL)

                    if content != original:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(content)
                        count += 1

    print(f"Aviation Silo Master: {count} pages perfected.")

if __name__ == "__main__":
    perfect_aviation_silo()
