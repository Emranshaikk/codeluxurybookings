import os
import re

# City mapping: key is the lowercase version to find, value is the properly capitalized version
CITIES = {
    'newyork': 'New York',
    'losangeles': 'Los Angeles',
    'lasvegas': 'Las Vegas',
    'sanfrancisco': 'San Francisco',
    'toronto': 'Toronto',
    'chicago': 'Chicago',
    'dallas': 'Dallas',
    'miami': 'Miami',
    'bahamas': 'Bahamas',
    'nice': 'Nice',
    'mykonos': 'Mykonos',
    'paris': 'Paris',
    'geneva': 'Geneva',
    'milan': 'Milan',
    'barcelona': 'Barcelona',
    'amsterdam': 'Amsterdam',
    'rome': 'Rome',
    'london': 'London',
    'dubai': 'Dubai',
    'cabo': 'Cabo',
    'abudhabi': 'Abu Dhabi',
    'doha': 'Doha'
}

def fix_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        for low, cap in CITIES.items():
            # Pattern: Case-insensitive match for the city name as a whole word
            # Negative lookbehind to ensure it's not part of a URL (/city or -city)
            # or part of a path.
            pattern = rf'(?i)(?<!/)(?<!-)\b{low}\b'
            content = re.sub(pattern, cap, content)
        
        if content != original:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
    except Exception as e:
        print(f"Error processing {path}: {e}")
    return False

if __name__ == "__main__":
    count = 0
    # Walk through the entire project
    for root, dirs, files in os.walk('.'):
        # Skip assets and hidden folders
        if any(x in root for x in ['assets', '.git', '.gemini']):
            continue
            
        for file in files:
            if file.endswith('.html'):
                if fix_file(os.path.join(root, file)):
                    count += 1
    
    print(f"Successfully standardized city names in {count} files.")
