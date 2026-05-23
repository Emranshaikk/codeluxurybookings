import os
import re

# Configuration
DIRECTORY = r'c:\Users\imran\OneDrive\Desktop\ELB code'
FORMSPREE_PATTERN = re.compile(r'<form\s+action="https://formspree\.io/f/xwvwanlj"\s+method="POST"', re.IGNORECASE)
ENDPOINT_JS = "const endpoint = 'https://eliteluxurybookings.com/submit-lead.php';"
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

def update_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if FORMSPREE_PATTERN.search(content):
        print(f"Updating {os.path.basename(filepath)}...")
        
        # 1. Update the form tag
        new_content = FORMSPREE_PATTERN.sub('<form id="leadForm" onsubmit="submitLead(event)"', content)
        
        # 2. Check if script already exists, if not append before </body>
        if 'submitLead(event)' in new_content and 'async function submitLead' not in new_content:
            if '</body>' in new_content:
                new_content = new_content.replace('</body>', SUBMIT_LEAD_JS + '\n</body>')
            else:
                new_content += SUBMIT_LEAD_JS
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

def main():
    count = 0
    for filename in os.listdir(DIRECTORY):
        if filename.endswith('.html'):
            if update_file(os.path.join(DIRECTORY, filename)):
                count += 1
    print(f"Finished. Updated {count} files.")

if __name__ == "__main__":
    main()
