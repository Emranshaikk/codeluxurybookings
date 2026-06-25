import os
import re

def clean_content(content):
    # 1. Clean nested headings using the backreference pattern to handle inline elements like <span>
    def heading_repl(match):
        tag_name = match.group(1)
        tag_attrs = match.group(2)
        text = match.group(3)
        cleaned = re.sub(r'\s*\b2026\b\s*', ' ', text)
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        cleaned = re.sub(r'\s*:\s*$', '', cleaned) # Clean trailing colon
        return f"<{tag_name}{tag_attrs}>{cleaned}</{tag_name}>"
        
    content = re.compile(r'<(h[1-3])([^>]*?)>(.*?)</\1>', re.IGNORECASE | re.DOTALL).sub(heading_repl, content)

    # 2. Specific body phrase cleanup
    replacements = {
        r'\bsecure a 2026 hull\b': 'secure a hull',
        r'\bAll 2026 charter vessels\b': 'All charter vessels',
        r'\bmaximizing your 2026 bareboat experience\b': 'maximizing your bareboat experience',
        r'\bCalculate your 2026 procurement costs\b': 'Calculate your procurement costs',
        r'\bRequest Your 2026 Dubai Charter Quote\b': 'Request Your Dubai Charter Quote',
        r'\b2026 Cost Masterclass\b': 'Cost Masterclass',
        r'\bLast Updated: May 2026\b': 'Last Updated: Recently',
        r'\b2026 pricing\b': 'current pricing',
        r'\b2026 Pricing\b': 'Current Pricing',
        r'\b2026 price estimates\b': 'current price estimates',
        r'\bIn 2026, the\b': 'Currently, the',
        r'\bin 2026, the\b': 'currently, the',
        r'\b2026 charter vessels\b': 'current charter vessels',
        r'\bJuly 12 - July 19, 2026\b': 'July 12 - July 19',
        r'\bOct 12 - Oct 22, 2026\b': 'Oct 12 - Oct 22',
        r'\bto secure a 2026 hull\b': 'to secure a hull',
        r'\b2026 hull in the Balearics\b': 'hull in the Balearics',
    }

    for pattern, repl in replacements.items():
        content = re.sub(pattern, repl, content, flags=re.IGNORECASE)

    return content

def process_file(filepath):
    if not filepath.endswith(".html"):
        return False
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    original = content
    content = clean_content(content)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    directory = "."
    files = [f for f in os.listdir(directory) if f.endswith(".html")]
    print(f"Executing advanced cleanup on {len(files)} HTML files...")
    
    cleaned_count = 0
    for filename in files:
        filepath = os.path.join(directory, filename)
        try:
            if process_file(filepath):
                print(f"Cleaned advanced phrases in: {filename}")
                cleaned_count += 1
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            
    print(f"Advanced cleanup complete. Cleaned {cleaned_count} files.")

if __name__ == "__main__":
    main()
