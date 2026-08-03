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

# Definition of the standard submitLead block for pages missing it
standard_submit_lead_script = """
    <!-- Operational submitLead and escapeHtml Functions -->
    <script>
    function escapeHtml(text) {
        if (!text) return '';
        return text.toString()
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;");
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
        const formType = formData.get('form_type') || formData.get('_target') || 'Private Jet Lead';

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

# Definition of the working handleInquirySubmit for island pages
standard_handle_inquiry_script = """
    <!-- Operational handleInquirySubmit and escapeHtml Functions -->
    <script>
    function escapeHtml(text) {
        if (!text) return '';
        return text.toString()
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;");
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

# 1. Update the 5 broken jet files
broken_jet_files = [
    "premium-jet-charter.html",
    "private-aircraft-charter.html",
    "private-aviation-service.html",
    "private-island-honeymoon-rental.html",
    "ultra-luxury-jet-charter.html"
]

print("Fixing 5 broken private jet pages...")
for fn in broken_jet_files:
    path = os.path.join(workspace_dir, fn)
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    if "submitLead" in content and "async function submitLead" in content:
        print(f"  {fn} already has submitLead defined.")
        continue
        
    # Inject before </body>
    if "</body>" in content:
        new_content = content.replace("</body>", standard_submit_lead_script + "\n</body>")
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"  Successfully fixed broken form in {fn}")

print("=" * 80)

# 2. Update the 6 fake island files
fake_island_files = [
    "all-inclusive-private-island-rental.html",
    "bahamas-private-island-rental.html",
    "caribbean-private-island-rental.html",
    "exclusive-private-island-rental.html",
    "luxury-private-island-rental.html",
    "maldives-private-island-rental.html"
]

print("Fixing 6 fake/non-submitting private island pages...")
for fn in fake_island_files:
    path = os.path.join(workspace_dir, fn)
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        
    # Replace existing handleInquirySubmit script block
    # Pattern to match: <script> ... function handleInquirySubmit ... </script>
    pattern = r'<script>\s*function\s+handleInquirySubmit\(event\).*?</script>'
    
    if re.search(pattern, content, re.S):
        new_content = re.sub(pattern, standard_handle_inquiry_script.strip(), content, flags=re.S)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"  Successfully fixed fake form in {fn}")
    else:
        # If not matching exactly, try a looser pattern or inject before </body>
        if "handleInquirySubmit" in content:
            # Replace the function block manually or search looser regex
            looser_pattern = r'function\s+handleInquirySubmit\(event\)\s*\{(?:[^{}]*|\{[^{}]*\})*\}'
            new_content = re.sub(looser_pattern, "/* replaced */", content, flags=re.S)
            # Inject standard script
            new_content = new_content.replace("</body>", standard_handle_inquiry_script + "\n</body>")
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"  Successfully replaced loose script and fixed fake form in {fn}")
        else:
            new_content = content.replace("</body>", standard_handle_inquiry_script + "\n</body>")
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"  Successfully injected handleInquirySubmit in {fn}")

print("=" * 80)

# 3. Add GA4 event tracking to existing functional form scripts
functional_pages = [
    "index.html",
    "contact.html",
    "luxury-villa-rentals.html",
    "luxury-yacht-rentals.html",
    "elite-private-jet-charter.html",
    "private-boat-trip-mallorca-to-formentera.html",
    "mallorca-to-ibiza-private-boat.html"
]

print("Injecting GA4 conversion tracking into functional form scripts...")

ga4_snippet = """
        // GA4 Lead Conversion Tracking
        try {
            const serviceInterest = (typeof formData !== 'undefined') ? (formData.get('interest') || formData.get('service') || formData.get('form_type') || 'General') : 'General';
            if (typeof gtag === 'function') {
                gtag('event', 'generate_lead', {
                    'form_location': window.location.href,
                    'service_interest': serviceInterest
                });
            }
        } catch(ga_err) { console.error('GA4 tracking error:', ga_err); }
"""

for fn in functional_pages:
    path = os.path.join(workspace_dir, fn)
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        
    if "generate_lead" in content and "form_location" in content:
        print(f"  {fn} already has GA4 generate_lead event configured.")
        continue
        
    # We want to inject this inside the try-catch block right after Promise.all
    # E.g. search for: await Promise.all([tgPromise, emailPromise]);
    # Or search for: await sendLeadToDestinations(formData, formType);
    
    if "await Promise.all([tgPromise, emailPromise]);" in content:
        # Prepend or append to Promise.all success
        target = "await Promise.all([tgPromise, emailPromise]);"
        replacement = target + ga4_snippet
        content = content.replace(target, replacement)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  Successfully injected GA4 event in {fn} success block (Promise.all)")
        
    elif "await sendLeadToDestinations(formData, formType);" in content:
        target = "await sendLeadToDestinations(formData, formType);"
        replacement = target + ga4_snippet
        content = content.replace(target, replacement)
        # Also handle other occurrences in index.html (like the lead magnet form)
        content = content.replace("await sendLeadToDestinations(formData, 'Lead Magnet');", "await sendLeadToDestinations(formData, 'Lead Magnet');" + ga4_snippet)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  Successfully injected GA4 event in {fn} success block (sendLeadToDestinations)")
        
    else:
        print(f"  [WARNING] Could not locate submission success anchor in {fn}")

print("=" * 80)
print("Forms and GA4 tracking upgrades complete.")
