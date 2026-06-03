import re
import os

def audit_page():
    filepath = r"c:\Users\imran\OneDrive\Desktop\ELB code\yacht-charter-available-now.html"
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
        "/all-inclusive-yacht-charter",
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
    primary = ["Yacht Charter Available Now"]
    
    secondary = [
        "luxury yacht charter available now",
        "private yacht available now",
        "yacht rental available now",
        "yacht booking available now",
        "luxury yacht rental available today",
        "instant yacht charter",
        "same day yacht charter",
        "yacht charter booking",
        "luxury yacht hire",
        "premium yacht charter",
        "yacht charter service",
        "luxury yacht vacation",
        "private yacht experience",
        "crewed yacht charter",
        "yacht rental near me",
        "luxury yacht rental",
        "yacht holiday package",
        "yacht vacation package"
    ]
    
    buyer_intent = [
        "book a yacht charter now",
        "yacht available for charter today",
        "reserve a yacht immediately",
        "luxury yacht quote",
        "yacht charter inquiry",
        "yacht rental pricing",
        "request yacht availability",
        "charter a yacht today",
        "same-day yacht booking",
        "last-minute yacht rental"
    ]
    
    long_tail = [
        "luxury yacht charter available now for family vacation",
        "yacht charter available now for corporate events",
        "private yacht available now for wedding celebrations",
        "same-day luxury yacht charter",
        "last-minute crewed yacht charter",
        "luxury yacht charter available now in the Caribbean",
        "luxury yacht rental available now with crew",
        "yacht charter available now for private parties",
        "luxury yacht vacation package available now",
        "yacht charter available now for special events"
    ]
    
    print("\n--- KEYWORD OCCURRENCES ---")
    def check_keywords(keyword_list, label):
        print(f"\n{label} Keywords:")
        for kw in keyword_list:
            count = len(re.findall(r'\b' + re.escape(kw) + r'\b', html, re.IGNORECASE))
            status = f"FOUND ({count} times)" if count > 0 else "MISSING [X]"
            print(f"- '{kw}': {status}")
            
    check_keywords(primary, "Primary")
    check_keywords(secondary, "Secondary")
    check_keywords(buyer_intent, "Buyer Intent")
    check_keywords(long_tail, "Long-tail")

if __name__ == "__main__":
    audit_page()
