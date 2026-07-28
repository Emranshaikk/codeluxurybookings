import json
import re

def extract_analysis_text():
    with open('audit_distances_comparison.json', 'r') as f:
        comparisons = json.load(f)
        
    incorrect_filenames = [
        'bahamas-to-newyork-private-jet-cost.html',
        'dallas-to-denver-private-jet-cost.html',
        'denver-to-dallas-private-jet-cost.html',
        'hawaii-to-losangeles-private-jet-cost.html',
        'houston-to-miami-private-jet-cost.html',
        'la-to-lasvegas-private-jet-cost.html',
        'lasvegas-to-la-private-jet-cost.html',
        'losangeles-to-hawaii-private-jet-cost.html',
        'maldives-to-riyadh-private-jet-cost.html',
        'miami-to-houston-private-jet-cost.html',
        'newyork-to-bahamas-private-jet-cost.html',
        'riyadh-to-maldives-private-jet-cost.html'
    ]
    
    results = {}
    
    for filename in incorrect_filenames:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
            
        # Match the corridor analysis paragraph
        analysis_match = re.search(r'Corridor Analysis</h2>\s*<p[^>]*>(.*?)</p>', content, re.DOTALL | re.IGNORECASE)
        results[filename] = analysis_match.group(1).strip() if analysis_match else "NOT FOUND"
        
    for k, v in results.items():
        print(f"File: {k}\nText: {v}\n" + "-"*50)

if __name__ == '__main__':
    extract_analysis_text()
