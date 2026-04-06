import os
import re

def personalize_whatsapp():
    count = 0
    # Walk through all directories
    for root, dirs, files in os.walk('.'):
        if 'index.html' in files:
            # We only want route pages like *-to-*-private-jet-cost
            if '-to-' in root and 'private-jet-cost' in root:
                path = os.path.join(root, 'index.html')
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    original = content
                    
                    # 1. Find the city pair from the H1 or title
                    # H1 example: Private Jet Charter <span class="gold-text">New York to Toronto</span>
                    # Title example: Private Jet cost (Bookings + New York to Toronto Flight Cost Breakdown)
                    
                    # We'll use the H1 pattern first
                    h1_match = re.search(r'class="gold-text">([^<]+)</span>', content)
                    cities = ""
                    if h1_match:
                        cities = h1_match.group(1).strip()
                    else:
                        # Fallback to title
                        title_match = re.search(r'\+ ([^)]+)', content)
                        if title_match:
                            cities = title_match.group(1).strip().replace(" Flight Cost Breakdown", "")
                    
                    if not cities:
                        continue
                        
                    # 2. Update the WhatsApp message in the script
                    # Previous template might vary, we standardize it.
                    message_template = f"Hello Elite Concierge, I have just requested a private jet proposal for {cities}. My Reference ID is ${{ref}}."
                    
                    # Find the specific line that sets waMsg or similar
                    # Pattern matching the waMsg line from previous versions
                    wa_pattern = r'const waMsg = encodeURIComponent\(`Hello Elite Concierge, I have just requested a private jet proposal for [^.]+\. My Reference ID is \$\{ref\}\.`\);'
                    new_wa_line = f"const waMsg = encodeURIComponent(`{message_template}`);"
                    
                    if re.search(wa_pattern, content):
                        content = re.sub(wa_pattern, new_wa_line, content)
                    else:
                        # If not found exactly, try a more lenient match for the waMsg line
                        wa_lenient = r'const waMsg = encodeURIComponent\(`[^`]+`\);'
                        content = re.sub(wa_lenient, new_wa_line, content)
                    
                    if content != original:
                        with open(path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        count += 1
                except Exception as e:
                    print(f"Error processing {path}: {e}")
                    
    print(f"Successfully personalized WhatsApp lead messages for {count} route pages.")

if __name__ == "__main__":
    personalize_whatsapp()
