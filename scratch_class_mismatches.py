import json

def check_all_optimal_classes():
    with open('audit_distances_comparison.json', 'r') as f:
        comparisons = json.load(f)
        
    light_limit = 2186
    midsize_limit = 3107
    heavy_limit = 4488
    
    mismatches = []
    
    for item in comparisons:
        dist = item['real_dist']
        filename = item['filename']
        opt_class = item['optimal_class']
        
        if dist == 0 or 'guide' in filename:
            continue
            
        # Determine expected class
        if dist <= light_limit:
            expected = 'Light Jet'
        elif dist <= midsize_limit:
            expected = 'Midsize Jet'
        elif dist <= heavy_limit:
            expected = 'Heavy Jet'
        else:
            expected = 'Ultra-Long Range Jet'
            
        # Check compatibility
        # If opt_class matches expected, or is a combination like "Heavy or Ultra-Long Range Jet" for long distance, it is fine.
        # But if a very long route is recommended as Light Jet, or vice versa, it is a mismatch.
        is_ok = True
        
        if expected == 'Light Jet':
            # Anything is safe for Light Jet distance, but typically we recommend Light Jet or Midsize
            if opt_class not in ['Light Jet', 'Midsize Jet', 'Midsize / Super-Mid', 'Heavy Jet', 'Heavy or Ultra-Long Range Jet']:
                is_ok = False
        elif expected == 'Midsize Jet':
            # Light Jet is not sufficient
            if opt_class in ['Light Jet']:
                is_ok = False
        elif expected == 'Heavy Jet':
            # Light Jet and Midsize Jet are not sufficient
            if opt_class in ['Light Jet', 'Midsize Jet', 'Midsize / Super-Mid']:
                is_ok = False
        elif expected == 'Ultra-Long Range Jet':
            # Light, Midsize, and Heavy Jet (non-ULR) are not sufficient
            if opt_class in ['Light Jet', 'Midsize Jet', 'Midsize / Super-Mid', 'Heavy Jet']:
                is_ok = False
                
        if not is_ok:
            mismatches.append((filename, dist, opt_class, expected))
            
    print(f"Optimal Class mismatches found: {len(mismatches)}")
    for filename, dist, opt_class, expected in mismatches:
        print(f"File: {filename}, Dist: {dist:.0f} miles, Stated Class: '{opt_class}', Expected Min Class: '{expected}'")

if __name__ == '__main__':
    check_all_optimal_classes()
