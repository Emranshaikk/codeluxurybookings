$keywords = @(
    "yacht-charter-ibiza", "yacht-rental-ibiza", "luxury-yacht-ibiza", "ibiza-yacht-hire",
    "yacht-charter-mallorca", "yacht-rental-mallorca", "boat-rental-mallorca-luxury",
    "yacht-charter-formentera", "yacht-charter-french-riviera", "luxury-yacht-monaco",
    "yacht-rental-nice-france", "monaco-yacht-charter", "yacht-charter-cannes",
    "yacht-charter-amalfi-coast", "yacht-rental-capri", "yacht-charter-positano",
    "yacht-charter-sardinia", "yacht-rental-italy-luxury", "italian-riviera-yacht-charter",
    "yacht-charter-mykonos", "yacht-charter-santorini", "greek-islands-yacht-charter",
    "greece-luxury-yacht-hire", "yacht-rental-cyclades", "yacht-charter-dubai",
    "luxury-yacht-dubai-marina", "rent-yacht-dubai-price", "dubai-private-yacht-rental",
    "yacht-hire-dubai-marina", "yacht-charter-maldives", "yacht-charter-miami",
    "yacht-charter-bahamas", "yacht-charter-croatia", "yacht-charter-montenegro",
    "ibiza-to-formentera-yacht-charter", "mallorca-to-ibiza-yacht-charter",
    "mykonos-to-santorini-yacht-charter", "dubai-marina-to-palm-jumeirah-yacht",
    "amalfi-coast-to-capri-yacht-charter", "monaco-to-saint-tropez-yacht-charter",
    "croatia-island-hopping-yacht-charter", "greece-island-yacht-itinerary",
    "sardinia-to-corsica-yacht-charter", "yacht-charter-ibiza-cost",
    "yacht-rental-mallorca-price", "yacht-charter-dubai-price-per-hour",
    "luxury-yacht-charter-cost-mediterranean", "yacht-hire-greece-cost",
    "yacht-charter-amalfi-coast-price", "yacht-rental-mykonos-cost",
    "private-yacht-charter-price-europe", "how-much-does-it-cost-to-rent-a-yacht",
    "yacht-charter-weekly-price", "how-to-charter-a-yacht", "how-to-rent-a-yacht-in-ibiza",
    "how-much-is-yacht-charter-dubai", "how-to-plan-yacht-vacation-mediterranean",
    "when-is-best-time-for-yacht-charter-ibiza", "when-to-visit-amalfi-coast-for-yachting",
    "when-to-book-yacht-dubai", "when-is-yacht-season-mediterranean",
    "where-to-rent-yacht-in-ibiza", "where-to-charter-yacht-in-greece",
    "where-to-start-yacht-charter-amalfi-coast", "where-are-best-yacht-destinations-europe",
    "luxury-yacht-experience-ibiza", "private-yacht-party-ibiza", "yacht-wedding-dubai",
    "yacht-honeymoon-greece", "yacht-birthday-party-dubai", "yacht-charter-with-chef",
    "yacht-charter-with-crew", "all-inclusive-yacht-charter", "catamaran-charter-mediterranean",
    "superyacht-charter-europe", "mega-yacht-rental-dubai", "sailing-yacht-charter-greece",
    "motor-yacht-charter-ibiza", "luxury-catamaran-charter",
    "7-day-yacht-charter-mediterranean-itinerary", "ibiza-yacht-itinerary-3-days",
    "amalfi-coast-yacht-itinerary", "greek-islands-yacht-route-guide",
    "best-yacht-destinations-europe", "yacht-charter-vs-cruise", "yacht-vs-boat-rental-difference",
    "private-yacht-vs-hotel-stay", "yacht-charter-vs-villa-vacation",
    "book-yacht-charter-ibiza", "rent-luxury-yacht-dubai", "hire-private-yacht-greece",
    "book-yacht-mediterranean", "yacht-charter-deals-europe"
)

$domain = "https://eliteluxurybookings.com"
$sitemapXml = '<?xml version="1.0" encoding="UTF-8"?>' + "`n"
$sitemapXml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "`n"

foreach ($slug in $keywords) {
    $sitemapXml += "  <url>`n"
    $sitemapXml += "    <loc>$domain/$slug</loc>`n"
    $sitemapXml += "    <changefreq>weekly</changefreq>`n"
    $sitemapXml += "    <priority>0.8</priority>`n"
    $sitemapXml += "  </url>`n"
}

$sitemapXml += "</urlset>"
Set-Content "sitemap_yacht.xml" $sitemapXml
