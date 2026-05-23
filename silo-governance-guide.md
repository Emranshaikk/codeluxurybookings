# Elite Luxury Bookings: Silo Governance & Maintenance Guide

To maintain your #1 rankings and ensure the "Waterfall Silo" doesn't break as you scale to 500+ pages, follow these strict rules for every new piece of content.

## 1. The "New Route" Checklist
Whenever you add a new route (e.g., *Paris to New York*):

- [ ] **Naming Convention**: Use the format `{city1}-to-{city2}-private-jet-cost.html`.
- [ ] **Breadcrumbs**: Add the top-level breadcrumb immediately after the `<body>` tag:
  `Home > Private Jets > [City] Routes > [Route Name]`
- [ ] **City Hub Link**: Ensure the page has a clear link back to its specific City Hub (e.g., `/paris-private-jet-routes/`).
- [ ] **Master Guide Link**: Link back to the main `/private-jet-booking-guide/`.
- [ ] **Conversion Link**: Every page must have a button or link to the **Pixel Page** (`/request-quote/`).
- [ ] **Update the Hub**: Go to the **City Hub** (e.g., `paris-private-jet-routes.html`) and add the new link to the "Popular Routes" grid.
- [ ] **Update the Global Silo**: Add the link to the relevant city section in `global-route-silo.html`.

## 2. Internal Linking Rules (The "Silo Shield")
To prevent "Link Juice" from leaking into unrelated areas:

- **Rule 1: No Random Jumping**: A London-to-Paris page should **never** link to a Dallas-to-Miami page. Only link to routes starting from the **same departure city**.
- **Rule 2: The Upward Flow**: Always link "Up" the chain (Route -> Hub -> Master Guide).
- **Rule 3: Anchor Text Precision**: 
  - When linking to a **City Hub**, use: *"Private jets from [City]"*.
  - When linking to a **Route Page**, use: *"[City1] to [City2] private jet cost"*.

## 3. Blog Integration Strategy
Blog posts are "Fuel" for your silos.

- **Topic Selection**: Write about specific city airports or "How to fly from [City]".
- **Linking**: A blog post about "London's Private Airports" should link to the **London City Hub** and its most popular **Route Pages**.
- **CTA**: Every blog post should link to the **Master Booking Guide**.

## 4. Scaling to 500+ Pages
As you grow, the `global-route-silo.html` will become your most important technical SEO asset.

- **Regional Grouping**: If you get 20+ cities, group the cities by Continent (Europe, Middle East, Americas) within the Global Silo.
- **Automated Sitemaps**: Ensure your `sitemap.xml` reflects this hierarchy.

## 5. Summary of the URL Hierarchy
1.  **Root**: `index.html`
2.  **Pillar**: `private-jet-booking-guide.html`
3.  **Directory**: `global-route-silo.html`
4.  **Hub**: `{city}-private-jet-routes.html`
5.  **Terminal**: `{city}-to-{city}-private-jet-cost.html`

> [!TIP]
> **Always use a Master Template.** I have created a `fragments/city_hub_template.html`. Use this for any new city you launch to ensure the design and SEO tokens remain 100% consistent.
