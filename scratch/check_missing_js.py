import os

def check_lead_forms():
    html_files = []
    for root, dirs, files in os.walk('.'):
        if '.git' in root or '_archive' in root or 'scratch' in root:
            continue
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
                
    missing_js_count = 0
    total_form_count = 0
    
    for file_path in html_files:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        if 'submitLead(event)' in content:
            total_form_count += 1
            if 'async function submitLead' not in content:
                missing_js_count += 1
                print(f"[MISSING JS] {file_path}")
                
    print(f"\nTotal pages calling submitLead(event): {total_form_count}")
    print(f"Pages missing the 'submitLead' JS function: {missing_js_count}")

if __name__ == '__main__':
    check_lead_forms()
