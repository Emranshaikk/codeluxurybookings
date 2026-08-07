import os
import re
import sys

# Ensure stdout uses UTF-8
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

workspace_dir = r"c:\Users\imran\OneDrive\Desktop\ELB code"
html_files = [f for f in os.listdir(workspace_dir) if f.endswith('.html')]

# Definitions of standard scripts
submit_lead_block = """
    <!-- Standard E-E-A-T & GA4 submitLead Handler -->
    <script>
    if (typeof escapeHtml !== 'function') {
        window.escapeHtml = function(text) {
            if (!text) return '';
            return text.toString()
                .replace(/&/g, "&amp;")
                .replace(/</g, "&lt;")
                .replace(/>/g, "&gt;");
        };
    }

    async function submitLead(event) {
        event.preventDefault();
        const form = event.target;
        const btn = form.querySelector('button[type="submit"]') || form.querySelector('button');
        const originalBtnText = btn ? btn.innerText : 'Submit';

        if (btn) {
            btn.innerText = 'SECURELY SENDING...';
            btn.disabled = true;
        }

        const formData = new FormData(form);
        const formType = formData.get('form_type') || formData.get('_target') || 'General Lead';

        // Telegram message formatting
        let message = `🚀 <b>New Elite Lead Received!</b>\\n\\n`;
        message += `<b>Source:</b> ${escapeHtml(formType)}\\n\\n`;

        const fields = {
            name: '👤 Name',
            phone: '📞 Phone',
            email: '📧 Email',
            route: '✈️ Route',
            departure: '🛫 Departure',
            destination: '🛬 Destination',
            date: '📅 Date',
            passengers: '👥 Passengers',
            service: '💼 Service',
            requirements: '📝 Requirements',
            message: '💬 Message',
            budget: '💰 Budget',
            whatsapp_pref: '💬 WhatsApp Pref'
        };

        for (const [key, label] of Object.entries(fields)) {
            const val = formData.get(key);
            if (val) {
                message += `<b>${label}:</b> ${escapeHtml(val)}\\n`;
            }
        }

        for (const [key, val] of formData.entries()) {
            if (!fields[key] && !['form_type', '_redirect', '_target', '_subject', '_cc'].includes(key) && val) {
                const formattedKey = key.charAt(0).toUpperCase() + key.slice(1);
                message += `<b>${formattedKey}:</b> ${escapeHtml(val)}\\n`;
            }
        }
        message += `\\n🕒 ${new Date().toISOString().replace('T', ' ').substr(0, 19)} UTC`;

        // 1. Send to Telegram
        const tgPromise = fetch('/submit-lead.php', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                chat_id: '5875175296',
                text: message,
                parse_mode: 'HTML'
            })
        }).then(r => r.json()).catch(err => ({ ok: false, error: err }));

        // 2. Send to Email via Formsubmit.co
        const formObject = {};
        formData.forEach((value, key) => {
            if (!['_redirect', '_cc', '_subject'].includes(key)) {
                formObject[key] = value;
            }
        });
        formObject['_subject'] = formData.get('_subject') || `New Lead: ${formType}`;

        const emailPromise = fetch('https://formsubmit.co/ajax/contactshaikk@gmail.com', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formObject)
        }).then(r => r.json()).catch(err => ({ success: false, error: err }));

        try {
            await Promise.all([tgPromise, emailPromise]);
            
            // --- GA4 generate_lead conversion tracking ---
            const serviceInterest = formData.get('interest') || formData.get('service') || formType;
            if (typeof gtag === 'function') {
                gtag('event', 'generate_lead', {
                    'form_location': window.location.href,
                    'service_interest': serviceInterest
                });
            }
            
            window.location.href = '/thank-you.html';
        } catch (error) {
            console.error(error);
            alert('Connection issue. Please connect directly with your concierge via WhatsApp.');
        } finally {
            if (btn) {
                btn.innerText = originalBtnText;
                btn.disabled = false;
            }
        }
    }
    </script>
"""

