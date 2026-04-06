import os
import re

def valens_cleanup():
    # Only target the Jet corridor index files
    count = 0
    
    for root, dirs, files in os.walk('.'):
        if 'private-jet' in root:
            for file in files:
                if file == 'index.html':
                    path = os.path.join(root, file)
                    
                    try:
                        with open(path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        original = content
                        
                        # Cleanup Pattern: Target from the Valens Widget to the start of the next Section or Footer
                        # This safely purges any manual form fragments left behind
                        pattern = r'<div class="valens-widget-container".*?(<!-- (ELB_FOOTER_START|section) -->|<section)'
                        
                        if re.search(pattern, content, re.DOTALL):
                            # Replace with just the Valens Widget HTML and the anchor we found
                            valens_clean = r"""
            <div class="valens-widget-container" style="min-height: 600px; width: 100%; margin-top: 2rem;">
                <iframe src="https://valens.jetluxe.com/?AffiliateID=elbookings" 
                        width="100%" height="600" frameborder="0" 
                        style="border:none; border-radius:12px; box-shadow: 0 10px 30px rgba(0,0,0,0.2);"></iframe>
            </div>
"""
                            # Extract the anchor (footer or section)
                            match = re.search(pattern, content, re.DOTALL)
                            anchor = match.group(1)
                            
                            content = re.sub(pattern, valens_clean + "\n\n    " + anchor, content, flags=re.DOTALL)

                        if content != original:
                            with open(path, 'w', encoding='utf-8') as f:
                                f.write(content)
                            count += 1
                            
                    except Exception as e:
                        print(f"Error on {path}: {e}")

    print(f"Elite Valens Cleanup: Finalized {count} aviation gateways with zero layout fragments.")

if __name__ == "__main__":
    valens_cleanup()
