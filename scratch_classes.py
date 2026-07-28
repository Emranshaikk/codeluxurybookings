import json

def get_optimal_classes():
    with open('audit_distances_comparison.json', 'r') as f:
        comparisons = json.load(f)
        
    classes = set()
    for item in comparisons:
        deviation = abs(item['stated_dist'] - item['real_dist']) / item['real_dist']
        if deviation <= 0.10:
            classes.add(item['optimal_class'])
            
    print("Unique Optimal Class values on correct routes:")
    for c in sorted(list(classes)):
        print(f"  - '{c}'")

if __name__ == '__main__':
    get_optimal_classes()
