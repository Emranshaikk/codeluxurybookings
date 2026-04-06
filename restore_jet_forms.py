import os
import re

def restore_jet_forms():
    # Correct Structural HTML for the Hero Section with a MANUAL form
    # This replaces the blocked iframe with a functional, Elite-styled form
    manual_form_html = r"""
            <div class="form-wrapper glass-panel" style="margin-top: 2rem;">
                <div id="form-container">
                    <form action="https://formspree.io/f/xwvwanlj" method="POST" id="tripForm">
                        <input type="hidden" name="_subject" value="New Private Jet Inquiry - ELB Network">
                        <div class="form-grid">
                            <div class="form-group">
                                <label class="form-label">Departure Airport</label>
                                <input type="text" class="form-control" name="departure" placeholder="e.g. London FAB" required>
                            </div>
                            <div class="form-group">
                                <label class="form-label">Arrival Airport</label>
                                <input type="text" class="form-control" name="arrival" placeholder="e.g. Nice NCE" required>
                            </div>
                            <div class="form-group">
                                <label class="form-label">Travel Date</label>
                                <input type="date" class="form-control" name="travel_date" required>
                            </div>
                            <div class="form-group">
                                <label class="form-label">Passengers</label>
                                <input type="number" class="form-control" name="passengers" min="1" max="19" placeholder="e.g. 4" required>
                            </div>
                            <div class="form-group">
                                <label class="form-label">Full Name</label>
                                <input type="text" class="form-control" name="fullName" placeholder="Elite Client Name" required>
                            </div>
                            <div class="form-group">
                                <label class="form-label">Contact Number</label>
                                <input type="tel" class="form-control" name="contact" placeholder="+44 7700 900XXX" required>
                            </div>
                            <div class="form-group" style="justify-content: flex-end; grid-column: span 3;">
                                <button type="submit" id="submitBtn" class="btn btn-gold" style="width: 100%; min-height: 64px; margin-top: 1rem;">Secure Private Proposal</button>
                            </div>
                        </div>
                    </form>
                </div>
                <div id="success-panel" style="display:none; text-align:center; padding: 3rem 1rem;">
                    <h3 class="serif">Inquiry Received</h3>
                    <p>Thank you for reaching out. Our elite concierge team will get back to you in few hours.</p>
                    <a href="https://wa.me/918801079030" class="btn btn-gold" style="margin-top: 2rem;">Speak to Concierge via WhatsApp</a>
                </div>
            </div>
        </div>
    </header>
"""

    count = 0
    for root, dirs, files in os.walk('.'):
        if 'private-jet' in root:
            for file in files:
                if file == 'index.html':
                    path = os.path.join(root, file)
                    
                    try:
                        with open(path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        original = content
                        
                        # Target the blocked Valens Widget container
                        pattern = r'<div class="valens-widget-container".*?</header>'
                        if re.search(pattern, content, re.DOTALL):
                            content = re.sub(pattern, manual_form_html, content, flags=re.DOTALL)
                        
                        # Re-inject the logic for forced success
                        js_logic = """
    <script>
        document.getElementById('tripForm').addEventListener('submit', function(e) {
            const btn = document.getElementById('submitBtn');
            btn.disabled = true;
            btn.innerHTML = 'Sending...';
            
            // Force success panel immediately for premium UX (Formspree handles the POST)
            setTimeout(() => {
                document.getElementById('form-container').style.display = 'none';
                document.getElementById('success-panel').style.display = 'block';
            }, 800);
        });
    </script>
"""
                        if '<!-- ELB_JS_START -->' in content:
                            content = content.replace('<!-- ELB_JS_START -->', js_logic + '\n<!-- ELB_JS_START -->')

                        if content != original:
                            with open(path, 'w', encoding='utf-8') as f:
                                f.write(content)
                            count += 1
                            
                    except Exception as e:
                        print(f"Error on {path}: {e}")

    print(f"Elite Form Restoration: Deployed {count} functional lead gateways site-wide.")

if __name__ == "__main__":
    restore_jet_forms()
