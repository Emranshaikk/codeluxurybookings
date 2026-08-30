# Elite Luxury Bookings: 3-Tier Content Hierarchy & Linking Architecture

This document establishes the mandatory 3-Tier structural and interlinking rule for all yacht charter, private jet, and villa destination pages across Elite Luxury Bookings.

---

## 1. The Core 3-Tier Architectural Model

Every geographic cluster must follow a strict 3-tier hierarchy:

```
┌─────────────────────────────────────────────────────────────┐
│ TIER 1: Global Service Pillar Hub (e.g. /luxury-yacht-rentals/) │
└──────────────────────────────┬──────────────────────────────┘
                               │ (Links Down to Regional Hubs)
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ TIER 2: Regional Umbrella Hub (e.g. /french-riviera-yacht-charter/) │
└──────────────────────────────┬──────────────────────────────┘
                               │ (Links Down to Specific City Guides)
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ TIER 3: City / Destination Authority Guides                 │
│  - /monaco-yacht-charter/                                   │
│  - /cannes-yacht-charter/                                   │
│  - (Future: /saint-tropez-yacht-charter/, /antibes-..., etc.)│
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Fundamental Architectural Rules

### Rule 1: No Orphan or Standalone City Pages
* A new city page must **never** be created as an isolated standalone page.
* Every city page must be added as a **Tier 3 child** under an existing or newly created **Tier 2 regional hub**.

### Rule 2: Content Complementarity (No Redundant Duplication)
* A Tier 2 regional hub must **never duplicate granular pricing tables, vessel listings, or local harbor dossiers** that belong to the Tier 3 city guides below it.
* **Tier 2 Role**: Synthesize the regional market, provide multi-destination routes/itineraries, introduce regional vessel categories (e.g., sailing catamarans vs. motor yachts), state broad regional price ranges, and provide clear shortcut cards linking down to Tier 3 pages.
* **Tier 3 Role**: Deliver exhaustive local intelligence, harbor berthing rules (e.g., Port Hercule vs. Fontvieille; Vieux Port vs. Port Canto), local day routes (Lérins Islands, Estérel), event specifics (Grand Prix, Film Festival), and granular day/weekly pricing tables.

### Rule 3: Bidirectional Breadcrumbs & JSON-LD Synchronization
Every Tier 3 city page must feature a 4-level visual breadcrumb and matching `BreadcrumbList` schema:

1. `Home` (`https://eliteluxurybookings.com/`)
2. `Luxury Yachts` (`https://eliteluxurybookings.com/luxury-yacht-rentals/`)
3. `[Region] Yacht Charter` (`https://eliteluxurybookings.com/[region]-yacht-charter/`)
4. `[City] Yacht Charter` (`https://eliteluxurybookings.com/[city]-yacht-charter/`)

---

## 3. Working Example: French Riviera Cluster

| Hierarchy Level | Page URL | Role & Linking Responsibility |
| :--- | :--- | :--- |
| **Tier 1 (Global Hub)** | `https://eliteluxurybookings.com/luxury-yacht-rentals/` | Introduces global yachting curation; links down to `/french-riviera-yacht-charter/` as the regional gateway. |
| **Tier 2 (Regional Hub)** | `https://eliteluxurybookings.com/french-riviera-yacht-charter/` | Covers Côte d'Azur regional overview, sailing/sailboat charter specifics, 7-day Nice-to-Cannes itinerary; links down to Monaco & Cannes; breadcrumb links up to Tier 1. |
| **Tier 3 (City Authority)** | `https://eliteluxurybookings.com/monaco-yacht-charter/` | Deep-dive into Port Hercule, Grand Prix trackside berthing, superyacht tiers; breadcrumbs link up to Tier 2 & Tier 1. |
| **Tier 3 (City Authority)** | `https://eliteluxurybookings.com/cannes-yacht-charter/` | Deep-dive into Lérins Islands, Estérel calanques, day cruisers, Vieux Port vs. Canto; breadcrumbs link up to Tier 2 & Tier 1. |

---

## 4. Checklist for Adding Future Destinations

When creating new city guides (e.g., *Saint-Tropez*, *Antibes*, *Ibiza*, *Amalfi Coast*):
- [ ] Confirm the parent **Tier 2 Regional Hub** exists (or create it first).
- [ ] Add the new city as a destination shortcut on the Tier 2 page.
- [ ] Implement the 4-level visual breadcrumb on the new Tier 3 page linking up to Tier 2 and Tier 1.
- [ ] Implement the 4-level `BreadcrumbList` JSON-LD schema matching the visual breadcrumb.
- [ ] Add horizontal cross-links to sibling Tier 3 city pages where cruising routes overlap.
- [ ] Add the new URL to `sitemap.xml`.
