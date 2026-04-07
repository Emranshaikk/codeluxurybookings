import os
import re

# ELB Elite Airport Database (Private Jet Hubs)
AIRPORT_DB = {
    'london': [
        ('EGLF', 'Farnborough (Primary Jet Hub)'),
        ('EGKB', 'Biggin Hill (South London)'),
        ('EGGW', 'Luton (North London)'),
        ('EGSS', 'Stansted (Northeast London)'),
        ('EGWU', 'Northolt (Military/VIP)')
    ],
    'newyork': [
        ('KTEB', 'Teterboro (Private Only)'),
        ('KJFK', 'JFK International'),
        ('KHPN', 'Westchester County'),
        ('KISP', 'Long Island MacArthur'),
        ('KEWR', 'Newark Liberty')
    ],
    'dubai': [
        ('OMDW', 'Al Maktoum (DWC/Jet Hub)'),
        ('OMDB', 'Dubai International (DXB)')
    ],
    'abudhabi': [
        ('OMAD', 'Bateen Executive (AZI)'),
        ('OMAA', 'Abu Dhabi International (AUH)')
    ],
    'paris': [
        ('LFPB', 'Paris Le Bourget (Exclusive)')
    ],
    'nice': [
        ('LFMN', 'Nice Côte d\'Azur')
    ],
    'ibiza': [
        ('LEIB', 'Ibiza Airport')
    ],
    'mallorca': [
        ('LEPA', 'Palma de Mallorca')
    ],
    'aspen': [
        ('KASE', 'Aspen Pitkin County')
    ],
    'geneva': [
        ('LSGG', 'Geneva International')
    ],
    'zurich': [
        ('LSZH', 'Zurich Airport')
    ],
    'milano': [
        ('LIML', 'Linate (Private Terminal)'),
        ('LIMC', 'Malpensa')
    ],
    'riyadh': [
        ('OERK', 'KKIA (Executive Terminal)')
    ],
    'jeddah': [
        ('OEJN', 'KAIA (VIP Terminal)')
    ],
    'doha': [
        ('OTBD', 'Doha International (Jet Hub)')
    ],
    'singapore': [
        ('WSSL', 'Seletar (Jet Terminal)'),
        ('WSSS', 'Changi Airport')
    ]
}

def generate_dropdown(city_key, label, is_from=True):
    city_key = city_key.lower().replace('-', '').replace(' ', '')
    airports = AIRPORT_DB.get(city_key, [('', f'Selected {label} Airport')])
    
    html = f'<select name="{"from_airport" if is_from else "to_airport"}" style="width: 100%; border-radius: 8px; border: 1px solid rgba(255,255,255,0.12); padding: 1.2rem; background: rgba(0,0,0,0.4); color: #fff;" required>\n'
    html += f'    <option value="" disabled selected>Select {label} Airport</option>\n'
    for code, name in airports:
        html += f'    <option value="{code}">{code} - {name}</option>\n'
    html += '    <option value="TBC">Other Executive Terminal</option>\n'
    html += '</select>'
    return html

def standardize_aviation_form(root_dir):
    count = 0
    # Common aviation cost patterns
    patterns = ['private-jet-cost', 'private-jet-charter', 'charter-cost']
    
    for subdir, dirs, files in os.walk(root_dir):
        if any(p in subdir.lower() for p in patterns) and 'index.html' in files:
            filepath = os.path.join(subdir, 'index.html')
            
            # Extract cities from path (e.g. abudhabi-to-doha-private-jet-cost)
            basename = os.path.basename(os.path.normpath(subdir))
            cities = basename.split('-to-')
            if len(cities) < 2:
                continue
            
            from_city = cities[0]
            to_city = cities[1].split('-')[0] # get "doha" from "doha-private-jet-cost"
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Identify the lead form area - we look for the centered hub
            if 'elite-lead-hub' in content:
                from_html = generate_dropdown(from_city, from_city.title(), True)
                to_html = generate_dropdown(to_city, to_city.title(), False)
                
                # Replace the simple inputs or names with specific dropdowns
                # We specifically look for the form structure in the lead hub
                form_pattern = r'(<form action="https://formspree\.io/f/xwvwanlj".*?>)(.*?)(</form>)'
                
                def replace_form_inputs(match):
                    form_start = match.group(1)
                    form_body = match.group(2)
                    form_end = match.group(3)
                    
                    # We inject the city dropdowns into the requirement area or as a new row
                    # Let's add them as a specific row above name/email
                    airport_row = f'\n                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">\n                    {from_html}\n                    {to_html}\n                </div>'
                    
                    # Insert before the first input
                    return form_start + airport_row + form_body + form_end

                new_content = re.sub(form_pattern, replace_form_inputs, content, flags=re.DOTALL)
                
                if new_content != content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    count += 1
                    print(f"Upgraded Dropdowns: {subdir}")

    print(f"\nFinalized {count} aviation pages with specific airport dropdowns.")

if __name__ == "__main__":
    standardize_aviation_form(".")
