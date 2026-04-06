import os
import re

def valens_restore():
    # Elite Valens Widget HTML - Clean & Centered
    valens_widget = """
            <div class="valens-widget-container" style="min-height: 600px; width: 100%; margin-top: 2rem;">
                <iframe src="https://valens.jetluxe.com/?AffiliateID=elbookings" 
                        width="100%" height="600" frameborder="0" 
                        style="border:none; border-radius:12px; box-shadow: 0 10px 30px rgba(0,0,0,0.2);"></iframe>
            </div>
    """
    
    count = 0
    
    # Selective sync for all Private Jet-related corridors
    for root, dirs, files in os.walk('.'):
        if 'private-jet' in root:
            for file in files:
                if file == 'index.html':
                    path = os.path.join(root, file)
                    
                    try:
                        with open(path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        original = content
                        
                        # Robust Purge: Targeted the entire form-wrapper including the success panel
                        # This ensures no fragments are left behind
                        pattern = r'<div class="form-wrapper glass-panel">.*?<!-- (ELB_FOOTER_START|section) -->'
                        # If the marker isn't found, use a slightly less direct but still deep pattern
                        if not re.search(pattern, content, re.DOTALL):
                            pattern = r'<div class="form-wrapper glass-panel">.*?<section class="section-padding"'
                            
                        # Standard replacement using the section/footer as the anchor
                        if re.search(pattern, content, re.DOTALL):
                            content = re.sub(pattern, valens_widget + "\n\n    <!-- \\1 -->", content, flags=re.DOTALL)
                        else:
                            # Fallback for pages with different structures: target the form-container to success-panel block
                            secondary_pattern = r'<div class="form-wrapper glass-panel">.*?<div id="success-panel">.*?</div>\s*</div>'
                            content = re.sub(secondary_pattern, valens_widget, content, flags=re.DOTALL)

                        if content != original:
                            with open(path, 'w', encoding='utf-8') as f:
                                f.write(content)
                            count += 1
                            
                    except Exception as e:
                        print(f"Error on {path}: {e}")

    print(f"Elite Valens Restore v2: Successfully cleaned and synchronized {count} aviation gateways.")

if __name__ == "__main__":
    valens_restore()
