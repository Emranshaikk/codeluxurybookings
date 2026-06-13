import os
import re

# Define the Villa Authority Silo HTML block
VILLA_SILO_BLOCK = """
    <!-- VILLA AUTHORITY SILO -->
    <div style="max-width: 1200px; margin: 3rem auto 0; padding: 2rem; border-top: 1px solid rgba(212,175,55,0.1); text-align: center;">
        <h4 class="serif gold-text" style="font-size: 1.4rem; margin-bottom: 1.5rem; letter-spacing: 2px;">Villa Authority Silo</h4>
        <div style="display: flex; justify-content: center; gap: 1.5rem; flex-wrap: wrap; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px;">
            <a href="https://eliteluxurybookings.com/ultimate-luxury-villa-rental-guide/" style="color: rgba(255,255,255,0.6); text-decoration: none; transition: 0.3s;" onmouseover="this.style.color='#D4AF37'" onmouseout="this.style.color='rgba(255,255,255,0.6)'">Villa Guide 2026</a>
            <a href="https://eliteluxurybookings.com/villa-vs-luxury-hotel-comparison/" style="color: rgba(255,255,255,0.6); text-decoration: none; transition: 0.3s;" onmouseover="this.style.color='#D4AF37'" onmouseout="this.style.color='rgba(255,255,255,0.6)'">Villa vs Hotel</a>
            <a href="https://eliteluxurybookings.com/how-to-book-luxury-villa-guide/" style="color: rgba(255,255,255,0.6); text-decoration: none; transition: 0.3s;" onmouseover="this.style.color='#D4AF37'" onmouseout="this.style.color='rgba(255,255,255,0.6)'">Booking Protocol</a>
            <a href="https://eliteluxurybookings.com/private-island-honeymoon-rental/" style="color: rgba(255,255,255,0.6); text-decoration: none; transition: 0.3s;" onmouseover="this.style.color='#D4AF37'" onmouseout="this.style.color='rgba(255,255,255,0.6)'">Honeymoon Rentals</a>
            <a href="https://eliteluxurybookings.com/luxury-villa-rentals/" style="color: rgba(255,255,255,0.6); text-decoration: none; transition: 0.3s;" onmouseover="this.style.color='#D4AF37'" onmouseout="this.style.color='rgba(255,255,255,0.6)'">View Portfolio</a>
        </div>
    </div>
    <!-- ELB_FOOTER_END -->
"""

def inject_silo(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".html"):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # If already has villa silo, skip
            if "VILLA AUTHORITY SILO" in content:
                continue
                
            # Replace ELB_FOOTER_END with Silo + ELB_FOOTER_END
            if "<!-- ELB_FOOTER_END -->" in content:
                new_content = content.replace("<!-- ELB_FOOTER_END -->", VILLA_SILO_BLOCK)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Injected Villa Silo into {filename}")

if __name__ == "__main__":
    target_dir = r"c:\Users\imran\OneDrive\Desktop\ELB code"
    inject_silo(target_dir)
