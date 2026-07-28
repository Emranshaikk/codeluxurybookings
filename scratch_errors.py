import json

def check_errors():
    with open('audit_distances_comparison.json', 'r') as f:
        comparisons = json.load(f)
        
    correct_count = 0
    incorrect_count = 0
    
    print("Files with distance mismatch (> 10% deviation):")
    for item in comparisons:
        deviation = abs(item['stated_dist'] - item['real_dist']) / item['real_dist']
        if deviation > 0.10:
            incorrect_count += 1
            print(f"File: {item['filename']}, Stated Dist: {item['stated_dist']:.0f}, Real Dist: {item['real_dist']:.0f}, Stated Time: {item['stated_time']}, Optimal Class: {item['optimal_class']}")
        else:
            correct_count += 1
            
    print(f"\nSummary:\nCorrect (deviation <= 10%): {correct_count}\nIncorrect (deviation > 10%): {incorrect_count}\nTotal: {len(comparisons)}")

if __name__ == '__main__':
    check_errors()
