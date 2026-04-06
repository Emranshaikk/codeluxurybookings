import os
import re

def update_success_logic():
    # Targeted text to provide reassurance and ensure tracking
    new_msg_text = "Thank you for reaching out. Our elite concierge team will get back to you in few hours."
    
    count = 0
    
    # 2. Targeted replacement logic for success panels
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.html'):
                path = os.path.join(root, file)
                
                # Skip known libraries/assets
                if any(x in root for x in ['assets', 'node_modules', '.git']):
                    continue
                
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    original = content
                    
                    # Target 1: The Home/Aviation Hub success text
                    # "A dedicated broker is evaluating active global routing. You may initiate a rapid secure connection via WhatsApp now."
                    pattern1 = r'evaluating active global (properties|routing).*?now\.'
                    content = re.sub(pattern1, new_msg_text, content)

                    # Target 2: The Route corridor success text
                    # "Our aviation brokers are evaluating active global routing for your mission."
                    pattern2 = r'Our aviation brokers are evaluating.*?mission\.'
                    content = re.sub(pattern2, new_msg_text, content)

                    # Target 3: The Contact page success text
                    # "A senior broker will evaluate your mission and reach out via your preferred channel."
                    pattern3 = r'A senior broker will evaluate your mission and reach out via your preferred channel\.'
                    content = re.sub(pattern3, new_msg_text, content)

                    # Target 4: Yacht Hub / Hero Mini forms
                    # "Your request is being prioritized. A concierge is now reviewing your requirements."
                    pattern4 = r'Your request is being prioritized\. A concierge is now reviewing your requirements\.'
                    content = re.sub(pattern4, new_msg_text, content)

                    if content != original:
                        with open(path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        count += 1
                        
                except Exception as e:
                    print(f"Error on {path}: {e}")

    print(f"Elite Reassurance Lock: Standardized {count} success messages site-wide.")

if __name__ == "__main__":
    update_success_logic()
