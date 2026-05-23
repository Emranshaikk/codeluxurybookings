import os
import re

def audit_html_file(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    issues = []
    
    # 1. Check if file is extremely small
    file_size = os.path.getsize(file_path)
    if file_size < 2000:
        issues.append(f"Extremely small file size ({file_size} bytes)")
        
    # 2. Check if <body> is missing or empty
    body_match = re.search(r'<body[^>]*>(.*?)</body>', content, re.DOTALL | re.IGNORECASE)
    if not body_match:
        if '<body' not in content.lower():
            issues.append("Missing <body> tag")
    else:
        body_content = body_match.group(1).strip()
        clean_body = re.sub(r'<!--.*?-->', '', body_content, flags=re.DOTALL)
        clean_body = re.sub(r'<script[^>]*>.*?</script>', '', clean_body, flags=re.DOTALL)
        clean_body = re.sub(r'<style[^>]*>.*?</style>', '', clean_body, flags=re.DOTALL)
        clean_body = re.sub(r'<[^>]+>', '', clean_body)
        clean_body = clean_body.strip()
        
        if len(clean_body) < 100:
            issues.append(f"Body content has very little visible text ({len(clean_body)} chars)")

    # 3. Check if <main> is empty
    main_match = re.search(r'<main[^>]*>(.*?)</main>', content, re.DOTALL | re.IGNORECASE)
    if main_match:
        main_content = main_match.group(1).strip()
        clean_main = re.sub(r'<!--.*?-->', '', main_content, flags=re.DOTALL)
        clean_main = re.sub(r'<script[^>]*>.*?</script>', '', clean_main, flags=re.DOTALL)
        clean_main = re.sub(r'<[^>]+>', '', clean_main)
        clean_main = clean_main.strip()
        if len(clean_main) < 50:
            issues.append(f"<main> tag has very little visible text ({len(clean_main)} chars)")
            
    # 4. Check if there is an unclosed <main> tag
    if '<main' in content.lower() and '</main>' not in content.lower():
        issues.append("Unclosed <main> tag (missing </main>)")
        
    # 5. Check if the page contains a blank template placeholder
    if "<!-- Hero Section -->" in content and len(re.findall(r'<section', content)) == 0 and '<main' in content.lower():
        issues.append("Contains empty main placeholder ('<!-- Hero Section -->')")

    return issues

def main():
    html_files = []
    for root, dirs, files in os.walk('.'):
        if '.git' in root or '_archive' in root or 'scratch' in root:
            continue
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
                
    print(f"Auditing {len(html_files)} HTML files for blank layouts...\n")
    
    blank_pages = 0
    for file_path in html_files:
        issues = audit_html_file(file_path)
        if issues:
            blank_pages += 1
            print(f"[WARNING] {file_path}")
            for issue in issues:
                print(f"   - {issue}")
            print()
            
    print(f"Audit completed. Found {blank_pages} potential blank pages.")

if __name__ == '__main__':
    main()
