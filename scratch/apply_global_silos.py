import os
import re

YACHT_SILO = """
    <!-- YACHTING AUTHORITY SILO -->
    <div style="max-width: 1200px; margin: 2rem auto 0; padding: 2rem 0 0; border-top: 1px solid rgba(212,175,55,0.1); text-align: center;">
        <h4 class="serif gold-text" style="font-size: 1.4rem; margin-bottom: 1.5rem; letter-spacing: 2px;">Yachting Authority Silo</h4>
        <div style="display: flex; justify-content: center; gap: 1.5rem; flex-wrap: wrap; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px;">
            <a href="https://eliteluxurybookings.com/motor-yacht-vs-sailing-yacht-charter/" style="color: rgba(255,255,255,0.6); text-decoration: none; transition: 0.3s;" onmouseover="this.style.color='#D4AF37'" onmouseout="this.style.color='rgba(255,255,255,0.6)'">Motor vs Sailing</a>
            <a href="https://eliteluxurybookings.com/cost-to-charter-superyacht-2026/" style="color: rgba(255,255,255,0.6); text-decoration: none; transition: 0.3s;" onmouseover="this.style.color='#D4AF37'" onmouseout="this.style.color='rgba(255,255,255,0.6)'">Charter Costs</a>
            <a href="https://eliteluxurybookings.com/best-mediterranean-yacht-destinations/" style="color: rgba(255,255,255,0.6); text-decoration: none; transition: 0.3s;" onmouseover="this.style.color='#D4AF37'" onmouseout="this.style.color='rgba(255,255,255,0.6)'">Mediterranean Guide</a>
            <a href="https://eliteluxurybookings.com/yacht-charter-apa-guide/" style="color: rgba(255,255,255,0.6); text-decoration: none; transition: 0.3s;" onmouseover="this.style.color='#D4AF37'" onmouseout="this.style.color='rgba(255,255,255,0.6)'">APA Guide</a>
            <a href="https://eliteluxurybookings.com/how-to-rent-superyacht-guide/" style="color: rgba(255,255,255,0.6); text-decoration: none; transition: 0.3s;" onmouseover="this.style.color='#D4AF37'" onmouseout="this.style.color='rgba(255,255,255,0.6)'">Booking Guide</a>
        </div>
    </div>
    <!-- END YACHTING AUTHORITY SILO -->
"""

AVIATION_SILO = """
    <!-- AVIATION AUTHORITY SILO -->
    <div style="max-width: 1200px; margin: 2rem auto 0; padding: 2rem 0 0; border-top: 1px solid rgba(212,175,55,0.1); text-align: center;">
        <h4 class="serif gold-text" style="font-size: 1.4rem; margin-bottom: 1.5rem; letter-spacing: 2px;">Aviation Authority Silo</h4>
        <div style="display: flex; justify-content: center; gap: 1.5rem; flex-wrap: wrap; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px;">
            <a href="https://eliteluxurybookings.com/private-jet-charter-cost-estimator/" style="color: rgba(255,255,255,0.6); text-decoration: none; transition: 0.3s;" onmouseover="this.style.color='#D4AF37'" onmouseout="this.style.color='rgba(255,255,255,0.6)'">Jet Cost Estimator</a>
            <a href="https://eliteluxurybookings.com/heavy-jet-vs-light-jet-charter/" style="color: rgba(255,255,255,0.6); text-decoration: none; transition: 0.3s;" onmouseover="this.style.color='#D4AF37'" onmouseout="this.style.color='rgba(255,255,255,0.6)'">Jet Class Analysis</a>
            <a href="https://eliteluxurybookings.com/empty-leg-flights-guide/" style="color: rgba(255,255,255,0.6); text-decoration: none; transition: 0.3s;" onmouseover="this.style.color='#D4AF37'" onmouseout="this.style.color='rgba(255,255,255,0.6)'">Empty Leg Mastery</a>
            <a href="https://eliteluxurybookings.com/elite-private-jet-charter/" style="color: rgba(255,255,255,0.6); text-decoration: none; transition: 0.3s;" onmouseover="this.style.color='#D4AF37'" onmouseout="this.style.color='rgba(255,255,255,0.6)'">View Global Fleet</a>
        </div>
    </div>
    <!-- END AVIATION AUTHORITY SILO -->
"""

VILLA_SILO = """
    <!-- VILLA AUTHORITY SILO -->
    <div style="max-width: 1200px; margin: 2rem auto 0; padding: 2rem 0 0; border-top: 1px solid rgba(212,175,55,0.1); text-align: center;">
        <h4 class="serif gold-text" style="font-size: 1.4rem; margin-bottom: 1.5rem; letter-spacing: 2px;">Villa Authority Silo</h4>
        <div style="display: flex; justify-content: center; gap: 1.5rem; flex-wrap: wrap; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px;">
            <a href="https://eliteluxurybookings.com/ultimate-luxury-villa-rental-guide-2026/" style="color: rgba(255,255,255,0.6); text-decoration: none; transition: 0.3s;" onmouseover="this.style.color='#D4AF37'" onmouseout="this.style.color='rgba(255,255,255,0.6)'">Villa Guide 2026</a>
            <a href="https://eliteluxurybookings.com/villa-vs-luxury-hotel-comparison/" style="color: rgba(255,255,255,0.6); text-decoration: none; transition: 0.3s;" onmouseover="this.style.color='#D4AF37'" onmouseout="this.style.color='rgba(255,255,255,0.6)'">Villa vs Hotel</a>
            <a href="https://eliteluxurybookings.com/how-to-book-luxury-villa-guide/" style="color: rgba(255,255,255,0.6); text-decoration: none; transition: 0.3s;" onmouseover="this.style.color='#D4AF37'" onmouseout="this.style.color='rgba(255,255,255,0.6)'">Booking Protocol</a>
            <a href="https://eliteluxurybookings.com/private-island-honeymoon-rental/" style="color: rgba(255,255,255,0.6); text-decoration: none; transition: 0.3s;" onmouseover="this.style.color='#D4AF37'" onmouseout="this.style.color='rgba(255,255,255,0.6)'">Honeymoon Rentals</a>
            <a href="https://eliteluxurybookings.com/luxury-villa-rentals/" style="color: rgba(255,255,255,0.6); text-decoration: none; transition: 0.3s;" onmouseover="this.style.color='#D4AF37'" onmouseout="this.style.color='rgba(255,255,255,0.6)'">View Portfolio</a>
        </div>
    </div>
    <!-- END VILLA AUTHORITY SILO -->
"""

