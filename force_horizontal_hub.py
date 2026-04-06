import os
import re

def force_horizontal_hub():
    # 1. FIXED Horizontal Hub Style (FORCED)
    FORCED_HUB_STYLE = """
<style>
    .elite-route-hub {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 1.5rem !important;
        overflow-x: auto !important;
        padding: 2.5rem 0 !important;
        margin: 4rem 0 !important;
        scrollbar-width: thin !important;
        -ms-overflow-style: auto !important;
        -webkit-overflow-scrolling: touch !important;
        align-items: flex-start !important;
    }
    /* Show scrollbar slightly for visual cue */
    .elite-route-hub::-webkit-scrollbar { height: 4px; background: rgba(5,5,5,0.1); }
    .elite-route-hub::-webkit-scrollbar-thumb { background: var(--primary-gold); border-radius: 4px; }
    
    .hub-column {
        flex: 0 0 300px !important; /* Forces 300px width, no shrinking */
        background: rgba(255,255,255,0.03) !important;
        border: 1px solid rgba(212,175,55,0.15) !important;
        border-radius: 15px !important;
        padding: 1.8rem !important;
        box-shadow: 0 15px 45px rgba(0,0,0,0.3) !important;
        transition: transform 0.3s ease !important;
    }
    .hub-column:hover { transform: translateY(-5px); border-color: var(--primary-gold) !important; }
    .hub-column h3 { font-size: 1.15rem !important; margin-bottom: 1.2rem !important; color: var(--primary-gold) !important; border-bottom: 1px solid rgba(212,175,55,0.2) !important; padding-bottom: 0.8rem; letter-spacing: 1.5px; }
    .hub-column ul { list-style: none !important; padding: 0 !important; margin: 0 !important; }
    .hub-column li { margin-bottom: 0.8rem !important; padding-left: 0 !important; border-bottom: 1px solid rgba(255,255,255,0.03); }
    .hub-column a { color: rgba(255,255,255,0.75) !important; text-decoration: none !important; font-size: 0.88rem !important; transition: all 0.3s; display: block; padding-bottom: 0.2rem; }
    .hub-column a:hover { color: #fff !important; transform: translateX(5px); }
</style>
"""

    count = 0
    # Walk through entire project
    for root, dirs, files in os.walk("."):
        for file in files:
            if file == "index.html":
                filepath = os.path.join(root, file)
                
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                if "elite-route-hub" in content:
                    original = content
                    
                    # Replace the style block and ensure the hub remains horizontal
                    # We look for the previous elite-route-hub block and replace it
                    content = re.sub(r'<style>\s*\.elite-route-hub.*?</style>', FORCED_HUB_STYLE, content, flags=re.DOTALL)
                    
                    if content != original:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(content)
                        count += 1

    print(f"Forced Horizontal Perfection: {count} hubs upgraded.")

if __name__ == "__main__":
    force_horizontal_hub()
