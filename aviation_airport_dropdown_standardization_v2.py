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
    
    name_attr = 'from_airport' if is_from else 'to_airport'
    html = f'<select name="{name_attr}" style="width: 100%; border-radius: 8px; border: 1px solid rgba(255,255,255,0.12); padding: 1.2rem; background: rgba(0,0,0,0.4); color: #fff;" required>\n'
    html += f'    <option value="" disabled selected>Departure: {label} Airport</option>\n' if is_from else f'    <option value="" disabled selected>Arrival: {label} Airport</option>\n'
    for code, name in airports:
        html += f'    <option value="{code}">{code} - {name}</option>\n'
    html += '    <option value="TBC">Other Executive Terminal</option>\n'
    html += '</select>'
    return html

def update_aviation_pages(root_dir):
    count = 0
    # Scan all directories in the root
    for folder in os.listdir(root_dir):
        if '-to-' in folder and 'private-jet-cost' in folder:
            filepath = os.path.join(root_dir, folder, 'index.html')
            if not os.path.exists(filepath):
                continue
                
            # Extract cities (e.g. abudhabi-to-doha-private-jet-cost)
            parts = folder.split('-to-')
            from_city = parts[0]
            to_city = parts[1].split('-')[0]
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            if 'elite-lead-hub' in content:
                from_dropdown = generate_dropdown(from_city, from_city.title(), True)
                to_dropdown = generate_dropdown(to_city, to_city.title(), False)
                
                # We want to replace the current from/to area or inject it before the name input
                # The aviation form usually has: <form ...> <input name="name"> ...
                # We will inject the new airport selection row at the start of the form
                
                form_start_match = re.search(r'<form[^>]*action="https://formspree\.io/f/xwvwanlj"[^>]*>', content)
                if form_start_match:
                    form_start_tag = form_start_match.group(0)
                    
                    # Check if already injected
                    if 'name="from_airport"' in content:
                        continue
                        
                    injection = f'\n                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1.2rem;">\n                    {from_dropdown}\n                    {to_dropdown}\n                </div>'
                    
                    new_content = content.replace(form_start_tag, form_start_tag + injection)
                    
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    
                    count += 1
                    print(f"Upgraded: {folder}")

    print(f"\nFinalized {count} aviation folders with executive airport dropdowns.")

if __name__ == "__main__":
    update_aviation_pages(".")