handle_inquiry_block = """
    <!-- Standard E-E-A-T & GA4 handleInquirySubmit Handler -->
    <script>
    if (typeof escapeHtml !== 'function') {
        window.escapeHtml = function(text) {
            if (!text) return '';
            return text.toString()
                .replace(/&/g, "&amp;")
                .replace(/</g, "&lt;")
                .replace(/>/g, "&gt;");
        };
    }

    async function handleInquirySubmit(event) {
        event.preventDefault();
        const form = event.target;
        const btn = form.querySelector('button[type="submit"]') || form.querySelector('button');
        const originalBtnText = btn ? btn.innerText : 'Submit Request';

        if (btn) {
            btn.innerText = 'SENDING...';
            btn.disabled = true;
        }

        const formData = new FormData(form);
        const formType = formData.get('form_type') || 'Private Island Inquiry';

        // Telegram message formatting
        let message = `🚀 <b>New Elite Lead Received!</b>\\n\\n`;
        message += `<b>Source:</b> ${escapeHtml(formType)}\\n\\n`;

        const fields = {
            name: '👤 Name',
            phone: '📞 Phone',
            email: '📧 Email',
            island: '🏝️ Island Preferred',
            date: '📅 Date',
            guests: '👥 Guests',
            requirements: '📝 Requirements',
            message: '💬 Message'
        };

        for (const [key, label] of Object.entries(fields)) {
            const val = formData.get(key);
            if (val) {
                message += `<b>${label}:</b> ${escapeHtml(val)}\\n`;
            }
        }

        for (const [key, val] of formData.entries()) {
            if (!fields[key] && !['form_type', '_redirect', '_target', '_subject', '_cc'].includes(key) && val) {
                const formattedKey = key.charAt(0).toUpperCase() + key.slice(1);
                message += `<b>${formattedKey}:</b> ${escapeHtml(val)}\\n`;
            }
        }
        message += `\\n🕒 ${new Date().toISOString().replace('T', ' ').substr(0, 19)} UTC`;

        // 1. Send to Telegram
        const tgPromise = fetch('/submit-lead.php', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                chat_id: '5875175296',
                text: message,
                parse_mode: 'HTML'
            })
        }).then(r => r.json()).catch(err => ({ ok: false, error: err }));

        // 2. Send to Email via Formsubmit.co
        const formObject = {};
        formData.forEach((value, key) => {
            if (!['_redirect', '_cc', '_subject'].includes(key)) {
                formObject[key] = value;
            }
        });
        formObject['_subject'] = `New Island Lead: ${formType}`;

        const emailPromise = fetch('https://formsubmit.co/ajax/contactshaikk@gmail.com', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formObject)
        }).then(r => r.json()).catch(err => ({ success: false, error: err }));

        try {
            await Promise.all([tgPromise, emailPromise]);
            
            // --- GA4 generate_lead conversion tracking ---
            if (typeof gtag === 'function') {
                gtag('event', 'generate_lead', {
                    'form_location': window.location.href,
                    'service_interest': 'Private Island'
                });
            }
            
            // Hide form and show success message
            form.style.display = 'none';
            const msgEl = document.getElementById('formSuccessMessage') || document.getElementById('successMessage');
            if (msgEl) {
                msgEl.style.display = 'block';
            } else {
                window.location.href = '/thank-you.html';
            }
        } catch (error) {
            console.error(error);
            alert('Connection issue. Please connect directly with your concierge via WhatsApp.');
        } finally {
            if (btn) {
                btn.innerText = originalBtnText;
                btn.disabled = false;
            }
        }
    }
    </script>
"""

