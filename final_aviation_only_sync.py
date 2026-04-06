import os
import re

# THE PREMIUM API-CONNECTED VALENS SEARCH ENGINE
API_ENGINE_HTML = r"""
        <!-- ELB_VALENS_API_ENGINE_START -->
        <div class="aviation-search-engine glass-panel" style="margin: 2rem auto; max-width: 1000px; padding: 2.5rem; border: 1px solid var(--primary-gold); position: relative; overflow: hidden; background: rgba(5,5,5,0.8); backdrop-filter: blur(20px); border-radius: 20px; box-shadow: 0 20px 50px rgba(0,0,0,0.5);">
            <div id="search-container">
                <h3 class="serif gold-text" style="font-size: 2.3rem; margin-bottom: 0.5rem; text-align: center;">Elite Search Engine</h3>
                <p style="text-align: center; color: var(--text-muted); font-size: 0.85rem; margin-bottom: 2.5rem; text-transform: uppercase; letter-spacing: 3px;">Direct Valens Dashboard Connection</p>
                
                <form id="valensEngineForm" style="display: flex; flex-direction: column; gap: 1.5rem;">
                    <div class="search-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1.2rem;">
                        <input type="text" id="v_dep" name="departure" class="form-control" placeholder="From (Airport or City)" style="border-radius: 8px; border: 1px solid rgba(255,255,255,0.12); padding: 1.1rem; background: rgba(255,255,255,0.03); color: #fff;" required>
                        <input type="text" id="v_arr" name="arrival" class="form-control" placeholder="To (Airport or City)" style="border-radius: 8px; border: 1px solid rgba(255,255,255,0.12); padding: 1.1rem; background: rgba(255,255,255,0.03); color: #fff;" required>
                        <input type="date" id="v_date" name="travel_date" class="form-control" style="border-radius: 8px; border: 1px solid rgba(255,255,255,0.12); padding: 1.1rem; background: rgba(255,255,255,0.03); color: #fff;" required>
                        <input type="number" id="v_pax" name="passengers" class="form-control" min="1" value="2" style="border-radius: 8px; border: 1px solid rgba(255,255,255,0.12); padding: 1.1rem; background: rgba(255,255,255,0.03); color: #fff;" required>
                    </div>

                    <div class="contact-grid" style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1.2rem;">
                        <input type="text" id="v_name" name="name" class="form-control" placeholder="Full Name" style="border-radius: 8px; border: 1px solid rgba(255,255,255,0.12); padding: 1.1rem; background: rgba(255,255,255,0.03); color: #fff;" required>
                        <input type="email" id="v_email" name="email" class="form-control" placeholder="Email Address" style="border-radius: 8px; border: 1px solid rgba(255,255,255,0.12); padding: 1.1rem; background: rgba(255,255,255,0.03); color: #fff;" required>
                        <input type="tel" id="v_phone" name="contact" class="form-control" placeholder="WhatsApp / Phone" style="border-radius: 8px; border: 1px solid rgba(255,255,255,0.12); padding: 1.1rem; background: rgba(255,255,255,0.03); color: #fff;" required>
                    </div>

                    <button type="submit" id="searchApiBtn" class="btn btn-gold" style="width: 100%; margin-top: 1rem; font-size: 1.2rem; min-height: 75px; font-weight: 700; text-transform: uppercase; letter-spacing: 4px; box-shadow: 0 10px 30px rgba(212, 175, 55, 0.2);">Search Global Fleet</button>
                </form>
            </div>

            <div id="engine-success" style="display: none; text-align: center; padding: 5rem 2rem;">
                <div style="font-size: 4rem; color: var(--primary-gold); margin-bottom: 2rem;">&#10003;</div>
                <h3 class="serif gold-text" style="font-size: 2.8rem;">Sync Successfully</h3>
                <p style="color: #fff; font-size: 1.2rem; max-width: 600px; margin: 0 auto; line-height: 1.6;">Your lead is now on our Valens dashboard. A senior aviation concierge will contact you within 15 minutes.</p>
                <div style="margin-top: 3.5rem; display: flex; gap: 1.5rem; justify-content: center;">
                    <a href="https://wa.me/918801079030" class="btn btn-gold">Priority WhatsApp</a>
                </div>
            </div>
        </div>

        <script>
        const VALENS_API = {
            ENDPOINT: 'https://jetluxe.jetlink.app/api/affiliate/valens/v1/trip/new',
            TOKEN: '64|t997lbxqnHWlW15TpE5FCogSyTev2hKpOLRo2Hjj7cad47bc',
            ICAO_DB: {
                'london': 'EGLL', 'nice': 'LFMN', 'dubai': 'OMDB', 'paris': 'LFPG', 'miami': 'KMIA',
                'new york': 'KJFK', 'jfk': 'KJFK', 'aspen': 'KASE', 'ibiza': 'LEIB'
            }
        };
        document.getElementById('valensEngineForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            const btn = document.getElementById('searchApiBtn');
            btn.disabled = true;
            btn.innerHTML = 'Connecting...';
            const dep_val = document.getElementById('v_dep').value.toLowerCase();
            const arr_val = document.getElementById('v_arr').value.toLowerCase();
            let dep_icao = 'EGLL', arr_icao = 'LFMN'; 
            for (const [key, icao] of Object.entries(VALENS_API.ICAO_DB)) {
                if (dep_val.includes(key)) dep_icao = icao;
                if (arr_val.includes(key)) arr_icao = icao;
            }
            const payload = {
                idempotency_key: crypto.randomUUID(),
                legs: [{
                    date: document.getElementById('v_date').value,
                    passengers: parseInt(document.getElementById('v_pax').value),
                    departure_icao: dep_icao,
                    arrival_icao: arr_icao,
                    time: "12:00"
                }],
                customer: {
                    full_name: document.getElementById('v_name').value,
                    contact: document.getElementById('v_phone').value,
                    email: document.getElementById('v_email').value
                }
            };
            try {
                const response = await fetch(VALENS_API.ENDPOINT, {
                    method: 'POST',
                    headers: { 'Authorization': `Bearer ${VALENS_API.TOKEN}`, 'Content-Type': 'application/json', 'Accept': 'application/json' },
                    body: JSON.stringify(payload)
                });
                if (response.ok) {
                    document.getElementById('search-container').style.display = 'none';
                    document.getElementById('engine-success').style.display = 'block';
                } else { alert("Sync failed. Please use WhatsApp support."); }
            } catch (err) { alert("Network error. Please use WhatsApp support."); }
        });
        </script>
        <!-- ELB_VALENS_API_ENGINE_END -->
"""

