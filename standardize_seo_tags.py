import os
import re

def standardize_seo():
    count = 0
    for root, dirs, files in os.walk('.'):
        if 'index.html' in files:
            # Focus only on the 111+ route pages
            if '-to-' in root and 'private-jet-cost' in root:
                path = os.path.join(root, 'index.html')
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    original = content
                    
                    # Extract city pair from previous fix (the capitalized H1)
                    h1_match = re.search(r'class="gold-text">([^<]+)</span>', content)
                    cities = ""
                    if h1_match:
                        cities = h1_match.group(1).strip()
                    
                    if not cities:
                        continue
                        
                    # Standardized CTR-Optimized Tags
                    new_title = f"Private Jet Charter: {cities} Cost (Bookings + Pricing)"
                    new_desc = f"Secure the elite private jet cost for the {cities} corridor. VIP terminal access and bespoke 24/7 coordination. Book your {cities} charter instantly."
                    
                    # Replacement for Title
                    content = re.sub(r'<title>.*?</title>', f'<title>{new_title}</title>', content)
                    # Replacement for Meta Description
                    content = re.sub(r'<meta name="description" content=".*?">', f'<meta name="description" content="{new_desc}">', content)
                    
                    if content != original:
                        with open(path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        count += 1
                except Exception as e:
                    print(f"Error: {e}")

    print(f"Successfully optimized SEO Meta Tags for {count} route pages.")

if __name__ == "__main__":
    standardize_seo()
