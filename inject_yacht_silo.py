import os
import re

# Define the Yachting Authority Silo HTML block
YACHT_SILO_BLOCK = """
    <!-- YACHTING AUTHORITY SILO -->
    <div style="max-width: 1200px; margin: 3rem auto 0; padding: 2rem; border-top: 1px solid rgba(212,175,55,0.1); text-align: center;">
        <h4 class="serif gold-text" style="font-size: 1.4rem; margin-bottom: 1.5rem; letter-spacing: 2px;">Yachting Authority Silo</h4>
        <div style="display: flex; justify-content: center; gap: 1.5rem; flex-wrap: wrap; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px;">
            <a href="https://eliteluxurybookings.com/motor-yacht-vs-sailing-yacht-charter/" style="color: rgba(255,255,255,0.6); text-decoration: none; transition: 0.3s;" onmouseover="this.style.color='#D4AF37'" onmouseout="this.style.color='rgba(255,255,255,0.6)'">Motor vs Sailing</a>
            <a href="https://eliteluxurybookings.com/cost-to-charter-superyacht-2026/" style="color: rgba(255,255,255,0.6); text-decoration: none; transition: 0.3s;" onmouseover="this.style.color='#D4AF37'" onmouseout="this.style.color='rgba(255,255,255,0.6)'">Charter Costs</a>
            <a href="https://eliteluxurybookings.com/best-mediterranean-yacht-destinations/" style="color: rgba(255,255,255,0.6); text-decoration: none; transition: 0.3s;" onmouseover="this.style.color='#D4AF37'" onmouseout="this.style.color='rgba(255,255,255,0.6)'">Mediterranean Guide</a>
            <a href="https://eliteluxurybookings.com/yacht-charter-apa-guide/" style="color: rgba(255,255,255,0.6); text-decoration: none; transition: 0.3s;" onmouseover="this.style.color='#D4AF37'" onmouseout="this.style.color='rgba(255,255,255,0.6)'">APA Guide</a>
            <a href="https://eliteluxurybookings.com/how-to-rent-superyacht-guide/" style="color: rgba(255,255,255,0.6); text-decoration: none; transition: 0.3s;" onmouseover="this.style.color='#D4AF37'" onmouseout="this.style.color='rgba(255,255,255,0.6)'">Booking Guide</a>
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
            
            # If already has yacht silo, skip
            if "YACHTING AUTHORITY SILO" in content:
                # Update it if it exists to include the new links
                if "APA Guide" not in content:
                    new_content = re.sub(r'<!-- YACHTING AUTHORITY SILO -->.*?<!-- ELB_FOOTER_END -->', YACHT_SILO_BLOCK, content, flags=re.DOTALL)
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Updated Yacht Silo in {filename}")
                continue
                
            # Replace ELB_FOOTER_END with Silo + ELB_FOOTER_END
            if "<!-- ELB_FOOTER_END -->" in content:
                new_content = content.replace("<!-- ELB_FOOTER_END -->", YACHT_SILO_BLOCK)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Injected Yacht Silo into {filename}")

if __name__ == "__main__":
    target_dir = r"c:\Users\imran\OneDrive\Desktop\ELB code"
    inject_silo(target_dir)