def final_aviation_sync():
    count = 0
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file == 'index.html':
                 path = os.path.join(root, file)
                 if any(x in root for x in ['node_modules', '.git', 'assets']): continue
                 
                 with open(path, 'r', encoding='utf-8') as f:
                     content = f.read()
                 
                 # ONLY target Aviation/Jet and STRICTLY exclude Yacht/Villa
                 is_aviation_path = 'private-jet' in root or 'charter-flights' in root or 'jet' in root.lower()
                 is_aviation_content = 'Private Jet' in content or 'Jet Charter' in content
                 is_yacht = 'luxury-yacht-rentals' in root or 'yacht' in root.lower()
                 is_villa = 'luxury-villa-rentals' in root or 'villa' in root.lower()
                 
                 if not (is_aviation_path or is_aviation_content): continue
                 if is_yacht or is_villa: continue # Safety: Don't touch these

                 original = content
                 
                 # Replace patterns
                 patterns = [
                     r'<!-- Affiliate.*?Widget -->\s*<div class="affiliate-widget">.*?</div>',
                     r'<!-- VALENS_WIDGET_START -->.*?<!-- VALENS_WIDGET_END -->',
                     r'<!-- Master Widget -->\s*<div class="affiliate-widget">.*?</div>'
                 ]
                 
                 for p in patterns:
                     content = re.sub(p, API_ENGINE_HTML, content, flags=re.DOTALL)
                 
                 # Specific check for hero-sub injection
                 if 'ELB_VALENS_API_ENGINE_START' not in content and 'hero-sub' in content:
                     content = content.replace('</p>', '</p>\n' + API_ENGINE_HTML, 1)

                 if content != original:
                     with open(path, 'w', encoding='utf-8') as f:
                         f.write(content)
                     count += 1
                     print(f"Final Aviation Sync: {path}")

    print(f"\nFinalized Elite Aviation search engine on {count} dedicated private jet pages.")

if __name__ == "__main__":
    final_aviation_sync()
