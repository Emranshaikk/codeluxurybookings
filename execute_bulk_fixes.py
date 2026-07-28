import os
import re
import json

# 12 Mismatched routes map with exact corrected values
CORRECTIONS = {
    'bahamas-to-newyork-private-jet-cost.html': {
        'old_dist': '5385', 'new_dist': '1101',
        'old_time': '11h 43m', 'new_time': '2h 45m',
        'old_hours': '11.72', 'new_hours': '2.75',
        'old_class': 'Heavy or Ultra-Long Range Jet', 'new_class': 'Light Jet'
    },
    'dallas-to-denver-private-jet-cost.html': {
        'old_dist': '6613', 'new_dist': '663',
        'old_time': '14h 16m', 'new_time': '1h 50m',
        'old_hours': '14.27', 'new_hours': '1.84',
        'old_class': 'Heavy or Ultra-Long Range Jet', 'new_class': 'Light Jet'
    },
    'denver-to-dallas-private-jet-cost.html': {
        'old_dist': '6613', 'new_dist': '663',
        'old_time': '14h 16m', 'new_time': '1h 50m',
        'old_hours': '14.27', 'new_hours': '1.84',
        'old_class': 'Heavy or Ultra-Long Range Jet', 'new_class': 'Light Jet'
    },
    'hawaii-to-losangeles-private-jet-cost.html': {
        'old_dist': '7812', 'new_dist': '2560',
        'old_time': '16h 46m', 'new_time': '5h 48m',
        'old_hours': '16.77', 'new_hours': '5.80',
        'old_class': 'Heavy or Ultra-Long Range Jet', 'new_class': 'Midsize Jet'
    },
    'houston-to-miami-private-jet-cost.html': {
        'old_dist': '5608', 'new_dist': '967',
        'old_time': '12h 11m', 'new_time': '2h 28m',
        'old_hours': '12.18', 'new_hours': '2.47',
        'old_class': 'Heavy or Ultra-Long Range Jet', 'new_class': 'Light Jet'
    },
    'la-to-lasvegas-private-jet-cost.html': {
        'old_dist': '7603', 'new_dist': '228',
        'old_time': '16h 20m', 'new_time': '0h 56m',
        'old_hours': '16.33', 'new_hours': '0.93',
        'old_class': 'Heavy or Ultra-Long Range Jet', 'new_class': 'Light Jet'
    },
    'lasvegas-to-la-private-jet-cost.html': {
        'old_dist': '7603', 'new_dist': '228',
        'old_time': '16h 20m', 'new_time': '0h 56m',
        'old_hours': '16.33', 'new_hours': '0.93',
        'old_class': 'Heavy or Ultra-Long Range Jet', 'new_class': 'Light Jet'
    },
    'losangeles-to-hawaii-private-jet-cost.html': {
        'old_dist': '7812', 'new_dist': '2560',
        'old_time': '16h 46m', 'new_time': '5h 48m',
        'old_hours': '16.77', 'new_hours': '5.80',
        'old_class': 'Heavy or Ultra-Long Range Jet', 'new_class': 'Midsize Jet'
    },
    'maldives-to-riyadh-private-jet-cost.html': {
        'old_dist': '3560', 'new_dist': '2309',
        'old_time': '7h 55m', 'new_time': '5h 16m',
        'old_hours': '7.92', 'new_hours': '5.27',
        'old_class': 'Heavy or Ultra-Long Range Jet', 'new_class': 'Midsize Jet'
    },
    'miami-to-houston-private-jet-cost.html': {
        'old_dist': '5608', 'new_dist': '967',
        'old_time': '12h 11m', 'new_time': '2h 28m',
        'old_hours': '12.18', 'new_hours': '2.47',
        'old_class': 'Heavy or Ultra-Long Range Jet', 'new_class': 'Light Jet'
    },
    'newyork-to-bahamas-private-jet-cost.html': {
        'old_dist': '5385', 'new_dist': '1101',
        'old_time': '11h 43m', 'new_time': '2h 45m',
        'old_hours': '11.72', 'new_hours': '2.75',
        'old_class': 'Heavy or Ultra-Long Range Jet', 'new_class': 'Light Jet'
    },
    'riyadh-to-maldives-private-jet-cost.html': {
        'old_dist': '3560', 'new_dist': '2309',
        'old_time': '7h 55m', 'new_time': '5h 16m',
        'old_hours': '7.92', 'new_hours': '5.27',
        'old_class': 'Heavy or Ultra-Long Range Jet', 'new_class': 'Midsize Jet'
    }
}

