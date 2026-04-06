import os
import re

def vip_urgency_sync():
    # Elite message for Priority (Jet) clients
    vip_msg_text = "Thank you for reaching out. A private concierge will connect with you in 30 minutes."
    
    count = 0
    
    # Target folders that are specifically Jet-related
    jet_identifiers = ['-private-jet', 'elite-private-jet-charter']
    
    for root, dirs, files in os.walk('.'):
        # Determine if this file is in a Jet-intent directory
        is_jet_page = any(ident in root for ident in jet_identifiers)
        
        for file in files:
            if file == 'index.html':
                path = os.path.join(root, file)
                
                # Double-check: must be a Jet page AND have the "few hours" message I just added
                if not is_jet_page:
                    continue
                
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    original = content
                    
                    # Target the message I just standardized in the previous step
                    legacy_text = "Thank you for reaching out. Our elite concierge team will get back to you in few hours."
                    
                    if legacy_text in content:
                        content = content.replace(legacy_text, vip_msg_text)
                    
                    if content != original:
                        with open(path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        count += 1
                        
                except Exception as e:
                    print(f"Error on {path}: {e}")

    print(f"Elite VIP Urgency Lock: Synchronized {count} high-intent lead confirmation points to 30-minute priority.")

if __name__ == "__main__":
    vip_urgency_sync()
