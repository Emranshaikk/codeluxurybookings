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
    ],
    'toronto': [('CYYZ', 'Toronto Pearson'), ('CYTZ', 'Billy Bishop')],
    'miami': [('KOPF', 'Opa-Locka (Jet Hub)'), ('KMIA', 'Miami Intl'), ('KFLL', 'Fort Lauderdale Executive')],
    'lax': [('KVNY', 'Van Nuys (Private Hub)'), ('KLAX', 'LAX International')],
    'losangeles': [('KVNY', 'Van Nuys (Private Hub)'), ('KLAX', 'LAX International')],
    'cabo': [('MMSD', 'San Jose del Cabo')],
    'cancun': [('MMUN', 'Cancun International')],
    'dallas': [('KDAL', 'Love Field (Executive Hub)')],
    'houston': [('KHOU', 'Hobby (Private Terminal)')],
    'chicago': [('KPWK', 'Palwaukee Executive'), ('KMDW', 'Midway Intl')],
    'aspen': [('KASE', 'Aspen Pitkin')],
    'geneva': [('LSGG', 'Geneva Executive')],
    'turksandcaicos': [('MBPV', 'Providenciales Intl')],
    'bahamas': [('MYNN', 'Nassau Lynden Pindling')],
    'ibiza': [('LEIB', 'Ibiza Executive')],
    'mallorca': [('LEPA', 'Palma Executive')],
    'palma': [('LEPA', 'Palma Executive')],
    'mykonos': [('LGMK', 'Mykonos Island')],
    'santorini': [('LGSR', 'Santorini (Thira)')]
}

def generate_select(city_key, label, element_id, name):
    city_key = city_key.lower().replace('-', '').replace(' ', '')
    airports = AIRPORT_DB.get(city_key, [(city_key.upper(), f'{city_key.title()} Terminal')])
    
    html = f'<select id="{element_id}" name="{name}" class="form-control" style="border-radius: 8px; border: 1px solid rgba(255,255,255,0.12); padding: 1.1rem; background: rgba(5,5,5,0.6); color: #fff; width: 100%;" required>\n'
    html += f'    <option value="" disabled selected>{label} Airport</option>\n'
    for code, desc in airports:
        html += f'    <option value="{code}">{code} - {desc}</option>\n'
    html += '    <option value="TBC">Other Private Terminal</option>\n'
    html += '</select>'
    return html

def upgrade_aviation_folders(root_dir):
    count = 0
    pattern = re.compile(r'([a-z]+)-to-([a-z0-9\-]+)-private-jet-cost', re.I)
    
    for folder in os.listdir(root_dir):
        match = pattern.match(folder)
        if match:
            from_city = match.group(1)
            to_city = match.group(2)
            
            filepath = os.path.join(root_dir, folder, 'index.html')
            if not os.path.exists(filepath):
                continue
                
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # If Valens Engine exists, upgrade it
            if 'valensEngineForm' in content:
                from_html = generate_select(from_city, from_city.title(), 'v_dep', 'departure')
                to_html = generate_select(to_city, to_city.title(), 'v_arr', 'arrival')
                
                # Replace the text inputs specifically
                dep_pattern = r'<input[^>]*id="v_dep"[^>]*>'
                arr_pattern = r'<input[^>]*id="v_arr"[^>]*>'
                
                new_content = re.sub(dep_pattern, from_html, content)
                new_content = re.sub(arr_pattern, to_html, new_content)
                
                if new_content != content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    count += 1
                    print(f"Upgraded Dropdowns: {folder}")
    
    print(f"\nFinalized {count} aviation pages with precise Executive Airport dropdowns.")

if __name__ == "__main__":
    upgrade_aviation_folders(".")
