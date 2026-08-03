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

files = [
    "index.html",
    "contact.html",
    "luxury-villa-rentals.html",
    "luxury-yacht-rentals.html",
    "elite-private-jet-charter.html",
    "private-boat-trip-mallorca-to-formentera.html",
    "mallorca-to-ibiza-private-boat.html"
]

workspace_dir = r"c:\Users\imran\OneDrive\Desktop\ELB code"

print("Auditing form submission mechanisms across pages...")
print("=" * 80)

for fn in files:
    path = os.path.join(workspace_dir, fn)
    if not os.path.exists(path):
        print(f"File not found: {fn}")
        continue
        
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()
        
    soup = BeautifulSoup(html, 'html.parser')
    forms = soup.find_all('form')
    
    print(f"File: {fn} (Found {len(forms)} forms)")
    
    for i, form in enumerate(forms):
        form_id = form.get('id', 'No ID')
        action = form.get('action', 'No Action')
        onsubmit = form.get('onsubmit', 'No onsubmit attribute')
        
        # Let's search the HTML content for scripts associated with form submission
        # Check if there is an event listener or submit function in scripts
        submit_functions_found = []
        if onsubmit != 'No onsubmit attribute':
            # find the function call
            func_match = re.search(r'(\w+)\s*\(', onsubmit)
            if func_match:
                func_name = func_match.group(1)
                # Find script lines defining this function
                func_def_pattern = rf'async\s+function\s+{func_name}\b|function\s+{func_name}\b'
                func_def_match = re.search(func_def_pattern, html)
                if func_def_match:
                    # extract the surrounding script block or function body
                    start_idx = func_def_match.start()
                    snippet = html[start_idx:start_idx + 1000]
                    submit_functions_found.append((func_name, snippet))
        
        print(f"  Form {i+1}: ID={form_id} | Action={action} | onsubmit={onsubmit}")
        if submit_functions_found:
            for name, snip in submit_functions_found:
                print(f"    Script function '{name}' starts with:")
                # print lines from snippet
                for line in snip.split('\n')[:15]:
                    print(f"      {line.strip()[:100]}")
        else:
            # Let's search script tag for "submit" or "fetch" or "XMLHttpRequest" related to the form
            js_snippets = re.findall(r'[^;]*\b' + re.escape(form_id) + r'\b[^;]*', html)
            if js_snippets:
                print("    JavaScript matches for form ID:")
                for js in js_snippets[:5]:
                    print(f"      - {js.strip()[:100]}")
                    
    print("-" * 80)
