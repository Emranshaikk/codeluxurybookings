import os
import re

SUBMIT_LEAD_JS = """
    <script>
        const endpoint = 'https://eliteluxurybookings.com/submit-lead.php';
        async function submitLead(event) {
            event.preventDefault();
            const btn = event.target.querySelector('button[type="submit"]');
            const form = event.target;
            const originalBtnText = btn.innerText;
            
            btn.innerText = 'SECURELY SENDING...';
            btn.disabled = true;
            
            const formData = new FormData(form);
            try {
                await fetch(endpoint, {
                    method: 'POST',
                    body: formData
                });
                window.location.href = '/thank-you.html';
            } catch (error) {
                console.error(error);
                alert('Connection issue. Please connect directly with your concierge via WhatsApp.');
            } finally {
                btn.innerText = originalBtnText;
                btn.disabled = false;
            }
        }
    </script>
"""

def fix_file_js(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        
    if 'submitLead(event)' in content and 'async function submitLead' not in content:
        print(f"Injecting submitLead JS in: {file_path}")
        
        # Check if </body> exists
        body_close_match = re.search(r'</body>', content, re.IGNORECASE)
        if body_close_match:
            insert_idx = body_close_match.start()
            new_content = content[:insert_idx] + SUBMIT_LEAD_JS + "\n" + content[insert_idx:]
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True
    return False

def main():
    html_files = []
    for root, dirs, files in os.walk('.'):
        if '.git' in root or '_archive' in root or 'scratch' in root:
            continue
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
                
    fixed_count = 0
    for file_path in html_files:
        if fix_file_js(file_path):
            fixed_count += 1
            
    print(f"\nCompleted! Injected submitLead JS in {fixed_count} files.")

if __name__ == '__main__':
    main()