EXCLUDE_FILES = {'404.html', 'thank-you.html', 'test_bot.html'}

def classify_page(filename, content):
    filename_lower = filename.lower()
    
    if filename_lower in EXCLUDE_FILES or 'blog' in filename_lower:
        return 'Brand'
    if filename_lower.startswith('_'):
        return 'Brand'
        
    # Check by keywords in filename
    if any(x in filename_lower for x in ['yacht', 'boat', 'sailing', 'catamaran', 'bareboat', 'sunreef', 'mallorca', 'formentera']):
        return 'Yacht'
    if any(x in filename_lower for x in ['jet', 'aviation', 'flight', 'route', 'airport', 'flying', 'heavy-jet', 'empty-leg']):
        return 'Aviation'
    if any(x in filename_lower for x in ['villa', 'island', 'honeymoon']):
        return 'Villa'
        
    # Check by content keywords if filename is ambiguous
    content_lower = content.lower()
    if 'yacht' in content_lower or 'catamaran' in content_lower:
        return 'Yacht'
    if 'private jet' in content_lower or 'aircraft' in content_lower:
        return 'Aviation'
    if 'villa' in content_lower or 'island rental' in content_lower:
        return 'Villa'
        
    return 'Brand'

def process_files():
    root_dir = r"c:\Users\imran\OneDrive\Desktop\ELB code"
    files = [f for f in os.listdir(root_dir) if f.endswith('.html')]
    
    updated_count = 0
    skipped_count = 0
    
    print(f"Auditing and applying silos to {len(files)} files...")
    
    for filename in files:
        filepath = os.path.join(root_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        category = classify_page(filename, content)
        
        # Clean up any existing silo blocks (both old style and new style)
        # 1. Clean up new style block (with explicit END comment)
        content = re.sub(r'<!-- YACHTING AUTHORITY SILO -->.*?<!-- END YACHTING AUTHORITY SILO -->', '', content, flags=re.DOTALL)
        content = re.sub(r'<!-- AVIATION AUTHORITY SILO -->.*?<!-- END AVIATION AUTHORITY SILO -->', '', content, flags=re.DOTALL)
        content = re.sub(r'<!-- VILLA AUTHORITY SILO -->.*?<!-- END VILLA AUTHORITY SILO -->', '', content, flags=re.DOTALL)
        
        # 2. Clean up old style blocks (without explicit END comment, matching the footer injection format)
        content = re.sub(r'<!-- YACHTING AUTHORITY SILO -->.*?<!-- ELB_FOOTER_END -->', '', content, flags=re.DOTALL)
        content = re.sub(r'<!-- AVIATION AUTHORITY SILO -->.*?<!-- ELB_FOOTER_END -->', '', content, flags=re.DOTALL)
        content = re.sub(r'<!-- VILLA AUTHORITY SILO -->.*?<!-- ELB_FOOTER_END -->', '', content, flags=re.DOTALL)
        
        # 3. Clean up legacy Elite Intelligence widgets
        content = re.sub(r'<!-- ELITE YACHTING INTELLIGENCE -->.*?</div>\s*</div>', '', content, flags=re.DOTALL)
        content = re.sub(r'<!-- ELITE VILLA INTELLIGENCE -->.*?</div>\s*</div>', '', content, flags=re.DOTALL)
        content = re.sub(r'<!-- ELITE AVIATION INTELLIGENCE -->.*?</div>\s*</div>', '', content, flags=re.DOTALL)
        
        # Also clean up stray comments
        content = content.replace('<!-- ELB_FOOTER_END -->', '')
        
        silo_block = ""
        if category == 'Yacht':
            silo_block = YACHT_SILO
        elif category == 'Aviation':
            silo_block = AVIATION_SILO
        elif category == 'Villa':
            silo_block = VILLA_SILO
            
        if silo_block:
            # Locate <div class="footer-bottom"> inside the footer
            # We want to insert the silo right before it
            if '<div class="footer-bottom">' in content:
                content = content.replace('<div class="footer-bottom">', silo_block.strip() + '\n            <div class="footer-bottom">', 1)
                updated_count += 1
            else:
                # If footer-bottom is not found, try placing it before </footer>
                if '</footer>' in content:
                    content = content.replace('</footer>', silo_block.strip() + '\n    </footer>', 1)
                    updated_count += 1
                else:
                    print(f"  [WARN] Could not find footer in: {filename}")
                    skipped_count += 1
        else:
            skipped_count += 1
            
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
            
    print(f"Completed! Injected silos into {updated_count} files. {skipped_count} files left clean/silo-free.")

if __name__ == "__main__":
    process_files()
