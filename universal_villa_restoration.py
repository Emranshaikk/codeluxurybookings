import os
import re

def universal_villa_restoration():
    count = 0
    # The Standardized GOLD Formspree Hub for Villas
    VILLA_FORM_HUB = """
    <!-- ELITE VILLA INQUIRY HUB -->
    <section id="villa-inquiry" style="padding: 100px 0; background: #050505; position: relative; overflow: hidden;">
        <div class="container" style="max-width: 800px; margin: 0 auto; position: relative; z-index: 2;">
            <div style="text-align: center; margin-bottom: 50px;">
                <div style="display: inline-block; padding: 8px 16px; background: rgba(212,175,55,0.1); border: 1px solid rgba(212,175,55,0.3); border-radius: 50px; color: #D4AF37; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 20px; animation: pulse 2s infinite;">
                    Elite Direct • Inquiry Received
                </div>
                <h2 style="font-family: 'Cormorant Garamond', serif; font-size: 3.5rem; color: #fff; margin-bottom: 20px;">Secure Your Private Estate</h2>
                <p style="color: rgba(255,255,255,0.7); font-size: 1.1rem; line-height: 1.6;">Our global villa desk provides off-market access to the world's most exclusive retreats. Submit your requirements for a bespoke portfolio.</p>
            </div>

            <div style="background: rgba(15,15,15,0.8); backdrop-filter: blur(20px); border: 1px solid rgba(212,175,55,0.2); border-radius: 24px; padding: 40px; box-shadow: 0 30px 60px rgba(0,0,0,0.5);">
                <form action="https://formspree.io/f/xwvwanlj" method="POST" style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                    <div style="grid-column: span 1;">
                        <label style="display: block; color: #D4AF37; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 10px;">Principal Name</label>
                        <input type="text" name="name" required style="width: 100%; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 15px; color: #fff; font-family: 'Inter', sans-serif;">
                    </div>
                    <div style="grid-column: span 1;">
                        <label style="display: block; color: #D4AF37; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 10px;">Priority Contact</label>
                        <input type="email" name="email" required placeholder="email or phone" style="width: 100%; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 15px; color: #fff; font-family: 'Inter', sans-serif;">
                    </div>
                    <div style="grid-column: span 1;">
                        <label style="display: block; color: #D4AF37; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 10px;">Destination Profile</label>
                        <input type="text" name="destination" placeholder="e.g. Ibiza, Maldives" style="width: 100%; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 15px; color: #fff; font-family: 'Inter', sans-serif;">
                    </div>
                    <div style="grid-column: span 1;">
                        <label style="display: block; color: #D4AF37; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 10px;">Preferred Dates</label>
                        <input type="text" name="dates" placeholder="Season 2026" style="width: 100%; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 15px; color: #fff; font-family: 'Inter', sans-serif;">
                    </div>
                    <div style="grid-column: span 2;">
                        <label style="display: block; color: #D4AF37; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 10px;">Bespoke Requirements</label>
                        <textarea name="message" rows="3" placeholder="Number of guests, staff requirements, helipad access..." style="width: 100%; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 15px; color: #fff; font-family: 'Inter', sans-serif; resize: none;"></textarea>
                    </div>
                    <button type="submit" style="grid-column: span 2; background: linear-gradient(135deg, #D4AF37 0%, #B8860B 100%); color: #000; border: none; border-radius: 12px; padding: 18px; font-weight: 700; text-transform: uppercase; letter-spacing: 2px; cursor: pointer; transition: all 0.3s; margin-top: 10px;">Initialize Personal Concierge</button>
                </form>
            </div>
        </div>
    </section>
    """

    for root, dirs, files in os.walk("."):
        if "index.html" in files:
            filepath = os.path.join(root, "index.html")
            
            # Skip aviation pages as we just fixed them
            if "private-jet" in root:
                continue
                
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                # Semantic Villa Detection
                is_villa = False
                if re.search(r"villa", content, re.I):
                    is_villa = True
                elif re.search(r"estate", content, re.I):
                    is_villa = True
                elif re.search(r"retreat", content, re.I):
                    is_villa = True

                # Exclude Yacht pages even if they mention villa
                if re.search(r"yacht", content, re.I):
                    # If it's a yacht page, we don't want to turn it into a villa hub
                    # Unless it's primarily villa
                    if content.count("yacht") > content.count("villa") * 2:
                        continue

                # If identified as a Villa destination page
                if is_villa:
                    original = content
                    
                    # 1. Clean existing legacy forms (Maritime, search engine, etc.)
                    # We remove common form containers
                    # Look for old formspree or valens
                    content = re.sub(r'<(section|div) id=[^>]*form[^>]*>.*?</\1>', '', content, flags=re.DOTALL)
                    
                    # 2. Inject the New standardized Villa Lead Hub
                    # We inject it after the hero section (usually first section or header)
                    if "</header>" in content:
                        content = content.replace("</header>", "</header>\n" + VILLA_FORM_HUB)
                    elif "</section>" in content:
                        # Find the first closing section and inject after
                        content = content.replace("</section>", "</section>\n" + VILLA_FORM_HUB, 1)

                    if content != original:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(content)
                        count += 1
                        if count % 10 == 0:
                            print(f"Propagated Elite Villa Direct: {count} destinations...")

            except Exception as e:
                print(f"Error on {filepath}: {e}")

    print(f"\nFinalized {count} Private Villa destinations with the high-conversion Formspree Lead Hub.")

if __name__ == "__main__":
    universal_villa_restoration()
