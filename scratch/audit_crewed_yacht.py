import re
import os

def audit_page():
    filepath = r"c:\Users\imran\OneDrive\Desktop\ELB code\yacht-charter-with-crew.html"
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return
        
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # Calculate readable word count (strip head, style, script, HTML tags)
    body_match = re.search(r'<body>(.*?)</body>', html, re.DOTALL)
    body_content = body_match.group(1) if body_match else html
    
    # Strip script and style blocks inside body
    body_content = re.sub(r'<script.*?>.*?</script>', ' ', body_content, flags=re.DOTALL)
    body_content = re.sub(r'<style.*?>.*?</style>', ' ', body_content, flags=re.DOTALL)
    
    # Strip HTML tags
    text_content = re.sub(r'<[^>]+>', ' ', body_content)
    # Normalize whitespaces
    text_content = ' '.join(text_content.split())
    words = text_content.split()
    word_count = len(words)
    
    print("--- AUDIT RESULTS ---")
    print(f"Readable Word Count (approx text content inside body): {word_count}")
    print(f"Total HTML File Word Count: {len(html.split())}")
    
    # Check 9 cluster links
    target_links = [
        "/yacht-charter-available-now",
        "/all-inclusive-yacht-charter",
        "/luxury-yacht-charter-caribbean",
        "/yacht-charter-for-corporate-events",
        "/yacht-charter-for-wedding",
        "/private-yacht-vacation-package",
        "/last-minute-yacht-charter",
        "/luxury-yacht-rental-for-parties",
        "/private-yacht-charter-for-family-vacation"
    ]
    
    print("\n--- LINK VERIFICATION ---")
    all_links_found = True
    for link in target_links:
        count = html.count(link)
        status = "FOUND" if count > 0 else "MISSING [X]"
        if count == 0:
            all_links_found = False
        print(f"Link '{link}': {status}")
        
    # Check keywords presence
    primary = ["Yacht Charter With Crew"]
    
    secondary = [
        "crewed yacht charter",
        "luxury yacht charter with crew",
        "private yacht with captain and crew",
        "fully crewed yacht charter",
        "crewed luxury yacht rental",
        "yacht charter with professional crew",
        "luxury yacht rental with crew",
        "crewed yacht vacation",
        "private yacht experience",
        "luxury yacht holiday",
        "premium yacht charter",
        "yacht charter service",
        "luxury yacht rental",
        "private yacht charter",
        "yacht holiday package",
        "yacht charter booking",
        "luxury travel experience",
        "yacht rental with staff"
    ]
    
    buyer_intent = [
        "book a crewed yacht charter",
        "yacht charter with crew available now",
        "request yacht availability",
        "luxury yacht quote",
        "yacht charter pricing",
        "reserve a yacht with crew",
        "inquire about yacht rental",
        "crewed yacht charter cost",
        "charter a yacht with captain",
        "luxury yacht booking"
    ]
    
    long_tail = [
        "luxury yacht charter with crew for family vacation",
        "private yacht with captain and crew for corporate events",
        "crewed yacht charter for honeymoon",
        "luxury yacht rental with crew and chef",
        "fully crewed yacht charter in the Caribbean",
        "yacht charter with crew for wedding celebrations",
        "crewed yacht charter for special events",
        "luxury yacht vacation with professional crew",
        "yacht charter with captain chef and crew",
        "all inclusive crewed yacht charter"
    ]
    
    print("\n--- KEYWORD OCCURRENCES ---")
    def check_keywords(keyword_list, label):
        print(f"\n{label} Keywords:")
        for kw in keyword_list:
            # Look for literal string matches (case insensitive)
            count = len(re.findall(re.escape(kw), html, re.IGNORECASE))
            status = f"FOUND ({count} times)" if count > 0 else "MISSING [X]"
            print(f"- '{kw}': {status}")
            
    check_keywords(primary, "Primary")
    check_keywords(secondary, "Secondary")
    check_keywords(buyer_intent, "Buyer Intent")
    check_keywords(long_tail, "Long-tail")

if __name__ == "__main__":
    audit_page()
