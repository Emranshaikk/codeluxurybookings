import json

def check_missing():
    with open('audit_distances_comparison.json', 'r') as f:
        comparisons = json.load(f)
        
    for item in comparisons:
        if item['stated_dist'] == 0:
            print(f"File: {item['filename']} has 0 stated distance.")
            
if __name__ == '__main__':
    check_missing()
