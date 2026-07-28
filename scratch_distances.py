import os
import re
import json
import math

# Coordinates for all 47 cities (Latitude, Longitude)
CITY_COORDS = {
    'Abudhabi': (24.4686, 54.3773),
    'Amsterdam': (52.3676, 4.9041),
    'Aspen': (39.1911, -106.8175),
    'Bahamas': (25.0343, -77.3963),
    'Bali': (-8.4095, 115.1889),
    'Barcelona': (41.3851, 2.1734),
    'Beijing': (39.9042, 116.4074),
    'Brisbane': (-27.4698, 153.0251),
    'Cabo': (22.8905, -109.9167),
    'Cancun': (21.1619, -86.8515),
    'Chicago': (41.8781, -87.6298),
    'Dallas': (32.7767, -96.7970),
    'Denver': (39.7392, -104.9903),
    'Doha': (25.2854, 51.5310),
    'Dubai': (25.2048, 55.2708),
    'Geneva': (46.2044, 6.1432),
    'Goldcoast': (-28.0167, 153.4000),
    'Hawaii': (21.3069, -157.8583),
    'Hongkong': (22.3193, 114.1694),
    'Houston': (29.7604, -95.3698),
    'Ibiza': (38.9067, 1.4206),
    'La': (34.0522, -118.2437),
    'Lasvegas': (36.1716, -115.1398),
    'London': (51.5074, -0.1278),
    'Losangeles': (34.0522, -118.2437),
    'Maldives': (3.2028, 73.2207),
    'Marrakesh': (31.6295, -7.9811),
    'Melbourne': (-37.8136, 144.9631),
    'Miami': (25.7617, -80.1918),
    'Milan': (45.4642, 9.1900),
    'Mykonos': (37.4453, 25.3287),
    'Newyork': (40.7128, -74.0060),
    'Nice': (43.7102, 7.2620),
    'Palma': (39.5696, 2.6502),
    'Paris': (48.8566, 2.3522),
    'Perth': (-31.9505, 115.8605),
    'Riyadh': (24.7136, 46.6753),
    'Rome': (41.9028, 12.4964),
    'Sanfrancisco': (37.7749, -122.4194),
    'Santorini': (36.3932, 25.4615),
    'Seoul': (37.5665, 126.9780),
    'Shanghai': (31.2304, 121.4737),
    'Singapore': (1.3521, 103.8198),
    'Sydney': (-33.8688, 151.2093),
    'Tokyo': (35.6762, 139.6503),
    'Toronto': (43.6532, -79.3832),
    'Turksandcaicos': (21.7833, -71.7333)
}

def haversine_distance(coord1, coord2):
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    
    R = 3958.8 # Earth radius in statute miles
    
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    a = math.sin(delta_phi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c

def analyze_distances():
    with open('route_audit_raw.json', 'r') as f:
        data = json.load(f)
        
    audit_results = []
    
    for filename, info in data.items():
        orig_key = info['origin'].replace(' ', '').title()
        dest_key = info['destination'].replace(' ', '').title()
        
        # Standardize La and Losangeles
        if orig_key == 'La': orig_key = 'Losangeles'
        if dest_key == 'La': dest_key = 'Losangeles'
        
        coord1 = CITY_COORDS.get(orig_key)
        coord2 = CITY_COORDS.get(dest_key)
        
        if not coord1 or not coord2:
            print(f"Missing coords for {orig_key} ({coord1}) or {dest_key} ({coord2}) in {filename}")
            continue
            
        real_dist = haversine_distance(coord1, coord2)
        stated_dist = float(info['distance'].replace(',', '')) if info['distance'] != 'N/A' else 0.0
        
        audit_results.append({
            'filename': filename,
            'origin': info['origin'],
            'destination': info['destination'],
            'stated_dist': stated_dist,
            'real_dist': real_dist,
            'stated_time': info['flight_time'],
            'optimal_class': info['optimal_class']
        })
        
    # Write to a file for review
    with open('audit_distances_comparison.json', 'w') as out_f:
        json.dump(audit_results, out_f, indent=2)
        
    print(f"Processed {len(audit_results)} files for comparison.")
    
if __name__ == '__main__':
    analyze_distances()
