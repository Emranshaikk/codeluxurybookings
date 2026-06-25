import os
import re

def clean_content(content):
    # 1. Clean <title>...</title>
    def title_repl(match):
        text = match.group(1)
        cleaned = re.sub(r'\s*\b2026\b\s*', ' ', text)
        cleaned = re.sub(r'\s*\|\s*$', '', cleaned) # Clean trailing dividers
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        return f"<title>{cleaned}</title>"
    content = re.sub(r'<title>(.*?)</title>', title_repl, content, flags=re.IGNORECASE)

    # 2. Clean meta description: <meta name="description" content="..." />
    def meta_desc_repl(match):
        tag_start = match.group(1)
        text = match.group(2)
        cleaned = re.sub(r'\s*\b2026\b\s*', ' ', text)
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        return f'<meta {tag_start}content="{cleaned}"'
    # Capture any attributes before content
    content = re.sub(r'<meta\s+([^>]*?)content=["\'](.*?)["\']', meta_desc_repl, content, flags=re.IGNORECASE)

    # 3. Clean meta property og/twitter tags that were missed (specifically searching for content attribute)
    # This is handled by the meta_desc_repl above because it matches any <meta ... content="..." />.
    # But let's verify if there are meta tags where content comes before property/name.
    # If content comes before: <meta content="..." property="..." />
    def meta_content_first_repl(match):
        text = match.group(1)
        tag_end = match.group(2)
        cleaned = re.sub(r'\s*\b2026\b\s*', ' ', text)
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        return f'<meta content="{cleaned}"{tag_end}'
    content = re.sub(r'<meta\s+content=["\'](.*?)["\']([^>]*?)', meta_content_first_repl, content, flags=re.IGNORECASE)

    # 4. Clean <h1>, <h2>, <h3> headings
    def heading_repl(match):
        tag_open = match.group(1)
        text = match.group(2)
        cleaned = re.sub(r'\s*\b2026\b\s*', ' ', text)
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        # Clean trailing colon or spaces if left over
        cleaned = re.sub(r'\s*:\s*$', '', cleaned)
        return f"<{tag_open}>{cleaned}</"
    content = re.sub(r'<(h[1-3][^>]*?)>(.*?)</', heading_repl, content, flags=re.IGNORECASE | re.DOTALL)

    # 5. Generic body text cleanups for standalone 2026 where appropriate (e.g. "for 2026", "in 2026")
    content = re.sub(r'\bfor 2026\b', 'currently', content, flags=re.IGNORECASE)
    content = re.sub(r'\bin 2026\b', 'currently', content, flags=re.IGNORECASE)
    content = re.sub(r'\b2026 pricing\b', 'current pricing', content, flags=re.IGNORECASE)
    content = re.sub(r'\b2026 Pricing\b', 'Current Pricing', content, flags=re.IGNORECASE)
    content = re.sub(r'\b2026 Price Estimator\b', 'Bespoke Price Estimator', content, flags=re.IGNORECASE)
    content = re.sub(r'\b2026 price estimator\b', 'bespoke price estimator', content, flags=re.IGNORECASE)
    content = re.sub(r'\bSummer 2026\b', 'the Upcoming Summer', content, flags=re.IGNORECASE)

    return content

def process_file(filepath):
    # Skip non-HTML files
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
    print(f"Cleaning standalone 2026 occurrences in {len(files)} HTML files...")
    
    cleaned_count = 0
    for filename in files:
        filepath = os.path.join(directory, filename)
        try:
            if process_file(filepath):
                print(f"Cleaned metadata in: {filename}")
                cleaned_count += 1
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            
    print(f"Cleanup complete. Cleaned {cleaned_count} files.")

if __name__ == "__main__":
    main()
