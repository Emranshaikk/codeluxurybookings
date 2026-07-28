import json

# Define range limits
light_limit = 2186
midsize_limit = 3107
heavy_limit = 4488

def get_proposed_class(dist):
    if dist <= light_limit:
        return "Light Jet"
    elif dist <= midsize_limit:
        return "Midsize Jet"
    elif dist <= heavy_limit:
        return "Heavy Jet"
    else:
        return "Ultra-Long Range Jet"

def generate_audit_table():
    with open('audit_distances_comparison.json', 'r') as f:
        comparisons = json.load(f)
        
    lines = []
    lines.append("| Route Page File | Real Dist (mi) | Stated Dist (mi) | Proposed Dist (mi) | Stated Time | Proposed Time | Stated Class | Proposed Class | Status |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    
    for item in comparisons:
        filename = item['filename']
        if 'guide' in filename:
            continue
            
        real_dist = round(item['real_dist'])
        stated_dist = round(item['stated_dist'])
        stated_time = item['stated_time']
        stated_class = item['optimal_class']
        
        deviation = abs(stated_dist - real_dist) / real_dist if real_dist > 0 else 0
        
        # Proposed values
        prop_dist = real_dist
        
        # Calculate flight time
        # Hours = 0.002088 * Distance + 0.453
        prop_hours = 0.002088 * real_dist + 0.453
        h_part = int(prop_hours)
        m_part = round((prop_hours - h_part) * 60)
        if m_part == 60:
            h_part += 1
            m_part = 0
        prop_time = f"{h_part}h {m_part}m"
        
        prop_class = get_proposed_class(real_dist)
        
        # Is correct?
        if deviation > 0.10:
            status = "❌ Incorrect"
            prop_dist_str = f"**{prop_dist}**"
            prop_time_str = f"**{prop_time}**"
            prop_class_str = f"**{prop_class}**"
        else:
            status = "✅ Correct"
            prop_dist_str = f"{stated_dist}"
            prop_time_str = f"{stated_time}"
            prop_class_str = f"{stated_class}"
            
        lines.append(f"| [{filename}](file:///c:/Users/imran/OneDrive/Desktop/ELB%20code/{filename}) | {real_dist} | {stated_dist} | {prop_dist_str} | {stated_time} | {prop_time_str} | {stated_class} | {prop_class_str} | {status} |")
        
    with open('audit_table.md', 'w', encoding='utf-8') as out_f:
        out_f.write("\n".join(lines))
        
    print(f"Generated markdown audit table for {len(comparisons)-1} routes.")

if __name__ == '__main__':
    generate_audit_table()
