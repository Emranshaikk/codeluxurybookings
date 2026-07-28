import os
import re
import json

def analyze_all_routes():
    files = [f for f in os.listdir('.') if f.endswith('.html') and '-to-' in f and 'private-jet-cost' in f]
    print(f"Found {len(files)} route files.")
    
    results = {}
    unique_cities = set()
    
    for f in files:
        filepath = os.path.join('.', f)
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
            
        # Extract distance, flight time, and optimal class
        distance_match = re.search(r'Mission Distance</p>\s*<h3[^>]*>\s*([\d,]+)\s*<span[^>]*>Miles</span></h3>', content, re.IGNORECASE)
        if not distance_match:
            distance_match = re.search(r'([\d,]+)\s*Miles', content, re.IGNORECASE)
            
        time_match = re.search(r'Est\. Flight Time</p>\s*<h3[^>]*>\s*([\d\w\s]+)</h3>', content, re.IGNORECASE)
        if not time_match:
            time_match = re.search(r'Flight Time Estimate:</span>\s*<strong[^>]*>([\d\w\s]+)</strong>', content, re.IGNORECASE)
            
        class_match = re.search(r'Optimal Class</p>\s*<h3[^>]*>\s*([^<]+)</h3>', content, re.IGNORECASE)
        
        # Extract email target
        email_match = re.search(r'formsubmit\.co/ajax/([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', content)
        
        # Extract breadcrumbs
        breadcrumb_match = re.search(r'href="([^"]+)"[^>]*>Private Jets</a>', content)
        schema_breadcrumb_match = re.search(r'"position": 2,\s*"name": "Private Jet Charter",\s*"item": "([^"]+)"', content)
        
        # Extract schema pricing
        schema_price_match = re.search(r'"offers": \{\s*"@type": "AggregateOffer",\s*"lowPrice": "([^"]+)",\s*"highPrice": "([^"]+)",\s*"priceCurrency": "([^"]+)"', content)
        
        # Extract LocalBusiness image
        local_business_img = re.search(r'"@type": "LocalBusiness",.*? "image": "([^"]+)"', content, re.DOTALL)
        
        # Check ticker for corrupted chars
        corrupted_ticker = "??" in content or "Intelligence Alert" in content
        
        dist = distance_match.group(1).strip() if distance_match else "N/A"
        time_val = time_match.group(1).strip() if time_match else "N/A"
        opt_class = class_match.group(1).strip() if class_match else "N/A"
        email_tgt = email_match.group(1).strip() if email_match else "N/A"
        bc_href = breadcrumb_match.group(1).strip() if breadcrumb_match else "N/A"
        bc_schema = schema_breadcrumb_match.group(1).strip() if schema_breadcrumb_match else "N/A"
        
        low_p = schema_price_match.group(1) if schema_price_match else "N/A"
        high_p = schema_price_match.group(2) if schema_price_match else "N/A"
        curr_p = schema_price_match.group(3) if schema_price_match else "N/A"
        
        lb_img = local_business_img.group(1) if local_business_img else "N/A"
        
        # Get city names from filename
        # e.g., houston-to-miami-private-jet-cost.html
        parts = f.replace('-private-jet-cost.html', '').replace('-private-jet-cost-guide.html', '').split('-to-')
        if len(parts) == 2:
            orig, dest = parts[0], parts[1]
            unique_cities.add(orig.replace('-', ' ').title())
            unique_cities.add(dest.replace('-', ' ').title())
        else:
            orig, dest = "Unknown", "Unknown"
            
        results[f] = {
            "origin": orig,
            "destination": dest,
            "distance": dist,
            "flight_time": time_val,
            "optimal_class": opt_class,
            "email_target": email_tgt,
            "breadcrumb_href": bc_href,
            "breadcrumb_schema": bc_schema,
            "low_price": low_p,
            "high_price": high_p,
            "currency": curr_p,
            "local_business_img": lb_img
        }
        
    print(f"Unique cities: {sorted(list(unique_cities))}")
    print(f"Total unique cities: {len(unique_cities)}")
    
    with open('route_audit_raw.json', 'w') as out_f:
        json.dump(results, out_f, indent=2)
        
if __name__ == '__main__':
    analyze_all_routes()