def process_all_files():
    with open('audit_distances_comparison.json', 'r', encoding='utf-8') as f:
        comp_data = json.load(f)
    dist_map = {item['filename']: item['real_dist'] for item in comp_data}

    files = [f for f in os.listdir('.') if f.endswith('.html') and '-to-' in f and 'private-jet-cost' in f]
    print(f"Processing {len(files)} route files...")

    updated_count = 0
    
    for filename in files:
        if 'guide' in filename:
            continue

        filepath = os.path.join('.', filename)
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        orig_content = content

        # -------------------------------------------------------------
        # TASK 1: Apply Route Data Corrections (for 12 flagged files)
        # -------------------------------------------------------------
        if filename in CORRECTIONS:
            c = CORRECTIONS[filename]
            
            # Distance
            content = content.replace(f">{c['old_dist']} <span", f">{c['new_dist']} <span")
            content = content.replace(f"For this {c['old_dist']}-mile mission", f"For this {c['new_dist']}-mile mission")
            
            # Flight Time
            content = content.replace(f">{c['old_time']}</h3>", f">{c['new_time']}</h3>")
            content = content.replace(f">{c['old_time']}</strong>", f">{c['new_time']}</strong>")
            content = content.replace(f"ensure a {c['old_time']} arrival", f"ensure a {c['new_time']} arrival")
            content = re.sub(r'const flightTimeHours\s*=\s*' + re.escape(c['old_hours']) + r';', f"const flightTimeHours = {c['new_hours']};", content)
            
            # Optimal Class
            content = content.replace(f">{c['old_class']}</h3>", f">{c['new_class']}</h3>")
            content = content.replace(f"recommend a {c['old_class']}", f"recommend a {c['new_class']}")

        # -------------------------------------------------------------
        # TASK 2: Remove Product Schema
        # -------------------------------------------------------------
        content = re.sub(r'<script\s+type="application/ld\+json">\s*\{\s*"@context":\s*"https://schema\.org",\s*"@type":\s*"Product".*?</script>\s*', '', content, flags=re.DOTALL)
        content = re.sub(r'<script\s+type="application/ld\+json">\{"@context":"https://schema\.org","@type":"Product".*?</script>\s*', '', content, flags=re.DOTALL)

        # -------------------------------------------------------------
        # TASK 6: Remove LocalBusiness Schema
        # -------------------------------------------------------------
        content = re.sub(r'<script\s+type="application/ld\+json">\s*\{\s*"@context":\s*"https://schema\.org",\s*"@type":\s*"LocalBusiness".*?</script>\s*', '', content, flags=re.DOTALL)

        # -------------------------------------------------------------
        # TASK 3: Fix Hardcoded Personal Email & Placeholder
        # -------------------------------------------------------------
        content = content.replace('placeholder="contactshaikk@gmail.com"', 'placeholder="john@example.com"')
        content = content.replace("placeholder='contactshaikk@gmail.com'", "placeholder='john@example.com'")
        content = content.replace('https://formsubmit.co/ajax/contactshaikk@gmail.com', '/submit-lead.php')
        
        # Clean submitLead JS emailPromise block
        content = re.sub(r'// Send to Email via Formsubmit.*?const emailPromise = fetch\(.*?formsubmit\.co.*?\);', '', content, flags=re.DOTALL)
        content = content.replace('await Promise.all([tgPromise, emailPromise]);', 'await tgPromise;')
        content = content.replace('contactshaikk@gmail.com', 'contact@eliteluxurybookings.com')

        # -------------------------------------------------------------
        # TASK 4: Fix Corrupted Navigation / Ticker Character Encoding
        # -------------------------------------------------------------
        content = content.replace('?? Intelligence Alert:', '⚠️ Intelligence Alert:')
        content = content.replace('?? Global Inventory Update:', '⚠️ Global Inventory Update:')
        content = content.replace('? Private Jets', '✈ Private Jets')
        content = content.replace('?? Luxury Villas', '🏡 Luxury Villas')
        content = content.replace('? Luxury Yachts', '⚓ Luxury Yachts')
        content = content.replace('?? Blog', '📰 Blog')
        content = content.replace('?? Contact', '📞 Contact')
        content = content.replace('ÔÜá´©Å', '⚠️')

        # -------------------------------------------------------------
        # TASK 5: Fix Breadcrumb Link Mismatch
        # -------------------------------------------------------------
        content = content.replace('href="https://eliteluxurybookings.com/private-jet-booking-guide/"', 'href="https://eliteluxurybookings.com/elite-private-jet-charter/"')
        content = content.replace('href="/private-jet-booking-guide/"', 'href="/elite-private-jet-charter/"')

        # -------------------------------------------------------------
        # TASK 7: Remove Fake Urgency Alert Styling
        # -------------------------------------------------------------
        new_alert = """<div class="availability-status" style="border: 1px solid rgba(212, 175, 55, 0.25); background: rgba(212, 175, 55, 0.02); padding: 12px 20px; border-radius: 12px; margin: 0 auto 1.5rem; max-width: 700px; display: flex; align-items: center; justify-content: center; gap: 12px;">
                <span style="color: var(--primary-gold); font-size: 0.95rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;">✨ Route Status: High-Availability Executive Corridors Open. Inquire for guaranteed slots.</span>
            </div>"""
        content = re.sub(r'<div[^>]*class="urgency-alert"[^>]*>.*?</div>', new_alert, content, flags=re.DOTALL)

        # -------------------------------------------------------------
        # TASK 1 Extra: Dynamic Range Warning in Calculator
        # -------------------------------------------------------------
        real_dist = dist_map.get(filename, 0)
        
        # Add range warning placeholder div if not already present
        if 'id="range-warning"' not in content and 'id="jet-per-pax-cost"' in content:
            pax_cost_div = '<div style="display: flex; justify-content: space-between;">'
            warning_placeholder = '<div id="range-warning" style="display: none; margin-top: 1rem; padding: 0.8rem; background: rgba(255,77,77,0.08); border: 1px solid rgba(255,77,77,0.3); border-radius: 6px; color: #ff4d4d; font-size: 0.85rem; font-weight: 500; text-align: center;"></div>'
            content = content.replace(pax_cost_div, warning_placeholder + '\n                        ' + pax_cost_div)

        # Add range check logic inside updateJetCalculator
        if 'function updateJetCalculator(' in content and 'const routeDistance =' not in content:
            calc_range_code = f"""            const routeDistance = {round(real_dist)};
            const warningEl = document.getElementById('range-warning');
            if (warningEl) {{
                let warningText = '';
                if (routeDistance > 4488 && selectedJetClass !== 'airliner') {{
                    warningText = '⚠️ Route distance requires an Ultra-Long Range Jet or a refueling stop.';
                }} else if (routeDistance > 3107 && (selectedJetClass === 'light' || selectedJetClass === 'midsize')) {{
                    warningText = '⚠️ Selected class range is insufficient for non-stop flight; Heavy or ULR Jet recommended.';
                }} else if (routeDistance > 2186 && selectedJetClass === 'light') {{
                    warningText = '⚠️ Light Jet range is insufficient for non-stop flight; Midsize or Heavy Jet recommended.';
                }}
                if (warningText) {{
                    warningEl.innerText = warningText;
                    warningEl.style.display = 'block';
                }} else {{
                    warningEl.style.display = 'none';
                }}
            }}"""
            
            content = content.replace("document.getElementById('jet-per-pax-cost').innerText = '€' + perPaxCost.toLocaleString() + ' / pax';", "document.getElementById('jet-per-pax-cost').innerText = '€' + perPaxCost.toLocaleString() + ' / pax';\n" + calc_range_code)

        # Write out updated content if changed
        if content != orig_content:
            with open(filepath, 'w', encoding='utf-8') as out_f:
                out_f.write(content)
            updated_count += 1
            print(f"Updated: {filename}")

    print(f"\nSuccessfully updated {updated_count} files.")

if __name__ == '__main__':
    process_all_files()
