import re
import os

def audit_page():
    filepath = r"c:\Users\imran\OneDrive\Desktop\ELB code\all-inclusive-yacht-charter.html"
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
        "/luxury-yacht-charter-caribbean",
        "/yacht-charter-for-corporate-events",
        "/yacht-charter-for-wedding",
        "/private-yacht-vacation-package",
        "/yacht-charter-with-crew",
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
    primary = ["All Inclusive Yacht Charter"]
    
    secondary = [
        "luxury all inclusive yacht charter",
        "all inclusive yacht rental",
        "private yacht charter all inclusive",
        "luxury yacht vacation package",
        "yacht holiday package",
        "fully crewed yacht charter",
        "yacht charter with meals included",
        "yacht charter with crew",
        "yacht charter package",
        "premium yacht charter",
        "luxury yacht rental",
        "private yacht experience",
        "yacht charter service",
        "luxury yacht holiday",
        "all inclusive yacht vacation",
        "yacht charter booking",
        "luxury sailing vacation",
        "yacht travel package"
    ]
    
    buyer_intent = [
        "book an all inclusive yacht charter",
        "luxury yacht quote",
        "request yacht availability",
        "yacht charter pricing",
        "reserve a private yacht charter",
        "yacht vacation package quote",
        "inquire about yacht rental",
        "yacht charter available now",
        "charter a yacht today",
        "luxury yacht booking"
    ]
    
    long_tail = [
        "all inclusive yacht charter for family vacation",
        "luxury all inclusive yacht charter in the Caribbean",
        "private yacht charter with crew and meals included",
        "all inclusive yacht charter for honeymoon",
        "yacht charter package for couples",
        "luxury yacht charter with private chef",
        "all inclusive yacht vacation package",
        "yacht charter for corporate retreats",
        "luxury yacht charter with water sports",
        "all inclusive yacht rental for special events"
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
