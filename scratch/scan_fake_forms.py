import os
import re
import sys
from bs4 import BeautifulSoup

# Ensure stdout uses UTF-8
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

workspace_dir = r"c:\Users\imran\OneDrive\Desktop\ELB code"
html_files = [f for f in os.listdir(workspace_dir) if f.endswith('.html')]

print(f"Scanning {len(html_files)} HTML files for potential fake/untracked forms...")
print("=" * 80)

fake_forms = []

for fn in sorted(html_files):
    path = os.path.join(workspace_dir, fn)
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()
        
    soup = BeautifulSoup(html, 'html.parser')
    forms = soup.find_all('form')
    
    if not forms:
        continue
        
    for i, form in enumerate(forms):
        form_id = form.get('id', '')
        action = form.get('action', '')
        onsubmit = form.get('onsubmit', '')
        
        # Check if submit is processed in script or action
        is_submitting = False
        
        if action and not action.startswith('#') and 'No Action' not in action:
            is_submitting = True
            
        if onsubmit:
            # Let's check what the onsubmit function does by scanning scripts in this file
            func_match = re.search(r'(\w+)\s*\(', onsubmit)
            if func_match:
                func_name = func_match.group(1)
                # Check if this function defines a fetch/ajax post
                if re.search(rf'function\s+{func_name}\b.*?fetch|function\s+{func_name}\b.*?XMLHttpRequest|function\s+{func_name}\b.*?\$', html, re.S | re.I):
                    is_submitting = True
                elif re.search(rf'async\s+function\s+{func_name}\b.*?fetch|async\s+function\s+{func_name}\b.*?XMLHttpRequest', html, re.S | re.I):
                    is_submitting = True
                    
        # Check if form ID has a submit listener in the scripts
        if not is_submitting and form_id:
            # e.g., document.getElementById('form_id').addEventListener('submit'...)
            listener_pattern = rf'getElementById\(["\']{form_id}["\']\).*?addEventListener\(["\']submit["\']'
            if re.search(listener_pattern, html, re.S | re.I):
                is_submitting = True
                
        if not is_submitting:
            # Check if there is any script containing fetch or submit in the page
            if 'fetch(' in html or 'XMLHttpRequest' in html or '$.ajax' in html or 'submit-lead' in html:
                # E.g., it might have a generic handler or be a valid form that is handled globally
                # Let's inspect further or mark as suspicious
                suspicious = True
            else:
                suspicious = True
            
            fake_forms.append((fn, form_id, action, onsubmit, suspicious))

print(f"Audit complete. Found {len(fake_forms)} forms that might not be sending data:")
for fn, f_id, act, onsub, susp in fake_forms:
    print(f"File: {fn}")
    print(f"  Form ID: {f_id if f_id else 'None'}")
    print(f"  Action:  {act if act else 'None'}")
    print(f"  onsubmit: {onsub if onsub else 'None'}")
    print(f"  Suspicious level: {'HIGH (No fetch/ajax found in page)' if not ('fetch(' in open(os.path.join(workspace_dir, fn), encoding='utf-8', errors='ignore').read()) else 'MEDIUM'}")
    print("-" * 80)
