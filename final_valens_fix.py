import os
import re

def final_valens_fix():
    count = 0
    
    # Correct Structural HTML for the Hero Section integration
    valens_integration = """
            <div class="valens-widget-container" style="min-height: 600px; width: 100%; margin-top: 2rem;">
                <iframe src="https://valens.jetluxe.com/?AffiliateID=elbookings" 
                        width="100%" height="600" frameborder="0" 
                        style="border:none; border-radius:12px; box-shadow: 0 10px 30px rgba(0,0,0,0.2);"></iframe>
            </div>
        </div>
    </header>
"""

    for root, dirs, files in os.walk('.'):
        if 'private-jet' in root:
            for file in files:
                if file == 'index.html':
                    path = os.path.join(root, file)
                    
                    try:
                        with open(path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        original = content
                        
                        # Phase 1: Fix High-Level Structure (Hero Container)
                        # Target from the Valens Widget to the start of the next Section
                        struct_pattern = r'<div class="valens-widget-container".*?<section'
                        if re.search(struct_pattern, content, re.DOTALL):
                            content = re.sub(struct_pattern, valens_integration + "\n\n    <section", content, flags=re.DOTALL)
                        
                        # Phase 2: Purge Legacy Form Script
                        # Target the script block that starts with tripForm listener
                        script_pattern = r'<script>\s*document\.getElementById\(\'tripForm\'\).*?</script>'
                        content = re.sub(script_pattern, '', content, flags=re.DOTALL)
                        
                        # Phase 3: Cleanup potential double footer starts
                        content = re.sub(r'<!-- ELB_FOOTER_START -->\s*<!-- ELB_FOOTER_START -->', '<!-- ELB_FOOTER_START -->', content)

                        if content != original:
                            with open(path, 'w', encoding='utf-8') as f:
                                f.write(content)
                            count += 1
                            
                    except Exception as e:
                        print(f"Error on {path}: {e}")

    print(f"Elite Structural Fix: Restored and decontaminated {count} aviation hubs.")

if __name__ == "__main__":
    final_valens_fix()
