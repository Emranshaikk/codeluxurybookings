import json

def list_correct_speeds():
    with open('audit_distances_comparison.json', 'r') as f:
        comparisons = json.load(f)
        
    correct_list = []
    for item in comparisons:
        deviation = abs(item['stated_dist'] - item['real_dist']) / item['real_dist']
        if deviation <= 0.10:
            # Parse stated time e.g. "12h 11m" into hours
            time_str = item['stated_time']
            hours = 0.0
            if 'h' in time_str:
                parts = time_str.split('h')
                hours += float(parts[0])
                if 'm' in parts[1]:
                    hours += float(parts[1].replace('m', '')) / 60.0
            elif 'm' in time_str:
                hours += float(time_str.replace('m', '')) / 60.0
            
            speed = item['real_dist'] / hours if hours > 0 else 0
            correct_list.append((item['filename'], item['real_dist'], hours, time_str, speed))
            
    correct_list.sort(key=lambda x: x[1])
    print(f"Correct routes sorted by distance ({len(correct_list)} total):")
    for item in correct_list:
        print(f"File: {item[0]}, Distance: {item[1]:.0f} mi, Stated Time: {item[3]}, Hours: {item[2]:.2f}, Speed: {item[4]:.1f} mph")

if __name__ == '__main__':
    list_correct_speeds()
