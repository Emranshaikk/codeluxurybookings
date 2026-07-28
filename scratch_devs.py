import json

def check_fit_deviations():
    with open('audit_distances_comparison.json', 'r') as f:
        comparisons = json.load(f)
        
    A = 0.002088
    B = 0.452986
    
    deviations = []
    
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
            
            pred = A * item['real_dist'] + B
            dev = pred - hours
            deviations.append((item['filename'], item['real_dist'], hours, pred, dev))
            
    deviations.sort(key=lambda x: abs(x[4]), reverse=True)
    print("Top 15 deviations from fit:")
    for item in deviations[:15]:
        print(f"File: {item[0]}, Dist: {item[1]:.0f}, Stated Time: {item[2]:.2f}h, Pred Time: {item[3]:.2f}h, Dev: {item[4]*60:.1f}m")

if __name__ == '__main__':
    check_fit_deviations()
