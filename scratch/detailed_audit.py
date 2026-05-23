import os
import re

def clean_html_for_text_length(html_content):
    # Remove script, style, comments
    text = re.sub(r'<script[^>]*>.*?</script>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
    # Remove all HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Normalize spacing
    text = re.sub(r'\s+', ' ', text)
    return len(text.strip())

def audit_html_file(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    file_size = os.path.getsize(file_path)
    issues = []
    
    # 1. Check if file size is extremely small
    if file_size < 3000:
        issues.append(f"Extremely small file size ({file_size} bytes)")
        
    # 2. Check body and text length
    body_match = re.search(r'<body[^>]*>(.*?)</body>', content, re.DOTALL | re.IGNORECASE)
    if not body_match:
        if '<body' not in content.lower():
            issues.append("Missing <body> tag")
    else:
        body_content = body_match.group(1).strip()
        body_text_len = clean_html_for_text_length(body_content)
        if body_text_len < 300:
            issues.append(f"Body content has extremely little visible text ({body_text_len} characters)")

    # 3. Check main tag content length and placeholders
    main_match = re.search(r'<main[^>]*>(.*?)</main>', content, re.DOTALL | re.IGNORECASE)
    if main_match:
        main_content = main_match.group(1).strip()
        main_text_len = clean_html_for_text_length(main_content)
        if main_text_len < 100:
            issues.append(f"<main> tag content is extremely short ({main_text_len} characters)")
    elif '<main' in content.lower() and '</main>' not in content.lower():
        # Tag is opened but not closed, so regex r'<main[^>]*>(.*?)</main>' fails
        # Let's extract content from <main> to the end of the file or next structural tag
        main_idx = content.lower().find('<main')
        main_content = content[main_idx:]
        main_text_len = clean_html_for_text_length(main_content)
        if main_text_len < 100:
            issues.append(f"Unclosed <main> tag contains extremely short content ({main_text_len} characters)")
    else:
        # No main tag at all
        pass

    # 4. Check for unclosed <main> tag
    if '<main' in content.lower() and '</main>' not in content.lower():
        issues.append("Unclosed <main> tag (missing </main>)")

    # 5. Check if it contains the empty main placeholder
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
    
    flagged_pages = []
    for file_path in html_files:
        issues = audit_html_file(file_path)
        if issues:
            flagged_pages.append((file_path, issues))
            
    # Print results grouped by severity
    critical_issues = []
    structural_issues = []
    
    for file_path, issues in flagged_pages:
        # Determine if it's critical (completely blank, placeholders, extremely short text)
        is_critical = False
        for issue in issues:
            if "extremely small" in issue.lower() or "little visible text" in issue.lower() or "empty main placeholder" in issue.lower():
                is_critical = True
                break
        
        if is_critical:
            critical_issues.append((file_path, issues))
        else:
            structural_issues.append((file_path, issues))
            
    print(f"=== CRITICAL ISSUES (Pages that look blank or have no content: {len(critical_issues)}) ===")
    for path, issues in critical_issues:
        print(f"[CRITICAL] {path}")
        for issue in issues:
            print(f"   - {issue}")
        print()
        
    print(f"=== STRUCTURAL WARNINGS (Pages with content but malformed HTML: {len(structural_issues)}) ===")
    print(f"Found {len(structural_issues)} pages with structural warnings (mostly unclosed <main> tags).")
    # Show a few examples
    for path, issues in structural_issues[:5]:
        print(f"[WARNING] {path}")
        for issue in issues:
            print(f"   - {issue}")
        print()
    if len(structural_issues) > 5:
        print(f"... and {len(structural_issues) - 5} more pages with similar warnings.")
        
if __name__ == '__main__':
    main()
