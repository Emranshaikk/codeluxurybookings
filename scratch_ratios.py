import os
import re
import json

def analyze_ratios():
    files = [f for f in os.listdir('.') if f.endswith('.html') and '-to-' in f and 'private-jet-cost' in f]
    ratios = []
    
    for f in files:
        filepath = os.path.join('.', f)
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
            
        distance_match = re.search(r'Mission Distance</p>\s*<h3[^>]*>\s*([\d,]+)', content, re.IGNORECASE)
        flight_time_match = re.search(r'const flightTimeHours\s*=\s*([\d.]+)', content)
        
        if distance_match and flight_time_match:
            dist = float(distance_match.group(1).replace(',', ''))
            hours = float(flight_time_match.group(1))
            if hours > 0:
                speed = dist / hours
                ratios.append((f, dist, hours, speed))
                
    ratios.sort(key=lambda x: x[3])
    print(f"Parsed {len(ratios)} files with valid distance and hours.")
    print("Sample of speeds (miles/hour):")
    for r in ratios[:10]:
        print(f"File: {r[0]}, Dist: {r[1]}, Hours: {r[2]}, Speed: {r[3]:.2f}")
    print("...")
    for r in ratios[-10:]:
        print(f"File: {r[0]}, Dist: {r[1]}, Hours: {r[2]}, Speed: {r[3]:.2f}")

if __name__ == '__main__':
    analyze_ratios()
