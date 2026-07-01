# Task Tracker: New York to Aspen Private Jet Cost Optimization

- [x] **Section 1: Bug Fixes**
  - [x] Remove all client-side Telegram bot tokens, chat IDs, and fetch calls
  - [x] Fix the `/submit-lead.php` AJAX post logic (send to submit-lead.php instead of direct Telegram calls)
  - [x] Consolidate duplicate `toggleMobileMenu()` declarations
  - [x] Repair `twitter:description` meta tag closing brackets
  - [x] Replace broken emojis with proper Font Awesome icons or UTF-8 characters
  - [x] Load Font Awesome via standard CDN Link stylesheet

- [x] **Section 2: Conversion Rate Optimization & UX**
  - [x] Pre-fill "Departure" as "New York (KTEB)" and "Destination" as "Aspen (KASE)"
  - [x] Limit `required` inputs in the form to only Name + Email
  - [x] Create inline thank-you state on successful submission with WhatsApp button
  - [x] Add alternative email messaging under the CTA
  - [x] Unify all currency representations to USD ($)
  - [x] Add dynamic JS Peak Season/Year-round banner with gold design
  - [x] Upgrade testimonials to feel verifiable (stars, company types, dates, badges, route-specific)
  - [x] Add sticky bottom mobile CTA bar dismissible with sessionStorage

- [x] **Section 3: Article Content (1,400–1,600 Words)**
  - [x] H2: The True Cost of Flying New York to Aspen by Private Jet (Pricing table, USD estimates)
  - [x] H2: Why Aspen-Pitkin (KASE) Demands a Specialist Operator (Altitude, runway, convective wind, weight restrictions, FBOs)
  - [x] H3: New York FBO Options: Teterboro vs. White Plains (Listing Signature, Atlantic, Jet Aviation, Meridian vs. KHPN)
  - [x] H2: Seasonal Demand: Ski Season vs. Summer in Aspen (Winter peak slots, Summer festivals, shoulder seasons)
  - [x] H2: Empty Legs: New York to Aspen at Significant Discount (Repositioning flights, savings, scheduling)
  - [x] H2: Safety, Certification & Operator Standards (ARGUS, Wyvern, KASE approach certifications, EBAA, BACA)
  - [x] H2: Frequently Asked Questions (8 questions mirroring schema)

- [x] **Section 4: SEO & Schema Upgrades**
  - [x] Add HowTo schema block
  - [x] Expand FAQs to 8 items in both visible HTML and FAQPage schema
  - [x] Align visible breadcrumbs to JSON-LD BreadcrumbList schema pointing to `/elite-private-jet-charter/`
  - [x] Add 6-card "Related Routes" block (Aspen/LA, NY/Miami, NY/LA, Aspen/Miami, NY/Jackson Hole, NY/London)
  - [x] Update Product AggregateOffer prices to $18,000 - $75,000

- [x] **Section 5: Code Quality & Accessibility**
  - [x] Single consolidated script block inside DOMContentLoaded listener
  - [x] Enhance form accessibility (labels, focus styles, aria attributes)
  - [x] Standardize alt tags for images and decorative icon tags
  - [x] Add skip-to-content link
  - [x] Wrap pricing table in scroll container

- [x] **Section 6: Global Mobile Optimization & Lead Security Audit**
  - [x] Enforce html, body horizontal scroll lock globally across 209 files
  - [x] Wrap overflowing header tag strips and jet selector buttons responsive layouts
  - [x] Resolve squished lead forms by scaling mobile paddings to 2.5rem/1.5rem
  - [x] Create server-side `submit-lead.php` relay endpoint with Telegram Bot Token + Chat ID
  - [x] Migrate all client-side exposed Telegram bot API requests to point to `/submit-lead.php` in 148 files
  - [x] Perform validation checks to verify complete token removal from client-side code
