import os
import re

def interlink_aviation():
    files = [
        'luxury-private-jet-charter.html',
        'private-jet-available-now.html',
        'business-jet-charter.html',
        'corporate-jet-charter.html',
        'private-aircraft-charter.html'
    ]

    css_style = """
        /* Interlinking Hubs */
        .authority-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 3rem;
            margin: 4rem 0;
            padding: 3rem;
            border-top: 1px solid var(--glass-border);
            border-bottom: 1px solid var(--glass-border);
            background: var(--glass);
            border-radius: 20px;
        }
        .authority-col h3 {
            font-size: 1.8rem;
            color: var(--primary-gold);
            margin-top: 0;
            margin-bottom: 1.5rem;
            font-family: 'Cormorant Garamond', serif;
        }
        .authority-col p {
            font-size: 0.95rem;
            color: var(--text-muted);
            margin-bottom: 1.5rem;
        }
        .authority-col ul {
            list-style: none;
            padding: 0;
            margin: 0;
        }
        .authority-col ul li {
            margin-bottom: 1rem;
        }
        .authority-col ul li a {
            color: #fff;
            text-decoration: none;
            font-weight: 600;
            transition: color 0.3s;
        }
        .authority-col ul li a:hover {
            color: var(--primary-gold);
        }
        @media (max-width: 768px) {
            .authority-grid {
                grid-template-columns: 1fr;
                gap: 2rem;
                padding: 2rem;
            }
        }
"""

    html_content = """
        <!-- Interlinking Yacht & Aviation Hubs -->
        <div class="authority-grid">
            <div class="authority-col">
                <h3>✈️ Elite Aviation Authority Hub</h3>
                <p style="font-size: 0.95rem; color: var(--text-muted); margin-bottom: 1.5rem;">Select your optimal charter procurement model or explore direct routes.</p>
                <ul>
                    <li><a href="https://eliteluxurybookings.com/luxury-private-jet-charter/">Luxury Private Jet Charter</a> – Elite Air Sourcing & VIP Concierge</li>
                    <li><a href="https://eliteluxurybookings.com/private-jet-available-now/">Private Jet Available Now</a> – 2-to-4 Hour Rapid Tarmac Dispatch</li>
                    <li><a href="https://eliteluxurybookings.com/business-jet-charter/">Business Jet Charter</a> – Premium Corporate Charter Flights</li>
                    <li><a href="https://eliteluxurybookings.com/corporate-jet-charter/">Corporate Jet Charter</a> – Scaled Enterprise Fleet Sourcing</li>
                    <li><a href="https://eliteluxurybookings.com/private-aircraft-charter/">Private Aircraft Charter</a> – Global Jet Sourcing & Rentals</li>
                </ul>
            </div>
            <div class="authority-col">
                <h3>⚓ Private Yacht Authority Hub</h3>
                <p style="font-size: 0.95rem; color: var(--text-muted); margin-bottom: 1.5rem;">Seamless maritime pairings for Amalfi Coast, Monaco, and French Riviera arrivals.</p>
                <ul>
                    <li><a href="https://eliteluxurybookings.com/amalfi-coast-yacht-rental/">Amalfi Coast Yacht Rental</a> – 7 Best Deals & Custom Capri Charters</li>
                    <li><a href="https://eliteluxurybookings.com/cost-to-charter-superyacht-2026/">Superyacht Cost Guide</a> – Base Rates, APA, Vetting & Fees</li>
                    <li><a href="https://eliteluxurybookings.com/best-mediterranean-yacht-destinations/">Top Mediterranean Destinations</a> – Summer Itinerary Authority</li>
                    <li><a href="https://eliteluxurybookings.com/how-to-rent-superyacht-guide/">Superyacht Booking Guide</a> – Vetting Operators & Broker Tips</li>
                </ul>
            </div>
        </div>
"""

    for fname in files:
        if not os.path.exists(fname):
            print(f"File {fname} not found!")
            continue

        with open(fname, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # 1. Inject CSS Style before </style>
        if '.authority-grid' not in content:
            style_idx = content.find('</style>')
            if style_idx != -1:
                content = content[:style_idx] + css_style + content[style_idx:]
                print(f"[{fname}] Injected local interlinking CSS styles.")

        # Remove existing HTML block if present
        if '<!-- Interlinking Yacht & Aviation Hubs -->' in content:
            start_idx = content.find('<!-- Interlinking Yacht & Aviation Hubs -->')
            end_idx = content.find('<section class="cta-banner">')
            if end_idx == -1:
                end_idx = content.find("<section class='cta-banner'>")
            if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
                content = content[:start_idx] + content[end_idx:]
                print(f"[{fname}] Cleared old interlinking block for update.")

        # 2. Inject HTML Section before <section class="cta-banner">
        cta_idx = content.find('<section class="cta-banner">')
        if cta_idx != -1:
            content = content[:cta_idx] + html_content + content[cta_idx:]
            print(f"[{fname}] Injected structural authority interlinking hubs.")
        else:
            cta_idx = content.find("<section class='cta-banner'>")
            if cta_idx != -1:
                content = content[:cta_idx] + html_content + content[cta_idx:]
                print(f"[{fname}] Injected structural authority interlinking hubs (single quote).")

        with open(fname, 'w', encoding='utf-8') as f:
            f.write(content)

if __name__ == '__main__':
    interlink_aviation()
