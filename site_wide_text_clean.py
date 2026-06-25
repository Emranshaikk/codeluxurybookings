import os
import re

def clean_html_text(html):
    # Split HTML by tags: odd elements are tags (e.g., <span class="...">), even are text nodes
    parts = re.split(r'(<[^>]*>)', html)
    
    for i in range(len(parts)):
        # Only process text nodes (even indices)
        if i % 2 == 0:
            text = parts[i]
            
            # 1. Protect YYYY-MM-DD dates (e.g. 2026-05-11) by replacing them with tokens
            dates = re.findall(r'\b2026-\d{2}-\d{2}\b', text)
            date_tokens = {}
            for d in dates:
                token = f"__PROTECTED_DATE_{len(date_tokens)}__"
                date_tokens[token] = d
                text = text.replace(d, token)
            
            # 2. Protect timeline year tags or explicit timeline numbers if they are single numbers in timelines
            # If the text is exactly "2026" (common in timeline divs), let's protect it
            is_timeline_year = text.strip() == "2026"
            if is_timeline_year:
                continue
                
            # 3. Clean specific phrases first to keep them smooth
            phrases = {
                r'\bSummer 2026\b': 'the Upcoming Summer',
                r'\bsummer 2026\b': 'the upcoming summer',
                r'\bMay 2026\b': 'Recently',
                r'\bJune 2026\b': 'Recently',
                r'\bJuly 2026\b': 'Recently',
                r'\bAugust 2026\b': 'Recently',
            }
            for pattern, repl in phrases.items():
                text = re.sub(pattern, repl, text, flags=re.IGNORECASE)
                
            # 4. Clean standalone "2026" with surrounding spaces or colons
            # Match ": 2026" or "2026:" or " - 2026" or "2026"
            text = re.sub(r'\s*:\s*\b2026\b', ':', text)
            text = re.sub(r'\b2026\b\s*:\s*', '', text)
            text = re.sub(r'\s*-\s*\b2026\b', '', text)
            text = re.sub(r'\b2026\b\s*-\s*', '', text)
            text = re.sub(r'\b2026\b', '', text)
            
            # 5. Clean up any double spaces introduced
            text = re.sub(r'  +', ' ', text)
            
            # 6. Restore protected dates
            for token, d in date_tokens.items():
                text = text.replace(token, d)
                
            parts[i] = text
            
    return ''.join(parts)

def process_file(filepath):
    if not filepath.endswith(".html"):
        return False
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    original = content
    content = clean_html_text(content)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    directory = "."
    files = [f for f in os.listdir(directory) if f.endswith(".html")]
    print(f"Purging remaining standalone 2026 references in text nodes for {len(files)} files...")
    
    cleaned_count = 0
    for filename in files:
        filepath = os.path.join(directory, filename)
        # Skip raw templates to protect developer template files
        if "template" in filename:
            continue
        try:
            if process_file(filepath):
                print(f"Text cleaned in: {filename}")
                cleaned_count += 1
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            
    print(f"Text cleanup complete. Cleaned {cleaned_count} files.")

if __name__ == "__main__":
    main()
