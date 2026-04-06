import os

def nurture_form_sync():
    # Targets for the Lead Nurture funnel
    new_endpoint = "https://formspree.io/f/xwvwanlj"
    old_endpoint_partial = "AKfycbxwH6b82MCg90tYS-yTwUMWw1ePx2S3oBdn3BC5U1UAt2uQRCB2bq03bzPP52ygUGU6UA/exec"
    
    count = 0
    
    # Selective sync: ONLY targeted nurture hubs
    hubs_to_update = [
        'index.html',                              # Home Page
        'contact/index.html',                      # Contact Hub
        'luxury-villa-rentals/index.html',         # Villa Hub
        'luxury-yacht-rentals/index.html'          # Yacht Hub
    ]
    
    # Search for all index files but explicitly exclude Private Jet directories
    for root, dirs, files in os.walk('.'):
        # EXCLUSION RULE: Skip everything related to Private Jets
        if 'private-jet' in root or 'elite-private-jet-charter' in root:
            continue
            
        for file in files:
            if file == 'index.html':
                path = os.path.join(root, file)
                
                # Further double-check to ensure we are only in Nurture hubs
                # Or any blog post that isn't jet related
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    original = content
                    
                    # Update to Formspree endpoint if it has the manual script
                    if old_endpoint_partial in content:
                        # Find the full endpoint string and replace it
                        # The full URL starts with https://script.google.com... and ends with /exec
                        start = content.find("https://script.google.com")
                        end = content.find("/exec", start) + 5
                        if start != -1 and end != -1:
                            target_url = content[start:end]
                            content = content.replace(target_url, new_endpoint)
                    
                    if content != original:
                        with open(path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        count += 1
                        
                except Exception as e:
                    print(f"Error on {path}: {e}")

    print(f"Elite Selective Sync: Standardized {count} lead capture points site-wide (Excluding Jet Funnel).")

if __name__ == "__main__":
    nurture_form_sync()
