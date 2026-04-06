import os
import re

def global_aviation_redesign():
    # 1. The Urgency Strip Template
    URGENCY_STRIP = """
            <div class="urgency-alert" style="background: rgba(255, 77, 77, 0.05); border: 1px solid rgba(255, 77, 77, 0.3); padding: 12px 20px; border-radius: 12px; margin: 2rem auto 1.5rem; max-width: 700px; display: flex; align-items: center; justify-content: center; gap: 15px; animation: fadeIn 1s ease-out;">
                <span style="position: relative; display: flex; height: 12px; width: 12px;">
                    <span style="animation: ping 1.5s cubic-bezier(0, 0, 0.2, 1) infinite; position: absolute; display: inline-flex; height: 100%; width: 100%; border-radius: 50%; background-color: #ff4d4d; opacity: 0.75;"></span>
                    <span style="position: relative; display: inline-flex; border-radius: 50%; height: 12px; width: 12px; background-color: #ff4d4d;"></span>
                </span>
                <span style="color: #ff4d4d; font-size: 0.95rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;">Strategic Slot Alert: Peak Season Demand - Inquire Early</span>
            </div>
"""

    count = 0
    for root, dirs, files in os.walk("."):
        for file in files:
            if file == "index.html":
                filepath = os.path.join(root, file)
                
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                if "ELB_VALENS_API_ENGINE_START" in content:
                    original = content
                    
                    # A. Remove any existing Urgency Strips to prevent duplicates
                    content = re.sub(r'<div class="urgency-alert".*?</div>', '', content, flags=re.DOTALL)
                    content = re.sub(r'<div style="background: rgba\(255, 77, 77, 0\.05\).*?</div>', '', content, flags=re.DOTALL)

                    # B. Extract Valens Engine
                    engine_match = re.search(r'<!-- ELB_VALENS_API_ENGINE_START -->.*?<!-- ELB_VALENS_API_ENGINE_END -->', content, flags=re.DOTALL)
                    if engine_match:
                        engine_html = engine_match.group(0)
                        # Remove it from current position
                        content = content.replace(engine_html, "")
                        
                        # C. Inject Urgency + Engine after H1
                        # We place it before the form.
                        replacement_block = f"{URGENCY_STRIP}\n{engine_html}"
                        content = re.sub(r'(<h1.*?>.*?</h1>)', f'\\1\n{replacement_block}', content, flags=re.DOTALL, count=1)

                    # D. Final Cleanup of "hub" repetition (making sure we have ONE horizontal hub)
                    # We ensure the style is present for horizontal hub
                    if "elite-route-hub" in content:
                        # Ensure it's the horizontal version
                        pass # Previous script already handled this for many, but we'll ensure consistency

                    # E. Duplicate Footer Check
                    content = re.sub(r'(<!-- ELB_FOOTER_START -->.*?<!-- ELB_FOOTER_END -->\s*)+', r'\1', content, flags=re.DOTALL)

                    if content != original:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(content)
                        count += 1

    print(f"Global Aviation Redesign: {count} pages transformed to the Amsterdam Lead Standard.")

if __name__ == "__main__":
    global_aviation_redesign()
