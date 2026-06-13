import os
import re

# Standardized Footer Block
FOOTER_BLOCK = """
    <!-- Elite Intelligence Hubs -->
    <div class="intel-hub-section">
        <div class="container" style="max-width: 1200px;">
            <div class="intel-hub-grid">
                <div class="intel-hub-card">
                    <h5>Aviation Intelligence</h5>
                    <div class="intel-hub-links">
                        <a href="https://eliteluxurybookings.com/private-jet-charter-cost-estimator/">Jet Cost Estimator</a>
                        <a href="https://eliteluxurybookings.com/heavy-jet-vs-light-jet-charter/">Jet Class Analysis</a>
                        <a href="https://eliteluxurybookings.com/empty-leg-flights-guide/">Empty Leg Mastery</a>
                    </div>
                </div>
                <div class="intel-hub-card">
                    <h5>Maritime Intelligence</h5>
                    <div class="intel-hub-links">
                        <a href="https://eliteluxurybookings.com/cost-to-charter-superyacht-2026/">Yacht Charter Costs</a>
                        <a href="https://eliteluxurybookings.com/yacht-charter-apa-guide/">APA Protocol</a>
                        <a href="https://eliteluxurybookings.com/best-mediterranean-yacht-destinations/">Mediterranean Guide</a>
                    </div>
                </div>
                <div class="intel-hub-card">
                    <h5>Villa Intelligence</h5>
                    <div class="intel-hub-links">
                        <a href="https://eliteluxurybookings.com/ultimate-luxury-villa-rental-guide/">Villa Guide 2026</a>
                        <a href="https://eliteluxurybookings.com/how-to-book-luxury-villa-guide/">Booking Protocol</a>
                        <a href="https://eliteluxurybookings.com/villa-vs-luxury-hotel-comparison/">Villa vs Hotel</a>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Master Footer -->
    <footer class="footer">
        <div class="container" style="max-width: 1200px;">
            <div class="footer-grid">
                <div class="footer-brand">
                    <h2>Elite Luxury <span class="gold-text">Bookings</span></h2>
                    <p>The definitive global authority for private aviation procurement, maritime coordination, and exclusive estate coordination.</p>
                    <div class="footer-socials">
                        <a href="https://www.facebook.com/eliteluxurybookings"><i class="fab fa-facebook"></i></a>
                        <a href="https://www.instagram.com/eliteluxurybookings"><i class="fab fa-instagram"></i></a>
                        <a href="https://www.linkedin.com/company/elite-luxury-bookings/"><i class="fab fa-linkedin"></i></a>
                        <a href="https://x.com/eliteluxuryb"><i class="fab fa-x-twitter"></i></a>
                    </div>
                </div>
                <div class="footer-col">
                    <h4>Pillar Services</h4>
                    <ul>
                        <li><a href="https://eliteluxurybookings.com/elite-private-jet-charter/">Private Jet Charter</a></li>
                        <li><a href="https://eliteluxurybookings.com/luxury-yacht-rentals/">Luxury Yacht Charter</a></li>
                        <li><a href="https://eliteluxurybookings.com/luxury-villa-rentals/">Luxury Villa Rentals</a></li>
                    </ul>
                </div>
                <div class="footer-col">
                    <h4>Company</h4>
                    <ul>
                        <li><a href="https://eliteluxurybookings.com/about/">About Our Mission</a></li>
                        <li><a href="https://eliteluxurybookings.com/contact/">Global Concierge</a></li>
                        <li><a href="https://eliteluxurybookings.com/privacy/">Privacy Protocol</a></li>
                    </ul>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2026 Elite Luxury Bookings. All Rights Reserved.</p>
                <div class="footer-legal">
                    <a href="https://eliteluxurybookings.com/privacy/">Privacy</a>
                    <a href="https://eliteluxurybookings.com/terms/">Terms</a>
                </div>
            </div>
        </div>
    </footer>
"""

FONTAWESOME_LINK = '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">'

files_to_fix = [
    "best-sailing-yacht-charter.html",
    "dubai-private-jet-routes.html",
    "guide-to-mediterranean-yacht-charter.html",
    "london-to-ibiza-private-jet-cost-guide.html",
    "newyork-private-jet-routes.html",
    "paris-private-jet-routes.html",
    "private-jet-booking-guide.html",
    "request-quote.html",
    "thank-you.html"
]

for filename in files_to_fix:
    path = os.path.join(r"c:\Users\imran\OneDrive\Desktop\ELB code", filename)
    if not os.path.exists(path):
        print(f"Skipping {filename}, not found.")
        continue
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add FontAwesome if missing
    if "font-awesome" not in content:
        if "</head>" in content:
            content = content.replace("</head>", f"    {FONTAWESOME_LINK}\n</head>")
    
    # Add Footer before </body> if missing
    if "</footer>" not in content:
        if "</body>" in content:
            content = content.replace("</body>", f"{FOOTER_BLOCK}\n</body>")
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed {filename}")