handle_enquiry_block = """
    <!-- Standard E-E-A-T & GA4 handleEnquiry Handler -->
    <script>
    if (typeof escapeHtml !== 'function') {
        window.escapeHtml = function(text) {
            if (!text) return '';
            return text.toString()
                .replace(/&/g, "&amp;")
                .replace(/</g, "&lt;")
                .replace(/>/g, "&gt;");
        };
    }

    async function handleEnquiry(event, suffix) {
        event.preventDefault();
        const form = event.target;
        const btn = form.querySelector('button[type="submit"]') || form.querySelector('button');
        const originalBtnText = btn ? btn.innerText : 'Submit Request';

        if (btn) {
            btn.innerText = 'SENDING...';
            btn.disabled = true;
        }

        const formData = new FormData(form);
        const formType = formData.get('form_type') || 'Solar Eclipse Yacht Inquiry';

        // Telegram message formatting
        let message = `🚀 <b>New Elite Lead Received!</b>\\n\\n`;
        message += `<b>Source:</b> ${escapeHtml(formType)}\\n\\n`;

        const fields = {
            name: '👤 Name',
            contact: '📞 Contact Details',
            guests: '👥 Guests',
            port: '⚓ Preferred Port'
        };

        for (const [key, label] of Object.entries(fields)) {
            const val = formData.get(key);
            if (val) {
                message += `<b>${label}:</b> ${escapeHtml(val)}\\n`;
            }
        }
        message += `\\n🕒 ${new Date().toISOString().replace('T', ' ').substr(0, 19)} UTC`;

        // 1. Send to Telegram
        const tgPromise = fetch('/submit-lead.php', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                chat_id: '5875175296',
                text: message,
                parse_mode: 'HTML'
            })
        }).then(r => r.json()).catch(err => ({ ok: false, error: err }));

        // 2. Send to Email via Formsubmit.co
        const formObject = {};
        formData.forEach((value, key) => {
            if (!['_redirect', '_cc', '_subject'].includes(key)) {
                formObject[key] = value;
            }
        });
        formObject['_subject'] = `New Solar Eclipse Lead: ${formType}`;

        const emailPromise = fetch('https://formsubmit.co/ajax/contactshaikk@gmail.com', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formObject)
        }).then(r => r.json()).catch(err => ({ success: false, error: err }));

        try {
            await Promise.all([tgPromise, emailPromise]);
            
            // --- GA4 generate_lead conversion tracking ---
            if (typeof gtag === 'function') {
                gtag('event', 'generate_lead', {
                    'form_location': window.location.href,
                    'service_interest': 'Solar Eclipse Yacht'
                });
            }
            
            form.style.display = 'none';
            // Show success message
            const successSibling = form.nextElementSibling;
            if (successSibling && successSibling.id && successSibling.id.includes('success')) {
                successSibling.style.display = 'block';
            } else {
                const parent = form.parentNode;
                const newMsg = document.createElement('div');
                newMsg.innerHTML = '<h3 class="serif gold-text" style="font-size:2rem; margin-bottom:1rem;">Inquiry Secured</h3><p>Our elite desk has received your brief. A coordinator will be in touch shortly.</p>';
                newMsg.style.textAlign = 'center';
                newMsg.style.padding = '2rem 0';
                parent.appendChild(newMsg);
            }
        } catch (error) {
            console.error(error);
            alert('Connection issue. Please connect directly with your concierge via WhatsApp.');
        } finally {
            if (btn) {
                btn.innerText = originalBtnText;
                btn.disabled = false;
            }
        }
    }
    </script>
"""

print(f"Scanning all {len(html_files)} files for missing handler functions...")
print("=" * 80)

modified_count = 0

for fn in sorted(html_files):
    path = os.path.join(workspace_dir, fn)
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()
        
    original_html = html
    
    # 1. Check submitLead
    if 'onsubmit="submitLead(event)"' in html or "onsubmit='submitLead(event)'" in html:
        if not re.search(r'function\s+submitLead\b', html):
            if "submitLead" not in html or html.count("submitLead") == 1:
                # Inject standard submitLead
                if "</body>" in html:
                    html = html.replace("</body>", submit_lead_block.strip() + "\n</body>")
                    
    # 2. Check handleInquirySubmit
    if 'onsubmit="handleInquirySubmit(event)"' in html or "onsubmit='handleInquirySubmit(event)'" in html:
        if not re.search(r'function\s+handleInquirySubmit\b', html):
            if "handleInquirySubmit" not in html or html.count("handleInquirySubmit") == 1:
                # Inject standard handleInquirySubmit
                if "</body>" in html:
                    html = html.replace("</body>", handle_inquiry_block.strip() + "\n</body>")
                    
    # 3. Check handleEnquiry
    if 'handleEnquiry(' in html:
        if not re.search(r'function\s+handleEnquiry\b', html):
            # Inject standard handleEnquiry
            if "</body>" in html:
                html = html.replace("</body>", handle_enquiry_block.strip() + "\n</body>")
                
    if html != original_html:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        modified_count += 1
        print(f"Fixed missing form handler script(s) in {fn}")

print("-" * 80)
print(f"Completed! Fixed missing form handlers in {modified_count} files.")
