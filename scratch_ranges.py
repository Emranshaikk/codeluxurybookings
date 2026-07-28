import json

def check_ranges():
    with open('audit_distances_comparison.json', 'r') as f:
        comparisons = json.load(f)
        
    light_limit = 2186
    midsize_limit = 3107
    heavy_limit = 4488
    
    over_light = []
    over_midsize = []
    over_heavy = []
    
    for item in comparisons:
        dist = item['real_dist']
        filename = item['filename']
        
        # Skip the ibiza guide blog post
        if dist == 0 or 'guide' in filename:
            continue
            
        if dist > heavy_limit:
            over_heavy.append((filename, dist))
        elif dist > midsize_limit:
            over_midsize.append((filename, dist))
        elif dist > light_limit:
            over_light.append((filename, dist))
            
    print(f"Routes exceeding Light Jet limit ({light_limit} miles) but within Midsize ({len(over_light)}):")
    for filename, dist in over_light:
        print(f"  {filename} ({dist:.0f} miles)")
        
    print(f"\nRoutes exceeding Midsize limit ({midsize_limit} miles) but within Heavy ({len(over_midsize)}):")
    for filename, dist in over_midsize:
        print(f"  {filename} ({dist:.0f} miles)")
        
    print(f"\nRoutes exceeding Heavy limit ({heavy_limit} miles) ({len(over_heavy)}):")
    for filename, dist in over_heavy:
        print(f"  {filename} ({dist:.0f} miles)")

if __name__ == '__main__':
    check_ranges()
