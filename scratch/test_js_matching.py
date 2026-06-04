import json
import os

def test_matching():
    filepath = "blog-data.json"
    if not os.path.exists(filepath):
        print("blog-data.json not found!")
        return
        
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    yacht_list = []
    jet_list = []
    villa_list = []
    
    for item in data:
        url = item.get('url', '').lower()
        itemCat = item.get('category', '').lower()
        
        # Simulating JS filter logic
        # Jet:
        is_route_jet = '-private-jet-cost' in url or 'private-jet' in url or 'aviation' in url
        matches_jet = 'jet' in itemCat or 'aviation' in itemCat or 'aircraft' in itemCat or is_route_jet or 'lifestyle' in itemCat
        
        # Yacht:
        is_route_yacht = 'yacht' in url or 'boat' in url or 'catamaran' in url
        matches_yacht = 'yacht' in itemCat or 'boat' in itemCat or 'catamaran' in itemCat or is_route_yacht or 'lifestyle' in itemCat
        
        # Villa:
        is_route_villa = 'villa' in url or 'island' in url or 'estate' in url
        matches_villa = 'villa' in itemCat or 'island' in itemCat or 'estate' in itemCat or is_route_villa or 'lifestyle' in itemCat
        
        matched = []
        if matches_jet:
            matched.append('private jet')
            jet_list.append(item['url'])
        if matches_yacht:
            matched.append('private yacht')
            yacht_list.append(item['url'])
        if matches_villa:
            matched.append('luxury villa')
            villa_list.append(item['url'])
            
        if len(matched) > 1:
            print(f"OVERLAP: {item['url']} matches categories: {matched} | json_category: '{itemCat}'")
        elif len(matched) == 0:
            print(f"NO MATCH: {item['url']} matches zero categories | json_category: '{itemCat}'")

    print(f"\nSummary of JS Filter Matches:")
    print(f"Total under Private Jet tab: {len(jet_list)}")
    print(f"Total under Private Yacht tab: {len(yacht_list)}")
    print(f"Total under Luxury Villa tab: {len(villa_list)}")

if __name__ == '__main__':
    test_matching()
