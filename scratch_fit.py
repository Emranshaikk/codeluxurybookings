import json
import math

def fit_formula():
    with open('audit_distances_comparison.json', 'r') as f:
        comparisons = json.load(f)
        
    X = []
    Y = []
    
    for item in comparisons:
        deviation = abs(item['stated_dist'] - item['real_dist']) / item['real_dist']
        if deviation <= 0.10:
            time_str = item['stated_time']
            hours = 0.0
            if 'h' in time_str:
                parts = time_str.split('h')
                hours += float(parts[0])
                if 'm' in parts[1]:
                    hours += float(parts[1].replace('m', '')) / 60.0
            elif 'm' in time_str:
                hours += float(time_str.replace('m', '')) / 60.0
            
            X.append(item['real_dist'])
            Y.append(hours)
            
    n = len(X)
    sum_x = sum(X)
    sum_y = sum(Y)
    sum_xx = sum(x*x for x in X)
    sum_xy = sum(x*y for x, y in zip(X, Y))
    
    # Fit Y = A * X + B
    denom = n * sum_xx - sum_x * sum_x
    if denom == 0:
        print("Cannot fit: denominator is zero.")
        return
        
    A = (n * sum_xy - sum_x * sum_y) / denom
    B = (sum_y * sum_xx - sum_x * sum_xy) / denom
    
    print(f"Fit result: Hours = {A:.6f} * Distance + {B:.6f}")
    
    cruise_speed = 1 / A
    print(f"Effective cruise speed: {cruise_speed:.2f} mph")
    print(f"Effective taxi/overhead time: {B * 60:.1f} minutes ({B:.3f} hours)")
    
    # Check max deviation from fit
    max_dev_hours = 0.0
    for x, y in zip(X, Y):
        pred = A * x + B
        dev = abs(pred - y)
        if dev > max_dev_hours:
            max_dev_hours = dev
            
    print(f"Max deviation from fit: {max_dev_hours * 60:.1f} minutes")

if __name__ == '__main__':
    fit_formula()
